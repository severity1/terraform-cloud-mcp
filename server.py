#!/usr/bin/env python3
"""
Terraform Cloud MCP Server
"""
import logging
import os
import argparse
import sys
import re
from dataclasses import dataclass
from typing import Optional, Dict, Tuple
import httpx

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Parse command line arguments
parser = argparse.ArgumentParser(description='Terraform Cloud MCP Server')
args = parser.parse_args()

# Store default token from environment variable
# Security note: API tokens are sensitive data and should never be logged or exposed
DEFAULT_TOKEN = os.getenv("TFC_TOKEN")

if DEFAULT_TOKEN:
    logging.info("Default token provided (masked for security)")

# Create server instance
mcp = FastMCP("Terraform Cloud MCP Server")

# We'll use user-provided tokens directly in each request

# Constants
TERRAFORM_CLOUD_API_URL = "https://app.terraform.io/api/v2"

# Validation patterns
# Organization names must be lowercase alphanumeric with hyphens allowed, minimum 3 chars, maximum 60 chars
ORGANIZATION_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,58}[a-z0-9]$")

def validate_organization(organization: str) -> Tuple[bool, str]:
    """
    Validate organization name format according to Terraform Cloud rules
    
    Args:
        organization: Organization name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not organization:
        return (False, "Organization name is required")
        
    if not isinstance(organization, str):
        return (False, "Organization name must be a string")
        
    if not ORGANIZATION_NAME_PATTERN.match(organization):
        return (False, "Organization name must be lowercase alphanumeric with hyphens allowed, minimum 3 chars, maximum 60 chars")
        
    return (True, "")

async def make_api_request(path: str, method: str = "GET", token: Optional[str] = None, params: dict = {}, data: dict = {}) -> Tuple[bool, dict]:
    """
    Make a request to the Terraform Cloud API
    
    Args:
        path: API path to request (without base URL)
        method: HTTP method (default: GET)
        token: API token (defaults to DEFAULT_TOKEN)
        params: Query parameters for the request (optional)
        data: JSON data for POST/PATCH requests (optional)
        
    Returns:
        Tuple of (success, data) where data is either the response JSON or an error dict
    """
    if not token:
        token = DEFAULT_TOKEN
        
    if not token:
        return (False, {"error": "Token is required. Please set the TFC_TOKEN environment variable."})
    
    try:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/vnd.api+json"}
        
        async with httpx.AsyncClient() as client:
            url = f"{TERRAFORM_CLOUD_API_URL}/{path}"
            
            if method == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method == "POST":
                response = await client.post(url, headers=headers, params=params, json=data)
            elif method == "PATCH":
                response = await client.patch(url, headers=headers, params=params, json=data)
            elif method == "DELETE":
                response = await client.delete(url, headers=headers, params=params)
            else:
                return (False, {"error": f"Unsupported method: {method}"})
            
            # Handle different success response codes
            if response.status_code in [200, 201, 202, 204]:
                if response.status_code == 204:  # No content
                    return (True, {"status": "success"})
                try:
                    return (True, response.json())
                except ValueError:
                    return (True, {"status": "success", "raw_response": response.text})
            else:
                error_message = f"API request failed: {response.status_code}"
                try:
                    error_data = response.json()
                    return (False, {"error": error_message, "details": error_data})
                except ValueError:
                    return (False, {"error": error_message})
    except Exception as e:
        # Ensure no sensitive data is included in error messages
        error_message = str(e)
        if token and token in error_message:
            error_message = error_message.replace(token, "[REDACTED]")
        return (False, {"error": f"Request error: {error_message}"})

@dataclass
class AuthResult:
    """Result of an authentication operation"""
    success: bool
    message: str
    user_name: Optional[str] = None

# Define a simple resource
@mcp.resource("data://info")
def get_info():
    """Get basic server information"""
    return {
        "name": "Terraform Cloud MCP Server", 
        "status": "active",
        "api_url": TERRAFORM_CLOUD_API_URL
    }
    
# Authentication tools
@mcp.tool()
async def validate_token() -> AuthResult:
    """
    Validate a Terraform Cloud API token
        
    Returns:
        AuthResult containing success status and message
    """
    
    success, data = await make_api_request("account/details")
    
    if success:
        user_name = data.get("data", {}).get("attributes", {}).get("username")
        return AuthResult(True, f"Token validated successfully for user: {user_name}", user_name)
    else:
        return AuthResult(False, data.get("error", "Unknown error validating token"))
    
@mcp.tool()
async def get_terraform_user_info() -> dict:
    """
    Get user information for a Terraform Cloud API token
    
    Returns:
        User information from Terraform Cloud
    """
    
    success, data = await make_api_request("account/details")
    
    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary

# Workspace management tools
@mcp.tool()
async def list_workspaces(
    organization: str, 
    page_number: int = 1, 
    page_size: int = 20, 
    all_pages: bool = False, 
    search_name: str = "", 
    search_tags: str = "",
    search_exclude_tags: str = "",
    search_wildcard_name: str = "",
    sort: str = "",
    filter_project_id: str = "",
    filter_current_run_status: str = "",
    filter_tagged_key: str = "",
    filter_tagged_value: str = ""
) -> dict:
    """
    List workspaces in an organization with comprehensive filtering and pagination
    
    Args:
        organization: The organization name (required)
        page_number: Page number to fetch (default: 1)
        page_size: Number of results per page (default: 20, max: 100)
        all_pages: If True, fetch all pages and combine results (default: False)
        search_name: Filter workspaces by name using fuzzy search
        search_tags: Filter workspaces with specific tags (comma separated)
        search_exclude_tags: Exclude workspaces with specific tags (comma separated)
        search_wildcard_name: Filter workspaces by name with wildcard matching (e.g., "prod-*", "*-test")
        sort: Sort workspaces by "name", "current-run.created-at", or "latest-change-at" (prefix with "-" for descending)
        filter_project_id: Filter workspaces belonging to a specific project
        filter_current_run_status: Filter workspaces by current run status
        filter_tagged_key: Filter workspaces by tag key
        filter_tagged_value: Filter workspaces by tag value (used with filter_tagged_key)

    Returns:
        List of workspaces with pagination information
    """
    
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}
        
    # Validate pagination parameters
    if page_number < 1:
        return {"error": "Page number must be at least 1"}
    
    if page_size < 1 or page_size > 100:
        return {"error": "Page size must be between 1 and 100"}
    
    # Build query parameters
    params = {
        "page[number]": str(page_number),
        "page[size]": str(page_size)
    }
    
    # Add optional search and filter parameters
    if search_name:
        params["search[name]"] = search_name
    
    if search_tags:
        params["search[tags]"] = search_tags
    
    if search_exclude_tags:
        params["search[exclude-tags]"] = search_exclude_tags
    
    if search_wildcard_name:
        params["search[wildcard-name]"] = search_wildcard_name
    
    if sort:
        params["sort"] = sort
    
    if filter_project_id:
        params["filter[project][id]"] = filter_project_id
    
    if filter_current_run_status:
        params["filter[current-run][status]"] = filter_current_run_status
    
    if filter_tagged_key:
        params["filter[tagged][0][key]"] = filter_tagged_key
        if filter_tagged_value:
            params["filter[tagged][0][value]"] = filter_tagged_value
    
    # For all_pages mode, we'll start collecting all results
    if all_pages:
        all_workspaces = {"data": []}
        current_page = 1
        
        while True:
            params["page[number]"] = str(current_page)
            
            success, page_data = await make_api_request(
                f"organizations/{organization}/workspaces", 
                params=params
            )
            
            if not success:
                return page_data  # Return error info
                
            # Add this page's workspaces to our collection
            all_workspaces["data"].extend(page_data.get("data", []))
            
            # Check if there's a next page
            meta = page_data.get("meta", {})
            pagination = meta.get("pagination", {})
            current_page = pagination.get("current-page", 1)
            total_pages = pagination.get("total-pages", 1)
            
            # Add pagination metadata
            if "meta" not in all_workspaces:
                all_workspaces["meta"] = meta
                
            # If we're on the last page, stop
            if current_page >= total_pages:
                break
                
            # Otherwise, continue to the next page
            current_page += 1
        
        # Update the pagination info in the response
        if "meta" in all_workspaces:
            meta = all_workspaces["meta"]
            if isinstance(meta, dict) and "pagination" in meta:
                pagination = meta["pagination"]
                if isinstance(pagination, dict):
                    pagination["current-page"] = 1
                    pagination["prev-page"] = None
                    pagination["next-page"] = None
            
        return all_workspaces
    
    # Standard single-page mode
    else:
        success, data = await make_api_request(
            f"organizations/{organization}/workspaces", 
            params=params
        )
        
        if success:
            return data
        else:
            return data  # Error info is already in the data dictionary

@mcp.tool()
async def get_workspace_details(organization: str, workspace_name: str) -> dict:
    """
    Get details for a specific workspace
    
    Args:
        organization: The organization name (required)
        workspace_name: The workspace name (required)
        
    Returns:
        Workspace details
    """
    
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}
    
    if not workspace_name:
        return {"error": "Workspace name is required"}
    
    success, data = await make_api_request(f"organizations/{organization}/workspaces/{workspace_name}")
    
    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary

@mcp.tool()
async def create_workspace(
    organization: str, 
    name: str,
    description: str = "",
    terraform_version: str = "",
    working_directory: str = "",
    auto_apply: bool = False,
    file_triggers_enabled: bool = True,
    trigger_prefixes: list = [],
    trigger_patterns: list = [],
    queue_all_runs: bool = False,
    speculative_enabled: bool = True,
    global_remote_state: bool = False,
    execution_mode: str = "remote",
    allow_destroy_plan: bool = True,
    auto_apply_run_trigger: bool = False,
    project_id: str = "",
    vcs_repo: dict = {},
    tags: list = []
) -> dict:
    """
    Create a new workspace in an organization
    
    Args:
        organization: The organization name (required)
        name: The name of the workspace (required)
        description: A description for the workspace
        terraform_version: Specific Terraform version to use (default: latest)
        working_directory: Relative path that Terraform will execute within
        auto_apply: Automatically apply changes when a Terraform plan is successful
        file_triggers_enabled: Whether to filter runs based on changed files in VCS
        trigger_prefixes: List of path prefixes that will trigger runs
        trigger_patterns: List of glob patterns that Terraform monitors for changes
        queue_all_runs: Whether runs should be queued immediately after workspace creation
        speculative_enabled: Whether this workspace allows automatic speculative plans
        global_remote_state: Whether all workspaces in the organization can access this workspace's state
        execution_mode: Which execution mode to use: "remote", "local", or "agent"
        allow_destroy_plan: Whether destroy plans can be queued on the workspace
        auto_apply_run_trigger: Whether to automatically apply changes from run triggers
        project_id: The ID of the project to create the workspace in
        vcs_repo: Settings for the workspace's VCS repository (optional)
        tags: List of tags to attach to the workspace
        
    Returns:
        The created workspace details
    """
    
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}
    
    if not name:
        return {"error": "Workspace name is required"}
    
    # Build the request payload
    payload = {
        "data": {
            "type": "workspaces",
            "attributes": {
                "name": name
            }
        }
    }
    
    # Add optional attributes if provided
    if description:
        payload["data"]["attributes"]["description"] = description
    if terraform_version:
        payload["data"]["attributes"]["terraform-version"] = terraform_version
    if working_directory:
        payload["data"]["attributes"]["working-directory"] = working_directory
    
    # Add boolean attributes (only those that differ from API defaults need to be explicitly set)
    # Auto-apply defaults to false in API, so only set if true
    if auto_apply:
        payload["data"]["attributes"]["auto-apply"] = auto_apply
        
    # File-triggers-enabled defaults to true in API
    if file_triggers_enabled is False:
        payload["data"]["attributes"]["file-triggers-enabled"] = False
        
    # Queue-all-runs defaults to false in API
    if queue_all_runs:
        payload["data"]["attributes"]["queue-all-runs"] = queue_all_runs
        
    # Speculative-enabled defaults to true in API
    if speculative_enabled is False:
        payload["data"]["attributes"]["speculative-enabled"] = False
    
    # Global-remote-state defaults to false in API
    if global_remote_state:
        payload["data"]["attributes"]["global-remote-state"] = global_remote_state
        
    # Allow-destroy-plan defaults to true in API
    if allow_destroy_plan is False:
        payload["data"]["attributes"]["allow-destroy-plan"] = False
        
    # Auto-apply-run-trigger defaults to false in API
    if auto_apply_run_trigger:
        payload["data"]["attributes"]["auto-apply-run-trigger"] = auto_apply_run_trigger
    
    # Add trigger lists if provided
    if trigger_prefixes:
        payload["data"]["attributes"]["trigger-prefixes"] = trigger_prefixes
    if trigger_patterns:
        payload["data"]["attributes"]["trigger-patterns"] = trigger_patterns
    
    # Add execution mode
    if execution_mode not in ["remote", "local", "agent"]:
        return {"error": "Invalid execution mode. Must be one of: 'remote', 'local', 'agent'"}
    payload["data"]["attributes"]["execution-mode"] = execution_mode
    
    # Add VCS repository settings if provided
    if vcs_repo:
        if not isinstance(vcs_repo, dict):
            return {"error": "vcs_repo must be a dictionary"}
        payload["data"]["attributes"]["vcs-repo"] = vcs_repo
    
    # Add project relationship if provided
    if project_id:
        if "relationships" not in payload["data"]:
            payload["data"]["relationships"] = {}
        payload["data"]["relationships"]["project"] = {
            "data": {
                "id": project_id,
                "type": "projects"
            }
        }
    
    # Add tags if provided
    if tags:
        if not isinstance(tags, list):
            return {"error": "tags must be a list"}
            
        if "relationships" not in payload["data"]:
            payload["data"]["relationships"] = {}
            
        tag_bindings_data = []
        for tag in tags:
            if not isinstance(tag, dict) or "key" not in tag or "value" not in tag:
                return {"error": "Each tag must be a dictionary with 'key' and 'value' fields"}
                
            tag_bindings_data.append({
                "type": "tag-bindings",
                "attributes": {
                    "key": tag["key"],
                    "value": tag["value"]
                }
            })
            
        if tag_bindings_data:
            payload["data"]["relationships"]["tag-bindings"] = {
                "data": tag_bindings_data
            }
    
    # Make the API request
    success, data = await make_api_request(
        f"organizations/{organization}/workspaces",
        method="POST",
        data=payload
    )
    
    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary

@mcp.tool()
async def update_workspace(
    organization: str, 
    workspace_name: str,
    name: str = "",
    description: str = "",
    terraform_version: str = "",
    working_directory: str = "",
    auto_apply: Optional[bool] = None,
    file_triggers_enabled: Optional[bool] = None,
    trigger_prefixes: list = [],
    trigger_patterns: list = [],
    queue_all_runs: Optional[bool] = None,
    speculative_enabled: Optional[bool] = None,
    global_remote_state: Optional[bool] = None,
    execution_mode: str = "",
    allow_destroy_plan: Optional[bool] = None,
    auto_apply_run_trigger: Optional[bool] = None,
    project_id: str = "",
    vcs_repo: dict = {},
    tags: list = []
) -> dict:
    """
    Update an existing workspace in an organization
    
    Args:
        organization: The organization name (required)
        workspace_name: Current name of the workspace to update (required)
        name: New name for the workspace (optional)
        description: A description for the workspace
        terraform_version: Specific Terraform version to use
        working_directory: Relative path that Terraform will execute within
        auto_apply: Automatically apply changes when a Terraform plan is successful
        file_triggers_enabled: Whether to filter runs based on changed files in VCS
        trigger_prefixes: List of path prefixes that will trigger runs
        trigger_patterns: List of glob patterns that Terraform monitors for changes
        queue_all_runs: Whether runs should be queued immediately after workspace creation
        speculative_enabled: Whether this workspace allows automatic speculative plans
        global_remote_state: Whether all workspaces in the organization can access this workspace's state
        execution_mode: Which execution mode to use: "remote", "local", or "agent"
        allow_destroy_plan: Whether destroy plans can be queued on the workspace
        auto_apply_run_trigger: Whether to automatically apply changes from run triggers
        project_id: The ID of the project to move the workspace to
        vcs_repo: Settings for the workspace's VCS repository, or null to remove VCS
        tags: List of tags to attach to the workspace
        
    Returns:
        The updated workspace details
    """
    
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}
    
    if not workspace_name:
        return {"error": "Current workspace name is required"}
    
    # Build the request payload
    payload = {
        "data": {
            "type": "workspaces",
            "attributes": {}
        }
    }
    
    # Add new name if provided
    if name:
        payload["data"]["attributes"]["name"] = name
    
    # Add optional attributes if provided
    if description:
        payload["data"]["attributes"]["description"] = description
    if terraform_version:
        payload["data"]["attributes"]["terraform-version"] = terraform_version
    if working_directory:
        payload["data"]["attributes"]["working-directory"] = working_directory
    
    # Add boolean attributes if specified
    if auto_apply is not None:
        payload["data"]["attributes"]["auto-apply"] = auto_apply
    if file_triggers_enabled is not None:
        payload["data"]["attributes"]["file-triggers-enabled"] = file_triggers_enabled
    if queue_all_runs is not None:
        payload["data"]["attributes"]["queue-all-runs"] = queue_all_runs
    if speculative_enabled is not None:
        payload["data"]["attributes"]["speculative-enabled"] = speculative_enabled
    if global_remote_state is not None:
        payload["data"]["attributes"]["global-remote-state"] = global_remote_state
    if allow_destroy_plan is not None:
        payload["data"]["attributes"]["allow-destroy-plan"] = allow_destroy_plan
    if auto_apply_run_trigger is not None:
        payload["data"]["attributes"]["auto-apply-run-trigger"] = auto_apply_run_trigger
    
    # Add trigger lists if provided
    if trigger_prefixes:
        payload["data"]["attributes"]["trigger-prefixes"] = trigger_prefixes
    if trigger_patterns:
        payload["data"]["attributes"]["trigger-patterns"] = trigger_patterns
    
    # Add execution mode if provided
    if execution_mode:
        if execution_mode not in ["remote", "local", "agent"]:
            return {"error": "Invalid execution mode. Must be one of: 'remote', 'local', 'agent'"}
        payload["data"]["attributes"]["execution-mode"] = execution_mode
    
    # Add VCS repository settings if provided
    if vcs_repo is not None:
        if not isinstance(vcs_repo, dict):
            return {"error": "vcs_repo must be a dictionary or null"}
        payload["data"]["attributes"]["vcs-repo"] = vcs_repo
    
    # Add project relationship if provided
    if project_id:
        if "relationships" not in payload["data"]:
            payload["data"]["relationships"] = {}
        payload["data"]["relationships"]["project"] = {
            "data": {
                "id": project_id,
                "type": "projects"
            }
        }
    
    # Add tags if provided
    if tags:
        if not isinstance(tags, list):
            return {"error": "tags must be a list"}
            
        if "relationships" not in payload["data"]:
            payload["data"]["relationships"] = {}
            
        tag_bindings_data = []
        for tag in tags:
            if not isinstance(tag, dict) or "key" not in tag or "value" not in tag:
                return {"error": "Each tag must be a dictionary with 'key' and 'value' fields"}
                
            tag_bindings_data.append({
                "type": "tag-bindings",
                "attributes": {
                    "key": tag["key"],
                    "value": tag["value"]
                }
            })
            
        payload["data"]["relationships"]["tag-bindings"] = {
            "data": tag_bindings_data
        }
    
    # Make the API request
    success, data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}",
        method="PATCH",
        data=payload
    )
    
    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary

@mcp.tool()
async def delete_workspace(organization: str, workspace_name: str) -> dict:
    """
    Delete a workspace from an organization
    
    Args:
        organization: The organization name (required)
        workspace_name: The name of the workspace to delete (required)
        
    Returns:
        Success message or error details
    """
    
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}
    
    if not workspace_name:
        return {"error": "Workspace name is required"}
    
    # Make the API request
    success, data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}",
        method="DELETE"
    )
    
    if success:
        return {"status": "success", "message": f"Workspace '{workspace_name}' deleted successfully"}
    else:
        return data  # Error info is already in the data dictionary

@mcp.tool()
async def safe_delete_workspace(organization: str, workspace_name: str) -> dict:
    """
    Safely delete a workspace, but only if it's not managing any resources
    
    When you delete a Terraform workspace with resources, Terraform can no longer track
    or manage that infrastructure. During a safe delete, Terraform only deletes the
    workspace if it is not managing any resources.
    
    Args:
        organization: The organization name (required)
        workspace_name: The name of the workspace to delete (required)
        
    Returns:
        Success message or error details
    """
    
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}
    
    if not workspace_name:
        return {"error": "Workspace name is required"}
    
    # Make the safe-delete API request
    success, data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}/actions/safe-delete",
        method="POST"
    )
    
    if success:
        return {"status": "success", "message": f"Workspace '{workspace_name}' safely deleted successfully"}
    else:
        return data  # Error info is already in the data dictionary

@mcp.tool()
async def lock_workspace(organization: str, workspace_name: str, reason: str = "") -> dict:
    """
    Lock a workspace to prevent Terraform runs
    
    Args:
        organization: The organization name (required)
        workspace_name: The name of the workspace to lock (required)
        reason: Optional reason for locking the workspace
        
    Returns:
        Updated workspace details or error message
    """
    
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}
    
    if not workspace_name:
        return {"error": "Workspace name is required"}
    
    # Build the request payload
    payload = {
        "data": {
            "reason": reason if reason else "Locked via Terraform Cloud MCP Server"
        }
    }
    
    # First, get the workspace ID
    id_success, id_data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}"
    )
    
    if not id_success:
        return id_data  # Return error from workspace lookup
    
    # Extract the workspace ID
    try:
        workspace_id = id_data["data"]["id"]
    except (KeyError, TypeError):
        return {"error": "Failed to get workspace ID"}
    
    # Make the API request
    success, data = await make_api_request(
        f"workspaces/{workspace_id}/actions/lock",
        method="POST",
        data=payload
    )
    
    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary

@mcp.tool()
async def unlock_workspace(organization: str, workspace_name: str) -> dict:
    """
    Unlock a workspace to allow Terraform runs
    
    Args:
        organization: The organization name (required)
        workspace_name: The name of the workspace to unlock (required)
        
    Returns:
        Updated workspace details or error message
    """
    
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}
    
    if not workspace_name:
        return {"error": "Workspace name is required"}
    
    # First, get the workspace ID
    id_success, id_data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}"
    )
    
    if not id_success:
        return id_data  # Return error from workspace lookup
    
    # Extract the workspace ID
    try:
        workspace_id = id_data["data"]["id"]
    except (KeyError, TypeError):
        return {"error": "Failed to get workspace ID"}
    
    # Make the API request
    success, data = await make_api_request(
        f"workspaces/{workspace_id}/actions/unlock",
        method="POST"
    )
    
    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary

@mcp.tool()
async def force_unlock_workspace(organization: str, workspace_name: str) -> dict:
    """
    Force unlock a workspace that may be locked by another user or process
    
    Args:
        organization: The organization name (required)
        workspace_name: The name of the workspace to force unlock (required)
        
    Returns:
        Updated workspace details or error message
    """
    
    # Validate organization name
    valid, error_message = validate_organization(organization)
    if not valid:
        return {"error": error_message}
    
    if not workspace_name:
        return {"error": "Workspace name is required"}
    
    # First, get the workspace ID
    id_success, id_data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}"
    )
    
    if not id_success:
        return id_data  # Return error from workspace lookup
    
    # Extract the workspace ID
    try:
        workspace_id = id_data["data"]["id"]
    except (KeyError, TypeError):
        return {"error": "Failed to get workspace ID"}
    
    # Make the API request
    success, data = await make_api_request(
        f"workspaces/{workspace_id}/actions/force-unlock",
        method="POST"
    )
    
    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary

# Start server when run directly
if __name__ == "__main__":
    mcp.run()