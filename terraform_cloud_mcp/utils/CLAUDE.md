# CLAUDE.md for utils/

This file provides guidance about shared utility functions for consistent operations across the Terraform Cloud MCP implementation.

## Context Activation
This guidance activates when:
- Working in `terraform_cloud_mcp/utils/` directory
- Creating/editing utility functions (*.py)
- Implementing shared functionality (decorators, helpers, formatters)
- Adding error handling or payload creation utilities

**Companion directories**: tools/ (for usage), models/ (for integration), api/ (for requests)

## Utility Architecture

The utils directory provides common functionality to maintain consistency and reduce code duplication:

### Core Utilities
- **decorators.py**: `handle_api_errors` decorator for consistent error handling
- **env.py**: Centralized environment variable management (tokens, feature flags)
- **payload.py**: JSON:API payload creation and relationship management
- **request.py**: Query parameter transformation for API requests
- **filters.py**: Response filtering system for token optimization

## Implementation Standards

### Error Handling Pattern
- **@handle_api_errors decorator**: Apply to all API functions for consistent error formatting
- **Error format**: `{"error": "message"}` (never expose sensitive data)
- **Success preservation**: Decorator preserves successful responses without modification

### Environment Management
- **get_tfc_token()**: Centralized TFC_TOKEN access (never use direct os.getenv)
- **should_enable_delete_tools()**: Safety control for destructive operations
- **Centralized access**: All environment variables managed through utils/env.py

### Payload Creation
- **create_api_payload()**: JSON:API compliant payload creation from Pydantic models
- **add_relationship()**: Standardized relationship management for JSON:API
- **query_params()**: Pydantic model to API parameter transformation for list/filter operations

### Query Parameter Transformation
The `query_params()` function transforms Pydantic model fields to API parameters using consistent naming conventions:
- **Pagination**: `page_number` → `page[number]`, `page_size` → `page[size]`
- **Filters**: `filter_name` → `filter[name]`, `filter_permissions_update` → `filter[permissions][update]`
- **Search**: `search_term` → `search[term]`, `search_user` → `search[user]`
- **Query**: `query_email` → `q[email]`, `query_name` → `q[name]`
- **Direct params**: `q`, `search`, `sort` mapped directly

Usage pattern for all list operations: See `../tools/workspaces.py:list_workspaces` for the standard query parameter transformation approach.

### Parameter Model Integration

Functions use direct parameters with optional params objects. See `../tools/variables.py:create_workspace_variable` for the pattern of combining direct and optional parameters with request models.

## Usage Standards

### Core Requirements
- **Error handling**: Always use `@handle_api_errors` for API functions (never duplicate logic)
- **Environment access**: Use utility functions instead of direct `os.getenv()` calls
- **Payload creation**: Use `create_api_payload()` and `add_relationship()` for JSON:API operations
- **Parameter handling**: Use `query_params()` for all list/filter operations
- **Response filtering**: Review filter configurations when implementing new tools - check for new fields to filter

### Validated Audit-Safe Filtering System
**✅ FULLY TESTED AND VERIFIED**: All 7 tool categories validated for 100% audit compliance:
- **User accountability**: `created-at`, `updated-at`, `version-id` always preserved
- **Security configuration**: All permission and auth fields preserved  
- **Change tracking**: Status timestamps, source tracking, version data preserved
- **Operational context**: Status, timing, progress data for monitoring tools
- **Decision context**: Cost data, assessments, diagnostics for analysis tools
- **Conservative 5-15% token reduction**: Balanced optimization vs. complete audit capability
- **Audit-first principle**: When in doubt, preserve the field rather than filter it

### Development Guidelines
- **New utilities**: Place in appropriate module, document with type hints and examples
- **Consistency**: Maintain established patterns, consistent return types and error formats
- **Reusability**: Write utilities to be domain-agnostic and broadly applicable

## Error Handling Decision Matrix

### When to Use Decorator Only
- Standard CRUD operations with predictable API responses (200, 201, 204, 4xx, 5xx)
- Most list and get operations without complex parameter validation
- Tools that don't require business logic validation before API calls

### When to Add Custom Logic (WITH Decorator)
- Parameter validation requiring specific error messages beyond Pydantic
- API responses needing special status code interpretation
- Multi-step operations with intermediate error handling needs
- File operations requiring size/format validation

### Error Response Standards
- **Format**: `{"error": "descriptive message"}` (never expose sensitive data)
- **Success**: 200/201 return raw API response; 204 returns `{"status": "success", "status_code": 204}`
- **Consistency**: Always preserve @handle_api_errors decorator even with custom logic

## Development Standards

### Quality Checks
- **Format**: `ruff format .`
- **Lint**: `ruff check .`
- **Type Check**: `mypy .`
- **Test**: `pytest`

### Utility-Specific Requirements
- All functions must include proper error handling and consistent response format
- Apply security guidelines for sensitive data redaction
- Follow established patterns for error decoration and type safety
- Test with comprehensive quality check sequence after utility changes

### Code Style Requirements
- Type hints required for all parameters and return values
- Apply async patterns where appropriate
- Follow security practices for sensitive data handling
- Maintain consistent naming conventions

## Integration Guidelines

### Tool Integration
When utilities are used in tools:
- Apply `@handle_api_errors` decorator to all API functions
- Use `create_api_payload()` for JSON:API compliant requests
- Apply `query_params()` for all list/filter operations
- Use centralized environment variable access

### Model Integration
When utilities work with models:
- Use `create_api_payload()` with Pydantic model instances
- Apply `query_params()` for transforming model data to API parameters
- Handle model validation errors appropriately
- Ensure proper type safety throughout

### API Client Integration
When utilities work with API client:
- Use utilities for consistent request formatting
- Apply error handling decorators
- Use centralized token management
- Ensure proper response handling

## Implementation Workflow

### New Utility Development Process
1. **Define function signature**: Include proper type hints
2. **Implement core logic**: Follow established patterns
3. **Add error handling**: Apply consistent response formats
4. **Test thoroughly**: Cover success, error, and edge cases
5. **Document function**: Include usage examples and cross-references
6. **Update status**: Implementation tracking

### Quality Validation Checklist
For each utility implementation:
- [ ] Function includes proper error handling and consistent response format
- [ ] Type hints provided for all parameters and return values
- [ ] Documentation includes usage examples and patterns
- [ ] Security guidelines followed for sensitive data handling
- [ ] Quality checks passed: format, lint, type check
- [ ] Tests cover all scenarios: success, error, edge cases