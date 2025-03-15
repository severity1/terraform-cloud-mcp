"""Run management tools for Terraform Cloud MCP"""

from typing import Optional, List, Dict, Any, Union

from api.client import make_api_request
from utils.validators import validate_organization

# Run operation constants
RUN_OPERATIONS = ["plan_only", "plan_and_apply", "save_plan", "refresh_only", "destroy", "empty_apply"]

# Run status constants 
RUN_STATUSES = ["pending", "fetching", "fetching_completed", "pre_plan_running", 
                "pre_plan_completed", "queuing", "plan_queued", "planning", "planned", 
                "cost_estimating", "cost_estimated", "policy_checking", "policy_override", 
                "policy_soft_failed", "policy_checked", "confirmed", "post_plan_running", 
                "post_plan_completed", "planned_and_finished", "planned_and_saved", 
                "apply_queued", "applying", "applied", "discarded", "errored", 
                "canceled", "force_canceled"]

# Run sources
RUN_SOURCES = ["tfe-ui", "tfe-api", "tfe-configuration-version"]

# Run status groups
RUN_STATUS_GROUPS = ["non_final", "final", "discardable"]

async def create_run(
    organization: str,
    workspace_name: str,
    message: str = "",
    auto_apply: Optional[bool] = None,
    is_destroy: bool = False,
    refresh: bool = True,
    refresh_only: bool = False,
    plan_only: bool = False,
    allow_empty_apply: bool = False,
    allow_config_generation: bool = False,
    target_addrs: List[str] = [],
    replace_addrs: List[str] = [],
    variables: List[Dict[str, str]] = [],
    terraform_version: str = "",
    save_plan: bool = False,
    configuration_version_id: str = "",
    debugging_mode: bool = False
) -> dict:
    """
    Create a run in a workspace
    
    Args:
        organization: The organization name (required)
        workspace_name: The name of the workspace to run in (required)
        message: Message to include with the run (default: "Queued manually via Terraform Cloud MCP")
        auto_apply: Whether to auto-apply the run when planned (defaults to workspace setting)
        is_destroy: Whether this run should destroy all resources (default: false)
        refresh: Whether to refresh state before plan (default: true)
        refresh_only: Whether this is a refresh-only run (default: false)
        plan_only: Whether this is a speculative, plan-only run (default: false)
        allow_empty_apply: Whether to allow apply when there are no changes (default: false)
        allow_config_generation: Whether to allow generating config for imports (default: false)
        target_addrs: Resource addresses to target (optional)
        replace_addrs: Resource addresses to replace (optional)
        variables: Run-specific variables [{"key": "name", "value": "value"}] (optional)
        terraform_version: Specific Terraform version (only valid for plan-only runs)
        save_plan: Whether to save the plan without becoming the current run (default: false)
        configuration_version_id: The configuration version ID to use (defaults to workspace's latest)
        debugging_mode: Enable debug logging for this run (default: false)
        
    Returns:
        The created run details
    """
    
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}
    
    if not workspace_name:
        return {"error": "Workspace name is required"}
    
    # Validate mutually exclusive options
    if is_destroy and refresh_only:
        return {"error": "is_destroy and refresh_only are mutually exclusive"}
    
    # First, get the workspace ID (required for creating a run)
    success, workspace_data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}"
    )
    
    if not success:
        return workspace_data  # Return error from workspace lookup
    
    # Extract the workspace ID
    try:
        workspace_id = workspace_data["data"]["id"]
    except (KeyError, TypeError):
        return {"error": "Failed to get workspace ID"}
    
    # Build the request payload
    payload: Dict[str, Any] = {
        "data": {
            "type": "runs",
            "relationships": {
                "workspace": {
                    "data": {
                        "type": "workspaces",
                        "id": workspace_id
                    }
                }
            }
        }
    }
    
    # Add configuration version if specified
    if configuration_version_id:
        payload["data"]["relationships"]["configuration-version"] = {
            "data": {
                "type": "configuration-versions",
                "id": configuration_version_id
            }
        }
    
    # Add attributes
    payload["data"]["attributes"] = {}
    
    # Add message if specified (with default if not provided)
    if message:
        payload["data"]["attributes"]["message"] = message
    else:
        payload["data"]["attributes"]["message"] = "Queued manually via Terraform Cloud MCP"
    
    # Add boolean attributes
    if auto_apply is not None:
        payload["data"]["attributes"]["auto-apply"] = auto_apply
    
    if is_destroy:
        payload["data"]["attributes"]["is-destroy"] = True
    
    if not refresh:  # Only add if different from default (true)
        payload["data"]["attributes"]["refresh"] = False
    
    if refresh_only:
        payload["data"]["attributes"]["refresh-only"] = True
    
    if plan_only:
        payload["data"]["attributes"]["plan-only"] = True
    
    if allow_empty_apply:
        payload["data"]["attributes"]["allow-empty-apply"] = True
    
    if allow_config_generation:
        payload["data"]["attributes"]["allow-config-generation"] = True
    
    if save_plan:
        payload["data"]["attributes"]["save-plan"] = True
    
    if debugging_mode:
        payload["data"]["attributes"]["debugging-mode"] = True
    
    # Add terraform version (only valid for plan-only runs)
    if terraform_version:
        if not plan_only:
            return {"error": "terraform_version can only be set for plan-only runs"}
        payload["data"]["attributes"]["terraform-version"] = terraform_version
    
    # Add target and replace addresses if specified
    if target_addrs:
        payload["data"]["attributes"]["target-addrs"] = target_addrs
    
    if replace_addrs:
        payload["data"]["attributes"]["replace-addrs"] = replace_addrs
    
    # Add run variables if specified
    if variables:
        payload["data"]["attributes"]["variables"] = variables
    
    # Make the API request
    success, data = await make_api_request(
        "runs",
        method="POST",
        data=payload
    )
    
    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary

async def list_runs_in_workspace(
    organization: str,
    workspace_name: str,
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
    search_basic: str = ""
) -> dict:
    """
    List runs in a workspace with comprehensive filtering and pagination
    
    Args:
        organization: The organization name (required)
        workspace_name: The workspace name to list runs for (required)
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
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}
    
    if not workspace_name:
        return {"error": "Workspace name is required"}
    
    # First, get the workspace ID (required for listing runs)
    success, workspace_data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}"
    )
    
    if not success:
        return workspace_data  # Return error from workspace lookup
    
    # Extract the workspace ID
    try:
        workspace_id = workspace_data["data"]["id"]
    except (KeyError, TypeError):
        return {"error": "Failed to get workspace ID"}
    
    # Build query parameters
    params: Dict[str, Union[str, int]] = {
        "page[number]": page_number,
        "page[size]": page_size
    }
    
    # Add filters if specified
    if filter_operation:
        params["filter[operation]"] = filter_operation
    
    if filter_status:
        params["filter[status]"] = filter_status
    
    if filter_source:
        params["filter[source]"] = filter_source
    
    if filter_status_group:
        params["filter[status_group]"] = filter_status_group
    
    if filter_timeframe:
        params["filter[timeframe]"] = filter_timeframe
        
    if filter_agent_pool_names:
        params["filter[agent_pool_names]"] = filter_agent_pool_names
    
    # Add search parameters if specified
    if search_user:
        params["search[user]"] = search_user
    
    if search_commit:
        params["search[commit]"] = search_commit
    
    if search_basic:
        params["search[basic]"] = search_basic
    
    # Make the API request
    success, data = await make_api_request(
        f"workspaces/{workspace_id}/runs",
        method="GET",
        params=params
    )
    
    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary
        
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
    search_basic: str = ""
) -> dict:
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
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}
    
    # Build query parameters
    params: Dict[str, Union[str, int]] = {
        "page[number]": page_number,
        "page[size]": page_size
    }
    
    # Add filters if specified
    if filter_operation:
        params["filter[operation]"] = filter_operation
    
    if filter_status:
        params["filter[status]"] = filter_status
    
    if filter_source:
        params["filter[source]"] = filter_source
    
    if filter_status_group:
        params["filter[status_group]"] = filter_status_group
    
    if filter_timeframe:
        params["filter[timeframe]"] = filter_timeframe
        
    if filter_agent_pool_names:
        params["filter[agent_pool_names]"] = filter_agent_pool_names
        
    if filter_workspace_names:
        params["filter[workspace_names]"] = filter_workspace_names
    
    # Add search parameters if specified
    if search_user:
        params["search[user]"] = search_user
    
    if search_commit:
        params["search[commit]"] = search_commit
    
    if search_basic:
        params["search[basic]"] = search_basic
    
    # Make the API request
    success, data = await make_api_request(
        f"organizations/{organization}/runs",
        method="GET",
        params=params
    )
    
    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary
        
async def get_run_details(
    run_id: str
) -> dict:
    """
    Get detailed information about a specific run
    
    Args:
        run_id: The ID of the run to retrieve details for (required)
        
    Returns:
        The run details
    """
    if not run_id:
        return {"error": "Run ID is required"}
    
    # Make the API request
    success, data = await make_api_request(
        f"runs/{run_id}",
        method="GET"
    )
    
    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary
        
async def apply_run(
    run_id: str,
    comment: str = ""
) -> dict:
    """
    Apply a run that is paused waiting for confirmation after a plan
    
    This applies runs in the "needs confirmation" and "policy checked" states.
    
    Args:
        run_id: The ID of the run to apply (required)
        comment: An optional comment about the run
        
    Returns:
        Success message or error details
    """
    if not run_id:
        return {"error": "Run ID is required"}
    
    # Build the request payload with optional comment
    payload = {}
    if comment:
        payload = {"comment": comment}
        
    # Make the API request
    success, data = await make_api_request(
        f"runs/{run_id}/actions/apply",
        method="POST",
        data=payload
    )
    
    if success:
        return {"status": "success", "message": "Run apply has been queued"}
    else:
        return data  # Error info is already in the data dictionary
        
async def discard_run(
    run_id: str,
    comment: str = ""
) -> dict:
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
    if not run_id:
        return {"error": "Run ID is required"}
    
    # Build the request payload with optional comment
    payload = {}
    if comment:
        payload = {"comment": comment}
        
    # Make the API request
    success, data = await make_api_request(
        f"runs/{run_id}/actions/discard",
        method="POST",
        data=payload
    )
    
    if success:
        return {"status": "success", "message": "Run discard has been queued"}
    else:
        return data  # Error info is already in the data dictionary
        
async def cancel_run(
    run_id: str,
    comment: str = ""
) -> dict:
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
    if not run_id:
        return {"error": "Run ID is required"}
    
    # Build the request payload with optional comment
    payload = {}
    if comment:
        payload = {"comment": comment}
        
    # Make the API request
    success, data = await make_api_request(
        f"runs/{run_id}/actions/cancel",
        method="POST",
        data=payload
    )
    
    if success:
        return {"status": "success", "message": "Run cancel has been queued"}
    else:
        return data  # Error info is already in the data dictionary
        
async def force_cancel_run(
    run_id: str,
    comment: str = ""
) -> dict:
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
    if not run_id:
        return {"error": "Run ID is required"}
    
    # Build the request payload with optional comment
    payload = {}
    if comment:
        payload = {"comment": comment}
        
    # Make the API request
    success, data = await make_api_request(
        f"runs/{run_id}/actions/force-cancel",
        method="POST",
        data=payload
    )
    
    if success:
        return {"status": "success", "message": "Run has been force canceled"}
    else:
        return data  # Error info is already in the data dictionary
        
async def force_execute_run(
    run_id: str
) -> dict:
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
    if not run_id:
        return {"error": "Run ID is required"}
    
    # Make the API request (no payload)
    success, data = await make_api_request(
        f"runs/{run_id}/actions/force-execute",
        method="POST"
    )
    
    if success:
        return {"status": "success", "message": "Run force-execution has been initiated"}
    else:
        return data  # Error info is already in the data dictionary