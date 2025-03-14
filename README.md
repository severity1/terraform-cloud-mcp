# Terraform Cloud MCP Server

A Model Context Protocol (MCP) server that integrates Claude with the Terraform Cloud API, allowing Claude to manage your Terraform infrastructure through natural conversation.

## Features

- **Authentication** - Validate tokens and get user information
- **Workspace Management** - Create, read, update, delete, lock/unlock workspaces
- **Future Features** - Run operations, state management, variables management, and more

## Quick Start

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/terraform-cloud-mcp.git
cd terraform-cloud-mcp

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Starting the Server

The server supports multiple ways to provide your Terraform Cloud API token:

```bash
# Basic usage (no token)
python server.py

# With token via environment variable
export TFC_TOKEN=YOUR_TF_TOKEN
python server.py

# Using a .env file
echo "TFC_TOKEN=YOUR_TF_TOKEN" > .env
python server.py

# Run in background
python server.py > server.log 2>&1 & echo $! > server.pid
```

When a token is provided, Claude can use it without you having to specify it in every command.

### Connecting with Claude

#### Using Claude Desktop

1. Open Claude Desktop
2. Go to Settings → MCP Servers
3. Add a new server with URL: http://localhost:8000
4. Enable the server
5. Start chatting with Claude

#### Using Claude Code CLI

```bash
# Add the MCP server
claude mcp add terraform-cloud-mcp "$(pwd)/server.py"

# With token
claude mcp add terraform-cloud-mcp -e TFC_TOKEN=YOUR_TF_TOKEN -- "$(pwd)/server.py"

# Verify it was added
claude mcp list
```

## Available Tools

### Authentication Tools

| Tool | Description | Arguments |
|------|-------------|-----------|
| `validate_token()` | Validates a Terraform Cloud API token | None - Uses default token |
| `get_terraform_user_info()` | Gets user information for the provided token | None - Uses default token |

### Workspace Management Tools

#### List & Search

| Tool | Description | Arguments |
|------|-------------|-----------|
| `list_workspaces()` | List workspaces with comprehensive filtering | • `organization`: Organization name (required)<br>• `page_number`: Page number (default: 1)<br>• `page_size`: Results per page (default: 20)<br>• `all_pages`: Fetch all pages (default: False)<br>• `search_name`: Filter by name (fuzzy)<br>• `search_tags`: Filter by tags (comma separated)<br>• `search_exclude_tags`: Exclude tags (comma separated)<br>• `search_wildcard_name`: Filter by wildcard name<br>• `sort`: Sort field and direction<br>• `filter_project_id`: Filter by project ID<br>• `filter_current_run_status`: Filter by run status<br>• `filter_tagged_key`: Filter by tag key<br>• `filter_tagged_value`: Filter by tag value |
| `get_workspace_details()` | Get detailed workspace information | • `organization`: Organization name (required)<br>• `workspace_name`: Workspace name (required) |

#### Create & Update

| Tool | Description | Arguments |
|------|-------------|-----------|
| `create_workspace()` | Create a new workspace | • `organization`: Organization name (required)<br>• `name`: Workspace name (required)<br>• `description`: Workspace description<br>• `terraform_version`: Terraform version<br>• `working_directory`: Working directory<br>• `auto_apply`: Auto apply changes (default: False)<br>• `file_triggers_enabled`: Enable file triggers (default: True)<br>• `trigger_prefixes`: Path prefixes to trigger runs<br>• `trigger_patterns`: Glob patterns to trigger runs<br>• `queue_all_runs`: Queue all runs (default: False)<br>• `speculative_enabled`: Enable speculative plans (default: True)<br>• `global_remote_state`: Allow global state access (default: False)<br>• `execution_mode`: Execution mode (default: "remote")<br>• `allow_destroy_plan`: Allow destroy plans (default: True)<br>• `auto_apply_run_trigger`: Auto apply run triggers (default: False)<br>• `project_id`: Project ID<br>• `vcs_repo`: VCS repository settings<br>• `tags`: List of tags |
| `update_workspace()` | Update an existing workspace | • `organization`: Organization name (required)<br>• `workspace_name`: Current workspace name (required)<br>• `name`: New workspace name<br>• `description`: Workspace description<br>• `terraform_version`: Terraform version<br>• `working_directory`: Working directory<br>• `auto_apply`: Auto apply changes<br>• `file_triggers_enabled`: Enable file triggers<br>• `trigger_prefixes`: Path prefixes to trigger runs<br>• `trigger_patterns`: Glob patterns to trigger runs<br>• `queue_all_runs`: Queue all runs<br>• `speculative_enabled`: Enable speculative plans<br>• `global_remote_state`: Allow global state access<br>• `execution_mode`: Execution mode<br>• `allow_destroy_plan`: Allow destroy plans<br>• `auto_apply_run_trigger`: Auto apply run triggers<br>• `project_id`: Project ID<br>• `vcs_repo`: VCS repository settings<br>• `tags`: List of tags |

#### Delete

| Tool | Description | Arguments |
|------|-------------|-----------|
| `delete_workspace()` | Delete a workspace | • `organization`: Organization name (required)<br>• `workspace_name`: Workspace name (required) |
| `safe_delete_workspace()` | Delete only if not managing resources | • `organization`: Organization name (required)<br>• `workspace_name`: Workspace name (required) |

#### Lock & Unlock

| Tool | Description | Arguments |
|------|-------------|-----------|
| `lock_workspace()` | Lock a workspace | • `organization`: Organization name (required)<br>• `workspace_name`: Workspace name (required)<br>• `reason`: Reason for locking (optional) |
| `unlock_workspace()` | Unlock a workspace | • `organization`: Organization name (required)<br>• `workspace_name`: Workspace name (required) |
| `force_unlock_workspace()` | Force unlock a workspace | • `organization`: Organization name (required)<br>• `workspace_name`: Workspace name (required) |

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

### Coming Soon

```
User: Create a plan for my "production" workspace and explain the changes
Claude: [Will use create_run and explain_plan tools]

User: Apply the pending run for "staging" workspace
Claude: [Will use apply_run tool]

User: List all variables defined in "production"
Claude: [Will use list_workspace_variables tool]
```

## Development

### Requirements

- Python 3.9+
- FastMCP
- Terraform Cloud API token

### Extending the Server

To add new features:
1. Edit `server.py` to implement additional tools or resources
2. Follow the existing patterns for parameter validation and error handling
3. Update documentation in README.md
4. Add tests for new functionality

## Troubleshooting

If you encounter issues:

1. Check server logs (debug logging is enabled by default)
2. Note that `Processing request of type CallToolRequest` is informational, not an error
3. For more verbose logging:

```python
# Add to server.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

Contributions are welcome! Please open an issue or pull request if you'd like to contribute to this project.