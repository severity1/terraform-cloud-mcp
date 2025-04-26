# Project Model Examples

## Basic Usage

```python
from terraform_cloud_mcp.models.projects import (
    ProjectParams,
    TagBinding
)

# Create a basic project configuration
project_params = ProjectParams(
    name="My Project",
    description="Example project for infrastructure"
)

# Create a project with auto-destroy activity duration
auto_destroy_project = ProjectParams(
    name="Temporary Project",
    description="Projects with resources that auto-destroy after inactivity",
    auto_destroy_activity_duration="14d"  # 14 days
)
```

## Common Patterns

```python
# Configure project with tags
from terraform_cloud_mcp.models.projects import TagBinding

tagged_project = ProjectParams(
    name="Production Infrastructure",
    description="Production environment resources",
    tag_bindings=[
        TagBinding(key="environment", value="production"),
        TagBinding(key="team", value="platform"),
        TagBinding(key="cost-center", value="123456")
    ]
)
```

## Advanced Use Cases

```python
# Create a project with complete configuration
complete_project = ProjectParams(
    name="Development Infrastructure",
    description="Development environment resources",
    auto_destroy_activity_duration="7d",
    tag_bindings=[
        TagBinding(key="environment", value="development"),
        TagBinding(key="team", value="engineering"),
        TagBinding(key="auto-destroy", value="enabled")
    ]
)

# Configure tag bindings for update operation
tag_bindings = [
    TagBinding(key="environment", value="staging"),
    TagBinding(key="team", value="qa"),
    TagBinding(key="version", value="1.0")
]
```