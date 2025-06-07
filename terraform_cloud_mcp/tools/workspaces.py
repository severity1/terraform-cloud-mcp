"""Workspace management tools for Terraform Cloud MCP

This module implements the workspace-related endpoints of the Terraform Cloud API.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces
"""

import logging
from typing import Optional

from ..api.client import api_request
from ..utils.decorators import handle_api_errors
from ..utils.payload import create_api_payload
from ..utils.request import query_params
from ..models.base import APIResponse
from ..models.workspaces import (
    WorkspaceCreateRequest,
    WorkspaceUpdateRequest,
    WorkspaceListRequest,
    WorkspaceParams,
    DataRetentionPolicyRequest,
)


@handle_api_errors
async def create_workspace(
    organization: str, name: str, params: Optional[WorkspaceParams] = None
) -> APIResponse:
    """Create a new workspace in an organization.

    Creates a new Terraform Cloud workspace which serves as an isolated environment
    for managing infrastructure. Workspaces contain variables, state files, and run
    histories for a specific infrastructure configuration.

    API endpoint: POST /organizations/{organization}/workspaces

    Args:
        organization: The name of the organization
        name: The name to give the workspace

        params: Additional workspace parameters (optional):
            - description: Human-readable description of the workspace
            - execution_mode: How Terraform runs are executed (remote, local, agent)
            - terraform_version: Version of Terraform to use (default: latest)
            - working_directory: Subdirectory to use when running Terraform
            - vcs_repo: Version control repository configuration
            - auto_apply: Whether to automatically apply successful plans
            - file_triggers_enabled: Whether file changes trigger runs
            - trigger_prefixes: Directories that trigger runs when changed
            - trigger_patterns: Glob patterns that trigger runs when files match
            - allow_destroy_plan: Whether to allow destruction plans
            - auto_apply_run_trigger: Whether to auto-apply changes from run triggers

    Returns:
        The created workspace data including configuration, settings and metadata

    See:
        docs/tools/workspace.md for reference documentation
    """
    param_dict = params.model_dump(exclude_none=True) if params else {}
    request = WorkspaceCreateRequest(organization=organization, name=name, **param_dict)

    payload = create_api_payload(
        resource_type="workspaces", model=request, exclude_fields={"organization"}
    )

    return await api_request(
        f"organizations/{organization}/workspaces", method="POST", data=payload
    )


@handle_api_errors
async def update_workspace(
    organization: str, workspace_name: str, params: Optional[WorkspaceParams] = None
) -> APIResponse:
    """Update an existing workspace.

    Modifies the settings of a Terraform Cloud workspace. This can be used to change
    attributes like execution mode, VCS repository settings, description, or any other
    workspace configuration options. Only specified attributes will be updated;
    unspecified attributes remain unchanged.

    API endpoint: PATCH /organizations/{organization}/workspaces/{workspace_name}

    Args:
        organization: The name of the organization that owns the workspace
        workspace_name: The name of the workspace to update

        params: Workspace parameters to update (optional):
            - name: New name for the workspace (if renaming)
            - description: Human-readable description of the workspace
            - execution_mode: How Terraform runs are executed (remote, local, agent)
            - terraform_version: Version of Terraform to use
            - working_directory: Subdirectory to use when running Terraform
            - vcs_repo: Version control repository configuration (oauth-token-id, identifier)
            - auto_apply: Whether to automatically apply successful plans
            - file_triggers_enabled: Whether file changes trigger runs
            - trigger_prefixes: Directories that trigger runs when changed
            - trigger_patterns: Glob patterns that trigger runs when files match
            - allow_destroy_plan: Whether to allow destruction plans
            - auto_apply_run_trigger: Whether to auto-apply changes from run triggers

    Returns:
        The updated workspace with all current settings and configuration

    See:
        docs/tools/workspace.md for reference documentation
    """
    # Extract parameters from the params object if provided
    param_dict = params.model_dump(exclude_none=True) if params else {}

    # Create request using Pydantic model
    request = WorkspaceUpdateRequest(
        organization=organization, workspace_name=workspace_name, **param_dict
    )

    # Create API payload using utility function
    payload = create_api_payload(
        resource_type="workspaces",
        model=request,
        exclude_fields={"organization", "workspace_name"},
    )

    # Log payload for debugging
    logger = logging.getLogger(__name__)
    logger.debug(f"Update workspace payload: {payload}")

    # Make API request
    response = await api_request(
        f"organizations/{organization}/workspaces/{workspace_name}",
        method="PATCH",
        data=payload,
    )

    # Log response for debugging
    logger.debug(f"Update workspace response: {response}")

    return response


@handle_api_errors
async def list_workspaces(
    organization: str,
    page_number: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
) -> APIResponse:
    """List workspaces in an organization.

    Retrieves a paginated list of all workspaces in a Terraform Cloud organization.
    Results can be filtered using a search string to find specific workspaces by name.
    Use this tool to discover existing workspaces, check workspace configurations,
    or find specific workspaces by partial name match.

    API endpoint: GET /organizations/{organization}/workspaces

    Args:
        organization: The name of the organization to list workspaces from
        page_number: The page number to return (default: 1)
        page_size: The number of items per page (default: 20, max: 100)
        search: Optional search string to filter workspaces by name

    Returns:
        Paginated list of workspaces with their configuration settings and metadata

    See:
        docs/tools/workspace.md for reference documentation
    """
    # Create request using Pydantic model for validation
    request = WorkspaceListRequest(
        organization=organization,
        page_number=page_number,
        page_size=page_size,
        search=search,
    )

    params = query_params(request)

    return await api_request(
        f"organizations/{organization}/workspaces", method="GET", params=params
    )


@handle_api_errors
async def delete_workspace(organization: str, workspace_name: str) -> APIResponse:
    """Delete a workspace.

    Permanently deletes a Terraform Cloud workspace and all its resources including
    state versions, run history, and configuration versions. This action cannot be undone.

    WARNING: This is a destructive operation. For workspaces that have active resources,
    consider running a destroy plan first or use safe_delete_workspace instead.

    API endpoint: DELETE /organizations/{organization}/workspaces/{workspace_name}

    Args:
        organization: The name of the organization that owns the workspace
        workspace_name: The name of the workspace to delete

    Returns:
        Success message with no content (HTTP 204) if successful
        Error response with explanation if the workspace cannot be deleted

    See:
        docs/tools/workspace.md for reference documentation
    """
    # Make API request
    return await api_request(
        f"organizations/{organization}/workspaces/{workspace_name}",
        method="DELETE",
    )


@handle_api_errors
async def safe_delete_workspace(organization: str, workspace_name: str) -> APIResponse:
    """Safely delete a workspace by first checking if it can be deleted.

    Initiates a safe delete operation which checks if the workspace has resources
    before deleting it. This is a safer alternative to delete_workspace as it prevents
    accidental deletion of workspaces with active infrastructure.

    The operation follows these steps:
    1. Checks if the workspace has any resources
    2. If no resources exist, deletes the workspace
    3. If resources exist, returns an error indicating the workspace cannot be safely deleted

    API endpoint: POST /organizations/{organization}/workspaces/{workspace_name}/actions/safe-delete

    Args:
        organization: The name of the organization that owns the workspace
        workspace_name: The name of the workspace to delete

    Returns:
        Status of the safe delete operation including:
        - Success response if deletion was completed
        - Error with details if workspace has resources and cannot be safely deleted
        - List of resources that would be affected by deletion (if applicable)

    See:
        docs/tools/workspace.md for reference documentation
    """
    # Make API request
    return await api_request(
        f"organizations/{organization}/workspaces/{workspace_name}/actions/safe-delete",
        method="POST",
    )


@handle_api_errors
async def lock_workspace(workspace_id: str, reason: str = "") -> APIResponse:
    """Lock a workspace.

    Locks a workspace to prevent runs from being queued. This is useful when you want
    to prevent changes to infrastructure while performing maintenance or making manual
    adjustments. Locking a workspace does not affect currently running plans or applies.

    API endpoint: POST /workspaces/{workspace_id}/actions/lock

    Args:
        workspace_id: The ID of the workspace to lock (format: "ws-xxxxxxxx")
        reason: Optional reason for locking

    Returns:
        The workspace with updated lock status and related metadata

    See:
        docs/tools/workspace.md for reference documentation
    """
    payload = {}
    if reason:
        payload = {"reason": reason}
    return await api_request(
        f"workspaces/{workspace_id}/actions/lock", method="POST", data=payload
    )


@handle_api_errors
async def unlock_workspace(workspace_id: str) -> APIResponse:
    """Unlock a workspace.

    Removes the lock from a workspace, allowing runs to be queued. This enables
    normal operation of the workspace after it was previously locked.

    API endpoint: POST /workspaces/{workspace_id}/actions/unlock

    Args:
        workspace_id: The ID of the workspace to unlock (format: "ws-xxxxxxxx")

    Returns:
        The workspace with updated lock status and related metadata

    See:
        docs/tools/workspace.md for reference documentation
    """
    return await api_request(f"workspaces/{workspace_id}/actions/unlock", method="POST")


