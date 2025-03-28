# Terraform Cloud MCP Development Guide

This document outlines the development guidelines, code standards, and best practices for the Terraform Cloud MCP project.

## Getting Started

### Development Setup

```bash
# Clone the repository
git clone https://github.com/severity1/terraform-cloud-mcp.git
cd terraform-cloud-mcp

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install in development mode (editable)
uv pip install -e .

# Install development dependencies
uv pip install black mypy pydantic ruff
```

### Build & Run Commands

- Setup: `uv pip install -e .`
- Install dev deps: `uv pip install black mypy pydantic ruff`
- Run server: `uv run terraform_cloud_mcp/server.py` (use `TFC_TOKEN=token` or `.env`)
- MCP tools: `mcp dev terraform_cloud_mcp/server.py` (includes debugging interface)
- Debug: `TFC_TOKEN=token uv run -m pdb terraform_cloud_mcp/server.py`
- Tests: `uv run -m unittest discover tests`
- Single test: `uv run -m unittest tests.test_module.TestClass.test_method`
- Format: `uv run -m black .` 
- Type check: `uv run -m mypy .`
- Lint: `uv run -m ruff check .`
- Fix lint issues: `uv run -m ruff check --fix .`

### Development With Claude Integrations

#### Adding to Claude Code (Development Mode)

```bash
# Add to Claude Code with your development path and token
claude mcp add -e TFC_TOKEN=YOUR_TF_TOKEN -s user terraform-cloud-mcp -- "$(pwd)/terraform_cloud_mcp/server.py"
```

#### Adding to Claude Desktop (Development Mode)

Create a `claude_desktop_config.json` configuration file:
- mac: ~/Library/Application Support/Claude/claude_desktop_config.json
- win: %APPDATA%\Claude\claude_desktop_config.json

```json
{
  "mcpServers": {
    "terraform-cloud-mcp": {
      "command": "/path/to/uv", # Get this by running: `which uv`
      "args": [
        "--directory",
        "/path/to/your/terraform-cloud-mcp", # Full path to this project
        "run",
        "terraform_cloud_mcp/server.py"
      ],
      "env": {
        "TFC_TOKEN": "your_terraform_cloud_token" # Your actual TF Cloud token
      }
    }
  }
}
```

## Core Principles

- **KISS (Keep It Simple, Stupid)**: Favor simple, maintainable solutions over complex ones
- **DRY (Don't Repeat Yourself)**: Use utility functions for common patterns
- **Consistency**: Follow established patterns throughout the codebase
- **Type Safety**: Use proper typing and validation everywhere
- **Documentation**: All code should be well-documented with standardized formats
- **Testability**: Write code that can be easily tested
- **Modularity**: Keep components focused and decoupled

## Code Organization

```
terraform_cloud_mcp/
├── api/                # API client and core request handling
│   ├── __init__.py
│   └── client.py       # Core API client with error handling
├── models/             # Pydantic data models for validation
│   ├── __init__.py
│   ├── account.py      # Account-related models
│   ├── base.py         # Base model classes and shared types
│   ├── organizations.py # Organization models
│   ├── runs.py         # Run management models
│   └── workspaces.py   # Workspace management models
├── tools/              # Tool implementations exposed via MCP
│   ├── __init__.py
│   ├── account.py      # Account management tools
│   ├── organizations.py # Organization management tools
│   ├── runs.py         # Run management tools
│   └── workspaces.py   # Workspace management tools
├── utils/              # Shared utilities
│   ├── __init__.py
│   ├── decorators.py   # Error handling decorators
│   ├── payload.py      # JSON:API payload utilities
│   └── request.py      # Request parameter utilities
└── server.py           # MCP server entry point
```

## Code Style Guidelines

### General Guidelines

- **Imports**: stdlib → third-party → local, alphabetically within groups
- **Formatting**: Black, 100 char line limit
- **Types**: Type hints everywhere, Pydantic models for validation
- **Naming**: snake_case (functions/vars), PascalCase (classes), UPPER_CASE (constants)
- **Error handling**: Use `handle_api_errors` decorator from `terraform_cloud_mcp/utils/decorators.py`
- **Async pattern**: All API functions should be async, using httpx
- **Security**: Never log tokens, validate all inputs, redact sensitive data

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

### Pydantic Best Practices

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

## Documentation Standards

### Documentation Principles
- **Essential Information**: Focus on what's needed without verbosity
- **Completeness**: Provide enough context to understand usage
- **External References**: Move examples to dedicated documentation files
- **Agent-Friendly**: Include sufficient context for AI agents/LLMs

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

## Contributing

For details on how to extend the server, contribute code, and the release process, see our [Contributing Guide](CONTRIBUTING.md).