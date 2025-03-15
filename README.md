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
│   └── workspaces.py # Workspace management tools
├── utils/            # Utility functions
│   ├── __init__.py
│   └── validators.py # Input validation
├── server.py         # Main server entry point
└── requirements.txt  # Project dependencies
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
3. For more verbose logging:

```python
# Add to server.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

Contributions are welcome! Please open an issue or pull request if you'd like to contribute to this project.