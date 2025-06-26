"""State version output models for Terraform Cloud API

This module contains models for Terraform Cloud state version output-related requests.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-version-outputs
"""

from typing import Optional

from pydantic import Field

from .base import APIRequest


class StateVersionOutputListRequest(APIRequest):
    """Request parameters for listing state version outputs.

    Defines the parameters for the state version outputs listing API including pagination.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-version-outputs#list-state-version-outputs

    See:
        docs/models/state_version_outputs.md for reference
    """

    state_version_id: str = Field(
        ...,
        description="The ID of the state version to list outputs for",
        pattern=r"^sv-[a-zA-Z0-9]{16}$",  # Standard state version ID pattern
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


class StateVersionOutputRequest(APIRequest):
    """Request model for retrieving a specific state version output.

    Used to validate the state version output ID parameter for API requests.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-version-outputs#show-a-state-version-output

    See:
        docs/models/state_version_outputs.md for reference
    """

    state_version_output_id: str = Field(
        ...,
        description="The ID of the state version output to retrieve",
        pattern=r"^wsout-[a-zA-Z0-9]{16}$",  # Standard state version output ID pattern
    )


# Response handling is implemented through raw dictionaries