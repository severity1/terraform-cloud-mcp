# Run Model Examples

## Basic Usage

```python
from terraform_cloud_mcp.models.runs import RunParams, RunVariable

# Create a basic run configuration
run_params = RunParams(
    message="Deploy infrastructure changes"
)

# Create a plan-only run configuration
plan_run = RunParams(
    message="Test configuration changes",
    plan_only=True
)
```

## Common Patterns

```python
# Configure auto-apply settings
auto_apply_run = RunParams(
    message="Apply infrastructure changes automatically",
    auto_apply=True
)

# Create a run with variables
run_with_vars = RunParams(
    message="Deploy with custom variables",
    variables=[
        RunVariable(key="environment", value="production"),
        RunVariable(key="region", value="us-west-2"),
        RunVariable(key="instance_count", value="3")
    ]
)

# Configure run with refresh settings
refresh_run = RunParams(
    message="Update state and apply changes",
    refresh=True,
    refresh_only=False
)
```

## Advanced Use Cases

```python
# Create a destroy run configuration
destroy_run = RunParams(
    message="Decommission development environment",
    is_destroy=True,
    auto_apply=False
)

# Configure a run with targeted resources
targeted_run = RunParams(
    message="Update only specific resources",
    target_addrs=[
        "module.network",
        "aws_instance.web_servers"
    ]
)

# Configure a run that forces replacement of resources
replacement_run = RunParams(
    message="Replace database instances",
    replace_addrs=[
        "module.database.aws_db_instance.main"
    ]
)

# Debug mode run with custom terraform version
debug_run = RunParams(
    message="Debug configuration with specific Terraform version",
    terraform_version="1.3.7",
    debugging_mode=True,
    save_plan=True
)

# Empty apply configuration (allowing applies with no changes)
empty_apply_run = RunParams(
    message="Apply even if no changes detected",
    allow_empty_apply=True
)

# Run with import config generation enabled
import_run = RunParams(
    message="Import existing infrastructure",
    allow_config_generation=True
)
```