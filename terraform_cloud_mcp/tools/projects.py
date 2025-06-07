"""Project management tools for Terraform Cloud MCP

This module implements the project-related endpoints of the Terraform Cloud API.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects
"""

import logging
from typing import Dict, List, Optional

from ..api.client import api_request
from ..utils.decorators import handle_api_errors
from ..utils.payload import create_api_payload
from ..utils.request import query_params
from ..models.base import APIResponse
from ..models.projects import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
    ProjectListRequest,
    ProjectParams,
    ProjectTagBindingRequest,
    TagBinding,
    WorkspaceMoveRequest,
)


@handle_api_errors
async def create_project(
    organization: str, name: str, params: Optional[ProjectParams] = None
) -> APIResponse:
    """Create a new project in an organization.

    Creates a new Terraform Cloud project which serves as a container for workspaces.
    Projects help organize workspaces into logical groups and can have their own
    settings and permissions.

    API endpoint: POST /organizations/{organization}/projects

    Args:
        organization: The name of the organization
        name: The name to give the project
        params: Additional project parameters (optional):
            - description: Human-readable description of the project
            - auto_destroy_activity_duration: How long each workspace should wait before auto-destroying
              (e.g., '14d', '24h')
            - tag_bindings: List of tag key-value pairs to bind to the project

    Returns:
        The created project data including configuration, settings and metadata

    See:
        docs/tools/project.md for reference documentation
    """
    param_dict = params.model_dump(exclude_none=True) if params else {}
    request = ProjectCreateRequest(organization=organization, name=name, **param_dict)

    # Create the base payload
    payload = create_api_payload(
        resource_type="projects", model=request, exclude_fields={"organization"}
    )

    # Handle tag bindings if present
    if request.tag_bindings:
        tag_bindings_data = []
        for tag in request.tag_bindings:
            tag_bindings_data.append(
                {
                    "type": "tag-bindings",
                    "attributes": {"key": tag.key, "value": tag.value},
                }
            )

        if "relationships" not in payload["data"]:
            payload["data"]["relationships"] = {}

        payload["data"]["relationships"]["tag-bindings"] = {"data": tag_bindings_data}

    # Remove tag-bindings from attributes if present since we've moved them to relationships
    if "tag-bindings" in payload["data"]["attributes"]:
        del payload["data"]["attributes"]["tag-bindings"]

    logger = logging.getLogger(__name__)
    logger.debug(f"Create project payload: {payload}")

    return await api_request(
        f"organizations/{organization}/projects", method="POST", data=payload
    )


@handle_api_errors
async def update_project(
    project_id: str, params: Optional[ProjectParams] = None
) -> APIResponse:
    """Update an existing project.

    Modifies the settings of a Terraform Cloud project. This can be used to change
    attributes like name, description, auto-destroy duration, or tags. Only specified
    attributes will be updated; unspecified attributes remain unchanged.

    API endpoint: PATCH /projects/{project_id}

    Args:
        project_id: The ID of the project to update (format: "prj-xxxxxxxx")
        params: Project parameters to update (optional):
            - name: New name for the project
            - description: Human-readable description of the project
            - auto_destroy_activity_duration: How long each workspace should wait before
              auto-destroying (e.g., '14d', '24h')
            - tag_bindings: List of tag key-value pairs to bind to the project

    Returns:
        The updated project with all current settings and configuration

    See:
        docs/tools/project.md for reference documentation
    """
    # Extract parameters from the params object if provided
    param_dict = params.model_dump(exclude_none=True) if params else {}

    # Create request using Pydantic model
    request = ProjectUpdateRequest(project_id=project_id, **param_dict)

    # Create base API payload using utility function
    payload = create_api_payload(
        resource_type="projects",
        model=request,
        exclude_fields={"project_id"},
    )

    # Handle tag bindings if present
    if request.tag_bindings:
        tag_bindings_data = []
        for tag in request.tag_bindings:
            tag_bindings_data.append(
                {
                    "type": "tag-bindings",
                    "attributes": {"key": tag.key, "value": tag.value},
                }
            )

        if "relationships" not in payload["data"]:
            payload["data"]["relationships"] = {}

        payload["data"]["relationships"]["tag-bindings"] = {"data": tag_bindings_data}

    # Remove tag-bindings from attributes if present since we've moved them to relationships
    if "tag-bindings" in payload["data"]["attributes"]:
        del payload["data"]["attributes"]["tag-bindings"]

    # Log payload for debugging
    logger = logging.getLogger(__name__)
    logger.debug(f"Update project payload: {payload}")

    # Make API request
    return await api_request(f"projects/{project_id}", method="PATCH", data=payload)


