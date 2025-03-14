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

# Run with Terraform Cloud API token via environment variable
export TFC_TOKEN=YOUR_TF_TOKEN
python server.py

# Run in background with environment variable
export TFC_TOKEN=YOUR_TF_TOKEN
python server.py > server.log 2>&1 & echo $! > server.pid

# Using a .env file
# Create a .env file with TFC_TOKEN=YOUR_TF_TOKEN
python server.py
```

The server uses the `TFC_TOKEN` environment variable for authentication. This can be set directly or through a `.env` file.

When you provide a token via either method, the MCP tools can be used without explicitly passing the token each time. Organization names are always required as arguments since users may work with multiple organizations.

### Available Endpoints

Currently, this MCP server provides the following functionality:

- **Resource**: `data://info` - Returns basic server information

- **Authentication Tools**:
  - `validate_token()` - Validates the provided Terraform Cloud API token
  - `get_terraform_user_info()` - Retrieves user information using the provided token

- **Workspace Management Tools**:
  - `list_workspaces(organization, page_number=1, page_size=20, all_pages=False, search_name="", search_tags="", search_exclude_tags="", search_wildcard_name="", sort="", filter_project_id="", filter_current_run_status="", filter_tagged_key="", filter_tagged_value="")` - Lists workspaces in a specific organization with comprehensive filtering, sorting, and pagination options
  - `get_workspace_details(organization, workspace_name)` - Gets detailed information about a specific workspace
  - `create_workspace(organization, name, description="", terraform_version="", working_directory="", auto_apply=False, file_triggers_enabled=True, trigger_prefixes=[], trigger_patterns=[], queue_all_runs=False, speculative_enabled=True, global_remote_state=False, execution_mode="remote", allow_destroy_plan=True, auto_apply_run_trigger=False, project_id="", vcs_repo={}, tags=[])` - Creates a new workspace with many configurable options
  - `update_workspace(organization, workspace_name, name="", description="", terraform_version="", working_directory="", auto_apply=None, file_triggers_enabled=None, trigger_prefixes=[], trigger_patterns=[], queue_all_runs=None, speculative_enabled=None, global_remote_state=None, execution_mode="", allow_destroy_plan=None, auto_apply_run_trigger=None, project_id="", vcs_repo={}, tags=[])` - Updates an existing workspace with configurable options
  - `delete_workspace(organization, workspace_name)` - Deletes a workspace from an organization
  - `safe_delete_workspace(organization, workspace_name)` - Safely deletes a workspace only if it's not managing any resources
  - `lock_workspace(organization, workspace_name, reason="")` - Locks a workspace to prevent Terraform runs
  - `unlock_workspace(organization, workspace_name)` - Unlocks a workspace to allow Terraform runs
  - `force_unlock_workspace(organization, workspace_name)` - Force unlocks a workspace that may be locked by another user or process

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

# Start server with token via environment variable
claude mcp add terraform-cloud-mcp -e TFC_TOKEN=YOUR_TF_TOKEN -- "$(pwd)/server.py"

# From any other directory, specify the full path
claude mcp add terraform-cloud-mcp -e TFC_TOKEN=YOUR_TF_TOKEN -- "/path/to/terraform-cloud-mcp/server.py"
```

To verify the server was added:
```bash
claude mcp list
```

The token can be provided through the `TFC_TOKEN` environment variable when starting the server. This allows you to use the default token in your Claude conversations without explicitly providing it each time.

### Example Usage in Claude

```
# If server was started without a token
User: Can you validate this Terraform Cloud API token: my-tf-token-value
Claude: [Uses validate_token and returns validation result]

User: Can you list all my workspaces in the "example-org" Terraform Cloud organization using token: my-tf-token-value
Claude: [Uses list_workspaces tool and returns workspace list]

User: Can you get details for workspace "production" in organization "example-org" using token: my-tf-token-value?
Claude: [Uses get_workspace_details tool and returns workspace information]

# If server was started with a token (via TFC_TOKEN environment variable)
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
User: Can you create a new workspace in "example-org" called "staging" with auto-apply enabled?
Claude: [Uses create_workspace tool to create a new workspace with auto_apply=True]

User: Can you update my "staging" workspace in "example-org" to use a specific Terraform version?
Claude: [Uses update_workspace tool to update the workspace with a specific terraform_version]

User: Can you delete my "dev-test" workspace in the "example-org" organization?
Claude: [Uses delete_workspace tool to delete the specified workspace]

User: I want to delete my "staging" workspace in "example-org" but only if it doesn't have any resources. Can you help with that?
Claude: [Uses safe_delete_workspace tool to safely delete the workspace only if it has no resources]

User: Can you lock my "production" workspace so no changes can be applied while we're doing maintenance?
Claude: [Uses lock_workspace tool with a reason to lock the workspace]

User: The maintenance is complete, can you unlock the "production" workspace now?
Claude: [Uses unlock_workspace tool to unlock the workspace]

User: Someone left the "staging" workspace locked, and they're out today. Can you force unlock it?
Claude: [Uses force_unlock_workspace tool to force unlock the workspace]

User: Can you create a plan for my "production" workspace and explain what changes will be made?
Claude: [Will use create_run tool to generate a plan and explain_plan tool to provide a human-readable summary when implemented]
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