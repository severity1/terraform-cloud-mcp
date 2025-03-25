"""Run management tools for Terraform Cloud API.

This module provides tools for managing runs in Terraform Cloud.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run
"""

from typing import Optional

from api.client import api_request
from utils.decorators import handle_api_errors
from models.base import APIResponse
from models.runs import (
    RunListInWorkspaceRequest,
    RunListInOrganizationRequest,
    RunCreateRequest,
    RunActionRequest,
    RunParams,
)


@handle_api_errors
async def create_run(
    workspace_id: str,
    params: Optional[RunParams] = None,
) -> APIResponse:
    """
    Create a run in a workspace

    Args:
        workspace_id: The workspace ID to execute the run in (required, format: "ws-xxxxxxxx")
        params: Additional run parameters (optional)

    Returns:
        The created run details
    """
    # Extract parameters from the params object if provided
    param_dict = params.model_dump(exclude_none=True) if params else {}

    # Create request using Pydantic model
    request = RunCreateRequest(
        workspace_id=workspace_id, **param_dict
    )

    # Extract variables for special handling if present
    variables = request.variables

    # Extract attributes for payload, excluding routing fields
    attributes = request.model_dump(
        by_alias=True,
        exclude={"workspace_id", "variables"},
        exclude_none=True,
    )

    # Create API payload
    payload = {
        "data": {
            "type": "runs",
            "attributes": attributes,
            "relationships": {
                "workspace": {
                    "data": {
                        "type": "workspaces",
                        "id": workspace_id,
                    }
                }
            },
        }
    }

    # Add configuration version relationship if specified
    if request.configuration_version_id:
        payload["data"]["relationships"]["configuration-version"] = {
            "data": {
                "type": "configuration-versions",
                "id": request.configuration_version_id,
            }
        }

    # Add variables if present
    if variables:
        payload["data"]["attributes"]["variables"] = [
            {"key": var.key, "value": var.value} for var in variables
        ]

    # Make API request
    return await api_request("runs", method="POST", data=payload)


@handle_api_errors
async def list_runs_in_workspace(
    workspace_id: str,
    page_number: int = 1,
    page_size: int = 20,
    filter_operation: str = "",
    filter_status: str = "",
    filter_source: str = "",
    filter_status_group: str = "",
    filter_timeframe: str = "",
    filter_agent_pool_names: str = "",
    search_user: str = "",
    search_commit: str = "",
    search_basic: str = "",
) -> APIResponse:
    """
    List runs in a workspace with comprehensive filtering and pagination

    Args:
        workspace_id: The workspace ID to list runs for (required, format: "ws-xxxxxxxx")
        page_number: Page number to fetch (default: 1)
        page_size: Number of results per page (default: 20)
        filter_operation: Filter runs by operation type, comma-separated (e.g. "plan_only,plan_and_apply")
        filter_status: Filter runs by status, comma-separated (e.g. "planned,applied,errored")
        filter_source: Filter runs by source, comma-separated (e.g. "tfe-api,tfe-ui")
        filter_status_group: Filter runs by status group (e.g. "non_final", "final", "discardable")
        filter_timeframe: Filter runs by timeframe ("year" or specific year)
        filter_agent_pool_names: Filter runs by agent pool names, comma-separated
        search_user: Search for runs by VCS username
        search_commit: Search for runs by commit SHA
        search_basic: Basic search across run ID, message, commit SHA, and username

    Returns:
        List of runs with pagination information
    """
    # Create request using Pydantic model for validation
    request = RunListInWorkspaceRequest(
        workspace_id=workspace_id,
        page_number=page_number,
        page_size=page_size,
        filter_operation=filter_operation,
        filter_status=filter_status,
        filter_source=filter_source,
        filter_status_group=filter_status_group,
        filter_timeframe=filter_timeframe,
        filter_agent_pool_names=filter_agent_pool_names,
        search_user=search_user,
        search_commit=search_commit,
        search_basic=search_basic,
    )

    # Construct query parameters
    params = {
        "page[number]": str(request.page_number),
        "page[size]": str(request.page_size),
    }

    # Add optional filter and search parameters
    if request.filter_operation:
        params["filter[operation]"] = request.filter_operation
    if request.filter_status:
        params["filter[status]"] = request.filter_status
    if request.filter_source:
        params["filter[source]"] = request.filter_source
    if request.filter_status_group:
        params["filter[status_group]"] = request.filter_status_group
    if request.filter_timeframe:
        params["filter[timeframe]"] = request.filter_timeframe
    if request.filter_agent_pool_names:
        params["filter[agent_pool_names]"] = request.filter_agent_pool_names
    if request.search_user:
        params["search[user]"] = request.search_user
    if request.search_commit:
        params["search[commit]"] = request.search_commit
    if request.search_basic:
        params["search[basic]"] = request.search_basic

    # Make API request
    return await api_request(
        f"workspaces/{workspace_id}/runs", method="GET", params=params
    )


