# Run Tools Examples

## Basic Usage

```python
# Create a new run in a workspace
run = await create_run(
    workspace_id="ws-1234abcd"
)

# Get details for a specific run
run_details = await get_run_details(
    run_id="run-1234abcd"
)

# List runs in a workspace
runs = await list_runs_in_workspace(
    workspace_id="ws-1234abcd"
)
```

## Common Patterns

```python
# Create a run with custom message and auto-apply
from terraform_cloud_mcp.models.runs import RunParams

run = await create_run(
    workspace_id="ws-1234abcd",
    params=RunParams(
        message="Deploy production changes",
        auto_apply=True
    )
)

# List runs with filtering and pagination
pending_runs = await list_runs_in_workspace(
    workspace_id="ws-1234abcd",
    filter_status="pending,planning",
    page_size=50
)

# Apply a run that's waiting for confirmation
await apply_run(
    run_id="run-1234abcd",
    comment="Approved by change management"
)

# Discard a run that's no longer needed
await discard_run(
    run_id="run-1234abcd",
    comment="No longer required due to strategy change"
)
```

## Advanced Use Cases

```python
# Create a plan-only run with variables
from terraform_cloud_mcp.models.runs import RunParams, RunVariable

run = await create_run(
    workspace_id="ws-1234abcd",
    params=RunParams(
        message="Test configuration changes",
        plan_only=True,
        variables=[
            RunVariable(key="environment", value="staging"),
            RunVariable(key="instance_count", value="5")
        ]
    )
)

# Create a destroy run
destroy_run = await create_run(
    workspace_id="ws-1234abcd",
    params=RunParams(
        is_destroy=True,
        message="Decommission environment",
        refresh=True
    )
)

# Cancel a run in progress
await cancel_run(
    run_id="run-1234abcd",
    comment="Canceling due to configuration error"
)

# Force cancel a stuck run (use with caution)
await force_cancel_run(
    run_id="run-1234abcd",
    comment="Run stuck in planning state for over 1 hour"
)
```