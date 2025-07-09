# CLAUDE.md for models/

This file provides guidance about the Pydantic data models for Terraform Cloud API request validation.

## Context Activation
This guidance activates when:
- Working in `terraform_cloud_mcp/models/` directory
- Creating/editing Pydantic model files (*.py)
- Implementing request validation models
- Adding field validation or model hierarchies

**Companion directories**: tools/ (for usage), utils/ (for integration), api/ (for requests)

## Model Architecture

The models directory provides request validation through Pydantic models with:
- **Input validation**: API request parameter validation and type safety
- **Field mapping**: Aliases for kebab-case to snake_case API compatibility
- **Response typing**: All responses typed as `APIResponse = Dict[str, Any]` (not validated)

### Core Components
- **base.py**: `APIRequest` base class, `BaseModelConfig`, and `APIResponse` type alias
- **Domain modules**: Account, workspaces, runs, plans, applies, organizations, projects, cost estimates, assessment results

### Model Categories
- **Request models**: Validate API request parameters with field aliases and direct parameter fields
- **Parameter models**: Simplified configuration objects used only for operations with complex parameter sets
- **Enums**: Constrained choices based on API documentation

## Implementation Standards

### Model Patterns
- **Request models**: Extend `APIRequest`, include required fields directly and optional fields as individual parameters
- **Parameter models**: Create `*Params` objects only when operations have complex parameter sets requiring separation
- **Direct parameter approach**: Most models now include optional fields directly rather than nested in `params` objects
- **Base models**: Create `Base*Request` when ≥3 operations share >50% of fields
- **Enums**: Use for fields with API-documented constrained choices

### Implementation Approach
Request models include all parameters directly. See `variables.py:WorkspaceVariableCreateRequest` for the direct parameter pattern where optional fields are included in the model rather than nested in params objects.

### Field Standards
- **Required**: `Field(...)` with no default (follows API documentation)
- **Optional**: `Optional[Type]` with appropriate default values
- **Aliases**: Always use `alias="kebab-case-name"` for API compatibility
- **Validation**: Apply Field constraints when API docs specify limits

## Decision Criteria

### Model Creation Rules
- **BaseRequest**: When ≥3 operations share >50% of fields
- **Params objects**: Use sparingly - only when parameter sets are complex and need separation from routing parameters
- **Direct parameters**: Prefer including optional fields directly in request models rather than nested params
- **Separate Create/Update**: When models differ by >2 fields or validation rules
- **Enums**: When API docs specify constrained values (not examples)

## Decision Matrices

### Model Structure Decision Matrix
| Scenario | Base Model | Separate Models | Direct Parameters |
|----------|------------|-----------------|-------------------|
| ≥3 operations share >50% fields | ✅ | ❌ | ❌ |
| Operations differ by >2 fields | ❌ | ✅ | ❌ |
| <5 optional parameters | ❌ | ❌ | ✅ |
| Complex parameter validation needed | ❌ | Use params object | ❌ |

### Validation Strategy Decision Matrix
| Field Type | Validation Approach | Example |
|------------|---------------------|---------|
| API-documented constraints | Apply Field constraints | `maxLength=128` |
| Optional with API default | Use API default value | `default="latest"` |
| Truly optional in API | Use `None` default | `default=None` |
| Constrained choices in API docs | Create Enum | `ExecutionMode` |

### Parameter Object vs Direct Fields
| Criteria | Use Params Object | Use Direct Fields |
|----------|-------------------|-------------------|
| >5 optional parameters | ✅ | ❌ |
| Complex validation rules | ✅ | ❌ |
| Reuse across operations | ✅ | ❌ |
| Simple operation-specific | ❌ | ✅ |

### When to Use Params Objects vs Direct Parameters
**Use Params Objects When:**
- Tool function has >5 optional parameters requiring complex validation
- Parameters need reuse across multiple similar operations
- Separation of concerns between routing and configuration parameters is critical

**Use Direct Parameters When (Preferred):**
- Model has <5 optional parameters
- Parameters are operation-specific
- Simpler model structure improves maintainability

### Field Validation Rules
- **Validation constraints**: Apply when API docs specify limits (length, range, format)
- **Default values**: Use API defaults; None only when field truly optional in API
- **Required vs Optional**: Follow API documentation exactly
- **Field organization**: Group by domain, clear inheritance with APIRequest

## Development Standards

### Quality Checks
- **Format**: `ruff format .`
- **Lint**: `ruff check .`
- **Type Check**: `mypy .`
- **Test**: `pytest`

### Model-Specific Requirements
- All fields must have proper type hints and API-based validation
- Use `BaseModelConfig` and `APIRequest` for consistency
- Document all field aliases and constraint reasoning
- Apply comprehensive testing for validation rules

### Development Workflow
1. **Pattern implementation**: Follow model patterns and base classes
2. **API validation**: Ensure field alignment with API documentation
3. **Quality checks**: Format, lint, type check validation
4. **Alias mapping**: Verify kebab-case API compatibility

## Tool Integration

### Using Models in Tools
- Import models for parameter validation in tool functions
- Apply model validation to ensure type safety
- Use model instances for payload creation
- Leverage field aliases for API compatibility

### Payload Creation Integration
When working with utilities:
- Use `create_api_payload()` with model instances
- Apply `query_params()` for transforming model data to API parameters
- Handle model validation errors appropriately
- Ensure proper error handling for invalid inputs

### API Client Integration
When working with API client:
- Use models for request parameter validation
- Apply model serialization for API requests
- Handle validation errors before API calls
- Ensure proper type safety throughout request pipeline

## Implementation Workflow

### New Model Development Process
1. **Define model structure**: Extend `APIRequest` base class
2. **Add field validation**: Follow API documentation requirements
3. **Apply aliases**: Use kebab-case aliases for API compatibility
4. **Create enums**: For API-documented constrained choices
5. **Test validation**: Cover valid inputs, invalid inputs, edge cases
6. **Update documentation**: Implementation status tracking

### Quality Validation Checklist
For each model implementation:
- [ ] Model extends `APIRequest` base class with appropriate field aliases
- [ ] Field validation follows API documentation requirements exactly
- [ ] Parameter models created when needed for complex operations
- [ ] Enums defined for API-documented constrained choices
- [ ] Quality checks passed: format, lint, type check
- [ ] Documentation updated: implementation status tracking
- [ ] Tests cover validation scenarios: valid, invalid, edge cases