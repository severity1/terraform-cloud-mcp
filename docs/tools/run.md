# Run Tools

This module provides tools for managing runs in Terraform Cloud.

## Overview

Runs in Terraform Cloud represent the process of executing Terraform operations (plan, apply) on a workspace. These tools allow you to create, list, and manage runs, including applying, discarding, and canceling them as needed.

## API Reference

These tools interact with the Terraform Cloud Runs API:
- [Runs API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run)
- [Run Workflow](https://developer.hashicorp.com/terraform/cloud-docs/run/states)

## Tools Reference

### create_run

**Function:** `create_run(workspace_id: str, params: Optional[RunParams] = None) -> Dict[str, Any]`

**Description:** Creates and queues a new Terraform run in a workspace.

**Parameters:**
- `workspace_id` (str): The workspace ID to execute the run in (format: "ws-xxxxxxxx")
- `params` (RunParams, optional): Run configuration options:
  - `message`: Description of the run's purpose
  - `is_destroy`: Whether to destroy all resources (default: False)
  - `auto_apply`: Whether to auto-apply after a successful plan
  - `refresh`: Whether to refresh state before planning (default: True)
  - `refresh_only`: Only refresh the state without planning changes
  - `plan_only`: Create a speculative plan without applying
  - `target_addrs`: List of resource addresses to target
  - `replace_addrs`: List of resource addresses to force replacement
  - `variables`: Run-specific variable overrides

**Returns:** JSON response with run details including:
- Run ID and creation timestamp
- Status and status timestamps
- Relationships to workspace, configuration version, and plan

**Notes:**
- Requires "queue run" permission on the workspace
- Workspace must be unlocked to create a run
- Only one run can be active in a workspace at a time
- Run execution depends on the workspace's execution mode

### list_runs_in_workspace

**Function:** `list_runs_in_workspace(workspace_id: str, page_number: int = 1, page_size: int = 20, filter_operation: Optional[str] = None, filter_status: Optional[str] = None, filter_source: Optional[str] = None, filter_status_group: Optional[str] = None, filter_timeframe: Optional[str] = None, filter_agent_pool_names: Optional[str] = None, search_user: Optional[str] = None, search_commit: Optional[str] = None, search_basic: Optional[str] = None) -> Dict[str, Any]`

**Description:** Lists and filters runs in a specific workspace.

**Parameters:**
- `workspace_id` (str): The workspace ID (format: "ws-xxxxxxxx")
- `page_number` (int, optional): Page number to fetch (default: 1)
- `page_size` (int, optional): Number of results per page (default: 20)
- `filter_operation`: Filter by operation type (e.g., "plan,apply")
- `filter_status`: Filter by status (e.g., "pending,planning,applying")
- `filter_source`: Filter by source (e.g., "tfe-ui,tfe-api")
- `filter_status_group`: Filter by status group (e.g., "running,pending")
- And many other filtering options...

**Returns:** JSON response with paginated list of runs and metadata.

**Notes:**
- Requires "read runs" permission on the workspace
- Use multiple comma-separated values for filter parameters
- Results are sorted with most recent runs first

### list_runs_in_organization

**Function:** `list_runs_in_organization(organization: str, page_number: int = 1, page_size: int = 20, filter_operation: Optional[str] = None, filter_status: Optional[str] = None, filter_source: Optional[str] = None, filter_status_group: Optional[str] = None, filter_timeframe: Optional[str] = None, filter_agent_pool_names: Optional[str] = None, filter_workspace_names: Optional[str] = None, search_user: Optional[str] = None, search_commit: Optional[str] = None, search_basic: Optional[str] = None) -> Dict[str, Any]`

**Description:** Lists runs across all workspaces in an organization.

**Parameters:**
- `organization` (str): The organization name
- Same filtering parameters as list_runs_in_workspace plus:
- `filter_workspace_names` (str, optional): Filter by workspace names

**Returns:** JSON response with paginated list of runs across the organization.

**Notes:**
- Requires appropriate permissions on workspaces
- Useful for organization-wide auditing and monitoring
- Returns only runs from workspaces the user has access to

### get_run_details

**Function:** `get_run_details(run_id: str) -> Dict[str, Any]`

**Description:** Gets detailed information about a specific run.

**Parameters:**
- `run_id` (str): The ID of the run (format: "run-xxxxxxxx")

**Returns:** JSON response with comprehensive run details including:
- Run status and phase information
- Timestamps for each state transition
- Configuration information
- Relationships to plans, applies, and cost estimates

**Notes:**
- Requires "read runs" permission on the associated workspace
- Provides access to related resources via relationships

### apply_run

**Function:** `apply_run(run_id: str, comment: str = "") -> Dict[str, Any]`

**Description:** Confirms and applies a run that is paused waiting for confirmation.

**Parameters:**
- `run_id` (str): The ID of the run to apply
- `comment` (str, optional): Comment explaining the approval reason

**Returns:** JSON response with updated run details.

**Notes:**
- Requires "apply" permission on the workspace
- Run must be in "planned" status with changes to apply
- Comment is recorded in the audit log

### discard_run

**Function:** `discard_run(run_id: str, comment: str = "") -> Dict[str, Any]`

**Description:** Discards a run that is paused waiting for confirmation.

**Parameters:**
- `run_id` (str): The ID of the run to discard
- `comment` (str, optional): Comment explaining the discard reason

**Returns:** JSON response with updated run details showing discarded state.

**Notes:**
- Requires "apply" permission on the workspace
- Run must be in "planned" status to be discarded
- Discarded runs cannot be applied later

### cancel_run

**Function:** `cancel_run(run_id: str, comment: str = "") -> Dict[str, Any]`

**Description:** Gracefully cancels a run that is currently planning or applying.

**Parameters:**
- `run_id` (str): The ID of the run to cancel
- `comment` (str, optional): Comment explaining the cancellation reason

**Returns:** JSON response with updated run details showing canceled state.

**Notes:**
- Requires "cancel" permission on the workspace
- Run must be in an active state (planning, applying)
- Attempts to gracefully terminate the process

### force_cancel_run

**Function:** `force_cancel_run(run_id: str, comment: str = "") -> Dict[str, Any]`

**Description:** Force cancels a run immediately.

**Parameters:**
- `run_id` (str): The ID of the run to force cancel
- `comment` (str, optional): Comment explaining the force cancellation reason

**Returns:** JSON response with updated run details showing force-canceled state.

**Notes:**
- Requires "cancel" permission on the workspace
- Use only when normal cancellation doesn't work
- May result in inconsistent state if used during apply
- Immediately unlocks the workspace

### force_execute_run

**Function:** `force_execute_run(run_id: str) -> Dict[str, Any]`

**Description:** Cancels all prior runs to execute a specific run immediately.

**Parameters:**
- `run_id` (str): The ID of the run to execute

**Returns:** JSON response confirming the run has been promoted.

**Notes:**
- Requires "cancel" permission on the workspace
- Cancels all pending runs in the queue to prioritize this run
- Useful for urgent changes or when runs are queued

**Common Error Scenarios:**

| Error | Cause | Solution |
|-------|-------|----------|
| 404 | Run not found | Verify the run ID |
| 403 | Insufficient permissions | Ensure you have proper permissions |
| 409 | Run cannot be applied/discarded/canceled | Verify run is in correct state |
| 422 | Workspace locked by another run | Wait for the current run to finish or cancel it |
| 409 | Workspace already has active run | Cancel the active run or wait for it to complete |