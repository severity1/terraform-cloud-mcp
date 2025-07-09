# Variable Tools

This module provides tools for managing variables and variable sets in Terraform Cloud.

## Overview

Variables in Terraform Cloud are used to provide inputs to your Terraform configurations and set environment variables during runs. These tools allow you to manage variables at the workspace level and create reusable variable sets that can be shared across multiple workspaces and projects.

## API Reference

These tools interact with the Terraform Cloud Variables API:
- [Workspace Variables API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables)
- [Variable Sets API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets)
- [Variables in Terraform Cloud](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/variables)

## Tools Reference

### list_workspace_variables

**Function:** `list_workspace_variables(workspace_id: str) -> Dict[str, Any]`

**Description:** Retrieves all variables (both Terraform and environment) configured for a specific workspace.

**Parameters:**
- `workspace_id` (str): The ID of the workspace (format: "ws-xxxxxxxx")

**Returns:** JSON response containing list of workspace variables with their configuration and values.

**Notes:**
- Requires "read variables" permission on the workspace
- Sensitive variable values are not returned in the response
- Both Terraform and environment variables are included

### create_workspace_variable

**Function:** `create_workspace_variable(workspace_id: str, key: str, category: str, params: Optional[WorkspaceVariableParams] = None) -> Dict[str, Any]`

**Description:** Creates a new Terraform or environment variable within a workspace.

**Parameters:**
- `workspace_id` (str): The ID of the workspace (format: "ws-xxxxxxxx")
- `key` (str): The variable name/key
- `category` (str): Variable category ("terraform" or "env")
- `params` (WorkspaceVariableParams, optional): Additional variable parameters including value, description, HCL format, and sensitivity settings

**Returns:** JSON response with the created variable including its configuration and metadata.

**Notes:**
- Requires "write variables" permission on the workspace
- HCL format is only valid for terraform category variables
- Sensitive variables will have their values hidden in responses

### update_workspace_variable

**Function:** `update_workspace_variable(workspace_id: str, variable_id: str, params: Optional[WorkspaceVariableParams] = None) -> Dict[str, Any]`

**Description:** Modifies the configuration of an existing workspace variable. Only specified attributes will be updated.

**Parameters:**
- `workspace_id` (str): The ID of the workspace (format: "ws-xxxxxxxx")
- `variable_id` (str): The ID of the variable (format: "var-xxxxxxxx")
- `params` (WorkspaceVariableParams, optional): Variable parameters to update including key, value, description, category, HCL format, and sensitivity

**Returns:** JSON response with the updated variable including all current settings.

**Notes:**
- Requires "write variables" permission on the workspace
- Only specified attributes are updated; others remain unchanged
- Cannot change a sensitive variable to non-sensitive

### delete_workspace_variable

**Function:** `delete_workspace_variable(workspace_id: str, variable_id: str) -> Dict[str, Any]`

**Description:** Permanently removes a variable from a workspace. This action cannot be undone.

**Parameters:**
- `workspace_id` (str): The ID of the workspace (format: "ws-xxxxxxxx")
- `variable_id` (str): The ID of the variable (format: "var-xxxxxxxx")

**Returns:** Empty response with HTTP 204 status code if successful.

**Notes:**
- DESTRUCTIVE OPERATION: Requires `ENABLE_DELETE_TOOLS=true` environment variable
- Requires "write variables" permission on the workspace
- This action cannot be undone

### list_variable_sets

**Function:** `list_variable_sets(organization: str, page_number: int = 1, page_size: int = 20) -> Dict[str, Any]`

**Description:** Retrieves a paginated list of all variable sets in a Terraform Cloud organization.

**Parameters:**
- `organization` (str): The name of the organization
- `page_number` (int, optional): The page number to return (default: 1)
- `page_size` (int, optional): Number of items per page (default: 20, max: 100)

**Returns:** JSON response containing paginated list of variable sets with their configuration and metadata.

**Notes:**
- Requires "read variable sets" permission on the organization
- Variable sets allow you to reuse variables across multiple workspaces
- Results are paginated with metadata indicating total count

### get_variable_set

**Function:** `get_variable_set(varset_id: str) -> Dict[str, Any]`

