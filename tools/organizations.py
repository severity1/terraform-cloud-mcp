"""Organization management tools for Terraform Cloud MCP

This module implements the /organizations endpoints of the Terraform Cloud API.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations
"""

from typing import Dict, Any

from api.client import api_request
from utils.decorators import handle_api_errors
from models.organizations import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest,
    OrganizationListRequest,
)


@handle_api_errors
async def get_organization_details(organization: str) -> Dict[str, Any]:
    """
    Get details for a specific organization

    Args:
        organization: The organization name to retrieve details for (required)

    Returns:
        Organization details
    """
    return await api_request(f"organizations/{organization}")


@handle_api_errors
async def get_organization_entitlements(organization: str) -> Dict[str, Any]:
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
) -> Dict[str, Any]:
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
async def create_organization(name: str, email: str, **kwargs) -> Dict[str, Any]:
    """
    Create a new organization in Terraform Cloud

    Args:
        name: The name of the organization (required)
        email: Admin email address (required)
        **kwargs: Additional optional organization attributes with defaults defined in the model:
            - session_timeout: Session timeout after inactivity in minutes (default: 20160)
            - session_remember: Session expiration in minutes (default: 20160)
            - collaborator_auth_policy: Authentication policy ('password' or 'two_factor_mandatory') (default: 'password')
            - cost_estimation_enabled: Whether cost estimation is enabled for all workspaces (default: False)
            - send_passing_statuses_for_untriggered_speculative_plans: Whether to send VCS status updates (default: False)
            - aggregated_commit_status_enabled: Whether to aggregate VCS status updates (default: True)
            - speculative_plan_management_enabled: Whether to enable automatic cancellation of plan-only runs (default: True)
            - owners_team_saml_role_id: SAML only - the name of the "owners" team (default: None)
            - assessments_enforced: Whether to compel health assessments for all eligible workspaces (default: False)
            - allow_force_delete_workspaces: Whether workspace admins can delete workspaces with resources (default: False)
            - default_execution_mode: Default execution mode ('remote', 'local', or 'agent') (default: 'remote')
            - default_agent_pool_id: The ID of the agent pool (required when default_execution_mode is 'agent')

    Returns:
        The created organization details or error information
    """
    # Create request using Pydantic model with defaults
    request = OrganizationCreateRequest(name=name, email=email, **kwargs)

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
async def update_organization(organization: str, **kwargs) -> Dict[str, Any]:
    """
    Update an existing organization in Terraform Cloud

    Args:
        organization: The name of the organization to update (required)
        **kwargs: Optional attributes to update, including:
            - name: New name for the organization
            - email: New admin email address
            - session_timeout: Session timeout after inactivity in minutes
            - session_remember: Session expiration in minutes
            - collaborator_auth_policy: Authentication policy ('password' or 'two_factor_mandatory')
            - cost_estimation_enabled: Whether cost estimation is enabled for all workspaces
            - send_passing_statuses_for_untriggered_speculative_plans: Whether to send VCS status updates
            - aggregated_commit_status_enabled: Whether to aggregate VCS status updates
            - speculative_plan_management_enabled: Whether to enable automatic cancellation of plan-only runs
            - owners_team_saml_role_id: SAML only - the name of the "owners" team
            - assessments_enforced: Whether to compel health assessments for all eligible workspaces
            - allow_force_delete_workspaces: Whether workspace admins can delete workspaces with resources
            - default_execution_mode: Default execution mode ('remote', 'local', or 'agent')
            - default_agent_pool_id: The ID of the agent pool (required when default_execution_mode is 'agent')

    Returns:
        The updated organization details or error information
    """
    # Create request using Pydantic model
    request = OrganizationUpdateRequest(organization=organization, **kwargs)

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
async def delete_organization(organization: str) -> Dict[str, Any]:
    """
    Delete an organization from Terraform Cloud

    Args:
        organization: The name of the organization to delete (required)

    Returns:
        Success message or error details
    """
    return await api_request(f"organizations/{organization}", method="DELETE")
