# CLAUDE.md for models/

This file provides guidance about the data models used in this repository.

## Models Overview

The models directory contains Pydantic data models for validating Terraform Cloud API requests. These models provide:

1. Input validation for API requests
2. Type safety through static typing
3. Consistent serialization/deserialization
4. Field aliases for API compatibility

We validate requests using Pydantic models but do not validate responses (responses are typed as `APIResponse = Dict[str, Any]`).

## Key Components

- **base.py**: Base model classes and common types
  - `BaseModelConfig`: Core configuration for all models
  - `APIRequest`: Base class for all API requests
  - Common enums used across modules
  - `APIResponse` type alias

- Domain-specific models:
  - **account.py**: Account-related models
  - **workspaces.py**: Workspace management models
  - **runs.py**: Run management models
  - **plans.py**: Plan management models
  - **applies.py**: Apply management models
  - **organizations.py**: Organization management models
  - **projects.py**: Project management models
  - **cost_estimates.py**: Cost estimation models
  - **assessment_results.py**: Health assessment results models

## Pydantic Model Pattern

Each domain follows a consistent pattern:

```python
# Request model for specific operations
class ExampleRequest(APIRequest):
    """Request model for example operation."""
    field_name: str = Field(..., alias="field-name")
    optional_field: Optional[bool] = Field(False, alias="optional-field")

# Parameters model for flexible configurations
class ExampleParams(APIRequest):
    """Parameters for example operations without routing fields."""
    name: Optional[str] = None
    description: Optional[str] = None
    
# Enum for constrained choices
class ExampleStatus(str, Enum):
    """Status options for examples."""
    ACTIVE = "active"
    INACTIVE = "inactive"
```

## Field Handling

- **Required fields**: Use `Field(...)` with no default
- **Optional fields**: Use `Optional[Type]` with a default value
- **Field aliases**: Use `alias="kebab-case-name"` for API compatibility
- **Validation**: Use Field constraints (e.g., `min_length`, `ge`, `le`)
- **Description**: Include field descriptions in docstrings

## Common Patterns

1. **Base Request Models**:
   ```python
   class BaseWorkspaceRequest(APIRequest):
       """Base class with common workspace parameters."""
       name: Optional[str] = None
   ```

2. **Parameter Models**:
   ```python
   class WorkspaceParams(APIRequest):
       """Parameters for workspace operations."""
       description: Optional[str] = None
   ```

3. **Enum Classes**:
   ```python
   class ExecutionMode(str, Enum):
       """Execution mode options."""
       REMOTE = "remote"
       LOCAL = "local"
   ```

## Usage Guidelines

1. Always extend from `APIRequest` for all request models
2. Use field aliases for API compatibility with kebab-case to snake_case mapping
3. Add validation for all fields that have constraints
4. Include proper docstrings with references to Terraform Cloud API docs
5. For new features, follow the pattern in existing models
6. For complex parameter objects, create a separate `*Params` model
7. Use enums for all fields with constrained choices