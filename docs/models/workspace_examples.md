# Workspace Model Examples

## Basic Usage

```python
from terraform_cloud_mcp.models.workspaces import (
    WorkspaceParams,
    VcsRepoConfig,
    ExecutionMode
)

# Creating a basic workspace configuration
workspace_params = WorkspaceParams(
    name="my-workspace",
    description="Example workspace for terraform configurations",
    terraform_version="1.5.0",
    working_directory="terraform/"
)

# Using the ExecutionMode enum for type safety
remote_workspace = WorkspaceParams(
    name="remote-workspace",
    execution_mode=ExecutionMode.REMOTE,
    terraform_version="latest"
)
```

## Common Patterns

```python
# Configure workspace with auto-apply and speculative plans
workspace_config = WorkspaceParams(
    description="Production infrastructure workspace",
    auto_apply=True,
    terraform_version="1.4.6",
    speculative_enabled=True,
    global_remote_state=False
)

# Set up file triggers to control when runs are queued
workspace_with_triggers = WorkspaceParams(
    file_triggers_enabled=True,
    trigger_prefixes=["modules/", "environments/prod/"],
    trigger_patterns=["**/*.tf", "*.tfvars"]
)
```

## Advanced Use Cases

```python
# Connect workspace to a VCS repository
vcs_repo = VcsRepoConfig(
    identifier="organization/repo-name",
    oauth_token_id="ot-1234abcd",
    branch="main",
    ingress_submodules=True
)

vcs_workspace = WorkspaceParams(
    name="vcs-workspace",
    description="Workspace connected to GitHub",
    vcs_repo=vcs_repo,
    auto_apply=False,
    working_directory="environments/staging"
)

# Configure agent execution mode
agent_workspace = WorkspaceParams(
    name="agent-workspace",
    description="Uses self-hosted agent for execution",
    execution_mode=ExecutionMode.AGENT,
    agent_pool_id="apool-1234abcd"
)

# Workspace with custom settings and overrides
custom_workspace = WorkspaceParams(
    name="custom-workspace",
    terraform_version="1.5.0",
    auto_apply=True,
    auto_apply_run_trigger=False,
    queue_all_runs=False,
    setting_overwrites={
        "execution_mode": True,
        "agent_pool_id": True
    }
)
```