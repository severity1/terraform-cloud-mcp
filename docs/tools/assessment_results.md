# Assessment Results API Tools

This document describes the tools for interacting with Terraform Cloud Health Assessment Results.
Health assessments automatically verify that real infrastructure matches the requirements defined in Terraform configurations.

## Overview

Health assessments provide automated drift detection and continuous validation for Terraform Cloud workspaces.
The assessment results API allows you to retrieve assessment details, plans, schemas, and logs.

> **Note**: Health assessments are a premium feature available in HCP Terraform Plus and Premium editions.

## Available Tools

| Tool Name | Description |
|-----------|-------------|
| `get_assessment_result_details` | Retrieve basic information about an assessment result |
| `get_assessment_json_output` | Get the JSON plan from an assessment |
| `get_assessment_json_schema` | Get the provider schema from an assessment |
| `get_assessment_log_output` | Get logs from an assessment run |

## Tool Usage

### Get Assessment Result Details

Retrieves information about a specific health assessment result, including status and drift detection.

```python
get_assessment_result_details(assessment_result_id="asmtres-XXXXXXXXXX")
```

#### Parameters

- `assessment_result_id`: The ID of the assessment result (format: "asmtres-XXXXXXXXXX")

#### Response Example

```json
{
  "id": "asmtres-UG5rE9L1373hMYMA",
  "type": "assessment-results",
  "data": {
    "attributes": {
      "drifted": true,
      "succeeded": true,
      "error-msg": null,
      "created-at": "2022-07-02T22:29:58+00:00",
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

### Get Assessment JSON Output

Retrieves the JSON plan output from an assessment result.

```python
get_assessment_json_output(assessment_result_id="asmtres-XXXXXXXXXX")
```

#### Parameters

- `assessment_result_id`: The ID of the assessment result (format: "asmtres-XXXXXXXXXX")

#### Response Example

```json
{
  "content": "{\n  \"format_version\": \"1.0\",\n  \"terraform_version\": \"1.3.0\",\n  \"planned_values\": { ... },\n  \"resource_changes\": [ ... ],\n  \"configuration\": { ... }\n}"
}
```

### Get Assessment JSON Schema

Retrieves the provider schema from an assessment result.

```python
get_assessment_json_schema(assessment_result_id="asmtres-XXXXXXXXXX")
```

#### Parameters

- `assessment_result_id`: The ID of the assessment result (format: "asmtres-XXXXXXXXXX")

#### Response Example

```json
{
  "content": "{\n  \"format_version\": \"1.0\",\n  \"provider_schemas\": { ... }\n}"
}
```

### Get Assessment Log Output

Retrieves the logs from an assessment run.

```python
get_assessment_log_output(assessment_result_id="asmtres-XXXXXXXXXX")
```

#### Parameters

- `assessment_result_id`: The ID of the assessment result (format: "asmtres-XXXXXXXXXX")

#### Response Example

```json
{
  "content": "Terraform initiated...\nGathering resources...\nDetecting drift...\n"
}
```

## Authentication Requirements

The assessment results endpoints have specific authentication requirements:

- `get_assessment_result_details`: Accessible to users with read access to a workspace
- All other endpoints (`json-output`, `json-schema`, `log-output`): Require admin level access and cannot be accessed with organization tokens. You must use a user token or team token with admin access.

## Reference

For more detailed information, see the [official Terraform Cloud API documentation](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/assessment-results).