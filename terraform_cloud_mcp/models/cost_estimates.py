"""Cost estimate models for Terraform Cloud API

This module contains models for Terraform Cloud cost estimate-related requests.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/cost-estimates
"""

from enum import Enum
from typing import Optional

from pydantic import Field

from .base import APIRequest


class CostEstimateStatus(str, Enum):
    """Status options for cost estimates in Terraform Cloud.

    Defines the various states a cost estimate can be in during its lifecycle:
    - PENDING: Cost estimate has not yet started
    - QUEUED: Cost estimate is queued for execution
    - RUNNING: Cost estimate is currently running
    - ERRORED: Cost estimate has encountered an error
    - CANCELED: Cost estimate was canceled
    - FINISHED: Cost estimate has completed successfully
    - UNREACHABLE: Cost estimate is in an unreachable state

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/cost-estimates

    See:
        docs/models/cost_estimate.md for reference
    """

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    ERRORED = "errored"
    CANCELED = "canceled"
    FINISHED = "finished"
    UNREACHABLE = "unreachable"


class StatusTimestamps(APIRequest):
    """Model for cost estimate execution timestamps.

    Captures the timestamps for various stages in a cost estimate's lifecycle.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/cost-estimates

    See:
        docs/models/cost_estimate.md for reference
    """

    queued_at: Optional[str] = Field(
        None,
        alias="queued-at",
        description="When the cost estimate was queued",
    )
    finished_at: Optional[str] = Field(
        None,
        alias="finished-at",
        description="When the cost estimate execution completed",
    )


class CostEstimateRequest(APIRequest):
    """Request model for retrieving a cost estimate.

    Used to validate the cost estimate ID parameter for API requests.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/cost-estimates#show-a-cost-estimate

    See:
        docs/models/cost_estimate.md for reference
    """

    cost_estimate_id: str = Field(
        ...,
        # No alias needed as field name matches API parameter
        description="The ID of the cost estimate to retrieve",
        pattern=r"^ce-[a-zA-Z0-9]{16}$",  # Standard cost estimate ID pattern
    )


# Response handling is implemented through raw dictionaries
