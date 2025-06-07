"""Organization management tools for Terraform Cloud MCP

This module implements the /organizations endpoints of the Terraform Cloud API.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations
"""

from typing import Optional

from ..api.client import api_request
from ..utils.decorators import handle_api_errors
from ..utils.payload import create_api_payload
from ..utils.request import query_params
from ..models.base import APIResponse
from ..models.organizations import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest,
    OrganizationListRequest,
    OrganizationParams,
    OrganizationDetailsRequest,
    OrganizationEntitlementsRequest,
    OrganizationDeleteRequest,
)


@handle_api_errors
async def get_organization_details(organization: str) -> APIResponse:
    """Get details for a specific organization

    Retrieves comprehensive information about an organization including settings,
    email contact info, and configuration defaults.

    API endpoint: GET /organizations/{organization}

    Args:
        organization: The organization name to retrieve details for (required)

    Returns:
        Organization details including name, email, settings and configuration

    See:
        docs/tools/organization.md for reference documentation
    """
    request = OrganizationDetailsRequest(organization=organization)
    return await api_request(f"organizations/{request.organization}")


@handle_api_errors
async def get_organization_entitlements(organization: str) -> APIResponse:
    """Show entitlement set for organization features

    Retrieves information about available features and capabilities based on
    the organization's subscription tier.

    API endpoint: GET /organizations/{organization}/entitlement-set

    Args:
        organization: The organization name to retrieve entitlements for (required)

    Returns:
        Entitlement set details including feature limits and subscription information

    See:
        docs/tools/organization.md for reference documentation
    """
    request = OrganizationEntitlementsRequest(organization=organization)
    return await api_request(f"organizations/{request.organization}/entitlement-set")


@handle_api_errors
async def list_organizations(
    page_number: int = 1,
    page_size: int = 20,
    q: Optional[str] = None,
    query_email: Optional[str] = None,
    query_name: Optional[str] = None,
) -> APIResponse:
    """List organizations with filtering options

    Retrieves a paginated list of organizations the current user has access to,
    with options to search by name or email address.

    API endpoint: GET /organizations

    Args:
        page_number: Page number to fetch (default: 1)
        page_size: Number of results per page (default: 20)
        q: Search query to filter by name and email
        query_email: Search query to filter by email only
        query_name: Search query to filter by name only

    Returns:
        List of organizations with metadata and pagination information

    See:
        docs/tools/organization.md for reference documentation
    """
    request = OrganizationListRequest(
        page_number=page_number,
        page_size=page_size,
        q=q,
        query_email=query_email,
        query_name=query_name,
    )

    # Get all query parameters - now automatically handles query_email and query_name
    params = query_params(request)

    return await api_request("organizations", params=params)


@handle_api_errors
async def create_organization(
    name: str, email: str, params: Optional[OrganizationParams] = None
) -> APIResponse:
    """Create a new organization in Terraform Cloud

    Creates a new organization with the given name and email, allowing workspaces
    and teams to be created within it. This is the first step in setting up a new
    environment in Terraform Cloud.

    API endpoint: POST /organizations

    Args:
        name: The name of the organization (required)
        email: Admin email address (required)
        params: Additional organization settings:
            - collaborator_auth_policy: Authentication policy (password or two_factor_mandatory)
            - session_timeout: Session timeout after inactivity in minutes
            - session_remember: Session total expiration time in minutes
            - cost_estimation_enabled: Whether to enable cost estimation for workspaces
            - default_execution_mode: Default workspace execution mode (remote, local, agent)
            - aggregated_commit_status_enabled: Whether to aggregate VCS status updates
            - speculative_plan_management_enabled: Whether to auto-cancel unused speculative plans
            - assessments_enforced: Whether to enforce health assessments for all workspaces
            - allow_force_delete_workspaces: Whether to allow deleting workspaces with resources
            - default_agent_pool_id: Default agent pool ID (required when using agent mode)

    Returns:
        The created organization details including ID and created timestamp

    See:
        docs/tools/organization.md for reference documentation
    """
    # Extract parameters from the params object if provided
    param_dict = params.model_dump(exclude_none=True) if params else {}

    # Create request using Pydantic model with defaults
    request = OrganizationCreateRequest(name=name, email=email, **param_dict)

    # Create API payload using utility function
    payload = create_api_payload(resource_type="organizations", model=request)

    # Make the API request
    return await api_request("organizations", method="POST", data=payload)


@handle_api_errors
async def update_organization(
    organization: str, params: Optional[OrganizationParams] = None
) -> APIResponse:
    """Update an existing organization in Terraform Cloud

    Modifies organization settings such as email contact, authentication policy,
    or other configuration options. Only specified attributes will be updated.

    API endpoint: PATCH /organizations/{organization}

    Args:
        organization: The name of the organization to update (required)
        params: Organization parameters to update:
            - email: Admin email address for the organization
            - collaborator_auth_policy: Authentication policy (password or two_factor_mandatory)
            - session_timeout: Session timeout after inactivity in minutes
            - session_remember: Session total expiration time in minutes
            - cost_estimation_enabled: Whether to enable cost estimation for workspaces
            - default_execution_mode: Default workspace execution mode (remote, local, agent)
            - aggregated_commit_status_enabled: Whether to aggregate VCS status updates
            - speculative_plan_management_enabled: Whether to auto-cancel unused speculative plans
            - assessments_enforced: Whether to enforce health assessments for all workspaces
            - allow_force_delete_workspaces: Whether to allow deleting workspaces with resources

    Returns:
        The updated organization with all current settings

    See:
        docs/tools/organization.md for reference documentation
    """
    # Extract parameters from the params object if provided
    param_dict = params.model_dump(exclude_none=True) if params else {}

    # Create request using Pydantic model
    request = OrganizationUpdateRequest(organization=organization, **param_dict)

    # Create API payload using utility function
    payload = create_api_payload(
        resource_type="organizations", model=request, exclude_fields={"organization"}
    )

    # Make the API request
    return await api_request(
        f"organizations/{organization}", method="PATCH", data=payload
    )


@handle_api_errors
async def delete_organization(organization: str) -> APIResponse:
    """Delete an organization from Terraform Cloud

    Permanently removes an organization including all its workspaces, teams, and resources.
    This action cannot be undone. Organization names are globally unique and cannot be
    recreated with the same name later.

    API endpoint: DELETE /organizations/{organization}

    Args:
        organization: The name of the organization to delete (required)

    Returns:
        Success confirmation (HTTP 204 No Content) or error details

    See:
        docs/tools/organization.md for reference documentation
    """
    # Create request using Pydantic model
    request = OrganizationDeleteRequest(organization=organization)

    # Make API request
    return await api_request(f"organizations/{request.organization}", method="DELETE")
