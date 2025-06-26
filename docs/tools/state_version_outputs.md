# State Version Outputs Tools Documentation

This document describes tools for working with state version outputs in Terraform Cloud.

## Available Tools

### list_state_version_outputs

List outputs for a state version with pagination.

```python
async def list_state_version_outputs(
    state_version_id: str,
    page_number: int = 1,
    page_size: int = 20
) -> APIResponse
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| state_version_id | str | Yes | The ID of the state version (format: "sv-xxxxxxxx") |
| page_number | int | No | Page number to fetch (default: 1) |
| page_size | int | No | Number of results per page (default: 20, max: 100) |

**Returns:**

A paginated list of outputs for the specified state version.

**Example:**

```python
# List all outputs for a state version
outputs = await list_state_version_outputs(state_version_id="sv-1234567890abcdef")
```

### get_state_version_output

Get details for a specific state version output.

```python
async def get_state_version_output(state_version_output_id: str) -> APIResponse
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| state_version_output_id | str | Yes | The ID of the state version output (format: "wsout-xxxxxxxx") |

**Returns:**

Details about the specified state version output including name, value, and type information.

**Example:**

```python
# Get details for a specific output
output = await get_state_version_output(state_version_output_id="wsout-1234567890abcdef")
```

## Response Structure

### State Version Output Object

The state version output object includes the following attributes:

| Attribute | Description |
|-----------|-------------|
| name | Name of the output as defined in Terraform |
| sensitive | Boolean flag indicating if the output contains sensitive information |
| type | Simplified data type of the output value |
| value | The actual output value |
| detailed_type | Detailed type information, especially for complex types |

**Example Output:**

```json
{
  "data": {
    "id": "wsout-xFAmCR3VkBGepcee",
    "type": "state-version-outputs",
    "attributes": {
      "name": "vpc_id",
      "sensitive": false,
      "type": "string",
      "value": "vpc-1234567890abcdef",
      "detailed_type": "string"
    },
    "links": {
      "self": "/api/v2/state-version-outputs/wsout-xFAmCR3VkBGepcee"
    }
  }
}
```

## Usage Notes

1. **Asynchronous Processing:** State version outputs are populated asynchronously by HCP Terraform after a state version is uploaded. The `resources-processed` property on the [state version object](./state_versions.md) indicates whether or not processing is complete.

2. **Sensitive Values:** Outputs marked as sensitive will include the `sensitive: true` attribute but will not expose the actual value in API responses.

3. **Accessing Outputs:** You can access outputs in two ways:
   - List all outputs for a state version with `list_state_version_outputs`
   - Get a specific output by ID with `get_state_version_output`

4. **Output Types:** The `type` field provides a simplified data type, while `detailed_type` contains more specific type information, particularly for complex structures like objects or tuples.

## Related Resources

- [State Version Outputs Models Documentation](../models/state_version_outputs.md)
- [State Version Tools Documentation](./state_versions.md)
- [Terraform Cloud API Documentation - State Version Outputs](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-version-outputs)