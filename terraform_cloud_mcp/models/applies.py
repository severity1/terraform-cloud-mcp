"""Apply models for Terraform Cloud API

This module contains models for Terraform Cloud apply-related requests.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies
"""

from enum import Enum
from typing import Optional

from pydantic import Field

from .base import APIRequest


class ApplyStatus(str, Enum):
    """Status options for applies in Terraform Cloud.

    Defines the various states an apply can be in during its lifecycle:
    - PENDING: Apply has not yet started
    - MANAGED_QUEUED/QUEUED: Apply is queued for execution
    - RUNNING: Apply is currently running
    - ERRORED: Apply has encountered an error
    - CANCELED: Apply was canceled
    - FINISHED: Apply has completed successfully
    - UNREACHABLE: Apply is in an unreachable state

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies

    See:
        docs/models/apply.md for reference
    """

    PENDING = "pending"
    MANAGED_QUEUED = "managed_queued"
    QUEUED = "queued"
    RUNNING = "running"
    ERRORED = "errored"
    CANCELED = "canceled"
    FINISHED = "finished"
    UNREACHABLE = "unreachable"


class ExecutionDetails(APIRequest):
    """Model for apply execution details.

    Represents execution mode specific details for an apply, including agent
    information when running in agent execution mode.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies

    See:
        docs/models/apply.md for reference
    """

    agent_id: Optional[str] = Field(
        None,
        alias="agent-id",
        description="ID of the agent that ran the apply",
    )
    agent_name: Optional[str] = Field(
        None,
        alias="agent-name",
        description="Name of the agent that ran the apply",
    )
    agent_pool_id: Optional[str] = Field(
        None,
        alias="agent-pool-id",
        description="ID of the agent pool the apply ran in",
    )
    agent_pool_name: Optional[str] = Field(
        None,
        alias="agent-pool-name",
        description="Name of the agent pool the apply ran in",
    )
    # Additional execution mode details can be added here


class StatusTimestamps(APIRequest):
    """Model for apply execution timestamps.

    Captures the timestamps for various stages in an apply's lifecycle.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies

    See:
        docs/models/apply.md for reference
    """

    queued_at: Optional[str] = Field(
        None,
        alias="queued-at",
        description="When the apply was queued",
    )
    pending_at: Optional[str] = Field(
        None,
        alias="pending-at",
        description="When the apply entered pending state",
    )
    started_at: Optional[str] = Field(
        None,
        alias="started-at",
        description="When the apply execution started",
    )
    finished_at: Optional[str] = Field(
        None,
        alias="finished-at",
        description="When the apply execution completed",
    )


class ApplyRequest(APIRequest):
    """Request model for retrieving an apply.

    Used to validate the apply ID parameter for API requests.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies#show-an-apply

    See:
        docs/models/apply.md for reference
    """

    apply_id: str = Field(
        ...,
        # No alias needed as field name matches API parameter
        description="The ID of the apply to retrieve",
        pattern=r"^apply-[a-zA-Z0-9]{16}$",  # Standard apply ID pattern
    )


class ApplyErroredStateRequest(APIRequest):
    """Request model for retrieving an apply's errored state.

    Used to validate the apply ID parameter for errored state API requests.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies#recover-a-failed-state-upload-after-applying

    See:
        docs/models/apply.md for reference
    """

    apply_id: str = Field(
        ...,
        # No alias needed as field name matches API parameter
        description="The ID of the apply with a failed state upload",
        pattern=r"^apply-[a-zA-Z0-9]{16}$",  # Standard apply ID pattern
    )


# Response handling is implemented through raw dictionaries
