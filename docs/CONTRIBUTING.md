# Contributing to Terraform Cloud MCP

Thank you for your interest in contributing to the Terraform Cloud MCP project! This document provides guidelines and instructions for contributing to this project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your forked repository locally
3. Set up the development environment as described in the [Development Guide](DEVELOPMENT.md)

## Development Environment

```bash
# Clone the repository
git clone https://github.com/severity1/terraform-cloud-mcp.git
cd terraform-cloud-mcp

# Create virtual environment and activate it
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with development dependencies
uv pip install -e .
uv pip install black mypy pydantic ruff
```

## Code Quality Standards

Before submitting your contribution, please ensure your code meets our quality standards:

1. **Type Checking**: Use proper type hints everywhere
   ```bash
   uv run -m mypy .
   ```

2. **Linting**: Ensure code follows our style guidelines
   ```bash
   uv run -m ruff check .
   ```

3. **Formatting**: Format code with Black
   ```bash
   uv run -m black .
   ```

4. **Tests**: Add tests for new functionality
   ```bash
   uv run -m unittest discover tests
   ```

## Contribution Guidelines

### Pull Request Process

1. Create a feature branch for your changes
2. Make your changes following the code style guidelines in the [Development Guide](DEVELOPMENT.md)
3. Add or update tests to verify your changes
4. Update documentation, including:
   - Function docstrings
   - Example files in the appropriate `docs/` subdirectory
   - README.md if adding new features or changing APIs
5. Run all quality checks to ensure your code meets our standards
6. Commit your changes with a clear, descriptive commit message
7. Push your branch and create a pull request

### Commit Messages

Write clear, descriptive commit messages that explain *why* the change was made, not just *what* changed. For example:

```
Fix workspace creation validation for execution mode

The workspace creation API was not properly validating the execution
mode and defaulting to 'local' instead of 'remote', causing confusion
for users. This fix ensures defaults match API documentation.
```

## Extending the Server

To add new functionality to the MCP server:

1. Add model classes in the `terraform_cloud_mcp/models` directory:
   - Define enums for constrained choices
   - Create request models inheriting from `APIRequest`
   - Create a `*Params` model for function parameters
   - For examples, see:
     - `account.py` for simple request models
     - `workspaces.py` for comprehensive models with params 
     - `cost_estimates.py` for models with enums and status tracking

2. Add tool functions in the `terraform_cloud_mcp/tools` directory:
   - Accept typed `params` objects instead of `**kwargs`
   - Use the `@handle_api_errors` decorator
   - Use utility functions from `utils/payload.py` for JSON:API payloads
   - Use utility functions from `utils/request.py` for parameters
   - Return `APIResponse` type
   - For examples, see:
     - `account.py` for simple GET operations
     - `workspaces.py` for full CRUD operations
     - `cost_estimates.py` for specialized retrieval operations

3. Register new tools in `terraform_cloud_mcp/server.py`:
   - Add import statements at the top
   - Use `mcp.tool()(module_name.function_name)` to register each function
   - Group related tools together with comments

4. Follow the Pydantic pattern for parameter validation and error handling

5. Ensure all functions include proper type hints and docstrings

6. Update documentation in the appropriate places (following reference-based documentation approach):
   - Add model documentation to `docs/models/` (e.g., `cost_estimate.md`) with model structure, validation rules, and references to actual implementations
   - Add tool reference documentation to `docs/tools/` (e.g., `cost_estimate.md`) following the established format:
     - Overview section explaining the tool's purpose
     - API Reference section with links to Terraform Cloud API documentation
     - Tools Reference section with function signatures, parameters, return values, and references to actual implementations
     - Notes section for important usage information
     - Common Error Scenarios section in table format
   - Add conversation examples to `docs/conversations/` (e.g., `cost-estimate-conversation.md`) showing real-world usage patterns with the API
   - Update `docs/README.md` to include new functionality
   - Update `README.md` to include new functionality
   - Update `docs/CONTRIBUTING.md` (this file) to reflect new patterns or processes
   - Update `docs/DEVELOPMENT.md` to include new development standards or patterns

7. Update existing integration files:
   - Add exports to `models/__init__.py`
   - Add imports to `tools/__init__.py`

8. Update `CLAUDE.md` files to document new functionality:
   - Update main `CLAUDE.md` if adding major new components
   - Update `docs/CLAUDE.md` with changes to documentation structure or standards
   - Update component-specific CLAUDE.md files as needed:
     - `terraform_cloud_mcp/api/CLAUDE.md` for API client changes
     - `terraform_cloud_mcp/models/CLAUDE.md` for model patterns
     - `terraform_cloud_mcp/tools/CLAUDE.md` for tool implementation patterns
     - `terraform_cloud_mcp/utils/CLAUDE.md` for utility function patterns
   - These files should include:
     - New patterns introduced
     - Additional examples for AI assistance
     - Component-specific guidelines
   - These files are critical for AI-assisted development and should document any non-obvious patterns

## Release Process

If you are a maintainer with release permissions, follow these steps for releasing a new version:

1. Update version number in:
   - `pyproject.toml`
   - `README.md` badges
   - Create release notes

2. Run quality checks:
   - `uv run -m mypy .`
   - `uv run -m ruff check .`
   - `uv run -m black --check .`
   - `uv run -m unittest discover tests`

3. Commit changes with clear message

4. Tag the release with the version number:
   - `git tag v0.x.y`

5. Push changes and tags:
   - `git push origin main --tags`

## Questions?

If you have any questions or need help, please open an issue on GitHub and we'll be happy to assist you.

Thank you for contributing!