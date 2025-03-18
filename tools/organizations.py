"""Organization management tools for Terraform Cloud MCP"""

from typing import Optional, Dict, Any, Union

from api.client import make_api_request
from utils.validators import validate_organization


async def get_organization_details(organization: str, include: str = "") -> dict:
    """
    Get details for a specific organization

    Args:
        organization: The organization name to retrieve details for (required)
        include: Optional related resources to include (comma-separated, e.g., "entitlement-set")

    Returns:
        Organization details
    """
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}

    # Build query parameters
    params = {}
    if include:
        params["include"] = include

    # Make the API request
    success, data = await make_api_request(
        f"organizations/{organization}", params=params
    )

    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary


async def list_organizations(
    page_number: int = 1,
    page_size: int = 20,
    query: str = "",
    query_email: str = "",
    query_name: str = "",
) -> dict:
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
    # Validate pagination parameters
    if page_number < 1:
        return {"error": "Page number must be at least 1"}

    # Build query parameters
    params = {"page[number]": str(page_number), "page[size]": str(page_size)}

    # Add search parameters if provided
    if query:
        params["q"] = query
    if query_email:
        params["q[email]"] = query_email
    if query_name:
        params["q[name]"] = query_name

    # Make the API request
    success, data = await make_api_request("organizations", params=params)

    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary


async def create_organization(
    name: str,
    email: str,
    session_timeout: int = 20160,
    session_remember: int = 20160,
    collaborator_auth_policy: str = "password",
    cost_estimation_enabled: bool = False,
    send_passing_statuses_for_untriggered_speculative_plans: bool = False,
    aggregated_commit_status_enabled: bool = True,
    speculative_plan_management_enabled: bool = True,
    owners_team_saml_role_id: str = "",
    assessments_enforced: bool = False,
    allow_force_delete_workspaces: bool = False,
    default_execution_mode: str = "remote",
    default_agent_pool_id: str = "",
) -> dict:
    """
    Create a new organization in Terraform Cloud

    Args:
        name: The name of the organization (required)
        email: Admin email address (required)
        session_timeout: Session timeout after inactivity in minutes (default: 20160)
        session_remember: Session expiration in minutes (default: 20160)
        collaborator_auth_policy: Authentication policy ('password' or 'two_factor_mandatory') (default: 'password')
        cost_estimation_enabled: Whether cost estimation is enabled for all workspaces (default: False)
        send_passing_statuses_for_untriggered_speculative_plans: Whether to send VCS status updates for untriggered plans (default: False)
        aggregated_commit_status_enabled: Whether to aggregate VCS status updates (default: True)
        speculative_plan_management_enabled: Whether to enable automatic cancellation of plan-only runs (default: True)
        owners_team_saml_role_id: SAML only - the name of the "owners" team (default: "")
        assessments_enforced: Whether to compel health assessments for all eligible workspaces (default: False)
        allow_force_delete_workspaces: Whether workspace admins can delete workspaces with resources (default: False)
        default_execution_mode: Default execution mode ('remote', 'local', or 'agent') (default: 'remote')
        default_agent_pool_id: The ID of the agent pool (required when default_execution_mode is 'agent')

    Returns:
        The created organization details or error information
    """
    # Validate required parameters
    if not name:
        return {"error": "Organization name is required"}

    # Validate the organization name format
    valid, error_message = validate_organization(name)
    if not valid:
        return {"error": error_message}

    if not email:
        return {"error": "Email is required"}

    # Validate collaborator_auth_policy
    if collaborator_auth_policy not in ["password", "two_factor_mandatory"]:
        return {
            "error": "collaborator_auth_policy must be 'password' or 'two_factor_mandatory'"
        }

    # Validate default_execution_mode
    if default_execution_mode not in ["remote", "local", "agent"]:
        return {
            "error": "default_execution_mode must be one of: 'remote', 'local', 'agent'"
        }

    # Check if default_agent_pool_id is provided when using agent mode
    if default_execution_mode == "agent" and not default_agent_pool_id:
        return {
            "error": "default_agent_pool_id is required when default_execution_mode is 'agent'"
        }

    # Check for mutually exclusive settings
    if (
        send_passing_statuses_for_untriggered_speculative_plans
        and aggregated_commit_status_enabled
    ):
        return {
            "error": "aggregated_commit_status_enabled cannot be True when send_passing_statuses_for_untriggered_speculative_plans is True"
        }

    # Build the request payload
    payload: Dict[str, Any] = {
        "data": {
            "type": "organizations",
            "attributes": {
                "name": name,
                "email": email,
            },
        }
    }

    # Add optional parameters if they differ from API defaults
    if session_timeout != 20160:
        payload["data"]["attributes"]["session-timeout"] = session_timeout

    if session_remember != 20160:
        payload["data"]["attributes"]["session-remember"] = session_remember

    if collaborator_auth_policy != "password":
        payload["data"]["attributes"][
            "collaborator-auth-policy"
        ] = collaborator_auth_policy

    if cost_estimation_enabled:
        payload["data"]["attributes"]["cost-estimation-enabled"] = True

    if send_passing_statuses_for_untriggered_speculative_plans:
        payload["data"]["attributes"][
            "send-passing-statuses-for-untriggered-speculative-plans"
        ] = True

    if not aggregated_commit_status_enabled:
        payload["data"]["attributes"]["aggregated-commit-status-enabled"] = False

    if not speculative_plan_management_enabled:
        payload["data"]["attributes"]["speculative-plan-management-enabled"] = False

    if owners_team_saml_role_id:
        payload["data"]["attributes"][
            "owners-team-saml-role-id"
        ] = owners_team_saml_role_id

    if assessments_enforced:
        payload["data"]["attributes"]["assessments-enforced"] = True

    if allow_force_delete_workspaces:
        payload["data"]["attributes"]["allow-force-delete-workspaces"] = True

    # Default execution mode and agent pool
    if default_execution_mode != "remote":
        payload["data"]["attributes"]["default-execution-mode"] = default_execution_mode

    if default_agent_pool_id and default_execution_mode == "agent":
        if "relationships" not in payload["data"]:
            payload["data"]["relationships"] = {}

        payload["data"]["relationships"]["default-agent-pool"] = {
            "data": {"id": default_agent_pool_id, "type": "agent-pools"}
        }

    # Make the API request
    success, data = await make_api_request("organizations", method="POST", data=payload)

    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary


