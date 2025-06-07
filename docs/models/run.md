# Run Models

This document describes the data models used for run operations in Terraform Cloud.

## Overview

Run models provide structure and validation for initiating and managing runs in Terraform Cloud. These models define run configuration options, variables, targeting, and behavior settings. Runs represent the execution of Terraform plans and applies, serving as the primary method for making infrastructure changes.

## Models Reference

### RunVariable

**Type:** Object

**Description:** Defines a variable to be included with a specific run. Run variables override workspace variables for the duration of the run.

**Fields:**
- `key` (string, required): The variable name (max length: 128)
- `value` (string, required): The variable value (max length: 256)

**JSON representation:**
```json
{
  "key": "environment",
  "value": "production"
}
```

**Usage Context:**
Run variables provide a way to override workspace variables temporarily for a specific run without changing the workspace configuration. This is useful for testing changes with different variable values or handling one-off scenarios.

### RunOperation

**Type:** Enum (string)

**Description:** Describes the type of operation being performed by a run.

**Values:**
- `plan`: Standard planning operation
- `plan_destroy`: Planning a destroy operation
- `apply`: Standard apply operation
- `destroy`: Destroying resources operation

**Usage Context:**
Used for filtering runs and determining the type of operation being performed.

### RunSource

**Type:** Enum (string)

**Description:** Indicates the origin that initiated the run.

**Values:**
- `api`: Run was created via the API
- `cli`: Run was created using Terraform CLI
- `ui`: Run was created through the web UI
- `vcs`: Run was triggered by a VCS change
- `run_trigger`: Run was triggered by another workspace's changes

**Usage Context:**
Useful for identifying how a run was created and for filtering runs by their origin.

### RunStatusGroup

**Type:** Enum (string)

**Description:** Categorizes runs into logical groupings based on their current state.

**Values:**
- `pending`: Runs that haven't completed their execution (includes planning, applying)
- `completed`: Runs that have finished execution successfully (planned, applied, etc.)
- `failed`: Runs that have encountered errors or been canceled
- `discarded`: Runs whose changes were not applied

**Usage Context:**
Provides a higher-level categorization of run statuses for filtering and reporting.

### RunParams

**Type:** Object

**Description:** Parameters for run operations. Used to specify configuration options when creating a run.

**Fields:**
- `message` (string, optional): Description of the run's purpose
- `is_destroy` (boolean, optional): Whether to destroy all resources (default: false)
- `auto_apply` (boolean, optional): Whether to auto-apply after successful plan
- `refresh` (boolean, optional): Whether to refresh state before planning (default: true)
- `refresh_only` (boolean, optional): Only refresh state without planning changes (default: false)
- `plan_only` (boolean, optional): Create speculative plan without applying (default: false)
- `allow_empty_apply` (boolean, optional): Allow applies with no changes (default: false)
- `target_addrs` (array, optional): List of resource addresses to target
- `replace_addrs` (array, optional): List of resource addresses to force replacement
- `variables` (array, optional): Run-specific variables that override workspace variables
- `terraform_version` (string, optional): Specific Terraform version for this run
- `save_plan` (boolean, optional): Save the plan for later execution (default: false)
- `debugging_mode` (boolean, optional): Enable extended debug logging (default: false)
- `allow_config_generation` (boolean, optional): Allow generating config for imports (default: false)

**JSON representation:**
```json
{
  "data": {
    "type": "runs",
    "attributes": {
      "message": "Deploy infrastructure changes",
      "plan-only": false,
      "is-destroy": false,
      "refresh": true,
      "auto-apply": false,
      "target-addrs": ["module.network", "aws_instance.web_servers"],
      "replace-addrs": ["module.database.aws_db_instance.main"],
      "variables": [
        {"key": "environment", "value": "production"},
        {"key": "region", "value": "us-west-2"}
      ]
    },
    "relationships": {
      "workspace": {
        "data": {
          "id": "ws-example123",
          "type": "workspaces"
        }
      }
    }
  }
}
```

**Validation Rules:**
- When using `plan_only`, the run will not proceed to apply phase
- If `is_destroy` is true, the run will create a plan to destroy all resources
- `terraform_version` can only be specified for plan-only runs
- `replace_addrs` and `target_addrs` must be valid resource addresses

### RunStatus

**Type:** Enum (string)

