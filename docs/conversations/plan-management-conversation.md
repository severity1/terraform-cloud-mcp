# Plan Management Conversation Examples

This document provides example conversations demonstrating how to use the plan management tools in the Terraform Cloud MCP.

## Getting Plan Details

```
User: I'd like to see details for my plan with ID plan-aBcdEfGh12345678

Claude: I'll retrieve the details for that plan for you.

[Tool use: get_plan_details with plan_id="plan-aBcdEfGh12345678"]

Claude: Here are the details for plan-aBcdEfGh12345678:

Status: finished
Resources to add: 3
Resources to change: 1  
Resources to destroy: 0

The plan was queued at 2025-02-15T14:30:22Z, started at 2025-02-15T14:31:05Z, and finished at 2025-02-15T14:32:18Z.

It's associated with run-pQrStUvW12345678 in workspace "production-infrastructure".
```

## Retrieving Plan JSON Output

```
User: Can you get me the JSON execution output for plan-aBcdEfGh12345678? I need to analyze the changes.

Claude: I'll retrieve the JSON execution plan for you.

[Tool use: get_plan_json_output with plan_id="plan-aBcdEfGh12345678"]

Claude: I've obtained the JSON execution plan. Here's an analysis of the planned changes:

The plan includes:
- 2 resources to be created (aws_s3_bucket.data and aws_iam_role.lambda_role)
- 1 resource to be modified (aws_security_group.allow_http)
- 0 resources to be destroyed

Key modifications:
- The security group is having a new ingress rule added for HTTPS (port 443)
- The new S3 bucket will have versioning enabled
- The IAM role has permissions for Lambda and S3 access

The plan was generated with Terraform 1.5.7 and includes all configuration details and state information. Would you like me to extract any specific part of the plan for more detailed analysis?
```

## Retrieving Run Plan JSON Output

```
User: I'm working with a run ID run-xYzAbCdE12345678 and need the JSON execution plan from that run.

Claude: I'll get the JSON plan output from that run for you.

[Tool use: get_run_plan_json_output with run_id="run-xYzAbCdE12345678"]

Claude: I've retrieved the JSON execution plan for run-xYzAbCdE12345678. This is a destruction plan that will remove the following resources:

- aws_instance.web_server (EC2 instance)
- aws_security_group.web_access
- aws_s3_bucket.logs
- aws_cloudwatch_metric_alarm.high_cpu

The plan was generated with Terraform version 1.6.2. All four resources will be completely removed, and the state will be updated accordingly. 

The plan shows that this will remove:
- 1 EC2 t2.micro instance in us-west-2
- 1 security group with 3 ingress rules
- 1 S3 bucket containing approximately 250MB of log data
- 1 CloudWatch alarm that was monitoring the EC2 instance

Would you like me to extract any specific details from the plan?
```

## Working with Plan Status

```
User: My plan seems to be taking a long time. The ID is plan-mNoPqRsT12345678. What's its status?

Claude: Let me check the status of that plan for you.

[Tool use: get_plan_details with plan_id="plan-mNoPqRsT12345678"]

Claude: Your plan with ID plan-mNoPqRsT12345678 is currently in the "running" status. 

It was queued at 2025-03-01T09:15:33Z and started execution at 2025-03-01T09:16:10Z (about 25 minutes ago).

This plan is running in an agent execution mode on agent "prod-deployment-agent-05" in the "Production" agent pool. Complex plans with many resources can take time to complete, especially if there are many computed values or external data sources.

Would you like me to check if there are any logs available that might provide more information about the progress?
```

## Analyzing Plan Resources

```
User: I need to understand what resources will be created in plan-gHiJkLmN12345678

Claude: I'll retrieve and analyze the plan details for you.

[Tool use: get_plan_details with plan_id="plan-gHiJkLmN12345678"]

Claude: The plan plan-gHiJkLmN12345678 will create 5 new resources:

- 2 aws_security_group resources
- 1 aws_instance (EC2) resource
- 1 aws_s3_bucket resource
- 1 aws_iam_role resource

The plan will also modify 2 existing resources and destroy 1 resource.

This plan was created as part of run-eFgHiJkL12345678 in workspace "network-infrastructure" and has already finished execution. It's ready to be applied.

For more detailed analysis of the exact resource configurations, I can retrieve the JSON execution plan which contains the full definition of all resource changes.
```

## Comparing Multiple Plans

```
User: I have two plans I want to compare: plan-qRsTuVwX12345678 and plan-yZaBcDeF12345678

Claude: I'll retrieve both plans and compare them for you.

[Tool use: get_plan_details with plan_id="plan-qRsTuVwX12345678"]
[Tool use: get_plan_details with plan_id="plan-yZaBcDeF12345678"]

Claude: Here's a comparison of the two plans:

Plan 1 (plan-qRsTuVwX12345678):
- Status: finished
- Resources to add: 4
- Resources to change: 2
- Resources to destroy: 1
- Execution time: 1m 45s (2025-03-10)
- Run: run-aBcDeFgH12345678

Plan 2 (plan-yZaBcDeF12345678):
- Status: finished
- Resources to add: 4
- Resources to change: 3
- Resources to destroy: 0
- Execution time: 2m 12s (2025-03-15)
- Run: run-iJkLmNoP12345678

The second plan (from March 15) modifies one additional resource compared to the first plan (from March 10), but doesn't destroy any resources. Both plans add the same number of new resources.

To see exactly what changed between these plans, I can retrieve and compare the JSON output for both.
```