async def update_organization(
    organization: str,
    name: str = "",
    email: str = "",
    session_timeout: Optional[int] = None,
    session_remember: Optional[int] = None,
    collaborator_auth_policy: str = "",
    cost_estimation_enabled: Optional[bool] = None,
    send_passing_statuses_for_untriggered_speculative_plans: Optional[bool] = None,
    aggregated_commit_status_enabled: Optional[bool] = None,
    speculative_plan_management_enabled: Optional[bool] = None,
    owners_team_saml_role_id: str = "",
    assessments_enforced: Optional[bool] = None,
    allow_force_delete_workspaces: Optional[bool] = None,
    default_execution_mode: str = "",
    default_agent_pool_id: str = "",
) -> dict:
    """
    Update an existing organization in Terraform Cloud

    Args:
        organization: The name of the organization to update (required)
        name: New name for the organization (optional)
        email: New admin email address (optional)
        session_timeout: New session timeout after inactivity in minutes (optional)
        session_remember: New session expiration in minutes (optional)
        collaborator_auth_policy: New authentication policy ('password' or 'two_factor_mandatory') (optional)
        cost_estimation_enabled: Whether cost estimation is enabled for all workspaces (optional)
        send_passing_statuses_for_untriggered_speculative_plans: Whether to send VCS status updates for untriggered plans (optional)
        aggregated_commit_status_enabled: Whether to aggregate VCS status updates (optional)
        speculative_plan_management_enabled: Whether to enable automatic cancellation of plan-only runs (optional)
        owners_team_saml_role_id: SAML only - the name of the "owners" team (optional)
        assessments_enforced: Whether to compel health assessments for all eligible workspaces (optional)
        allow_force_delete_workspaces: Whether workspace admins can delete workspaces with resources (optional)
        default_execution_mode: Default execution mode ('remote', 'local', or 'agent') (optional)
        default_agent_pool_id: The ID of the agent pool (required when default_execution_mode is 'agent')

    Returns:
        The updated organization details or error information
    """
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}

    # Validate new name if provided
    if name:
        valid, error_message = validate_organization(name)
        if not valid:
            return {"error": f"New organization name invalid: {error_message}"}

    # Validate collaborator_auth_policy if provided
    if collaborator_auth_policy and collaborator_auth_policy not in [
        "password",
        "two_factor_mandatory",
    ]:
        return {
            "error": "collaborator_auth_policy must be 'password' or 'two_factor_mandatory'"
        }

    # Validate default_execution_mode if provided
    if default_execution_mode and default_execution_mode not in [
        "remote",
        "local",
        "agent",
    ]:
        return {
            "error": "default_execution_mode must be one of: 'remote', 'local', 'agent'"
        }

    # Check if default_agent_pool_id is provided when using agent mode
    if default_execution_mode == "agent" and not default_agent_pool_id:
        return {
            "error": "default_agent_pool_id is required when default_execution_mode is 'agent'"
        }

    # Check for mutually exclusive settings if both are provided
    if (
        send_passing_statuses_for_untriggered_speculative_plans is not None
        and aggregated_commit_status_enabled is not None
        and send_passing_statuses_for_untriggered_speculative_plans
        and aggregated_commit_status_enabled
    ):
        return {
            "error": "aggregated_commit_status_enabled cannot be True when send_passing_statuses_for_untriggered_speculative_plans is True"
        }

    # Build the request payload
    payload: Dict[str, Any] = {"data": {"type": "organizations", "attributes": {}}}

    # Add attributes only if provided
    if name:
        payload["data"]["attributes"]["name"] = name

    if email:
        payload["data"]["attributes"]["email"] = email

    if session_timeout is not None:
        payload["data"]["attributes"]["session-timeout"] = session_timeout

    if session_remember is not None:
        payload["data"]["attributes"]["session-remember"] = session_remember

    if collaborator_auth_policy:
        payload["data"]["attributes"][
            "collaborator-auth-policy"
        ] = collaborator_auth_policy

    if cost_estimation_enabled is not None:
        payload["data"]["attributes"][
            "cost-estimation-enabled"
        ] = cost_estimation_enabled

    if send_passing_statuses_for_untriggered_speculative_plans is not None:
        payload["data"]["attributes"][
            "send-passing-statuses-for-untriggered-speculative-plans"
        ] = send_passing_statuses_for_untriggered_speculative_plans

    if aggregated_commit_status_enabled is not None:
        payload["data"]["attributes"][
            "aggregated-commit-status-enabled"
        ] = aggregated_commit_status_enabled

    if speculative_plan_management_enabled is not None:
        payload["data"]["attributes"][
            "speculative-plan-management-enabled"
        ] = speculative_plan_management_enabled

    if owners_team_saml_role_id:
        payload["data"]["attributes"][
            "owners-team-saml-role-id"
        ] = owners_team_saml_role_id

    if assessments_enforced is not None:
        payload["data"]["attributes"]["assessments-enforced"] = assessments_enforced

    if allow_force_delete_workspaces is not None:
        payload["data"]["attributes"][
            "allow-force-delete-workspaces"
        ] = allow_force_delete_workspaces

    # Default execution mode if provided
    if default_execution_mode:
        payload["data"]["attributes"]["default-execution-mode"] = default_execution_mode

    # Add agent pool relationship if provided
    if default_agent_pool_id and default_execution_mode == "agent":
        if "relationships" not in payload["data"]:
            payload["data"]["relationships"] = {}

        payload["data"]["relationships"]["default-agent-pool"] = {
            "data": {"id": default_agent_pool_id, "type": "agent-pools"}
        }

    # Check if we have any attributes to update
    if not payload["data"]["attributes"] and "relationships" not in payload["data"]:
        return {"error": "At least one attribute must be provided for update"}

    # Make the API request
    success, data = await make_api_request(
        f"organizations/{organization}", method="PATCH", data=payload
    )

    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary


async def delete_organization(organization: str, confirm: bool = False) -> dict:
    """
    Delete an organization from Terraform Cloud

    Args:
        organization: The name of the organization to delete (required)
        confirm: Set to True to confirm deletion, otherwise returns a confirmation request (default: False)

    Returns:
        Success message, confirmation request, or error details
    """
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}

    # If not confirmed, return a confirmation request
    if not confirm:
        return {
            "status": "confirmation_required",
            "message": f"WARNING: You're about to delete organization '{organization}'. This will delete ALL workspaces, variables, and other resources in this organization. This action cannot be undone. Call this function again with confirm=True to proceed.",
            "organization": organization,
        }

    # Make the API request
    success, data = await make_api_request(
        f"organizations/{organization}", method="DELETE"
    )

    if success:
        return {
            "status": "success",
            "message": f"Organization '{organization}' deleted successfully",
        }
    else:
        return data  # Error info is already in the data dictionary
