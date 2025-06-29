# CLAUDE.md for docs/

This file provides guidance about the documentation structure and standards in this repository.

## Documentation Architecture

### Core Files
- **DEVELOPMENT.md**: Development standards and comprehensive build/quality guidance
- **CONTRIBUTING.md**: Contributing guidelines and PR process
- **README.md**: Documentation directory overview
- **API_REFERENCES.md**: Terraform Cloud API reference links and implementation status

### Multi-Layer Structure
Documentation follows a consistent 4-layer pattern for each domain:

1. **conversations/**: Real-world usage examples and interaction patterns
2. **models/**: Pydantic model documentation with validation rules and API mappings
3. **tools/**: API tool reference with signatures, parameters, and error scenarios
4. **Code docstrings**: Implementation-level documentation with cross-references

## Documentation Standards

### Core Principles
- **Consistency**: Each domain has documentation across all 4 layers
- **Implementation-focused**: Reference actual code rather than duplicate examples
- **Cross-referenced**: All layers link to related documentation
- **API-aligned**: Include Terraform Cloud API documentation references

### Quality Requirements
- Document input parameters, return types, and error handling
- Organize examples from basic to advanced
- Use consistent anchor names (#lowercase-with-hyphens)
- Maintain valid cross-references with relative paths

## New Tool Documentation Workflow

### Implementation Steps
1. **Model Documentation**: Create `docs/models/{domain}.md` with validation rules and API mappings
2. **Tool Documentation**: Create `docs/tools/{domain}.md` with function signatures and examples
3. **Conversation Examples**: Create `docs/conversations/{domain}-conversation.md` with usage scenarios
4. **Cross-References**: Link all layers bidirectionally
5. **Integration**: Update `docs/README.md` and relevant CLAUDE.md files

### Cross-Reference Requirements
Every new tool must maintain bidirectional links across all 4 layers:
- **Code docstrings** → docs/tools/ sections
- **docs/tools/** ↔ docs/models/ (bidirectional)
- **docs/tools/** → docs/conversations/ examples  
- **docs/models/** → tools that use the model
- **docs/conversations/** → specific tool and model sections

### Validation Checklist
- [ ] All markdown links use relative paths
- [ ] Cross-references use consistent anchor names (#lowercase-with-hyphens)
- [ ] Each layer references appropriate related layers
- [ ] All links are valid and accessible

## Development Integration

### Quality Standards
Complete development guidance is in [DEVELOPMENT.md](DEVELOPMENT.md):
- **Build Commands**: Setup and quality check sequences
- **Quality Protocols**: 5-step mandatory validation process
- **Style Guidelines**: KISS/DRY principles and error handling patterns

### AI Documentation Guidelines
- Maintain consistency with existing documentation patterns
- Reference actual code implementations rather than duplicate examples
- Ensure examples include proper error handling
- Keep examples concise but comprehensive
- Follow cross-reference requirements above

## Component Cross-References

### Related Guidance
- **[../terraform_cloud_mcp/tools/CLAUDE.md](../terraform_cloud_mcp/tools/CLAUDE.md)** - Tool documentation patterns
- **[../terraform_cloud_mcp/models/CLAUDE.md](../terraform_cloud_mcp/models/CLAUDE.md)** - Model documentation standards
- **[../terraform_cloud_mcp/utils/CLAUDE.md](../terraform_cloud_mcp/utils/CLAUDE.md)** - Utility documentation patterns
- **[../terraform_cloud_mcp/api/CLAUDE.md](../terraform_cloud_mcp/api/CLAUDE.md)** - API documentation integration

---

## Documentation Templates

### Code Docstring Template
```python
"""Tool description with clear usage context.

API endpoint: METHOD /path/to/endpoint

Args:
    param_name: Description with format/constraints (e.g., "ws-xxxxxxxx")
    
Returns:
    Description of return structure and key fields
    
See:
    docs/tools/domain.md#tool-name for usage examples
"""
```

### Tool Reference Template  
```markdown
### tool_name
**Function:** `tool_name(param1: str, param2: int = 0) -> APIResponse`  
**Description:** What it does and when to use it
**Parameters:** 
- param1: Description with format requirements
- param2: Description with default value
**Returns:** Return structure explanation
**Models:** [DomainModel](../models/domain.md#domainmodel)
**Examples:** [Usage Scenario](../conversations/domain-conversation.md#scenario-name)
```

### Model Documentation Template
```markdown
### ModelName
**Purpose:** What this model validates
**Used by:** [tool_name](../tools/domain.md#tool-name), [other_tool](../tools/domain.md#other-tool)
**Fields:** Field descriptions and validation rules
**API Mapping:** model_field -> "api-field-name"
```

### Conversation Example Template
```markdown
## Scenario Name
**Tools used:** [tool_name](../tools/domain.md#tool-name)
**Models:** [ModelName](../models/domain.md#modelname)
**Description:** Realistic usage scenario with expected inputs/outputs
```