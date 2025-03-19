# Workspace Management - Example Conversations

This document shows example conversations with Claude using the Terraform Cloud MCP workspace management features.

## Listing and Finding Workspaces

**User**: List all my workspaces in "example-org"

**Claude**: I'll list all workspaces in the "example-org" organization.

```python
workspaces = await list_workspaces(organization="example-org")
```

Here are all the workspaces in "example-org":

1. **production** - Production environment (Terraform v1.5.2)
   - Status: Active, Unlocked
   - Last run: Applied 2 days ago
   - VCS: Connected to GitHub (main branch)

2. **staging** - Staging environment (Terraform v1.5.2)
   - Status: Active, Unlocked
   - Last run: Applied 6 hours ago
   - VCS: Connected to GitHub (develop branch)

3. **dev-environment** - Development workspace (Terraform v1.5.3)
   - Status: Active, Unlocked
   - Last run: Planning 5 minutes ago
   - VCS: Connected to GitHub (feature/new-db branch)

4. **network-infra** - Network infrastructure (Terraform v1.4.6)
   - Status: Active, Locked by jane@example.com
   - Last run: Applied 2 weeks ago
   - VCS: Not connected

5. **security-baseline** - Security controls (Terraform v1.5.0)
   - Status: Active, Unlocked
   - Last run: Discarded 3 days ago
   - VCS: Connected to GitHub (main branch)

**User**: Find all workspaces in "example-org" with names containing "prod"

**Claude**: I'll search for workspaces in the "example-org" organization that have "prod" in their names.

```python
workspaces = await list_workspaces(organization="example-org", search_name="prod")
```

I found the following workspaces in "example-org" with "prod" in their names:

1. **production** - Production environment (Terraform v1.5.2)
   - Status: Active, Unlocked
   - Last run: Applied 2 days ago
   - VCS: Connected to GitHub (main branch)

2. **products-api** - Products API infrastructure (Terraform v1.5.0)
   - Status: Active, Unlocked
   - Last run: Applied 5 days ago
   - VCS: Connected to GitHub (release/v2 branch)

3. **prod-db-cluster** - Production database cluster (Terraform v1.5.1)
   - Status: Active, Locked by system
   - Last run: Errored 12 hours ago
   - VCS: Connected to GitHub (main branch)

**User**: List workspaces in "example-org" with the "environment:production" tag

**Claude**: I'll find workspaces in "example-org" that have the "environment:production" tag.

```python
workspaces = await list_workspaces(
    organization="example-org",
    search_tags="environment:production"
)
```

Here are the workspaces in "example-org" tagged with "environment:production":

1. **production** - Production environment (Terraform v1.5.2)
   - Tags: environment:production, region:us-west-2
   - Status: Active, Unlocked
   - Last run: Applied 2 days ago

2. **prod-db-cluster** - Production database cluster (Terraform v1.5.1)
   - Tags: environment:production, service:database, region:us-west-2
   - Status: Active, Locked by system
   - Last run: Errored 12 hours ago

3. **frontend-prod** - Production frontend resources (Terraform v1.5.0)
   - Tags: environment:production, service:frontend, region:us-west-2
   - Status: Active, Unlocked
   - Last run: Applied 1 week ago

4. **api-gateway-prod** - Production API gateway (Terraform v1.4.6)
   - Tags: environment:production, service:api, region:us-west-2
   - Status: Active, Unlocked
   - Last run: Applied 3 days ago

## Workspace Details and Management

**User**: Get details for the "production" workspace in "example-org"

**Claude**: I'll retrieve detailed information about the "production" workspace in "example-org".

```python
workspace = await get_workspace_details(
    organization="example-org",
    workspace_name="production"
)
```

Here are the details for the "production" workspace in "example-org":

**Basic Information:**
- Name: production
- Description: Production environment for main application
- ID: ws-7H9QJDXpY98V4w2Y
- Created: January 15, 2023
- Updated: May 3, 2024

**Terraform Configuration:**
- Version: 1.5.2
- Working Directory: /terraform
- Execution Mode: Remote
- Auto Apply: False
- Terraform State Version: 4
- Resource Count: 143

**VCS Integration:**
- Repository: github.com/example-org/main-infrastructure
- Branch: main
- Working Directory: /terraform
- Trigger Prefixes: ["/modules", "/environments/prod"]

**Current Status:**
- State: Active
- Lock Status: Unlocked
- Current Run: None
- Last Run: run-bP9xtXmqFoQNfjH7 (Applied 2 days ago)

**Tags:**
- environment:production
- region:us-west-2
- team:infrastructure

**User**: Create a new workspace in "example-org" called "staging" with auto-apply enabled

**Claude**: I'll create a new workspace called "staging" in the "example-org" organization with auto-apply enabled.

```python
new_workspace = await create_workspace(
    organization="example-org",
    name="staging",
    auto_apply=True,
    description="Staging environment for testing",
    terraform_version="1.5.2",
    working_directory="/terraform/staging",
    execution_mode="remote"
)
```

I've successfully created the "staging" workspace in "example-org" with auto-apply enabled. Here are the details:

**Workspace Details:**
- Name: staging
- Description: Staging environment for testing
- ID: ws-2VcPMzXqD75r8nL9
- Created: Just now
- Terraform Version: 1.5.2
- Working Directory: /terraform/staging
- Execution Mode: Remote
- Auto Apply: Enabled

The workspace is now ready to use. Since auto-apply is enabled, any successful plans will automatically be applied without requiring manual approval.

**User**: Update my "staging" workspace to use Terraform version 1.5.0

**Claude**: I'll update the "staging" workspace in "example-org" to use Terraform version 1.5.0.

```python
updated_workspace = await update_workspace(
    organization="example-org",
    workspace_name="staging",
    terraform_version="1.5.0"
)
```

I've successfully updated the "staging" workspace to use Terraform version 1.5.0. Here's the confirmation:

**Updated Workspace Details:**
- Name: staging
- ID: ws-2VcPMzXqD75r8nL9
- Terraform Version: 1.5.0 (previously 1.5.2)
- Working Directory: /terraform/staging
- Execution Mode: Remote
- Auto Apply: Enabled

The change has been applied immediately. Any new runs in this workspace will now use Terraform 1.5.0 instead of 1.5.2.

## Workspace Deletion

**User**: Delete my "dev-test" workspace in "example-org"

**Claude**: I'll help you delete the "dev-test" workspace in "example-org". This is a significant action that requires confirmation.

```python
delete_response = await delete_workspace(
    organization="example-org", 
    workspace_name="dev-test", 
    confirm=False
)
```

**WARNING: Confirmation Required**

You've requested to delete the "dev-test" workspace in "example-org". This action:
- Will permanently delete the workspace and all its configurations
- Will delete all workspace variables
- Will delete all state versions and state snapshots
- Cannot be undone

To confirm deletion, please explicitly confirm that you want to proceed.

**User**: Yes, please delete the workspace

**Claude**: I'll proceed with deleting the "dev-test" workspace as confirmed.

```python
delete_response = await delete_workspace(
    organization="example-org", 
    workspace_name="dev-test", 
    confirm=True
)
```

**Deletion Successful**

The "dev-test" workspace in "example-org" has been permanently deleted. All associated resources, variables, and state files have been removed.

**User**: Delete my "staging" workspace but only if it's not managing any resources

**Claude**: I'll help you safely delete the "staging" workspace, but only if it's not currently managing any resources.

```python
delete_response = await safe_delete_workspace(
    organization="example-org", 
    workspace_name="staging", 
    confirm=False
)
```

**WARNING: Confirmation Required**

You've requested to safely delete the "staging" workspace in "example-org". This operation:
- Will only proceed if the workspace is not managing any resources
- Will fail if there are resources under management
- Will delete all workspace configurations and variables
- Cannot be undone

To proceed with the safe deletion, please confirm.

**User**: Yes, proceed with the safe delete

**Claude**: I'll proceed with the safe deletion of the "staging" workspace.

```python
delete_response = await safe_delete_workspace(
    organization="example-org", 
    workspace_name="staging", 
    confirm=True
)
```

**Safe Deletion Successful**

The "staging" workspace in "example-org" has been safely deleted. The workspace had no infrastructure resources under management, so the deletion was allowed to proceed.

All workspace configurations, variables, and settings have been removed. The operation completed successfully.

## Workspace Locking and Unlocking

**User**: Lock my "production" workspace while we do maintenance

**Claude**: I'll lock the "production" workspace to prevent any changes during your maintenance period.

```python
lock_response = await lock_workspace(
    organization="example-org",
    workspace_name="production",
    reason="Scheduled maintenance in progress"
)
```

**Workspace Locked**

I've successfully locked the "production" workspace in "example-org". While locked:
- No new runs can be queued
- Existing runs in progress will continue until completion
- The workspace will remain locked until explicitly unlocked

**Lock Details:**
- Workspace: production
- Locked by: Your account (admin@example.com)
- Reason: Scheduled maintenance in progress
- Locked at: [Current timestamp]

The workspace will remain locked until you request it to be unlocked.

**User**: The maintenance is complete, unlock "production" now

**Claude**: I'll unlock the "production" workspace now that maintenance is complete.

```python
unlock_response = await unlock_workspace(
    organization="example-org",
    workspace_name="production"
)
```

**Workspace Unlocked**

The "production" workspace in "example-org" has been successfully unlocked. Normal operations can now resume:
- New runs can be queued
- Automatic runs will trigger as configured
- VCS-triggered runs will process normally

The workspace is now available for use.

**User**: Someone left "staging" locked and they're out today. Can you force unlock it?

**Claude**: I'll force unlock the "staging" workspace since the person who locked it is unavailable today.

```python
force_unlock_response = await force_unlock_workspace(
    organization="example-org",
    workspace_name="staging"
)
```

**Workspace Force Unlocked**

I've successfully force unlocked the "staging" workspace in "example-org". The workspace was previously locked by jane@example.com with reason "Testing configuration changes".

The force unlock has:
- Removed the lock regardless of who placed it
- Made the workspace available for immediate use
- Allowed new runs to be queued

The workspace is now unlocked and available for normal operations. Note that force unlocking should only be done in situations like this where the original locker is unavailable.