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
    "data": "{\"format_version\":\"1.2\",\"terraform_version\":\"1.11.2\",\"planned_values\":{\"root_module\":{}},\"resource_changes\":[{\"address\":\"null_resource.example\",\"mode\":\"managed\",\"type\":\"null_resource\",\"name\":\"example\",\"provider_name\":\"registry.terraform.io/hashicorp/null\",\"change\":{\"actions\":[\"delete\"],\"before\":{\"id\":\"398772014703504259\",\"triggers\":{\"random_value\":\"wskqamu3a6ql2vpp\"}},\"after\":null,\"after_unknown\":{},\"before_sensitive\":{\"triggers\":{}},\"after_sensitive\":false}},{\"address\":\"random_string.example\",\"mode\":\"managed\",\"type\":\"random_string\",\"name\":\"example\",\"provider_name\":\"registry.terraform.io/hashicorp/random\",\"change\":{\"actions\":[\"delete\"],\"before\":{\"id\":\"wskqamu3a6ql2vpp\",\"keepers\":null,\"length\":16,\"lower\":true,\"min_lower\":0,\"min_numeric\":0,\"min_special\":0,\"min_upper\":0,\"number\":true,\"numeric\":true,\"override_special\":null,\"result\":\"wskqamu3a6ql2vpp\",\"special\":false,\"upper\":false},\"after\":null,\"after_unknown\":{},\"before_sensitive\":{},\"after_sensitive\":false}}],\"output_changes\":{\"random_string_value\":{\"actions\":[\"delete\"],\"before\":\"wskqamu3a6ql2vpp\",\"after\":null,\"after_unknown\":false,\"before_sensitive\":false,\"after_sensitive\":false}},\"prior_state\":{\"format_version\":\"1.0\",\"terraform_version\":\"1.11.2\",\"values\":{\"outputs\":{\"random_string_value\":{\"sensitive\":false,\"value\":\"wskqamu3a6ql2vpp\",\"type\":\"string\"}},\"root_module\":{\"resources\":[{\"address\":\"null_resource.example\",\"mode\":\"managed\",\"type\":\"null_resource\",\"name\":\"example\",\"provider_name\":\"registry.terraform.io/hashicorp/null\",\"schema_version\":0,\"values\":{\"id\":\"398772014703504259\",\"triggers\":{\"random_value\":\"wskqamu3a6ql2vpp\"}},\"sensitive_values\":{\"triggers\":{}},\"depends_on\":[\"random_string.example\"]},{\"address\":\"random_string.example\",\"mode\":\"managed\",\"type\":\"random_string\",\"name\":\"example\",\"provider_name\":\"registry.terraform.io/hashicorp/random\",\"schema_version\":2,\"values\":{\"id\":\"wskqamu3a6ql2vpp\",\"keepers\":null,\"length\":16,\"lower\":true,\"min_lower\":0,\"min_numeric\":0,\"min_special\":0,\"min_upper\":0,\"number\":true,\"numeric\":true,\"override_special\":null,\"result\":\"wskqamu3a6ql2vpp\",\"special\":false,\"upper\":false},\"sensitive_values\":{}}]}}},\"configuration\":{\"provider_config\":{\"null\":{\"name\":\"null\",\"full_name\":\"registry.terraform.io/hashicorp/null\",\"version_constraint\":\"3.2.1\"},\"random\":{\"name\":\"random\",\"full_name\":\"registry.terraform.io/hashicorp/random\",\"version_constraint\":\"3.5.1\"}},\"root_module\":{\"outputs\":{\"random_string_value\":{\"expression\":{\"references\":[\"random_string.example.result\",\"random_string.example\"]}}},\"resources\":[{\"address\":\"null_resource.example\",\"mode\":\"managed\",\"type\":\"null_resource\",\"name\":\"example\",\"provider_config_key\":\"null\",\"expressions\":{\"triggers\":{\"references\":[\"random_string.example.result\",\"random_string.example\"]}},\"schema_version\":0},{\"address\":\"random_string.example\",\"mode\":\"managed\",\"type\":\"random_string\",\"name\":\"example\",\"provider_config_key\":\"random\",\"expressions\":{\"length\":{\"constant_value\":16},\"special\":{\"constant_value\":false},\"upper\":{\"constant_value\":false}},\"schema_version\":2}]}},\"relevant_attributes\":[{\"resource\":\"random_string.example\",\"attribute\":[\"result\"]}],\"timestamp\":\"2025-03-25T06:02:15Z\",\"applyable\":true,\"complete\":true,\"errored\":false}"
}
```

The 'data' field contains a JSON string that can be parsed to access detailed information about the planned resource changes. The JSON includes information about resource additions, changes, deletions, and the configuration that generated the plan.