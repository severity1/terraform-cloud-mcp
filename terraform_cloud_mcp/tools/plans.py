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
        docs/tools/plan.md for reference documentation
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

    API endpoint: GET /plans/{plan_id}/json-output

    Args:
        plan_id: The ID of the plan to retrieve JSON output for (format: "plan-xxxxxxxx")

    Returns:
        The complete JSON formatted plan with resource changes, metadata,
        and planned actions. The redirect is automatically followed.

    See:
        docs/tools/plan.md for reference documentation
    """
    # Validate parameters
    params = PlanJsonOutputRequest(plan_id=plan_id)

    # Make API request
    return await api_request(f"plans/{params.plan_id}/json-output")


@handle_api_errors
async def get_run_plan_json_output(run_id: str) -> APIResponse:
    """Retrieve the JSON execution plan from a run.

    Gets the JSON representation of a run's current plan execution details,
    providing a machine-readable format of the planned resource changes.

    API endpoint: GET /runs/{run_id}/plan/json-output

    Args:
        run_id: The ID of the run to retrieve plan JSON output for (format: "run-xxxxxxxx")

    Returns:
        The complete JSON formatted plan with resource changes, metadata,
        and planned actions. The redirect is automatically followed.

    See:
        docs/tools/plan.md for reference documentation
    """
    # Validate parameters
    params = RunPlanJsonOutputRequest(run_id=run_id)

    # Make API request
    return await api_request(f"runs/{params.run_id}/plan/json-output")


@handle_api_errors
async def get_plan_logs(plan_id: str) -> APIResponse:
    """Retrieve logs from a plan.

    Gets the raw log output from a Terraform Cloud plan operation,
    providing detailed information about the execution plan.

    API endpoint: Uses the log-read-url from GET /plans/{plan_id}

    Args:
        plan_id: The ID of the plan to retrieve logs for (format: "plan-xxxxxxxx")

    Returns:
        The raw logs from the plan operation. The redirect to the log file
        is automatically followed.

    See:
        docs/tools/plan.md for reference documentation
    """
    # Validate parameters using existing model
    params = PlanRequest(plan_id=plan_id)

    # First get plan details to get the log URL
    plan_details = await api_request(f"plans/{params.plan_id}")

    # Extract log read URL
    log_read_url = (
        plan_details.get("data", {}).get("attributes", {}).get("log-read-url")
    )
    if not log_read_url:
        return {"error": "No log URL available for this plan"}

    # Use the enhanced api_request to fetch logs from the external URL
    return await api_request(log_read_url, external_url=True, accept_text=True)
