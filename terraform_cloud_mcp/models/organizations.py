"""Organization models for Terraform Cloud API

This module contains models for Terraform Cloud organization-related requests.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations
"""

from enum import Enum
from typing import Optional, Union

from pydantic import Field, ConfigDict

from models.base import APIRequest


class CollaboratorAuthPolicy(str, Enum):
    """Authentication policy options for organization collaborators."""

    PASSWORD = "password"
    TWO_FACTOR_MANDATORY = "two_factor_mandatory"


class ExecutionMode(str, Enum):
    """Execution mode options for workspaces."""

    REMOTE = "remote"
    LOCAL = "local"
    AGENT = "agent"


class OrganizationListRequest(APIRequest):
    """
    Request parameters for listing organizations.

    These parameters map to the query parameters in the organizations API.
    """

    page_number: Optional[int] = Field(1, ge=1, description="Page number to fetch")
    page_size: Optional[int] = Field(
        20, ge=1, le=100, description="Number of results per page"
    )
    query: Optional[str] = Field(None, description="Search query for name and email")
    query_email: Optional[str] = Field(None, description="Search query for email")
    query_name: Optional[str] = Field(None, description="Search query for name")


class BaseOrganizationRequest(APIRequest):
    """Base class for organization create and update requests with common fields."""

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra="ignore",
    )

    # Fields common to both create and update requests with API defaults from docs
    name: Optional[str] = Field(None, description="Name of the organization")
    email: Optional[str] = Field(None, description="Admin email address")
    session_timeout: Optional[int] = Field(
        20160,
        alias="session-timeout",
        description="Session timeout after inactivity in minutes",
    )
    session_remember: Optional[int] = Field(
        20160, alias="session-remember", description="Session expiration in minutes"
    )
    collaborator_auth_policy: Optional[Union[str, CollaboratorAuthPolicy]] = Field(
        CollaboratorAuthPolicy.PASSWORD,
        alias="collaborator-auth-policy",
        description="Authentication policy",
    )
    cost_estimation_enabled: Optional[bool] = Field(
        False,
        alias="cost-estimation-enabled",
        description="Whether cost estimation is enabled for all workspaces",
    )
    send_passing_statuses_for_untriggered_speculative_plans: Optional[bool] = Field(
        False,
        alias="send-passing-statuses-for-untriggered-speculative-plans",
        description="Whether to send VCS status updates for untriggered plans",
    )
    aggregated_commit_status_enabled: Optional[bool] = Field(
        True,
        alias="aggregated-commit-status-enabled",
        description="Whether to aggregate VCS status updates",
    )
    speculative_plan_management_enabled: Optional[bool] = Field(
        True,
        alias="speculative-plan-management-enabled",
        description="Whether to enable automatic cancellation of plan-only runs",
    )
    owners_team_saml_role_id: Optional[str] = Field(
        None,
        alias="owners-team-saml-role-id",
        description="SAML only - the name of the 'owners' team",
    )
    assessments_enforced: Optional[bool] = Field(
        False,
        alias="assessments-enforced",
        description="Whether to compel health assessments for all eligible workspaces",
    )
    allow_force_delete_workspaces: Optional[bool] = Field(
        False,
        alias="allow-force-delete-workspaces",
        description="Whether workspace admins can delete workspaces with resources",
    )
    default_execution_mode: Optional[Union[str, ExecutionMode]] = Field(
        ExecutionMode.REMOTE,
        alias="default-execution-mode",
        description="Default execution mode",
    )
    default_agent_pool_id: Optional[str] = Field(
        None,
        alias="default-agent-pool-id",
        description="The ID of the agent pool (required when default_execution_mode is 'agent')",
    )


class OrganizationCreateRequest(BaseOrganizationRequest):
    """
    Request model for creating a Terraform Cloud organization.

    Validates and structures the request according to the Terraform Cloud API
    requirements for creating organizations.
    """

    # Override name and email to make them required for creation
    name: str = Field(..., description="Name of the organization")
    email: str = Field(..., description="Admin email address")


class OrganizationUpdateRequest(BaseOrganizationRequest):
    """
    Request model for updating a Terraform Cloud organization.

    Validates and structures the request according to the Terraform Cloud API
    requirements for updating organizations. All fields are optional.
    """

    # Add organization field which is required for updates but not part of the attributes
    organization: str = Field(..., description="The name of the organization to update")


# Response handling is implemented through raw dictionaries
