"""Base models for Terraform Cloud MCP.

This module defines base models for Terraform Cloud API requests.
We validate requests using Pydantic models but do not validate responses.
Response structures are documented in comments for reference only.
"""

from typing import Any, Dict, TypeVar
from pydantic import BaseModel, ConfigDict


class BaseModelConfig(BaseModel):
    """Base model configuration for all models in the project."""

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra="ignore",
    )


class APIRequest(BaseModelConfig):
    """Base model for API requests"""

    pass


# Response type for all API calls - just a dictionary with no validation
APIResponse = Dict[str, Any]


# Type variable for API requests to use with generics
ReqT = TypeVar("ReqT", bound=APIRequest)
