"""Terraform Cloud plan management tools.

This module provides tools for working with plans in Terraform Cloud.
It includes functions to retrieve plan details and JSON output.

Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/plans
"""

from ..api.client import api_request
from ..models.base import APIResponse
from ..models.plans import (
    PlanJsonOutputRequest,
    PlanRequest,
    RunPlanJsonOutputRequest,
)
from ..utils.decorators import handle_api_errors


@handle_api_errors
async def get_plan_details(plan_id: str) -> APIResponse:
    """Get details for a specific plan.

    Retrieves comprehensive information about a plan including its current status,
    logs, resource counts, and relationship to other resources.

    API endpoint: GET /plans/{plan_id}

    Args:
        plan_id: The ID of the plan to retrieve details for (format: "plan-xxxxxxxx")

    Returns:
        Plan details including status, timestamps, and resource change counts

    See:
        docs/tools/plan_tools.md for usage examples
    """
    # Validate parameters
    params = PlanRequest(plan_id=plan_id)

    # Make API request
    return await api_request(f"plans/{params.plan_id}")


@handle_api_errors
async def get_plan_json_output(plan_id: str) -> APIResponse:
    """Retrieve the JSON execution plan.

    Gets the JSON representation of a plan's execution details, providing a
    machine-readable format of the planned resource changes.
    
    Note: This endpoint returns a pre-signed URL that requires direct access with 
    Terraform Cloud authentication. The URL is returned in the 'redirect_url' field
    of the response.

    API endpoint: GET /plans/{plan_id}/json-output

    Args:
        plan_id: The ID of the plan to retrieve JSON output for (format: "plan-xxxxxxxx")

    Returns:
        Dictionary with 'redirect_url' containing the temporary authenticated URL 
        to the JSON formatted plan. Use this URL directly with your TFC authentication.

    See:
        docs/tools/plan_tools.md for usage examples
    """
    # Validate parameters
    params = PlanJsonOutputRequest(plan_id=plan_id)

    # Make API request
    response = await api_request(f"plans/{params.plan_id}/json-output")
    
    # Handle both direct response and redirect response formats
    if "redirect_url" in response:
        return response
    elif "error" in response and "307" in response.get("error", ""):
        # Fall back to explaining the issue if we're still getting a 307 error
        return {
            "error": "The plan JSON output requires following a redirect which needs direct authentication.",
            "workaround": "Use the Terraform Cloud UI to view the plan details for this run.",
            "run_url": f"https://app.terraform.io/app/organizations/workspaces/runs/{plan_id}"
        }
    else:
        return response


@handle_api_errors
async def get_run_plan_json_output(run_id: str) -> APIResponse:
    """Retrieve the JSON execution plan from a run.

    Gets the JSON representation of a run's current plan execution details,
    providing a machine-readable format of the planned resource changes.
    
    Note: This endpoint returns a pre-signed URL that requires direct access with 
    Terraform Cloud authentication. The URL is returned in the 'redirect_url' field
    of the response.

    API endpoint: GET /runs/{run_id}/plan/json-output

    Args:
        run_id: The ID of the run to retrieve plan JSON output for (format: "run-xxxxxxxx")

    Returns:
        Dictionary with 'redirect_url' containing the temporary authenticated URL 
        to the JSON formatted plan. Use this URL directly with your TFC authentication.

    See:
        docs/tools/plan_tools.md for usage examples
    """
    # Validate parameters
    params = RunPlanJsonOutputRequest(run_id=run_id)

    # Make API request
    response = await api_request(f"runs/{params.run_id}/plan/json-output")
    
    # Handle both direct response and redirect response formats
    if "redirect_url" in response:
        return response
    elif "error" in response and "307" in response.get("error", ""):
        # Fall back to explaining the issue if we're still getting a 307 error
        return {
            "error": "The plan JSON output requires following a redirect which needs direct authentication.",
            "workaround": "Use the Terraform Cloud UI to view the plan details for this run.",
            "run_url": f"https://app.terraform.io/app/organizations/workspaces/runs/{run_id}"
        }
    else:
        return response
