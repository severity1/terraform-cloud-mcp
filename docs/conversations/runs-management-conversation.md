# Run Management - Example Conversations

This document shows example conversations with Claude using the Terraform Cloud MCP run management features.

## Creating and Managing Runs

**User**: Create a plan for my "production" workspace

**Claude**: I'll create a plan-only run in your "production" workspace.

```python
# First, get the workspace ID for the production workspace
workspace = await get_workspace_details(
    organization="example-org",
    workspace_name="production"
)
workspace_id = workspace["data"]["id"]

# Create the run using the workspace ID
run = await create_run(
    workspace_id=workspace_id,
    message="Plan requested via Claude",
    plan_only=True
)
```

I've created a plan-only run in the "production" workspace. Here are the details:

**Run Details:**
- Run ID: run-J7cW8p2qRmYx3Dkv
- Status: Pending
- Created by: Your account (admin@example.com)
- Message: "Plan requested via Claude"
- Type: Plan only (will not auto-apply)

The run has been queued and will start shortly. Since this is a plan-only run, you'll need to review the plan output before applying any changes. I'll let you know when the plan is complete.

**User**: Create a destroy plan for "dev-test" workspace

**Claude**: I'll create a destroy plan for your "dev-test" workspace.

```python
# First, get the workspace ID for the dev-test workspace
workspace = await get_workspace_details(
    organization="example-org",
    workspace_name="dev-test"
)
workspace_id = workspace["data"]["id"]

# Create the run using the workspace ID
run = await create_run(
    workspace_id=workspace_id,
    message="Destroy plan requested via Claude",
    is_destroy=True,
    plan_only=True
)
```

I've created a destroy plan in the "dev-test" workspace. Here are the details:

**Run Details:**
- Run ID: run-L2tP6k8xZnQv1Bmj
- Status: Pending
- Created by: Your account (admin@example.com)
- Message: "Destroy plan requested via Claude"
- Type: Destroy plan (will delete all resources)
- Auto-apply: No (plan only)

This run will create a plan to destroy all resources managed by the "dev-test" workspace. Since this is a plan-only run, you'll need to review and explicitly approve the destruction before any resources are deleted.

**User**: Run a targeted plan in "staging" that only affects the database resources

**Claude**: I'll create a targeted plan in the "staging" workspace that only affects database resources.

```python
# First, get the workspace ID for the staging workspace
workspace = await get_workspace_details(
    organization="example-org",
    workspace_name="staging"
)
workspace_id = workspace["data"]["id"]

# Create the run using the workspace ID
run = await create_run(
    workspace_id=workspace_id,
    message="Targeted plan for database resources only",
    target_addrs=["module.database", "aws_rds_cluster.main", "aws_rds_instance.replicas"]
)
```

I've created a targeted plan in the "staging" workspace that will only affect database resources. Here are the details:

**Run Details:**
- Run ID: run-K3jR7m9zXpYw2Ctn
- Status: Pending
- Created by: Your account (admin@example.com)
- Message: "Targeted plan for database resources only"
- Type: Plan
- Targets: 
  - module.database
  - aws_rds_cluster.main
  - aws_rds_instance.replicas

The run has been queued and will start shortly. This plan will only show changes related to the database resources you specified. Other resources in the workspace will not be affected by this run.

**User**: Create a plan with custom variables in the "development" workspace

**Claude**: I'll create a run with custom variables in the "development" workspace.

```python
# First, get the workspace ID for the development workspace
workspace = await get_workspace_details(
    organization="example-org",
    workspace_name="development"
)
workspace_id = workspace["data"]["id"]

# Create the run using the workspace ID
run = await create_run(
    workspace_id=workspace_id,
    message="Plan with custom variable values",
    variables=[
        {"key": "environment", "value": "dev"},
        {"key": "instance_type", "value": "t3.large"},
        {"key": "enable_monitoring", "value": "true"}
    ]
)
```

I've created a plan in the "development" workspace with the custom variables you specified. Here are the details:

**Run Details:**
- Run ID: run-P8vT5q2nWxYz1Fmb
- Status: Pending
- Created by: Your account (admin@example.com)
- Message: "Plan with custom variable values"

**Custom Variables for this Run:**
- environment = "dev"
- instance_type = "t3.large"
- enable_monitoring = "true"

