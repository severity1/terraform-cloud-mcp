"""Terraform Cloud API client

This module provides functions for making requests to the Terraform Cloud API.
It handles authentication, request formatting, response processing, and
specialized redirect handling for Terraform Cloud API's pre-signed URLs.

The client implements custom redirect handling rather than using httpx's
automatic redirect following because:
1. We need to preserve authentication headers when following redirects
2. We need content-type specific processing of redirect responses
3. Terraform Cloud API uses pre-signed URLs that require the original auth headers
"""

import os
import logging
from typing import Optional, Dict, TypeVar, Union, Any
import httpx
from pydantic import BaseModel

TERRAFORM_CLOUD_API_URL = "https://app.terraform.io/api/v2"
DEFAULT_TOKEN = os.getenv("TFC_TOKEN")
logger = logging.getLogger(__name__)

if DEFAULT_TOKEN:
    logger.info("Default token provided (masked for security)")


# Type variable for generic request models
ReqT = TypeVar("ReqT", bound=BaseModel)


async def api_request(
    path: str,
    method: str = "GET",
    token: Optional[str] = None,
    params: Dict[str, Any] = {},
    data: Union[Dict[str, Any], BaseModel] = {},
    external_url: bool = False,
    accept_text: bool = False,
) -> Dict[str, Any]:
    """Make a request to the Terraform Cloud API with proper error handling.

    Creates an authenticated request to the Terraform Cloud API, handling
    authentication, request formatting, and basic error checking.

    Args:
        path: API path to request (without leading slash) or full URL if external_url=True
        method: HTTP method to use (GET, POST, PATCH, DELETE)
        token: API token (defaults to TFC_TOKEN from environment)
        params: Query parameters for the request
        data: JSON payload data (dict or Pydantic model)
        external_url: Whether path is a complete external URL instead of a TFC API path
        accept_text: Whether to accept and return text content instead of JSON

    Returns:
        JSON response from the API as a dictionary or text content if accept_text=True

    Raises:
        HTTPStatusError: For HTTP errors (wrapped by handle_api_errors)
        RequestError: For network/connection issues

    Note:
        This function expects TFC_TOKEN to be set in the environment or .env file
    """
    token = token or DEFAULT_TOKEN
    if not token:
        return {
            "error": "Token is required. Please set the TFC_TOKEN environment variable."
        }

    # Convert Pydantic models to dict
    request_data = (
        data.model_dump(exclude_unset=True) if isinstance(data, BaseModel) else data
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/vnd.api+json",
    }

    async with httpx.AsyncClient(follow_redirects=False) as client:
        url = path if external_url else f"{TERRAFORM_CLOUD_API_URL}/{path}"
        methods = {
            "GET": client.get,
            "POST": client.post,
            "PATCH": client.patch,
            "DELETE": client.delete,
        }
        method_func = methods.get(method)
        if not method_func:
            return {"error": f"Unsupported method: {method}"}

        kwargs = {"headers": headers, "params": params}
        if method in ["POST", "PATCH"]:
            kwargs["json"] = request_data

        try:
            # Cast to proper callable type to satisfy mypy
            response = await method_func(url, **kwargs)  # type: ignore

            # Handle redirects manually
            if response.status_code in (301, 302, 307, 308):
                location = response.headers.get("Location")
                if not location:
                    return {
                        "error": "Redirect received, but no Location header provided."
                    }
                return await handle_redirect(location, headers, client, accept_text)

            # For text responses
            if accept_text:
                return {"content": response.text}

            # Handle 204 No Content responses
            if response.status_code == 204:
                return {"status": "success", "status_code": 204}

            # Handle other success responses
            json_data = response.json()
            # Ensure we return a dict as specified in the function signature
            if isinstance(json_data, dict):
                return json_data
            return {"data": json_data}

        except httpx.RequestError as e:
            logger.error(f"Network error while making request to {url}: {e}")
            return {"error": f"Network error: {str(e)}"}
        except ValueError as e:
            if accept_text and "response" in locals():
                return {"content": response.text}
            logger.error(f"Failed to parse JSON response from {url}: {e}")
            return {"error": f"Failed to parse JSON response: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error while making request to {url}: {e}")
            return {"error": f"Unexpected error: {str(e)}"}


async def handle_redirect(
    location: str,
    headers: Dict[str, str],
    client: httpx.AsyncClient,
    accept_text: bool = False,
) -> Dict[str, Any]:
    """Handle redirects manually, ensuring headers are forwarded."""
    try:
        response = await client.get(location, headers=headers)
        if 200 <= response.status_code < 300:
            # For text responses
            if accept_text:
                return {"content": response.text}

            # Parse the response as JSON and ensure it is a dictionary
            json_data = response.json()
            if isinstance(json_data, dict):
                return json_data
            return {"data": json_data}
        return {
            "error": f"Redirect request failed: {response.status_code}",
            "redirect_url": location,
        }
    except httpx.RequestError as e:
        return {
            "error": f"Failed to follow redirect due to network error: {str(e)}",
            "redirect_url": location,
        }
    except ValueError as e:
        # Try returning text content if we're expecting text
        if accept_text and "response" in locals():
            return {"content": response.text}
        return {
            "error": f"Failed to parse JSON response: {str(e)}",
            "redirect_url": location,
        }
    except Exception as e:
        return {
            "error": f"Unexpected error while following redirect: {str(e)}",
            "redirect_url": location,
        }
