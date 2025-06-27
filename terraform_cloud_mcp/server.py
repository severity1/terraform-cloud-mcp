#!/usr/bin/env python3
"""
Terraform Cloud MCP Server
"""
import logging
from dotenv import load_dotenv
from fastmcp import FastMCP

# Import tools and models
from terraform_cloud_mcp.tools import account
from terraform_cloud_mcp.tools import workspaces
from terraform_cloud_mcp.tools import runs
from terraform_cloud_mcp.tools import organizations
from terraform_cloud_mcp.tools import plans
from terraform_cloud_mcp.tools import applies
from terraform_cloud_mcp.tools import projects
from terraform_cloud_mcp.tools import cost_estimates
from terraform_cloud_mcp.tools import assessment_results
from terraform_cloud_mcp.tools import state_versions
from terraform_cloud_mcp.tools import state_version_outputs

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create server instance
mcp: FastMCP = FastMCP("Terraform Cloud MCP Server")

# Register account management tools
mcp.tool()(account.get_account_details)

# Register workspace management tools
mcp.tool()(workspaces.list_workspaces)
mcp.tool()(workspaces.get_workspace_details)
mcp.tool()(workspaces.create_workspace)
mcp.tool()(workspaces.update_workspace)
mcp.tool(enabled=False)(workspaces.delete_workspace)  # Disabled for safety
mcp.tool(enabled=False)(workspaces.safe_delete_workspace)  # Disabled for safety
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
mcp.tool(enabled=False)(organizations.delete_organization)  # Disabled for safety

# Register plan management tools
mcp.tool()(plans.get_plan_details)
mcp.tool()(plans.get_plan_json_output)
mcp.tool()(plans.get_run_plan_json_output)
mcp.tool()(plans.get_plan_logs)

# Register apply management tools
mcp.tool()(applies.get_apply_details)
mcp.tool()(applies.get_errored_state)
mcp.tool()(applies.get_apply_logs)

# Register project management tools
mcp.tool()(projects.create_project)
mcp.tool()(projects.update_project)
mcp.tool()(projects.list_projects)
mcp.tool()(projects.get_project_details)
mcp.tool(enabled=False)(projects.delete_project)  # Disabled for safety
mcp.tool()(projects.list_project_tag_bindings)
mcp.tool()(projects.add_update_project_tag_bindings)
mcp.tool()(projects.move_workspaces_to_project)

# Register cost estimates tools
mcp.tool()(cost_estimates.get_cost_estimate_details)

# Register assessment results tools
mcp.tool()(assessment_results.get_assessment_result_details)
mcp.tool()(assessment_results.get_assessment_json_output)
mcp.tool()(assessment_results.get_assessment_json_schema)
mcp.tool()(assessment_results.get_assessment_log_output)

# Register state version tools
mcp.tool()(state_versions.list_state_versions)
mcp.tool()(state_versions.get_current_state_version)
mcp.tool()(state_versions.get_state_version)
mcp.tool()(state_versions.create_state_version)
mcp.tool()(state_versions.download_state_file)

# Register state version outputs tools
mcp.tool()(state_version_outputs.list_state_version_outputs)
mcp.tool()(state_version_outputs.get_state_version_output)


def main() -> None:
    """Run the Terraform Cloud MCP server."""

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
