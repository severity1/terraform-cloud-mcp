# Workspace Tools Examples

## Basic Usage

```python
# List workspaces in an organization
workspaces = await list_workspaces(organization="my-organization")

# Get details for a specific workspace
workspace = await get_workspace_details(
    organization="my-organization", 
    workspace_name="my-workspace"
)

# Create a new workspace
new_workspace = await create_workspace(
    organization="my-organization",
    name="new-workspace"
)
```

## Common Patterns

```python
# Update a workspace with new settings
updated_workspace = await update_workspace(
    organization="my-organization",
    workspace_name="my-workspace",
    params={
        "description": "Updated workspace description",
        "terraform_version": "1.5.0",
        "auto_apply": True,
        "working_directory": "terraform/"
    }
)

# Lock a workspace before maintenance
locked_workspace = await lock_workspace(
    workspace_id="ws-1234abcd",
    reason="Scheduled maintenance"
)

# Unlock a workspace when maintenance is complete
unlocked_workspace = await unlock_workspace(
    workspace_id="ws-1234abcd"
)
```

## Advanced Use Cases

```python
# Create a workspace with VCS repository connection
from terraform_cloud_mcp.models.workspaces import VcsRepoConfig

new_workspace = await create_workspace(
    organization="my-organization",
    name="vcs-connected-workspace",
    params={
        "description": "Workspace connected to GitHub",
        "execution_mode": "remote",
        "vcs_repo": VcsRepoConfig(
            identifier="my-org/my-repo",
            oauth_token_id="ot-1234abcd",
            branch="main",
            ingress_submodules=False
        )
    }
)

# Safely delete a workspace with cleanup
await safe_delete_workspace(
    organization="my-organization",
    workspace_name="workspace-to-delete"
)

# Force unlock a stuck workspace (use with caution)
await force_unlock_workspace(
    workspace_id="ws-1234abcd"
)
```