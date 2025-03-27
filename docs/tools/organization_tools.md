# Organization Tools Examples

## Basic Usage

```python
# List all organizations the authenticated user has access to
orgs = await list_organizations()

# Get details for a specific organization
org_details = await get_organization_details(organization="my-organization")

# Get entitlement set for an organization (features and limits)
entitlements = await get_organization_entitlements(organization="my-organization")
```

## Common Patterns

```python
# Create a new organization with basic settings
from terraform_cloud_mcp.models.organizations import OrganizationParams

new_org = await create_organization(
    name="new-organization", 
    email="admin@example.com"
)

# List organizations with pagination and search filtering
search_results = await list_organizations(
    page_number=1,
    page_size=10,
    query_name="terraform"
)

# Update organization settings
from terraform_cloud_mcp.models.organizations import CollaboratorAuthPolicy

updated_org = await update_organization(
    organization="my-organization",
    params={
        "email": "updated-admin@example.com",
        "collaborator_auth_policy": CollaboratorAuthPolicy.TWO_FACTOR_MANDATORY
    }
)
```

## Advanced Use Cases

```python
# Create a new organization with detailed configuration
from terraform_cloud_mcp.models.organizations import (
    OrganizationParams,
    ExecutionMode,
    CollaboratorAuthPolicy
)

enterprise_org = await create_organization(
    name="enterprise-org",
    email="enterprise@example.com",
    params=OrganizationParams(
        default_execution_mode=ExecutionMode.AGENT,
        default_agent_pool_id="apool-1234abcd",
        cost_estimation_enabled=True,
        assessments_enforced=True,
        collaborator_auth_policy=CollaboratorAuthPolicy.TWO_FACTOR_MANDATORY,
        session_timeout=60,  # minutes
        session_remember=1440,  # minutes (1 day)
        aggregated_commit_status_enabled=True,
        allow_force_delete_workspaces=False
    )
)

# Check organization entitlements before performing operations
entitlements = await get_organization_entitlements(organization="my-organization")

# Check if the organization has cost estimation features
if entitlements.get("data", {}).get("attributes", {}).get("cost-estimation"):
    print("Cost estimation is available for this organization")
else:
    print("Cost estimation is not available for this organization")

# Delete an organization (use with extreme caution!)
await delete_organization(organization="org-to-delete")
```