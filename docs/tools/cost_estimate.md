# Cost Estimate Tools

The cost estimate tools module provides functions for working with cost estimates in Terraform Cloud.

## Overview

Cost estimates provide insights into the financial impact of infrastructure changes, allowing you to understand the cost implications of your Terraform changes before applying them. These tools allow you to retrieve and analyze cost estimate details.

## API Reference

These tools interact with the Terraform Cloud Cost Estimation API:
- [Cost Estimation API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/cost-estimates)
- [Cost Estimation Concepts](https://developer.hashicorp.com/terraform/cloud-docs/cost-estimation)

## Tools Reference

### get_cost_estimate_details

**Function:** `get_cost_estimate_details(cost_estimate_id: str) -> Dict[str, Any]`

**Description:** Retrieves detailed information about a specific cost estimate by ID.

**Parameters:**
- `cost_estimate_id` (str): The ID of the cost estimate (format: "ce-xxxxxxxx")

**Returns:** JSON response containing comprehensive cost estimate details including:
- Status (pending, queued, running, errored, canceled, finished, unreachable)
- Cost projections (prior monthly cost, proposed monthly cost, delta monthly cost)
- Resource counts (total, matched, unmatched resources)
- Execution timestamps
- Related workspaces and runs

**Notes:**
- There is no endpoint to list cost estimates directly
- Cost estimate IDs are typically found in the `relationships.cost-estimate` property of run objects
- Requires "read" permission for the associated workspace
- You can extract the cost estimate ID from a run by accessing:
  ```
  relationships = run_result.get("data", {}).get("relationships", {})
  cost_estimate_data = relationships.get("cost-estimate", {}).get("data", {})
  cost_estimate_id = cost_estimate_data.get("id")
  ```

**Common Error Scenarios:**

| Error | Cause | Solution |
|-------|-------|----------|
| 404 | Cost estimate not found | Verify the ID exists and you have proper permissions |
| 422 | Invalid cost estimate ID format | Ensure the ID matches pattern "ce-xxxxxxxx" |
| 403 | Insufficient permissions | Verify your API token has proper access |