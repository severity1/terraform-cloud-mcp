# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Terraform Cloud MCP Development Guide

## Subagent Usage Guidelines

Subagents MUST be used for complex tasks following these rules:

- Use a minimum of 2 and maximum of 6 subagents for complex tasks
- Assign different roles/"hats" to each subagent for more effective task division:
  - Researcher: For finding patterns, documentation, and existing implementations
  - Architect: For designing complex features and ensuring adherence to project patterns
  - Implementer: For writing the actual code following project conventions
  - Tester/Reviewer: For verifying implementations and checking for edge cases
- Use subagents particularly for:
  - Complex multi-step search operations or investigations
  - Independent verification of implementations
  - Early planning stages of complex features
  - Test-driven development to avoid overfitting

## Component-Specific Guidelines

For detailed guidance on specific components, refer to the relevant CLAUDE.md files:

- [docs/CLAUDE.md](docs/CLAUDE.md) - Documentation structure and standards
- [terraform_cloud_mcp/api/CLAUDE.md](terraform_cloud_mcp/api/CLAUDE.md) - API client details and usage
- [terraform_cloud_mcp/models/CLAUDE.md](terraform_cloud_mcp/models/CLAUDE.md) - Pydantic models patterns and implementation
- [terraform_cloud_mcp/tools/CLAUDE.md](terraform_cloud_mcp/tools/CLAUDE.md) - MCP tools implementation
- [terraform_cloud_mcp/utils/CLAUDE.md](terraform_cloud_mcp/utils/CLAUDE.md) - Utility functions and patterns

## Build & Run Commands
- Setup: `uv pip install -e .` (install with latest changes)
- Install dev deps: `uv pip install black mypy pydantic ruff`
- Format: `uv pip install black && uv run -m black .` 
- Type check: `uv pip install mypy && uv run -m mypy .`
- Lint: `uv pip install ruff && uv run -m ruff check .`
- Fix lint issues: `uv pip install ruff && uv run -m ruff check --fix .`

## Code Style Guidelines

> Note: Development documentation references actual code implementations rather than using code snippets. See docs/DEVELOPMENT.md for details.
- **KISS Principle**: Keep It Simple, Stupid. Favor simple, maintainable solutions over complex ones.
- **DRY Principle**: Don't Repeat Yourself. Use utility functions for common patterns.
- **Imports**: stdlib → third-party → local, alphabetically within groups
- **Formatting**: Black, 100 char line limit
- **Types**: Type hints everywhere, Pydantic models for validation
- **Pydantic Pattern**: See `terraform_cloud_mcp/models/workspaces.py` for reference implementation:
  - Use `BaseModelConfig` base class for common configuration
  - Use `APIRequest` for request validation
  - Define explicit model classes for parameter objects (e.g., `WorkspaceParams`)
  - Use `params` parameter instead of `**kwargs` in tool functions
  - Use explicit field aliases (e.g., `alias="kebab-case-name"`) for API field mapping
  - Type API responses as `APIResponse` (alias for `Dict[str, Any]`)
- **Utility Functions**: Use common utilities for repetitive patterns:
  - `create_api_payload()` from `utils/payload.py` for JSON:API payload creation
  - `add_relationship()` from `utils/payload.py` for relationship management
  - `query_params()` from `utils/request.py` for converting model to API parameters
- **API Response Handling**:
  - Handle 204 No Content responses properly, returning `{"status": "success", "status_code": 204}`
  - Implement custom redirect handling for pre-signed URLs
  - Use proper error handling for JSON parsing failures
- **Naming**: snake_case (functions/vars), PascalCase (classes), UPPER_CASE (constants)
- **Error handling**: Use `handle_api_errors` decorator from `terraform_cloud_mcp/utils/decorators.py` for consistent API error handling
- **Async pattern**: All API functions should be async, using httpx
- **Security**: Never log tokens, validate all inputs, redact sensitive data
- **Documentation**: 
  - Docstrings with Args/Returns for all functions
  - Reference specific code implementations in docs rather than code snippets
  - See cost_estimates.py for latest documentation patterns
- **Comments**: Follow KISS principles for comments:
  - Only explain the non-obvious "why" behind code choices, not the "what"
  - Add comments for complex logic, edge cases, security measures, or API-specific requirements
  - Avoid redundant, unnecessary, or self-explanatory comments
  - Keep comments concise and directly relevant

## Workflow Guidelines
- When adding/implementing new tools:
  - Create model documentation in `docs/models/`
  - Create documentation in `docs/tools/`
  - Create conversation example in `docs/conversations/`
  - Always update `docs/README.md`, `docs/DEVELOPMENT.md`
  - Update any relevant `CLAUDE.md` files to include tool information

- Update `TASKS.md` to mark task as completed if it exists and is used for the task.