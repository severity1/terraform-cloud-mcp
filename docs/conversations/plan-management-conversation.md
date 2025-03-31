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

Claude: I've obtained a temporary authenticated URL to download the JSON execution plan:

https://app.terraform.io/api/v2/plans/plan-aBcdEfGh12345678/json-output?token=eyJhbGciOiJ...

This URL is valid for a limited time and contains your authentication token. You can use it to download the complete plan in JSON format, which contains detailed information about all planned resource changes.

The JSON plan includes detailed resource additions (3), modifications (1), and metadata about the execution environment.
```

## Retrieving Run Plan JSON Output

```
User: I'm working with a run ID run-xYzAbCdE12345678 and need the JSON execution plan from that run.

Claude: I'll get the JSON plan output from that run for you.

[Tool use: get_run_plan_json_output with run_id="run-xYzAbCdE12345678"]

Claude: I've retrieved the JSON execution plan URL for run-xYzAbCdE12345678:

https://app.terraform.io/api/v2/runs/run-xYzAbCdE12345678/plan/json-output?token=eyJhbGciOiJ...

This temporary URL allows you to download the complete plan details in JSON format. The JSON contains comprehensive information about all planned infrastructure changes, including resource configurations, computed attributes, and dependency relationships.

You can use tools like jq to parse and analyze this JSON output for any specific information you need about the planned changes.
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