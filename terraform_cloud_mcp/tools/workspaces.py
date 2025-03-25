"""Terraform Cloud Workspace Management Tools

This module provides tools for managing workspaces in Terraform Cloud.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces
"""

from typing import Optional

from api.client import api_request
from utils.decorators import handle_api_errors
from models.base import APIResponse
from models.workspaces import (
    WorkspaceCreateRequest,
    WorkspaceUpdateRequest,
    WorkspaceListRequest,
    WorkspaceParams,
)


@handle_api_errors
async def create_workspace(
    organization: str, name: str, params: Optional[WorkspaceParams] = None
) -> APIResponse:
    """
    Create a new workspace in an organization.

    Args:
        organization: The name of the organization
        name: The name to give the workspace
        params: Additional workspace parameters (optional)

    Returns:
        The created workspace data
    """
    # Extract parameters from the params object if provided
    param_dict = params.model_dump(exclude_none=True) if params else {}

    # Create request using Pydantic model
    request = WorkspaceCreateRequest(organization=organization, name=name, **param_dict)

    # Extract attributes for payload, excluding organization which is part of the URL
    attributes = request.model_dump(
        by_alias=True, exclude={"organization"}, exclude_none=True
    )

    # Create API payload
    payload = {"data": {"type": "workspaces", "attributes": attributes}}

    # Make API request
    return await api_request(
        f"organizations/{organization}/workspaces", method="POST", data=payload
    )


@handle_api_errors
async def update_workspace(
    organization: str, workspace_name: str, params: Optional[WorkspaceParams] = None
) -> APIResponse:
    """
    Update an existing workspace.

    Args:
        organization: The name of the organization that owns the workspace
        workspace_name: The name of the workspace to update
        params: Workspace parameters to update (optional)

    Returns:
        The updated workspace data
    """
    # Extract parameters from the params object if provided
    param_dict = params.model_dump(exclude_none=True) if params else {}

    # Create request using Pydantic model
    request = WorkspaceUpdateRequest(
        organization=organization, workspace_name=workspace_name, **param_dict
    )

    # Extract attributes for payload, excluding fields not part of the attributes
    attributes = request.model_dump(
        by_alias=True,
        exclude={"organization", "workspace_name"},
        exclude_none=True,
    )

    # Create API payload
    payload = {"data": {"type": "workspaces", "attributes": attributes}}

    # Debug print
    print(f"DEBUG: Update workspace payload: {payload}")

    # Make API request
    response = await api_request(
        f"organizations/{organization}/workspaces/{workspace_name}",
        method="PATCH",
        data=payload,
    )

    # Debug print
    print(f"DEBUG: Update workspace response: {response}")

    return response


@handle_api_errors
async def list_workspaces(
    organization: str,
    page_number: int = 1,
    page_size: int = 20,
    search: str = "",
) -> APIResponse:
    """
    List workspaces in an organization.

    Args:
        organization: The name of the organization to list workspaces from
        page_number: The page number to return (default: 1)
        page_size: The number of items per page (default: 20, max: 100)
        search: Optional search string to filter workspaces

    Returns:
        Paginated list of workspaces
    """
    # Create request using Pydantic model for validation
    request = WorkspaceListRequest(
        organization=organization,
        page_number=page_number,
        page_size=page_size,
        search=search,
    )

    # Extract query parameters
    params = {
        "page[number]": str(request.page_number),
        "page[size]": str(request.page_size),
    }

    if request.search:
        params["search"] = request.search

    # Make API request
    return await api_request(
        f"organizations/{organization}/workspaces", method="GET", params=params
    )


@handle_api_errors
async def delete_workspace(organization: str, workspace_name: str) -> APIResponse:
    """
    Delete a workspace.

    Args:
        organization: The name of the organization that owns the workspace
        workspace_name: The name of the workspace to delete

    Returns:
        Success message
    """
    # Make API request
    return await api_request(
        f"organizations/{organization}/workspaces/{workspace_name}",
        method="DELETE",
    )


@handle_api_errors
async def safe_delete_workspace(organization: str, workspace_name: str) -> APIResponse:
    """
    Safely delete a workspace by first checking if it can be deleted.

    Args:
        organization: The name of the organization that owns the workspace
        workspace_name: The name of the workspace to delete

    Returns:
        Status of the safe delete operation
    """
    # Make API request
    return await api_request(
        f"organizations/{organization}/workspaces/{workspace_name}/actions/safe-delete",
        method="POST",
    )


@handle_api_errors
async def lock_workspace(workspace_id: str, reason: str = "") -> APIResponse:
    """
    Lock a workspace.

    Args:
        workspace_id: The ID of the workspace to lock
        reason: Optional reason for locking

    Returns:
        The locked workspace data
    """
    # Create payload if reason is provided
    payload = None
    if reason:
        payload = {"reason": reason}

    # Make API request
    return await api_request(
        f"workspaces/{workspace_id}/actions/lock", method="POST", data=payload
    )


@handle_api_errors
async def unlock_workspace(workspace_id: str) -> APIResponse:
    """
    Unlock a workspace.

    Args:
        workspace_id: The ID of the workspace to unlock

    Returns:
        The unlocked workspace data
    """
    # Make API request
    return await api_request(f"workspaces/{workspace_id}/actions/unlock", method="POST")


@handle_api_errors
async def force_unlock_workspace(workspace_id: str) -> APIResponse:
    """
    Force unlock a workspace. This should be used with caution.

    Args:
        workspace_id: The ID of the workspace to force unlock

    Returns:
        The unlocked workspace data
    """
    # Make API request
    return await api_request(
        f"workspaces/{workspace_id}/actions/force-unlock", method="POST"
    )


@handle_api_errors
async def set_data_retention_policy(workspace_id: str, days: int) -> APIResponse:
    """
    Set a data retention policy for a workspace.

    Args:
        workspace_id: The ID of the workspace
        days: Number of days to retain data

    Returns:
        The created data retention policy
    """
    # Create API payload
    payload = {"data": {"type": "data-retention-policy", "attributes": {"days": days}}}

    # Make API request
    return await api_request(
        f"workspaces/{workspace_id}/relationships/data-retention-policy",
        method="POST",
        data=payload,
    )


@handle_api_errors
async def get_data_retention_policy(workspace_id: str) -> APIResponse:
    """
    Get the data retention policy for a workspace.

    Args:
        workspace_id: The ID of the workspace

    Returns:
        The workspace data retention policy
    """
    # Make API request
    return await api_request(
        f"workspaces/{workspace_id}/relationships/data-retention-policy", method="GET"
    )


@handle_api_errors
async def delete_data_retention_policy(workspace_id: str) -> APIResponse:
    """
    Delete the data retention policy for a workspace.

    Args:
        workspace_id: The ID of the workspace

    Returns:
        Success message
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
    """
    Get details for a specific workspace, identified either by ID or by org name and workspace name.

    Args:
        workspace_id: The ID of the workspace (mutually exclusive with org+name)
        organization: The name of the organization (required if workspace_id not provided)
        workspace_name: The name of the workspace (required if workspace_id not provided)

    Returns:
        The workspace details
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
