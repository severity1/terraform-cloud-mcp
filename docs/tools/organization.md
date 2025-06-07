# Organization Tools

This module provides tools for managing organizations in Terraform Cloud.

## Overview

Organizations in Terraform Cloud are the top-level resource that represents a group or company. Organizations contain workspaces, teams, and other shared settings. These tools allow you to create, read, update, delete organizations, and view organization entitlements.

## API Reference

These tools interact with the Terraform Cloud Organizations API:
- [Organizations API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations)
- [Organizations and Teams](https://developer.hashicorp.com/terraform/cloud-docs/users-teams-organizations/organizations)

## Tools Reference

### list_organizations

**Function:** `list_organizations(page_number: int = 1, page_size: int = 20, q: Optional[str] = None, query_email: Optional[str] = None, query_name: Optional[str] = None) -> Dict[str, Any]`

**Description:** Retrieves a paginated list of organizations the current user has access to.

**Parameters:**
- `page_number` (int, optional): Page number to fetch (default: 1)
- `page_size` (int, optional): Number of results per page (default: 20)
- `q` (str, optional): Search query to filter by name and email
- `query_email` (str, optional): Search query to filter by email only
- `query_name` (str, optional): Search query to filter by name only

**Returns:** JSON response containing list of organizations with their metadata.

**Notes:**
- Returns only organizations the authenticated user has access to
- Search filters are partial matches (substrings)
- Response is paginated with links to next/previous pages

### get_organization_details

**Function:** `get_organization_details(organization: str) -> Dict[str, Any]`

**Description:** Retrieves comprehensive information about a specific organization.

**Parameters:**
- `organization` (str): The name of the organization to retrieve details for

**Returns:** JSON response containing detailed organization information including:
- Name, email, and creation timestamp
- Authentication policy settings
- Default execution mode
- Subscription and feature settings

**Notes:**
- Requires read access to the organization
- Provides essential information before working with organization resources

### get_organization_entitlements

**Function:** `get_organization_entitlements(organization: str) -> Dict[str, Any]`

**Description:** Retrieves information about available features based on the organization's subscription tier.

**Parameters:**
- `organization` (str): The name of the organization to retrieve entitlements for

**Returns:** JSON response containing feature limits and subscription information:
- Available features (e.g., cost estimation, policy enforcement)
- Resource limits (e.g., teams, private modules)
- Subscription tier information

**Notes:**
- Essential for determining which features are available to an organization
- Useful before attempting to use premium features
- Different subscription tiers have different feature sets

### create_organization

**Function:** `create_organization(name: str, email: str, params: Optional[OrganizationParams] = None) -> Dict[str, Any]`

**Description:** Creates a new organization with the specified name and email.

**Parameters:**
- `name` (str): The name for the organization (must follow naming rules)
- `email` (str): Email address for the admin contact
- `params` (OrganizationParams, optional): Additional configuration settings:
  - `collaborator_auth_policy`: Authentication policy (password or two_factor_mandatory)
  - `session_timeout`: Session timeout after inactivity in minutes
  - `cost_estimation_enabled`: Whether to enable cost estimation
  - `default_execution_mode`: Default workspace execution mode
  - And many other options...

**Returns:** JSON response with the created organization details.

**Notes:**
- Organization names must follow format constraints (lowercase alphanumeric, hyphens)
- Names must be globally unique across Terraform Cloud
- Only certain users have permission to create organizations

### update_organization

**Function:** `update_organization(organization: str, params: Optional[OrganizationParams] = None) -> Dict[str, Any]`

**Description:** Updates an existing organization's settings.

**Parameters:**
- `organization` (str): The name of the organization to update
- `params` (OrganizationParams, optional): Settings to update:
  - `email`: Admin email address
  - `session_timeout`: Session timeout after inactivity
  - `collaborator_auth_policy`: Authentication policy
  - And all other options available in create_organization...

**Returns:** JSON response with the updated organization details.

**Notes:**
- Only specified attributes will be updated
- Requires admin permissions on the organization
- Cannot change the organization name (immutable)

### delete_organization

**Function:** `delete_organization(organization: str) -> Dict[str, Any]`

**Description:** Permanently deletes an organization and all its content.

**Parameters:**
- `organization` (str): The name of the organization to delete

**Returns:** Success confirmation (HTTP 204 No Content) or error details.

**Notes:**
- This is an extremely destructive operation
- Will delete all workspaces, teams, configurations, and state files
- Organization names cannot be recreated after deletion
- Requires owner permissions

**Common Error Scenarios:**

| Error | Cause | Solution |
|-------|-------|----------|
| 404 | Organization not found | Verify the organization name |
| 403 | Insufficient permissions | Must be an organization owner to delete |
| 422 | Validation failure | Ensure the name format is correct |
| 409 | Organization has child resources | Delete all child resources first |