# State Version Models

This document describes the data models used for state version operations in Terraform Cloud.

## Overview

State version models provide structure and validation for interacting with the Terraform Cloud State Versions API. These models define the format of state version data, status values, and request validation for managing point-in-time snapshots of Terraform state files.

## Models Reference

### StateVersionStatus

**Type:** Enum (string)

**Description:** Represents the possible states a state version can be in during its lifecycle.

**Values:**
- `pending`: State version has been created but the state data is not encoded within the request
- `finalized`: State version has been successfully uploaded or created with valid state attribute
- `discarded`: State version was discarded because it was superseded by a newer state version
- `backing_data_soft_deleted`: *Enterprise only* - backing files are marked for garbage collection
- `backing_data_permanently_deleted`: *Enterprise only* - backing files have been permanently deleted

**Usage Context:**
Used to filter state versions by their current status and determine if processing is complete.

### StateVersionListRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for listing state versions in a workspace.

**Fields:**
- `workspace_name` (string, required): The name of the workspace to list state versions for
- `organization` (string, required): The name of the organization that owns the workspace
- `filter_status` (StateVersionStatus, optional): Filter state versions by status
- `page_number` (integer, optional): Page number to fetch (default: 1, minimum: 1)
- `page_size` (integer, optional): Number of results per page (default: 20, max: 100)

### StateVersionRequest

**Type:** Request Validation Model

**Description:** Used to validate state version ID parameters in API requests.

**Fields:**
- `state_version_id` (string, required): The ID of the state version to retrieve
  - Format: Must match pattern "sv-[a-zA-Z0-9]{16}"
  - Example: "sv-BPvFFrYCqRV6qVBK"

### CurrentStateVersionRequest

**Type:** Request Validation Model

**Description:** Used to validate workspace ID parameters for current state version requests.

**Fields:**
- `workspace_id` (string, required): The ID of the workspace
  - Format: Must match pattern "ws-[a-zA-Z0-9]{16}"
  - Example: "ws-BPvFFrYCqRV6qVBK"

### StateVersionCreateRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for creating new state versions.

**Fields:**
- `workspace_id` (string, required): The ID of the workspace to create the state version in
- `serial` (integer, required): The serial number of this state instance (minimum: 0)
- `md5` (string, required): An MD5 hash of the raw state version (32 character hex string)
- `state` (string, optional): Base64 encoded raw state file
- `lineage` (string, optional): Lineage of the state version
- `json_state` (string, optional): Base64 encoded JSON state from "terraform show -json"
- `json_state_outputs` (string, optional): Base64 encoded JSON state outputs
- `run_id` (string, optional): The ID of the run to associate with the state version

### StateVersionParams

**Type:** Parameter Object

**Description:** Flexible parameter model for state version operations without routing fields.

**Fields:**
All fields from StateVersionCreateRequest excluding workspace_id, with all fields optional.

**JSON representation:**
```json
{
  "serial": 1,
  "md5": "d41d8cd98f00b204e9800998ecf8427e",
  "lineage": "871d1b4a-e579-fb7c-ffdb-f0c858a647a7",
  "json-state": "H4sIAAAA...",
  "json-state-outputs": "H4sIAAAA..."
}
```

**Notes:**
- Field names in JSON responses use kebab-case format (e.g., "json-state")
- Field names in the model use snake_case format (e.g., json_state)
- All encoded fields expect Base64 format

## API Response Structure

While models validate requests, responses are returned as raw JSON. A typical state version response has this structure:

```json
{
  "data": {
    "id": "sv-BPvFFrYCqRV6qVBK",
    "type": "state-versions",
    "attributes": {
      "created-at": "2023-05-01T12:34:56Z",
      "size": 1024,
      "hosted-state-download-url": "https://...",
      "hosted-json-state-download-url": "https://...",
      "modules": {...},
      "providers": {...},
      "resources": [...],
      "serial": 1,
      "state-version": 4,
      "terraform-version": "1.5.0",
      "vcs-commit-sha": "abc123",
      "vcs-commit-url": "https://..."
    },
    "relationships": {
      "run": {...},
      "created-by": {...}
    }
  }
}
```

## Related Resources

- [State Version Tools](../tools/state_versions.md)
- [State Version Outputs Models](./state_version_outputs.md)
- [Terraform Cloud API - State Versions](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions)