# State Management Conversation Example

This document demonstrates how to use the State Management tools in Terraform Cloud MCP.

## Scenario: Working with State Versions and Their Outputs

In this scenario, we'll show how to:
1. List state versions for a workspace
2. Get details of the current state version
3. Extract output values from the state
4. Create a new state version
5. Download a state file

### Conversation

```
**User:** I need to examine the state versions in my "production" workspace and understand the outputs in the current state.

**Claude:** I'll help you examine the state versions in your production workspace. Let me start by listing all the state versions.

[Claude uses list_state_versions tool]

I found 15 state versions in your production workspace. Here are the most recent ones:

- State version 15 created on 2024-03-15 at 14:30 UTC (status: finalized)
- State version 14 created on 2024-03-10 at 09:15 UTC (status: finalized)  
- State version 13 created on 2024-03-08 at 16:45 UTC (status: finalized)

Now let me get the details of your current state version to understand what's deployed.

[Claude uses get_workspace_details tool]
[Claude uses get_current_state_version tool]

Your current state (ID: sv-abc123def456) is at serial 15 and was created with Terraform version 1.6.2. It contains 47 managed resources including VPCs, security groups, EC2 instances, and RDS databases.

Let me examine the outputs from this state version.

[Claude uses list_state_version_outputs tool]

Here are the outputs from your current state:

- vpc_id (string): vpc-1234567890abcdef
- database_endpoint (string): prod-db.abc123.us-east-1.rds.amazonaws.com
- load_balancer_dns (string): prod-alb-123456789.us-east-1.elb.amazonaws.com
- database_password (string): [SENSITIVE]
- api_key (string): [SENSITIVE]

The state includes 5 outputs total, with 2 marked as sensitive for security.
```

```
**User:** I need to create a new state version for this workspace. I have a state file exported from my local environment that I want to upload.

**Claude:** I'll help you create a new state version for your workspace using your local state file. This process requires several steps to ensure the state is properly uploaded and validated.

First, I need to lock the workspace since state version creation requires exclusive access.

[Claude uses lock_workspace tool]

The workspace is now locked with the reason "Uploading new state version from local environment".

Now I'll create the new state version using your local state file. I've processed your terraform.tfstate file and extracted the necessary information:

- Serial number: 16 (incremented from current state)
- MD5 hash: d41d8cd98f00b204e9800998ecf8427e  
- Lineage: 871d1b4a-e579-fb7c-ffdb-f0c858a647a7

[Claude uses create_state_version tool]

Great! I've successfully created the new state version with ID: sv-xyz789abc123. The state has been uploaded and is now being processed by Terraform Cloud.

Let me unlock the workspace now that the upload is complete.

[Claude uses unlock_workspace tool]

The workspace is now unlocked and your new state version is active. The state contains 52 resources (5 more than the previous version) and includes the changes from your local environment.
```

```
**User:** I want to see what resources are included in one of our state versions. Can I download a specific state version and examine it?

**Claude:** Absolutely! I can help you examine the contents of a specific state version. Let me get the details of a state version and show you what resources it contains.

Let me start by getting the details of state version sv-abc123def456:

[Claude uses get_state_version tool]

Great! This state version has been fully processed and contains detailed resource information. Here's what I found:

**Resources in state (47 total):**
- aws_vpc.main
- aws_subnet.public_1a  
- aws_subnet.public_1b
- aws_security_group.web
- aws_security_group.database
- aws_instance.web_server_1
- aws_instance.web_server_2
- aws_db_instance.main
- aws_load_balancer.main
- aws_route53_record.main
- And 37 more resources...

**Modules used:**
- root module: 35 resources
- module.networking: 8 resources  
- module.security: 4 resources

**Providers in state:**
- hashicorp/aws: 45 resources
- hashicorp/random: 2 resources

Now let me download the actual state file so you can examine it locally:

[Claude uses download_state_file tool]

I've downloaded the raw state file successfully. The state contains all the resource configurations and current values.

I can also download it in JSON format since this state was created with Terraform 1.6.2:

[Claude uses download_state_file tool with JSON format]

Perfect! I've downloaded both the raw state file and the JSON-formatted version. The JSON format is easier to parse and examine programmatically.

The state file has been saved locally as "downloaded_state.tfstate" for your inspection. You can now examine all the resource details, dependencies, and current values managed by Terraform.
```

## Summary

In this conversation, we demonstrated how to:

1. **List state versions** - View all state versions in a workspace with their creation dates and status
2. **Examine current state** - Get details about the active state version including resource counts and Terraform version
3. **Review state outputs** - Access output values from the state, with proper handling of sensitive values
4. **Create new state versions** - Upload state from local environments with proper workspace locking
5. **Download and analyze state** - Retrieve state files in both raw and JSON formats for detailed examination

These operations help in managing Terraform state, examining infrastructure outputs, and troubleshooting state-related issues without requiring technical implementation knowledge.