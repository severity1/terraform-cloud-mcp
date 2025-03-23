# Organization Management - Example Conversations

This document shows example conversations with Claude using the Terraform Cloud MCP organization management features.

## Listing and Finding Organizations

**User**: List all my Terraform Cloud organizations

**Claude**: I'll list all the Terraform Cloud organizations you have access to.

```python
organizations = await list_organizations()
```

Here are all the Terraform Cloud organizations you have access to:

1. **example-org**
   - Email: admin@example.com
   - Created: January 15, 2023
   - Plan: Team & Governance

2. **terraform-demo**
   - Email: terraform@example.com
   - Created: March 3, 2023
   - Plan: Free

3. **acme-corp**
   - Email: devops@acme-corp.com
   - Created: June 12, 2023
   - Plan: Business

4. **infrastructure-team**
   - Email: infra@example.com
   - Created: August 8, 2023
   - Plan: Free

5. **test-org**
   - Email: test@example.com
   - Created: December 1, 2023
   - Plan: Free

**User**: Show me details for my "example-org" organization

**Claude**: I'll retrieve detailed information about the "example-org" organization.

```python
org_details = await get_organization_details(organization="example-org")
```

Here are the details for the "example-org" organization:

**Basic Information:**
- Name: example-org
- ID: org-WV6DfwfxxXvLfvfs
- External ID: org-WV6DfwfxxXvLfvfs
- Created: January 15, 2023
- Email: admin@example.com

**Plan Details:**
- Plan Type: Team & Governance
- Plan Expired: No
- Trial Status: Not on trial
- Enterprise Plan: No

**Settings:**
- Default Execution Mode: Remote
- Collaborator Auth Policy: Password
- Cost Estimation Enabled: Yes
- Run Queuing Enabled: Yes
- VCS Status Updates: Aggregated (commit status enabled)
- SAML Enabled: No

**Permissions:**
- You can manage users, teams, and workspaces
- You can manage VCS connections
- You can create and manage modules
- You can create and manage policy sets
- You can manage subscription settings

This organization is on the Team & Governance tier with active cost estimation features and standard remote execution setup.

**User**: Get information about "example-org" organization

**Claude**: I'll retrieve the details for the "example-org" organization.

```python
org_details = await get_organization_details(organization="example-org")
```

Here are the details for the "example-org" organization:

**Basic Information:**
- Name: example-org
- ID: org-WV6DfwfxxXvLfvfs
- External ID: org-WV6DfwfxxXvLfvfs
- Created: January 15, 2023
- Email: admin@example.com
- Plan Type: Team & Governance

The organization is on the Team & Governance tier. If you'd like to see the organization's entitlements and feature limits, I can retrieve that information separately.

**User**: What are the entitlements for my "example-org" organization?

**Claude**: I'll specifically check the entitlements for your "example-org" organization.

```python
entitlements = await get_organization_entitlements(organization="example-org")
```

Here are the detailed entitlements for your "example-org" organization:

**Features:**
- Operations: Yes (remote Terraform operations)
- Private Module Registry: Yes
- Sentinel Policies: Yes
- Teams: Yes
- Cost Estimation: Yes
- VCS Integrations: Yes
- State Storage: Yes
- Self-Serve Billing: Yes
- Configuration Designer: Yes
- Run Tasks: Yes

**Enterprise Features (Not Available):**
- SSO: No
- Audit Logging: No
- Agents: No
- Private Policy Agents: No

**Limits:**
- User Limit: 25
- Team Limit: Unlimited
- Policy Limit: 15
- Policy Set Limit: 20
- Run Task Limit: 10
- Run Task Workspace Limit: 100
- Policy Mandatory Enforcement Limit: 5

Your organization has the Team & Governance tier features, including policy as code (Sentinel), cost estimation, and team management. You don't currently have access to enterprise features like SSO or audit logging. Your organization can have up to 25 users and has reasonable limits for policies and run tasks.

**User**: Find organizations with "prod" in their name

**Claude**: I'll search for organizations with "prod" in their name.

```python
prod_orgs = await list_organizations(query_name="prod")
```

I found the following organizations with "prod" in their name:

1. **production-infra**
   - Email: prod-admin@example.com
   - Created: February 10, 2023
   - Plan: Business

2. **acme-prod**
   - Email: ops@acme.com
   - Created: July 7, 2023
   - Plan: Team & Governance

3. **production-systems**
   - Email: sysadmin@example.com
   - Created: October 15, 2023
   - Plan: Free

These three organizations match your search query for "prod" in their names. Each has different plan levels and was created at different times.

## Creating and Managing Organizations

**User**: Create a new organization named "terraform-demo" with my email "admin@example.com"

**Claude**: I'll create a new organization named "terraform-demo" with your email.

```python
new_org = await create_organization(
    name="terraform-demo",
    email="admin@example.com"
)
```

I've successfully created a new organization in Terraform Cloud. Here are the details:

**Organization Created:**
- Name: terraform-demo
- Email: admin@example.com
- ID: org-Bzyc2JuegvVLAibn
- Creation Date: Just now

**Default Configuration:**
- Execution Mode: Remote
- Authentication Policy: Password
- Cost Estimation: Disabled
- Session Timeout: 20160 minutes (14 days)

**Initial Entitlements:**
- Private Module Registry: Yes
- State Storage: Yes
- VCS Integrations: Yes
- Teams: No (Free tier)
- Sentinel Policies: No (Free tier)
- User Limit: 5 (Free tier)

The organization has been created with default settings. You're currently the owner of this organization. You can invite additional members and create workspaces within this organization.

**User**: Update my "terraform-demo" organization to enable cost estimation

**Claude**: I'll update the "terraform-demo" organization to enable cost estimation.

```python
updated_org = await update_organization(
    organization="terraform-demo",
    cost_estimation_enabled=True
)
```

I've updated the "terraform-demo" organization to enable cost estimation. Here's the confirmation:

**Organization Updated:**
- Name: terraform-demo
- Email: admin@example.com
- ID: org-Bzyc2JuegvVLAibn

**Updated Setting:**
- Cost Estimation: Enabled (previously Disabled)

**Note:**
Cost estimation is now enabled for this organization. This feature will:
- Show estimated costs for all Terraform plans
- Calculate cost impact of planned changes
- Display cost breakdowns by resource type
- Show cost trend analysis

The cost estimation feature uses cloud provider pricing data to estimate the cost of resources in your Terraform configurations. This can help teams understand the financial impact of their infrastructure changes before applying them.

**User**: Change the email address for "terraform-demo" to "terraform@example.com"

**Claude**: I'll update the email address for the "terraform-demo" organization.

```python
updated_org = await update_organization(
    organization="terraform-demo",
    email="terraform@example.com"
)
```

I've successfully updated the email address for the "terraform-demo" organization. Here's the confirmation:

**Organization Updated:**
- Name: terraform-demo
- New Email: terraform@example.com (previously admin@example.com)
- ID: org-Bzyc2JuegvVLAibn

The organization's notification email has been changed to terraform@example.com. All system notifications and alerts will now be sent to this address.

**User**: Delete the "test-org" organization

**Claude**: I'll help you delete the "test-org" organization. This is a significant action that will permanently delete all resources.

```python
delete_response = await delete_organization(organization="test-org")
```

**Organization Deletion Successful**

The "test-org" organization has been permanently deleted. All associated resources have been removed:
- All workspaces and their configurations
- All state files and state versions
- All team memberships and user associations
- All variables, policy sets, and modules

The organization name "test-org" is now available for use again if you wish to recreate it in the future.

**Note**: This operation is irreversible. All data associated with the organization has been permanently deleted.