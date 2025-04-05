# Apply Management Conversation

This document illustrates how to interact with the apply management tools through a conversation with an AI assistant.

## Conversation Flow

**User**: I'd like to check on the status of an apply in my Terraform Cloud workspace.

**Assistant**: I can help you check the status of an apply. To get the details of a specific apply, I'll need its ID. Apply IDs typically start with "apply-" followed by a string of alphanumeric characters.

**User**: The apply ID is apply-gH2Ns7VBP9a2QMcr

**Assistant**: I'll retrieve the details for that apply for you.

```python
from terraform_cloud_mcp.tools.applies import get_apply_details

apply_info = await get_apply_details(apply_id="apply-gH2Ns7VBP9a2QMcr")
```

Looking at the details:

- Status: finished
- Resources added: 3
- Resources changed: 1
- Resources destroyed: 0
- Started at: 2023-11-15T14:32:18Z
- Finished at: 2023-11-15T14:35:42Z

The apply has completed successfully, adding 3 resources and modifying 1 resource. The operation took about 3 minutes and 24 seconds to complete.

**User**: Great! Can you also check if there have been any errors with the last few applies?

**Assistant**: I'll check the recent applies with errors.

```python
from terraform_cloud_mcp.tools.runs import list_runs_in_workspace
from terraform_cloud_mcp.models import ApplyStatus

# Assuming we know the workspace ID
runs = await list_runs_in_workspace(
    workspace_id="ws-6GnbcbEA8M9wXQsR", 
    filter_status="errored"
)

# Check if there are any errored runs
if runs["meta"]["pagination"]["total-count"] > 0:
    # Get details for each errored run's apply if available
    for run in runs["data"]:
        if "apply" in run["relationships"] and run["relationships"]["apply"]["data"]:
            apply_id = run["relationships"]["apply"]["data"]["id"]
            apply_info = await get_apply_details(apply_id=apply_id)
            
            # Check if the apply itself errored
            if apply_info["data"]["attributes"]["status"] == ApplyStatus.ERRORED:
                print(f"Errored apply found: {apply_id}")
```

I found one apply with an error from yesterday: apply-rT5Kp2VsMx3zNPqf. Would you like me to check if there's a failed state upload that needs to be recovered?

**User**: Yes, please check if there's a failed state to recover.

**Assistant**: I'll check if there's an errored state for that apply that we can recover.

```python
from terraform_cloud_mcp.tools.applies import get_errored_state

try:
    errored_state = await get_errored_state(apply_id="apply-rT5Kp2VsMx3zNPqf")
    
    # If we get here, there's state data to recover
    state_version = errored_state["terraform_state"]["version"]
    resource_count = len(errored_state["terraform_state"]["resources"])
    
    print(f"Found state version {state_version} with {resource_count} resources")
    
except Exception as e:
    print(f"No errored state to recover: {e}")
```

I found the failed state upload. It contains state data for 12 resources. This state can be used to recover the workspace state to prevent drift between what Terraform knows about your infrastructure and what actually exists.

To recover this state:

1. The state data has already been retrieved by our API call
2. You can download it locally if needed by handling the response data
3. You could upload this state to the workspace manually using Terraform CLI or the state versions API

Would you like me to help you with any of these recovery steps?

**User**: No need to recover it right now, but can you check the details of the apply to see why it failed?

**Assistant**: I'll check the details of the failed apply to understand what went wrong.

```python
apply_details = await get_apply_details(apply_id="apply-rT5Kp2VsMx3zNPqf")

# Extract relevant error information
status = apply_details["data"]["attributes"]["status"]
log_read_url = apply_details["data"]["attributes"].get("log-read-url")

# Check any error messages or status notes
error_message = apply_details["data"]["attributes"].get("status-message", "No specific error message provided")
```

I've examined the failed apply. Here's what I found:

- Status: errored
- Error message: "Error uploading state: connection timeout"
- The apply operation itself completed, but there was a problem uploading the final state to Terraform Cloud
- This is why there's a recoverable errored state available

The logs indicate that the infrastructure changes were actually applied successfully, but due to a network issue, the final state couldn't be uploaded to Terraform Cloud. This means:

1. Your infrastructure was modified as planned
2. The state file wasn't properly saved to Terraform Cloud
3. This can cause drift if not resolved, as Terraform Cloud doesn't have the latest record of your infrastructure

Since we were able to retrieve the errored state earlier, you have the data needed to recover when you're ready.

**User**: That's helpful, thank you! Is there a way to check if any specific resources caused issues during the apply?

**Assistant**: Yes, I can check the apply details for information about resource failures.

```python
# Detailed analysis of resources from the apply details
resource_additions = apply_details["data"]["attributes"].get("resource-additions", 0)
resource_changes = apply_details["data"]["attributes"].get("resource-changes", 0)
resource_destructions = apply_details["data"]["attributes"].get("resource-destructions", 0)

# Get logs if available to check for specific resource errors
# Note: Full log retrieval may not be available through the API and might require
# following the log_read_url in a browser
```

From the apply details:

- Resources attempted to add: 5
- Resources successfully added: 5
- Resources attempted to change: 2
- Resources successfully changed: 2
- Resources attempted to destroy: 0

The apply process itself did not have any resource-specific failures. All resource operations completed successfully. The error occurred after all resources were successfully applied, during the state upload phase. This means:

1. All infrastructure changes were successfully applied
2. No specific resources caused problems during the apply
3. The failure happened during the state management phase

This confirms that your infrastructure is in the expected state, but Terraform Cloud's record of it is not current. When you're ready to recover, you'll need to update Terraform Cloud's state to match the actual infrastructure.

## Additional Conversations

### Comparing Apply Details

**User**: Can you compare the details of two different applies for me?

**Assistant**: I'd be happy to compare two applies for you. Please provide the two apply IDs you'd like me to compare.

**User**: apply-8HqpY2tKnGbR5xVz and apply-cJm3L7sWvZ4dNfQk

**Assistant**: I'll retrieve and compare the details of both applies.

```python
from terraform_cloud_mcp.tools.applies import get_apply_details
import iso8601
from datetime import datetime

# Get details for both applies
first_apply = await get_apply_details(apply_id="apply-8HqpY2tKnGbR5xVz")
second_apply = await get_apply_details(apply_id="apply-cJm3L7sWvZ4dNfQk")

# Extract key information for comparison
def extract_apply_info(apply_data):
    attributes = apply_data["data"]["attributes"]
    timestamps = attributes.get("status-timestamps", {})
    
    return {
        "status": attributes.get("status"),
        "started_at": timestamps.get("started-at"),
        "finished_at": timestamps.get("finished-at"),
        "duration": calculate_duration(timestamps.get("started-at"), timestamps.get("finished-at")),
        "additions": attributes.get("resource-additions", 0),
        "changes": attributes.get("resource-changes", 0),
        "destructions": attributes.get("resource-destructions", 0),
        "total_actions": (
            attributes.get("resource-additions", 0) + 
            attributes.get("resource-changes", 0) + 
            attributes.get("resource-destructions", 0)
        )
    }

def calculate_duration(start, end):
    if not start or not end:
        return None
    start_time = iso8601.parse_date(start)
    end_time = iso8601.parse_date(end)
    return (end_time - start_time).total_seconds()

# Extract and compare
first_info = extract_apply_info(first_apply)
second_info = extract_apply_info(second_apply)
```

Here's a comparison of the two applies:

| Metric | First Apply (8HqpY2) | Second Apply (cJm3L7) |
|--------|---------------------|----------------------|
| Status | finished | finished |
| Duration | 4m 12s | 2m 38s |
| Resources Added | 8 | 2 |
| Resources Changed | 3 | 5 |
| Resources Destroyed | 0 | 4 |
| Total Actions | 11 | 11 |

Key differences:
- The second apply was faster by about 1m 34s
- The first apply focused more on adding resources (8 vs 2)
- The second apply included destructions (4) while the first had none
- Both applies had the same total number of resource actions (11)

Would you like me to analyze any specific aspect of these applies in more detail?