# Terraform Cloud MCP Project Standards

This document outlines the standards and best practices for the Terraform Cloud MCP project. Following these standards ensures consistency, maintainability, and quality across the codebase.

## Core Principles

- **KISS (Keep It Simple, Stupid)**: Favor simple, maintainable solutions over complex ones
- **DRY (Don't Repeat Yourself)**: Use utility functions for common patterns
- **Consistency**: Follow established patterns throughout the codebase
- **Type Safety**: Use proper typing and validation everywhere
- **Documentation**: All code should be well-documented with standardized formats
- **Testability**: Write code that can be easily tested
- **Modularity**: Keep components focused and decoupled

## Pydantic Model Standards

### Pattern Principles
- **Validation First**: Use Pydantic to validate all input parameters
- **Explicit Aliases**: Use field aliases for API compatibility (`kebab-case` to `snake_case`)
- **Base Models**: Extend from common base classes
- **No Response Models**: Use `APIResponse` type alias (`Dict[str, Any]`) for responses

### Model Structure

1. **Base Classes**:
   ```python
   class BaseModelConfig(BaseModel):
       """Base configuration for all models."""
       model_config = ConfigDict(
           populate_by_name=True,  # Allow both snake_case and kebab-case
           use_enum_values=True,   # Serialize enums to their values
           extra="ignore",         # Ignore extra fields in input
       )

   class APIRequest(BaseModelConfig):
       """Base class for all API requests."""
       pass

   # Type alias for responses - we don't validate responses
   APIResponse = Dict[str, Any]
   ```

2. **Request Models**:
   ```python
   class ExampleRequest(APIRequest):
       """Example request model with field aliases."""
       # Required field with alias for API compatibility
       field_name: str = Field(..., alias="field-name")
       
       # Optional field with default value
       optional_field: Optional[bool] = Field(False, alias="optional-field")
       
       # Field with validator
       validated_field: int = Field(..., ge=1, le=100, alias="validated-field")
   ```

3. **Enum Classes**:
   ```python
   class ExecutionMode(str, Enum):
       """Execution mode options."""
       REMOTE = "remote"
       LOCAL = "local"
       AGENT = "agent"
   ```

### Implementation Pattern

1. **Tool Implementation**:
   ```python
   @handle_api_errors
   async def example_function(
       param1: str, 
       params: Optional[ExampleRequest] = None
   ) -> APIResponse:
       """Example tool function with Pydantic model."""
       # Extract parameters from the params object if provided
       param_dict = params.model_dump(exclude_none=True) if params else {}
       
       # Create request using Pydantic model
       request = ExampleRequest(field_name=param1, **param_dict)
       
       # Create API payload using utility function
       payload = create_api_payload(
           resource_type="resource_type",
           model=request,
           exclude_fields={"field_to_exclude"}
       )
       
       # Add relationship if needed
       add_relationship(
           payload=payload,
           relation_name="related_resource",
           resource_type="related_resources",
           resource_id="resource-id"
       )
       
       # Make API request
       return await api_request("endpoint", method="POST", data=payload)
   ```

### Best Practices

1. **Use Field Aliases** for API compatibility:
   ```python
   field_name: str = Field(..., alias="field-name")
   ```

2. **Use Field Validators** for constraints:
   ```python
   count: int = Field(..., ge=1, le=100)  # Between 1 and 100
   name: str = Field(..., min_length=3)   # At least 3 characters
   ```

3. **Use Description** for clarity:
   ```python
   name: str = Field(..., description="Name of the resource")
   ```

4. **Use Enums** for constrained choices:
   ```python
   mode: ExecutionMode = Field(ExecutionMode.REMOTE)
   ```

5. **Parameter Inheritance** for common parameters:
   ```python
   class BaseWorkspaceRequest(APIRequest):
       """Base class with common workspace parameters."""
       name: Optional[str] = None
       
   class WorkspaceCreateRequest(BaseWorkspaceRequest):
       """Request to create a workspace, inherits common parameters."""
       organization: str  # Required for creation
   ```

## Utility Functions

### JSON:API Payload Utilities
To ensure consistent handling of API payloads, use these utility functions from `terraform_cloud_mcp/utils/payload.py`:

1. **create_api_payload**:
   ```python
   def create_api_payload(
       resource_type: str, 
       model: BaseModel,
       exclude_fields: Optional[Set[str]] = None,
   ) -> Dict[str, Any]:
       """Creates a JSON:API compliant payload from a Pydantic model."""
   ```

2. **add_relationship**:
   ```python
   def add_relationship(
       payload: Dict[str, Any], 
       relation_name: str,
       resource_type: str,
       resource_id: str
   ) -> Dict[str, Any]:
       """Adds a relationship to a JSON:API payload."""
   ```

### Request Parameter Utilities
For handling pagination and request parameters, use utilities from `terraform_cloud_mcp/utils/request.py`:

1. **pagination_params**:
   ```python
   def pagination_params(
       model: PaginationModel,
       search_field: Optional[str] = "search"
   ) -> Dict[str, Any]:
       """Creates pagination parameters from a Pydantic request model."""
   ```

## Docstring Standards

### Documentation Principles
- **Essential Information**: Focus on what's needed without verbosity
- **Completeness**: Provide enough context to understand usage
- **External References**: Move examples to dedicated documentation files
- **Agent-Friendly**: Include sufficient context for AI agents/LLMs

## Code Commenting Standards

The KISS (Keep It Simple, Stupid) principle applies to comments as much as code. Comments should be minimal, precise, and focused only on what's not obvious from the code itself.

### Comment Only When Necessary

Add comments only in these essential situations:

1. **Non-obvious "Why"**: Explain reasoning that isn't evident from reading the code
2. **Complex Logic**: Brief explanation of multi-step transformations or algorithms
3. **Edge Cases**: Why special handling is needed for boundary conditions
4. **Security Considerations**: Rationale for security measures (without exposing vulnerabilities)
5. **API Requirements**: Explanations of why code conforms to specific API requirements

### Avoid Unnecessary Comments

1. **No "What" Comments**: Don't describe what the code does when it's self-evident
2. **No Redundant Information**: Don't repeat documentation that exists in docstrings
3. **No Commented-Out Code**: Delete unused code rather than commenting it out
4. **No Obvious Comments**: Don't state the obvious (e.g., "Increment counter")

### Effective Comment Examples

#### For Complex Transformations
```python
# Transform variables array to required API format with key-value pairs
variables_array = [{"key": var.key, "value": var.value} for var in variables]
```

#### For Error Handling
```python
# Return standardized success response for 204 No Content to ensure consistent interface
if response.status_code == 204:
    return {"status": "success"}
```

#### For Security Measures
```python
# Redact token from error message to prevent credential exposure
error_message = error_message.replace(token, "[REDACTED]")
```

#### For Performance Considerations
```python
# Use exclude_unset to prevent default values from overriding server defaults
request_data = data.model_dump(exclude_unset=True)
```

#### For Utility Usage
```python
# Create API payload using utility function - avoids manual JSON:API structure creation
payload = create_api_payload(
    resource_type="workspaces",
    model=request,
    exclude_fields={"organization", "workspace_name"}  # Fields handled separately
)

# Transform complex filter parameters to API-compatible format
for field in filter_fields:
    # Convert field name from filter_status to filter[status] format required by API
    api_param = f"filter[{field[7:]}]"  # Remove 'filter_' prefix
    params[api_param] = value
```

### Comment Implementation Checklist

When adding or reviewing comments in code:

1. **Ask "Why not What"**: Does the comment explain reasoning rather than just describing the code?
2. **Check for Necessity**: Is this information not obvious from the code itself?
3. **Verify Conciseness**: Is the comment as brief as possible while still being clear?
4. **Avoid Redundancy**: Is this information already available in docstrings?
5. **Check for Value**: Does this comment help a future developer understand the code better?

### Comment Review Process

During code reviews:

1. Flag unnecessarily verbose comments
2. Identify code that needs explanatory comments but doesn't have them
3. Ensure all comments follow the "why not what" principle
4. Check that security-related code has appropriate explanatory comments

### Model Classes

```python
class ExampleModel(BaseModel):
    """Brief description of the model's purpose.
    
    Longer description explaining its role and context.
    
    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/section
    
    Fields:
        field_name: Description of the field (only in base classes)
        
    Note: 
        Any important usage notes or inheritance details.
        
    See: 
        docs/models/model_name_examples.md for usage examples
    """
```

For derived classes, only document new or overridden fields and indicate inheritance:

```python
class DerivedModel(BaseModel):
    """Brief description of the derived model.
    
    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/section
    
    Note:
        This inherits all fields from BaseModel.
        Only new/overridden fields documented here.
        
    See: 
        docs/models/model_name_examples.md for usage examples
    """
```

### Tool Functions

```python
async def example_function(param1: str, param2: int = 0) -> APIResponse:
    """Brief description of what the function does.
    
    Context about WHEN to use this tool and its purpose.
    
    API endpoint: METHOD /path/to/endpoint
    
    Args:
        param1: Brief description of parameter
        param2: Brief description including default value
        params: Optional configuration settings:
            - option1: Description of what this option does
            - option2: Description with possible values
            
    Returns:
        Description of return structure and important fields
        
    See:
        docs/tools/tool_name.md for usage examples
    """
```

### Utility Functions

```python
def helper_function(param: Any) -> ResultType:
    """Brief description of what this helper does.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When error conditions are met
    """
```

### Documentation Structure

Examples should be moved to dedicated markdown files:

```
docs/
  models/
    account_examples.md
    organization_examples.md
    workspace_examples.md
    run_examples.md
  tools/
    account_tools.md
    organization_tools.md
    workspace_tools.md
    run_tools.md
```

### Documentation Best Practices

### General Practices
- Don't duplicate information already in type hints
- Don't include lengthy examples in docstrings (use dedicated documentation files)
- Use "See" references to point to external documentation

### For Model Docstrings
- Always include API documentation reference links
- Document fields in base classes, not derived classes
- Use "Note" section to indicate inheritance relationships
- Don't repeat field descriptions already in Field(..., description="...")

### For Tool Docstrings
- Provide enough context to understand when and why to use the tool
- Document complex parameter objects with one option per line using dashes
- Include API endpoint with correct HTTP method
- Describe return structure with important fields to expect
- Ensure docstrings provide enough context for AI agents/LLMs