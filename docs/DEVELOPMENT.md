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

- Setup: `uv pip install -e .` (install with latest changes)
- Install dev deps: `uv pip install black mypy pydantic ruff`
- Format: `uv pip install black && uv run -m black .` 
- Type check: `uv pip install mypy && uv run -m mypy .`
- Lint: `uv pip install ruff && uv run -m ruff check .`
- Fix lint issues: `uv pip install ruff && uv run -m ruff check --fix .`

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
│   ├── applies.py      # Apply-related models
│   ├── assessment_results.py # Assessment results models
│   ├── base.py         # Base model classes and shared types
│   ├── cost_estimates.py # Cost estimation models
│   ├── organizations.py # Organization models
│   ├── plans.py        # Plan-related models
│   ├── projects.py     # Project management models
│   ├── runs.py         # Run management models
│   └── workspaces.py   # Workspace management models
├── tools/              # Tool implementations exposed via MCP
│   ├── __init__.py
│   ├── account.py      # Account management tools
│   ├── applies.py      # Apply management tools
│   ├── assessment_results.py # Assessment results tools
│   ├── cost_estimates.py # Cost estimation tools
│   ├── organizations.py # Organization management tools
│   ├── plans.py        # Plan management tools
│   ├── projects.py     # Project management tools
│   ├── runs.py         # Run management tools
│   └── workspaces.py   # Workspace management tools
├── utils/              # Shared utilities
│   ├── __init__.py
│   ├── decorators.py   # Error handling decorators
│   ├── filters.py      # Response filtering for token optimization
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
- **Audit-safe filtering**: Automatic filtering system uses conservative 5-15% token reduction while preserving 100% audit compliance - all user accountability, security, and change tracking data preserved
- **Async pattern**: All API functions should be async, using httpx
- **Security**: Never log tokens, validate all inputs, redact sensitive data
- **MCP Tool Registration**: Follow minimal pattern in `server.py`:
  - Use simple `mcp.tool()(function_name)` for standard operations
  - Use `mcp.tool(enabled=False)(function_name)` for dangerous delete operations

## Pydantic Model Standards

### Pattern Principles
- **Validation First**: Use Pydantic to validate all input parameters
- **Explicit Aliases**: Use field aliases for API compatibility (`kebab-case` to `snake_case`)
- **Base Models**: Extend from common base classes
- **No Response Models**: Use `APIResponse` type alias (`Dict[str, Any]`) for responses

### Model Structure

1. **Base Classes**:
   See the base classes defined in `terraform_cloud_mcp/models/base.py`:
   - `BaseModelConfig` - Core configuration for all models
   - `APIRequest` - Base class for all API requests
   - `APIResponse` type alias

2. **Request Models**:
   For examples of request models with field aliases, see:
   - `VcsRepoConfig` in `terraform_cloud_mcp/models/workspaces.py`
   - `WorkspaceCreateRequest` in `terraform_cloud_mcp/models/workspaces.py`
   - `WorkspaceListRequest` in `terraform_cloud_mcp/models/workspaces.py`

3. **Enum Classes**:
   For enum implementation examples, see:
   - `ExecutionMode` in `terraform_cloud_mcp/models/base.py`
   - Status enums in `terraform_cloud_mcp/models/runs.py`

### Implementation Pattern

1. **Tool Implementation**:
   See the implementation pattern in `terraform_cloud_mcp/tools/workspaces.py`:
   - `create_workspace` function for a complete implementation example
   - `update_workspace` function for updating existing resources
   - `list_workspaces` function for listing resources with pagination
   - Other CRUD operations in workspace management tools

### Pydantic Best Practices

1. **Use Field Aliases** for API compatibility:
   See the `execution_mode` field in `terraform_cloud_mcp/models/workspaces.py` (class `BaseWorkspaceRequest`)

2. **Use Field Validators** for constraints:
   See the `page_size` field in `terraform_cloud_mcp/models/workspaces.py` (class `WorkspaceListRequest`) 

3. **Use Description** for clarity:
   See the `description` field in `terraform_cloud_mcp/models/workspaces.py` (class `BaseWorkspaceRequest`)

4. **Use Enums** for constrained choices:
   See `ExecutionMode` enum in `terraform_cloud_mcp/models/base.py`

5. **Parameter Inheritance** for common parameters:
   See the class hierarchy in `terraform_cloud_mcp/models/workspaces.py`:
   - `BaseWorkspaceRequest` defines common fields
   - `WorkspaceCreateRequest` extends it with required fields
   - `WorkspaceUpdateRequest` adds routing fields
   - `WorkspaceParams` provides a parameter object without routing fields

## Utility Functions

### JSON:API Payload Utilities
To ensure consistent handling of API payloads, use the utility functions from `terraform_cloud_mcp/utils/payload.py`:

1. **create_api_payload**:
   See implementation in `terraform_cloud_mcp/utils/payload.py` and example usage in `create_workspace` function in `terraform_cloud_mcp/tools/workspaces.py`

2. **add_relationship**:
   See implementation in `terraform_cloud_mcp/utils/payload.py` and usage examples in `terraform_cloud_mcp/tools/runs.py`

### Request Parameter Utilities
For handling pagination and request parameters, see `terraform_cloud_mcp/utils/request.py` and its usage in list operations like `list_workspaces` in `terraform_cloud_mcp/tools/workspaces.py`

## Documentation Standards

### Documentation Principles
- **Essential Information**: Focus on what's needed without verbosity
- **Completeness**: Provide enough context to understand usage
- **External References**: Move examples to dedicated documentation files
- **Agent-Friendly**: Include sufficient context for AI agents/LLMs

### Model Classes

See `VcsRepoConfig` class in `terraform_cloud_mcp/models/workspaces.py` for proper model documentation

For derived classes that inherit from a base class, see `WorkspaceCreateRequest` in `terraform_cloud_mcp/models/workspaces.py` as an example of how to document inheritance

### Tool Functions

See `create_workspace` function in `terraform_cloud_mcp/tools/workspaces.py` for proper tool function documentation including:
- Purpose description
- API endpoint reference
- Parameter documentation
- Return value description
- External documentation references

### Utility Functions

See utility functions in `terraform_cloud_mcp/utils/payload.py` and `terraform_cloud_mcp/utils/request.py` for examples of properly documented helper functions

### Documentation Structure

Documentation is organized in dedicated markdown files:

```
docs/
  models/             # Documentation for Pydantic models
    account.md
    apply.md
    assessment_result.md
    cost_estimate.md
    organization.md
    plan.md
    project.md
    run.md
    workspace.md
  tools/              # Reference documentation for MCP tools
    account.md
    apply.md
    assessment_results.md
    cost_estimate.md
    organization.md
    plan.md
    project.md
    run.md
    workspace.md
  conversations/      # Example conversations using the tools
    account.md
    apply-management-conversation.md
    assessment-results-conversation.md
    cost-estimate-conversation.md
    organization-entitlements-conversation.md
    organizations-management-conversation.md
    plan-management-conversation.md
    project-management-conversation.md
    runs-management-conversation.md
    workspace-management-conversation.md
```

#### Tool Documentation Format

Each tool documentation file should follow this structure:

```markdown
# Module Name Tools

Brief introduction about the module's purpose.

## Overview

Detailed explanation of the functionality and concepts.

## API Reference

Links to relevant Terraform Cloud API documentation:
- [API Section 1](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/section)
- [API Section 2](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/section)

## Tools Reference

### function_name

**Function:** `function_name(param1: type, param2: type) -> ReturnType`

**Description:** Explanation of what the function does.

**Parameters:**
- `param1` (type): Parameter description
- `param2` (type): Parameter description

**Returns:** Description of return value structure

**Notes:**
- Important usage information
- Related functionality
- Permissions required

**Common Error Scenarios:**

| Error | Cause | Solution |
|-------|-------|----------|
| 404   | Resource not found | Verify ID and permissions |
| 422   | Invalid parameters | Ensure values match required format |
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

## Quality Assurance Protocol

### Mandatory Quality Check Sequence

After ANY code changes, run these commands in exact order:

1. **`uv run -m ruff check --fix .`** - Fix linting issues automatically
2. **`uv run -m black .`** - Format code consistently  
3. **`uv run -m mypy .`** - Verify type safety
4. **Manual Testing** - Test basic tool functionality (see methodology below)
5. **Documentation Completeness** - Verify using checklist below

**IMPORTANT**: Fix all issues at each step before proceeding to the next step.

### Manual Testing Methodology

For each new tool, test these scenarios in order:

1. **Happy Path**: Test with valid, typical parameters
2. **Edge Cases**: Test with boundary values, empty strings, None values  
3. **Error Cases**: Test with invalid IDs, missing permissions, malformed data
4. **Integration**: Test with related tools in realistic workflows

### Documentation Completeness Checklist

- [ ] Function docstring includes API endpoint reference
- [ ] Parameter descriptions include formats and constraints
- [ ] Return value description explains structure and key fields
- [ ] docs/tools/ entry created with function signature and examples
- [ ] docs/models/ entry created if new models added
- [ ] docs/conversations/ updated with realistic usage scenario
- [ ] Cross-references between all documentation layers verified
- [ ] All links in documentation are valid and accessible

### Quality Standards

- **Code Coverage**: All new functions must have comprehensive docstrings
- **Type Safety**: All parameters and return values must have type hints
- **Error Handling**: All tools must use @handle_api_errors decorator
- **Security**: No tokens or sensitive data in logs or error messages
- **Consistency**: New code must follow established patterns in existing codebase

## Enhanced Code Style Guidelines

### Core Principles
- **KISS Principle**: Keep It Simple, Stupid. Favor simple, maintainable solutions over complex ones.
- **DRY Principle**: Don't Repeat Yourself. Use utility functions for common patterns.
- **Imports**: stdlib → third-party → local, alphabetically within groups
- **Formatting**: Black, 100 char line limit
- **Types**: Type hints everywhere, Pydantic models for validation
- **Naming**: snake_case (functions/vars), PascalCase (classes), UPPER_CASE (constants)
- **Error handling**: Use `handle_api_errors` decorator from `terraform_cloud_mcp/utils/decorators.py`
- **Async pattern**: All API functions should be async, using httpx
- **Security**: Never log tokens, validate all inputs, redact sensitive data

### Pydantic Patterns
See `terraform_cloud_mcp/models/workspaces.py` for reference implementation:
- Use `BaseModelConfig` base class for common configuration
- Use `APIRequest` for request validation
- Define explicit model classes for parameter objects (e.g., `WorkspaceParams`)
- Use `params` parameter instead of `**kwargs` in tool functions
- Use explicit field aliases (e.g., `alias="kebab-case-name"`) for API field mapping
- Type API responses as `APIResponse` (alias for `Dict[str, Any]`)

### Utility Functions
Use common utilities for repetitive patterns:
- `create_api_payload()` from `utils/payload.py` for JSON:API payload creation
- `add_relationship()` from `utils/payload.py` for relationship management
- `query_params()` from `utils/request.py` for converting model to API parameters

### API Response Handling
- Handle 204 No Content responses properly, returning `{"status": "success", "status_code": 204}`
- Implement custom redirect handling for pre-signed URLs
- Use proper error handling for JSON parsing failures

### Documentation Standards
- Docstrings with Args/Returns for all functions
- Reference specific code implementations in docs rather than code snippets
- See cost_estimates.py for latest documentation patterns

### Comments Guidelines
Follow KISS principles for comments:
- Only explain the non-obvious "why" behind code choices, not the "what"
- Add comments for complex logic, edge cases, security measures, or API-specific requirements
- Avoid redundant, unnecessary, or self-explanatory comments
- Keep comments concise and directly relevant

## Contributing

For details on how to extend the server, contribute code, and the release process, see our [Contributing Guide](CONTRIBUTING.md).