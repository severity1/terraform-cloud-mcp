# Account Models

This document describes the data models used for account operations in Terraform Cloud.

## Overview

Account models provide structure for working with Terraform Cloud account information. These models help with accessing and validating account data retrieved from the Terraform Cloud API.

## Models Reference

### AccountDetailsRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for retrieving account details.

**Fields:** None - This model simply enforces the validation pattern for the account details endpoint.

**Usage Context:**
Used by the `get_account_details` function to validate request parameters (which are none in this case).

### AccountDetails

**Type:** Response Model

**Description:** Represents the account information of the current user or service account.

**Fields:**
- `id` (string): The ID of the account (e.g., "user-12345abcd")
- `username` (string): The username of the account
- `email` (string): The email address associated with the account
- `is_service_account` (boolean): Whether this is a service account (true) or user account (false)
- `avatar_url` (string, optional): URL to the user's avatar image
- `two_factor` (TwoFactorInfo, optional): Information about two-factor authentication status
  - `enabled` (boolean): Whether 2FA is enabled
  - `verified` (boolean): Whether 2FA has been verified

**JSON representation:**
```json
{
  "data": {
    "id": "user-12345abcd",
    "type": "users",
    "attributes": {
      "username": "admin-user",
      "email": "admin@example.com",
      "is-service-account": false,
      "avatar-url": "https://example.com/avatar.png",
      "two-factor": {
        "enabled": true,
        "verified": true
      }
    }
  }
}
```

**Notes:**
- Field names in JSON responses use kebab-case format (e.g., "is-service-account")
- Field names in the model use snake_case format (e.g., is_service_account)
- The `from_api_response` static method helps parse API responses into this model
- Email is only returned for the authenticated user's own account

**Usage Examples:**
```python
# Parse account details from API response
account = AccountDetails.from_api_response(api_response)

# Check if account has two-factor authentication enabled
if account.two_factor and account.two_factor.enabled:
    print(f"2FA is enabled for {account.username}")

# Check if the account is a service account
if account.is_service_account:
    print(f"{account.username} is a service account")
```

## API Response Structure

When retrieving account details, the Terraform Cloud API returns a response with this structure:

```json
{
  "data": {
    "id": "user-12345abcd",
    "type": "users",
    "attributes": {
      "username": "admin-user",
      "email": "admin@example.com",
      "is-service-account": false,
      "avatar-url": "https://example.com/avatar.png",
      "two-factor": {
        "enabled": true,
        "verified": true
      }
    }
  }
}
```

## Related Resources

- [Account Tools](../tools/account.md)
- [Terraform Cloud API - Account](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/account)