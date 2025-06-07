"""Account models for Terraform Cloud API

This module contains models for Terraform Cloud account-related requests.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/account
"""

from .base import APIRequest


class AccountDetailsRequest(APIRequest):
    """Request model for getting account details.

    This model is used for the GET /account/details endpoint which requires no parameters.
    The endpoint returns information about the currently authenticated user or service account.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/account#show-account-details

    Note:
        For team and organization tokens, this endpoint returns information about
        a synthetic "service user" account associated with the token.

    See:
        docs/models/account.md for reference
    """

    pass  # No parameters needed for this endpoint
