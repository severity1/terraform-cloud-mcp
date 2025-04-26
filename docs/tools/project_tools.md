# Project Tools Examples

## Basic Usage

```python
# List all projects in an organization
projects = await list_projects(organization="my-organization")

# Get details for a specific project
project_details = await get_project_details(project_id="prj-WsVcWRr7SfxRci1v")

# List tag bindings for a project
tag_bindings = await list_project_tag_bindings(project_id="prj-WsVcWRr7SfxRci1v")
```

## Common Patterns

```python
# Create a new project with basic settings
from terraform_cloud_mcp.models.projects import ProjectParams

new_project = await create_project(
    organization="my-organization", 
    name="Infrastructure Project"
)

# List projects with pagination and search filtering
search_results = await list_projects(
    organization="my-organization",
    page_number=1,
    page_size=10,
    query="infrastructure"
)

# Update project settings
from terraform_cloud_mcp.models.projects import ProjectParams

updated_project = await update_project(
    project_id="prj-WsVcWRr7SfxRci1v",
    params=ProjectParams(
        name="Updated Project Name",
        description="Updated project description"
    )
)
```

## Advanced Use Cases

```python
# Create a new project with detailed configuration
from terraform_cloud_mcp.models.projects import (
    ProjectParams,
    TagBinding
)

complete_project = await create_project(
    organization="my-organization",
    name="Production Infrastructure",
    params=ProjectParams(
        description="Production environment resources",
        auto_destroy_activity_duration="30d",
        tag_bindings=[
            TagBinding(key="environment", value="production"),
            TagBinding(key="team", value="platform"),
            TagBinding(key="cost-center", value="123456")
        ]
    )
)

# Add or update tag bindings on an existing project
from terraform_cloud_mcp.models.projects import TagBinding

updated_tags = await add_update_project_tag_bindings(
    project_id="prj-WsVcWRr7SfxRci1v",
    tag_bindings=[
        TagBinding(key="environment", value="staging"),
        TagBinding(key="version", value="2.0")
    ]
)

# Move workspaces to a project
await move_workspaces_to_project(
    project_id="prj-WsVcWRr7SfxRci1v",
    workspace_ids=["ws-AQEct2XFuH4HBsmS", "ws-BqZ9wfcV7KLmJT2n"]
)

# Delete a project (will fail if it contains workspaces)
await delete_project(project_id="prj-YoriCxAawTMDLswn")
```