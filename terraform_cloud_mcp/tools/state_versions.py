"""Terraform Cloud state version management tools.

This module provides tools for working with state versions in Terraform Cloud.
It includes functions to retrieve, list, and create state versions.

Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions
"""

from typing import Optional

from ..api.client import api_request
from ..models.base import APIResponse
from ..models.state_versions import (
    CurrentStateVersionRequest,
    StateVersionCreateRequest,
    StateVersionListRequest,
    StateVersionParams,
    StateVersionRequest,
    StateVersionStatus,
)
from ..utils.decorators import handle_api_errors
from ..utils.payload import create_api_payload, add_relationship
from ..utils.request import query_params


@handle_api_errors
async def list_state_versions(
    organization: str,
    workspace_name: str,
    page_number: int = 1,
    page_size: int = 20,
    filter_status: Optional[str] = None,
) -> APIResponse:
    """List state versions in a workspace.

    Retrieves a paginated list of all state versions in a Terraform Cloud workspace.
    Results can be filtered using status to find specific state versions.

    API endpoint: GET /state-versions

    Args:
        organization: The name of the organization that owns the workspace
        workspace_name: The name of the workspace to list state versions from
        page_number: The page number to return (default: 1)
        page_size: The number of items per page (default: 20, max: 100)
        filter_status: Filter state versions by status: 'pending', 'finalized', or 'discarded'

    Returns:
        Paginated list of state versions with their configuration settings and metadata

    See:
        docs/tools/state_versions.md for reference documentation
    """
    # Convert filter_status string to enum if provided
    status_enum = None
    if filter_status:
        try:
            status_enum = StateVersionStatus(filter_status)
        except ValueError:
            valid_values = ", ".join([s.value for s in StateVersionStatus])
            raise ValueError(
                f"Invalid filter_status value: {filter_status}. Valid values: {valid_values}"
            )

    # Validate parameters
    params = StateVersionListRequest(
        filter_workspace_name=workspace_name,
        filter_organization_name=organization,
        page_number=page_number,
        page_size=page_size,
        filter_status=status_enum,
    )

    # Build query parameters using utility function
    query = query_params(params)

    # Make API request
    return await api_request("state-versions", params=query)


@handle_api_errors
async def get_current_state_version(workspace_id: str) -> APIResponse:
    """Get the current state version for a workspace.

    Retrieves the current state version for a workspace, which is the input
    state when running terraform operations.

    API endpoint: GET /workspaces/:workspace_id/current-state-version

    Args:
        workspace_id: The ID of the workspace (format: "ws-xxxxxxxx")

    Returns:
        The current state version including details and download URLs

    See:
        docs/tools/state_versions.md for reference documentation
    """
    # Validate parameters
    params = CurrentStateVersionRequest(workspace_id=workspace_id)

    # Make API request
    return await api_request(f"workspaces/{params.workspace_id}/current-state-version")


@handle_api_errors
async def get_state_version(state_version_id: str) -> APIResponse:
    """Get details for a specific state version.

    Retrieves comprehensive information about a state version including its status,
    download URLs, and resource information.

    API endpoint: GET /state-versions/:state_version_id

    Args:
        state_version_id: The ID of the state version to retrieve (format: "sv-xxxxxxxx")

    Returns:
        State version details including status, timestamps, and resource metadata

    See:
        docs/tools/state_versions.md for reference documentation
    """
    # Validate parameters
    params = StateVersionRequest(state_version_id=state_version_id)

    # Make API request
    return await api_request(f"state-versions/{params.state_version_id}")


@handle_api_errors
async def create_state_version(
    workspace_id: str,
    serial: int,
    md5: str,
    params: Optional[StateVersionParams] = None,
) -> APIResponse:
    """Create a state version in a workspace.

    Creates a new state version and sets it as the current state version for the
    given workspace. The workspace must be locked by the user creating a state version.
    This is most useful for migrating existing state from Terraform Community edition
    into a new HCP Terraform workspace.

    API endpoint: POST /workspaces/:workspace_id/state-versions

    Args:
        workspace_id: The ID of the workspace (format: "ws-xxxxxxxx")
        serial: The serial number of this state instance
        md5: An MD5 hash of the raw state version
        params: Additional state version parameters (optional):
            - state: Base64 encoded raw state file
            - lineage: Lineage of the state version
            - json_state: Base64 encoded JSON state
            - json_state_outputs: Base64 encoded JSON state outputs
            - run_id: The ID of the run to associate with the state version

    Returns:
        The created state version data including download URLs and status information

    See:
        docs/tools/state_versions.md for reference documentation
    """
    # Extract parameters from params object
    param_dict = params.model_dump(exclude_none=True, by_alias=False) if params else {}

    # Add required parameters
    param_dict["serial"] = serial
    param_dict["md5"] = md5

    # Create request using Pydantic model
    request_params = StateVersionCreateRequest(
        workspace_id=workspace_id,
        **param_dict
    )

    # Create API payload using utility function
    payload = create_api_payload(
        resource_type="state-versions",
        model=request_params,
        exclude_fields={"workspace_id"},
    )

    # Add relationship if run_id is provided
    if param_dict.get("run_id"):

        payload = add_relationship(
            payload=payload,
            relation_name="run",
            resource_type="runs",
            resource_id=param_dict["run_id"],
        )

    # Make API request
    return await api_request(
        f"workspaces/{request_params.workspace_id}/state-versions",
        method="POST",
        data=payload,
    )


@handle_api_errors
async def download_state_file(
    state_version_id: str, json_format: bool = False
) -> APIResponse:
    """Download the state file content.

    Retrieves the raw state file or JSON formatted state file for a specific state version.

    API endpoint: Uses the hosted URLs from GET /state-versions/:state_version_id

    Args:
        state_version_id: The ID of the state version (format: "sv-xxxxxxxx")
        json_format: Whether to download the JSON formatted state (default: False)

    Returns:
        The raw state file content or JSON formatted state content

    See:
        docs/tools/state_versions.md for reference documentation
    """
    # Validate parameters
    params = StateVersionRequest(state_version_id=state_version_id)

    # First get state version details to get the download URL
    state_version = await api_request(f"state-versions/{params.state_version_id}")

    # Determine which URL to use based on format request
    url_attr = (
        "hosted-json-state-download-url" if json_format else "hosted-state-download-url"
    )
    download_url = state_version.get("data", {}).get("attributes", {}).get(url_attr)

    # Check if URL is available
    if not download_url:
        if json_format:
            return {
                "error": "JSON state download URL not available. This may be because the state was not created with Terraform 1.3+"
            }
        else:
            return {"error": "State download URL not available for this state version"}

    # Use the enhanced api_request to fetch state from the external URL
    return await api_request(download_url, external_url=True, accept_text=True)
