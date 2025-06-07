# Project Tools

This module provides tools for managing projects in Terraform Cloud.

## Overview

Projects in Terraform Cloud are containers for workspaces that help organize them into logical groups. These tools allow you to create, read, update, and delete projects, as well as manage tag bindings and move workspaces between projects.

## API Reference

These tools interact with the Terraform Cloud Projects API:
- [Projects API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects)
- [Projects Guide](https://developer.hashicorp.com/terraform/cloud-docs/projects)

## Tools Reference

### list_projects

**Function:** `list_projects(organization: str, page_number: int = 1, page_size: int = 20, q: Optional[str] = None, filter_names: Optional[str] = None, filter_permissions_update: Optional[bool] = None, filter_permissions_create_workspace: Optional[bool] = None, sort: Optional[str] = None) -> Dict[str, Any]`

**Description:** Retrieves a paginated list of projects in an organization.

**Parameters:**
- `organization` (str): The organization name
- `page_number` (int, optional): Page number to fetch (default: 1)
- `page_size` (int, optional): Number of results per page (default: 20, max: 100)
- `q` (str, optional): Search query to filter projects by name
- `filter_names` (str, optional): Filter projects by name (comma-separated list)
- `filter_permissions_update` (bool, optional): Filter projects that the user can update
- `filter_permissions_create_workspace` (bool, optional): Filter projects that the user can create workspaces in
- `sort` (str, optional): Sort projects by name ('name' or '-name' for descending)

**Returns:** JSON response containing paginated list of projects with their configuration and metadata.

**Notes:**
- Requires "list projects" permission on the organization
- Use the search parameter for partial name matches
- Permissions filters are useful for determining which projects you can modify

### get_project_details

**Function:** `get_project_details(project_id: str) -> Dict[str, Any]`

**Description:** Retrieves comprehensive information about a specific project.

**Parameters:**
- `project_id` (str): The ID of the project to retrieve details for (format: "prj-xxxxxxxx")

**Returns:** JSON response with project details including:
- Name and description
- Creation and update timestamps
- Auto-destroy activity duration settings
- Tag bindings
- Workspace count

**Notes:**
- Requires "show project" permission
- Essential for retrieving tag bindings and workspace counts

### create_project

**Function:** `create_project(organization: str, name: str, params: Optional[ProjectParams] = None) -> Dict[str, Any]`

**Description:** Creates a new project in an organization.

**Parameters:**
- `organization` (str): The organization name
- `name` (str): The name for the new project
- `params` (ProjectParams, optional): Additional configuration options:
  - `description`: Human-readable description of the project
  - `auto_destroy_activity_duration`: How long each workspace should wait before auto-destroying
  - `tag_bindings`: List of tag key-value pairs to bind to the project

**Returns:** JSON response with the created project details.

**Notes:**
- Requires "create projects" permission on the organization
- Project names must be unique within an organization
- Tags bound to the project are inherited by workspaces within the project

### update_project

**Function:** `update_project(project_id: str, params: Optional[ProjectParams] = None) -> Dict[str, Any]`

**Description:** Updates an existing project's settings.

**Parameters:**
- `project_id` (str): The ID of the project to update
- `params` (ProjectParams, optional): Settings to update:
  - `name`: New name for the project
  - `description`: Human-readable description
  - `auto_destroy_activity_duration`: How long each workspace should wait before auto-destroying

**Returns:** JSON response with the updated project details.

**Notes:**
- Requires "update project" permission
- Only specified attributes will be updated
- Does not update tag bindings directly (use add_update_project_tag_bindings)

### delete_project

**Function:** `delete_project(project_id: str) -> Dict[str, Any]`

**Description:** Permanently deletes a project.

**Parameters:**
- `project_id` (str): The ID of the project to delete

**Returns:** Empty response with HTTP 204 status code if successful.

**Notes:**
- Requires "delete project" permission
- Will fail if the project contains any workspaces or stacks
- Move or delete workspaces first before deleting a project

### list_project_tag_bindings

**Function:** `list_project_tag_bindings(project_id: str) -> Dict[str, Any]`

**Description:** Lists all tags bound to a specific project.

**Parameters:**
- `project_id` (str): The ID of the project

**Returns:** JSON response with list of tag bindings including key-value pairs.

**Notes:**
- Requires "show project" permission
- Project tag bindings are inherited by all workspaces within the project
- Useful for understanding which tags will be applied to workspaces

### add_update_project_tag_bindings

**Function:** `add_update_project_tag_bindings(project_id: str, tag_bindings: List[TagBinding]) -> Dict[str, Any]`

**Description:** Adds or updates tag bindings on a project.

**Parameters:**
- `project_id` (str): The ID of the project
- `tag_bindings`: List of TagBinding objects with key-value pairs

**Returns:** JSON response with the complete list of updated tag bindings.

**Notes:**
- Requires "update project" permission
- This is an additive operation (doesn't remove existing tags)
- If a key already exists, its value will be updated
- Tags are automatically propagated to all workspaces in the project

### move_workspaces_to_project

**Function:** `move_workspaces_to_project(project_id: str, workspace_ids: List[str]) -> Dict[str, Any]`

**Description:** Moves one or more workspaces into a project.

**Parameters:**
- `project_id` (str): The ID of the destination project
- `workspace_ids`: List of workspace IDs to move

**Returns:** Empty response with HTTP 204 status code if successful.

**Notes:**
- Requires permission to move workspaces on both source and destination projects
- Workspaces will inherit tags from the destination project
- Useful for reorganizing workspaces between projects

**Common Error Scenarios:**

| Error | Cause | Solution |
|-------|-------|----------|
| 404 | Project not found | Verify the project ID |
| 403 | Insufficient permissions | Ensure you have proper permissions on projects |
| 422 | Project contains workspaces | Move workspaces out before deleting |
| 422 | Duplicate tag keys | Remove duplicates from tag binding list |