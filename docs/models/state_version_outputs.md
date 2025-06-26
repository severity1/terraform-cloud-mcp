# State Version Outputs Models Documentation

This document describes the Pydantic models used for state version outputs operations in the Terraform Cloud MCP.

## Overview

State version outputs are the output values from a Terraform state file. They include the name and value of the output, as well as a sensitive boolean if the value should be hidden by default in UIs. State version output models are used to:

1. List outputs for a specific state version
2. Get details about a specific output

## Model Structure

### StateVersionOutputListRequest

Request model for listing outputs for a state version:

```python
class StateVersionOutputListRequest(APIRequest):
    state_version_id: str
    page_number: Optional[int] = 1
    page_size: Optional[int] = 20
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| state_version_id | str | Yes | The ID of the state version to list outputs for (format: "sv-xxxxxxxx") |
| page_number | int | No | Page number to fetch (default: 1) |
| page_size | int | No | Number of results per page (default: 20, max: 100) |

### StateVersionOutputRequest

Request model for retrieving a specific state version output:

```python
class StateVersionOutputRequest(APIRequest):
    state_version_output_id: str  # Format: "wsout-xxxxxxxxxxxxxxxx"
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| state_version_output_id | str | Yes | The ID of the state version output to retrieve (format: "wsout-xxxxxxxx") |

## Usage Examples

### Creating a request to list state version outputs

```python
from terraform_cloud_mcp.models.state_version_outputs import StateVersionOutputListRequest

# Create a request to list outputs for a state version
request = StateVersionOutputListRequest(
    state_version_id="sv-1234567890abcdef",
    page_number=1,
    page_size=20
)
```

### Creating a request to get a specific state version output

```python
from terraform_cloud_mcp.models.state_version_outputs import StateVersionOutputRequest

# Create a request to get a specific state version output
request = StateVersionOutputRequest(
    state_version_output_id="wsout-1234567890abcdef"
)
```

## Related Resources

- [State Version Outputs Tools Documentation](../tools/state_version_outputs.md)
- [State Version Models Documentation](./state_versions.md)
- [Terraform Cloud API Documentation - State Version Outputs](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-version-outputs)