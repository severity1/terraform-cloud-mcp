"""Account management tools for Terraform Cloud API

This module implements the /account endpoints of the Terraform Cloud API.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/account
"""

from ..api.client import api_request
from ..utils.decorators import handle_api_errors
from ..models.base import APIResponse
from ..models.account import AccountDetailsRequest


@handle_api_errors
async def get_account_details() -> APIResponse:
    """Get account details for a Terraform Cloud API token

    This endpoint shows information about the currently authenticated user or service account,
    useful for verifying identity, retrieving email address, and checking authentication status.
    It returns the same type of object as the Users API, but also includes an email address,
    which is hidden when viewing info about other users.

    API endpoint: GET /account/details

    Returns:
        Raw API response with account information from Terraform Cloud
        including user ID, username, email address, and authentication status

    See:
        docs/tools/account.md for reference documentation
    """
    AccountDetailsRequest()
    return await api_request("account/details")
