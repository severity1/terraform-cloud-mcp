# Account Tools Examples

## Basic Usage

```python
# Get the current authenticated user's account details
account_details = await get_account_details()

# Parse the account details response into a structured object
from terraform_cloud_mcp.models.account import AccountDetails

account = AccountDetails.from_api_response(account_details)
print(f"Logged in as: {account.username} ({account.email})")
```

## Common Patterns

```python
# Check if the current token belongs to a service account
account_details = await get_account_details()
account = AccountDetails.from_api_response(account_details)

if account.is_service_account:
    print("Using a service account")
else:
    print("Using a user account")

# Verify 2FA status for security compliance
if account.two_factor and account.two_factor.enabled and account.two_factor.verified:
    print("Account complies with 2FA security requirements")
else:
    print("WARNING: 2FA is not properly configured on this account")
```

## Advanced Use Cases

```python
# Use account information to verify permissions
# (This is a conceptual example - actual implementation would depend on the specific use case)

async def verify_account_permissions():
    """Verify that the current account has sufficient permissions for operations."""
    account_details = await get_account_details()
    account = AccountDetails.from_api_response(account_details)
    
    # Check if service account or regular user
    if account.is_service_account:
        # Service accounts usually have specific, limited permissions
        print("Operating as service account, permissions may be limited")
    else:
        print(f"Operating as user {account.username}")
    
    # Return the account details for further processing
    return account

# Example usage
account = await verify_account_permissions()
```