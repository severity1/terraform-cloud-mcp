# Plan Management Tools

The Terraform Cloud MCP provides tools for retrieving plan details and JSON output. Plans represent the execution plan that Terraform generates during a run.

## Overview

A plan in Terraform Cloud contains information about the changes Terraform will make to your infrastructure, including resources to add, change, or delete. The plan tools allow you to:

1. Retrieve detailed information about a plan
2. Get plan JSON output for machine-readable analysis
3. Get a plan's JSON output from a run

## Usage Examples

### Get Plan Details

```python
# Get details about a specific plan
plan_details = await get_plan_details(plan_id="plan-AbCdEfGhIjKlMnOp")

# Access plan information
status = plan_details["data"]["attributes"]["status"]
resource_additions = plan_details["data"]["attributes"]["resource-additions"]
resource_changes = plan_details["data"]["attributes"]["resource-changes"]
resource_destructions = plan_details["data"]["attributes"]["resource-destructions"]
```

### Get Plan JSON Output

```python
# Get JSON formatted plan output
plan_json = await get_plan_json_output(plan_id="plan-AbCdEfGhIjKlMnOp")

# The response contains the complete plan data
resource_changes = plan_json["resource_changes"]
terraform_version = plan_json["terraform_version"]

# This data can be parsed and analyzed programmatically
```

### Get Run Plan JSON Output

```python
# Get JSON formatted plan output from a run
run_plan_json = await get_run_plan_json_output(run_id="run-AbCdEfGhIjKlMnOp")

# The response contains the complete plan data
resource_changes = run_plan_json["resource_changes"]
terraform_version = run_plan_json["terraform_version"]

# This data can be parsed and analyzed programmatically
```

## API Reference

### get_plan_details

Get details for a specific plan.

**Parameters:**
- `plan_id` (string, required): The ID of the plan to retrieve (format: "plan-xxxxxxxx")

**Returns:**
- Plan details including status, timestamps, and resource change counts

### get_plan_json_output

Retrieve the JSON execution plan.

**Parameters:**
- `plan_id` (string, required): The ID of the plan to retrieve JSON output for (format: "plan-xxxxxxxx")

**Returns:**
- The complete JSON formatted plan with resource changes, metadata, and planned actions

### get_run_plan_json_output

Retrieve the JSON execution plan from a run.

**Parameters:**
- `run_id` (string, required): The ID of the run to retrieve plan JSON output for (format: "run-xxxxxxxx")

**Returns:**
- The complete JSON formatted plan with resource changes, metadata, and planned actions