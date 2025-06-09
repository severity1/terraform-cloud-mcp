"""Terraform Cloud assessment results management tools.

This module provides tools for working with health assessment results in Terraform Cloud.
It includes functions to retrieve assessment details, JSON output, schema files, and logs.

Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/assessment-results
"""

from ..api.client import api_request
from ..models.base import APIResponse
from ..models.assessment_results import AssessmentResultRequest, AssessmentOutputRequest
from ..utils.decorators import handle_api_errors


@handle_api_errors
async def get_assessment_result_details(assessment_result_id: str) -> APIResponse:
    """Get details for a specific assessment result.

    Retrieves comprehensive information about an assessment result including its current status,
    whether drift was detected, and links to related resources like JSON output and logs.

    API endpoint: GET /api/v2/assessment-results/{assessment_result_id}

    Args:
        assessment_result_id: The ID of the assessment result to retrieve details for (format: "asmtres-xxxxxxxx")

    Returns:
        Assessment result details including status, timestamps, and drift detection information

    See:
        docs/tools/assessment_results.md for reference documentation
    """
    # Validate parameters
    params = AssessmentResultRequest(assessment_result_id=assessment_result_id)

    # Make API request
    return await api_request(f"assessment-results/{params.assessment_result_id}")


@handle_api_errors
async def get_assessment_json_output(assessment_result_id: str) -> APIResponse:
    """Retrieve the JSON execution plan from an assessment result.

    Gets the JSON representation of the plan execution details from an assessment,
    providing a machine-readable format of the planned resource changes.

    API endpoint: GET /api/v2/assessment-results/{assessment_result_id}/json-output

    Args:
        assessment_result_id: The ID of the assessment result to retrieve JSON output for (format: "asmtres-xxxxxxxx")

    Returns:
        The complete JSON formatted plan with resource changes, metadata,
        and planned actions. The redirect is automatically followed.

    Note:
        This endpoint requires admin level access to the workspace and cannot be accessed
        with organization tokens.

    See:
        docs/tools/assessment_results.md for reference documentation
    """
    # Validate parameters
    params = AssessmentOutputRequest(assessment_result_id=assessment_result_id)

    # Make API request with text acceptance since it may be a large JSON file
    return await api_request(
        f"assessment-results/{params.assessment_result_id}/json-output",
        accept_text=True
    )


@handle_api_errors
async def get_assessment_json_schema(assessment_result_id: str) -> APIResponse:
    """Retrieve the JSON schema file from an assessment result.

    Gets the JSON schema representation of the provider schema used during the assessment,
    providing information about available resources and their configuration options.

    API endpoint: GET /api/v2/assessment-results/{assessment_result_id}/json-schema

    Args:
        assessment_result_id: The ID of the assessment result to retrieve schema for (format: "asmtres-xxxxxxxx")

    Returns:
        The JSON schema file containing provider information. The redirect is automatically followed.

    Note:
        This endpoint requires admin level access to the workspace and cannot be accessed
        with organization tokens.

    See:
        docs/tools/assessment_results.md for reference documentation
    """
    # Validate parameters
    params = AssessmentOutputRequest(assessment_result_id=assessment_result_id)

    # Make API request with text acceptance since it may be a large JSON file
    return await api_request(
        f"assessment-results/{params.assessment_result_id}/json-schema",
        accept_text=True
    )


@handle_api_errors
async def get_assessment_log_output(assessment_result_id: str) -> APIResponse:
    """Retrieve logs from an assessment result.

    Gets the raw log output from a Terraform Cloud assessment operation,
    providing detailed information about the execution and any errors.

    API endpoint: GET /api/v2/assessment-results/{assessment_result_id}/log-output

    Args:
        assessment_result_id: The ID of the assessment result to retrieve logs for (format: "asmtres-xxxxxxxx")

    Returns:
        The raw logs from the assessment operation. The redirect to the log file
        is automatically followed.

    Note:
        This endpoint requires admin level access to the workspace and cannot be accessed
        with organization tokens.

    See:
        docs/tools/assessment_results.md for reference documentation
    """
    # Validate parameters
    params = AssessmentOutputRequest(assessment_result_id=assessment_result_id)

    # Make API request with text acceptance for the logs
    return await api_request(
        f"assessment-results/{params.assessment_result_id}/log-output",
        accept_text=True
    )