"""Organization management tools for Terraform Cloud MCP

This module implements the /organizations endpoints of the Terraform Cloud API.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations
"""

from typing import Optional

from api.client import api_request
from utils.decorators import handle_api_errors
from models.base import APIResponse
from models.organizations import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest,
    OrganizationListRequest,
    OrganizationParams,
)


@handle_api_errors
async def get_organization_details(organization: str) -> APIResponse:
    """
    Get details for a specific organization

    Args:
        organization: The organization name to retrieve details for (required)

    Returns:
        Organization details
    """
    return await api_request(f"organizations/{organization}")


@handle_api_errors
async def get_organization_entitlements(organization: str) -> APIResponse:
    """
    Show entitlement set for organization features

    Args:
        organization: The organization name to retrieve entitlements for (required)

    Returns:
        Entitlement set details including feature limits and entitlements
    """
    return await api_request(f"organizations/{organization}/entitlement-set")


@handle_api_errors
async def list_organizations(
    page_number: int = 1,
    page_size: int = 20,
    query: str = "",
    query_email: str = "",
    query_name: str = "",
) -> APIResponse:
    """
    List organizations with filtering options

    Args:
        page_number: Page number to fetch (default: 1)
        page_size: Number of results per page (default: 20)
        query: A search query string to filter organizations by name and notification email
        query_email: A search query string to filter organizations by notification email
        query_name: A search query string to filter organizations by name

    Returns:
        List of organizations with pagination information
    """
    request = OrganizationListRequest(
        page_number=page_number,
        page_size=page_size,
        query=query,
        query_email=query_email,
        query_name=query_name,
    )

    params = {
        "page[number]": str(request.page_number),
        "page[size]": str(request.page_size),
    }

    if request.query:
        params["q"] = request.query
    if request.query_email:
        params["q[email]"] = request.query_email
    if request.query_name:
        params["q[name]"] = request.query_name

    return await api_request("organizations", params=params)


@handle_api_errors
async def create_organization(
    name: str, email: str, params: Optional[OrganizationParams] = None
) -> APIResponse:
    """
    Create a new organization in Terraform Cloud

    Args:
        name: The name of the organization (required)
        email: Admin email address (required)
        params: Additional organization parameters (optional)

    Returns:
        The created organization details or error information
    """
    # Extract parameters from the params object if provided
    param_dict = params.model_dump(exclude_none=True) if params else {}

    # Create request using Pydantic model with defaults
    request = OrganizationCreateRequest(name=name, email=email, **param_dict)

    # Create API payload directly
    attributes = request.model_dump(by_alias=True, exclude_none=True)

    payload = {
        "data": {
            "type": "organizations",
            "attributes": attributes,
        }
    }

    # Make the API request
    return await api_request("organizations", method="POST", data=payload)


@handle_api_errors
async def update_organization(
    organization: str, params: Optional[OrganizationParams] = None
) -> APIResponse:
    """
    Update an existing organization in Terraform Cloud

    Args:
        organization: The name of the organization to update (required)
        params: Organization parameters to update (optional)

    Returns:
        The updated organization details or error information
    """
    # Extract parameters from the params object if provided
    param_dict = params.model_dump(exclude_none=True) if params else {}

    # Create request using Pydantic model
    request = OrganizationUpdateRequest(organization=organization, **param_dict)

    # Create API payload directly
    attributes = request.model_dump(
        by_alias=True, exclude={"organization"}, exclude_none=True
    )

    payload = {
        "data": {
            "type": "organizations",
            "attributes": attributes,
        }
    }

    # Make the API request
    return await api_request(
        f"organizations/{organization}", method="PATCH", data=payload
    )


@handle_api_errors
async def delete_organization(organization: str) -> APIResponse:
    """
    Delete an organization from Terraform Cloud

    Args:
        organization: The name of the organization to delete (required)

    Returns:
        Success message or error details
    """
    return await api_request(f"organizations/{organization}", method="DELETE")
