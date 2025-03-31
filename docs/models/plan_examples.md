# Plan Model Examples

This document provides examples of using the Plan models in the Terraform Cloud MCP.

## PlanStatus Enum

The `PlanStatus` enum represents the various states a plan can be in during its lifecycle.

```python
from terraform_cloud_mcp.models import PlanStatus

# Check if a plan is running
if plan_status == PlanStatus.RUNNING:
    print("Plan is still in progress")

# Check if a plan is finished
if plan_status == PlanStatus.FINISHED:
    print("Plan has completed successfully")

# Check if a plan had an error
if plan_status == PlanStatus.ERRORED:
    print("Plan encountered an error during execution")
```

## ExecutionDetails Model

The `ExecutionDetails` model contains information about how a plan was executed, particularly useful for agent-based execution.

```python
from terraform_cloud_mcp.models import ExecutionDetails

# Create execution details for agent execution
execution_details = ExecutionDetails(
    agent_id="agent-AbCdEfGhIjKlMnOp",
    agent_name="production-agent-01",
    agent_pool_id="apool-AbCdEfGhIjKlMnOp",
    agent_pool_name="Production Agents"
)

# Access execution details
agent_name = execution_details.agent_name
agent_pool = execution_details.agent_pool_name
```

## StatusTimestamps Model

The `StatusTimestamps` model captures timing information about a plan's execution.

```python
from terraform_cloud_mcp.models import StatusTimestamps

# Create timestamps for a plan
timestamps = StatusTimestamps(
    queued_at="2023-09-01T12:00:00Z",
    pending_at="2023-09-01T12:01:00Z",
    started_at="2023-09-01T12:02:00Z",
    finished_at="2023-09-01T12:10:00Z"
)

# Access timestamp information
started = timestamps.started_at
finished = timestamps.finished_at
```

## PlanRequest Model

The `PlanRequest` model is used to validate plan ID parameters.

```python
from terraform_cloud_mcp.models import PlanRequest

# Create a plan request
request = PlanRequest(plan_id="plan-AbCdEfGhIjKlMnOp")

# Access the validated plan ID
plan_id = request.plan_id
```

## PlanJsonOutputRequest Model

The `PlanJsonOutputRequest` model is used to validate parameters for plan JSON output requests.

```python
from terraform_cloud_mcp.models import PlanJsonOutputRequest

# Create a plan JSON output request
request = PlanJsonOutputRequest(plan_id="plan-AbCdEfGhIjKlMnOp")

# Access the validated plan ID
plan_id = request.plan_id
```

## RunPlanJsonOutputRequest Model

The `RunPlanJsonOutputRequest` model is used to validate parameters for run plan JSON output requests.

```python
from terraform_cloud_mcp.models import RunPlanJsonOutputRequest

# Create a run plan JSON output request
request = RunPlanJsonOutputRequest(run_id="run-AbCdEfGhIjKlMnOp")

# Access the validated run ID
run_id = request.run_id
```

## Example Plan Response

While responses aren't modeled with Pydantic, here's an example of a plan response structure:

```python
plan_response = {
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
        }
    }
}
```

## Example Plan JSON Output Response

```python
plan_json_output_response = {
    "data": {
        "id": "plan-json-AbCdEfGhIjKlMnOp",
        "type": "plan-exports",
        "attributes": {
            "url": "https://app.terraform.io/api/v2/plans/plan-AbCdEfGhIjKlMnOp/json-output?token=temporary-authentication-token"
        }
    }
}
```

This URL can be used to download the JSON-formatted plan, which includes detailed information about resource changes.