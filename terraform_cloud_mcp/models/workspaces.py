"""Workspace models for Terraform Cloud API

This module contains models for Terraform Cloud workspace-related requests.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces
"""

from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import Field, ConfigDict

from models.base import APIRequest


class ExecutionMode(str, Enum):
    """Execution mode options for workspaces."""

    REMOTE = "remote"
    LOCAL = "local"
    AGENT = "agent"


class VcsRepoConfig(APIRequest):
    """VCS repository configuration for a workspace."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )

    branch: Optional[str] = Field(
        None, description="The repository branch that Terraform executes from"
    )
    identifier: Optional[str] = Field(
        None, description="A reference to your VCS repository in the format :org/:repo"
    )
    ingress_submodules: Optional[bool] = Field(
        None,
        alias="ingress-submodules",
        description="Whether submodules should be fetched when cloning the VCS repository",
    )
    oauth_token_id: Optional[str] = Field(
        None,
        alias="oauth-token-id",
        description="Specifies the VCS OAuth connection and token",
    )
    github_app_installation_id: Optional[str] = Field(
        None,
        alias="github-app-installation-id",
        description="The VCS Connection GitHub App Installation to use",
    )
    tags_regex: Optional[str] = Field(
        None,
        alias="tags-regex",
        description="A regular expression used to match Git tags",
    )


class WorkspaceListRequest(APIRequest):
    """
    Request parameters for listing workspaces in an organization.

    These parameters map to the query parameters in the workspace listing API.
    """

    organization_name: str = Field(
        ..., description="The name of the organization to list workspaces from"
    )
    page_number: Optional[int] = Field(1, ge=1, description="Page number to fetch")
    page_size: Optional[int] = Field(
        20, ge=1, le=100, description="Number of results per page"
    )
    search: Optional[str] = Field(None, description="Substring to search for")


class BaseWorkspaceRequest(APIRequest):
    """Base class for workspace create and update requests with common fields.

    This includes all fields that are commonly used in request payloads for the workspace
    creation and update APIs.
    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra="ignore",
    )

    # Fields common to both create and update requests with API defaults from docs
    name: Optional[str] = Field(None, description="Name of the workspace")
    description: Optional[str] = Field(None, description="Description of the workspace")
    execution_mode: Optional[Union[str, ExecutionMode]] = Field(
        ExecutionMode.REMOTE,
        alias="execution-mode",
        description="How operations are executed",
    )
    agent_pool_id: Optional[str] = Field(
        None, alias="agent-pool-id", description="The ID of the agent pool"
    )
    assessments_enabled: Optional[bool] = Field(
        False,
        alias="assessments-enabled",
        description="Whether to perform health assessments",
    )
    auto_apply: Optional[bool] = Field(
        False,
        alias="auto-apply",
        description="Whether to automatically apply changes in runs triggered by VCS, UI, or CLI",
    )
    auto_apply_run_trigger: Optional[bool] = Field(
        False,
        alias="auto-apply-run-trigger",
        description="Whether to automatically apply changes initiated by run triggers",
    )
    auto_destroy_at: Optional[str] = Field(
        None,
        alias="auto-destroy-at",
        description="Timestamp when the next scheduled destroy run will occur",
    )
    auto_destroy_activity_duration: Optional[str] = Field(
        None,
        alias="auto-destroy-activity-duration",
        description="Value and units for automatically scheduled destroy runs based on workspace activity",
    )
    file_triggers_enabled: Optional[bool] = Field(
        True,
        alias="file-triggers-enabled",
        description="Whether to filter runs based on file paths",
    )
    working_directory: Optional[str] = Field(
        None,
        alias="working-directory",
        description="The directory to execute commands in",
    )
    speculative_enabled: Optional[bool] = Field(
        True,
        alias="speculative-enabled",
        description="Whether this workspace allows speculative plans",
    )
    terraform_version: Optional[str] = Field(
        "latest",
        alias="terraform-version",
        description="Specifies the version of Terraform to use for this workspace",
    )
    global_remote_state: Optional[bool] = Field(
        False,
        alias="global-remote-state",
        description="Whether to allow all workspaces to access this workspace's state",
    )
    vcs_repo: Optional[Union[VcsRepoConfig, None]] = Field(
        None,
        alias="vcs-repo",
        description="Settings for the workspace's VCS repository",
    )
    allow_destroy_plan: Optional[bool] = Field(
        True,
        alias="allow-destroy-plan",
        description="Whether to allow destruction plans",
    )
    queue_all_runs: Optional[bool] = Field(
        False,
        alias="queue-all-runs",
        description="Whether runs should be queued immediately",
    )
    source_name: Optional[str] = Field(
        None,
        alias="source-name",
        description="Indicates where the workspace settings originated",
    )
    source_url: Optional[str] = Field(
        None, alias="source-url", description="URL to origin source"
    )
    trigger_prefixes: Optional[List[str]] = Field(
        None, alias="trigger-prefixes", description="List of paths that trigger runs"
    )
    trigger_patterns: Optional[List[str]] = Field(
        None,
        alias="trigger-patterns",
        description="List of glob patterns that trigger runs",
    )
    setting_overwrites: Optional[Dict[str, bool]] = Field(
        None,
        alias="setting-overwrites",
        description="Specifies attributes that have organization-level defaults",
    )


class WorkspaceCreateRequest(BaseWorkspaceRequest):
    """
    Request model for creating a Terraform Cloud workspace.

    Validates and structures the request according to the Terraform Cloud API
    requirements for creating workspaces.
    """

    # Override organization_name and name to make them required for creation
    organization_name: str = Field(
        ..., description="The name of the organization to create the workspace in"
    )
    name: str = Field(..., description="Name of the workspace")


class WorkspaceUpdateRequest(BaseWorkspaceRequest):
    """
    Request model for updating a Terraform Cloud workspace.

    Validates and structures the request according to the Terraform Cloud API
    requirements for updating workspaces. All fields except organization_name and workspace_name
    are optional.
    """

    # Add fields which are required for updates but not part of the workspace attributes payload
    organization_name: str = Field(
        ..., description="The name of the organization that owns the workspace"
    )
    workspace_name: str = Field(..., description="The name of the workspace to update")


# Response handling is implemented through raw dictionaries
