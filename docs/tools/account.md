# Account Tools

This module provides tools for retrieving information about the currently authenticated Terraform Cloud account.

## Overview

Account tools allow you to access details about the currently authenticated user or service account. This is useful for retrieving account information, verifying authentication status, and checking permissions.

## API Reference

These tools interact with the Terraform Cloud Account API:
- [Account API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/account)

## Tools Reference

### get_account_details

**Function:** `get_account_details() -> Dict[str, Any]`

**Description:** Retrieves information about the currently authenticated user or service account.

**Parameters:** None - uses the authentication from the API token environment variable.

**Returns:** JSON response containing comprehensive account details including:
- User ID and username
- Email address
- Two-factor authentication status
- Service account status
- User permissions and attributes

**Notes:**
- This endpoint returns additional information (email address) beyond what is returned by the standard Users API
- Useful for determining if you're authenticated as a user or a service account
- Can be used to verify 2FA compliance and permissions
- Returns the same type of object as the Users API, but with additional information

**Common Error Scenarios:**

| Error | Cause | Solution |
|-------|-------|----------|
| 401 | Invalid or expired API token | Generate a new API token in Terraform Cloud settings |
| 403 | Token lacks sufficient permissions | Ensure the token has proper access rights |