@handle_api_errors
async def list_runs_in_organization(
    organization: str,
    page_number: int = 1,
    page_size: int = 20,
    filter_operation: str = "",
    filter_status: str = "",
    filter_source: str = "",
    filter_status_group: str = "",
    filter_timeframe: str = "",
    filter_agent_pool_names: str = "",
    filter_workspace_names: str = "",
    search_user: str = "",
    search_commit: str = "",
    search_basic: str = "",
) -> APIResponse:
    """
    List runs in an organization with comprehensive filtering and pagination

    Args:
        organization: The organization name (required)
        page_number: Page number to fetch (default: 1)
        page_size: Number of results per page (default: 20)
        filter_operation: Filter runs by operation type, comma-separated (e.g. "plan_only,plan_and_apply")
        filter_status: Filter runs by status, comma-separated (e.g. "planned,applied,errored")
        filter_source: Filter runs by source, comma-separated (e.g. "tfe-api,tfe-ui")
        filter_status_group: Filter runs by status group (e.g. "non_final", "final", "discardable")
        filter_timeframe: Filter runs by timeframe ("year" or specific year)
        filter_agent_pool_names: Filter runs by agent pool names, comma-separated
        filter_workspace_names: Filter runs by workspace names, comma-separated
        search_user: Search for runs by VCS username
        search_commit: Search for runs by commit SHA
        search_basic: Basic search across run ID, message, commit SHA, and username

    Returns:
        List of runs with pagination information
    """
    # Create request using Pydantic model for validation
    request = RunListInOrganizationRequest(
        organization=organization,
        page_number=page_number,
        page_size=page_size,
        filter_operation=filter_operation,
        filter_status=filter_status,
        filter_source=filter_source,
        filter_status_group=filter_status_group,
        filter_timeframe=filter_timeframe,
        filter_agent_pool_names=filter_agent_pool_names,
        filter_workspace_names=filter_workspace_names,
        search_user=search_user,
        search_commit=search_commit,
        search_basic=search_basic,
    )

    # Construct query parameters
    params = {
        "page[number]": str(request.page_number),
        "page[size]": str(request.page_size),
    }

    # Add optional filter and search parameters
    if request.filter_operation:
        params["filter[operation]"] = request.filter_operation
    if request.filter_status:
        params["filter[status]"] = request.filter_status
    if request.filter_source:
        params["filter[source]"] = request.filter_source
    if request.filter_status_group:
        params["filter[status_group]"] = request.filter_status_group
    if request.filter_timeframe:
        params["filter[timeframe]"] = request.filter_timeframe
    if request.filter_agent_pool_names:
        params["filter[agent_pool_names]"] = request.filter_agent_pool_names
    if request.filter_workspace_names:
        params["filter[workspace_names]"] = request.filter_workspace_names
    if request.search_user:
        params["search[user]"] = request.search_user
    if request.search_commit:
        params["search[commit]"] = request.search_commit
    if request.search_basic:
        params["search[basic]"] = request.search_basic

    # Make API request
    return await api_request(
        f"organizations/{organization}/runs", method="GET", params=params
    )