@handle_api_errors
async def force_unlock_workspace(workspace_id: str) -> APIResponse:
    """Force unlock a workspace. This should be used with caution.

    Forces a workspace to unlock even when the normal unlock process isn't possible.
    This is typically needed when a run has orphaned a lock or when the user who locked
    the workspace is unavailable. This operation requires admin privileges on the workspace.

    WARNING: Forcing an unlock can be dangerous if the workspace is legitimately locked
    for active operations. Only use this when you are certain it's safe to unlock.

    API endpoint: POST /workspaces/{workspace_id}/actions/force-unlock

    Args:
        workspace_id: The ID of the workspace to force unlock (format: "ws-xxxxxxxx")

    Returns:
        The workspace with updated lock status and related metadata

    See:
        docs/tools/workspace.md for reference documentation
    """
    # Make API request
    return await api_request(
        f"workspaces/{workspace_id}/actions/force-unlock", method="POST"
    )


@handle_api_errors
async def set_data_retention_policy(workspace_id: str, days: int) -> APIResponse:
    """Set a data retention policy for a workspace.

    Creates or updates a data retention policy that determines how long Terraform Cloud
    keeps run history and state files for a workspace. This can be used to comply with
    data retention requirements or to reduce resource usage.

    API endpoint: POST /workspaces/{workspace_id}/relationships/data-retention-policy

    Args:
        workspace_id: The ID of the workspace (format: "ws-xxxxxxxx")
        days: Number of days to retain data

    Returns:
        The created data retention policy with configuration details and timestamps

    See:
        docs/tools/workspace.md for reference documentation
    """
    # Create request using Pydantic model
    request = DataRetentionPolicyRequest(workspace_id=workspace_id, days=days)

    # Create API payload using utility function
    payload = create_api_payload(
        resource_type="data-retention-policy",
        model=request,
        exclude_fields={"workspace_id"},
    )

    # Make API request
    return await api_request(
        f"workspaces/{workspace_id}/relationships/data-retention-policy",
        method="POST",
        data=payload,
    )


@handle_api_errors
async def get_data_retention_policy(workspace_id: str) -> APIResponse:
    """Get the data retention policy for a workspace.

    Retrieves the current data retention policy for a workspace, which defines how long
    Terraform Cloud keeps run history and state files before automatic removal.

    API endpoint: GET /workspaces/{workspace_id}/relationships/data-retention-policy

    Args:
        workspace_id: The ID of the workspace (format: "ws-xxxxxxxx")

    Returns:
        The data retention policy with configuration details and timestamps

    See:
        docs/tools/workspace.md for reference documentation
    """
    # Make API request
    return await api_request(
        f"workspaces/{workspace_id}/relationships/data-retention-policy", method="GET"
    )


@handle_api_errors
async def delete_data_retention_policy(workspace_id: str) -> APIResponse:
    """Delete the data retention policy for a workspace.

    Removes the data retention policy from a workspace, reverting to the default behavior
    of retaining all data indefinitely. This is useful when you no longer want to automatically
    remove historical data after a certain period.

    API endpoint: DELETE /workspaces/{workspace_id}/relationships/data-retention-policy

    Args:
        workspace_id: The ID of the workspace (format: "ws-xxxxxxxx")

    Returns:
        Empty response with HTTP 204 status code indicating successful deletion

    See:
        docs/tools/workspace.md for reference documentation
    """
    # Make API request
    return await api_request(
        f"workspaces/{workspace_id}/relationships/data-retention-policy",
        method="DELETE",
    )


@handle_api_errors
async def get_workspace_details(
    workspace_id: str = "", organization: str = "", workspace_name: str = ""
) -> APIResponse:
    """Get details for a specific workspace, identified either by ID or by org name and workspace name.

    Retrieves comprehensive information about a workspace including its configuration,
    VCS settings, execution mode, and other attributes. This is useful for checking
    workspace settings before operations or determining the current state of a workspace.

    The workspace can be identified either by its ID directly, or by the combination
    of organization name and workspace name.

    API endpoint:
    - GET /workspaces/{workspace_id} (when using workspace_id)
    - GET /organizations/{organization}/workspaces/{workspace_name} (when using org+name)

    Args:
        workspace_id: The ID of the workspace (format: "ws-xxxxxxxx")
        organization: The name of the organization (required if workspace_id not provided)
        workspace_name: The name of the workspace (required if workspace_id not provided)

    Returns:
        Comprehensive workspace details including settings, configuration and status

    See:
        docs/tools/workspace.md for reference documentation
    """
    # Ensure we have either workspace_id OR both organization and workspace_name
    if not workspace_id and not (organization and workspace_name):
        raise ValueError(
            "Either workspace_id OR both organization and workspace_name must be provided"
        )

    # Determine API path based on provided parameters
    if workspace_id:
        path = f"workspaces/{workspace_id}"
    else:
        path = f"organizations/{organization}/workspaces/{workspace_name}"

    # Make API request
    return await api_request(path, method="GET")
