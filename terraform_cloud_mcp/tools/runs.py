"""Run management tools for Terraform Cloud API.

This module provides tools for managing runs in Terraform Cloud.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run
"""

from typing import Optional

from ..api.client import api_request
from ..utils.decorators import handle_api_errors
from ..utils.payload import create_api_payload, add_relationship
from ..utils.request import query_params
from ..models.base import APIResponse
from ..models.runs import (
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
    """Create a run in a workspace

    Creates a new Terraform run to trigger infrastructure changes through Terraform Cloud,
    representing a single execution of plan and apply operations. The run queues in the
    workspace and executes based on the workspace's execution mode and settings. Use this
    to deploy new infrastructure, apply configuration changes, or destroy resources.

    API endpoint: POST /runs

    Args:
        workspace_id: The workspace ID to execute the run in (format: "ws-xxxxxxxx")
        params: Optional run configuration with:
            - message: Description of the run's purpose
            - is_destroy: Whether to destroy all resources managed by the workspace
            - auto_apply: Whether to auto-apply after a successful plan
            - refresh: Whether to refresh Terraform state before planning
            - refresh_only: Only refresh the state without planning changes
            - plan_only: Create a speculative plan without applying
            - allow_empty_apply: Allow applying when there are no changes
            - target_addrs: List of resource addresses to specifically target
            - replace_addrs: List of resource addresses to force replacement
            - variables: Run-specific variables that override workspace variables
            - terraform_version: Specific Terraform version to use for this run
            - save_plan: Save the plan for later execution
            - debugging_mode: Enable extended debug logging

    Returns:
        The created run details with ID, status, configuration information,
        workspace relationship, and links to associated resources

    See:
        docs/tools/run.md for reference documentation
    """
    # Convert optional params to dictionary
    param_dict = params.model_dump(exclude_none=True) if params else {}

    # Create validated request object
    request = RunCreateRequest(workspace_id=workspace_id, **param_dict)

    # Extract variables for special handling
    variables = request.variables

    # Create API payload using utility function
    payload = create_api_payload(
        resource_type="runs",
        model=request,
        exclude_fields={"workspace_id", "variables"},  # Fields handled separately
    )

    # Add workspace relationship
    add_relationship(
        payload=payload,
        relation_name="workspace",
        resource_type="workspaces",
        resource_id=workspace_id,
    )

    # Add optional configuration version relationship
    if request.configuration_version_id:
        add_relationship(
            payload=payload,
            relation_name="configuration-version",
            resource_type="configuration-versions",
            resource_id=request.configuration_version_id,
        )

    # Transform variables to key-value format required by API
    if variables:
        payload["data"]["attributes"]["variables"] = [
            {"key": var.key, "value": var.value} for var in variables
        ]

    return await api_request("runs", method="POST", data=payload)


@handle_api_errors
async def list_runs_in_workspace(
    workspace_id: str,
    page_number: int = 1,
    page_size: int = 20,
    filter_operation: Optional[str] = None,
    filter_status: Optional[str] = None,
    filter_source: Optional[str] = None,
    filter_status_group: Optional[str] = None,
    filter_timeframe: Optional[str] = None,
    filter_agent_pool_names: Optional[str] = None,
    search_user: Optional[str] = None,
    search_commit: Optional[str] = None,
    search_basic: Optional[str] = None,
) -> APIResponse:
    """List runs in a workspace with filtering and pagination

    Retrieves run history for a specific workspace with options to filter by status,
    operation type, source, and other criteria. Useful for auditing changes, troubleshooting,
    or monitoring deployment history.

    API endpoint: GET /workspaces/{workspace_id}/runs

    Args:
        workspace_id: The workspace ID to list runs for (format: "ws-xxxxxxxx")
        page_number: Page number to fetch (default: 1)
        page_size: Number of results per page (default: 20)
        filter_operation: Filter by operation type
        filter_status: Filter by status
        filter_source: Filter by source
        filter_status_group: Filter by status group
        filter_timeframe: Filter by timeframe
        filter_agent_pool_names: Filter by agent pool names
        search_user: Search by VCS username
        search_commit: Search by commit SHA
        search_basic: Search across run ID, message, commit SHA, and username

    Returns:
        List of runs with metadata, status info, and pagination details

    See:
        docs/tools/run.md for reference documentation
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

    # Use the unified query params utility function
    params = query_params(request)

    # Make API request
    return await api_request(
        f"workspaces/{workspace_id}/runs", method="GET", params=params
    )


@handle_api_errors
async def list_runs_in_organization(
    organization: str,
    page_number: int = 1,
    page_size: int = 20,
    filter_operation: Optional[str] = None,
    filter_status: Optional[str] = None,
    filter_source: Optional[str] = None,
    filter_status_group: Optional[str] = None,
    filter_timeframe: Optional[str] = None,
    filter_agent_pool_names: Optional[str] = None,
    filter_workspace_names: Optional[str] = None,
    search_user: Optional[str] = None,
    search_commit: Optional[str] = None,
    search_basic: Optional[str] = None,
) -> APIResponse:
    """List runs across all workspaces in an organization

    Retrieves run history across all workspaces in an organization with powerful filtering.
    Useful for organization-wide auditing, monitoring deployments across teams, or finding
    specific runs by commit or author.

    API endpoint: GET /organizations/{organization}/runs

    Args:
        organization: The organization name
        page_number: Page number to fetch (default: 1)
        page_size: Number of results per page (default: 20)
        filter_operation: Filter by operation type
        filter_status: Filter by status
        filter_source: Filter by source
        filter_status_group: Filter by status group
        filter_timeframe: Filter by timeframe
        filter_agent_pool_names: Filter by agent pool names
        filter_workspace_names: Filter by workspace names
        search_user: Search by VCS username
        search_commit: Search by commit SHA
        search_basic: Basic search across run attributes

    Returns:
        List of runs across workspaces with metadata and pagination details

    See:
        docs/tools/run.md for reference documentation
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

    # Use the unified query params utility function
    params = query_params(request)

    # Make API request
    return await api_request(
        f"organizations/{organization}/runs", method="GET", params=params
    )


@handle_api_errors
async def get_run_details(run_id: str) -> APIResponse:
    """Get detailed information about a specific run

    Retrieves comprehensive information about a run including its current status,
    plan output, and relationship to other resources. Use to check run progress or results.

    API endpoint: GET /runs/{run_id}

    Args:
        run_id: The ID of the run to retrieve details for (format: "run-xxxxxxxx")

    Returns:
        Complete run details including status, plan, and relationships

    See:
        docs/tools/run.md for reference documentation
    """
    # Make API request
    return await api_request(f"runs/{run_id}", method="GET")


@handle_api_errors
async def apply_run(run_id: str, comment: str = "") -> APIResponse:
    """Apply a run that is paused waiting for confirmation after a plan

    Confirms and executes the apply phase for a run that has completed planning and is
    waiting for approval. Use this when you've reviewed the plan output and want to
    apply the proposed changes to your infrastructure.

    API endpoint: POST /runs/{run_id}/actions/apply

    Args:
        run_id: The ID of the run to apply (format: "run-xxxxxxxx")
        comment: An optional comment explaining the reason for applying the run

    Returns:
        Run details with updated status information and confirmation of the apply action
        including timestamp information and any comment provided

    See:
        docs/tools/run.md for reference documentation
    """
    request = RunActionRequest(run_id=run_id, comment=comment)

    # Create payload if comment is provided
    payload = {}
    if request.comment:
        payload = {"comment": request.comment}

    # Make API request
    return await api_request(
        f"runs/{run_id}/actions/apply", method="POST", data=payload
    )


@handle_api_errors
async def discard_run(run_id: str, comment: str = "") -> APIResponse:
    """Discard a run that is paused waiting for confirmation

    Cancels a run without applying its changes, typically used when the plan
    shows undesired changes or after reviewing and rejecting a plan. This action
    removes the run from the queue and unlocks the workspace for new runs.

    API endpoint: POST /runs/{run_id}/actions/discard

    Args:
        run_id: The ID of the run to discard (format: "run-xxxxxxxx")
        comment: An optional explanation for why the run was discarded

    Returns:
        Run status update with discarded state information, timestamp of the
        discard action, and user information

    See:
        docs/tools/run.md for reference documentation
    """
    request = RunActionRequest(run_id=run_id, comment=comment)

    # Create payload if comment is provided
    payload = {}
    if request.comment:
        payload = {"comment": request.comment}

    # Make API request
    return await api_request(
        f"runs/{run_id}/actions/discard", method="POST", data=payload
    )


@handle_api_errors
async def cancel_run(run_id: str, comment: str = "") -> APIResponse:
    """Cancel a run that is currently planning or applying

    Gracefully stops an in-progress run during planning or applying phases. Use this
    when you need to stop a run that's taking too long, consuming too many resources,
    or needs to be stopped for any reason. The operation attempts to cleanly terminate
    the run by sending an interrupt signal.

    API endpoint: POST /runs/{run_id}/actions/cancel

    Args:
        run_id: The ID of the run to cancel (format: "run-xxxxxxxx")
        comment: An optional explanation for why the run was canceled

    Returns:
        Run status update with canceled state, timestamp of cancellation,
        and any provided comment in the response metadata

    See:
        docs/tools/run.md for reference documentation
    """
    request = RunActionRequest(run_id=run_id, comment=comment)

    # Create payload if comment is provided
    payload = {}
    if request.comment:
        payload = {"comment": request.comment}

    # Make API request
    return await api_request(
        f"runs/{run_id}/actions/cancel", method="POST", data=payload
    )


@handle_api_errors
async def force_cancel_run(run_id: str, comment: str = "") -> APIResponse:
    """Forcefully cancel a run immediately

    Immediately terminates a run that hasn't responded to a normal cancel request.
    Use this as a last resort when a run is stuck and not responding to regular
    cancellation. This action bypasses the graceful shutdown process and forces
    the workspace to be unlocked.

    API endpoint: POST /runs/{run_id}/actions/force-cancel

    Args:
        run_id: The ID of the run to force cancel (format: "run-xxxxxxxx")
        comment: An optional explanation for why the run was force canceled

    Returns:
        Run status update confirming forced cancellation with timestamp,
        user information, and workspace unlock status

    See:
        docs/tools/run.md for reference documentation
    """
    request = RunActionRequest(run_id=run_id, comment=comment)

    # Create payload if comment is provided
    payload = {}
    if request.comment:
        payload = {"comment": request.comment}

    # Make API request
    return await api_request(
        f"runs/{run_id}/actions/force-cancel", method="POST", data=payload
    )


@handle_api_errors
async def force_execute_run(run_id: str) -> APIResponse:
    """Forcefully execute a run by canceling all prior runs

    Prioritizes a specific run by canceling other queued runs to unlock the workspace,
    equivalent to clicking "Run this plan now" in the UI. Use this when a run is
    stuck in the pending queue but needs immediate execution due to urgency or
    priority over other queued runs.

    API endpoint: POST /runs/{run_id}/actions/force-execute

    Args:
        run_id: The ID of the run to execute (format: "run-xxxxxxxx")

    Returns:
        Status update confirming the run has been promoted to active status,
        with information about which runs were canceled to allow execution

    See:
        docs/tools/run.md for reference documentation
    """
    # Make API request
    return await api_request(f"runs/{run_id}/actions/force-execute", method="POST")
