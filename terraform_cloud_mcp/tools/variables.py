"""Variable management tools for Terraform Cloud MCP

This module implements workspace variables and variable sets endpoints
of the Terraform Cloud API.

Reference:
- https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables
- https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variable-sets
"""

from typing import List, Optional, Dict, Any

from ..api.client import api_request
from ..utils.decorators import handle_api_errors
from ..models.base import APIResponse
from ..models.variables import (
    WorkspaceVariableParams,
    VariableSetParams,
    VariableSetVariableParams,
)


# Workspace Variables Tools


@handle_api_errors
async def list_workspace_variables(workspace_id: str) -> APIResponse:
    """List all variables for a workspace.

    Retrieves all variables (both Terraform and environment) configured
    for a specific workspace.

    API endpoint: GET /workspaces/{workspace_id}/vars

    Args:
        workspace_id: The ID of the workspace (format: "ws-xxxxxxxx")

    Returns:
        List of workspace variables with their configuration and values

    See:
        docs/tools/variables.md#list-workspace-variables for reference documentation
    """
    endpoint = f"workspaces/{workspace_id}/vars"
    return await api_request(endpoint, method="GET")


@handle_api_errors
async def create_workspace_variable(
    workspace_id: str,
    key: str,
    category: str,
    params: Optional[WorkspaceVariableParams] = None,
) -> APIResponse:
    """Create a new variable in a workspace.

    Creates a new Terraform or environment variable within a workspace.
    Variables can be marked as sensitive to hide their values.

    API endpoint: POST /workspaces/{workspace_id}/vars

    Args:
        workspace_id: The ID of the workspace (format: "ws-xxxxxxxx")
        key: The variable name/key
        category: Variable category ("terraform" or "env")

        params: Additional variable parameters (optional):
            - value: Variable value
            - description: Description of the variable
            - hcl: Whether the value is HCL code (terraform variables only)
            - sensitive: Whether the variable value is sensitive

    Returns:
        The created variable with its configuration and metadata

    See:
        docs/tools/variables.md#create-workspace-variable for reference documentation
    """
    # Build the API payload
    attributes: Dict[str, Any] = {
        "key": key,
        "category": category,
    }

    # Add optional parameters if provided
    if params:
        if params.value is not None:
            attributes["value"] = params.value
        if params.description is not None:
            attributes["description"] = params.description
        if params.hcl is not None:
            attributes["hcl"] = params.hcl
        if params.sensitive is not None:
            attributes["sensitive"] = params.sensitive

    payload = {"data": {"type": "vars", "attributes": attributes}}
    endpoint = f"workspaces/{workspace_id}/vars"
    return await api_request(endpoint, method="POST", data=payload)


@handle_api_errors
async def update_workspace_variable(
    workspace_id: str,
    variable_id: str,
    params: Optional[WorkspaceVariableParams] = None,
) -> APIResponse:
    """Update an existing workspace variable.

    Modifies the configuration of an existing workspace variable. Only
    specified attributes will be updated; unspecified attributes remain unchanged.

    API endpoint: PATCH /workspaces/{workspace_id}/vars/{variable_id}

    Args:
        workspace_id: The ID of the workspace (format: "ws-xxxxxxxx")
        variable_id: The ID of the variable (format: "var-xxxxxxxx")

        params: Variable parameters to update (optional):
            - key: New variable name/key
            - value: New variable value
            - description: New description of the variable
            - category: New variable category ("terraform" or "env")
            - hcl: Whether the value is HCL code (terraform variables only)
            - sensitive: Whether the variable value is sensitive

    Returns:
        The updated variable with all current settings and configuration

    See:
        docs/tools/variables.md#update-workspace-variable for reference documentation
    """
    attributes: Dict[str, Any] = {}

    # Add parameters to update if provided
    if params:
        if params.key is not None:
            attributes["key"] = params.key
        if params.value is not None:
            attributes["value"] = params.value
        if params.description is not None:
            attributes["description"] = params.description
        if params.category is not None:
            attributes["category"] = str(params.category)
        if params.hcl is not None:
            attributes["hcl"] = params.hcl
        if params.sensitive is not None:
            attributes["sensitive"] = params.sensitive

    payload = {"data": {"type": "vars", "attributes": attributes}}
    endpoint = f"workspaces/{workspace_id}/vars/{variable_id}"
    return await api_request(endpoint, method="PATCH", data=payload)


@handle_api_errors
async def delete_workspace_variable(workspace_id: str, variable_id: str) -> APIResponse:
    """Delete a workspace variable.

    Permanently removes a variable from a workspace. This action cannot be undone.

    API endpoint: DELETE /workspaces/{workspace_id}/vars/{variable_id}

    Args:
        workspace_id: The ID of the workspace (format: "ws-xxxxxxxx")
        variable_id: The ID of the variable (format: "var-xxxxxxxx")

    Returns:
        Empty response with HTTP 204 status code if successful

    See:
        docs/tools/variables.md#delete-workspace-variable for reference documentation
    """
    endpoint = f"workspaces/{workspace_id}/vars/{variable_id}"
    return await api_request(endpoint, method="DELETE")


# Variable Sets Tools


@handle_api_errors
async def list_variable_sets(
    organization: str,
    page_number: int = 1,
    page_size: int = 20,
) -> APIResponse:
    """List variable sets in an organization.

    Retrieves a paginated list of all variable sets in a Terraform Cloud organization.
    Variable sets allow you to reuse variables across multiple workspaces.

    API endpoint: GET /organizations/{organization}/varsets

    Args:
        organization: The name of the organization
        page_number: The page number to return (default: 1)
        page_size: The number of items per page (default: 20, max: 100)

    Returns:
        Paginated list of variable sets with their configuration and metadata

    See:
        docs/tools/variables.md#list-variable-sets for reference documentation
    """
    endpoint = f"organizations/{organization}/varsets"
    params = {
        "page[number]": page_number,
        "page[size]": page_size,
    }
    return await api_request(endpoint, method="GET", params=params)


@handle_api_errors
async def get_variable_set(varset_id: str) -> APIResponse:
    """Get details for a specific variable set.

    Retrieves comprehensive information about a variable set including its
    variables, workspace assignments, and configuration.

    API endpoint: GET /varsets/{varset_id}

    Args:
        varset_id: The ID of the variable set (format: "varset-xxxxxxxx")

    Returns:
        Variable set details including configuration and relationships

    See:
        docs/tools/variables.md#get-variable-set for reference documentation
    """
    endpoint = f"varsets/{varset_id}"
    return await api_request(endpoint, method="GET")


@handle_api_errors
async def create_variable_set(
    organization: str,
    name: str,
    params: Optional[VariableSetParams] = None,
) -> APIResponse:
    """Create a new variable set in an organization.

    Creates a new variable set which can be used to manage variables across
    multiple workspaces and projects.

    API endpoint: POST /organizations/{organization}/varsets

    Args:
        organization: The name of the organization
        name: The name to give the variable set

        params: Additional variable set parameters (optional):
            - description: Description of the variable set
            - global: Whether this is a global variable set
            - priority: Whether this variable set takes priority over workspace variables

    Returns:
        The created variable set with its configuration and metadata

    See:
        docs/tools/variables.md#create-variable-set for reference documentation
    """
    # Build the API payload
    attributes: Dict[str, Any] = {
        "name": name,
    }

    # Add optional parameters if provided
    if params:
        if params.description is not None:
            attributes["description"] = params.description
        if params.global_ is not None:
            attributes["global"] = params.global_
        if params.priority is not None:
            attributes["priority"] = params.priority

    payload = {"data": {"type": "varsets", "attributes": attributes}}
    endpoint = f"organizations/{organization}/varsets"
    return await api_request(endpoint, method="POST", data=payload)


@handle_api_errors
async def update_variable_set(
    varset_id: str,
    params: Optional[VariableSetParams] = None,
) -> APIResponse:
    """Update an existing variable set.

    Modifies the settings of a variable set. Only specified attributes will be
    updated; unspecified attributes remain unchanged.

    API endpoint: PATCH /varsets/{varset_id}

    Args:
        varset_id: The ID of the variable set (format: "varset-xxxxxxxx")

        params: Variable set parameters to update (optional):
            - name: New name for the variable set
            - description: New description of the variable set
            - global: Whether this is a global variable set
            - priority: Whether this variable set takes priority over workspace variables

    Returns:
        The updated variable set with all current settings and configuration

    See:
        docs/tools/variables.md#update-variable-set for reference documentation
    """
    attributes: Dict[str, Any] = {}

    # Add parameters to update if provided
    if params:
        if params.name is not None:
            attributes["name"] = params.name
        if params.description is not None:
            attributes["description"] = params.description
        if params.global_ is not None:
            attributes["global"] = params.global_
        if params.priority is not None:
            attributes["priority"] = params.priority

    payload = {"data": {"type": "varsets", "attributes": attributes}}
    endpoint = f"varsets/{varset_id}"
    return await api_request(endpoint, method="PATCH", data=payload)


