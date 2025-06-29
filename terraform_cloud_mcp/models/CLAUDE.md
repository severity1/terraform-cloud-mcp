# CLAUDE.md for models/

This file provides guidance about the Pydantic data models for Terraform Cloud API request validation.

## Model Architecture

The models directory provides request validation through Pydantic models with:
- **Input validation**: API request parameter validation and type safety
- **Field mapping**: Aliases for kebab-case to snake_case API compatibility
- **Response typing**: All responses typed as `APIResponse = Dict[str, Any]` (not validated)

### Core Components
- **base.py**: `APIRequest` base class, `BaseModelConfig`, and `APIResponse` type alias
- **Domain modules**: Account, workspaces, runs, plans, applies, organizations, projects, cost estimates, assessment results

### Model Categories
- **Request models**: Validate API request parameters with field aliases
- **Parameter models**: Flexible configuration objects for operations with >3 optional parameters  
- **Enums**: Constrained choices based on API documentation

## Implementation Standards

### Model Patterns
- **Request models**: Extend `APIRequest`, use field aliases for kebab-case mapping
- **Parameter models**: Create `*Params` objects for operations with >3 optional parameters
- **Base models**: Create `Base*Request` when ≥3 operations share >50% of fields
- **Enums**: Use for fields with API-documented constrained choices

### Field Standards
- **Required**: `Field(...)` with no default (follows API documentation)
- **Optional**: `Optional[Type]` with appropriate default values
- **Aliases**: Always use `alias="kebab-case-name"` for API compatibility
- **Validation**: Apply Field constraints when API docs specify limits

## Decision Criteria

### Model Creation Rules
- **BaseRequest**: When ≥3 operations share >50% of fields
- **Params objects**: When function has >3 optional configuration parameters  
- **Separate Create/Update**: When models differ by >2 fields or validation rules
- **Enums**: When API docs specify constrained values (not examples)

### Field Validation Rules
- **Validation constraints**: Apply when API docs specify limits (length, range, format)
- **Default values**: Use API defaults; None only when field truly optional in API
- **Required vs Optional**: Follow API documentation exactly
- **Field organization**: Group by domain, clear inheritance with APIRequest

## Development Integration

### Standards Reference
Complete development guidance is in [docs/DEVELOPMENT.md](../../docs/DEVELOPMENT.md):
- **Pydantic Patterns**: `APIRequest` base class, field aliases, parameter objects
- **Quality Standards**: Type hints, Field constraints, validation rules
- **Development Cycle**: Pattern implementation → API validation → Quality checks → Alias mapping

### Model-Specific Requirements
- All fields must have proper type hints and API-based validation
- Use `BaseModelConfig` and `APIRequest` for consistency
- Document all field aliases and constraint reasoning
- Apply 5-step quality check sequence after model changes

## Component Cross-References

### Related Component Guidance
- **Tool Implementation**: [../tools/CLAUDE.md](../tools/CLAUDE.md) for using models in tool functions
- **Utility Functions**: [../utils/CLAUDE.md](../utils/CLAUDE.md) for payload creation and parameter handling
- **API Client**: [../api/CLAUDE.md](../api/CLAUDE.md) for API request integration
- **Documentation**: [../../docs/CLAUDE.md](../../docs/CLAUDE.md) for model documentation standards