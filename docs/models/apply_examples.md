# Apply Models Examples

This document provides examples of using the models for Terraform Cloud apply operations.

## Status Enum

The `ApplyStatus` enum represents the possible states of an apply operation:

```python
from terraform_cloud_mcp.models import ApplyStatus

# Check the status of an apply
if apply_response["data"]["attributes"]["status"] == ApplyStatus.FINISHED:
    print("Apply completed successfully")
elif apply_response["data"]["attributes"]["status"] == ApplyStatus.ERRORED:
    print("Apply encountered an error")
elif apply_response["data"]["attributes"]["status"] == ApplyStatus.RUNNING:
    print("Apply is currently executing")
```

## Request Models

### Apply Request

The `ApplyRequest` model validates parameters for retrieving apply details:

```python
from terraform_cloud_mcp.models import ApplyRequest

# Valid apply ID
try:
    params = ApplyRequest(apply_id="apply-1234567890abcdef")
    print(f"Validated apply ID: {params.apply_id}")
except ValueError as e:
    print(f"Invalid apply ID: {e}")

# Invalid apply ID format
try:
    params = ApplyRequest(apply_id="invalid-format")
    # This will raise an exception
except ValueError as e:
    print(f"Invalid apply ID format: {e}")
```

### Errored State Request

The `ApplyErroredStateRequest` model validates parameters for retrieving errored state information:

```python
from terraform_cloud_mcp.models import ApplyErroredStateRequest

# Valid apply ID
try:
    params = ApplyErroredStateRequest(apply_id="apply-1234567890abcdef")
    print(f"Validated apply ID for errored state request: {params.apply_id}")
except ValueError as e:
    print(f"Invalid apply ID: {e}")
```

## Supporting Models

### Apply Execution Details

The `ApplyExecutionDetails` model captures execution-specific information for agent runs:

```python
from terraform_cloud_mcp.models import ApplyExecutionDetails

# Extract execution details from API response
execution_data = apply_response["data"]["attributes"]["execution-details"]

# Create model instance
execution_details = ApplyExecutionDetails(
    agent_id=execution_data.get("agent-id"),
    agent_name=execution_data.get("agent-name"),
    agent_pool_id=execution_data.get("agent-pool-id"),
    agent_pool_name=execution_data.get("agent-pool-name")
)

# Access model properties
if execution_details.agent_pool_name:
    print(f"Apply executed by agent in pool: {execution_details.agent_pool_name}")
if execution_details.agent_name:
    print(f"Apply executed by agent: {execution_details.agent_name}")
```

### Apply Status Timestamps

The `ApplyStatusTimestamps` model captures timing information for an apply's lifecycle:

```python
from terraform_cloud_mcp.models import ApplyStatusTimestamps
from datetime import datetime
import iso8601

# Extract timestamp data from API response
timestamp_data = apply_response["data"]["attributes"]["status-timestamps"]

# Create model instance
timestamps = ApplyStatusTimestamps(
    queued_at=timestamp_data.get("queued-at"),
    started_at=timestamp_data.get("started-at"),
    finished_at=timestamp_data.get("finished-at")
)

# Calculate duration if apply is complete
if timestamps.finished_at and timestamps.started_at:
    start_time = iso8601.parse_date(timestamps.started_at)
    end_time = iso8601.parse_date(timestamps.finished_at)
    duration = (end_time - start_time).total_seconds()
    print(f"Apply completed in {duration} seconds")

# Check if the apply was queued for a long time
if timestamps.queued_at and timestamps.started_at:
    queue_time = iso8601.parse_date(timestamps.started_at)
    queue_start = iso8601.parse_date(timestamps.queued_at)
    queue_duration = (queue_time - queue_start).total_seconds()
    print(f"Apply was queued for {queue_duration} seconds")
```

## Complete API Usage Example

Here's a comprehensive example showing how these models can be used together:

```python
from terraform_cloud_mcp.tools.applies import get_apply_details
from terraform_cloud_mcp.models import ApplyStatus, ApplyExecutionDetails, ApplyStatusTimestamps
import iso8601
from datetime import datetime

async def analyze_apply(apply_id):
    # Get the apply details
    apply_data = await get_apply_details(apply_id)
    
    # Extract attributes
    attributes = apply_data["data"]["attributes"]
    status = attributes["status"]
    
    # Check status using enum
    if status == ApplyStatus.FINISHED:
        print("Apply completed successfully")
        
        # Get resource counts
        additions = attributes.get("resource-additions", 0)
        changes = attributes.get("resource-changes", 0)
        destructions = attributes.get("resource-destructions", 0)
        print(f"Resources: {additions} added, {changes} changed, {destructions} destroyed")
        
        # Extract timestamps
        timestamp_data = attributes.get("status-timestamps", {})
        timestamps = ApplyStatusTimestamps(
            queued_at=timestamp_data.get("queued-at"),
            started_at=timestamp_data.get("started-at"),
            finished_at=timestamp_data.get("finished-at")
        )
        
        # Calculate duration
        if timestamps.finished_at and timestamps.started_at:
            start_time = iso8601.parse_date(timestamps.started_at)
            end_time = iso8601.parse_date(timestamps.finished_at)
            duration = (end_time - start_time).total_seconds()
            print(f"Apply completed in {duration} seconds")
            
        # Check execution details
        if "execution-details" in attributes:
            execution_data = attributes["execution-details"]
            execution_details = ApplyExecutionDetails(
                agent_id=execution_data.get("agent-id"),
                agent_name=execution_data.get("agent-name"),
                agent_pool_id=execution_data.get("agent-pool-id"),
                agent_pool_name=execution_data.get("agent-pool-name")
            )
            
            if execution_details.agent_name:
                print(f"Apply executed by agent: {execution_details.agent_name}")
    
    elif status == ApplyStatus.ERRORED:
        print("Apply encountered an error")
        # Here you might want to retrieve the errored state
        
    elif status == ApplyStatus.RUNNING:
        print("Apply is currently executing")
```

## See Also

- [Apply Tools Documentation](../tools/apply_tools.md)
- [Terraform Cloud API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies)