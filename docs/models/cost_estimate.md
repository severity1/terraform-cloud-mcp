# Cost Estimate Models

This document describes the data models used for cost estimation in Terraform Cloud.

## Overview

Cost estimate models provide structure and validation for interacting with the Terraform Cloud Cost Estimation API. These models define the format of cost estimate data, status values, and request validation.

## Models Reference

### CostEstimateStatus

**Type:** Enum (string)

**Description:** Represents the possible states a cost estimate can be in during its lifecycle.

**Values:**
- `pending`: Cost estimate has not yet started
- `queued`: Cost estimate is queued for execution
- `running`: Cost estimate is currently running
- `errored`: Cost estimate has encountered an error
- `canceled`: Cost estimate was canceled
- `finished`: Cost estimate has completed successfully
- `unreachable`: Cost estimate is in an unreachable state

**Usage Context:**
Used to determine the current state of a cost estimate operation and whether it has completed successfully.

### StatusTimestamps

**Type:** Object

**Description:** Captures timing information for various stages in a cost estimate's lifecycle.

**Fields:**
- `queued_at` (string, optional): ISO8601 timestamp when the cost estimate was queued
- `finished_at` (string, optional): ISO8601 timestamp when the cost estimate execution completed

**JSON representation:**
```json
{
  "queued-at": "2023-05-01T12:34:56Z",
  "finished-at": "2023-05-01T12:35:30Z"
}
```

**Notes:**
- Field names in JSON responses use kebab-case format (e.g., "queued-at")
- Field names in the model use snake_case format (e.g., queued_at)
- All timestamp fields follow ISO8601 format

### CostEstimateRequest

**Type:** Request Validation Model

**Description:** Used to validate cost estimate ID parameters in API requests.

**Fields:**
- `cost_estimate_id` (string, required): The ID of the cost estimate to retrieve
  - Format: Must match pattern "ce-[a-zA-Z0-9]{16}"
  - Example: "ce-BPvFFrYCqRV6qVBK"

**Validation Rules:**
- Cost estimate ID must start with "ce-" prefix
- Must contain exactly 16 alphanumeric characters after the prefix

**Used by:**
- `get_cost_estimate_details` tool function to validate the cost estimate ID format before making API requests

## API Response Structure

While models validate requests, responses are returned as raw JSON. A typical cost estimate response has this structure:

```json
{
  "data": [
    {
      "id": "ce-BPvFFrYCqRV6qVBK",
      "type": "cost-estimates",
      "attributes": {
        "error-message": null,
        "status": "finished",
        "status-timestamps": {
          "queued-at": "2023-05-01T12:34:56Z",
          "finished-at": "2023-05-01T12:35:30Z"
        },
        "resources-count": 4,
        "matched-resources-count": 3,
        "unmatched-resources-count": 1,
        "prior-monthly-cost": "0.0",
        "proposed-monthly-cost": "25.488",
        "delta-monthly-cost": "25.488"
      },
      "links": {
        "self": "/api/v2/cost-estimate/ce-BPvFFrYCqRV6qVBK"
      }
    }
  ]
}
```

## Related Resources

- [Cost Estimate Tools](../tools/cost_estimate.md)
- [Terraform Cloud API - Cost Estimates](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/cost-estimates)