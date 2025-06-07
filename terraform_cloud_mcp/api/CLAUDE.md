# CLAUDE.md for api/

This file provides guidance about the API client implementation in this repository.

## API Client Overview

The API client module provides the core functionality for making requests to the Terraform Cloud API and handling responses. It's responsible for:

1. Authentication with Terraform Cloud
2. Request formatting and submission
3. Response handling and error management
4. Custom redirect handling for pre-signed URLs

## Key Components

- **client.py**: Core API client with error handling and redirect management
  - `api_request()`: Main function for all API calls
  - `handle_redirect()`: Custom redirect handling for Terraform Cloud pre-signed URLs

## API Request Pattern

```python
async def api_request(
    path: str,               # API path without leading slash
    method: str = "GET",     # HTTP method (GET, POST, PATCH, DELETE)
    token: Optional[str] = None,  # API token (defaults to TFC_TOKEN env var)
    params: Dict[str, Any] = {},  # Query parameters
    data: Union[Dict[str, Any], BaseModel] = {},  # Request body
    external_url: bool = False,   # Whether path is a complete URL
    accept_text: bool = False,    # Whether to accept text response
) -> Dict[str, Any]:         # Return API response or error information
```

## Custom Redirect Handling

The client implements custom redirect handling rather than using httpx's automatic redirect following because:
1. We need to preserve authentication headers when following redirects
2. We need content-type specific processing of redirect responses
3. Terraform Cloud API uses pre-signed URLs that require the original auth headers

## Error Handling

The API client handles several types of errors:
- HTTP status errors (400, 404, 500)
- Network/connection issues
- JSON parsing failures
- General exceptions

## Special Response Handling

- 204 No Content: Returns `{"status": "success", "status_code": 204}`
- Redirects: Uses custom handling to follow with authentication
- JSON Failures: When expecting text, returns the raw content

## Security Considerations

- Never logs tokens or credentials
- Validates inputs to prevent injection
- Uses proper authentication headers
- Implements proper error redaction

## Usage Guidelines

1. Always use with the `handle_api_errors` decorator from utils/decorators.py
2. For downloading content via redirects, set `accept_text=True`
3. Ensure proper error handling in the calling function
4. Use environment variables for token management
5. Convert Pydantic models to API payload using utils/payload.py