# CLAUDE.md for tools/

This file provides guidance for MCP tool implementations that expose Terraform Cloud API functionality to AI assistants.

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

## Implementation Requirements

### Essential Patterns
1. Use @handle_api_errors decorator for consistent error handling
2. Create corresponding Pydantic models for validation
3. Follow function signature pattern: (routing_params, optional_params, params_object)
4. Use utility functions for payload creation and parameter handling
5. Document thoroughly with API endpoint references
6. Register appropriately in server.py based on destructiveness

### Documentation Integration
- Reference [docs/API_REFERENCES.md](../../docs/API_REFERENCES.md) for official API groupings
- Create usage examples in docs/tools/
- Link to model definitions and conversation examples

## Development Integration

### Standards Reference
Complete development guidance is in [docs/DEVELOPMENT.md](../../docs/DEVELOPMENT.md):
- **Build Commands**: Quality check sequences and environment setup
- **Quality Protocols**: 5-step mandatory validation process  
- **Code Style**: Function patterns, async implementation, and validation requirements

### Tool-Specific Requirements
- Use @handle_api_errors decorator for all API functions
- Follow (routing_params, optional_params, params_object) signature pattern
- Apply comprehensive testing: Happy path → Edge cases → Error cases → Integration
- Use Pydantic models for validation (see [../models/CLAUDE.md](../models/CLAUDE.md))

## Component Cross-References

### Related Component Guidance
- **Model Development**: [../models/CLAUDE.md](../models/CLAUDE.md) for Pydantic model patterns and validation
- **Utility Functions**: [../utils/CLAUDE.md](../utils/CLAUDE.md) for error handling and payload utilities  
- **API Client**: [../api/CLAUDE.md](../api/CLAUDE.md) for API request patterns
- **Documentation**: [../../docs/CLAUDE.md](../../docs/CLAUDE.md) for documentation framework