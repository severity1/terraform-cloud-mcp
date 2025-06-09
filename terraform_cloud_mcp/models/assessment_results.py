"""Assessment result models for Terraform Cloud API.

This module contains models for Terraform Cloud assessment result-related requests.
Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/assessment-results
"""

from enum import Enum
from typing import Optional

from pydantic import Field

from .base import APIRequest


class AssessmentResultStatus(str, Enum):
    """Status options for assessment results in Terraform Cloud.

    Defines the various states an assessment result can be in during its lifecycle:
    - PENDING: Assessment has not yet started
    - QUEUED: Assessment is queued for execution
    - RUNNING: Assessment is currently running
    - ERRORED: Assessment has encountered an error
    - CANCELED: Assessment was canceled
    - FINISHED: Assessment has completed successfully

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/assessment-results

    See:
        docs/models/assessment_result.md for reference
    """

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    ERRORED = "errored"
    CANCELED = "canceled"
    FINISHED = "finished"


class AssessmentResultRequest(APIRequest):
    """Request model for retrieving assessment result details.

    Used to validate the assessment result ID parameter for API requests.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/assessment-results#show-assessment-result

    See:
        docs/models/assessment_result.md for reference
    """

    assessment_result_id: str = Field(
        ...,
        # No alias needed as field name matches API parameter
        description="The ID of the assessment result to retrieve",
        pattern=r"^asmtres-[a-zA-Z0-9]{8,}$",  # Standard assessment result ID pattern
    )


class AssessmentOutputRequest(AssessmentResultRequest):
    """Request model for retrieving assessment result outputs.

    Extends the base AssessmentResultRequest for specialized outputs like
    JSON plan, schema, and log output.

    Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/assessment-results#retrieve-the-json-output-from-the-assessment-execution

    See:
        docs/models/assessment_result.md for reference
    """

    pass  # Uses the same validation as the parent class


# Response handling is implemented through raw dictionaries