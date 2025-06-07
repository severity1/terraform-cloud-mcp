# Plan Management Tools

This module provides tools for retrieving information about Terraform plans.

## Overview

A plan in Terraform Cloud contains information about the changes Terraform will make to your infrastructure, including resources to add, change, or delete. Plans represent the execution plan that Terraform generates during a run before any changes are applied.

## API Reference

These tools interact with the Terraform Cloud Plan API:
- [Plan API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/plans)
- [Run Workflow](https://developer.hashicorp.com/terraform/cloud-docs/run/states)

## Tools Reference

### get_plan_details

**Function:** `get_plan_details(plan_id: str) -> Dict[str, Any]`

**Description:** Retrieves comprehensive information about a specific plan including its status, resource counts, and timestamps.

**Parameters:**
- `plan_id` (str): The ID of the plan to retrieve details for (format: "plan-xxxxxxxx")

**Returns:** JSON response containing plan details including:
- Status (queued, running, errored, canceled, finished)
- Status timestamps (queued-at, started-at, finished-at)
- Resource statistics (additions, changes, destructions)
- Log read URL
- Relationships to runs and configuration versions

**Notes:**
- Plan IDs can be found in the relationships of a run object
- Successful plans have a status of "finished"
- The log-read-url is a pre-signed URL to access the full plan logs
- Resource counts are useful for understanding the impact of changes

### get_plan_json_output

**Function:** `get_plan_json_output(plan_id: str) -> Dict[str, Any]`

**Description:** Retrieves the JSON representation of a plan's execution details.

**Parameters:**
- `plan_id` (str): The ID of the plan to retrieve JSON output for (format: "plan-xxxxxxxx")

**Returns:** Machine-readable JSON format of the plan containing:
- Detailed resource changes
- Provider configurations
- Output changes
- Variables values used
- Complete planned actions in structured format

**Notes:**
- Automatically follows HTTP redirects to retrieve the plan JSON content
- Ideal for programmatic analysis of infrastructure changes
- Contains much more detailed information than the summary in plan details
- Useful for custom validation or visualization of changes

### get_run_plan_json_output

**Function:** `get_run_plan_json_output(run_id: str) -> Dict[str, Any]`

**Description:** Retrieves the JSON representation of a run's current plan execution details.

**Parameters:**
- `run_id` (str): The ID of the run to retrieve plan JSON output for (format: "run-xxxxxxxx")

**Returns:** Same JSON plan format as get_plan_json_output but referenced by run ID.

**Notes:**
- Provides the same JSON plan data as get_plan_json_output
- Useful when you only have the run ID and not the plan ID
- Automatically follows HTTP redirects to retrieve the content
- Returns the current plan for the run

### get_plan_logs

**Function:** `get_plan_logs(plan_id: str) -> Dict[str, Any]`

**Description:** Retrieves the raw log output from a Terraform plan operation.

**Parameters:**
- `plan_id` (str): The ID of the plan to retrieve logs for (format: "plan-xxxxxxxx")

**Returns:** Text content of the plan logs including:
- Terraform output during planning
- Resource change details in human-readable format
- Warnings and errors that occurred during planning

**Notes:**
- Handles HTTP redirects automatically to retrieve the log content
- Useful for troubleshooting plan failures
- Contains the same output as displayed in Terraform Cloud UI
- May include sensitive information depending on your code

**Common Error Scenarios:**

| Error | Cause | Solution |
|-------|-------|----------|
| 404 | Plan not found | Verify the plan ID is correct |
| 403 | Insufficient permissions | Ensure your token has read access to the workspace |
| 422 | Invalid plan ID format | Ensure the ID follows the format "plan-xxxxxxxx" |