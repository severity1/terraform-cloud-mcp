#!/usr/bin/env python3
"""
Terraform Cloud MCP Server
"""
import logging
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Import tools and models
from terraform_cloud_mcp.tools import account
from terraform_cloud_mcp.tools import workspaces
from terraform_cloud_mcp.tools import runs
from terraform_cloud_mcp.tools import organizations
from terraform_cloud_mcp.tools import plans
from terraform_cloud_mcp.tools import applies

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create server instance
mcp = FastMCP("Terraform Cloud MCP Server")

# Register account management tools
mcp.tool()(account.get_account_details)

# Register workspace management tools
mcp.tool()(workspaces.list_workspaces)
mcp.tool()(workspaces.get_workspace_details)
mcp.tool()(workspaces.create_workspace)
mcp.tool()(workspaces.update_workspace)
mcp.tool()(workspaces.delete_workspace)  # Uses confirm=False pattern
mcp.tool()(workspaces.safe_delete_workspace)  # Uses confirm=False pattern
mcp.tool()(workspaces.lock_workspace)
mcp.tool()(workspaces.unlock_workspace)
mcp.tool()(workspaces.force_unlock_workspace)

# Register run management tools
mcp.tool()(runs.create_run)
mcp.tool()(runs.list_runs_in_workspace)
mcp.tool()(runs.list_runs_in_organization)
mcp.tool()(runs.get_run_details)
mcp.tool()(runs.apply_run)
mcp.tool()(runs.discard_run)
mcp.tool()(runs.cancel_run)
mcp.tool()(runs.force_cancel_run)
mcp.tool()(runs.force_execute_run)

# Register organization management tools
mcp.tool()(organizations.get_organization_details)
mcp.tool()(organizations.get_organization_entitlements)
mcp.tool()(organizations.list_organizations)
mcp.tool()(organizations.create_organization)
mcp.tool()(organizations.update_organization)
mcp.tool()(organizations.delete_organization)

# Register plan management tools
mcp.tool()(plans.get_plan_details)
mcp.tool()(plans.get_plan_json_output)
mcp.tool()(plans.get_run_plan_json_output)

# Register apply management tools
mcp.tool()(applies.get_apply_details)
mcp.tool()(applies.get_errored_state)


def main() -> None:
    """Run the Terraform Cloud MCP server."""

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
