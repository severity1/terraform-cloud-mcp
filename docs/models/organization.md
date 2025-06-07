# Organization Models

This document describes the data models used for organization operations in Terraform Cloud.

## Overview

Organization models provide structure and validation for interacting with the Terraform Cloud Organizations API. These models define organization settings, authentication policies, and default configurations for workspaces.

## Models Reference

### CollaboratorAuthPolicy

**Type:** Enum (string)

**Description:** Authentication policy options for organization collaborators.

**Values:**
- `password`: Password-only authentication is allowed
- `two_factor_mandatory`: Two-factor authentication is required for all users

**JSON representation:**
```json
{
  "collaborator-auth-policy": "two_factor_mandatory"
}
```

**Usage Context:**
Used to enforce security policies across an organization. Setting this to `two_factor_mandatory` requires all users to have 2FA enabled before they can access organization resources.

### ExecutionMode

**Type:** Enum (string)

**Description:** Execution mode options for workspaces and organizations.

**Values:**
- `remote`: Terraform runs on Terraform Cloud's infrastructure
- `local`: Terraform runs on your local machine
- `agent`: Terraform runs on your own infrastructure using an agent

**JSON representation:**
```json
{
  "default-execution-mode": "remote"
}
```

**Usage Context:**
Used to define how Terraform operations are executed for workspaces in an organization.

### OrganizationParams

**Type:** Object

**Description:** Parameters for organization operations. Used to configure organization settings when creating or updating organizations.

**Fields:**
- `name` (string, optional): Name of the organization (min length: 3, must match pattern: ^[a-z0-9][-a-z0-9_]*[a-z0-9]$)
- `email` (string, optional): Admin email address (must be valid email format)
- `collaborator_auth_policy` (CollaboratorAuthPolicy, optional): Authentication policy (password or two_factor_mandatory)
- `session_timeout` (integer, optional): Session timeout after inactivity in minutes (default: 20160)
- `session_remember` (integer, optional): Session total expiration time in minutes (default: 20160)
- `cost_estimation_enabled` (boolean, optional): Whether to enable cost estimation (default: false)
- `default_execution_mode` (ExecutionMode, optional): Default execution mode for workspaces (remote, local, agent)
- `aggregated_commit_status_enabled` (boolean, optional): Whether to aggregate VCS status updates (default: true)
- `speculative_plan_management_enabled` (boolean, optional): Whether to auto-cancel unused speculative plans (default: true)
- `assessments_enforced` (boolean, optional): Whether to enforce health assessments for all workspaces (default: false)
- `allow_force_delete_workspaces` (boolean, optional): Allow deleting workspaces with resources (default: false)
- `default_agent_pool_id` (string, optional): Default agent pool ID (required when default_execution_mode=agent)
- `owners_team_saml_role_id` (string, optional): The SAML role for owners team
- `send_passing_statuses_for_untriggered_speculative_plans` (boolean, optional): Whether to send VCS status for untriggered plans (default: false)

**JSON representation:**
```json
{
  "data": {
    "type": "organizations",
    "attributes": {
      "name": "my-organization",
      "email": "admin@example.com",
      "session-timeout": 60,
      "session-remember": 1440,
      "collaborator-auth-policy": "two_factor_mandatory",
      "cost-estimation-enabled": true,
      "default-execution-mode": "remote",
      "assessments-enforced": true
    }
  }
}
```

**Notes:**
- Field names in JSON use kebab-case format (e.g., "default-execution-mode")
- Field names in the model use snake_case format (e.g., default_execution_mode)
- All fields are optional when updating (PATCH) but name and email are required when creating (POST)

**Validation Rules:**
- Organization names must be 3 or more characters
- Organization names must start and end with a lowercase letter or number
- Organization names may contain lowercase letters, numbers, hyphens, and underscores
- Email addresses must be valid format
- Session timeouts and remembers must be between 1 and 43200 minutes (30 days)

### OrganizationDetailsRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for retrieving organization details.

**Fields:**
- `organization` (string, required): The name of the organization to retrieve details for

**Used by:**
- `get_organization_details` tool function to validate the organization name parameter

### OrganizationEntitlementsRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for retrieving organization entitlements.

**Fields:**
- `organization` (string, required): The name of the organization to retrieve entitlements for

**Used by:**
- `get_organization_entitlements` tool function to validate the organization name parameter

### OrganizationDeleteRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for deleting an organization.

**Fields:**
- `organization` (string, required): The name of the organization to delete

**Used by:**
- `delete_organization` tool function to validate the organization name parameter

### OrganizationListRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for listing organizations.

**Fields:**
- `page_number` (int, optional): Page number to return (default: 1)
- `page_size` (int, optional): Number of items per page (default: 20)
- `q` (str, optional): Search query to filter by name and email
- `query_email` (str, optional): Search query to filter by email only
- `query_name` (str, optional): Search query to filter by name only

**Used by:**
- `list_organizations` tool function to validate pagination and search parameters

### OrganizationCreateRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for creating an organization.

**Fields:**
- `name` (string, required): The name for the organization
- `email` (string, required): Admin email address
- `params` (OrganizationParams, optional): Additional configuration options

**Used by:**
- `create_organization` tool function to validate organization creation parameters

### OrganizationUpdateRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for updating an organization.

**Fields:**
- `organization` (string, required): The name of the organization to update
- `params` (OrganizationParams, optional): Settings to update

**Used by:**
- `update_organization` tool function to validate organization update parameters

## API Response Structure

### Organization Details Response

```json
{
  "data": {
    "id": "org-ABcd1234",
    "type": "organizations",
    "attributes": {
      "name": "my-organization",
      "external-id": "org-12345",
      "created-at": "2023-01-15T12:34:56Z",
      "email": "admin@example.com",
      "session-timeout": 60,
      "session-remember": 1440,
      "collaborator-auth-policy": "two_factor_mandatory",
      "cost-estimation-enabled": true,
      "default-execution-mode": "remote",
      "permissions": {
        "can-destroy": true,
        "can-update": true
      }
    },
    "relationships": {
      "subscription": {
        "data": {
          "id": "sub-XYZ789",
          "type": "subscriptions"
        }
      }
    },
    "links": {
      "self": "/api/v2/organizations/my-organization"
    }
  }
}
```

### Organization Entitlements Response

```json
{
  "data": {
    "id": "org-ABcd1234",
    "type": "organization-entitlements",
    "attributes": {
      "cost-estimation": true,
      "operations": true,
      "private-modules": true,
      "sentinel": true,
      "teams": true,
      "vcs-integrations": true,
      "usage-reporting": true,
      "self-serve-billing": true,
      "state-storage": {
        "unlimited": true
      },
      "teams": {
        "limit": 5,
        "used": 3
      },
      "private-module-registry": {
        "limit": 100,
        "used": 25
      }
    }
  }
}
```

## Related Resources

- [Organization Tools](../tools/organization.md)
- [Workspace Models](workspace.md)
- [Terraform Cloud API - Organizations](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations)