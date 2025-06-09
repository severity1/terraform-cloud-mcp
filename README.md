[![MseeP.ai Security Assessment Badge](https://mseep.net/mseep-audited.png)](https://mseep.ai/app/severity1-terraform-cloud-mcp)

# Terraform Cloud MCP Server

A Model Context Protocol (MCP) server that integrates AI assistants with the Terraform Cloud API, allowing you to manage your infrastructure through natural conversation. Built with Pydantic models and structured around domain-specific modules, this server is compatible with any MCP-supporting platform including Claude, Claude Code CLI, Claude Desktop, Cursor, Copilot Studio, and others.

![Version](https://img.shields.io/badge/version-0.8.12-blue)
![Python](https://img.shields.io/badge/python-3.12+-green)
![Type Checking](https://img.shields.io/badge/type_checking-mypy-brightgreen)
![Code Quality](https://img.shields.io/badge/code_quality-100%25-success)

---

## Features

- **Account Management**: Get account details for authenticated users or service accounts.
- **Workspace Management**: Create, read, update, delete, lock/unlock workspaces.
- **Project Management**: Create, list, update, and delete projects; manage project tag bindings and move workspaces between projects.
- **Run Management**: Create runs, list runs, get run details, apply/discard/cancel runs.
- **Plan Management**: Retrieve plan details and JSON execution output with advanced HTTP redirect handling.
- **Apply Management**: Get apply details and recover from failed state uploads.
- **Organization Management**: List, create, update, delete organizations, and view organization entitlements.
- **Cost Estimation**: Retrieve detailed cost estimates for infrastructure changes including proposed monthly costs, prior costs, resource counts, and usage projections.
- **Future Features**: Variables management, state versions, and more.

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

<!-- Future implementation: Data Retention
- `set_data_retention_policy(workspace_id, days)`: Set a data retention policy.
- `get_data_retention_policy(workspace_id)`: Get the current data retention policy.
- `delete_data_retention_policy(workspace_id)`: Delete the data retention policy. -->

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

### Plan Management Tools

- `get_plan_details(plan_id)`: Get detailed information about a specific plan.
- `get_plan_json_output(plan_id)`: Retrieve the JSON execution plan for a specific plan with proper redirect handling.
- `get_run_plan_json_output(run_id)`: Retrieve the JSON execution plan from a run with proper redirect handling.

### Apply Management Tools

- `get_apply_details(apply_id)`: Get detailed information about a specific apply.
- `get_errored_state(apply_id)`: Retrieve the errored state from a failed apply for recovery.

### Project Management Tools

- `create_project(organization, name, params)`: Create a new project with optional parameters.
- `update_project(project_id, params)`: Update an existing project's configuration.
- `list_projects(organization, ...)`: List and filter projects in an organization.
- `get_project_details(project_id)`: Get detailed information about a specific project.
- `delete_project(project_id)`: Delete a project (fails if it contains workspaces).
- `list_project_tag_bindings(project_id)`: List tags bound to a project.
- `add_update_project_tag_bindings(project_id, tag_bindings)`: Add or update tag bindings on a project.
- `move_workspaces_to_project(project_id, workspace_ids)`: Move workspaces into a project.

### Organization Management Tools

- `get_organization_details(organization)`: Get detailed information about a specific organization.
- `get_organization_entitlements(organization)`: Show entitlement set for organization features.
- `list_organizations(page_number, page_size, query, query_email, query_name)`: List and filter organizations.
- `create_organization(name, email, params)`: Create a new organization with optional parameters.
- `update_organization(organization, params)`: Update an existing organization's settings.
- `delete_organization(organization)`: Delete an organization and all its content.

### Cost Estimation Tools

- `get_cost_estimate_details(cost_estimate_id)`: Get detailed information about a specific cost estimate, including resource counts (matched and unmatched), prior monthly cost, proposed monthly cost, and delta monthly cost estimations. Use run relationships to find cost estimate IDs for specific runs.

---

## Development Guide

For detailed development guidance including code standards, Pydantic patterns, and contribution workflows, see our [Development Documentation](docs/DEVELOPMENT.md).

### Quick Development Setup

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

### Basic Development Commands

```bash
# Run the server in development mode
mcp dev terraform_cloud_mcp/server.py

# Run tests and quality checks
uv run -m mypy .
uv run -m ruff check .
uv run -m black .
```

For detailed information on code organization, architecture, development workflows, and code quality guidelines, refer to [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

---

## Documentation

The codebase includes comprehensive documentation:

- **Code Comments**: Focused on explaining the "why" behind implementation decisions
- **Docstrings**: All public functions and classes include detailed docstrings
- **Implementation References**: Development documentation now references actual code examples rather than using code snippets
- **Example Files**: The `docs/` directory contains detailed examples for each domain:
  - `docs/DEVELOPMENT.md`: Development standards and coding guidelines with references to actual code
  - `docs/CONTRIBUTING.md`: Guidelines for contributing to the project
  - `docs/models/`: Reference documentation for all model types
  - `docs/tools/`: Detailed reference documentation for each tool
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

See our [Contributing Guide](docs/CONTRIBUTING.md) for detailed instructions on how to get started, code quality standards, and the pull request process.

## Disclaimer

This project is not affiliated with, associated with, or endorsed by HashiCorp or Terraform.  
"Terraform" and "Terraform Cloud" are trademarks of HashiCorp.  
This project merely interacts with the Terraform Cloud public API under fair use.