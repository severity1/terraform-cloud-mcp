# CLAUDE.md for tools/

This file provides guidance about the MCP tool implementations in this repository.

## Tools Overview

The tools directory contains all Model Context Protocol (MCP) tools that are exposed to AI assistants for interacting with the Terraform Cloud API. Each module implements domain-specific tools following a consistent pattern.

## Key Components

- **__init__.py**: Tool registration and imports
- Domain-specific tool modules:
  - **account.py**: Account management tools
  - **workspaces.py**: Workspace management tools
  - **runs.py**: Run management tools
  - **plans.py**: Plan management tools
  - **applies.py**: Apply management tools
  - **organizations.py**: Organization management tools
  - **projects.py**: Project management tools
  - **cost_estimates.py**: Cost estimate tools
  - **assessment_results.py**: Health assessment results tools

## Tool Implementation Pattern

Each tool follows a consistent implementation pattern:

```python
@handle_api_errors
async def example_tool(
    required_param: str,
    optional_param: int = 0,
    params: Optional[ExampleParams] = None
) -> APIResponse:
    """Tool description with clear context on when and how to use it.
    
    API endpoint: METHOD /path/to/endpoint
    
    Args:
        required_param: Description of parameter
        optional_param: Description including default value
        params: Optional configuration settings:
            - option1: Description of what this option does
            - option2: Description with possible values
            
    Returns:
        Description of return structure and important fields
        
    See:
        docs/tools/example_tools.md for usage examples
    """
    # Validate parameters
    request_params = ExampleRequest(
        required_param=required_param,
        optional_param=optional_param
    )
    
    # Extract parameters from params object
    param_dict = params.model_dump(exclude_none=True) if params else {}
    
    # Create API payload
    payload = create_api_payload(
        resource_type="resource_type",
        model=request_params,
        exclude_fields={"field_to_exclude"}
    )
    
    # Make API request
    return await api_request("endpoint", method="POST", data=payload)
```

## Tool Categories

1. **CRUD Operations**:
   - `create_*` - Create new resources
   - `get_*` - Retrieve resource details
   - `update_*` - Modify existing resources
   - `delete_*` - Remove resources

2. **List Operations**:
   - `list_*` - List and filter resources
   
3. **Action Operations**:
   - `lock_*`, `unlock_*` - Change resource state
   - `apply_*`, `cancel_*` - Control resource processes

4. **Specialized Operations**:
   - Operations specific to certain resource types

## Error Handling

All tools use the `handle_api_errors` decorator from utils/decorators.py to provide consistent error handling, ensuring:

1. Validation errors are properly reported
2. API errors are formatted consistently
3. Unexpected exceptions are caught and formatted

## Guidelines for Adding New Tools

1. Follow the established naming convention for the tool
2. Use the `handle_api_errors` decorator
3. Create corresponding Pydantic models in models/
4. Document the tool thoroughly with docstrings
5. Create usage examples in docs/tools/
6. Register the tool in server.py
7. Use utility functions from utils/ for payload creation and parameter handling

## Related Documentation

For each tool category, refer to the corresponding documentation:
- Model definitions in `models/*.py`
- Usage examples in `docs/tools/*.md`
- Conversation examples in `docs/conversations/*.md`