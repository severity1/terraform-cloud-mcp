# Variables Models

This document describes the data models used for variable and variable set operations in Terraform Cloud.

## Overview

Variable models provide structure and validation for interacting with the Terraform Cloud Variables API. These models define workspace variable configuration, variable set management, and cross-workspace variable sharing. Variables serve as input parameters for Terraform configurations and environment settings for runs, while variable sets enable reusable variable collections across multiple workspaces and projects.

## Models Reference

### VariableCategory

**Type:** Enum (string)

**Description:** Defines the type of variable for use in Terraform operations.

**Values:**
- `terraform`: Terraform input variables available in configuration
- `env`: Environment variables available during plan/apply operations

**JSON representation:**
```json
{
  "category": "terraform"
}
```

**Usage Context:**
The variable category determines how the variable is exposed during Terraform operations. Terraform variables are available as input variables in the configuration, while environment variables are available to the Terraform process and any custom scripts.

**Notes:**
- HCL format is only valid for terraform category variables
- Environment variables are typically used for provider authentication or configuration

### WorkspaceVariable

**Type:** Object

**Description:** Complete model for workspace variable data including all configuration options.

**Fields:**
- `key` (string, required): Variable name/key (1-255 characters)
- `value` (string, optional): Variable value (max 256,000 characters)
- `description` (string, optional): Description of the variable (max 512 characters)
- `category` (VariableCategory, required): Variable category (terraform or env)
- `hcl` (boolean, optional): Whether the value is HCL code (default: false, terraform only)
- `sensitive` (boolean, optional): Whether the variable value is sensitive (default: false)

**JSON representation:**
```json
{
  "data": {
    "type": "vars",
    "attributes": {
      "key": "instance_type",
      "value": "t3.micro",
      "description": "EC2 instance type for the web server",
      "category": "terraform",
      "hcl": false,
      "sensitive": false
    }
  }
}
```

**Usage Context:**
Workspace variables provide configuration values specific to a single workspace. They can be Terraform input variables or environment variables, with support for sensitive values and HCL syntax for complex data structures.

### VariableSet

**Type:** Object

**Description:** Configuration model for variable sets that can be shared across workspaces and projects.

**Fields:**
- `name` (string, required): Variable set name (1-90 characters)
- `description` (string, optional): Description of the variable set (max 512 characters)
- `global` (boolean, optional): Whether this is a global variable set (default: false)
- `priority` (boolean, optional): Whether this variable set takes priority over workspace variables (default: false)

**JSON representation:**
```json
{
  "data": {
    "type": "varsets",
    "attributes": {
      "name": "production-env",
      "description": "Common variables for production environment",
      "global": false,
      "priority": true
    }
  }
}
```

**Usage Context:**
Variable sets enable sharing common variables across multiple workspaces and projects. Global variable sets are automatically applied to all workspaces, while priority variable sets override workspace-level variables with the same keys.

### WorkspaceVariableParams

**Type:** Object

**Description:** Parameters for workspace variable operations without routing fields. Used to specify configuration parameters for creating or updating workspace variables.

**Fields:**
- `key` (string, optional): Variable name/key
- `value` (string, optional): Variable value
- `description` (string, optional): Description of the variable
- `category` (VariableCategory, optional): Variable category (terraform or env)
- `hcl` (boolean, optional): Whether the value is HCL code (terraform variables only)
- `sensitive` (boolean, optional): Whether the variable value is sensitive

**Usage Context:**
Used as optional parameters in variable creation and update operations, allowing specification of only the fields that need to be set or changed.

### VariableSetParams

**Type:** Object

**Description:** Parameters for variable set operations without routing fields. Used to specify configuration parameters for creating or updating variable sets.

**Fields:**
- `name` (string, optional): Variable set name
- `description` (string, optional): Description of the variable set
- `global` (boolean, optional): Whether this is a global variable set
- `priority` (boolean, optional): Whether this variable set takes priority over workspace variables

**Usage Context:**
Used as optional parameters in variable set creation and update operations, enabling modification of only specified attributes while leaving others unchanged.

### WorkspaceVariableCreateRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for creating workspace variables.

**Fields:**
- `workspace_id` (string, required): The workspace ID (format: "ws-xxxxxxxx")
- `key` (string, required): Variable name/key
- `category` (VariableCategory, required): Variable category
- `params` (WorkspaceVariableParams, optional): Additional variable parameters

**Used by:**
- `create_workspace_variable` tool function to validate variable creation parameters

### WorkspaceVariableUpdateRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for updating workspace variables.