**Description:** Retrieves comprehensive information about a variable set including its variables, workspace assignments, and configuration.

**Parameters:**
- `varset_id` (str): The ID of the variable set (format: "varset-xxxxxxxx")

**Returns:** JSON response with variable set details including configuration and relationships.

**Notes:**
- Requires "read variable sets" permission
- Includes information about workspace and project assignments
- Shows global status and priority settings

### create_variable_set

**Function:** `create_variable_set(organization: str, name: str, params: Optional[VariableSetParams] = None) -> Dict[str, Any]`

**Description:** Creates a new variable set which can be used to manage variables across multiple workspaces and projects.

**Parameters:**
- `organization` (str): The name of the organization
- `name` (str): The name to give the variable set
- `params` (VariableSetParams, optional): Additional variable set parameters including description, global status, and priority settings

**Returns:** JSON response with the created variable set including its configuration and metadata.

**Notes:**
- Requires "write variable sets" permission on the organization
- Global variable sets are automatically applied to all workspaces
- Priority variable sets override workspace-level variables

### update_variable_set

**Function:** `update_variable_set(varset_id: str, params: Optional[VariableSetParams] = None) -> Dict[str, Any]`

**Description:** Modifies the settings of a variable set. Only specified attributes will be updated.

**Parameters:**
- `varset_id` (str): The ID of the variable set (format: "varset-xxxxxxxx")
- `params` (VariableSetParams, optional): Variable set parameters to update including name, description, global status, and priority

**Returns:** JSON response with the updated variable set including all current settings.

**Notes:**
- Requires "write variable sets" permission
- Only specified attributes are updated; others remain unchanged
- Changing global status affects workspace assignments

### delete_variable_set

**Function:** `delete_variable_set(varset_id: str) -> Dict[str, Any]`

**Description:** Permanently removes a variable set and all its variables. The variable set will be unassigned from all workspaces and projects.

**Parameters:**
- `varset_id` (str): The ID of the variable set (format: "varset-xxxxxxxx")

**Returns:** Empty response with HTTP 204 status code if successful.

**Notes:**
- DESTRUCTIVE OPERATION: Requires `ENABLE_DELETE_TOOLS=true` environment variable
- Requires "write variable sets" permission
- This action cannot be undone and removes all variables in the set

### assign_variable_set_to_workspaces

**Function:** `assign_variable_set_to_workspaces(varset_id: str, workspace_ids: List[str]) -> Dict[str, Any]`

**Description:** Makes the variables in a variable set available to the specified workspaces.

**Parameters:**
- `varset_id` (str): The ID of the variable set (format: "varset-xxxxxxxx")
- `workspace_ids` (List[str]): List of workspace IDs (format: ["ws-xxxxxxxx", ...])

**Returns:** Empty response with HTTP 204 status code if successful.

**Notes:**
- Variables from variable sets take precedence over workspace variables if the variable set has priority enabled
- Does not affect global variable sets (they're automatically applied)

### unassign_variable_set_from_workspaces

**Function:** `unassign_variable_set_from_workspaces(varset_id: str, workspace_ids: List[str]) -> Dict[str, Any]`

**Description:** Removes the variable set assignment from the specified workspaces. The variables will no longer be available in those workspaces.

**Parameters:**
- `varset_id` (str): The ID of the variable set (format: "varset-xxxxxxxx")
- `workspace_ids` (List[str]): List of workspace IDs (format: ["ws-xxxxxxxx", ...])

**Returns:** Empty response with HTTP 204 status code if successful.

**Notes:**
- Cannot unassign global variable sets from workspaces
- Variables become unavailable immediately in the affected workspaces

### assign_variable_set_to_projects

**Function:** `assign_variable_set_to_projects(varset_id: str, project_ids: List[str]) -> Dict[str, Any]`

**Description:** Makes the variables in a variable set available to all workspaces within the specified projects.

**Parameters:**
- `varset_id` (str): The ID of the variable set (format: "varset-xxxxxxxx")
- `project_ids` (List[str]): List of project IDs (format: ["prj-xxxxxxxx", ...])

**Returns:** Empty response with HTTP 204 status code if successful.

**Notes:**
- All workspaces in the project receive the variable set
- New workspaces added to the project will automatically inherit the variable set

### unassign_variable_set_from_projects

**Function:** `unassign_variable_set_from_projects(varset_id: str, project_ids: List[str]) -> Dict[str, Any]`

**Description:** Removes the variable set assignment from the specified projects. The variables will no longer be available in workspaces within those projects.

**Parameters:**
- `varset_id` (str): The ID of the variable set (format: "varset-xxxxxxxx")
- `project_ids` (List[str]): List of project IDs (format: ["prj-xxxxxxxx", ...])

**Returns:** Empty response with HTTP 204 status code if successful.

**Notes:**
- Affects all workspaces within the specified projects
- Cannot unassign global variable sets from projects

### list_variables_in_variable_set

**Function:** `list_variables_in_variable_set(varset_id: str) -> Dict[str, Any]`

**Description:** Retrieves all variables that belong to a specific variable set, including their configuration and values.

**Parameters:**
- `varset_id` (str): The ID of the variable set (format: "varset-xxxxxxxx")

**Returns:** JSON response containing list of variables in the variable set with their configuration.

**Notes:**
- Requires "read variable sets" permission
- Sensitive variable values are not returned in the response
- Both Terraform and environment variables are included

### create_variable_in_variable_set

**Function:** `create_variable_in_variable_set(varset_id: str, key: str, category: str, params: Optional[VariableSetVariableParams] = None) -> Dict[str, Any]`

**Description:** Creates a new Terraform or environment variable within a variable set.

**Parameters:**
- `varset_id` (str): The ID of the variable set (format: "varset-xxxxxxxx")
- `key` (str): The variable name/key
- `category` (str): Variable category ("terraform" or "env")
- `params` (VariableSetVariableParams, optional): Additional variable parameters including value, description, HCL format, and sensitivity settings

**Returns:** JSON response with the created variable including its configuration and metadata.

**Notes:**
- Requires "write variable sets" permission
- HCL format is only valid for terraform category variables
- Variable becomes available in all workspaces/projects assigned to the variable set

### update_variable_in_variable_set

**Function:** `update_variable_in_variable_set(varset_id: str, var_id: str, params: Optional[VariableSetVariableParams] = None) -> Dict[str, Any]`

**Description:** Modifies the configuration of an existing variable within a variable set. Only specified attributes will be updated.

**Parameters:**
- `varset_id` (str): The ID of the variable set (format: "varset-xxxxxxxx")
- `var_id` (str): The ID of the variable (format: "var-xxxxxxxx")
- `params` (VariableSetVariableParams, optional): Variable parameters to update including key, value, description, category, HCL format, and sensitivity

**Returns:** JSON response with the updated variable including all current settings.

**Notes:**
- Requires "write variable sets" permission
- Only specified attributes are updated; others remain unchanged
- Changes affect all workspaces using this variable set

### delete_variable_from_variable_set

**Function:** `delete_variable_from_variable_set(varset_id: str, var_id: str) -> Dict[str, Any]`

**Description:** Permanently removes a variable from a variable set. This action cannot be undone.

**Parameters:**
- `varset_id` (str): The ID of the variable set (format: "varset-xxxxxxxx")
- `var_id` (str): The ID of the variable (format: "var-xxxxxxxx")

**Returns:** Empty response with HTTP 204 status code if successful.

**Notes:**
- DESTRUCTIVE OPERATION: Requires `ENABLE_DELETE_TOOLS=true` environment variable
- Requires "write variable sets" permission
- This action cannot be undone
- Variable becomes unavailable in all workspaces using this variable set

## Common Error Scenarios

| Error | Description | Resolution |
|-------|-------------|------------|
| 401 Unauthorized | Invalid or missing authentication token | Verify TFC_TOKEN environment variable |
| 403 Forbidden | Insufficient permissions for the operation | Check user/team permissions on workspace/organization |
| 404 Not Found | Workspace, variable set, or variable not found | Verify the ID format and existence |
| 422 Unprocessable Entity | Invalid variable configuration (e.g., HCL on env variable) | Review variable parameters and constraints |
| 409 Conflict | Variable key already exists in workspace/variable set | Use a different key or update the existing variable |