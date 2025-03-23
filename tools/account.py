"""Account management tools for Terraform Cloud API

This module implements the /account endpoints of the Terraform Cloud API.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/account
"""

from typing import Dict, Any

from api.client import api_request
from utils.decorators import handle_api_errors


@handle_api_errors
async def get_account_details() -> Dict[str, Any]:
    """
    Get account details for a Terraform Cloud API token

    `GET /account/details`

    This endpoint shows information about the currently authenticated user or service account.
    It returns the same type of object as the Users API, but also includes an email address,
    which is hidden when viewing info about other users.

    For internal reasons, HCP Terraform associates team and organization tokens with a synthetic
    user account called "service user". HCP Terraform returns the associated service user for
    account requests authenticated by a team or organization token.

    Returns:
        Raw API response with account information from Terraform Cloud
    """
    return await api_request("account/details")
