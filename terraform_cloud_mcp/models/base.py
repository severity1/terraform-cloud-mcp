"""Base models for Terraform Cloud MCP.

This module defines base models for Terraform Cloud API requests.
We validate requests using Pydantic models but do not validate responses.
Response structures are documented in comments for reference only.

Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs
"""

from enum import Enum
from typing import Any, Dict, TypeVar
from pydantic import BaseModel, ConfigDict


class BaseModelConfig(BaseModel):
    """Base model configuration for all models in the project.

    Provides common configuration settings for Pydantic models including:
    - populate_by_name: Allow populating models by alias name or field name
    - use_enum_values: Use string values from enums instead of enum objects
    - extra: Ignore extra fields in input data

    See:
        docs/models/base.md for reference
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra="ignore",
    )


class APIRequest(BaseModelConfig):
    """Base model for API requests.

    All API request models should inherit from this class to ensure
    consistent configuration and behavior. It inherits settings from
    BaseModelConfig.

    Note:
        This class provides the foundation for all API requests and inherits
        model configuration from BaseModelConfig.

    See:
        docs/models/base.md for reference
    """

    pass


# Common enums used across multiple modules
class ExecutionMode(str, Enum):
    """Execution mode options for workspaces and organizations.

    Defines how Terraform operations are executed:
    - REMOTE: Terraform runs on Terraform Cloud's infrastructure
    - LOCAL: Terraform runs on your local machine
    - AGENT: Terraform runs on your own infrastructure using an agent

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings#execution-mode

    See:
        docs/models/workspace.md for reference
    """

    REMOTE = "remote"
    LOCAL = "local"
    AGENT = "agent"


class CollaboratorAuthPolicy(str, Enum):
    """Authentication policy options for organization collaborators.

    Defines the authentication requirements for organization members:
    - PASSWORD: Password-only authentication is allowed
    - TWO_FACTOR_MANDATORY: Two-factor authentication is required for all users

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/users-teams-organizations/organizations#authentication

    See:
        docs/models/organization.md for reference
    """

    PASSWORD = "password"
    TWO_FACTOR_MANDATORY = "two_factor_mandatory"


# Response type for all API calls - just a dictionary with no validation
APIResponse = Dict[str, Any]


# Type variable for API requests to use with generics
ReqT = TypeVar("ReqT", bound=APIRequest)
