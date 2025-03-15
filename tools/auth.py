"""Authentication tools for Terraform Cloud MCP"""

from models.auth import AuthResult
from api.client import make_api_request

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
