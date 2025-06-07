# CLAUDE.md for docs/

This file provides guidance about the documentation structure in this repository.

## Documentation Structure

- **CONTRIBUTING.md**: Contributing guidelines including code quality standards and PR process
- **DEVELOPMENT.md**: Detailed development standards, code organization, and best practices
- **README.md**: Overview of the documentation directory

### Subdirectories

- **conversations/**: Example conversation flows with the API showing real-world usage patterns
  - Usage examples demonstrating how to interact with each domain
  - Each file focuses on a specific domain (e.g., workspace management, run management, cost estimation)

- **models/**: Reference documentation for all Pydantic model types
  - Descriptions of model structure, fields, and usage
  - Organized by domain (e.g., workspace.md, run.md, cost_estimate.md)
  - Includes validation rules and API mapping details

- **tools/**: Reference documentation for each API tool
  - Function signatures, parameters, and return values
  - Error handling patterns and expected responses
  - Organized by domain (e.g., workspace.md, run.md, cost_estimate.md)
  - Includes API endpoints and common error scenarios

## Documentation Standards

- Each domain should have consistent documentation across models/, tools/, and conversations/
- Reference specific code implementations rather than duplicating code examples
- Document input parameters, return types, and error handling
- Include references to Terraform Cloud API documentation where relevant
- Organize examples from basic to advanced
- Provide direct references to actual code for implementation details

## Adding New Documentation

When adding a new feature:

1. Create model documentation in docs/models/{feature}.md
2. Create tool documentation in docs/tools/{feature}.md
3. Create conversation examples in docs/conversations/{feature}-conversation.md
4. Update main README.md to include new functionality

## AI Guidelines

When working with docs:
- Maintain consistent style with existing documentation
- Include complete working examples that can be copied and run
- Ensure code examples are consistent with actual implementation
- Include proper error handling in examples
- Keep examples concise but complete