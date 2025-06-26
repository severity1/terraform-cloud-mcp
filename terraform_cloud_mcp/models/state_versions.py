"""State version models for Terraform Cloud API

This module contains models for Terraform Cloud state version-related requests.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions
"""

from enum import Enum
from typing import Optional

from pydantic import Field

from .base import APIRequest


class StateVersionStatus(str, Enum):
    """Status options for state versions in Terraform Cloud.

    Defines the various states a state version can be in during its lifecycle:
    - PENDING: State version has been created but state data is not encoded within the request
    - FINALIZED: State version has been successfully uploaded or created with valid state attribute
    - DISCARDED: State version was discarded because it was superseded by a newer version
    - BACKING_DATA_SOFT_DELETED: Enterprise only - backing files are marked for garbage collection
    - BACKING_DATA_PERMANENTLY_DELETED: Enterprise only - backing files have been permanently deleted

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions#state-version-status

    See:
        docs/models/state_versions.md for reference
    """

    PENDING = "pending"
    FINALIZED = "finalized"
    DISCARDED = "discarded"
    BACKING_DATA_SOFT_DELETED = "backing_data_soft_deleted"
    BACKING_DATA_PERMANENTLY_DELETED = "backing_data_permanently_deleted"


class StateVersionListRequest(APIRequest):
    """Request parameters for listing state versions.

    Defines the parameters for the state version listing API including pagination
    and filtering options.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions#list-state-versions

    See:
        docs/models/state_versions.md for reference
    """

    workspace_name: str = Field(
        ...,
        description="The name of the workspace to list state versions for",
    )
    organization: str = Field(
        ...,
        description="The name of the organization that owns the workspace",
    )
    filter_status: Optional[StateVersionStatus] = Field(
        None,
        description="Filter state versions by status",
    )
    page_number: Optional[int] = Field(
        1,
        ge=1,
        description="Page number to fetch",
    )
    page_size: Optional[int] = Field(
        20,
        ge=1,
        le=100,
        description="Number of results per page",
    )


class StateVersionRequest(APIRequest):
    """Request model for retrieving a state version.

    Used to validate the state version ID parameter for API requests.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions

    See:
        docs/models/state_versions.md for reference
    """

    state_version_id: str = Field(
        ...,
        description="The ID of the state version to retrieve",
        pattern=r"^sv-[a-zA-Z0-9]{16}$",  # Standard state version ID pattern
    )


class CurrentStateVersionRequest(APIRequest):
    """Request model for retrieving a workspace's current state version.

    Used to validate the workspace ID parameter for current state version API requests.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions#get-current-state-version

    See:
        docs/models/state_versions.md for reference
    """

    workspace_id: str = Field(
        ...,
        description="The ID of the workspace to retrieve the current state version for",
        pattern=r"^ws-[a-zA-Z0-9]{16}$",  # Standard workspace ID pattern
    )


class StateVersionCreateRequest(APIRequest):
    """Request model for creating a state version.

    Validates and structures the request according to the Terraform Cloud API
    requirements for creating state versions.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions#create-a-state-version

    See:
        docs/models/state_versions.md for reference
    """

    workspace_id: str = Field(
        ...,
        description="The ID of the workspace to create a state version in",
        pattern=r"^ws-[a-zA-Z0-9]{16}$",  # Standard workspace ID pattern
    )
    serial: int = Field(
        ...,
        description="The serial of the state version",
        ge=0,
    )
    md5: str = Field(
        ...,
        description="An MD5 hash of the raw state version",
        pattern=r"^[a-fA-F0-9]{32}$",  # MD5 hash pattern
    )
    state: Optional[str] = Field(
        None,
        description="Base64 encoded raw state file",
    )
    lineage: Optional[str] = Field(
        None,
        description="Lineage of the state version",
    )
    json_state: Optional[str] = Field(
        None,
        alias="json-state",
        description='Base64 encoded json state, as expressed by "terraform show -json"',
    )
    json_state_outputs: Optional[str] = Field(
        None,
        alias="json-state-outputs",
        description='Base64 encoded output values as represented by "terraform show -json"',
    )
    run_id: Optional[str] = Field(
        None,
        description="The ID of the run to associate with the state version",
        pattern=r"^run-[a-zA-Z0-9]{16}$",  # Standard run ID pattern
    )


class StateVersionParams(APIRequest):
    """Parameters for state version operations without routing fields.

    This model provides all optional parameters for creating state versions,
    reusing field definitions from StateVersionCreateRequest. It separates configuration
    parameters from routing information.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions

    See:
        docs/models/state_versions.md for reference
    """

    serial: Optional[int] = Field(
        None,
        description="The serial of the state version",
        ge=0,
    )
    md5: Optional[str] = Field(
        None,
        description="An MD5 hash of the raw state version",
        pattern=r"^[a-fA-F0-9]{32}$",  # MD5 hash pattern
    )
    state: Optional[str] = Field(
        None,
        description="Base64 encoded raw state file",
    )
    lineage: Optional[str] = Field(
        None,
        description="Lineage of the state version",
    )
    json_state: Optional[str] = Field(
        None,
        alias="json-state",
        description='Base64 encoded json state, as expressed by "terraform show -json"',
    )
    json_state_outputs: Optional[str] = Field(
        None,
        alias="json-state-outputs",
        description='Base64 encoded output values as represented by "terraform show -json"',
    )
    run_id: Optional[str] = Field(
        None,
        description="The ID of the run to associate with the state version",
        pattern=r"^run-[a-zA-Z0-9]{16}$",  # Standard run ID pattern
    )


# Response handling is implemented through raw dictionaries
