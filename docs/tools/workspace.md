# Workspace Tools

This module provides tools for managing workspaces in Terraform Cloud.

## Overview

Workspaces in Terraform Cloud are isolated environments for managing infrastructure, containing Terraform configurations, state files, variables, and run histories. These tools allow you to create, read, update, delete, lock, and unlock workspaces.

## API Reference

These tools interact with the Terraform Cloud Workspaces API:
- [Workspaces API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces)
- [Workspace Settings](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings)

## Tools Reference

### list_workspaces

**Function:** `list_workspaces(organization: str, page_number: int = 1, page_size: int = 20, search: Optional[str] = None) -> Dict[str, Any]`

**Description:** Retrieves a paginated list of all workspaces in an organization.

**Parameters:**
- `organization` (str): The name of the organization to list workspaces from
- `page_number` (int, optional): The page number to return (default: 1)
- `page_size` (int, optional): Number of items per page (default: 20, max: 100)
- `search` (str, optional): Filter workspaces by name

**Returns:** JSON response containing paginated list of workspaces with their configuration and metadata.

**Notes:**
- Requires "read workspaces" permission on the organization
- Use the search parameter to find workspaces by partial name match
- Results are paginated, with metadata indicating total count and links to additional pages

### get_workspace_details

**Function:** `get_workspace_details(workspace_id: str = "", organization: str = "", workspace_name: str = "") -> Dict[str, Any]`

**Description:** Gets detailed information about a specific workspace, identified by ID or by organization and workspace name.

**Parameters:**
- `workspace_id` (str, optional): The ID of the workspace (format: "ws-xxxxxxxx")
- `organization` (str, optional): The organization name (required if workspace_id not provided)
- `workspace_name` (str, optional): The workspace name (required if workspace_id not provided)

**Returns:** JSON response with comprehensive workspace details including configuration and current status.

**Notes:**
- You can identify the workspace either by ID directly, or by organization+name combination
- Requires "read workspaces" permission on the organization or workspace

### create_workspace

**Function:** `create_workspace(organization: str, name: str, params: Optional[WorkspaceParams] = None) -> Dict[str, Any]`

**Description:** Creates a new workspace in the specified organization.

**Parameters:**
- `organization` (str): The organization name
- `name` (str): The name for the new workspace
- `params` (WorkspaceParams, optional): Additional configuration options:
  - `description`: Human-readable description
  - `execution_mode`: How operations are executed (remote, local, agent)
  - `terraform_version`: Version of Terraform to use
  - `working_directory`: Subdirectory for Terraform configuration
  - `vcs_repo`: Version control repository configuration
  - `auto_apply`: Whether to auto-apply successful plans
  - And many other options...

**Returns:** JSON response with the created workspace details.

**Notes:**
- Requires "create workspaces" permission on the organization
- Workspace names must be unique within an organization
- Default execution mode is "remote" unless otherwise specified

### update_workspace

**Function:** `update_workspace(organization: str, workspace_name: str, params: Optional[WorkspaceParams] = None) -> Dict[str, Any]`

**Description:** Updates an existing workspace's settings.

**Parameters:**
- `organization` (str): The organization name
- `workspace_name` (str): The current workspace name
- `params` (WorkspaceParams, optional): Settings to update, including:
  - `name`: New name for the workspace (if renaming)
  - `description`: Human-readable description
  - And all other options available in create_workspace...

**Returns:** JSON response with the updated workspace details.

**Notes:**
- Requires "update workspace settings" permission
- Only specified attributes will be updated; unspecified attributes remain unchanged
- To rename a workspace, include the new name in the params

### delete_workspace

**Function:** `delete_workspace(organization: str, workspace_name: str) -> Dict[str, Any]`

**Description:** Permanently deletes a workspace and all related resources.

**Parameters:**
- `organization` (str): The organization name
- `workspace_name` (str): The workspace name to delete

**Returns:** Success message with no content (HTTP 204) if successful.

**Notes:**
- Requires "delete workspaces" permission
- This is a destructive operation that cannot be undone
- Will delete all state versions, run history, and configuration versions
- Use safe_delete_workspace if you want to check for resources first

### safe_delete_workspace

**Function:** `safe_delete_workspace(organization: str, workspace_name: str) -> Dict[str, Any]`

**Description:** Safely deletes a workspace after checking if it has resources.

**Parameters:**
- `organization` (str): The organization name
- `workspace_name` (str): The workspace name to delete

**Returns:** Success message or error if the workspace has resources.

**Notes:**
- Requires "delete workspaces" permission
- Prevents accidental deletion of workspaces with active infrastructure
- Will fail if the workspace has any resources

### lock_workspace

**Function:** `lock_workspace(workspace_id: str, reason: str = "") -> Dict[str, Any]`

**Description:** Locks a workspace to prevent runs from being queued.

**Parameters:**
- `workspace_id` (str): The ID of the workspace to lock
- `reason` (str, optional): Reason for locking the workspace

**Returns:** JSON response with updated workspace including lock information.

**Notes:**
- Requires "lock workspaces" permission
- Locking prevents new runs but doesn't affect already running plans or applies
- Useful during maintenance or when making manual changes

### unlock_workspace

**Function:** `unlock_workspace(workspace_id: str) -> Dict[str, Any]`

**Description:** Unlocks a previously locked workspace.

**Parameters:**
- `workspace_id` (str): The ID of the workspace to unlock

**Returns:** JSON response with updated workspace showing unlocked status.

**Notes:**
- Requires "unlock workspaces" permission
- Can only unlock workspaces that you locked (unless you have admin rights)

### force_unlock_workspace

**Function:** `force_unlock_workspace(workspace_id: str) -> Dict[str, Any]`

**Description:** Force unlocks a workspace even if locked by another user.

**Parameters:**
- `workspace_id` (str): The ID of the workspace to force unlock

**Returns:** JSON response with updated workspace showing unlocked status.

**Notes:**
- Requires admin privileges on the workspace
- Use with caution - should only be used when the normal unlock process isn't possible
- Typically needed when a run has orphaned a lock or the user who locked is unavailable

**Common Error Scenarios:**

| Error | Cause | Solution |
|-------|-------|----------|
| 404 | Workspace not found | Verify the workspace ID or name exists |
| 403 | Insufficient permissions | Ensure you have the proper permissions |
| 422 | Validation error | Ensure workspace name follows conventions (only lowercase letters, numbers, hyphens, underscores) |
| 409 | Conflict | Workspace name already exists in organization |
| 423 | Workspace is locked | Unlock the workspace first or use force_unlock_workspace |