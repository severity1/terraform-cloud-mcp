# CLAUDE.md for utils/

This file provides guidance about the utility functions in this repository.

## Utils Overview

The utils directory contains shared utility functions that handle common operations across the codebase. These utilities help maintain consistency, reduce code duplication, and encapsulate complex operations.

## Key Components

- **decorators.py**: Function decorators for error handling
  - `handle_api_errors`: Decorator for consistent API error handling

- **payload.py**: JSON:API payload utilities
  - `create_api_payload`: Creates JSON:API compliant payloads from Pydantic models
  - `add_relationship`: Adds relationships to JSON:API payloads

- **request.py**: Request parameter utilities
  - `query_params`: Transforms Pydantic models to API query parameters

## Decorator Patterns

```python
@handle_api_errors
async def example_function() -> APIResponse:
    """A function that makes API calls."""
    # Function body
    return result
```

The `handle_api_errors` decorator:
1. Wraps async functions that make API calls
2. Catches exceptions and formats them consistently
3. Returns errors in a standardized format: `{"error": "message"}`
4. Preserves successful responses without modification

## JSON:API Payload Utilities

```python
# Create a payload from a Pydantic model
payload = create_api_payload(
    resource_type="workspaces",
    model=workspace_request,
    exclude_fields={"organization"}  # Fields to exclude
)

# Add a relationship to the payload
payload = add_relationship(
    payload=payload,
    relation_name="organization",
    resource_type="organizations",
    resource_id="my-org"
)
```

## Request Parameter Utilities

```python
# Convert a Pydantic model to API query parameters
params = query_params(request_model)

# Result transforms fields following these patterns:
# - page_number -> page[number]
# - filter_name -> filter[name]
# - search_term -> search[term]
# - query_email -> q[email]
# - q, search, sort -> direct mapping
```

## Usage Guidelines

1. **Error Handling**:
   - Always use `handle_api_errors` for functions that make API calls
   - Never duplicate error handling logic that's in the decorator

2. **JSON:API Payload Creation**:
   - Use `create_api_payload` instead of manual payload construction
   - Use `add_relationship` for all relationship handling

3. **Query Parameter Handling**:
   - Use `query_params` for all list/filter operations
   - Follow the field naming conventions for proper parameter conversion

4. **Adding New Utilities**:
   - Place generic utilities in the appropriate module
   - Document clearly with docstrings and type hints
   - Include example usage in docstring
   - Write utilities to be reusable across domains

5. **Consistency**:
   - Maintain consistent return types and error formats
   - Follow established patterns for new utilities
   - Ensure all utilities have proper type hints