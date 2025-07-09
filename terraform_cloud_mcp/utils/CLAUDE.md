# CLAUDE.md for utils/

This file provides guidance about shared utility functions for consistent operations across the Terraform Cloud MCP implementation.

## Utility Architecture

The utils directory provides common functionality to maintain consistency and reduce code duplication:

### Core Utilities
- **decorators.py**: `handle_api_errors` decorator for consistent error handling
- **env.py**: Centralized environment variable management (tokens, feature flags)
- **payload.py**: JSON:API payload creation and relationship management
- **request.py**: Query parameter transformation for API requests

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
- **query_params()**: Pydantic model to API parameter transformation

## Usage Standards

### Core Requirements
- **Error handling**: Always use `@handle_api_errors` for API functions (never duplicate logic)
- **Environment access**: Use utility functions instead of direct `os.getenv()` calls
- **Payload creation**: Use `create_api_payload()` and `add_relationship()` for JSON:API operations
- **Parameter handling**: Use `query_params()` for all list/filter operations

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

## Development Integration

### Standards Reference
Complete development guidance is in [docs/DEVELOPMENT.md](../../docs/DEVELOPMENT.md):
- **Quality Protocol**: Error handling standards and 5-step validation sequence
- **Build Commands**: Development workflow and testing requirements
- **Code Style**: Type hints, async patterns, naming conventions, security practices

### Utility-Specific Requirements
- All functions must include proper error handling and consistent response format
- Apply security guidelines for sensitive data redaction
- Follow established patterns for error decoration and type safety
- Test with mandatory quality check sequence after utility changes

## Component Cross-References

### Related Component Guidance
- **Tool Implementation**: [../tools/CLAUDE.md](../tools/CLAUDE.md) for using utilities in tool functions
- **Model Development**: [../models/CLAUDE.md](../models/CLAUDE.md) for validation patterns that use utilities
- **API Client**: [../api/CLAUDE.md](../api/CLAUDE.md) for API request integration with utilities
- **Documentation**: [../../docs/CLAUDE.md](../../docs/CLAUDE.md) for utility documentation standards