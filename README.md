# Terraform Cloud MCP Server

A Model Context Protocol (MCP) server that integrates AI assistants with the Terraform Cloud API, allowing you to manage your infrastructure through natural conversation. Built with Pydantic models and structured around domain-specific modules, this server is compatible with any MCP-supporting platform including Claude, Claude Code CLI, Claude Desktop, Cursor, Copilot Studio, and others.

![Version](https://img.shields.io/badge/version-0.8.6-blue)
![Python](https://img.shields.io/badge/python-3.12+-green)
![Type Checking](https://img.shields.io/badge/type_checking-mypy-brightgreen)
![Code Quality](https://img.shields.io/badge/code_quality-100%25-success)

---

## Features

- **Account Management**: Get account details for authenticated users or service accounts.
- **Workspace Management**: Create, read, update, delete, lock/unlock workspaces.
- **Run Management**: Create runs, list runs, get run details, apply/discard/cancel runs.
- **Organization Management**: List, create, update, delete organizations, and view organization entitlements.
- **Future Features**: State management, variables management, and more.

---

## Quick Start

### Prerequisites

- Python 3.12+
- MCP (includes FastMCP and development tools)
- `uv` package manager (recommended) or `pip`
- Terraform Cloud API token

---

### Installation

```bash
# Clone the repository
git clone https://github.com/severity1/terraform-cloud-mcp.git
cd terraform-cloud-mcp

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install package
uv pip install .
```

### Adding to Claude Environments

#### Adding to Claude Code CLI

```bash
# Add to Claude Code with your Terraform Cloud token
claude mcp add -e TFC_TOKEN=YOUR_TF_TOKEN -s user terraform-cloud-mcp -- "terraform-cloud-mcp"
```

#### Adding to Claude Desktop

Create a `claude_desktop_config.json` configuration file:
- mac: ~/Library/Application Support/Claude/claude_desktop_config.json
- win: %APPDATA%\Claude\claude_desktop_config.json

```json
{
  "mcpServers": {
    "terraform-cloud-mcp": {
      "command": "/path/to/uv", # Get this by running: `which uv`
      "args": [
        "--directory",
        "/path/to/your/terraform-cloud-mcp", # Full path to this project
        "run",
        "terraform-cloud-mcp"
      ],
      "env": {
        "TFC_TOKEN": "my token..." # replace with actual token
      }
    }
  }
}
```

Replace `your_terraform_cloud_token` with your actual Terraform Cloud API token.

#### Other MCP-Compatible Platforms

For other platforms (like Cursor, Copilot Studio, or Glama), follow their platform-specific instructions for adding an MCP server. Most platforms require:
1. The server path or command to start the server.
2. Environment variables for the Terraform Cloud API token.
3. Configuration to auto-start the server when needed.

---

## Available Tools

### Account Tools

- `get_account_details()`: Gets account information for the authenticated user or service account.

### Workspace Management Tools

#### List & Search
- `list_workspaces(organization, page_number, page_size, search)`: List and filter workspaces.
- `get_workspace_details(workspace_id, organization, workspace_name)`: Get detailed information about a specific workspace.

#### Create & Update
- `create_workspace(organization, name, params)`: Create a new workspace with optional parameters.
- `update_workspace(organization, workspace_name, params)`: Update an existing workspace's configuration.

#### Delete
- `delete_workspace(organization, workspace_name)`: Delete a workspace and all its content.
- `safe_delete_workspace(organization, workspace_name)`: Delete only if the workspace isn't managing any resources.

#### Lock & Unlock
- `lock_workspace(workspace_id, reason)`: Lock a workspace to prevent runs.
- `unlock_workspace(workspace_id)`: Unlock a workspace to allow runs.
- `force_unlock_workspace(workspace_id)`: Force unlock a workspace locked by another user.

#### Data Retention
- `set_data_retention_policy(workspace_id, days)`: Set a data retention policy.
- `get_data_retention_policy(workspace_id)`: Get the current data retention policy.
- `delete_data_retention_policy(workspace_id)`: Delete the data retention policy.

### Run Management Tools

- `create_run(workspace_id, params)`: Create and queue a Terraform run in a workspace using its ID.
- `list_runs_in_workspace(workspace_id, ...)`: List and filter runs in a specific workspace using its ID.
- `list_runs_in_organization(organization, ...)`: List and filter runs across an entire organization.
- `get_run_details(run_id)`: Get detailed information about a specific run.
- `apply_run(run_id, comment)`: Apply a run waiting for confirmation.
- `discard_run(run_id, comment)`: Discard a run waiting for confirmation.
- `cancel_run(run_id, comment)`: Cancel a run currently planning or applying.
- `force_cancel_run(run_id, comment)`: Forcefully cancel a run immediately.
- `force_execute_run(run_id)`: Forcefully execute a pending run by canceling prior runs.

### Organization Management Tools

- `get_organization_details(organization)`: Get detailed information about a specific organization.
- `get_organization_entitlements(organization)`: Show entitlement set for organization features.
- `list_organizations(page_number, page_size, query, query_email, query_name)`: List and filter organizations.
- `create_organization(name, email, params)`: Create a new organization with optional parameters.
- `update_organization(organization, params)`: Update an existing organization's settings.
- `delete_organization(organization)`: Delete an organization and all its content.

---

## Development Guide

> **Note**: This project uses explicit Pydantic models for request validation and parameter handling. Common patterns like JSON:API payload construction have been extracted to utility functions in `utils/payload.py` and `utils/request.py` following KISS and DRY principles.

### Development Setup

If you're contributing to or modifying the codebase, use this development setup:

```bash
# Clone the repository
git clone https://github.com/severity1/terraform-cloud-mcp.git
cd terraform-cloud-mcp

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install in development mode (editable)
uv pip install -e .

# Install development dependencies
uv pip install black mypy pydantic ruff
```

For development work, the editable installation (`-e` flag) is essential as it allows you to modify the code and have changes reflected immediately without reinstalling the package.

---

### Adding to Claude Code (Development Mode)

For development work with Claude Code CLI, you can add the MCP server as follows:

```bash
# Add to Claude Code with your development path and token
claude mcp add -e TFC_TOKEN=YOUR_TF_TOKEN -s user terraform-cloud-mcp -- "$(pwd)/terraform_cloud_mcp/server.py"
```

This points Claude Code to your local development version rather than the installed package. Replace `YOUR_TF_TOKEN` with your actual Terraform Cloud API token.

---

### Adding to Claude Desktop (Development Mode)

For development work with Claude Desktop, create a `claude_desktop_config.json` configuration file:

```json
{
  "mcpServers": {
    "terraform-cloud-mcp": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/path/to/terraform-cloud-mcp",
        "run",
        "terraform_cloud_mcp/server.py"
      ],
      "env": {
        "TFC_TOKEN": "your_terraform_cloud_token"
      }
    }
  }
}
```

Replace the placeholders with the following:
- `/path/to/uv`: The full path to the `uv` executable (find it with `which uv` on macOS/Linux or `where uv` on Windows).
- `/path/to/terraform-cloud-mcp`: The full path to your local `terraform-cloud-mcp` project directory.
- `your_terraform_cloud_token`: Your actual Terraform Cloud API token.

This configuration tells Claude Desktop how to start the MCP server automatically in development mode.

---

## Code Structure

The project follows a modular structure organized by domain and responsibility:

```
terraform_cloud_mcp/
├── api/                 # API client and core request handling
│   ├── __init__.py
│   └── client.py        # Core API client with error handling
├── models/              # Pydantic data models for validation
│   ├── __init__.py
│   ├── account.py       # Account-related models
│   ├── base.py          # Base model classes and shared types
│   ├── organizations.py # Organization models
│   ├── runs.py          # Run management models
│   └── workspaces.py    # Workspace management models
├── tools/               # Tool implementations exposed via MCP
│   ├── __init__.py
│   ├── account.py       # Account management tools
│   ├── organizations.py # Organization management tools
│   ├── runs.py          # Run management tools
│   └── workspaces.py    # Workspace management tools
├── utils/               # Shared utilities
│   ├── __init__.py
│   ├── decorators.py    # Error handling decorators
│   ├── payload.py       # JSON:API payload utilities
│   └── request.py       # Request parameter utilities
└── server.py            # MCP server entry point
```

### Architecture

The project follows a layered architecture:

1. **Models Layer** (`models/`): Pydantic data models for validation and serialization
2. **API Layer** (`api/`): Core HTTP client for Terraform Cloud API communication
3. **Utilities Layer** (`utils/`): Shared helper functions and decorators 
4. **Tools Layer** (`tools/`): User-facing tool implementations that compose the other layers
5. **Server Layer** (`server.py`): MCP protocol implementation and tool registration

### Code Quality Guidelines

The project follows strict code quality guidelines including:

- **KISS Commenting**: Comments explain only non-obvious "why" behind code choices, not "what"
- **DRY Pattern**: Common code patterns use utility functions to reduce duplication
- **Strong Type Safety**: Comprehensive type hints and Pydantic validation throughout
- **Consistent Documentation**: Clear, standardized docstrings with Args/Returns sections

### Development Commands

The project uses these tools for quality assurance:

```bash
# Run the server in development mode with MCP Inspector UI
mcp dev terraform_cloud_mcp/server.py

# Debug with PDB
TFC_TOKEN=your_token uv run -m pdb terraform_cloud_mcp/server.py

# Run type checking
uv run -m mypy .

# Run linter
uv run -m ruff check .

# Auto-fix linting issues
uv run -m ruff check --fix .

# Format code with Black
uv run -m black .

# Run tests (when available)
uv run -m unittest discover tests
```

Type checking configuration is available in both `pyproject.toml` and `mypy.ini`. The configuration enforces strict typing rules including:

- Disallowing untyped definitions
- Warning on returning `Any` types
- Checking completeness of function definitions
- Namespace packages support
- Module-specific configurations

---

### Additional Commands

```bash
# Using MCP dev tools (provides debugging tools)
mcp dev terraform_cloud_mcp/server.py

# Using MCP run command
mcp run terraform_cloud_mcp/server.py

# Standard method
uv run terraform_cloud_mcp/server.py

# With token via environment variable
export TFC_TOKEN=YOUR_TF_TOKEN
uv run terraform_cloud_mcp/server.py

# Using a .env file
echo "TFC_TOKEN=YOUR_TF_TOKEN" > .env
uv run terraform_cloud_mcp/server.py
```

---

### Extending the Server

1. Add model classes in the `terraform_cloud_mcp/models` directory:
   - Define enums for constrained choices
   - Create request models inheriting from `APIRequest`
   - Create a `*Params` model for function parameters
2. Add tool functions in the `terraform_cloud_mcp/tools` directory:
   - Accept typed `params` objects instead of `**kwargs`
   - Use the `@handle_api_errors` decorator
   - Use utility functions from `utils/payload.py` for JSON:API payloads:
     - `create_api_payload()` for standard payload creation
     - `add_relationship()` for resource relationships
   - Use utility functions from `utils/request.py` for parameters:
     - `pagination_params()` for standard pagination parameters
   - Return `APIResponse` type
3. Register new tools in `terraform_cloud_mcp/server.py`.
4. Follow the Pydantic pattern for parameter validation and error handling.
5. Ensure all functions include proper type hints and docstrings.
6. Update documentation in `README.md`.
7. Add tests for new functionality.

---

## Documentation

The codebase includes comprehensive documentation:

- **Code Comments**: Focused on explaining the "why" behind implementation decisions
- **Docstrings**: All public functions and classes include detailed docstrings
- **Example Files**: The `docs/` directory contains detailed examples for each domain:
  - `docs/models/`: Usage examples for all model types
  - `docs/tools/`: Detailed usage examples for each tool
  - `docs/standards.md`: Comprehensive coding standards guidelines
  - `docs/conversations/`: Sample conversation flows with the API

## Troubleshooting

1. Check server logs (debug logging is enabled by default)
2. Use the MCP Inspector (http://localhost:5173) for debugging
3. Debug logging is already enabled in `server.py`:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

---

## Contributing

Contributions are welcome! Please open an issue or pull request if you'd like to contribute to this project.

Guidelines:
- Ensure all code includes proper type hints.
- Run mypy type checking before submitting PRs.
- Add tests for new functionality.
- Update documentation for any new features or changes.