@handle_api_errors
async def get_run_details(run_id: str) -> APIResponse:
    """
    Get detailed information about a specific run

    Args:
        run_id: The ID of the run to retrieve details for (required)

    Returns:
        The run details
    """
    # Make API request
    return await api_request(f"runs/{run_id}", method="GET")


@handle_api_errors
async def apply_run(run_id: str, comment: str = "") -> APIResponse:
    """
    Apply a run that is paused waiting for confirmation after a plan

    This applies runs in the "needs confirmation" and "policy checked" states.

    Args:
        run_id: The ID of the run to apply (required)
        comment: An optional comment about the run

    Returns:
        Success message or error details
    """
    request = RunActionRequest(run_id=run_id, comment=comment)

    # Create payload if comment is provided
    payload = None
    if request.comment:
        payload = {"comment": request.comment}

    # Make API request
    return await api_request(
        f"runs/{run_id}/actions/apply", method="POST", data=payload
    )


@handle_api_errors
async def discard_run(run_id: str, comment: str = "") -> APIResponse:
    """
    Discard a run that is paused waiting for confirmation

    This discards runs in the "pending", "needs confirmation", "policy checked",
    and "policy override" states.

    Args:
        run_id: The ID of the run to discard (required)
        comment: An optional explanation for why the run was discarded

    Returns:
        Success message or error details
    """
    request = RunActionRequest(run_id=run_id, comment=comment)

    # Create payload if comment is provided
    payload = None
    if request.comment:
        payload = {"comment": request.comment}

    # Make API request
    return await api_request(
        f"runs/{run_id}/actions/discard", method="POST", data=payload
    )


@handle_api_errors
async def cancel_run(run_id: str, comment: str = "") -> APIResponse:
    """
    Cancel a run that is currently planning or applying

    This is equivalent to hitting ctrl+c during a Terraform plan or apply on the CLI.
    The running Terraform process is sent an INT signal to end its work safely.

    Args:
        run_id: The ID of the run to cancel (required)
        comment: An optional explanation for why the run was canceled

    Returns:
        Success message or error details
    """
    request = RunActionRequest(run_id=run_id, comment=comment)

    # Create payload if comment is provided
    payload = None
    if request.comment:
        payload = {"comment": request.comment}

    # Make API request
    return await api_request(
        f"runs/{run_id}/actions/cancel", method="POST", data=payload
    )


@handle_api_errors
async def force_cancel_run(run_id: str, comment: str = "") -> APIResponse:
    """
    Forcefully cancel a run immediately

    Unlike cancel_run, this action ends the run immediately and places it
    into a canceled state. The workspace is immediately unlocked.

    Note: This endpoint requires that a normal cancel is performed first,
    and a cool-off period has elapsed.

    Args:
        run_id: The ID of the run to force cancel (required)
        comment: An optional explanation for why the run was force canceled

    Returns:
        Success message or error details
    """
    request = RunActionRequest(run_id=run_id, comment=comment)

    # Create payload if comment is provided
    payload = None
    if request.comment:
        payload = {"comment": request.comment}

    # Make API request
    return await api_request(
        f"runs/{run_id}/actions/force-cancel", method="POST", data=payload
    )


@handle_api_errors
async def force_execute_run(run_id: str) -> APIResponse:
    """
    Forcefully execute a run by canceling all prior runs

    This action cancels all prior runs that are not already complete,
    unlocking the run's workspace and allowing the run to be executed.
    This is the same as clicking "Run this plan now" in the UI.

    Prerequisites:
    - The target run must be in the "pending" state
    - The workspace must be locked by another run
    - The run locking the workspace must be in a discardable state

    Args:
        run_id: The ID of the run to execute (required)

    Returns:
        Success message or error details
    """
    # Make API request
    return await api_request(f"runs/{run_id}/actions/force-execute", method="POST")
