"""Project models for Terraform Cloud API

This module contains models for Terraform Cloud project-related requests.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects
"""

from typing import List, Optional

from pydantic import Field

from .base import APIRequest


class TagBinding(APIRequest):
    """Tag binding configuration for a project.

    Defines a tag key-value pair that can be bound to a project
    and inherited by its workspaces.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects

    See:
        docs/models/project.md for reference
    """

    # Inherits model_config from APIRequest -> BaseModelConfig

    key: str = Field(..., description="The key of the tag")
    value: str = Field(..., description="The value of the tag")


class ProjectListRequest(APIRequest):
    """Request parameters for listing projects in an organization.

    Defines the parameters for the project listing API including pagination
    and search filtering options.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#list-projects

    See:
        docs/models/project.md for reference
    """

    organization: str = Field(
        ...,
        description="The name of the organization to list projects from",
        min_length=3,
        pattern=r"^[a-z0-9][-a-z0-9_]*[a-z0-9]$",
    )
    page_number: Optional[int] = Field(1, ge=1, description="Page number to fetch")
    page_size: Optional[int] = Field(
        20, ge=1, le=100, description="Number of results per page"
    )
    q: Optional[str] = Field(None, description="Search query for name")
    filter_names: Optional[str] = Field(
        None, description="Filter projects by name (comma-separated)"
    )
    filter_permissions_update: Optional[bool] = Field(
        None, description="Filter projects by update permission"
    )
    filter_permissions_create_workspace: Optional[bool] = Field(
        None, description="Filter projects by create workspace permission"
    )
    sort: Optional[str] = Field(
        None, description="Sort projects by name ('name' or '-name' for descending)"
    )


class BaseProjectRequest(APIRequest):
    """Base class for project create and update requests with common fields.

    This includes common fields used in request payloads for project
    creation and update APIs, providing a foundation for more specific project models.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects

    Note:
        This class inherits model_config from APIRequest -> BaseModelConfig and provides
        default values for fields based on Terraform Cloud API defaults.

    See:
        docs/models/project.md for detailed field descriptions and usage examples
    """

    # Fields common to both create and update requests
    name: Optional[str] = Field(
        None,
        description="Name of the project",
    )
    description: Optional[str] = Field(
        None,
        description="Description of the project",
    )
    auto_destroy_activity_duration: Optional[str] = Field(
        None,
        alias="auto-destroy-activity-duration",
        description="How long each workspace should wait before auto-destroying (e.g., '14d', '24h')",
    )
    tag_bindings: Optional[List[TagBinding]] = Field(
        None,
        alias="tag-bindings",
        description="Tags to bind to the project, inherited by workspaces",
    )


class ProjectCreateRequest(BaseProjectRequest):
    """Request model for creating a Terraform Cloud project.

    Validates and structures the request according to the Terraform Cloud API
    requirements for creating projects. Extends BaseProjectRequest with
    required fields for creation.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#create-a-project

    Note:
        This inherits all configuration fields from BaseProjectRequest
        while making organization and name required.

    See:
        docs/models/project.md for reference
    """

    # Organization is needed for routing but not included in the payload
    organization: str = Field(
        ...,
        description="The name of the organization to create the project in",
    )

    # Override name to make it required for creation
    name: str = Field(
        ...,
        description="Name of the project",
    )


class ProjectUpdateRequest(BaseProjectRequest):
    """Request model for updating a Terraform Cloud project.

    Validates and structures the request for updating projects. Extends BaseProjectRequest
    with routing fields while keeping all configuration fields optional.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#update-a-project

    Note:
        This inherits all configuration fields from BaseProjectRequest
        and adds required routing field for the update operation.

    See:
        docs/models/project.md for reference
    """

    # Add project_id which is required for updates but not part of the project attributes payload
    project_id: str = Field(
        ...,
        description="The ID of the project to update",
    )


class ProjectParams(BaseProjectRequest):
    """Parameters for project operations without routing fields.

    This model provides all optional parameters for creating or updating projects,
    reusing field definitions from BaseProjectRequest. It separates configuration
    parameters from routing information like organization and project ID.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects

    Note:
        When updating a project, use this model to specify only the attributes
        you want to change. Unspecified attributes retain their current values.
        All fields are inherited from BaseProjectRequest.

    See:
        docs/models/project.md for reference
    """

    # Inherits model_config and all fields from BaseProjectRequest


class ProjectTagBindingRequest(APIRequest):
    """Request model for adding or updating tag bindings on a project.

    This model is used for the PATCH /projects/{project_id}/tag-bindings endpoint,
    which allows adding or updating tag bindings on an existing project.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#add-or-update-tag-bindings-on-a-project

    See:
        docs/models/project.md for reference
    """

    project_id: str = Field(
        ...,
        description="The ID of the project to update tag bindings for",
    )
    tag_bindings: List[TagBinding] = Field(
        ...,
        description="Tags to bind to the project",
    )


class WorkspaceMoveRequest(APIRequest):
    """Request model for moving workspaces into a project.

    This model is used for the POST /projects/{project_id}/relationships/workspaces endpoint,
    which allows moving one or more workspaces into a project.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#move-workspaces-into-a-project

    See:
        docs/models/project.md for reference
    """

    project_id: str = Field(
        ...,
        description="The ID of the destination project",
    )
    workspace_ids: List[str] = Field(
        ...,
        description="The IDs of workspaces to move into the project",
    )
