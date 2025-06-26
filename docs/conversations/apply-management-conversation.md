# Apply Management Conversation Examples

This document provides example conversations demonstrating how to use the apply management tools in the Terraform Cloud MCP.

## Getting Apply Details

```
**User:** I'd like to check on the status of an apply in my Terraform Cloud workspace. The apply ID is apply-gH2Ns7VBP9a2QMcr

**Claude:** I'll retrieve the details for that apply for you.

[Claude uses get_apply_details tool]

Here are the details for apply-gH2Ns7VBP9a2QMcr:

Status: finished
Resources added: 3
Resources changed: 1  
Resources destroyed: 0

The apply was queued at 2023-11-15T14:31:05Z, started at 2023-11-15T14:32:18Z, and finished at 2023-11-15T14:35:42Z.

The operation took about 3 minutes and 24 seconds to complete.
```

## Retrieving Apply Logs

```
**User:** Can you show me the logs for apply-gH2Ns7VBP9a2QMcr? I want to see what changes were made.

**Claude:** I'll retrieve the logs for that apply.

[Claude uses get_apply_logs tool]

Here are the logs from the apply:

The apply used Terraform v1.4.6 on linux and successfully completed the following actions:

- Created an AWS security group (sg-0a1b2c3d4e5f6g7h8) in 3 seconds
- Created an AWS instance for the web server (i-0a1b2c3d4e5f6g7h8) which took 30 seconds
- Created an S3 bucket for logs (my-example-logs-bucket) in 5 seconds
- Modified a security group rule to allow HTTPS traffic in 2 seconds

The apply completed successfully with 3 resources added and 1 resource changed, taking about 40 seconds total.

Would you like me to explain any specific part of the apply process?
```

## Working with Errored States

```
**User:** I found an apply with an error: apply-rT5Kp2VsMx3zNPqf. Can you check if there's a failed state to recover?

**Claude:** I'll check if there's an errored state for that apply that we can recover.

[Claude uses get_errored_state tool]

I found the failed state upload for apply-rT5Kp2VsMx3zNPqf. It contains state data for 12 resources.

The state version is 4, and it includes resources like:
- aws_vpc.main (vpc-0a1b2c3d)
- aws_subnet.public (2 instances)
- aws_subnet.private (2 instances)
- aws_route_table.public
- aws_route_table.private
- aws_internet_gateway.main
- aws_security_group.web
- aws_instance.app_server (2 instances)
- aws_s3_bucket.logs

This state can be recovered to prevent drift between what Terraform Cloud knows about your infrastructure and what actually exists. Would you like me to help with the recovery process?
```

## Understanding Apply Failures

```
**User:** Can you check the details of apply-xYz123AbCd and tell me why it failed?

**Claude:** I'll examine what went wrong with that apply.

[Claude uses get_apply_details tool]
[Claude uses get_apply_logs tool]

I've analyzed the failed apply. Here's what happened:

The apply failed during resource creation with error code 403 (Forbidden).

The specific error occurred while creating an AWS IAM role:
- Resource: aws_iam_role.lambda_execution_role
- Error: "AccessDenied: User is not authorized to perform iam:CreateRole"

The Terraform credentials being used don't have sufficient permissions to create IAM roles. The apply attempted to create 3 resources but failed after creating the first 2 (an S3 bucket and Lambda function), failing on the IAM role creation.

To resolve this, you'll need to either:
1. Add IAM permissions to the credentials being used
2. Have someone with appropriate permissions create the IAM role separately
3. Use a different approach that doesn't require creating new IAM roles
```

## Comparing Multiple Applies

```
**User:** Can you compare the details of two different applies for me? apply-8HqpY2tKnGbR5xVz and apply-cJm3L7sWvZ4dNfQk

**Claude:** I'll retrieve and compare the details of both applies.

[Claude uses get_apply_details tool]
[Claude uses get_apply_details tool]

Here's a comparison of the two applies:

Apply 1 (apply-8HqpY2tKnGbR5xVz):
- Status: finished
- Duration: 4m 12s
- Resources Added: 8
- Resources Changed: 3
- Resources Destroyed: 0
- Total Actions: 11
- Started: 2025-03-10T15:22:18Z

Apply 2 (apply-cJm3L7sWvZ4dNfQk):
- Status: finished
- Duration: 2m 38s
- Resources Added: 2
- Resources Changed: 5
- Resources Destroyed: 4
- Total Actions: 11
- Started: 2025-03-15T09:45:32Z

Key differences:
- Apply 2 completed faster (2m 38s vs 4m 12s)
- Apply 1 created more resources (8 vs 2)
- Apply 2 destroyed resources (4) while Apply 1 had none
- Both applies had the same total number of resource actions (11)

Would you like me to analyze any specific aspect of these applies in more detail?
```