**Description:** Represents the possible states of a run during its lifecycle.

**Values:**
- `pending`: Not yet started
- `planning`: Currently running the plan phase
- `planned`: Plan phase completed successfully
- `cost_estimating`: Cost estimate in progress
- `cost_estimated`: Cost estimate completed
- `policy_checking`: Policy check in progress
- `policy_override`: Policy check soft-failed, requires override
- `policy_checked`: Policy check passed
- `confirmed`: Plan confirmed for apply
- `planned_and_finished`: Plan completed, no changes required
- `applying`: Currently applying changes
- `applied`: Apply phase completed successfully
- `discarded`: Discarded and not applied
- `errored`: Encountered an error during the run
- `canceled`: Was canceled during execution
- `force_canceled`: Was forcibly canceled during execution

**Usage Context:**
Used to determine the current phase and state of a run and what actions can be taken on it. For example:
- Only runs in `planned` status can be applied
- Only runs in `planning`, `applying`, or other active states can be canceled

### RunCreateRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for creating a run.

**Fields:**
- `workspace_id` (string, required): The ID of the workspace to create a run in
- `params` (RunParams, optional): Configuration options for the run

**Used by:**
- `create_run` tool function to validate run creation parameters

### RunDetailsRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for retrieving run details.

**Fields:**
- `run_id` (string, required): The ID of the run to retrieve details for
  - Format: Must match pattern "run-[a-zA-Z0-9]{16}"
  - Example: "run-AbCdEfGhIjKlMnOp"

**Validation Rules:**
- Run ID must start with "run-" prefix
- Must contain exactly 16 alphanumeric characters after the prefix

### RunActionRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for performing actions on a run.

**Fields:**
- `run_id` (string, required): The ID of the run to perform an action on
- `comment` (string, optional): An optional explanation for the action

**Used by:**
- `apply_run`, `discard_run`, `cancel_run`, `force_cancel_run` tool functions

### RunListRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for listing runs in a workspace.

**Fields:**
- `workspace_id` (string, required): The workspace ID to list runs for
- `page_number` (int, optional): Page number to fetch (default: 1)
- `page_size` (int, optional): Number of results per page (default: 20)
- Filter fields for more specific results:
  - `filter_operation`, `filter_status`, `filter_source`, `filter_status_group`

**Used by:**
- `list_runs_in_workspace` tool function to validate listing parameters

## API Response Structure

### Run Details Response

```json
{
  "data": {
    "id": "run-CKJhKBXrxZuc9WLS",
    "type": "runs",
    "attributes": {
      "status": "planned",
      "message": "Deploy infrastructure changes",
      "has-changes": true,
      "created-at": "2023-05-05T15:45:22Z",
      "is-destroy": false,
      "source": "tfe-cli",
      "status-timestamps": {
        "planned-at": "2023-05-05T15:46:02Z"
      }
    },
    "relationships": {
      "workspace": {
        "data": {
          "id": "ws-SihZTyXKfNXUWuUa",
          "type": "workspaces"
        }
      },
      "plan": {
        "data": {
          "id": "plan-j9yycwFSJ2Mn8wuC",
          "type": "plans"
        }
      },
      "cost-estimate": {
        "data": {
          "id": "ce-BPvFFrYCqRV6qVBK",
          "type": "cost-estimates"
        }
      }
    },
    "links": {
      "self": "/api/v2/runs/run-CKJhKBXrxZuc9WLS"
    }
  }
}
```

### List Runs Response

```json
{
  "data": [
    {
      "id": "run-CKJhKBXrxZuc9WLS",
      "type": "runs",
      "attributes": {
        "status": "applied",
        "message": "Weekly infrastructure update",
        "has-changes": true,
        "created-at": "2023-05-05T15:45:22Z",
        "is-destroy": false,
        "source": "tfe-cli"
      }
    },
    {
      "id": "run-DKJhKBXrxZuc9WLA",
      "type": "runs",
      "attributes": {
        "status": "planned",
        "message": "Update database configuration",
        "has-changes": true,
        "created-at": "2023-05-06T09:12:34Z",
        "is-destroy": false,
        "source": "api"
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

- [Run Tools](../tools/run.md)
- [Plan Models](plan.md)
- [Apply Models](apply.md)
- [Cost Estimate Models](cost_estimate.md)
- [Terraform Cloud API - Runs](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run)