@handle_api_errors
async def delete_variable_set(varset_id: str) -> APIResponse:
    """Delete a variable set.

    Permanently removes a variable set and all its variables. This action cannot be undone.
    The variable set will be unassigned from all workspaces and projects.

    API endpoint: DELETE /varsets/{varset_id}

    Args:
        varset_id: The ID of the variable set (format: "varset-xxxxxxxx")

    Returns:
        Empty response with HTTP 204 status code if successful

    See:
        docs/tools/variables.md#delete-variable-set for reference documentation
    """
    endpoint = f"varsets/{varset_id}"
    return await api_request(endpoint, method="DELETE")


@handle_api_errors
async def assign_variable_set_to_workspaces(
    varset_id: str, workspace_ids: List[str]
) -> APIResponse:
    """Assign a variable set to one or more workspaces.

    Makes the variables in a variable set available to the specified workspaces.
    Variables from variable sets take precedence over workspace variables if
    the variable set has priority enabled.

    API endpoint: POST /varsets/{varset_id}/relationships/workspaces

    Args:
        varset_id: The ID of the variable set (format: "varset-xxxxxxxx")
        workspace_ids: List of workspace IDs (format: ["ws-xxxxxxxx", ...])

    Returns:
        Empty response with HTTP 204 status code if successful

    See:
        docs/tools/variables.md#assign-variable-set-to-workspaces for reference documentation
    """
    # Build relationships payload
    relationships_data = []
    for workspace_id in workspace_ids:
        relationships_data.append({"id": workspace_id, "type": "workspaces"})

    payload = {"data": relationships_data}
    endpoint = f"varsets/{varset_id}/relationships/workspaces"
    return await api_request(endpoint, method="POST", data=payload)


@handle_api_errors
async def unassign_variable_set_from_workspaces(
    varset_id: str, workspace_ids: List[str]
) -> APIResponse:
    """Remove a variable set from one or more workspaces.

    Removes the variable set assignment from the specified workspaces. The variables
    will no longer be available in those workspaces.

    API endpoint: DELETE /varsets/{varset_id}/relationships/workspaces

    Args:
        varset_id: The ID of the variable set (format: "varset-xxxxxxxx")
        workspace_ids: List of workspace IDs (format: ["ws-xxxxxxxx", ...])

    Returns:
        Empty response with HTTP 204 status code if successful

    See:
        docs/tools/variables.md#unassign-variable-set-from-workspaces for reference documentation
    """
    # Build relationships payload
    relationships_data = []
    for workspace_id in workspace_ids:
        relationships_data.append({"id": workspace_id, "type": "workspaces"})

    payload = {"data": relationships_data}
    endpoint = f"varsets/{varset_id}/relationships/workspaces"
    return await api_request(endpoint, method="DELETE", data=payload)


@handle_api_errors
async def assign_variable_set_to_projects(
    varset_id: str, project_ids: List[str]
) -> APIResponse:
    """Assign a variable set to one or more projects.

    Makes the variables in a variable set available to all workspaces within
    the specified projects.

    API endpoint: POST /varsets/{varset_id}/relationships/projects

    Args:
        varset_id: The ID of the variable set (format: "varset-xxxxxxxx")
        project_ids: List of project IDs (format: ["prj-xxxxxxxx", ...])

    Returns:
        Empty response with HTTP 204 status code if successful

    See:
        docs/tools/variables.md#assign-variable-set-to-projects for reference documentation
    """
    # Build relationships payload
    relationships_data = []
    for project_id in project_ids:
        relationships_data.append({"id": project_id, "type": "projects"})

    payload = {"data": relationships_data}
    endpoint = f"varsets/{varset_id}/relationships/projects"
    return await api_request(endpoint, method="POST", data=payload)


@handle_api_errors
async def unassign_variable_set_from_projects(
    varset_id: str, project_ids: List[str]
) -> APIResponse:
    """Remove a variable set from one or more projects.

    Removes the variable set assignment from the specified projects. The variables
    will no longer be available in workspaces within those projects.

    API endpoint: DELETE /varsets/{varset_id}/relationships/projects

    Args:
        varset_id: The ID of the variable set (format: "varset-xxxxxxxx")
        project_ids: List of project IDs (format: ["prj-xxxxxxxx", ...])

    Returns:
        Empty response with HTTP 204 status code if successful

    See:
        docs/tools/variables.md#unassign-variable-set-from-projects for reference documentation
    """
    # Build relationships payload
    relationships_data = []
    for project_id in project_ids:
        relationships_data.append({"id": project_id, "type": "projects"})

    payload = {"data": relationships_data}
    endpoint = f"varsets/{varset_id}/relationships/projects"
    return await api_request(endpoint, method="DELETE", data=payload)


# Variable Set Variables Tools


@handle_api_errors
async def list_variables_in_variable_set(varset_id: str) -> APIResponse:
    """List all variables in a variable set.

    Retrieves all variables that belong to a specific variable set,
    including their configuration and values.

    API endpoint: GET /varsets/{varset_id}/relationships/vars

    Args:
        varset_id: The ID of the variable set (format: "varset-xxxxxxxx")

    Returns:
        List of variables in the variable set with their configuration

    See:
        docs/tools/variables.md#list-variables-in-variable-set for reference documentation
    """
    endpoint = f"varsets/{varset_id}/relationships/vars"
    return await api_request(endpoint, method="GET")


@handle_api_errors
async def create_variable_in_variable_set(
    varset_id: str,
    key: str,
    category: str,
    params: Optional[VariableSetVariableParams] = None,
) -> APIResponse:
    """Create a new variable in a variable set.

    Creates a new Terraform or environment variable within a variable set.
    Variables can be marked as sensitive to hide their values.

    API endpoint: POST /varsets/{varset_id}/relationships/vars

    Args:
        varset_id: The ID of the variable set (format: "varset-xxxxxxxx")
        key: The variable name/key
        category: Variable category ("terraform" or "env")

        params: Additional variable parameters (optional):
            - value: Variable value
            - description: Description of the variable
            - hcl: Whether the value is HCL code (terraform variables only)
            - sensitive: Whether the variable value is sensitive

    Returns:
        The created variable with its configuration and metadata

    See:
        docs/tools/variables.md#create-variable-in-variable-set for reference documentation
    """
    # Build the API payload
    attributes: Dict[str, Any] = {
        "key": key,
        "category": category,
    }

    # Add optional parameters if provided
    if params:
        if params.value is not None:
            attributes["value"] = params.value
        if params.description is not None:
            attributes["description"] = params.description
        if params.hcl is not None:
            attributes["hcl"] = params.hcl
        if params.sensitive is not None:
            attributes["sensitive"] = params.sensitive

    payload = {"data": {"type": "vars", "attributes": attributes}}
    endpoint = f"varsets/{varset_id}/relationships/vars"
    return await api_request(endpoint, method="POST", data=payload)


@handle_api_errors
async def update_variable_in_variable_set(
    varset_id: str,
    var_id: str,
    params: Optional[VariableSetVariableParams] = None,
) -> APIResponse:
    """Update an existing variable in a variable set.

    Modifies the configuration of an existing variable within a variable set. Only
    specified attributes will be updated; unspecified attributes remain unchanged.

    API endpoint: PATCH /varsets/{varset_id}/relationships/vars/{var_id}

    Args:
        varset_id: The ID of the variable set (format: "varset-xxxxxxxx")
        var_id: The ID of the variable (format: "var-xxxxxxxx")

        params: Variable parameters to update (optional):
            - key: New variable name/key
            - value: New variable value
            - description: New description of the variable
            - category: New variable category ("terraform" or "env")
            - hcl: Whether the value is HCL code (terraform variables only)
            - sensitive: Whether the variable value is sensitive

    Returns:
        The updated variable with all current settings and configuration

    See:
        docs/tools/variables.md#update-variable-in-variable-set for reference documentation
    """
    attributes: Dict[str, Any] = {}

    # Add parameters to update if provided
    if params:
        if params.key is not None:
            attributes["key"] = params.key
        if params.value is not None:
            attributes["value"] = params.value
        if params.description is not None:
            attributes["description"] = params.description
        if params.category is not None:
            attributes["category"] = str(params.category)
        if params.hcl is not None:
            attributes["hcl"] = params.hcl
        if params.sensitive is not None:
            attributes["sensitive"] = params.sensitive

    payload = {"data": {"type": "vars", "attributes": attributes}}
    endpoint = f"varsets/{varset_id}/relationships/vars/{var_id}"
    return await api_request(endpoint, method="PATCH", data=payload)


@handle_api_errors
async def delete_variable_from_variable_set(varset_id: str, var_id: str) -> APIResponse:
    """Delete a variable from a variable set.

    Permanently removes a variable from a variable set. This action cannot be undone.

    API endpoint: DELETE /varsets/{varset_id}/relationships/vars/{var_id}

    Args:
        varset_id: The ID of the variable set (format: "varset-xxxxxxxx")
        var_id: The ID of the variable (format: "var-xxxxxxxx")

    Returns:
        Empty response with HTTP 204 status code if successful

    See:
        docs/tools/variables.md#delete-variable-from-variable-set for reference documentation
    """
    endpoint = f"varsets/{varset_id}/relationships/vars/{var_id}"
    return await api_request(endpoint, method="DELETE")
