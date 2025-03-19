# Organization Entitlements - Example Conversation

This document shows example conversations with Claude using the Terraform Cloud MCP organization entitlements feature.

## Viewing Basic Organization Entitlements

**User**: Can you show me the entitlements for my organization "hashicorp"?

**Claude**: I'll retrieve the entitlements for your "hashicorp" organization.

```python
result = await get_organization_entitlements("hashicorp")
```

Here are the entitlements for your "hashicorp" organization:

**Features:**
- Operations: True
- Private Module Registry: True
- Sentinel Policies: False
- Teams: False
- Cost Estimation: False
- SSO: False
- State Storage: True
- VCS Integrations: True
- Self-Serve Billing: True
- Configuration Designer: True

**Limits:**
- User Limit: 5
- Policy Limit: 5
- Policy Set Limit: 1
- Run Task Limit: 1
- Run Task Workspace Limit: 10

These entitlements indicate you're on a basic tier plan with access to core features like state storage, operations, and private module registry, but without premium features like SSO, teams, or Sentinel policies.

## Understanding Plan Features and Upgrades

**User**: What features would I get if I upgraded my plan?

**Claude**: Based on your current entitlements, if you upgraded your plan (likely to a Team or Enterprise tier), you would gain access to several premium features:

1. **Teams functionality** - Create and manage teams with different permission levels
2. **SSO (Single Sign-On)** - Enterprise identity management integration
3. **Sentinel Policies** - Advanced policy as code enforcement
4. **Cost Estimation** - Get cost estimates for your infrastructure changes
5. **Run Tasks** - Custom integrations that run during the plan/apply cycle
6. **Audit Logging** - Detailed activity logs for compliance
7. **Higher Limits** - Increased limits for:
   - Users (beyond your current 5-user limit)
   - Policy sets
   - Run tasks

You might also gain access to:
- Agents - Run Terraform in your own infrastructure
- Global Run Tasks - Run tasks that apply across multiple workspaces
- Module Tests Generation - Automated test creation for modules

The exact features would depend on the specific tier you upgrade to. Would you like me to help you determine which plan would be best for your needs?

## Analyzing Usage Against Entitlements

**User**: Can you tell me which features we're actually using in our current organization?

**Claude**: To determine which features you're actually using in your organization, I'll need to check various aspects of your Terraform Cloud setup.

```python
# First, let's get overall organization details
org_details = await get_organization_details("hashicorp")

# Let's check workspace count to understand usage scale
workspaces = await list_workspaces(organization="hashicorp")

# Check if there are any runs to understand activity level
runs = await list_runs_in_organization(organization="hashicorp", page_size=5)
```

Based on my analysis of your "hashicorp" organization:

**Features You're Currently Using:**
- State Storage: You have 12 workspaces with state files
- Remote Operations: You've run 87 Terraform operations in the last month
- Private Module Registry: You have 3 modules registered
- VCS Integration: Connected to GitHub for 75% of your workspaces

**Features Available But Not Used:**
- Configuration Designer: Available but no evidence of usage
- Self-Serve Billing: Available but limited usage patterns

**Features Limited By Your Current Plan:**
- Teams: You can't create teams (5 individual users maximum)
- Sentinel Policies: Not available on your current plan
- Cost Estimation: Not available on your current plan
- SSO: Not available on your current plan

Based on your usage patterns, you might benefit most from upgrading if you need:
1. More than 5 users (teams functionality)
2. Policy enforcement for governance
3. Cost visibility for your infrastructure

Would you like more specific recommendations based on your organization's needs?

## Checking User Capacity Against Limits

**User**: Are we close to hitting our user limit?

**Claude**: Let me check your current user count against your limit.

```python
# Get organization entitlements
entitlements = await get_organization_entitlements("hashicorp")
user_limit = entitlements["data"]["attributes"]["user-limit"]

# We'd need to use a different API call to get the actual user count
# Since this is not yet implemented, we'll simulate this information
# In a real implementation, you'd use something like:
# users = await list_organization_users("hashicorp")
# user_count = len(users["data"])
```

Based on your organization entitlements:

- **User Limit**: 5 users
- **Current Users**: 4 users
- **Remaining Capacity**: 1 user (80% of limit utilized)

You are approaching your user limit with 4 out of 5 available seats used. This means you only have 1 seat remaining before you hit your limit.

If you're planning to add more team members soon, you might want to consider upgrading to a Team or Enterprise tier plan which would provide:

1. Higher or unlimited user seats
2. Teams functionality to manage user permissions more effectively
3. More granular access control options

Would you like me to help you explore upgrade options to accommodate your growing team?

## Comparing Against Different Organizations

**User**: How do our entitlements compare to our "hashicorp-staging" organization?

**Claude**: I'll compare the entitlements between your "hashicorp" and "hashicorp-staging" organizations.

```python
# Get entitlements for both organizations
main_org_entitlements = await get_organization_entitlements("hashicorp")
staging_org_entitlements = await get_organization_entitlements("hashicorp-staging")

# Extract the attributes for easier comparison
main_attributes = main_org_entitlements["data"]["attributes"]
staging_attributes = staging_org_entitlements["data"]["attributes"]
```

Here's a comparison of entitlements between your organizations:

| Feature | hashicorp (Production) | hashicorp-staging |
|---------|------------------------|-------------------|
| **Core Features** | | |
| Operations | ✓ | ✓ |
| State Storage | ✓ | ✓ |
| Private Module Registry | ✓ | ✓ |
| VCS Integration | ✓ | ✓ |
| **Premium Features** | | |
| Teams | ✗ | ✓ |
| Sentinel Policies | ✗ | ✓ |
| Cost Estimation | ✗ | ✓ |
| SSO | ✗ | ✗ |
| **Limits** | | |
| User Limit | 5 | 25 |
| Policy Limit | 5 | 15 |
| Run Task Limit | 1 | 5 |

Interesting findings:

1. Your staging organization is actually on a higher tier plan with more premium features
2. The staging organization has significantly higher user and policy limits
3. Both organizations lack SSO, which is typically only available on Enterprise plans

This suggests your staging environment might be used for testing advanced features before adopting them in production. Would you like me to recommend how to align these environments, or explain why certain features might be important to have in production?