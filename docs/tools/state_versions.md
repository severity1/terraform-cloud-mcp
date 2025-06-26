# State Version Tools Documentation

This document describes tools for working with state versions in Terraform Cloud.

## Available Tools

### list_state_versions

List state versions in a workspace with filtering and pagination options.

```python
async def list_state_versions(
    organization: str,
    workspace_name: str,
    page_number: int = 1,
    page_size: int = 20,
    filter_status: Optional[str] = None,
) -> APIResponse
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| organization | str | Yes | The organization name |
| workspace_name | str | Yes | The workspace name |
| page_number | int | No | Page number to fetch (default: 1) |
| page_size | int | No | Number of results per page (default: 20, max: 100) |
| filter_status | str | No | Filter state versions by status: 'pending', 'finalized', or 'discarded' |

**Returns:**

A paginated list of state versions for the specified workspace.

**Example:**

```python
# List all finalized state versions for a workspace
state_versions = await list_state_versions(
    organization="hashicorp", 
    workspace_name="my-workspace",
    filter_status="finalized"
)
```

### get_current_state_version

Get the current state version for a workspace.

```python
async def get_current_state_version(workspace_id: str) -> APIResponse
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workspace_id | str | Yes | The ID of the workspace (format: "ws-xxxxxxxx") |

**Returns:**

The current state version details for the specified workspace.

**Example:**

```python
# Get the current state version for a workspace
current_state = await get_current_state_version(workspace_id="ws-1234567890abcdef")
```

### get_state_version

Get details for a specific state version.

```python
async def get_state_version(state_version_id: str) -> APIResponse
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| state_version_id | str | Yes | The ID of the state version (format: "sv-xxxxxxxx") |

**Returns:**

Comprehensive details about the specified state version including download URLs.

**Example:**

```python
# Get details for a specific state version
state_version = await get_state_version(state_version_id="sv-1234567890abcdef")
```

### create_state_version

Create a new state version in a workspace.

```python
async def create_state_version(
    workspace_id: str,
    serial: int,
    md5: str,
    params: Optional[StateVersionParams] = None,
) -> APIResponse
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workspace_id | str | Yes | The ID of the workspace (format: "ws-xxxxxxxx") |
| serial | int | Yes | The serial number of this state instance |
| md5 | str | Yes | An MD5 hash of the raw state version |
| params | StateVersionParams | No | Additional parameters for state version creation |

**State Version Params:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| state | str | No | Base64 encoded raw state file |
| lineage | str | No | Lineage of the state version |
| json_state | str | No | Base64 encoded JSON state |
| json_state_outputs | str | No | Base64 encoded JSON state outputs |
| run_id | str | No | The ID of the run to associate with the state version |

**Returns:**

The created state version details including URLs for state upload (if applicable).

**Example:**

```python
from terraform_cloud_mcp.models.state_versions import StateVersionParams

# Create optional parameters
params = StateVersionParams(
    state="H4sIAAAA...",  # Base64 encoded state
    lineage="871d1b4a-e579-fb7c-ffdb-f0c858a647a7"
)

# Create a new state version
new_state_version = await create_state_version(
    workspace_id="ws-1234567890abcdef",
    serial=1,
    md5="d41d8cd98f00b204e9800998ecf8427e",
    params=params
)
```

### download_state_file

Download the state file content.

```python
async def download_state_file(state_version_id: str, json_format: bool = False) -> APIResponse
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| state_version_id | str | Yes | The ID of the state version (format: "sv-xxxxxxxx") |
| json_format | bool | No | Whether to download the JSON formatted state (default: False) |

**Returns:**

The raw state file content or JSON formatted state content.

**Example:**

```python
# Download the raw state file
state_content = await download_state_file(state_version_id="sv-1234567890abcdef")

# Download the JSON formatted state (requires Terraform 1.3+)
json_state_content = await download_state_file(
    state_version_id="sv-1234567890abcdef",
    json_format=True
)
```

## Usage Notes

1. **Workspace Locking:** When creating a state version, the workspace must be locked by the user creating the state version. The workspace may be locked with the API or with the UI.

2. **Asynchronous Processing:** Some information returned in a state version API object might be populated asynchronously by HCP Terraform. This includes resources, modules, providers, and the outputs. The `resources-processed` property on the state version object indicates whether or not processing is complete.

3. **State Download URLs:** The state version object includes URLs from which the state can be downloaded:
   - `hosted-state-download-url`: For downloading raw state data
   - `hosted-json-state-download-url`: For downloading JSON formatted state (Terraform 1.3+)

4. **State Upload URLs:** When creating a state version without providing state data, you'll receive URLs to upload the state content separately:
   - `hosted-state-upload-url`: For uploading raw state data
   - `hosted-json-state-upload-url`: For uploading JSON formatted state

## Related Resources

- [State Version Models Documentation](../models/state_versions.md)
- [State Version Outputs Documentation](./state_version_outputs.md)
- [Terraform Cloud API Documentation - State Versions](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions)