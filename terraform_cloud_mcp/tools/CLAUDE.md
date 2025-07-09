# CLAUDE.md for tools/

This file provides guidance for MCP tool implementations that expose Terraform Cloud API functionality to AI assistants.

## Context Activation
This guidance activates when:
- Working in `terraform_cloud_mcp/tools/` directory
- Reading/editing tool implementation files (*.py)
- Implementing MCP functions for Terraform Cloud API
- Adding new tool domains or expanding existing tools

**Companion directories**: models/ (for validation), utils/ (for utilities), api/ (for client)

## Tool Architecture

### Directory Structure
- **__init__.py**: Tool registration and imports
- **Domain modules**: Account, workspaces, runs, plans, applies, organizations, projects, cost estimates, assessment results

### Implementation Standards
- **Consistent patterns**: All tools follow standardized implementation patterns
- **Error handling**: Use @handle_api_errors decorator for consistent error management
- **Async patterns**: All API functions are async using httpx
- **Parameter validation**: Use Pydantic models for input validation

## Tool Organization

### Operation Categories
- **CRUD**: create_*, get_*, update_*, delete_* operations
- **List**: list_* operations with filtering and pagination
- **Actions**: lock_*, unlock_*, apply_*, cancel_* state changes
- **Specialized**: Domain-specific operations

### File Organization Rules
- **Add to existing**: Tool fits domain and file has < 15 functions
- **Create new file**: New domain OR existing file ≥ 15 functions  
- **Split file**: When file exceeds 20 functions, split by logical sub-domains
- **Domain boundaries**: Create new domain for ≥ 5 conceptually distinct tools
- **Naming**: Use singular form matching API domain (e.g., workspace.py)

### Registration Classification
- **Non-destructive**: get_*, list_*, create_*, update_* (basic registration)
- **Destructive**: delete_*, force_*, *_unlock affecting running processes (conditional)
- **Potentially destructive**: cancel_*, discard_* operations (case-by-case)

## Decision Matrices

### When to Create New File vs Add to Existing
| Scenario | New File | Add to Existing |
|----------|----------|-----------------|
| New API domain (≥5 conceptually distinct tools) | ✅ | ❌ |
| Existing file has ≥15 functions | ✅ | ❌ |
| Tool fits existing domain + file <15 functions | ❌ | ✅ |
| Existing file will exceed 20 functions | ✅ Split by sub-domains | ❌ |

### Tool Registration Decision Matrix
| Operation Type | Examples | Registration | Reason |
|----------------|----------|-------------|---------|
| Non-destructive | get_*, list_*, create_*, update_* | Basic | Safe operations |
| Destructive | delete_*, force_*, *_unlock | Conditional | Affects running processes |
| Potentially destructive | cancel_*, discard_* | Case-by-case | Context-dependent impact |

### Function Signature Pattern Decision
| Parameter Count | Structure | Example |
|-----------------|-----------|---------|
| 1-2 required | Direct parameters | `get_workspace(workspace_id)` |
| 3+ required | Routing + individual + params | `create_workspace(org, name, params)` |
| 5+ optional | Use params object | `update_workspace(org, name, params)` |
| <5 optional | Direct parameters | `list_workspaces(org, search, page)` |

## Implementation Requirements

### Essential Patterns
1. Use @handle_api_errors decorator for consistent error handling
2. Create corresponding Pydantic models for validation
3. Follow function signature pattern: (required_routing_params, optional_individual_params, optional_params_object)
4. Use utility functions for payload creation and parameter handling:
   - `create_api_payload()` for JSON:API compliant payload creation
   - `query_params()` for transforming Pydantic models to API parameters
5. Document thoroughly with API endpoint references
6. Register appropriately in server.py based on destructiveness

### Function Signature Patterns

Tool functions follow a consistent parameter structure. See `variables.py:create_workspace_variable` for the standard pattern.

**Parameter Order:**
1. **Required routing parameters** (workspace_id, organization, etc.)
2. **Required API parameters** (key, category, name, etc.)  
3. **Optional params object** for additional configuration

### Query Parameter Pattern
For list operations with filtering/pagination, use `query_params()` utility. See `workspaces.py:list_workspaces` for the standard pattern of transforming request models to API parameters.

### Documentation Integration
- Reference API_REFERENCES.md for official API groupings
- Create usage examples in docs/tools/
- Link to model definitions and conversation examples

## Development Standards

### Quality Checks
- **Format**: `ruff format .`
- **Lint**: `ruff check .`
- **Type Check**: `mypy .`
- **Test**: `pytest`

### Code Style Requirements
- Use @handle_api_errors decorator for all API functions
- Follow (required_routing_params, optional_individual_params, optional_params_object) signature pattern
- Apply async patterns with httpx for all API calls
- Use Pydantic models for input validation
- Apply comprehensive testing: Happy path → Edge cases → Error cases → Integration

### Model Integration
When working with models:
- Create corresponding Pydantic models for all tool parameters
- Use model validation for input parameters
- Follow field naming conventions (snake_case for Python, kebab-case for API)
- Apply proper type hints and validation rules

### Utility Function Usage
Essential utility functions for tool implementation:
- `create_api_payload()`: For JSON:API compliant payload creation
- `query_params()`: For transforming Pydantic models to API parameters
- `@handle_api_errors`: Decorator for consistent error handling
- Request helpers: Authentication, pagination, filtering

## Implementation Workflow

### New Tool Development Process
1. **Define function signature**: Follow parameter order pattern
2. **Create Pydantic models**: For validation and type safety
3. **Implement core logic**: Using utility functions and decorators
4. **Add error handling**: Apply @handle_api_errors decorator
5. **Register in server.py**: Based on destructiveness classification
6. **Test thoroughly**: Cover happy path, edge cases, and error conditions
7. **Update documentation**: TASKS.md, API_REFERENCES.md status updates

### Quality Validation Checklist
For each tool implementation:
- [ ] Function follows Essential Patterns (decorator, models, utilities)
- [ ] Pydantic models created and validated
- [ ] Tool registered in server.py with appropriate classification
- [ ] Quality checks passed: format, lint, type check
- [ ] Documentation updated: implementation status tracking
- [ ] Tests cover all scenarios: success, edge cases, errors