"""Run models for Terraform Cloud API

This module contains models for Terraform Cloud run-related requests.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run
"""

from enum import Enum
from typing import List, Optional

from pydantic import Field

from .base import APIRequest


class RunOperation(str, Enum):
    """Operation options for runs in Terraform Cloud.

    Defines the different types of operations a run can perform:
    - PLAN_ONLY: Create a plan without applying changes
    - PLAN_AND_APPLY: Create a plan and apply if approved
    - SAVE_PLAN: Save the plan for later use
    - REFRESH_ONLY: Only refresh state without planning changes
    - DESTROY: Destroy all resources
    - EMPTY_APPLY: Apply even with no changes detected

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run#list-runs-in-a-workspace

    See:
        docs/models/run.md for reference
    """

    PLAN_ONLY = "plan_only"
    PLAN_AND_APPLY = "plan_and_apply"
    SAVE_PLAN = "save_plan"
    REFRESH_ONLY = "refresh_only"
    DESTROY = "destroy"
    EMPTY_APPLY = "empty_apply"


class RunStatus(str, Enum):
    """Status options for runs in Terraform Cloud.

    Defines the various states a run can be in during its lifecycle,
    from initial creation through planning, policy checks, application,
    and completion or cancellation.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run#list-runs-in-a-workspace

    See:
        docs/models/run.md for reference
    """

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
    """Source options for runs in Terraform Cloud.

    Identifies the origin of a run:
    - TFE_UI: Created through the Terraform Cloud web interface
    - TFE_API: Created through the API
    - TFE_CONFIGURATION_VERSION: Created by uploading a configuration version

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run#list-runs-in-a-workspace

    See:
        docs/models/run.md for reference
    """

    TFE_UI = "tfe-ui"
    TFE_API = "tfe-api"
    TFE_CONFIGURATION_VERSION = "tfe-configuration-version"


class RunStatusGroup(str, Enum):
    """Status group options for categorizing runs.

    Groups run statuses into categories for filtering:
    - NON_FINAL: Runs that are still in progress
    - FINAL: Runs that have reached a terminal state
    - DISCARDABLE: Runs that can be discarded

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run#list-runs-in-a-workspace

    See:
        docs/models/run.md for reference
    """

    NON_FINAL = "non_final"
    FINAL = "final"
    DISCARDABLE = "discardable"


class RunVariable(APIRequest):
    """Model for run-specific variables.

    Run variables are used to provide input values for a specific run,
    which override any workspace variables for that run only.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run#create-a-run

    See:
        docs/models/run.md for reference
    """

    key: str = Field(
        ...,
        # No alias needed as field name matches API field name
        description="Variable key",
        min_length=1,
        max_length=128,
    )
    value: str = Field(
        ...,
        # No alias needed as field name matches API field name
        description="Variable value",
        max_length=256,
    )


class RunListInWorkspaceRequest(APIRequest):
    """Request parameters for listing runs in a workspace.

    Used with the GET /workspaces/{workspace_id}/runs endpoint to retrieve
    and filter run data for a specific workspace.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run#list-runs-in-a-workspace

    See:
        docs/models/run.md for reference
    """

    workspace_id: str = Field(
        ...,
        description="The workspace ID to list runs for",
        pattern=r"^ws-[a-zA-Z0-9]{16}$",  # Standardized workspace ID pattern
    )
    page_number: Optional[int] = Field(1, ge=1, description="Page number to fetch")
    page_size: Optional[int] = Field(
        20, ge=1, le=100, description="Number of results per page"
    )
    filter_operation: Optional[str] = Field(
        None,
        description="Filter runs by operation type, comma-separated",
        max_length=100,
    )
    filter_status: Optional[str] = Field(
        None, description="Filter runs by status, comma-separated", max_length=100
    )
    filter_source: Optional[str] = Field(
        None, description="Filter runs by source, comma-separated", max_length=100
    )
    filter_status_group: Optional[str] = Field(
        None, description="Filter runs by status group", max_length=50
    )
    filter_timeframe: Optional[str] = Field(
        None, description="Filter runs by timeframe", max_length=50
    )
    filter_agent_pool_names: Optional[str] = Field(
        None,
        description="Filter runs by agent pool names, comma-separated",
        max_length=100,
    )
    search_user: Optional[str] = Field(
        None, description="Search for runs by VCS username", max_length=100
    )
    search_commit: Optional[str] = Field(
        None, description="Search for runs by commit SHA", max_length=40
    )
    search_basic: Optional[str] = Field(
        None,
        description="Basic search across run ID, message, commit SHA, and username",
        max_length=100,
    )


