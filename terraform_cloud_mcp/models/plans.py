"""Plan models for Terraform Cloud API

This module contains models for Terraform Cloud plan-related requests.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/plans
"""

from enum import Enum
from typing import Optional

from pydantic import Field

from .base import APIRequest


class PlanStatus(str, Enum):
    """Status options for plans in Terraform Cloud.

    Defines the various states a plan can be in during its lifecycle:
    - PENDING: Plan has not yet started
    - MANAGED_QUEUED/QUEUED: Plan is queued for execution
    - RUNNING: Plan is currently running
    - ERRORED: Plan has encountered an error
    - CANCELED: Plan was canceled
    - FINISHED: Plan has completed successfully
    - UNREACHABLE: Plan is in an unreachable state

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/plans

    See:
        docs/models/plan.md for reference
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
    """Model for plan execution details.

    Represents execution mode specific details for a plan, including agent
    information when running in agent execution mode.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/plans

    See:
        docs/models/plan.md for reference
    """

    agent_id: Optional[str] = Field(
        None,
        alias="agent-id",
        description="ID of the agent that ran the plan",
    )
    agent_name: Optional[str] = Field(
        None,
        alias="agent-name",
        description="Name of the agent that ran the plan",
    )
    agent_pool_id: Optional[str] = Field(
        None,
        alias="agent-pool-id",
        description="ID of the agent pool the plan ran in",
    )
    agent_pool_name: Optional[str] = Field(
        None,
        alias="agent-pool-name",
        description="Name of the agent pool the plan ran in",
    )
    # Additional execution mode details can be added here


class StatusTimestamps(APIRequest):
    """Model for plan execution timestamps.

    Captures the timestamps for various stages in a plan's lifecycle.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/plans

    See:
        docs/models/plan.md for reference
    """

    queued_at: Optional[str] = Field(
        None,
        alias="queued-at",
        description="When the plan was queued",
    )
    pending_at: Optional[str] = Field(
        None,
        alias="pending-at",
        description="When the plan entered pending state",
    )
    started_at: Optional[str] = Field(
        None,
        alias="started-at",
        description="When the plan execution started",
    )
    finished_at: Optional[str] = Field(
        None,
        alias="finished-at",
        description="When the plan execution completed",
    )


class PlanRequest(APIRequest):
    """Request model for retrieving a plan.

    Used to validate the plan ID parameter for API requests.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/plans#show-a-plan

    See:
        docs/models/plan.md for reference
    """

    plan_id: str = Field(
        ...,
        # No alias needed as field name matches API parameter
        description="The ID of the plan to retrieve",
        pattern=r"^plan-[a-zA-Z0-9]{16}$",  # Standard plan ID pattern
    )


class PlanJsonOutputRequest(APIRequest):
    """Request model for retrieving a plan's JSON output.

    Used to validate the plan ID parameter for JSON output API requests.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/plans#retrieve-the-json-execution-plan

    See:
        docs/models/plan.md for reference
    """

    plan_id: str = Field(
        ...,
        # No alias needed as field name matches API parameter
        description="The ID of the plan to retrieve JSON output for",
        pattern=r"^plan-[a-zA-Z0-9]{16}$",  # Standard plan ID pattern
    )


class RunPlanJsonOutputRequest(APIRequest):
    """Request model for retrieving a run's plan JSON output.

    Used to validate the run ID parameter for JSON output API requests.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/plans#retrieve-the-json-execution-plan-from-a-run

    See:
        docs/models/plan.md for reference
    """

    run_id: str = Field(
        ...,
        # No alias needed as field name matches API parameter
        description="The ID of the run to retrieve plan JSON output for",
        pattern=r"^run-[a-zA-Z0-9]{16}$",  # Standard run ID pattern
    )


# Response handling is implemented through raw dictionaries
