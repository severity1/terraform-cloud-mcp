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

from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Parse command line arguments
parser = argparse.ArgumentParser(description='Terraform Cloud MCP Server')
parser.add_argument('--token', '-t', help='Terraform Cloud API token')
args = parser.parse_args()

# Store default token - check environment variable first, then command line arg
# Security note: API tokens are sensitive data and should never be logged or exposed
DEFAULT_TOKEN = os.environ.get("TFC_TOKEN") or args.token

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

async def make_api_request(path: str, method: str = "GET", token: str = "", params: dict = {}) -> Tuple[bool, dict]:
    """
    Make a request to the Terraform Cloud API
    
    Args:
        path: API path to request (without base URL)
        method: HTTP method (default: GET)
        token: API token (defaults to DEFAULT_TOKEN)
        params: Query parameters for the request (optional)
        
    Returns:
        Tuple of (success, data) where data is either the response JSON or an error dict
    """
    if not token:
        token = DEFAULT_TOKEN
        
    if not token:
        return (False, {"error": "Token is required. Either start the server with --token or TFC_TOKEN environment variable."})
    
    try:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/vnd.api+json"}
        
        async with httpx.AsyncClient() as client:
            url = f"{TERRAFORM_CLOUD_API_URL}/{path}"
            if method == "GET":
                response = await client.get(url, headers=headers, params=params)
            else:
                # For future methods (POST, PUT, etc.)
                return (False, {"error": f"Unsupported method: {method}"})
                
            if response.status_code == 200:
                return (True, response.json())
            else:
                return (False, {"error": f"API request failed: {response.status_code}"})
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

# Start server when run directly
if __name__ == "__main__":
    mcp.run()