@handle_api_errors
async def list_projects(
    organization: str,
    page_number: int = 1,
    page_size: int = 20,
    q: Optional[str] = None,
    filter_names: Optional[str] = None,
    filter_permissions_update: Optional[bool] = None,
    filter_permissions_create_workspace: Optional[bool] = None,
    sort: Optional[str] = None,
) -> APIResponse:
    """List projects in an organization.

    Retrieves a paginated list of all projects in a Terraform Cloud organization.
    Results can be filtered using a search string or permissions filters to find
    specific projects.

    API endpoint: GET /organizations/{organization}/projects

    Args:
        organization: The name of the organization to list projects from
        page_number: The page number to return (default: 1)
        page_size: The number of items per page (default: 20, max: 100)
        q: Optional search query to filter projects by name
        filter_names: Filter projects by name (comma-separated list)
        filter_permissions_update: Filter projects that the user can update
        filter_permissions_create_workspace: Filter projects that the user can create workspaces in
        sort: Sort projects by name ('name' or '-name' for descending)

    Returns:
        Paginated list of projects with their configuration settings and metadata

    See:
        docs/tools/project.md for reference documentation
    """
    # Create request using Pydantic model for validation
    request = ProjectListRequest(
        organization=organization,
        page_number=page_number,
        page_size=page_size,
        q=q,
        filter_names=filter_names,
        filter_permissions_update=filter_permissions_update,
        filter_permissions_create_workspace=filter_permissions_create_workspace,
        sort=sort,
    )

    # Use the unified query params utility function
    params = query_params(request)

    # Make API request
    return await api_request(
        f"organizations/{organization}/projects", method="GET", params=params
    )


@handle_api_errors
async def get_project_details(project_id: str) -> APIResponse:
    """Get details for a specific project.

    Retrieves comprehensive information about a project including its configuration,
    tag bindings, workspace count, and other attributes.

    API endpoint: GET /projects/{project_id}

    Args:
        project_id: The ID of the project (format: "prj-xxxxxxxx")

    Returns:
        Project details including settings, configuration and status

    See:
        docs/tools/project.md for reference documentation
    """
    # Make API request
    return await api_request(f"projects/{project_id}", method="GET")


@handle_api_errors
async def delete_project(project_id: str) -> APIResponse:
    """Delete a project.

    Permanently deletes a Terraform Cloud project. This operation will
    fail if the project contains any workspaces or stacks.

    API endpoint: DELETE /projects/{project_id}

    Args:
        project_id: The ID of the project to delete (format: "prj-xxxxxxxx")

    Returns:
        Empty response with HTTP 204 status code if successful

    See:
        docs/tools/project.md for reference documentation
    """
    # Make API request
    return await api_request(f"projects/{project_id}", method="DELETE")


@handle_api_errors
async def list_project_tag_bindings(project_id: str) -> APIResponse:
    """List tag bindings for a project.

    Retrieves the list of tags bound to a specific project. These tags are
    inherited by all workspaces within the project.

    API endpoint: GET /projects/{project_id}/tag-bindings

    Args:
        project_id: The ID of the project (format: "prj-xxxxxxxx")

    Returns:
        List of tag bindings with their key-value pairs and creation timestamps

    See:
        docs/tools/project.md for reference documentation
    """
    # Make API request
    return await api_request(f"projects/{project_id}/tag-bindings", method="GET")


@handle_api_errors
async def add_update_project_tag_bindings(
    project_id: str, tag_bindings: List[TagBinding]
) -> APIResponse:
    """Add or update tag bindings on a project.

    Adds new tag bindings or updates existing ones on a project. This is an
    additive operation that doesn't remove existing tags.

    API endpoint: PATCH /projects/{project_id}/tag-bindings

    Args:
        project_id: The ID of the project (format: "prj-xxxxxxxx")
        tag_bindings: List of TagBinding objects with key-value pairs to add or update

    Returns:
        The complete list of updated tag bindings for the project

    See:
        docs/tools/project.md for reference documentation
    """
    # Create request using Pydantic model
    request = ProjectTagBindingRequest(project_id=project_id, tag_bindings=tag_bindings)

    # Create payload
    tag_bindings_data = []
    for tag in request.tag_bindings:
        tag_bindings_data.append(
            {"type": "tag-bindings", "attributes": {"key": tag.key, "value": tag.value}}
        )

    payload = {"data": tag_bindings_data}

    # Make API request
    return await api_request(
        f"projects/{project_id}/tag-bindings", method="PATCH", data=payload
    )


@handle_api_errors
async def move_workspaces_to_project(
    project_id: str, workspace_ids: List[str]
) -> APIResponse:
    """Move workspaces into a project.

    Moves one or more workspaces into a project. The user must have permission
    to move workspaces on both source and destination projects.

    API endpoint: POST /projects/{project_id}/relationships/workspaces

    Args:
        project_id: The ID of the destination project (format: "prj-xxxxxxxx")
        workspace_ids: List of workspace IDs to move (format: ["ws-xxxxxxxx", ...])

    Returns:
        Empty response with HTTP 204 status code if successful

    See:
        docs/tools/project.md for reference documentation
    """
    # Create request using Pydantic model
    request = WorkspaceMoveRequest(project_id=project_id, workspace_ids=workspace_ids)

    # Create payload
    payload: Dict[str, List[Dict[str, str]]] = {"data": []}
    for workspace_id in request.workspace_ids:
        payload["data"].append({"type": "workspaces", "id": workspace_id})

    # Make API request
    return await api_request(
        f"projects/{project_id}/relationships/workspaces", method="POST", data=payload
    )
