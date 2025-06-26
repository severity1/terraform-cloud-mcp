# State Version Outputs Models

This document describes the data models used for state version outputs operations in Terraform Cloud.

## Overview

State version outputs models provide structure and validation for interacting with the Terraform Cloud State Version Outputs API. These models handle the output values from Terraform state files, including name, value, type, and sensitivity information.

## Models Reference

### StateVersionOutputListRequest

**Type:** Request Validation Model

**Description:** Used to validate parameters for listing outputs for a specific state version.

**Fields:**
- `state_version_id` (string, required): The ID of the state version to list outputs for
  - Format: Must match pattern "sv-[a-zA-Z0-9]{16}"
  - Example: "sv-BPvFFrYCqRV6qVBK"
- `page_number` (integer, optional): Page number to fetch (default: 1, minimum: 1)
- `page_size` (integer, optional): Number of results per page (default: 20, max: 100)

**Validation Rules:**
- State version ID must start with "sv-" prefix
- Must contain exactly 16 alphanumeric characters after the prefix
- Page number must be positive integer
- Page size must be between 1 and 100

### StateVersionOutputRequest

**Type:** Request Validation Model

**Description:** Used to validate state version output ID parameters in API requests.

**Fields:**
- `state_version_output_id` (string, required): The ID of the state version output to retrieve
  - Format: Must match pattern "wsout-[a-zA-Z0-9]{16}"
  - Example: "wsout-BPvFFrYCqRV6qVBK"

**Validation Rules:**
- State version output ID must start with "wsout-" prefix
- Must contain exactly 16 alphanumeric characters after the prefix

**Used by:**
- `get_state_version_output` tool function to validate the output ID format before making API requests

## API Response Structure

While models validate requests, responses are returned as raw JSON. A typical state version output response has this structure:

```json
{
  "data": {
    "id": "wsout-BPvFFrYCqRV6qVBK",
    "type": "state-version-outputs",
    "attributes": {
      "name": "vpc_id",
      "sensitive": false,
      "type": "string",
      "value": "vpc-1234567890abcdef",
      "detailed-type": "string"
    },
    "relationships": {
      "configurable": {
        "data": {
          "id": "sv-BPvFFrYCqRV6qVBK",
          "type": "state-versions"
        }
      }
    }
  }
}
```

**Key Attributes:**
- `name`: The name of the output as defined in Terraform configuration
- `sensitive`: Boolean indicating if the output contains sensitive information
- `type`: Simplified data type (string, number, bool, etc.)
- `value`: The actual output value (hidden for sensitive outputs)
- `detailed-type`: More specific type information for complex structures

## Related Resources

- [State Version Outputs Tools](../tools/state_version_outputs.md)
- [State Version Models](./state_versions.md)
- [Terraform Cloud API - State Version Outputs](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-version-outputs)