These custom variable values will override the workspace's default values for this specific run only. The run has been queued and will start shortly.

**User**: Create a run in "sandbox" workspace with auto-apply enabled

**Claude**: I'll create a run with auto-apply enabled in the "sandbox" workspace.

```python
# First, get the workspace ID for the sandbox workspace
workspace = await get_workspace_details(
    organization="example-org",
    workspace_name="sandbox"
)
workspace_id = workspace["data"]["id"]

# Create the run using the workspace ID
run = await create_run(
    workspace_id=workspace_id,
    message="Run with auto-apply enabled",
    auto_apply=True
)
```

I've created a run with auto-apply enabled in the "sandbox" workspace. Here are the details:

**Run Details:**
- Run ID: run-Q9wU6r3oZyXa2Gnd
- Status: Pending
- Created by: Your account (admin@example.com)
- Message: "Run with auto-apply enabled"
- Auto-apply: Yes (will automatically apply after successful plan)

The run has been queued and will start shortly. Since auto-apply is enabled for this run, it will automatically apply the changes after the plan completes successfully, without requiring manual approval.

## Listing and Viewing Runs

**User**: List all runs in my "production" workspace

**Claude**: I'll list all runs in your "production" workspace.

```python
# First, get the workspace ID for the production workspace
workspace = await get_workspace_details(
    organization="example-org", 
    workspace_name="production"
)
workspace_id = workspace["data"]["id"]

# List runs using the workspace ID
runs = await list_runs_in_workspace(
    workspace_id=workspace_id
)
```

Here are the recent runs in your "production" workspace:

1. **run-J7cW8p2qRmYx3Dkv** - "Plan requested via Claude"
   - Created: 10 minutes ago
   - Status: Planned (awaiting approval)
   - Created by: You (admin@example.com)
   - Type: Plan only

2. **run-K4jR7p9qZnYw2Lmp** - "Weekly infrastructure update"
   - Created: Yesterday at 14:32
   - Status: Applied
   - Created by: CI/CD Pipeline
   - Changes: 3 to add, 1 to change, 0 to destroy

3. **run-L5kS8q1rAoZx3Mnq** - "Security patch application"
   - Created: 3 days ago
   - Status: Applied
   - Created by: jane@example.com
   - Changes: 0 to add, 5 to change, 0 to destroy

4. **run-M6lT9r2sBpAy4Nod** - "Roll back configuration change"
   - Created: 5 days ago
   - Status: Discarded
   - Created by: john@example.com
   - Changes: 0 to add, 3 to change, 0 to destroy

5. **run-N7mU0s3tCqBz5Ope** - "Add new monitoring resources"
   - Created: 7 days ago
   - Status: Applied
   - Created by: You (admin@example.com)
   - Changes: 8 to add, 0 to change, 0 to destroy

**User**: Show me runs in "example-org" that have errored in the last month

**Claude**: I'll find runs in the "example-org" organization that have errored in the last month.

```python
error_runs = await list_runs_in_organization(
    organization="example-org",
    filter_status="errored",
    page_size=10
)
```

I found the following runs in "example-org" that have errored in the last month:

1. **run-P8vT5q2nWxYz1Fmb** - "Plan with custom variable values"
   - Workspace: development
   - Created: Today at 09:45
   - Status: Errored (Planning failed)
   - Error: "Invalid value for variable 'instance_type'"

2. **run-S9pV6u3rDsEa8Ijf** - "Deploy new database resources"
   - Workspace: prod-db-cluster
   - Created: Yesterday at 18:22
   - Status: Errored (Apply failed)
   - Error: "Error creating RDS instance: InsufficientDBInstanceCapacity"

3. **run-T0qW7v4sEtFb9Jkg** - "Update network configuration"
   - Workspace: network-infra
   - Created: 3 days ago
   - Status: Errored (Planning failed)
   - Error: "Provider configuration not found for aws"

4. **run-U1rX8w5tFuGc0Klh** - "Scale up application servers"
   - Workspace: app-servers
   - Created: 5 days ago
   - Status: Errored (Apply failed)
   - Error: "Error applying Auto Scaling configuration: ValidationError"

5. **run-V2sY9x6uGvHd1Lmi** - "Security patch deployment"
   - Workspace: security-baseline
   - Created: 2 weeks ago
   - Status: Errored (Planning timed out)
   - Error: "Terraform operation timed out after 1 hour"

**User**: Find all destroy plan runs in my organization

**Claude**: I'll find all destroy plan runs in your organization.

```python
destroy_runs = await list_runs_in_organization(
    organization="example-org",
    filter_operation="plan_and_apply",
    page_size=10
)

# We need to filter the results to find destroy runs
# Note: In a real implementation, there might be a direct filter parameter for destroy runs
```

Here are the destroy plan runs I found in the "example-org" organization:

1. **run-L2tP6k8xZnQv1Bmj** - "Destroy plan requested via Claude"
   - Workspace: dev-test
   - Created: Today at 09:32
   - Status: Planned (awaiting approval)
   - Type: Destroy (will delete all resources)
   - Created by: You (admin@example.com)

2. **run-W3tZ0y7vHwIe2Mnj** - "Decommission test environment"
   - Workspace: feature-test
   - Created: 3 days ago
   - Status: Applied
   - Type: Destroy (deleted all resources)
   - Created by: jane@example.com
   - Result: 0 to add, 0 to change, 27 to destroy

3. **run-X4uA1z8wIxJf3Nok** - "Clean up temporary resources"
   - Workspace: sandbox
   - Created: 1 week ago
   - Status: Applied
   - Type: Destroy (partial)
   - Created by: john@example.com
   - Result: 0 to add, 0 to change, 5 to destroy

4. **run-Y5vB2a9xJyKg4Opl** - "Remove deprecated services"
   - Workspace: legacy-systems
   - Created: 2 weeks ago
   - Status: Discarded
   - Type: Destroy (partial)
   - Created by: CI/CD Pipeline

**User**: Get details for run ID "run-J7cW8p2qRmYx3Dkv"

**Claude**: I'll get the details for run ID "run-J7cW8p2qRmYx3Dkv".

```python
run_details = await get_run_details(run_id="run-J7cW8p2qRmYx3Dkv")
```

Here are the details for run ID "run-J7cW8p2qRmYx3Dkv":

**Basic Information:**
- Run ID: run-J7cW8p2qRmYx3Dkv
- Status: Planned and finished (awaiting approval)
- Message: "Plan requested via Claude"
- Created: Today at 09:30 (10 minutes ago)
- Created by: You (admin@example.com)

**Workspace:**
- Name: production
- Organization: example-org
- Terraform Version: 1.5.2

**Plan Details:**
- Resources to add: 2
- Resources to change: 1
- Resources to destroy: 0
- Changes summary:
  - Adding 2 AWS Lambda functions
  - Updating IAM role permissions

**Phases:**
- Plan started: Today at 09:30:15
- Plan completed: Today at 09:31:45
- Plan duration: 90 seconds
- Apply phase: Awaiting approval

**Configuration:**
- VCS commit: 7a8b9c0d... (feat: add new lambda functions)
- Plan only: Yes (requires manual apply)
- Auto-apply: No
- Terraform Version: 1.5.2
- Working directory: /terraform

The run is currently awaiting your approval to apply the plan. You can apply it using the apply_run function with this run ID.

## Run Actions

**User**: Apply the pending run for "staging" workspace

**Claude**: I'll apply the pending run for the "staging" workspace.

```python
# First, let's find the pending run in the staging workspace
pending_runs = await list_runs_in_workspace(
    organization="example-org",
    workspace_name="staging",
    filter_status="planned"
)

# Apply the most recent pending run (first in the list)
if pending_runs and "data" in pending_runs and pending_runs["data"]:
    run_id = pending_runs["data"][0]["id"]
    apply_result = await apply_run(
        run_id=run_id,
        comment="Applied via Claude after review"
    )
```

I've applied the pending run (run-K3jR7m9zXpYw2Ctn) in the "staging" workspace. Here's the status:

**Apply Initiated:**
- Run ID: run-K3jR7m9zXpYw2Ctn
- Status: Applying
- Comment: "Applied via Claude after review"
- Action taken: Apply started

The run is now applying the planned changes to your infrastructure. The apply process typically takes a few minutes to complete. The targeted changes to your database resources are now being executed.

**User**: Cancel the run "run-P8vT5q2nWxYz1Fmb", it's taking too long

**Claude**: I'll cancel the run "run-P8vT5q2nWxYz1Fmb" that's taking too long.

```python
cancel_result = await cancel_run(
    run_id="run-P8vT5q2nWxYz1Fmb",
    comment="Cancelled due to long execution time"
)
```

I've initiated the cancellation of run "run-P8vT5q2nWxYz1Fmb". Here's the status:

**Cancellation Initiated:**
- Run ID: run-P8vT5q2nWxYz1Fmb
- Status: Cancelling
- Comment: "Cancelled due to long execution time"

The system is now gracefully stopping the run. It may take a moment to completely cancel as Terraform needs to clean up any in-progress operations. Once cancelled, the workspace will be unlocked and available for new runs.

**User**: Discard the plan for the "dev" workspace, those changes aren't needed

**Claude**: I'll discard the pending plan for the "dev" workspace.

```python
# First, let's find the pending run in the dev workspace
pending_runs = await list_runs_in_workspace(
    organization="example-org",
    workspace_name="dev",
    filter_status="planned"
)

# Discard the most recent pending run (first in the list)
if pending_runs and "data" in pending_runs and pending_runs["data"]:
    run_id = pending_runs["data"][0]["id"]
    discard_result = await discard_run(
        run_id=run_id,
        comment="Changes no longer needed"
    )
```

I've discarded the pending plan (run-Z6wC3b0yKzLh5Pqm) in the "dev" workspace. Here's the confirmation:

**Plan Discarded:**
- Run ID: run-Z6wC3b0yKzLh5Pqm
- Status: Discarded
- Comment: "Changes no longer needed"
- Created by: You (admin@example.com)

The plan has been discarded and will not be applied. The workspace is now unlocked and available for new runs. No changes were made to your infrastructure.

**User**: Force cancel the stuck run in "production"

**Claude**: I'll force cancel the stuck run in the "production" workspace.

```python
# First, let's find the stuck run in the production workspace
running_runs = await list_runs_in_workspace(
    organization="example-org",
    workspace_name="production",
    filter_status="running"
)

# Force cancel the stuck run (we'll use the first running run found)
if running_runs and "data" in running_runs and running_runs["data"]:
    run_id = running_runs["data"][0]["id"]
    
    # First we need to attempt a normal cancel
    await cancel_run(
        run_id=run_id,
        comment="Initial cancel attempt for stuck run"
    )
    
    # Then we can force cancel after the normal cancel has begun
    force_cancel_result = await force_cancel_run(
        run_id=run_id,
        comment="Force cancelling stuck run"
    )
```

I've initiated a force cancel for the stuck run (run-A7xD4c1zLaMe6Rqn) in the "production" workspace. Here's the status:

**Force Cancellation Initiated:**
- Run ID: run-A7xD4c1zLaMe6Rqn
- Status: Force cancelling
- Comment: "Force cancelling stuck run"

I first attempted a normal cancel operation, and then proceeded with the force cancel to immediately terminate the run. This will immediately unlock the workspace, allowing you to queue new runs. Note that force cancelling may leave some Terraform state operations incomplete, but it's necessary when a run is truly stuck.

**User**: I need to execute this run immediately, force execute it

**Claude**: I'll force execute a run to bypass the queue and start it immediately.

```python
# First, let's find a pending run that's waiting in the queue
pending_runs = await list_runs_in_organization(
    organization="example-org",
    filter_status="pending"
)

# Force execute the pending run (first in the list)
if pending_runs and "data" in pending_runs and pending_runs["data"]:
    run_id = pending_runs["data"][0]["id"]
    force_execute_result = await force_execute_run(run_id=run_id)
```

I've force executed the pending run (run-B8yE5d2aLbNf7Sro). Here's what happened:

**Force Execution Initiated:**
- Run ID: run-B8yE5d2aLbNf7Sro
- Status: Running (Planning)
- Workspace: deployment
- Original position: #3 in queue

The force execute command:
1. Cancelled all prior runs that were blocking this run
2. Unlocked the workspace
3. Started this run immediately

The run is now actively planning and has bypassed the queue. This is useful in urgent situations, but should be used sparingly as it cancels other queued runs.