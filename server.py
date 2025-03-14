#!/usr/bin/env python3
"""
Terraform Cloud MCP Server
"""
import logging
import os
import argparse
import sys
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Import tools and models
from api.client import TERRAFORM_CLOUD_API_URL
import tools.auth as auth
import tools.workspaces as workspaces
import tools.runs as runs

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create server instance
mcp = FastMCP("Terraform Cloud MCP Server")

# Register authentication tools
mcp.tool()(auth.validate_token)
mcp.tool()(auth.get_terraform_user_info)

# Register workspace management tools
mcp.tool()(workspaces.list_workspaces)
mcp.tool()(workspaces.get_workspace_details)
mcp.tool()(workspaces.create_workspace)
mcp.tool()(workspaces.update_workspace)
mcp.tool()(workspaces.delete_workspace)
mcp.tool()(workspaces.safe_delete_workspace)
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

# Start server when run directly
if __name__ == "__main__":
    mcp.run()