# Account Model Examples

## Basic Usage

```python
from terraform_cloud_mcp.models.account import AccountDetails

# Access account details from API response
account_data = {
    "data": {
        "id": "user-12345abcd",
        "type": "users",
        "attributes": {
            "username": "admin-user",
            "email": "admin@example.com",
            "is-service-account": False,
            "avatar-url": "https://example.com/avatar.png",
            "two-factor": {
                "enabled": True,
                "verified": True
            }
        }
    }
}

# Parse account details from API response
account_details = AccountDetails.from_api_response(account_data)

# Access account attributes
username = account_details.username
email = account_details.email
is_2fa_enabled = account_details.two_factor.enabled
```

## Common Patterns

```python
# Working with API responses
api_response = await get_account_details()
account = AccountDetails.from_api_response(api_response)

# Check if account has two-factor authentication enabled
if account.two_factor and account.two_factor.enabled:
    print(f"2FA is enabled for {account.username}")
else:
    print(f"2FA is NOT enabled for {account.username}")

# Check if the account is a service account
if account.is_service_account:
    print(f"{account.username} is a service account")
else:
    print(f"{account.username} is a user account")
```

## Advanced Use Cases

```python
# Serialize account details for logging or display
# (omitting sensitive information)
def format_account_info(account: AccountDetails) -> dict:
    """Format account information for display, omitting sensitive details."""
    return {
        "username": account.username,
        "account_type": "service" if account.is_service_account else "user",
        "security": {
            "two_factor_enabled": account.two_factor.enabled if account.two_factor else False,
            "two_factor_verified": account.two_factor.verified if account.two_factor else False
        }
    }

# Example usage
account = AccountDetails.from_api_response(api_response)
account_info = format_account_info(account)
```