# Workspace Models

This document describes the data models used for workspace operations in Terraform Cloud.

## Overview

Workspace models provide structure and validation for interacting with the Terraform Cloud Workspaces API. These models define workspace configuration options, VCS repository settings, and execution modes. Workspaces serve as the primary organizational unit in Terraform Cloud, containing Terraform configurations, state files, variables, and run history for managing specific infrastructure resources.

## Models Reference

### ExecutionMode

**Type:** Enum (string)

**Description:** Defines how Terraform operations are executed.

**Values:**
- `remote`: Terraform runs on Terraform Cloud's infrastructure
- `local`: Terraform runs on your local machine
- `agent`: Terraform runs on your own infrastructure using an agent

**JSON representation:**
```json
{
  "execution-mode": "remote"
}
```

**Usage Context:**
The execution mode determines where Terraform commands are run when triggered through the API, UI, or VCS. Different execution modes offer trade-offs between convenience, security, and integration with existing workflows.

**Notes:**
- Default value is `remote`
- When using `agent` mode, you must also specify an `agent-pool-id`
- The `local` mode is typically used for CLI-driven workflows

### VcsRepoConfig

**Type:** Object

**Description:** Version control system repository configuration for a workspace.

**Fields:**
- `branch` (string, optional): The repository branch that Terraform executes from
- `identifier` (string, optional): Repository reference in the format `:org/:repo`
- `ingress_submodules` (boolean, optional): Whether to fetch submodules when cloning
- `oauth_token_id` (string, optional): VCS OAuth connection and token ID
- `github_app_installation_id` (string, optional): GitHub App Installation ID
- `tags_regex` (string, optional): Regex pattern to match Git tags

**JSON representation:**
```json
{
  "vcs-repo": {
    "branch": "main",
    "identifier": "my-org/my-repo",
    "ingress-submodules": true,
    "oauth-token-id": "ot-1234abcd"
  }
}
```

**Usage Context:**
Configuring VCS integration allows Terraform Cloud to automatically queue runs when changes are pushed to the linked repository. The workspace will use the Terraform configuration files from the repository at the specified branch.

### WorkspaceParams

**Type:** Object

**Description:** Parameters for workspace operations without routing fields. Used to specify configuration parameters for creating or updating workspaces.

**Fields:**
- `name` (string, optional): Name of the workspace
- `description` (string, optional): Human-readable description
- `execution_mode` (string, optional): How operations are executed (remote, local, agent)
- `agent_pool_id` (string, optional): Agent pool ID (required when execution_mode=agent)
- `assessments_enabled` (boolean, optional): Whether to perform health assessments
- `auto_apply` (boolean, optional): Whether to auto-apply successful plans from VCS/CLI
- `auto_apply_run_trigger` (boolean, optional): Whether to auto-apply changes from run triggers
- `auto_destroy_at` (string, optional): Timestamp when the next destroy run will occur
- `auto_destroy_activity_duration` (string, optional): Auto-destroy duration based on inactivity
- `file_triggers_enabled` (boolean, optional): Whether to filter runs based on file paths
- `working_directory` (string, optional): Directory to execute commands in
- `speculative_enabled` (boolean, optional): Whether to allow speculative plans
- `terraform_version` (string, optional): Version of Terraform to use (default: latest)
- `global_remote_state` (boolean, optional): Allow all workspaces to access this state
- `vcs_repo` (VcsRepoConfig, optional): VCS repository configuration
- `allow_destroy_plan` (boolean, optional): Allow destruction plans (default: true)
- `queue_all_runs` (boolean, optional): Whether runs should be queued immediately
- `source_name` (string, optional): Where workspace settings originated
- `source_url` (string, optional): URL to origin source
- `trigger_prefixes` (array, optional): List of paths that trigger runs
- `trigger_patterns` (array, optional): List of glob patterns that trigger runs
- `setting_overwrites` (object, optional): Attributes with organization-level defaults

**JSON representation:**
```json
{
  "data": {
    "type": "workspaces",
    "attributes": {
      "name": "my-workspace",
      "description": "Example workspace for terraform configurations",
      "terraform-version": "1.5.0",
      "working-directory": "terraform/",
      "auto-apply": true,
      "file-triggers-enabled": true,
      "trigger-patterns": ["**/*.tf", "*.tfvars"],
      "vcs-repo": {
        "identifier": "organization/repo-name",
        "oauth-token-id": "ot-1234abcd",
        "branch": "main"
      }
    }
  }
}
```

