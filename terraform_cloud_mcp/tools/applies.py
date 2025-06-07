"""Terraform Cloud apply management tools.

This module provides tools for working with applies in Terraform Cloud.
It includes functions to retrieve apply details, logs, and errored state information.

Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies
"""

from ..api.client import api_request
from ..models.base import APIResponse
from ..models.applies import (
    ApplyRequest,
    ApplyErroredStateRequest,
)
from ..utils.decorators import handle_api_errors


@handle_api_errors
async def get_apply_details(apply_id: str) -> APIResponse:
    """Get details for a specific apply.

    Retrieves comprehensive information about an apply including its current status,
    logs, resource counts, and relationship to other resources.

    API endpoint: GET /applies/{apply_id}

    Args:
        apply_id: The ID of the apply to retrieve details for (format: "apply-xxxxxxxx")

    Returns:
        Apply details including status, timestamps, and resource change counts

    See:
        docs/tools/apply.md for reference documentation
    """
    # Validate parameters
    params = ApplyRequest(apply_id=apply_id)

    # Make API request
    return await api_request(f"applies/{params.apply_id}")


@handle_api_errors
async def get_errored_state(apply_id: str) -> APIResponse:
    """Retrieve the errored state from a failed apply.

    Gets information about a state file that failed to upload during an apply,
    providing access to the state data for recovery purposes.

    API endpoint: GET /applies/{apply_id}/errored-state

    Args:
        apply_id: The ID of the apply with a failed state upload (format: "apply-xxxxxxxx")

    Returns:
        Information about the errored state including access details.
        The redirect to the state file is automatically followed.

    See:
        docs/tools/apply.md for reference documentation
    """
    # Validate parameters
    params = ApplyErroredStateRequest(apply_id=apply_id)

    # Make API request - redirect handling happens automatically in the API client
    return await api_request(f"applies/{params.apply_id}/errored-state")


@handle_api_errors
async def get_apply_logs(apply_id: str) -> APIResponse:
    """Retrieve logs from an apply.

    Gets the raw log output from a Terraform Cloud apply operation,
    providing detailed information about resource changes and any errors.

    API endpoint: Uses the log-read-url from GET /applies/{apply_id}

    Args:
        apply_id: The ID of the apply to retrieve logs for (format: "apply-xxxxxxxx")

    Returns:
        The raw logs from the apply operation. The redirect to the log file
        is automatically followed.

    See:
        docs/tools/apply.md for reference documentation
    """
    # Validate parameters using existing model
    params = ApplyRequest(apply_id=apply_id)

    # First get apply details to get the log URL
    apply_details = await api_request(f"applies/{params.apply_id}")

    # Extract log read URL
    log_read_url = (
        apply_details.get("data", {}).get("attributes", {}).get("log-read-url")
    )
    if not log_read_url:
        return {"error": "No log URL available for this apply"}

    # Use the enhanced api_request to fetch logs from the external URL
    return await api_request(log_read_url, external_url=True, accept_text=True)
