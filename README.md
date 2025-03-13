# Terraform Cloud MCP Server

A Model Context Protocol server implementation using FastMCP that provides Terraform Cloud API integration capabilities to Claude.

## Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Starting the Server

```bash
# Run in foreground (basic)
python server.py

# Run with Terraform Cloud API token via command line
python server.py --token YOUR_TF_TOKEN
# Or with short option
python server.py -t YOUR_TF_TOKEN

# Run with Terraform Cloud API token via environment variable
export TFC_TOKEN=YOUR_TF_TOKEN
python server.py

# Run in background with token
python server.py --token YOUR_TF_TOKEN > server.log 2>&1 & echo $! > server.pid
# Or with environment variable
export TFC_TOKEN=YOUR_TF_TOKEN
python server.py > server.log 2>&1 & echo $! > server.pid
```

The server checks for the token in the following order:
1. `TFC_TOKEN` environment variable
2. `--token` or `-t` command line argument

When you provide a token via either method, the MCP tools can be used without explicitly passing the token each time. Organization names are always required as arguments since users may work with multiple organizations.

### Available Endpoints

Currently, this MCP server provides the following functionality:

- **Resource**: `data://info` - Returns basic server information

- **Authentication Tools**:
  - `validate_token()` - Validates the provided Terraform Cloud API token
  - `get_terraform_user_info()` - Retrieves user information using the provided token

- **Workspace Management Tools**:
  - `list_workspaces(organization, page_number=1, page_size=20, all_pages=False, search_name=None, search_tags=None, search_exclude_tags=None, search_wildcard_name=None, sort=None, filter_project_id=None, filter_current_run_status=None, filter_tagged_key=None, filter_tagged_value=None)` - Lists workspaces in a specific organization with comprehensive filtering, sorting, and pagination options
  - `get_workspace_details(organization, workspace_name)` - Gets detailed information about a specific workspace

The full set of Terraform Cloud API integrations is under development. See the [TASKS.md](./TASKS.md) file for the implementation roadmap.

### Connecting with Claude

#### Using Claude Desktop

1. Open Claude Desktop
2. Go to Settings → MCP Servers
3. Add a new MCP server with the local URL (default: http://localhost:8000)
4. Enable the server
5. Use Claude normally, and it will have access to your server's resources, tools, and prompts

#### Using Claude Code CLI

```bash
# From the project root directory (basic)
claude mcp add terraform-cloud-mcp "$(pwd)/server.py"

# Start server with token via command line and connect Claude Code in one command
claude mcp add terraform-cloud-mcp "$(pwd)/server.py --token YOUR_TF_TOKEN"

# Start server with token via environment variable
claude mcp add terraform-cloud-mcp -e TFC_TOKEN=YOUR_TF_TOKEN -- "$(pwd)/server.py"

# From any other directory, specify the full path
claude mcp add terraform-cloud-mcp "/path/to/terraform-cloud-mcp/server.py --token YOUR_TF_TOKEN"
# Or with environment variable
claude mcp add terraform-cloud-mcp -e TFC_TOKEN=YOUR_TF_TOKEN -- "/path/to/terraform-cloud-mcp/server.py"
```

To verify the server was added:
```bash
claude mcp list
```

The token can be provided either through the `--token` command line argument or the `TFC_TOKEN` environment variable when starting the server. This allows you to use the default token in your Claude conversations without explicitly providing it each time.

### Example Usage in Claude

```
# If server was started without a token (neither environment variable nor command line)
User: Can you validate this Terraform Cloud API token: my-tf-token-value
Claude: [Uses validate_token and returns validation result]

User: Can you list all my workspaces in the "example-org" Terraform Cloud organization using token: my-tf-token-value
Claude: [Uses list_workspaces tool and returns workspace list]

User: Can you get details for workspace "production" in organization "example-org" using token: my-tf-token-value?
Claude: [Uses get_workspace_details tool and returns workspace information]

# If server was started with a token (via TFC_TOKEN environment variable or --token command line)
User: Can you validate my Terraform Cloud API token?
Claude: [Uses validate_token with default token and returns validation result]

User: Can you list all my workspaces in the "example-org" Terraform Cloud organization
Claude: [Uses list_workspaces with default token but explicit organization]

User: Can you find all workspaces in "example-org" with names that contain "prod"
Claude: [Uses list_workspaces with search_wildcard_name="*prod*"]

User: Can you list all workspaces in "example-org" that have the "environment:production" tag?
Claude: [Uses list_workspaces with filter_tagged_key="environment" and filter_tagged_value="production"]

User: Can you get details for the "production" workspace in the "example-org" organization?
Claude: [Uses get_workspace_details with default token but explicit organization and workspace]
```

Future examples (planned implementation):
```
User: Can you create a plan for my "production" workspace and explain what changes will be made?
Claude: [Will use create_run tool to generate a plan and explain_plan tool to provide a human-readable summary]
```

## Development

### Extending the Server

To extend this server, modify `server.py` to add more resources, tools, and prompts.

### Terraform Cloud API Integration

This project aims to implement comprehensive Terraform Cloud API integration through MCP tools. The implementation roadmap is outlined in [TASKS.md](./TASKS.md).

Key features planned:
- Workspace management
- Run operations (plan/apply)
- State management
- Variable management
- Organization management
- Plan parsing and explanation

### Requirements

- Python 3.9+
- FastMCP
- Terraform Cloud API token (for accessing Terraform Cloud resources)

### Contributing

Contributions are welcome! Please see the [TASKS.md](./TASKS.md) file for areas that need implementation.

## Troubleshooting

### Debugging Server Issues

If you encounter errors or unexpected behavior:

1. Check the server logs - Debug logging is enabled by default
2. The log message `Processing request of type CallToolRequest` is informational, not an error
3. If you need more detailed logging, you can adjust the logging level in `server.py`

```python
# For even more verbose logging:
import logging
logging.basicConfig(level=logging.DEBUG)
```