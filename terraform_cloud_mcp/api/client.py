"""Terraform Cloud API client

This module provides functions for making requests to the Terraform Cloud API.
It handles authentication, request formatting, and response processing.
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
) -> Dict[str, Any]:
    """Make a request to the Terraform Cloud API with proper error handling.

    Creates an authenticated request to the Terraform Cloud API, handling
    authentication, request formatting, and basic error checking.

    Args:
        path: API path to request (without leading slash)
        method: HTTP method to use (GET, POST, PATCH, DELETE)
        token: API token (defaults to TFC_TOKEN from environment)
        params: Query parameters for the request
        data: JSON payload data (dict or Pydantic model)

    Returns:
        JSON response from the API as a dictionary

    Raises:
        HTTPStatusError: For HTTP errors (wrapped by handle_api_errors)
        RequestError: For network/connection issues

    Note:
        This function expects TFC_TOKEN to be set in the environment or .env file
    """
    # Use environment token if not explicitly provided
    if not token:
        token = DEFAULT_TOKEN

    # Fail early before network operations if token is missing
    if not token:
        return {
            "error": "Token is required. Please set the TFC_TOKEN environment variable."
        }

    # Convert Pydantic models to dict, excluding unset fields to respect server defaults
    request_data = data
    if isinstance(data, BaseModel):
        request_data = data.model_dump(exclude_unset=True)

    try:
        # Terraform Cloud API requires specific headers for authentication and content type
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.api+json",
        }

        async with httpx.AsyncClient() as client:
            url = f"{TERRAFORM_CLOUD_API_URL}/{path}"

            # Map HTTP methods to client functions for dynamic method selection
            methods: Dict[str, Any] = {
                "GET": client.get,
                "POST": client.post,
                "PATCH": client.patch,
                "DELETE": client.delete,
            }

            # Get method function or return error for unsupported methods
            method_func = methods.get(method)
            if not method_func:
                return {"error": f"Unsupported method: {method}"}

            # Build common request parameters
            kwargs = {"headers": headers, "params": params}

            # Add JSON data for methods that send request bodies
            if method in ["POST", "PATCH"]:
                json_data = request_data if isinstance(request_data, dict) else {}
                kwargs["json"] = json_data

            response = await method_func(url, **kwargs)

            if 200 <= response.status_code < 300:  # Success range
                if response.status_code == 204:  # No content responses need standardized formatting
                    return {"status": "success"}

                result = response.json()
                if isinstance(result, dict):
                    return result
                else:
                    # Non-dict responses wrapped for consistent interface
                    return {"data": result}
            else:
                try:
                    # Include detailed error info from response body when available
                    return {
                        "error": f"API request failed: {response.status_code}",
                        "details": response.json(),
                    }
                except ValueError:
                    # Some error responses (e.g. 502) don't include JSON bodies
                    return {"error": f"API request failed: {response.status_code}"}
    except Exception as e:
        # Security: Remove token from any error messages
        error_message = str(e)
        if token and token in error_message:
            error_message = error_message.replace(token, "[REDACTED]")
        return {"error": f"Request error: {error_message}"}