**Validation Rules:**
- Workspace names must be unique within an organization
- When using `agent` execution mode, `agent_pool_id` must be provided
- `terraform_version` must be a valid Terraform version string
- `trigger_patterns` and `trigger_prefixes` can only be used when `file_triggers_enabled` is true

### WorkspaceCreateRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for creating a workspace.

**Fields:**
- `organization` (string, required): The organization name
- `name` (string, required): The name for the new workspace
- `params` (WorkspaceParams, optional): Additional configuration options

**Used by:**
- `create_workspace` tool function to validate workspace creation parameters

### WorkspaceUpdateRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for updating a workspace.

**Fields:**
- `organization` (string, required): The organization name
- `workspace_name` (string, required): The name of the workspace to update
- `params` (WorkspaceParams, optional): Settings to update

**Used by:**
- `update_workspace` tool function to validate workspace update parameters

### WorkspaceListRequest

**Type:** Request Validation Model

**Description:** Parameters for listing workspaces in an organization.

**Fields:**
- `organization` (string, required): The name of the organization to list workspaces from
- `page_number` (integer, optional): Page number to fetch (default: 1)
- `page_size` (integer, optional): Number of results per page (default: 20, max: 100)
- `search` (string, optional): Substring to search for in workspace names

**Usage Context:**
Used to retrieve a paginated list of workspaces in an organization, with optional filtering by name search.

### WorkspaceLockRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for locking a workspace.

**Fields:**
- `workspace_id` (string, required): The ID of the workspace to lock
- `reason` (string, optional): Explanation for locking the workspace

**Used by:**
- `lock_workspace` tool function to validate workspace locking parameters

### DataRetentionPolicyRequest

**Type:** Request Validation Model

**Description:** Parameters for setting a data retention policy on a workspace.

**Fields:**
- `workspace_id` (string, required): The ID of the workspace to set the policy for
- `days` (integer, required): Number of days to retain data

**JSON representation:**
```json
{
  "data": {
    "type": "workspace-settings",
    "attributes": {
      "data-retention-days": 30
    }
  }
}
```

**Usage Context:**
Data retention policies control how long Terraform Cloud retains state versions and run history for a workspace, helping manage storage usage and comply with data policies.

## API Response Structure

### Workspace Details Response

```json
{
  "data": {
    "id": "ws-SihZTyXKfNXUWuUa",
    "type": "workspaces",
    "attributes": {
      "name": "my-workspace",
      "description": "Example workspace for terraform configurations",
      "auto-apply": true,
      "created-at": "2023-05-01T12:34:56Z",
      "environment": "default",
      "execution-mode": "remote",
      "file-triggers-enabled": true,
      "global-remote-state": false,
      "locked": false,
      "terraform-version": "1.5.0",
      "trigger-patterns": ["**/*.tf", "*.tfvars"],
      "working-directory": "terraform/"
    },
    "relationships": {
      "organization": {
        "data": {
          "id": "org-ABcd1234",
          "type": "organizations"
        }
      },
      "current-run": {
        "data": null
      },
      "latest-run": {
        "data": {
          "id": "run-CKJhKBXrxZuc9WLS",
          "type": "runs"
        }
      }
    },
    "links": {
      "self": "/api/v2/organizations/my-org/workspaces/my-workspace"
    }
  }
}
```

### List Workspaces Response

```json
{
  "data": [
    {
      "id": "ws-SihZTyXKfNXUWuUa",
      "type": "workspaces",
      "attributes": {
        "name": "production",
        "description": "Production infrastructure",
        "terraform-version": "1.5.0",
        "created-at": "2023-05-01T12:34:56Z",
        "execution-mode": "remote"
      },
      "relationships": {
        "organization": {
          "data": {
            "id": "org-ABcd1234",
            "type": "organizations"
          }
        },
        "current-state-version": {
          "data": {
            "id": "sv-12345abcde",
            "type": "state-versions"
          }
        }
      }
    },
    {
      "id": "ws-TjqZUyYLfOXWhwbC",
      "type": "workspaces",
      "attributes": {
        "name": "staging",
        "description": "Staging infrastructure",
        "terraform-version": "1.5.0",
        "created-at": "2023-05-02T09:12:34Z",
        "execution-mode": "remote"
      },
      "relationships": {
        "organization": {
          "data": {
            "id": "org-ABcd1234",
            "type": "organizations"
          }
        }
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

- [Workspace Tools](../tools/workspace.md)
- [Organization Models](organization.md)
- [Run Models](run.md)
- [Project Models](project.md)
- [Terraform Cloud API - Workspaces](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces)