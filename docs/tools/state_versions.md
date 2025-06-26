# State Version Tools

The state version tools module provides functions for working with state versions in Terraform Cloud.

## Overview

State versions represent point-in-time snapshots of Terraform state files. These tools allow you to manage the complete lifecycle of state versions, including listing, retrieving, creating, and downloading state data. This is particularly useful for state migration and workspace management.

## API Reference

These tools interact with the Terraform Cloud State Versions API:
- [State Versions API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions)
- [State Versions Concepts](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/state)

## Tools Reference

### list_state_versions

**Function:** `list_state_versions(organization: str, workspace_name: str, page_number: int = 1, page_size: int = 20, filter_status: Optional[str] = None) -> Dict[str, Any]`

**Description:** Retrieves a paginated list of state versions for a workspace with optional status filtering.

**Parameters:**
- `organization` (str): The organization name
- `workspace_name` (str): The workspace name
- `page_number` (int): Page number to fetch (default: 1)
- `page_size` (int): Number of results per page (default: 20, max: 100)
- `filter_status` (str): Filter by status: 'pending', 'finalized', or 'discarded'

**Returns:** JSON response containing paginated state versions with metadata including serial numbers, creation timestamps, and download URLs.

**Notes:**
- State versions are ordered by creation date (newest first)
- The `resources-processed` attribute indicates if asynchronous processing is complete
- Requires "read" permission for the workspace

### get_current_state_version

**Function:** `get_current_state_version(workspace_id: str) -> Dict[str, Any]`

**Description:** Retrieves the current active state version for a workspace.

**Parameters:**
- `workspace_id` (str): The ID of the workspace (format: "ws-xxxxxxxx")

**Returns:** JSON response containing the current state version details including download URLs and metadata.

**Notes:**
- Returns the state version that serves as input for new runs
- May return empty if no state versions exist for the workspace
- Requires "read" permission for the workspace

### get_state_version

**Function:** `get_state_version(state_version_id: str) -> Dict[str, Any]`

**Description:** Retrieves detailed information about a specific state version by ID.

**Parameters:**
- `state_version_id` (str): The ID of the state version (format: "sv-xxxxxxxx")

**Returns:** JSON response containing comprehensive state version details including resources, modules, providers, and download URLs.

**Notes:**
- Includes detailed resource and module information if processing is complete
- Contains both raw state and JSON state download URLs (when available)
- Requires "read" permission for the associated workspace

### create_state_version

**Function:** `create_state_version(workspace_id: str, serial: int, md5: str, params: Optional[StateVersionParams] = None) -> Dict[str, Any]`

**Description:** Creates a new state version in a workspace, useful for migrating state from Terraform Community Edition.

**Parameters:**
- `workspace_id` (str): The ID of the workspace (format: "ws-xxxxxxxx")
- `serial` (int): The serial number of this state instance
- `md5` (str): An MD5 hash of the raw state version
- `params` (StateVersionParams): Additional configuration including state data and lineage

**Returns:** JSON response containing the created state version with upload URLs if state data wasn't provided.

**Notes:**
- Workspace must be locked by the user creating the state version
- Can provide state data directly or use returned upload URLs
- Requires "write" permission for the workspace

### download_state_file

**Function:** `download_state_file(state_version_id: str, json_format: bool = False) -> Dict[str, Any]`

**Description:** Downloads the raw state file content or JSON formatted state for a specific state version.

**Parameters:**
- `state_version_id` (str): The ID of the state version (format: "sv-xxxxxxxx")
- `json_format` (bool): Whether to download JSON formatted state (default: False)

**Returns:** Raw state file content or JSON formatted state content.

**Notes:**
- JSON format requires Terraform 1.3+ to be available
- Raw format returns the actual Terraform state file
- Requires "read" permission for the associated workspace

**Common Error Scenarios:**

| Error | Cause | Solution |
|-------|-------|----------|
| 404 | State version not found | Verify the ID exists and you have proper permissions |
| 422 | Invalid state version ID format | Ensure the ID matches pattern "sv-xxxxxxxx" |
| 403 | Insufficient permissions | Verify your API token has proper workspace access |
| 409 | Workspace not locked (create only) | Lock the workspace before creating state versions |

## Related Resources

- [State Version Models](../models/state_versions.md)
- [State Version Outputs Tools](./state_version_outputs.md)
- [Terraform Cloud API - State Versions](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions)