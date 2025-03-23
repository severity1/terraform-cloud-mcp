"""Workspace management tools for Terraform Cloud MCP"""

from typing import Optional, List, Any, Dict

from api.client import make_api_request


async def list_workspaces(
    organization: str,
    page_number: int = 1,
    page_size: int = 20,
    all_pages: bool = False,
    search_name: str = "",
    search_tags: str = "",
    search_exclude_tags: str = "",
    search_wildcard_name: str = "",
    sort: str = "",
    filter_project_id: str = "",
    filter_current_run_status: str = "",
    filter_tagged_key: str = "",
    filter_tagged_value: str = "",
) -> dict:
    """
    List workspaces in an organization with comprehensive filtering and pagination

    Args:
        organization: The organization name (required)
        page_number: Page number to fetch (default: 1)
        page_size: Number of results per page (default: 20, max: 100)
        all_pages: If True, fetch all pages and combine results (default: False)
        search_name: Filter workspaces by name using fuzzy search
        search_tags: Filter workspaces with specific tags (comma separated)
        search_exclude_tags: Exclude workspaces with specific tags (comma separated)
        search_wildcard_name: Filter workspaces by name with wildcard matching (e.g., "prod-*", "*-test")
        sort: Sort workspaces by "name", "current-run.created-at", or "latest-change-at" (prefix with "-" for descending)
        filter_project_id: Filter workspaces belonging to a specific project
        filter_current_run_status: Filter workspaces by current run status
        filter_tagged_key: Filter workspaces by tag key
        filter_tagged_value: Filter workspaces by tag value (used with filter_tagged_key)

    Returns:
        List of workspaces with pagination information
    """

    # Validate pagination parameters
    if page_number < 1:
        return {"error": "Page number must be at least 1"}

    if page_size < 1 or page_size > 100:
        return {"error": "Page size must be between 1 and 100"}

    # Build query parameters
    params = {"page[number]": str(page_number), "page[size]": str(page_size)}

    # Add optional search and filter parameters
    if search_name:
        params["search[name]"] = search_name

    if search_tags:
        params["search[tags]"] = search_tags

    if search_exclude_tags:
        params["search[exclude-tags]"] = search_exclude_tags

    if search_wildcard_name:
        params["search[wildcard-name]"] = search_wildcard_name

    if sort:
        params["sort"] = sort

    if filter_project_id:
        params["filter[project][id]"] = filter_project_id

    if filter_current_run_status:
        params["filter[current-run][status]"] = filter_current_run_status

    if filter_tagged_key:
        params["filter[tagged][0][key]"] = filter_tagged_key
        if filter_tagged_value:
            params["filter[tagged][0][value]"] = filter_tagged_value

    # For all_pages mode, we'll start collecting all results
    if all_pages:
        all_workspaces: Dict[str, Any] = {"data": []}
        current_page = 1

        while True:
            params["page[number]"] = str(current_page)

            success, page_data = await make_api_request(
                f"organizations/{organization}/workspaces", params=params
            )

            if not success:
                return page_data  # Return error info

            # Add this page's workspaces to our collection
            all_workspaces["data"].extend(page_data.get("data", []))

            # Check if there's a next page
            meta = page_data.get("meta", {})
            pagination = meta.get("pagination", {})
            current_page = pagination.get("current-page", 1)
            total_pages = pagination.get("total-pages", 1)

            # Add pagination metadata
            if "meta" not in all_workspaces:
                all_workspaces["meta"] = meta

            # If we're on the last page, stop
            if current_page >= total_pages:
                break

            # Otherwise, continue to the next page
            current_page += 1

        # Update the pagination info in the response
        if "meta" in all_workspaces:
            meta = all_workspaces["meta"]
            if isinstance(meta, dict) and "pagination" in meta:
                pagination = meta["pagination"]
                if isinstance(pagination, dict):
                    pagination["current-page"] = 1
                    pagination["prev-page"] = None
                    pagination["next-page"] = None

        return all_workspaces

    # Standard single-page mode
    else:
        success, data = await make_api_request(
            f"organizations/{organization}/workspaces", params=params
        )

        if success:
            return data
        else:
            return data  # Error info is already in the data dictionary


async def get_workspace_details(organization: str, workspace_name: str) -> dict:
    """
    Get details for a specific workspace

    Args:
        organization: The organization name (required)
        workspace_name: The workspace name (required)

    Returns:
        Workspace details
    """

    if not workspace_name:
        return {"error": "Workspace name is required"}

    success, data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}"
    )

    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary


async def create_workspace(
    organization: str,
    name: str,
    description: str = "",
    terraform_version: str = "",
    working_directory: str = "",
    auto_apply: bool = False,
    file_triggers_enabled: bool = True,
    trigger_prefixes: List[str] = [],
    trigger_patterns: List[str] = [],
    queue_all_runs: bool = False,
    speculative_enabled: bool = True,
    global_remote_state: bool = False,
    execution_mode: str = "remote",
    allow_destroy_plan: bool = True,
    auto_apply_run_trigger: bool = False,
    project_id: str = "",
    vcs_repo: Dict[str, Any] = {},
    tags: List[Dict[str, str]] = [],
) -> dict:
    """
    Create a new workspace in an organization

    Args:
        organization: The organization name (required)
        name: The name of the workspace (required)
        description: A description for the workspace
        terraform_version: Specific Terraform version to use (default: latest)
        working_directory: Relative path that Terraform will execute within
        auto_apply: Automatically apply changes when a Terraform plan is successful
        file_triggers_enabled: Whether to filter runs based on changed files in VCS
        trigger_prefixes: List of path prefixes that will trigger runs
        trigger_patterns: List of glob patterns that Terraform monitors for changes
        queue_all_runs: Whether runs should be queued immediately after workspace creation
        speculative_enabled: Whether this workspace allows automatic speculative plans
        global_remote_state: Whether all workspaces in the organization can access this workspace's state
        execution_mode: Which execution mode to use: "remote", "local", or "agent"
        allow_destroy_plan: Whether destroy plans can be queued on the workspace
        auto_apply_run_trigger: Whether to automatically apply changes from run triggers
        project_id: The ID of the project to create the workspace in
        vcs_repo: Settings for the workspace's VCS repository (optional)
        tags: List of tags to attach to the workspace

    Returns:
        The created workspace details
    """

    if not name:
        return {"error": "Workspace name is required"}

    # Build the request payload
    payload: Dict[str, Any] = {
        "data": {"type": "workspaces", "attributes": {"name": name}}
    }

    # Add optional attributes if provided
    if description:
        payload["data"]["attributes"]["description"] = description
    if terraform_version:
        payload["data"]["attributes"]["terraform-version"] = terraform_version
    if working_directory:
        payload["data"]["attributes"]["working-directory"] = working_directory

    # Add boolean attributes (only those that differ from API defaults need to be explicitly set)
    # Auto-apply defaults to false in API, so only set if true
    if auto_apply:
        payload["data"]["attributes"]["auto-apply"] = auto_apply

    # File-triggers-enabled defaults to true in API
    if file_triggers_enabled is False:
        payload["data"]["attributes"]["file-triggers-enabled"] = False

    # Queue-all-runs defaults to false in API
    if queue_all_runs:
        payload["data"]["attributes"]["queue-all-runs"] = queue_all_runs

    # Speculative-enabled defaults to true in API
    if speculative_enabled is False:
        payload["data"]["attributes"]["speculative-enabled"] = False

    # Global-remote-state defaults to false in API
    if global_remote_state:
        payload["data"]["attributes"]["global-remote-state"] = global_remote_state

    # Allow-destroy-plan defaults to true in API
    if allow_destroy_plan is False:
        payload["data"]["attributes"]["allow-destroy-plan"] = False

    # Auto-apply-run-trigger defaults to false in API
    if auto_apply_run_trigger:
        payload["data"]["attributes"]["auto-apply-run-trigger"] = auto_apply_run_trigger

    # Add trigger lists if provided
    if trigger_prefixes:
        payload["data"]["attributes"]["trigger-prefixes"] = trigger_prefixes
    if trigger_patterns:
        payload["data"]["attributes"]["trigger-patterns"] = trigger_patterns

    # Add execution mode
    if execution_mode not in ["remote", "local", "agent"]:
        return {
            "error": "Invalid execution mode. Must be one of: 'remote', 'local', 'agent'"
        }
    payload["data"]["attributes"]["execution-mode"] = execution_mode

    # Add VCS repository settings if provided
    if vcs_repo:
        if not isinstance(vcs_repo, dict):
            return {"error": "vcs_repo must be a dictionary"}
        payload["data"]["attributes"]["vcs-repo"] = vcs_repo

    # Add project relationship if provided
    if project_id:
        if "relationships" not in payload["data"]:
            payload["data"]["relationships"] = {}
        payload["data"]["relationships"]["project"] = {
            "data": {"id": project_id, "type": "projects"}
        }

    # Add tags if provided
    if tags:
        if not isinstance(tags, list):
            return {"error": "tags must be a list"}

        if "relationships" not in payload["data"]:
            payload["data"]["relationships"] = {}

        tag_bindings_data = []
        for tag in tags:
            if not isinstance(tag, dict) or "key" not in tag or "value" not in tag:
                return {
                    "error": "Each tag must be a dictionary with 'key' and 'value' fields"
                }

            tag_bindings_data.append(
                {
                    "type": "tag-bindings",
                    "attributes": {"key": tag["key"], "value": tag["value"]},
                }
            )

        if tag_bindings_data:
            payload["data"]["relationships"]["tag-bindings"] = {
                "data": tag_bindings_data
            }

    # Make the API request
    success, data = await make_api_request(
        f"organizations/{organization}/workspaces", method="POST", data=payload
    )

    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary


async def update_workspace(
    organization: str,
    workspace_name: str,
    name: str = "",
    description: str = "",
    terraform_version: str = "",
    working_directory: str = "",
    auto_apply: Optional[bool] = None,
    file_triggers_enabled: Optional[bool] = None,
    trigger_prefixes: List[str] = [],
    trigger_patterns: List[str] = [],
    queue_all_runs: Optional[bool] = None,
    speculative_enabled: Optional[bool] = None,
    global_remote_state: Optional[bool] = None,
    execution_mode: str = "",
    allow_destroy_plan: Optional[bool] = None,
    auto_apply_run_trigger: Optional[bool] = None,
    project_id: str = "",
    vcs_repo: Dict[str, Any] = {},
    tags: List[Dict[str, str]] = [],
) -> dict:
    """
    Update an existing workspace in an organization

    Args:
        organization: The organization name (required)
        workspace_name: Current name of the workspace to update (required)
        name: New name for the workspace (optional)
        description: A description for the workspace
        terraform_version: Specific Terraform version to use
        working_directory: Relative path that Terraform will execute within
        auto_apply: Automatically apply changes when a Terraform plan is successful
        file_triggers_enabled: Whether to filter runs based on changed files in VCS
        trigger_prefixes: List of path prefixes that will trigger runs
        trigger_patterns: List of glob patterns that Terraform monitors for changes
        queue_all_runs: Whether runs should be queued immediately after workspace creation
        speculative_enabled: Whether this workspace allows automatic speculative plans
        global_remote_state: Whether all workspaces in the organization can access this workspace's state
        execution_mode: Which execution mode to use: "remote", "local", or "agent"
        allow_destroy_plan: Whether destroy plans can be queued on the workspace
        auto_apply_run_trigger: Whether to automatically apply changes from run triggers
        project_id: The ID of the project to move the workspace to
        vcs_repo: Settings for the workspace's VCS repository, or null to remove VCS
        tags: List of tags to attach to the workspace

    Returns:
        The updated workspace details
    """

    if not workspace_name:
        return {"error": "Current workspace name is required"}

    # Build the request payload
    payload: Dict[str, Any] = {"data": {"type": "workspaces", "attributes": {}}}

    # Add new name if provided
    if name:
        payload["data"]["attributes"]["name"] = name

    # Add optional attributes if provided
    if description:
        payload["data"]["attributes"]["description"] = description
    if terraform_version:
        payload["data"]["attributes"]["terraform-version"] = terraform_version
    if working_directory:
        payload["data"]["attributes"]["working-directory"] = working_directory

    # Add boolean attributes if specified
    if auto_apply is not None:
        payload["data"]["attributes"]["auto-apply"] = auto_apply
    if file_triggers_enabled is not None:
        payload["data"]["attributes"]["file-triggers-enabled"] = file_triggers_enabled
    if queue_all_runs is not None:
        payload["data"]["attributes"]["queue-all-runs"] = queue_all_runs
    if speculative_enabled is not None:
        payload["data"]["attributes"]["speculative-enabled"] = speculative_enabled
    if global_remote_state is not None:
        payload["data"]["attributes"]["global-remote-state"] = global_remote_state
    if allow_destroy_plan is not None:
        payload["data"]["attributes"]["allow-destroy-plan"] = allow_destroy_plan
    if auto_apply_run_trigger is not None:
        payload["data"]["attributes"]["auto-apply-run-trigger"] = auto_apply_run_trigger

    # Add trigger lists if provided
    if trigger_prefixes:
        payload["data"]["attributes"]["trigger-prefixes"] = trigger_prefixes
    if trigger_patterns:
        payload["data"]["attributes"]["trigger-patterns"] = trigger_patterns

    # Add execution mode if provided
    if execution_mode:
        if execution_mode not in ["remote", "local", "agent"]:
            return {
                "error": "Invalid execution mode. Must be one of: 'remote', 'local', 'agent'"
            }
        payload["data"]["attributes"]["execution-mode"] = execution_mode

    # Add VCS repository settings if provided
    if vcs_repo is not None:
        if not isinstance(vcs_repo, dict):
            return {"error": "vcs_repo must be a dictionary or null"}
        payload["data"]["attributes"]["vcs-repo"] = vcs_repo

    # Add project relationship if provided
    if project_id:
        if "relationships" not in payload["data"]:
            payload["data"]["relationships"] = {}
        payload["data"]["relationships"]["project"] = {
            "data": {"id": project_id, "type": "projects"}
        }

    # Add tags if provided
    if tags:
        if not isinstance(tags, list):
            return {"error": "tags must be a list"}

        if "relationships" not in payload["data"]:
            payload["data"]["relationships"] = {}

        tag_bindings_data = []
        for tag in tags:
            if not isinstance(tag, dict) or "key" not in tag or "value" not in tag:
                return {
                    "error": "Each tag must be a dictionary with 'key' and 'value' fields"
                }

            tag_bindings_data.append(
                {
                    "type": "tag-bindings",
                    "attributes": {"key": tag["key"], "value": tag["value"]},
                }
            )

        payload["data"]["relationships"]["tag-bindings"] = {"data": tag_bindings_data}

    # Make the API request
    success, data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}",
        method="PATCH",
        data=payload,
    )

    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary


async def delete_workspace(
    organization: str, workspace_name: str, confirm: bool = False
) -> dict:
    """
    Delete a workspace from an organization

    Args:
        organization: The organization name (required)
        workspace_name: The name of the workspace to delete (required)
        confirm: Set to True to confirm deletion, otherwise returns a confirmation request (default: False)

    Returns:
        Success message, confirmation request, or error details
    """

    if not workspace_name:
        return {"error": "Workspace name is required"}

    # If not confirmed, return a confirmation request
    if not confirm:
        return {
            "status": "confirmation_required",
            "message": f"WARNING: You're about to delete workspace '{workspace_name}' in organization '{organization}'. This will delete ALL configurations, variables, state files, and run history. This action cannot be undone. Call this function again with confirm=True to proceed.",
            "organization": organization,
            "workspace_name": workspace_name,
        }

    # Make the API request
    success, data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}", method="DELETE"
    )

    if success:
        return {
            "status": "success",
            "message": f"Workspace '{workspace_name}' deleted successfully",
        }
    else:
        return data  # Error info is already in the data dictionary


async def safe_delete_workspace(
    organization: str, workspace_name: str, confirm: bool = False
) -> dict:
    """
    Safely delete a workspace, but only if it's not managing any resources

    When you delete a Terraform workspace with resources, Terraform can no longer track
    or manage that infrastructure. During a safe delete, Terraform only deletes the
    workspace if it is not managing any resources.

    Args:
        organization: The organization name (required)
        workspace_name: The name of the workspace to delete (required)
        confirm: Set to True to confirm deletion, otherwise returns a confirmation request (default: False)

    Returns:
        Success message, confirmation request, or error details
    """

    if not workspace_name:
        return {"error": "Workspace name is required"}

    # If not confirmed, return a confirmation request
    if not confirm:
        return {
            "status": "confirmation_required",
            "message": f"WARNING: You're about to safely delete workspace '{workspace_name}' in organization '{organization}'. This will only proceed if the workspace is not managing any resources. If successful, this will delete all configurations, variables, and run history. Call this function again with confirm=True to proceed.",
            "organization": organization,
            "workspace_name": workspace_name,
        }

    # Make the safe-delete API request
    success, data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}/actions/safe-delete",
        method="POST",
    )

    if success:
        return {
            "status": "success",
            "message": f"Workspace '{workspace_name}' safely deleted successfully",
        }
    else:
        return data  # Error info is already in the data dictionary


async def lock_workspace(
    organization: str, workspace_name: str, reason: str = ""
) -> dict:
    """
    Lock a workspace to prevent Terraform runs

    Args:
        organization: The organization name (required)
        workspace_name: The name of the workspace to lock (required)
        reason: Optional reason for locking the workspace

    Returns:
        Updated workspace details or error message
    """

    if not workspace_name:
        return {"error": "Workspace name is required"}

    # Build the request payload
    payload = {
        "data": {
            "reason": reason if reason else "Locked via Terraform Cloud MCP Server"
        }
    }

    # First, get the workspace ID
    id_success, id_data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}"
    )

    if not id_success:
        return id_data  # Return error from workspace lookup

    # Extract the workspace ID
    try:
        workspace_id = id_data["data"]["id"]
    except (KeyError, TypeError):
        return {"error": "Failed to get workspace ID"}

    # Make the API request
    success, data = await make_api_request(
        f"workspaces/{workspace_id}/actions/lock", method="POST", data=payload
    )

    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary


async def unlock_workspace(organization: str, workspace_name: str) -> dict:
    """
    Unlock a workspace to allow Terraform runs

    Args:
        organization: The organization name (required)
        workspace_name: The name of the workspace to unlock (required)

    Returns:
        Updated workspace details or error message
    """

    if not workspace_name:
        return {"error": "Workspace name is required"}

    # First, get the workspace ID
    id_success, id_data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}"
    )

    if not id_success:
        return id_data  # Return error from workspace lookup

    # Extract the workspace ID
    try:
        workspace_id = id_data["data"]["id"]
    except (KeyError, TypeError):
        return {"error": "Failed to get workspace ID"}

    # Make the API request
    success, data = await make_api_request(
        f"workspaces/{workspace_id}/actions/unlock", method="POST"
    )

    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary


async def force_unlock_workspace(organization: str, workspace_name: str) -> dict:
    """
    Force unlock a workspace that may be locked by another user or process

    Args:
        organization: The organization name (required)
        workspace_name: The name of the workspace to force unlock (required)

    Returns:
        Updated workspace details or error message
    """

    if not workspace_name:
        return {"error": "Workspace name is required"}

    # First, get the workspace ID
    id_success, id_data = await make_api_request(
        f"organizations/{organization}/workspaces/{workspace_name}"
    )

    if not id_success:
        return id_data  # Return error from workspace lookup

    # Extract the workspace ID
    try:
        workspace_id = id_data["data"]["id"]
    except (KeyError, TypeError):
        return {"error": "Failed to get workspace ID"}

    # Make the API request
    success, data = await make_api_request(
        f"workspaces/{workspace_id}/actions/force-unlock", method="POST"
    )

    if success:
        return data
    else:
        return data  # Error info is already in the data dictionary
