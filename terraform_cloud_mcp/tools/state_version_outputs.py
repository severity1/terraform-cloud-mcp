"""Terraform Cloud state version outputs management tools.

This module provides tools for working with state version outputs in Terraform Cloud.
It includes functions to retrieve and list state version outputs.

Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-version-outputs
"""

from ..api.client import api_request
from ..models.base import APIResponse
from ..models.state_version_outputs import (
    StateVersionOutputListRequest,
    StateVersionOutputRequest,
)
from ..utils.decorators import handle_api_errors
from ..utils.request import query_params


@handle_api_errors
async def list_state_version_outputs(
    state_version_id: str, page_number: int = 1, page_size: int = 20
) -> APIResponse:
    """List outputs for a state version.

    Retrieves a paginated list of all outputs for a specific state version.
    These outputs include name, value, and sensitivity information.

    API endpoint: GET /state-versions/:state_version_id/outputs

    Args:
        state_version_id: The ID of the state version (format: "sv-xxxxxxxx")
        page_number: The page number to return (default: 1)
        page_size: The number of items per page (default: 20, max: 100)

    Returns:
        Paginated list of state version outputs with name, value, and sensitivity information

    See:
        docs/tools/state_version_outputs.md for reference documentation
    """
    # Validate parameters
    params = StateVersionOutputListRequest(
        state_version_id=state_version_id,
        page_number=page_number,
        page_size=page_size,
    )

    # Build query parameters using utility function
    query = query_params(params)

    # Make API request
    return await api_request(
        f"state-versions/{params.state_version_id}/outputs", params=query
    )


@handle_api_errors
async def get_state_version_output(state_version_output_id: str) -> APIResponse:
    """Get details for a specific state version output.

    Retrieves comprehensive information about a state version output including
    its name, value, type, and sensitivity information.

    API endpoint: GET /state-version-outputs/:state_version_output_id

    Args:
        state_version_output_id: The ID of the state version output (format: "wsout-xxxxxxxx")

    Returns:
        State version output details including name, value, type, and sensitivity information

    See:
        docs/tools/state_version_outputs.md for reference documentation
    """
    # Validate parameters
    params = StateVersionOutputRequest(state_version_output_id=state_version_output_id)

    # Make API request
    return await api_request(f"state-version-outputs/{params.state_version_output_id}")