class RunListInOrganizationRequest(APIRequest):
    """Request parameters for listing runs in an organization.

    These parameters map to the query parameters in the runs API.
    The endpoint returns a paginated list of runs across all workspaces in an organization,
    with options for filtering by workspace name, status, and other criteria.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run#list-runs-in-an-organization

    See:
        docs/models/run.md for reference
    """

    organization: str = Field(
        ...,
        description="The organization name",
        min_length=3,
        pattern=r"^[a-z0-9][-a-z0-9_]*[a-z0-9]$",
    )
    page_number: Optional[int] = Field(1, ge=1, description="Page number to fetch")
    page_size: Optional[int] = Field(
        20, ge=1, le=100, description="Number of results per page"
    )
    filter_operation: Optional[str] = Field(
        None,
        description="Filter runs by operation type, comma-separated",
        max_length=100,
    )
    filter_status: Optional[str] = Field(
        None, description="Filter runs by status, comma-separated", max_length=100
    )
    filter_source: Optional[str] = Field(
        None, description="Filter runs by source, comma-separated", max_length=100
    )
    filter_status_group: Optional[str] = Field(
        None, description="Filter runs by status group", max_length=50
    )
    filter_timeframe: Optional[str] = Field(
        None, description="Filter runs by timeframe", max_length=50
    )
    filter_agent_pool_names: Optional[str] = Field(
        None,
        description="Filter runs by agent pool names, comma-separated",
        max_length=100,
    )
    filter_workspace_names: Optional[str] = Field(
        None,
        description="Filter runs by workspace names, comma-separated",
        max_length=250,
    )
    search_user: Optional[str] = Field(
        None, description="Search for runs by VCS username", max_length=100
    )
    search_commit: Optional[str] = Field(
        None, description="Search for runs by commit SHA", max_length=40
    )
    search_basic: Optional[str] = Field(
        None,
        description="Basic search across run ID, message, commit SHA, and username",
        max_length=100,
    )


class BaseRunRequest(APIRequest):
    """Base class for run requests with common fields.

    Common fields shared across run creation and management APIs.
    Provides field definitions and validation rules for run operations.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run

    Note:
        Consolidates common parameters for consistency across endpoints

    See:
        docs/models/run.md for reference
    """

    # Inherits model_config from APIRequest -> BaseModelConfig

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
    """Request model for creating a Terraform Cloud run.

    Validates and structures the request according to the Terraform Cloud API
    requirements for creating runs. The model inherits common run attributes from
    BaseRunRequest and adds workspace_id as a required parameter.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run#create-a-run

    Note:
        This inherits all configuration fields from BaseRunRequest
        and adds workspace_id as a required parameter.
        This model is typically used internally by the create_run tool function,
        which accepts parameters directly and constructs the request object.

    See:
        docs/models/run.md for reference
    """

    # Required fields
    workspace_id: str = Field(
        ...,
        # No alias needed as field name matches API field name
        description="The workspace ID to execute the run in (required)",
        pattern=r"^ws-[a-zA-Z0-9]{16}$",  # Standardized workspace ID pattern
    )

    # Optional fields specific to run creation
    configuration_version_id: Optional[str] = Field(
        None,
        alias="configuration-version-id",
        description="The configuration version ID to use",
        pattern=r"^cv-[a-zA-Z0-9]{16}$",
    )


class RunActionRequest(APIRequest):
    """Base request model for run actions like apply, discard, cancel, etc.

    This model provides common fields used in run action requests such as
    applying, discarding, or canceling runs. It includes the run ID and
    an optional comment field that can be included with the action.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run#apply-a-run

    Note:
        This model is used for multiple run action endpoints that share the
        same basic structure but perform different operations on the run.

    See:
        docs/models/run.md for reference
    """

    run_id: str = Field(
        ...,
        # No alias needed as field name matches API field name
        description="The ID of the run to perform an action on",
        pattern=r"^run-[a-zA-Z0-9]{16}$",
    )
    comment: Optional[str] = Field(
        None,
        # No alias needed as field name matches API field name
        description="An optional comment about the run",
    )


class RunParams(BaseRunRequest):
    """Parameters for run operations without routing fields.

    This model provides all optional parameters that can be used when creating runs,
    reusing the field definitions from BaseRunRequest.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run#create-a-run

    Note:
        All fields are inherited from BaseRunRequest.

    See:
        docs/models/run.md for reference
    """

    # Inherits model_config and all fields from BaseRunRequest


# Response handling is implemented through raw dictionaries
