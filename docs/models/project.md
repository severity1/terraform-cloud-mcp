# Project Models

This document describes the data models used for project operations in Terraform Cloud.

## Overview

Project models provide structure and validation for interacting with the Terraform Cloud Projects API. These models define project configuration options, tag bindings, and other settings that can be applied to projects and inherited by their workspaces.

## Models Reference

### TagBinding

**Type:** Object

**Description:** Tag binding configuration for a project. Defines a tag key-value pair that can be bound to a project and inherited by its workspaces.

**Fields:**
- `key` (string, required): The key of the tag
- `value` (string, required): The value of the tag

**JSON representation:**
```json
{
  "key": "environment",
  "value": "production"
}
```

**Usage Context:**
Tag bindings can be applied to projects and are inherited by all workspaces within those projects. They provide a way to consistently categorize and organize workspaces that share common characteristics.

### ProjectParams

**Type:** Object

**Description:** Parameters for project operations without routing fields. Used to specify configuration options when creating or updating projects.

**Fields:**
- `name` (string, optional): Name of the project
- `description` (string, optional): Human-readable description of the project
- `auto_destroy_activity_duration` (string, optional): How long each workspace should wait before auto-destroying (e.g., '14d', '24h')
- `tag_bindings` (List[TagBinding], optional): List of tag key-value pairs to bind to the project

**JSON representation:**
```json
{
  "data": {
    "type": "projects",
    "attributes": {
      "name": "Production Infrastructure",
      "description": "Production environment resources",
      "auto-destroy-activity-duration": "14d"
    }
  }
}
```

**Notes:**
- Field names in JSON use kebab-case format (e.g., "auto-destroy-activity-duration")
- Field names in the model use snake_case format (e.g., auto_destroy_activity_duration)
- All fields are optional when updating but name is required when creating

### ProjectListRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for listing projects.

**Fields:**
- `organization` (string, required): The name of the organization to list projects from
- `page_number` (int, optional): Page number to fetch (default: 1)
- `page_size` (int, optional): Number of results per page (default: 20, max: 100)
- `q` (string, optional): Search query to filter projects by name
- `filter_names` (string, optional): Filter projects by name (comma-separated list)
- `filter_permissions_update` (bool, optional): Filter projects that the user can update
- `filter_permissions_create_workspace` (bool, optional): Filter projects that the user can create workspaces in
- `sort` (string, optional): Sort projects by name ('name' or '-name' for descending)

**Used by:**
- `list_projects` tool function to validate listing parameters

### BaseProjectRequest

**Type:** Request Validation Model

**Description:** Base request model containing common fields for project operations.

**Fields:**
- Includes all fields from ProjectParams

### ProjectCreateRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for creating a project.

**Fields:**
- `organization` (string, required): The organization name
- `name` (string, required): The name for the new project
- `params` (ProjectParams, optional): Additional configuration options

**Used by:**
- `create_project` tool function to validate project creation parameters

### ProjectUpdateRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for updating a project.

**Fields:**
- `project_id` (string, required): The ID of the project to update
- `params` (ProjectParams, optional): Settings to update

**Used by:**
- `update_project` tool function to validate project update parameters

### ProjectTagBindingRequest

**Type:** Request Validation Model

**Description:** Used to validate tag binding operations for projects.

**Fields:**
- `project_id` (string, required): The ID of the project

**Used by:**
- `list_project_tag_bindings` tool function to validate project ID

### WorkspaceMoveRequest

**Type:** Request Validation Model

**Description:** Used to validate workspace move operations.

**Fields:**
- `project_id` (string, required): The ID of the destination project
- `workspace_ids` (List[string], required): List of workspace IDs to move

**Used by:**
- `move_workspaces_to_project` tool function to validate move parameters

## API Response Structure

### Project Details Response

```json
{
  "data": {
    "id": "prj-AbCdEfGhIjKlMnOp",
    "type": "projects",
    "attributes": {
      "name": "Production Infrastructure",
      "description": "Production environment resources",
      "auto-destroy-activity-duration": "14d",
      "created-at": "2023-05-15T10:30:00Z", 
      "permissions": {
        "can-destroy": true,
        "can-update": true,
        "can-access-settings": true,
        "can-create-workspace": true,
        "can-move-workspaces": true
      }
    },
    "relationships": {
      "organization": {
        "data": {
          "id": "org-AbCdEfGh",
          "type": "organizations"
        }
      }
    }
  }
}
```

### Tag Bindings Response

```json
{
  "data": [
    {
      "id": "tag-AbCdEfGh",
      "type": "tag-bindings",
      "attributes": {
        "key": "environment",
        "value": "production",
        "created-at": "2023-05-15T10:35:00Z"
      }
    },
    {
      "id": "tag-IjKlMnOp",
      "type": "tag-bindings",
      "attributes": {
        "key": "team",
        "value": "platform",
        "created-at": "2023-05-15T10:35:00Z"
      }
    }
  ]
}
```

### List Projects Response

```json
{
  "data": [
    {
      "id": "prj-AbCdEfGh",
      "type": "projects",
      "attributes": {
        "name": "Production",
        "description": "Production infrastructure",
        "created-at": "2023-05-15T10:30:00Z",
        "workspaces-count": 12
      }
    },
    {
      "id": "prj-IjKlMnOp",
      "type": "projects",
      "attributes": {
        "name": "Development",
        "description": "Development infrastructure",
        "created-at": "2023-05-16T14:20:00Z",
        "workspaces-count": 8
      }
    }
  ],
  "meta": {
    "pagination": {
      "current-page": 1,
      "page-size": 20,
      "prev-page": null,
      "next-page": null,
      "total-pages": 1,
      "total-count": 2
    }
  }
}
```

## Related Resources

- [Project Tools](../tools/project.md)
- [Organization Models](organization.md)
- [Workspace Models](workspace.md)
- [Terraform Cloud API - Projects](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects)