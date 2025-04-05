# Apply Management Tools

This document describes the tools available for managing applies in Terraform Cloud.

## Overview

Applies in Terraform Cloud represent the execution phase of a Terraform run after the plan has been approved. These tools allow retrieving information about applies and recovering from failed state uploads.

## Tools

### get_apply_details

Retrieves detailed information about an apply including its status, resource counts, and timestamps.

```python
from terraform_cloud_mcp.tools.applies import get_apply_details

# Get details about a specific apply
apply_details = await get_apply_details(apply_id="apply-1234567890abcdef")

# Access apply information
status = apply_details["data"]["attributes"]["status"]
log_read_url = apply_details["data"]["attributes"]["log-read-url"]
resource_additions = apply_details["data"]["attributes"]["resource-additions"]
resource_changes = apply_details["data"]["attributes"]["resource-changes"]
resource_destructions = apply_details["data"]["attributes"]["resource-destructions"]

# Check if the apply has finished
if status == "finished":
    print(f"Apply completed successfully with {resource_changes} resources changed")
elif status == "errored":
    print("Apply encountered an error")
```

### get_errored_state

Retrieves information about a state file that failed to upload during an apply, enabling state recovery.

```python
from terraform_cloud_mcp.tools.applies import get_errored_state

# Get errored state information
state_info = await get_errored_state(apply_id="apply-1234567890abcdef")

# The redirect to the state file is automatically followed by the client
# so the response contains the actual state data
if "terraform_state" in state_info:
    # State data was successfully retrieved
    resources = state_info["terraform_state"]["resources"]
    print(f"Retrieved state data containing {len(resources)} resources")
else:
    # Error retrieving state or no errored state exists
    print("No errored state found or access denied")
```

## Error Handling

All functions use the `handle_api_errors` decorator which ensures consistent error handling:

- HTTP 401/403 errors are converted to authentication/permission errors
- HTTP 404 errors return clear "not found" messages
- HTTP 422 errors provide validation failure details
- Other HTTP errors include status code and message
- Network and timeout errors are properly handled

## Response Format

All tools return API responses in the standard JSON:API format used by Terraform Cloud:

```json
{
  "data": {
    "id": "apply-1234567890abcdef",
    "type": "applies",
    "attributes": {
      "status": "finished",
      "status-timestamps": {
        "queued-at": "2023-05-20T15:23:21+00:00",
        "started-at": "2023-05-20T15:24:10+00:00",
        "finished-at": "2023-05-20T15:25:45+00:00"
      },
      "log-read-url": "https://app.terraform.io/api/v2/applies/apply-1234567890abcdef/log",
      "resource-additions": 3,
      "resource-changes": 5,
      "resource-destructions": 2
    },
    "relationships": {
      "state-versions": {
        "data": [
          {
            "id": "sv-1234567890abcdef",
            "type": "state-versions"
          }
        ]
      }
    }
  }
}
```

For errored state requests, the response will contain the state data directly:

```json
{
  "terraform_state": {
    "version": 4,
    "terraform_version": "1.4.6",
    "serial": 15,
    "lineage": "12345678-90ab-cdef-1234-567890abcdef",
    "resources": [
      {
        "mode": "managed",
        "type": "aws_instance",
        "name": "example",
        "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
        "instances": [
          {
            "schema_version": 1,
            "attributes": {
              "id": "i-1234567890abcdef",
              "instance_type": "t2.micro",
              "ami": "ami-1234567890abcdef"
            }
          }
        ]
      }
    ]
  }
}
```

## See Also

- [Apply Models Documentation](../models/apply_examples.md)
- [Run Management Tools](./run_tools.md)
- [Plan Management Tools](./plan_tools.md)
- [Terraform Cloud API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies)