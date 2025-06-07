# Apply Management Tools

This module provides tools for managing applies in Terraform Cloud.

## Overview

Applies in Terraform Cloud represent the execution phase of a Terraform run after the plan has been approved. These tools allow retrieving information about applies and recovering from failed state uploads.

## API Reference

These tools interact with the Terraform Cloud Apply API:
- [Apply API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies)
- [Run Lifecycle](https://developer.hashicorp.com/terraform/cloud-docs/run/states)

## Tools Reference

### get_apply_details

**Function:** `get_apply_details(apply_id: str) -> Dict[str, Any]`

**Description:** Retrieves comprehensive information about an apply operation including its status, resource counts, and timestamps.

**Parameters:**
- `apply_id` (str): The ID of the apply to retrieve details for (format: "apply-xxxxxxxx")

**Returns:** JSON response containing apply details including:
- Status (queued, running, errored, canceled, finished)
- Status timestamps (queued-at, started-at, finished-at)
- Resource statistics (additions, changes, destructions)
- Log read URL
- Relationships to state versions and runs

**Notes:**
- Apply IDs can be found in the relationships of a run object
- Successful applies have a status of "finished"
- The log-read-url is a pre-signed URL to access the full apply logs
- Resource counts help track infrastructure changes

### get_apply_logs

**Function:** `get_apply_logs(apply_id: str) -> Dict[str, Any]`

**Description:** Retrieves the raw log output from a specific apply operation.

**Parameters:**
- `apply_id` (str): The ID of the apply to retrieve logs for (format: "apply-xxxxxxxx")

**Returns:** Text content of the apply logs including:
- Terraform output during apply
- Resource creation/modification details
- Error messages (if any occurred)
- Complete execution trace

**Notes:**
- Handles HTTP redirects automatically
- Useful for debugging failed applies
- Contains detailed information about each resource change
- Can be large for complex infrastructures

### get_errored_state

**Function:** `get_errored_state(apply_id: str) -> Dict[str, Any]`

**Description:** Retrieves information about a state file that failed to upload during an apply, enabling state recovery.

**Parameters:**
- `apply_id` (str): The ID of the apply with a failed state upload (format: "apply-xxxxxxxx")

**Returns:** Terraform state data that was not successfully uploaded, including:
- Complete state representation
- Resource definitions and attributes
- Terraform version information
- State metadata (serial, lineage)

**Notes:**
- Critical for recovering from failed state uploads
- Only available when a state upload has failed
- Allows administrators to manually recover state information
- Handles HTTP redirects automatically to retrieve the state data

**Common Error Scenarios:**

| Error | Cause | Solution |
|-------|-------|----------|
| 404 | Apply not found or no errored state | Verify the apply ID is correct and that it has a failed state |
| 403 | Insufficient permissions | Ensure your token has admin or state access permissions |
| 422 | Invalid apply ID format | Ensure the ID follows the format "apply-xxxxxxxx" |