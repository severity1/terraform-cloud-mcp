"""Terraform Cloud API client"""

import os
import logging
from typing import Optional, Dict, Tuple, TypeVar, Union, Any
import httpx
from pydantic import BaseModel

# Constants
TERRAFORM_CLOUD_API_URL = "https://app.terraform.io/api/v2"

# Store default token from environment variable
# Security note: API tokens are sensitive data and should never be logged or exposed
DEFAULT_TOKEN = os.getenv("TFC_TOKEN")

if DEFAULT_TOKEN:
    logging.info("Default token provided (masked for security)")


async def make_api_request(
    path: str,
    method: str = "GET",
    token: Optional[str] = None,
    params: dict = {},
    data: dict = {},
) -> Tuple[bool, dict]:
    """
    Make a request to the Terraform Cloud API

    Args:
        path: API path to request (without base URL)
        method: HTTP method (default: GET)
        token: API token (defaults to DEFAULT_TOKEN)
        params: Query parameters for the request (optional)
        data: JSON data for POST/PATCH requests (optional)

    Returns:
        Tuple of (success, data) where data is either the response JSON or an error dict
    """
    if not token:
        token = DEFAULT_TOKEN

    if not token:
        return (
            False,
            {
                "error": "Token is required. Please set the TFC_TOKEN environment variable."
            },
        )

    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.api+json",
        }

        async with httpx.AsyncClient() as client:
            url = f"{TERRAFORM_CLOUD_API_URL}/{path}"

            if method == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method == "POST":
                response = await client.post(
                    url, headers=headers, params=params, json=data
                )
            elif method == "PATCH":
                response = await client.patch(
                    url, headers=headers, params=params, json=data
                )
            elif method == "DELETE":
                response = await client.delete(url, headers=headers, params=params)
            else:
                return (False, {"error": f"Unsupported method: {method}"})

            # Handle different success response codes
            if response.status_code in [200, 201, 202, 204]:
                if response.status_code == 204:  # No content
                    return (True, {"status": "success"})
                try:
                    return (True, response.json())
                except ValueError:
                    return (True, {"status": "success", "raw_response": response.text})
            else:
                error_message = f"API request failed: {response.status_code}"
                try:
                    error_data = response.json()
                    return (False, {"error": error_message, "details": error_data})
                except ValueError:
                    return (False, {"error": error_message})
    except Exception as e:
        # Ensure no sensitive data is included in error messages
        error_message = str(e)
        if token and token in error_message:
            error_message = error_message.replace(token, "[REDACTED]")
        return (False, {"error": f"Request error: {error_message}"})


# Type variable for generic request models
ReqT = TypeVar("ReqT", bound=BaseModel)


async def api_request(
    path: str,
    method: str = "GET",
    token: Optional[str] = None,
    params: dict = {},
    data: Union[dict, BaseModel] = {},
) -> Dict[str, Any]:
    """
    Make a request to the Terraform Cloud API.
    Returns raw API response without validation.

    Args:
        path: API path to request (without base URL)
        method: HTTP method (default: GET)
        token: API token (defaults to DEFAULT_TOKEN)
        params: Query parameters for the request (optional)
        data: JSON data or Pydantic model for POST/PATCH requests (optional)

    Returns:
        Raw API response as a dictionary
    """
    # Get token from environment if not provided
    if not token:
        token = DEFAULT_TOKEN

    if not token:
        return {
            "error": "Token is required. Please set the TFC_TOKEN environment variable."
        }

    # Convert data to dict if it's a BaseModel
    request_data = data
    if isinstance(data, BaseModel):
        # Use standard Pydantic serialization - Pydantic v2
        request_data = data.model_dump(exclude_unset=True)  # type: ignore

    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.api+json",
        }

        async with httpx.AsyncClient() as client:
            url = f"{TERRAFORM_CLOUD_API_URL}/{path}"

            if method == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method == "POST":
                response = await client.post(
                    url, headers=headers, params=params, json=request_data
                )
            elif method == "PATCH":
                response = await client.patch(
                    url, headers=headers, params=params, json=request_data
                )
            elif method == "DELETE":
                response = await client.delete(url, headers=headers, params=params)
            else:
                return {"error": f"Unsupported method: {method}"}

            # Handle different response codes
            if response.status_code in [200, 201, 202]:
                # Return JSON response directly - verify it's a dict
                result = response.json()
                if isinstance(result, dict):
                    return result
                else:
                    # Wrap non-dict responses
                    return {"data": result}
            elif response.status_code == 204:  # No content
                return {"status": "success"}
            else:
                # Error case, try to get error details
                try:
                    return {
                        "error": f"API request failed: {response.status_code}",
                        "details": response.json(),
                    }
                except ValueError:
                    return {"error": f"API request failed: {response.status_code}"}
    except Exception as e:
        # Ensure no sensitive data is included in error messages
        error_message = str(e)
        if token and token in error_message:
            error_message = error_message.replace(token, "[REDACTED]")
        return {"error": f"Request error: {error_message}"}
