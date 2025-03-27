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

2. Add tool functions in the `terraform_cloud_mcp/tools` directory:
   - Accept typed `params` objects instead of `**kwargs`
   - Use the `@handle_api_errors` decorator
   - Use utility functions from `utils/payload.py` for JSON:API payloads
   - Use utility functions from `utils/request.py` for parameters
   - Return `APIResponse` type

3. Register new tools in `terraform_cloud_mcp/server.py`

4. Follow the Pydantic pattern for parameter validation and error handling

5. Ensure all functions include proper type hints and docstrings

6. Update documentation in the appropriate places:
   - Add model examples to `docs/models/`
   - Add tool examples to `docs/tools/`

7. Add tests for new functionality

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