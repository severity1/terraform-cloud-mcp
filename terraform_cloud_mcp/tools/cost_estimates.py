"""Terraform Cloud cost estimates management tools.

This module provides tools for working with cost estimates in Terraform Cloud.
It includes functions to retrieve cost estimate details.

Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/cost-estimates
"""

from ..api.client import api_request
from ..models.base import APIResponse
from ..models.cost_estimates import CostEstimateRequest
from ..utils.decorators import handle_api_errors


@handle_api_errors
async def get_cost_estimate_details(cost_estimate_id: str) -> APIResponse:
    """Get details for a specific cost estimate.

    Retrieves comprehensive information about a cost estimate including its current status,
    resource counts, monthly cost estimations, and relationship to other resources.

    API endpoint: GET /cost-estimates/{cost_estimate_id}

    Args:
        cost_estimate_id: The ID of the cost estimate to retrieve details for (format: "ce-xxxxxxxx")

    Returns:
        Cost estimate details including status, timestamps, resource counts,
        and monthly cost estimations

    Note:
        There is no endpoint to list cost estimates. You can find the ID for a cost estimate
        in the `relationships.cost-estimate` property of a run object.

    See:
        docs/tools/cost_estimate.md for reference documentation
    """
    # Validate parameters
    params = CostEstimateRequest(cost_estimate_id=cost_estimate_id)

    # Make API request
    return await api_request(f"cost-estimates/{params.cost_estimate_id}")
