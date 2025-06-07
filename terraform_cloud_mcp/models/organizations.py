"""Organization models for Terraform Cloud API

This module contains models for Terraform Cloud organization-related requests.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations
"""

from typing import Optional, Union

from pydantic import Field

from .base import APIRequest, CollaboratorAuthPolicy, ExecutionMode


class OrganizationDetailsRequest(APIRequest):
    """Request model for getting organization details.

    This model is used for the GET /organizations/{name} endpoint. The endpoint
    returns detailed information about an organization including its name,
    external ID, created date, and all organization-level settings.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations#show-an-organization

    See:
        docs/models/organization.md for reference
    """

    organization: str = Field(
        ...,
        # No alias needed as field name matches API field name
        description="The name of the organization to retrieve details for",
        min_length=3,
        pattern=r"^[a-z0-9][-a-z0-9_]*[a-z0-9]$",
    )


class OrganizationEntitlementsRequest(APIRequest):
    """Request model for getting organization entitlements.

    This model is used for the GET /organizations/{name}/entitlement-set endpoint.
    The endpoint returns information about which features and capabilities are
    available to the organization based on its subscription tier.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations#show-the-entitlement-set

    See:
        docs/models/organization.md for reference
    """

    organization: str = Field(
        ...,
        # No alias needed as field name matches API field name
        description="The name of the organization to retrieve entitlements for",
        min_length=3,
        pattern=r"^[a-z0-9][-a-z0-9_]*[a-z0-9]$",
    )


class OrganizationDeleteRequest(APIRequest):
    """Request model for deleting an organization.

    This model is used for the DELETE /organizations/{name} endpoint.
    Deleting an organization is a permanent action and cannot be undone.
    All workspaces, configurations, and associated resources will be deleted.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations#delete-an-organization

    Warning:
        This is a destructive operation that cannot be undone. Organization names
        are globally unique and cannot be recreated with the same name later.

    See:
        docs/models/organization.md for reference
    """

    organization: str = Field(
        ...,
        # No alias needed as field name matches API field name
        description="The name of the organization to delete",
        min_length=3,
        pattern=r"^[a-z0-9][-a-z0-9_]*[a-z0-9]$",
    )


class OrganizationListRequest(APIRequest):
    """Request parameters for listing organizations.

    These parameters map to the query parameters in the organizations API.
    The endpoint returns a paginated list of organizations that the authenticated
    user has access to, along with their details.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations#list-organizations

    See:
        docs/models/organization.md for reference
    """

    page_number: Optional[int] = Field(1, ge=1, description="Page number to fetch")
    page_size: Optional[int] = Field(
        20, ge=1, le=100, description="Number of results per page"
    )
    q: Optional[str] = Field(
        None, description="Search query for name and email", max_length=100
    )
    query_email: Optional[str] = Field(
        None, description="Search query for email", max_length=100
    )
    query_name: Optional[str] = Field(
        None, description="Search query for name", max_length=100
    )


class BaseOrganizationRequest(APIRequest):
    """Base class for organization create and update requests with common fields.

    This includes all fields that are commonly used in request payloads for the organization
    creation and update APIs.
    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations

    Note:
        This class inherits model_config from APIRequest -> BaseModelConfig

    See:
        docs/models/organization.md for fields and usage examples
    """

    # Fields common to both create and update requests with API defaults from docs
    name: Optional[str] = Field(
        None,
        # No alias needed as field name matches API field name
        description="Name of the organization",
        min_length=3,
        pattern=r"^[a-z0-9][-a-z0-9_]*[a-z0-9]$",
    )
    email: Optional[str] = Field(
        None,
        # No alias needed as field name matches API field name
        description="Admin email address",
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    )
    session_timeout: Optional[int] = Field(
        20160,
        alias="session-timeout",
        description="Session timeout after inactivity in minutes",
        ge=1,
        le=43200,  # 30 days in minutes
    )
    session_remember: Optional[int] = Field(
        20160,
        alias="session-remember",
        description="Session expiration in minutes",
        ge=1,
        le=43200,  # 30 days in minutes
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
    """Request model for creating a Terraform Cloud organization.

    Validates and structures the request according to the Terraform Cloud API
    requirements for creating organizations.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations#create-an-organization

    Note:
        This inherits all configuration fields from BaseOrganizationRequest
        while making name and email required.

    See:
        docs/models/organization.md for reference
    """

    # Override name and email to make them required for creation
    name: str = Field(..., description="Name of the organization")
    email: str = Field(..., description="Admin email address")


class OrganizationUpdateRequest(BaseOrganizationRequest):
    """Request model for updating a Terraform Cloud organization.

    Validates and structures the request according to the Terraform Cloud API
    requirements for updating organizations. All fields are optional.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations#update-an-organization

    Note:
        This inherits all configuration fields from BaseOrganizationRequest
        and adds a required organization field for routing.

    See:
        docs/models/organization.md for reference
    """

    # Add organization field which is required for updates but not part of the attributes
    organization: str = Field(
        ...,
        # No alias needed as field name matches API field name
        description="The name of the organization to update",
    )


class OrganizationParams(BaseOrganizationRequest):
    """Parameters for organization operations without routing fields.

    This model provides all optional parameters that can be used when creating or updating
    organizations, reusing the field definitions from BaseOrganizationRequest.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations

    Note:
        All fields are inherited from BaseOrganizationRequest.

    See:
        docs/models/organization.md for reference
    """

    # Inherits model_config and all fields from BaseOrganizationRequest


# Response handling is implemented through raw dictionaries
