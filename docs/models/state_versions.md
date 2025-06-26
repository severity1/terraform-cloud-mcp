# State Version Models Documentation

This document describes the Pydantic models used for state version operations in the Terraform Cloud MCP.

## Overview

State versions represent point-in-time snapshots of Terraform state files. State version models are used to:

1. List state versions for a workspace
2. Get details about a specific state version
3. Get the current state version for a workspace
4. Create new state versions
5. Download state file contents

## Model Structure

### StateVersionStatus

Enum representing the possible statuses of a state version:

```python
class StateVersionStatus(str, Enum):
    PENDING = "pending"
    FINALIZED = "finalized"
    DISCARDED = "discarded"
    BACKING_DATA_SOFT_DELETED = "backing_data_soft_deleted"
    BACKING_DATA_PERMANENTLY_DELETED = "backing_data_permanently_deleted"
```

| Status | Description |
|--------|-------------|
| `pending` | State version has been created but the state data is not encoded within the request |
| `finalized` | State version has been successfully uploaded or created with valid state attribute |
| `discarded` | State version was discarded because it was superseded by a newer state version |
| `backing_data_soft_deleted` | *Enterprise only* - backing files are marked for garbage collection |
| `backing_data_permanently_deleted` | *Enterprise only* - backing files have been permanently deleted |

### StateVersionListRequest

Request model for listing state versions:

```python
class StateVersionListRequest(APIRequest):
    workspace_name: str
    organization: str
    filter_status: Optional[StateVersionStatus] = None
    page_number: Optional[int] = 1
    page_size: Optional[int] = 20
```

### StateVersionRequest

Request model for retrieving a specific state version:

```python
class StateVersionRequest(APIRequest):
    state_version_id: str  # Format: "sv-xxxxxxxxxxxxxxxx"
```

### CurrentStateVersionRequest

Request model for retrieving a workspace's current state version:

```python
class CurrentStateVersionRequest(APIRequest):
    workspace_id: str  # Format: "ws-xxxxxxxxxxxxxxxx"
```

### StateVersionCreateRequest

Request model for creating a state version:

```python
class StateVersionCreateRequest(APIRequest):
    workspace_id: str
    serial: int
    md5: str
    state: Optional[str] = None
    lineage: Optional[str] = None
    json_state: Optional[str] = None
    json_state_outputs: Optional[str] = None
    run_id: Optional[str] = None
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| workspace_id | str | Yes | The ID of the workspace to create the state version in |
| serial | int | Yes | The serial number of this state instance |
| md5 | str | Yes | An MD5 hash of the raw state version |
| state | str | No | Base64 encoded raw state file |
| lineage | str | No | Lineage of the state version |
| json_state | str | No | Base64 encoded JSON state |
| json_state_outputs | str | No | Base64 encoded JSON state outputs |
| run_id | str | No | The ID of the run to associate with the state version |

### StateVersionParams

Parameters model for state version operations:

```python
class StateVersionParams(APIRequest):
    serial: Optional[int] = None
    md5: Optional[str] = None
    state: Optional[str] = None
    lineage: Optional[str] = None
    json_state: Optional[str] = None
    json_state_outputs: Optional[str] = None
    run_id: Optional[str] = None
```

## Usage Examples

### Creating a request to list state versions

```python
from terraform_cloud_mcp.models.state_versions import StateVersionListRequest

# Create a request to list state versions for a workspace
request = StateVersionListRequest(
    organization="my-organization",
    workspace_name="my-workspace",
    page_number=1,
    page_size=20,
    filter_status=StateVersionStatus.FINALIZED
)
```

### Creating a request to get a specific state version

```python
from terraform_cloud_mcp.models.state_versions import StateVersionRequest

# Create a request to get a specific state version
request = StateVersionRequest(
    state_version_id="sv-1234567890abcdef"
)
```

### Creating a request to create a state version

```python
from terraform_cloud_mcp.models.state_versions import StateVersionCreateRequest, StateVersionParams

# Create parameters for state version creation
params = StateVersionParams(
    serial=1,
    md5="d41d8cd98f00b204e9800998ecf8427e",
    lineage="871d1b4a-e579-fb7c-ffdb-f0c858a647a7",
    state="H4sIAAAA...", # Base64 encoded state content
)

# Create a request to create a state version
request = StateVersionCreateRequest(
    workspace_id="ws-1234567890abcdef",
    serial=1,
    md5="d41d8cd98f00b204e9800998ecf8427e"
)
```

## Related Resources

- [State Version Tools Documentation](../tools/state_versions.md)
- [State Version Outputs Models Documentation](./state_version_outputs.md)
- [Terraform Cloud API Documentation - State Versions](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions)