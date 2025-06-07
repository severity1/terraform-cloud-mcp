# Apply Models

This document describes the data models used for apply operations in Terraform Cloud.

## Overview

Apply models provide structure and validation for interacting with the Terraform Cloud Apply API. These models define apply statuses, execution details, and request validation for retrieving apply information and logs.

## Models Reference

### ApplyStatus

**Type:** Enum (string)

**Description:** Represents the possible states an apply can be in during its lifecycle.

**Values:**
- `pending`: Apply has not yet started
- `queued`: Apply is queued for execution
- `running`: Apply is currently executing
- `errored`: Apply encountered an error
- `canceled`: Apply was canceled
- `finished`: Apply completed successfully
- `unreachable`: Apply is in an unreachable state

**Usage Context:**
Used to determine the current state of an apply and whether it has completed successfully.

```python
from terraform_cloud_mcp.models import ApplyStatus

# Check the status of an apply
if apply_response["data"]["attributes"]["status"] == ApplyStatus.FINISHED:
    print("Apply completed successfully")
elif apply_response["data"]["attributes"]["status"] == ApplyStatus.ERRORED:
    print("Apply encountered an error")
```

### ApplyExecutionDetails

**Type:** Object

**Description:** Contains information about how an apply was executed, particularly for agent-based execution.

**Fields:**
- `agent_id` (string, optional): ID of the agent that executed the apply
- `agent_name` (string, optional): Name of the agent that executed the apply
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

**Notes:**
- Field names in JSON responses use kebab-case format (e.g., "agent-id")
- Field names in the model use snake_case format (e.g., agent_id)

### ApplyStatusTimestamps

**Type:** Object

**Description:** Captures timing information for various stages in an apply's lifecycle.

**Fields:**
- `queued_at` (string, optional): ISO8601 timestamp when the apply was queued
- `started_at` (string, optional): ISO8601 timestamp when apply execution started
- `finished_at` (string, optional): ISO8601 timestamp when apply execution completed

**JSON representation:**
```json
{
  "status-timestamps": {
    "queued-at": "2023-09-01T12:00:00Z",
    "started-at": "2023-09-01T12:01:00Z",
    "finished-at": "2023-09-01T12:05:00Z"
  }
}
```

**Notes:**
- Field names in JSON responses use kebab-case format (e.g., "queued-at")
- Field names in the model use snake_case format (e.g., queued_at)
- All timestamp fields follow ISO8601 format
- Can be used to calculate apply duration and queue waiting time

### ApplyRequest

**Type:** Request Validation Model

**Description:** Used to validate apply ID parameters in API requests.

**Fields:**
- `apply_id` (string, required): The ID of the apply to retrieve
  - Format: Must match pattern "apply-[a-zA-Z0-9]{16}"
  - Example: "apply-AbCdEfGhIjKlMnOp"

**Validation Rules:**
- Apply ID must start with "apply-" prefix
- Must contain exactly 16 alphanumeric characters after the prefix

**Used by:**
- `get_apply_details` and `get_apply_logs` tool functions to validate the apply ID format before making API requests

### ApplyErroredStateRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for retrieving errored state information.

**Fields:**
- `apply_id` (string, required): The ID of the apply with a failed state upload
  - Format: Must match pattern "apply-[a-zA-Z0-9]{16}"
  - Example: "apply-AbCdEfGhIjKlMnOp"

**Validation Rules:**
- Apply ID must start with "apply-" prefix
- Must contain exactly 16 alphanumeric characters after the prefix

**Used by:**
- `get_errored_state` tool function to validate the apply ID format before making API requests

## API Response Structure

### Apply Details Response

```json
{
  "data": {
    "id": "apply-AbCdEfGhIjKlMnOp",
    "type": "applies",
    "attributes": {
      "status": "finished",
      "status-timestamps": {
        "queued-at": "2023-09-01T12:00:00Z",
        "started-at": "2023-09-01T12:01:00Z",
        "finished-at": "2023-09-01T12:05:00Z"
      },
      "log-read-url": "https://archivist.terraform.io/v1/object/apply-AbCdEfGhIjKlMnOp",
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
      "state-versions": {
        "data": [
          {
            "id": "sv-AbCdEfGhIjKlMnOp",
            "type": "state-versions"
          }
        ]
      }
    }
  }
}
```

### Apply Logs Response

```json
{
  "content": "Terraform v1.4.6\nApplying changes...\nAWS instance: Creating...\nAWS instance: Creation complete\nApply complete! Resources: 1 added, 0 changed, 0 destroyed."
}
```

### Errored State Response

```json
{
  "terraform_state": {
    "version": 4,
    "terraform_version": "1.4.6",
    "serial": 15,
    "lineage": "12345678-90ab-cdef-1234-567890abcdef",
    "resources": [
      {
        "mode": "managed",
        "type": "aws_instance",
        "name": "example",
        "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
        "instances": [...]
      }
    ]
  }
}
```

## Related Resources

- [Apply Tools](../tools/apply.md)
- [Run Models](run.md)
- [Terraform Cloud API - Applies](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies)