# Plan Models

This document describes the data models used for plan operations in Terraform Cloud.

## Overview

Plan models provide structure and validation for interacting with the Terraform Cloud Plans API. These models define plan statuses, execution details, and request validation for retrieving plan information.

## Models Reference

### PlanStatus

**Type:** Enum (string)

**Description:** Represents the possible states a plan can be in during its lifecycle.

**Values:**
- `pending`: Plan has not yet started
- `managed_queued`: Plan is waiting for other runs in the queue
- `queued`: Plan is queued for execution
- `running`: Plan is currently executing
- `errored`: Plan encountered an error
- `canceled`: Plan was canceled
- `finished`: Plan completed successfully

**Usage Context:**
Used to determine the current state of a plan and whether it has completed successfully.

### ExecutionDetails

**Type:** Object

**Description:** Contains information about how a plan was executed, particularly for agent-based execution.

**Fields:**
- `agent_id` (string, optional): ID of the agent that executed the plan
- `agent_name` (string, optional): Name of the agent that executed the plan
- `agent_pool_id` (string, optional): ID of the agent pool the executing agent belongs to
- `agent_pool_name` (string, optional): Name of the agent pool the executing agent belongs to

**JSON representation:**
```json
{
  "execution-details": {
    "agent-id": "agent-AbCdEfGhIjKlMnOp",
    "agent-name": "production-agent-01",
    "agent-pool-id": "apool-AbCdEfGhIjKlMnOp",
    "agent-pool-name": "Production Agents"
  }
}
```

### StatusTimestamps

**Type:** Object

**Description:** Captures timing information for various stages in a plan's lifecycle.

**Fields:**
- `queued_at` (string, optional): ISO8601 timestamp when the plan was queued
- `pending_at` (string, optional): ISO8601 timestamp when the plan was pending
- `started_at` (string, optional): ISO8601 timestamp when plan execution started
- `finished_at` (string, optional): ISO8601 timestamp when plan execution completed

**JSON representation:**
```json
{
  "status-timestamps": {
    "queued-at": "2023-09-01T12:00:00Z",
    "pending-at": "2023-09-01T12:01:00Z",
    "started-at": "2023-09-01T12:02:00Z",
    "finished-at": "2023-09-01T12:10:00Z"
  }
}
```

**Notes:**
- Field names in JSON responses use kebab-case format (e.g., "queued-at")
- Field names in the model use snake_case format (e.g., queued_at)
- All timestamp fields follow ISO8601 format

### PlanRequest

**Type:** Request Validation Model

**Description:** Used to validate plan ID parameters in API requests.

**Fields:**
- `plan_id` (string, required): The ID of the plan to retrieve
  - Format: Must match pattern "plan-[a-zA-Z0-9]{16}"
  - Example: "plan-AbCdEfGhIjKlMnOp"

**Validation Rules:**
- Plan ID must start with "plan-" prefix
- Must contain exactly 16 alphanumeric characters after the prefix

### PlanJsonOutputRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for retrieving the JSON output of a plan.

**Fields:**
- `plan_id` (string, required): The ID of the plan to retrieve JSON output for
  - Format: Must match pattern "plan-[a-zA-Z0-9]{16}"
  - Example: "plan-AbCdEfGhIjKlMnOp"

### RunPlanJsonOutputRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for retrieving the JSON output of a run's plan.

**Fields:**
- `run_id` (string, required): The ID of the run to retrieve plan JSON output for
  - Format: Must match pattern "run-[a-zA-Z0-9]{16}"
  - Example: "run-AbCdEfGhIjKlMnOp"

## API Response Structure

### Plan Details Response

```json
{
  "data": {
    "id": "plan-AbCdEfGhIjKlMnOp",
    "type": "plans",
    "attributes": {
      "status": "finished",
      "status-timestamps": {
        "queued-at": "2023-09-01T12:00:00Z",
        "pending-at": "2023-09-01T12:01:00Z",
        "started-at": "2023-09-01T12:02:00Z",
        "finished-at": "2023-09-01T12:10:00Z"
      },
      "resource-additions": 3,
      "resource-changes": 2,
      "resource-destructions": 1,
      "execution-details": {
        "agent-id": "agent-AbCdEfGhIjKlMnOp",
        "agent-name": "production-agent-01",
        "agent-pool-id": "apool-AbCdEfGhIjKlMnOp",
        "agent-pool-name": "Production Agents"
      }
    },
    "relationships": {
      "run": {
        "data": {
          "id": "run-AbCdEfGhIjKlMnOp",
          "type": "runs"
        }
      },
      "state-versions": {
        "data": {
          "id": "sv-AbCdEfGhIjKlMnOp",
          "type": "state-versions"
        }
      }
    },
    "links": {
      "self": "/api/v2/plans/plan-AbCdEfGhIjKlMnOp",
      "json-output": "/api/v2/plans/plan-AbCdEfGhIjKlMnOp/json-output"
    }
  }
}
```

### Plan JSON Output Response

The plan JSON output response contains a string in the `data` field that can be parsed to access detailed information about the planned resource changes:

```json
{
  "data": "<JSON string containing the full plan details>"
}
```

The parsed plan data includes information about:
- Resource additions, changes, and deletions
- Output changes
- Provider configurations
- Prior state details
- Terraform version information

## Related Resources

- [Plan Tools](../tools/plan.md)
- [Run Models](run.md)
- [Terraform Cloud API - Plans](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/plans)