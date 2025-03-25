"""Run models for Terraform Cloud API

This module contains models for Terraform Cloud run-related requests.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run
"""

from enum import Enum
from typing import List, Optional

from pydantic import Field, ConfigDict

from models.base import APIRequest


class RunOperation(str, Enum):
    """Operation options for runs."""

    PLAN_ONLY = "plan_only"
    PLAN_AND_APPLY = "plan_and_apply"
    SAVE_PLAN = "save_plan"
    REFRESH_ONLY = "refresh_only"
    DESTROY = "destroy"
    EMPTY_APPLY = "empty_apply"


class RunStatus(str, Enum):
    """Status options for runs."""

    PENDING = "pending"
    FETCHING = "fetching"
    FETCHING_COMPLETED = "fetching_completed"
    PRE_PLAN_RUNNING = "pre_plan_running"
    PRE_PLAN_COMPLETED = "pre_plan_completed"
    QUEUING = "queuing"
    PLAN_QUEUED = "plan_queued"
    PLANNING = "planning"
    PLANNED = "planned"
    COST_ESTIMATING = "cost_estimating"
    COST_ESTIMATED = "cost_estimated"
    POLICY_CHECKING = "policy_checking"
    POLICY_OVERRIDE = "policy_override"
    POLICY_SOFT_FAILED = "policy_soft_failed"
    POLICY_CHECKED = "policy_checked"
    CONFIRMED = "confirmed"
    POST_PLAN_RUNNING = "post_plan_running"
    POST_PLAN_COMPLETED = "post_plan_completed"
    PLANNED_AND_FINISHED = "planned_and_finished"
    PLANNED_AND_SAVED = "planned_and_saved"
    APPLY_QUEUED = "apply_queued"
    APPLYING = "applying"
    APPLIED = "applied"
    DISCARDED = "discarded"
    ERRORED = "errored"
    CANCELED = "canceled"
    FORCE_CANCELED = "force_canceled"


class RunSource(str, Enum):
    """Source options for runs."""

    TFE_UI = "tfe-ui"
    TFE_API = "tfe-api"
    TFE_CONFIGURATION_VERSION = "tfe-configuration-version"


class RunStatusGroup(str, Enum):
    """Status group options for runs."""

    NON_FINAL = "non_final"
    FINAL = "final"
    DISCARDABLE = "discardable"


class RunVariable(APIRequest):
    """Model for run-specific variables."""

    key: str = Field(..., description="Variable key")
    value: str = Field(..., description="Variable value")


class RunListInWorkspaceRequest(APIRequest):
    """
    Request parameters for listing runs in a workspace.

    These parameters map to the query parameters in the runs API.
    """

    workspace_id: str = Field(..., description="The workspace ID to list runs for")
    page_number: Optional[int] = Field(1, ge=1, description="Page number to fetch")
    page_size: Optional[int] = Field(
        20, ge=1, le=100, description="Number of results per page"
    )
    filter_operation: Optional[str] = Field(
        None, description="Filter runs by operation type, comma-separated"
    )
    filter_status: Optional[str] = Field(
        None, description="Filter runs by status, comma-separated"
    )
    filter_source: Optional[str] = Field(
        None, description="Filter runs by source, comma-separated"
    )
    filter_status_group: Optional[str] = Field(
        None, description="Filter runs by status group"
    )
    filter_timeframe: Optional[str] = Field(
        None, description="Filter runs by timeframe"
    )
    filter_agent_pool_names: Optional[str] = Field(
        None, description="Filter runs by agent pool names, comma-separated"
    )
    search_user: Optional[str] = Field(
        None, description="Search for runs by VCS username"
    )
    search_commit: Optional[str] = Field(
        None, description="Search for runs by commit SHA"
    )
    search_basic: Optional[str] = Field(
        None,
        description="Basic search across run ID, message, commit SHA, and username",
    )


class RunListInOrganizationRequest(APIRequest):
    """
    Request parameters for listing runs in an organization.

    These parameters map to the query parameters in the runs API.
    """

    organization: str = Field(..., description="The organization name")
    page_number: Optional[int] = Field(1, ge=1, description="Page number to fetch")
    page_size: Optional[int] = Field(
        20, ge=1, le=100, description="Number of results per page"
    )
    filter_operation: Optional[str] = Field(
        None, description="Filter runs by operation type, comma-separated"
    )
    filter_status: Optional[str] = Field(
        None, description="Filter runs by status, comma-separated"
    )
    filter_source: Optional[str] = Field(
        None, description="Filter runs by source, comma-separated"
    )
    filter_status_group: Optional[str] = Field(
        None, description="Filter runs by status group"
    )
    filter_timeframe: Optional[str] = Field(
        None, description="Filter runs by timeframe"
    )
    filter_agent_pool_names: Optional[str] = Field(
        None, description="Filter runs by agent pool names, comma-separated"
    )
    filter_workspace_names: Optional[str] = Field(
        None, description="Filter runs by workspace names, comma-separated"
    )
    search_user: Optional[str] = Field(
        None, description="Search for runs by VCS username"
    )
    search_commit: Optional[str] = Field(
        None, description="Search for runs by commit SHA"
    )
    search_basic: Optional[str] = Field(
        None,
        description="Basic search across run ID, message, commit SHA, and username",
    )


class BaseRunRequest(APIRequest):
    """Base class for run requests with common fields.

    This includes all fields that are commonly used in request payloads for the run
    creation API.
    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra="ignore",
    )

    # Optional fields with their defaults
    message: Optional[str] = Field(None, description="Message to include with the run")
    auto_apply: Optional[bool] = Field(
        None,
        alias="auto-apply",
        description="Whether to auto-apply the run when planned (defaults to workspace setting)",
    )
    is_destroy: Optional[bool] = Field(
        False,
        alias="is-destroy",
        description="Whether this run should destroy all resources",
    )
    refresh: Optional[bool] = Field(
        True, description="Whether to refresh state before plan"
    )
    refresh_only: Optional[bool] = Field(
        False, alias="refresh-only", description="Whether this is a refresh-only run"
    )
    plan_only: Optional[bool] = Field(
        False,
        alias="plan-only",
        description="Whether this is a speculative, plan-only run",
    )
    allow_empty_apply: Optional[bool] = Field(
        False,
        alias="allow-empty-apply",
        description="Whether to allow apply when there are no changes",
    )
    allow_config_generation: Optional[bool] = Field(
        False,
        alias="allow-config-generation",
        description="Whether to allow generating config for imports",
    )
    target_addrs: Optional[List[str]] = Field(
        None, alias="target-addrs", description="Resource addresses to target"
    )
    replace_addrs: Optional[List[str]] = Field(
        None, alias="replace-addrs", description="Resource addresses to replace"
    )
    variables: Optional[List[RunVariable]] = Field(
        None, description="Run-specific variables"
    )
    terraform_version: Optional[str] = Field(
        None,
        alias="terraform-version",
        description="Specific Terraform version (only valid for plan-only runs)",
    )
    save_plan: Optional[bool] = Field(
        False,
        alias="save-plan",
        description="Whether to save the plan without becoming the current run",
    )
    debugging_mode: Optional[bool] = Field(
        False, alias="debugging-mode", description="Enable debug logging for this run"
    )


class RunCreateRequest(BaseRunRequest):
    """
    Request model for creating a Terraform Cloud run.

    Validates and structures the request according to the Terraform Cloud API
    requirements for creating runs.
    """

    # Required fields
    workspace_id: str = Field(..., description="The workspace ID to execute the run in (required)")

    # Optional fields specific to run creation
    configuration_version_id: Optional[str] = Field(
        None,
        alias="configuration-version-id",
        description="The configuration version ID to use",
    )


class RunActionRequest(APIRequest):
    """
    Base request model for run actions like apply, discard, cancel, etc.

    This model provides common fields used in run action requests.
    """

    run_id: str = Field(..., description="The ID of the run to perform an action on")
    comment: Optional[str] = Field(
        None, description="An optional comment about the run"
    )


class RunParams(BaseRunRequest):
    """
    Parameters for run operations without routing fields.

    This model provides all optional parameters that can be used when creating runs,
    reusing the field definitions from BaseRunRequest.

    Usage:
        params = RunParams(message="Triggered by API", auto_apply=True)
        create_run("my-org", "my-workspace", params)
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra="ignore",
    )

    # All fields are inherited from BaseRunRequest
    configuration_version_id: Optional[str] = Field(
        None,
        alias="configuration-version-id",
        description="The configuration version ID to use",
    )


# Response handling is implemented through raw dictionaries
