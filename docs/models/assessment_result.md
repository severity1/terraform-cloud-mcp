# Assessment Results Models

This document describes the Pydantic models used for validating input to the Assessment Results API.

## Overview

Assessment Results models provide validation for requests to Terraform Cloud's health assessment API endpoints. Health assessments automatically check whether deployed infrastructure matches the requirements defined in Terraform configurations.

## Models

### AssessmentResultStatus

```python
class AssessmentResultStatus(str, Enum):
    """Status options for assessment results in Terraform Cloud."""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    ERRORED = "errored"
    CANCELED = "canceled"
    FINISHED = "finished"
```

This enum defines the various states an assessment result can be in during its lifecycle:

- `PENDING`: Assessment has not yet started
- `QUEUED`: Assessment is queued for execution
- `RUNNING`: Assessment is currently running
- `ERRORED`: Assessment has encountered an error
- `CANCELED`: Assessment was canceled
- `FINISHED`: Assessment has completed successfully

### AssessmentResultRequest

```python
class AssessmentResultRequest(APIRequest):
    """Request model for retrieving assessment result details."""
    assessment_result_id: str = Field(
        ...,
        description="The ID of the assessment result to retrieve",
        pattern=r"^asmtres-[a-zA-Z0-9]{8,}$",
    )
```

This model validates the assessment result ID parameter for basic API requests:

- `assessment_result_id`: The ID of the assessment result to retrieve (format: "asmtres-xxxxxxxx")
  - Required field (no default value)
  - Must match the pattern of Terraform Cloud assessment result IDs
  - No alias needed as the field name matches the API parameter name

### AssessmentOutputRequest

```python
class AssessmentOutputRequest(AssessmentResultRequest):
    """Request model for retrieving assessment result outputs."""
    pass  # Uses the same validation as the parent class
```

This model extends `AssessmentResultRequest` to validate requests for specialized outputs:

- Used for JSON plan output requests
- Used for provider schema requests 
- Used for log output requests

## API Response Structure

While the responses are not validated with Pydantic models, they typically follow this structure:

```json
{
  "id": "asmtres-UG5rE9L1373hMYMA",
  "type": "assessment-results",
  "data": {
    "attributes": {
      "drifted": true,
      "succeeded": true,
      "error-msg": null,
      "created-at": "2022-07-02T22:29:58+00:00"
    },
    "links": {
      "self": "/api/v2/assessment-results/asmtres-UG5rE9L1373hMYMA/",
      "json-output": "/api/v2/assessment-results/asmtres-UG5rE9L1373hMYMA/json-output",
      "json-schema": "/api/v2/assessment-results/asmtres-UG5rE9L1373hMYMA/json-schema",
      "log-output": "/api/v2/assessment-results/asmtres-UG5rE9L1373hMYMA/log-output"
    }
  }
}
```

For specialized endpoint responses like JSON output, JSON schema, and log output, the response is provided in "content" field as raw text:

```json
{
  "content": "Raw output content here..."
}
```

## Reference 

For more detailed information, see:
- [Terraform Cloud API Documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/assessment-results)
- Tools implementation in `terraform_cloud_mcp/tools/assessment_results.py`