**Fields:**
- `workspace_id` (string, required): The workspace ID (format: "ws-xxxxxxxx")
- `variable_id` (string, required): The variable ID (format: "var-xxxxxxxx")
- `params` (WorkspaceVariableParams, optional): Variable parameters to update

**Used by:**
- `update_workspace_variable` tool function to validate variable update parameters

### VariableSetCreateRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for creating variable sets.

**Fields:**
- `organization` (string, required): The organization name
- `name` (string, required): Variable set name
- `params` (VariableSetParams, optional): Additional variable set parameters

**Used by:**
- `create_variable_set` tool function to validate variable set creation parameters

### VariableSetUpdateRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for updating variable sets.

**Fields:**
- `varset_id` (string, required): The variable set ID (format: "varset-xxxxxxxx")
- `params` (VariableSetParams, optional): Variable set parameters to update

**Used by:**
- `update_variable_set` tool function to validate variable set update parameters

### VariableSetAssignmentRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for assigning variable sets to workspaces or projects.

**Fields:**
- `varset_id` (string, required): The variable set ID (format: "varset-xxxxxxxx")
- `workspace_ids` (List[str], optional): List of workspace IDs to assign
- `project_ids` (List[str], optional): List of project IDs to assign

**Used by:**
- `assign_variable_set_to_workspaces` and `assign_variable_set_to_projects` tool functions

## API Response Structure

### Workspace Variable Response

```json
{
  "data": {
    "id": "var-EavQ1LztoRTQHSNT",
    "type": "vars",
    "attributes": {
      "key": "image_id",
      "value": "ami-0c55b159cbfafe1d0",
      "description": "AMI ID for the EC2 instance",
      "category": "terraform",
      "hcl": false,
      "sensitive": false,
      "created-at": "2023-05-01T12:34:56Z",
      "updated-at": "2023-05-01T12:34:56Z"
    },
    "relationships": {
      "configurable": {
        "data": {
          "id": "ws-SihZTyXKfNXUWuUa",
          "type": "workspaces"
        }
      }
    }
  }
}
```

### List Workspace Variables Response

```json
{
  "data": [
    {
      "id": "var-EavQ1LztoRTQHSNT",
      "type": "vars",
      "attributes": {
        "key": "image_id",
        "value": "ami-0c55b159cbfafe1d0",
        "description": "AMI ID for the EC2 instance",
        "category": "terraform",
        "hcl": false,
        "sensitive": false
      }
    },
    {
      "id": "var-GjyK2MzupSTRJTOU",
      "type": "vars",
      "attributes": {
        "key": "DATABASE_URL",
        "value": null,
        "description": "Database connection string",
        "category": "env",
        "hcl": false,
        "sensitive": true
      }
    }
  ]
}
```

### Variable Set Response

```json
{
  "data": {
    "id": "varset-47qC5ydmtMa8cYs2",
    "type": "varsets",
    "attributes": {
      "name": "aws-common-config",
      "description": "Common AWS configuration variables",
      "global": false,
      "priority": true,
      "created-at": "2023-05-01T12:34:56Z",
      "updated-at": "2023-05-01T12:34:56Z"
    },
    "relationships": {
      "organization": {
        "data": {
          "id": "org-ABcd1234",
          "type": "organizations"
        }
      },
      "vars": {
        "data": [
          {
            "id": "var-EavQ1LztoRTQHSNT",
            "type": "vars"
          }
        ]
      },
      "workspaces": {
        "data": [
          {
            "id": "ws-SihZTyXKfNXUWuUa",
            "type": "workspaces"
          }
        ]
      }
    }
  }
}
```

### List Variable Sets Response

```json
{
  "data": [
    {
      "id": "varset-47qC5ydmtMa8cYs2",
      "type": "varsets",
      "attributes": {
        "name": "production-config",
        "description": "Production environment variables",
        "global": false,
        "priority": true,
        "created-at": "2023-05-01T12:34:56Z"
      },
      "relationships": {
        "organization": {
          "data": {
            "id": "org-ABcd1234",
            "type": "organizations"
          }
        }
      }
    },
    {
      "id": "varset-58rD6zemvNb9dZt3",
      "type": "varsets",
      "attributes": {
        "name": "global-config",
        "description": "Global configuration variables",
        "global": true,
        "priority": false,
        "created-at": "2023-05-02T09:12:34Z"
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

- [Variable Tools](../tools/variables.md)
- [Workspace Models](workspace.md)
- [Project Models](project.md)
- [Terraform Cloud API - Workspace Variables](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables)
- [Terraform Cloud API - Variable Sets](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets)