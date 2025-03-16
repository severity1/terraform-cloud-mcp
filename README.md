# Terraform Cloud MCP Server

A Model Context Protocol (MCP) server that integrates Claude with the Terraform Cloud API, allowing Claude to manage your Terraform infrastructure through natural conversation.

![Version](https://img.shields.io/badge/version-0.6.0-blue)
![Python](https://img.shields.io/badge/python-3.12+-green)
![Type Checking](https://img.shields.io/badge/type_checking-mypy-brightgreen)

## Features

- **Authentication** - Validate tokens and get user information
- **Workspace Management** - Create, read, update, delete, lock/unlock workspaces
- **Run Management** - Create runs, list runs, get run details, apply/discard/cancel runs
- **Future Features** - State management, variables management, and more

## Quick Start

### Setup

```bash
# Clone the repository
git clone https://github.com/severity1/terraform-cloud-mcp.git
cd terraform-cloud-mcp

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e .
```

### Starting the Server

The server supports multiple ways to provide your Terraform Cloud API token:

```bash
# Using MCP dev tools (provides debugging tools)
mcp dev server.py

# Using MCP run command
mcp run server.py

# Standard method
uv run server.py

# With token via environment variable
export TFC_TOKEN=YOUR_TF_TOKEN
uv run server.py

# Using a .env file
echo "TFC_TOKEN=YOUR_TF_TOKEN" > .env
uv run server.py

# Run in background
uv run server.py > server.log 2>&1 & echo $! > server.pid
```

When a token is provided, Claude can use it without you having to specify it in every command.

### Connecting with Claude

#### Using Claude Code CLI

```bash
# Add the MCP server
claude mcp add terraform-cloud-mcp "uv run $(pwd)/server.py"

# With token
claude mcp add terraform-cloud-mcp -e TFC_TOKEN=YOUR_TF_TOKEN -- "uv run $(pwd)/server.py"

# Verify it was added
claude mcp list

# For debugging, you can use MCP Inspector with 'mcp dev' command
```

#### Using Claude Desktop

Create a `claude_desktop_config.json` configuration file:

```json
{
  "mcpServers": {
    "terraform-cloud-mcp": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/path/to/terraform-cloud-mcp",
        "run",
        "server.py"
      ],
      "env": {
        "TFC_TOKEN": "your_terraform_cloud_token"
      }
    }
  }
}
```

Replace the paths and token with your actual values:
- Use the full path to the uv executable (find it with `which uv` on macOS/Linux or `where uv` on Windows)
- Set the correct directory path to your terraform-cloud-mcp installation
- Add your Terraform Cloud API token

This configuration tells Claude Desktop how to start the MCP server automatically.

## Available Tools

### Authentication Tools

The following tools help validate and work with Terraform Cloud API tokens:

- `validate_token()`  
  Validates a Terraform Cloud API token

- `get_terraform_user_info()`  
  Gets user information for the provided token

### Workspace Management Tools

#### List & Search

Tools for finding and inspecting workspaces:

- `list_workspaces(organization, ...)`  
  List and filter workspaces with comprehensive options
  
  *Required:* `organization` - Organization name  
  *Optional:* Filtering by name, tags, pagination, sorting and more

- `get_workspace_details(organization, workspace_name)`  
  Get detailed information about a specific workspace
  
  *Required:* `organization`, `workspace_name`

#### Create & Update

Tools for creating and modifying workspaces:

- `create_workspace(organization, name, ...)`  
  Create a new workspace with various configuration options
  
  *Required:* `organization`, `name`  
  *Optional:* Configure Terraform version, VCS settings, execution mode, etc.

- `update_workspace(organization, workspace_name, ...)`  
  Update an existing workspace's configuration
  
  *Required:* `organization`, `workspace_name`  
  *Optional:* Update name, description, settings, VCS connections, etc.

#### Delete

Tools for removing workspaces:

- `delete_workspace(organization, workspace_name)`  
  Delete a workspace and all its content
  
  *Required:* `organization`, `workspace_name`

- `safe_delete_workspace(organization, workspace_name)`  
  Delete only if the workspace isn't managing any resources
  
  *Required:* `organization`, `workspace_name`

#### Lock & Unlock

Tools for controlling workspace access:

- `lock_workspace(organization, workspace_name, reason)`  
  Lock a workspace to prevent runs
  
  *Required:* `organization`, `workspace_name`  
  *Optional:* `reason` - Explanation for the lock

- `unlock_workspace(organization, workspace_name)`  
  Unlock a workspace to allow runs
  
  *Required:* `organization`, `workspace_name`

- `force_unlock_workspace(organization, workspace_name)`  
  Force unlock a workspace locked by another user
  
  *Required:* `organization`, `workspace_name`

### Run Management Tools

Tools for managing Terraform runs (plan, apply, and other operations):

- `create_run(organization, workspace_name, ...)`  
  Create and queue a Terraform run in a workspace
  
  *Required:* `organization`, `workspace_name`  
  *Optional:* `message`, `auto_apply`, `is_destroy`, `refresh`, `refresh_only`, `plan_only`, `target_addrs`, `replace_addrs`, `variables`, and more configuration options

- `list_runs_in_workspace(organization, workspace_name, ...)`  
  List and filter runs in a specific workspace with comprehensive options
  
  *Required:* `organization`, `workspace_name`  
  *Optional:* Pagination, filtering by status/operation/source, searching by user/commit

- `list_runs_in_organization(organization, ...)`  
  List and filter runs across an entire organization
  
  *Required:* `organization`  
  *Optional:* Pagination, filtering by workspace/status/operation/source, searching by user/commit

- `get_run_details(run_id)`  
  Get detailed information about a specific run
  
  *Required:* `run_id`
  
- `apply_run(run_id, comment)`  
  Apply a run that is paused waiting for confirmation after a plan
  
  *Required:* `run_id`  
  *Optional:* `comment`
  
- `discard_run(run_id, comment)`  
  Discard a run that is waiting for confirmation or priority
  
  *Required:* `run_id`  
  *Optional:* `comment`
  
- `cancel_run(run_id, comment)`  
  Cancel a run that is currently planning or applying
  
  *Required:* `run_id`  
  *Optional:* `comment`
  
- `force_cancel_run(run_id, comment)`  
  Forcefully cancel a run immediately (after a normal cancel)
  
  *Required:* `run_id`  
  *Optional:* `comment`
  
- `force_execute_run(run_id)`  
  Forcefully execute a pending run by canceling prior runs
  
  *Required:* `run_id`

## Example Conversations

### Authentication & Listing

```
# Using explicit token
User: Can you validate this Terraform Cloud API token: my-tf-token-value
Claude: [Validates token and confirms it's working]

# Using default token (if server started with TFC_TOKEN)
User: Can you validate my Terraform Cloud API token?
Claude: [Validates token and confirms it's working]

User: List all my workspaces in "example-org"
Claude: [Lists all workspaces in the organization]

User: Find all workspaces in "example-org" with names containing "prod"
Claude: [Lists matching workspaces with "prod" in their names]

User: List workspaces in "example-org" with the "environment:production" tag
Claude: [Lists workspaces with that specific tag]
```

### Workspace Management

```
User: Get details for the "production" workspace in "example-org"
Claude: [Shows detailed information about the workspace]

User: Create a new workspace in "example-org" called "staging" with auto-apply enabled
Claude: [Creates the requested workspace]

User: Update my "staging" workspace to use Terraform version 1.5.0
Claude: [Updates the workspace with the specified version]

User: Delete my "dev-test" workspace in "example-org"
Claude: [Deletes the workspace]

User: Delete my "staging" workspace but only if it's not managing any resources
Claude: [Uses safe_delete_workspace to safely delete the workspace]
```

### Locking Workspaces

```
User: Lock my "production" workspace while we do maintenance
Claude: [Locks the workspace with the provided reason]

User: The maintenance is complete, unlock "production" now
Claude: [Unlocks the workspace]

User: Someone left "staging" locked and they're out today. Can you force unlock it?
Claude: [Force unlocks the workspace]
```

### Run Management

```
User: Create a plan for my "production" workspace
Claude: [Creates a plan-only run in the workspace]

User: Create a destroy plan for "dev-test" workspace
Claude: [Creates a destroy plan run in the workspace]

User: Run a targeted plan in "staging" that only affects the database resources
Claude: [Creates a plan with target_addrs for database resources]

User: Create a plan with custom variables in the "development" workspace
Claude: [Creates a run with custom variable values for that specific run]

User: Create a run in "sandbox" workspace with auto-apply enabled
Claude: [Creates a run with auto_apply=True to automatically apply after planning]

User: List all runs in my "production" workspace
Claude: [Lists all runs in the workspace with details]

User: Show me runs in "example-org" that have errored in the last month
Claude: [Lists runs with error status in the organization]

User: Find all destroy plan runs in my organization
Claude: [Lists runs with is_destroy=true across all workspaces]

User: Get details for run ID "run-CZcmD7eagjhyX0vN"
Claude: [Shows detailed information about the specific run]
```

### Run Actions

```
User: Apply the pending run for "staging" workspace
Claude: [Uses apply_run to apply the waiting run]

User: Cancel the run "run-CZcmD7eagjhyX0vN", it's taking too long
Claude: [Uses cancel_run to safely interrupt the running process]

User: Discard the plan for the "dev" workspace, those changes aren't needed
Claude: [Uses discard_run to discard the pending run]

User: Force cancel the stuck run in "production"
Claude: [Uses force_cancel_run to immediately terminate the stuck run]

User: I need to execute this run immediately, force execute it
Claude: [Uses force_execute_run to bypass the queue and start the run]
```

### Coming Soon

```
User: List all variables defined in "production"
Claude: [Will use list_workspace_variables tool]

User: Show me the plan output and explain the changes
Claude: [Will use get_plan_output and explain_plan tools]
```

## Development

### Requirements

- Python 3.12+
- MCP (includes FastMCP and development tools)
- uv package manager (recommended) or pip
- Terraform Cloud API token

### Type Checking

This project uses mypy for static type checking to enhance code quality and catch type-related bugs early:

```bash
# Install mypy
uv pip install mypy

# Run type checking
uv run -m mypy .
```

Type checking configuration is available in both `pyproject.toml` and `mypy.ini`. The configuration enforces strict typing rules including:

- Disallowing untyped definitions
- Warning on returning Any types
- Checking completeness of function definitions
- Namespace packages support
- Module-specific configurations

### Project Structure

The code is organized into a modular structure:

```
terraform-cloud-mcp/
├── api/              # API client and communication
│   ├── __init__.py
│   └── client.py     # HTTP client for Terraform Cloud API
├── models/           # Data models
│   ├── __init__.py
│   └── auth.py       # Authentication models
├── tools/            # MCP tools implementation
│   ├── __init__.py
│   ├── auth.py       # Authentication tools
│   ├── runs.py       # Run management tools (create, list, apply, discard, cancel runs)
│   └── workspaces.py # Workspace management tools
├── utils/            # Utility functions
│   ├── __init__.py
│   └── validators.py # Input validation
├── server.py         # Main server entry point
├── pyproject.toml    # Project configuration and dependencies
├── mypy.ini          # Mypy type checking configuration
├── RELEASE_NOTES.md  # Version history and changes
└── uv.lock          # Dependency lock file for uv
```

### Extending the Server

To add new features:
1. Add new tools to the appropriate module in the `tools` directory
2. Register new tools in `server.py`
3. Follow the existing patterns for parameter validation and error handling
4. Update documentation in README.md
5. Add tests for new functionality

## Troubleshooting

If you encounter issues:

1. Check server logs (debug logging is enabled by default)
2. Note that `Processing request of type CallToolRequest` is informational, not an error
3. Debug logging is already enabled in server.py:

```python
# Already in server.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

4. If using `mcp dev server.py`, the MCP Inspector will automatically open at http://localhost:5173 for debugging
5. Use the server logs to debug API calls and responses

## Contributing

Contributions are welcome! Please open an issue or pull request if you'd like to contribute to this project.

When contributing, please follow these guidelines:
- Ensure all code includes proper type hints
- Run mypy type checking before submitting PRs
- Follow the code style guidelines in CLAUDE.md
- Add tests for new functionality
- Update documentation for any new features or changes
- Add entries to RELEASE_NOTES.md for significant changes