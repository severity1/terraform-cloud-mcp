"""Terraform Cloud API client"""

import logging
from typing import Optional, Dict, TypeVar, Union, Any
import httpx
from pydantic import BaseModel

from ..utils.env import get_tfc_token, should_return_raw_response, get_tfc_address
from ..utils.filters import (
    get_response_filter,
    should_filter_response,
    detect_resource_type,
    detect_operation_type,
)

DEFAULT_TOKEN = get_tfc_token()
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
    raw_response: Optional[bool] = None,
) -> Dict[str, Any]:
    """Make a request to the Terraform Cloud API with proper error handling."""
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
        tfc_address = get_tfc_address()
        url = path if external_url else f"{tfc_address}/api/v2/{path}"
        kwargs: Dict[str, Any] = {"headers": headers, "params": params}
        if request_data:
            kwargs["json"] = request_data

        try:
            response = await client.request(method, url, **kwargs)

            # Handle redirects manually
            if response.status_code in (301, 302, 307, 308):
                location = response.headers.get("Location")
                if not location:
                    return {
                        "error": "Redirect received, but no Location header provided."
                    }
                return await handle_redirect(
                    location, headers, client, accept_text, path, method, raw_response
                )

            # For text responses
            if accept_text:
                return {"content": response.text}

            # Handle 204 No Content responses
            if response.status_code == 204:
                return {"status": "success", "status_code": 204}

            # Handle other success responses
            json_data = response.json()
            # Ensure we return a dict as specified in the function signature
            if not isinstance(json_data, dict):
                json_data = {"data": json_data}

            # Apply response filtering if not disabled
            return _apply_response_filtering(json_data, path, method, raw_response)

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
    original_path: str = "",
    original_method: str = "GET",
    raw_response: Optional[bool] = None,
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
            if not isinstance(json_data, dict):
                json_data = {"data": json_data}

            # Apply response filtering if not disabled
            return _apply_response_filtering(
                json_data, original_path, original_method, raw_response
            )
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


def _apply_response_filtering(
    json_data: Dict[str, Any],
    path: str,
    method: str,
    raw_response: Optional[bool] = None,
) -> Dict[str, Any]:
    """Apply response filtering based on configuration and request context."""
    # Check if raw response is requested
    if raw_response is True or (raw_response is None and should_return_raw_response()):
        return json_data

    # Check if this response should be filtered
    if not should_filter_response(path, method):
        return json_data

    try:
        # Detect resource type and operation type
        resource_type = detect_resource_type(path, json_data)
        operation_type = detect_operation_type(path, method)

        # Get and apply the appropriate filter
        filter_func = get_response_filter(resource_type)
        filtered_data = filter_func(json_data, operation_type)

        logger.info(
            f"Applied {resource_type} filter ({filter_func.__name__}) for {operation_type} operation on {path}"
        )
        return dict(filtered_data)

    except Exception as e:
        # If filtering fails, log error and return raw data
        logger.warning(
            f"Response filtering failed for {path}: {e}. Returning raw response."
        )
        return json_data
