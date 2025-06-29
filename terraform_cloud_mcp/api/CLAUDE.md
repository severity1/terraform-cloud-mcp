# CLAUDE.md for api/

This file provides guidance about the Terraform Cloud API client implementation.

## API Client Architecture

The API client provides core functionality for Terraform Cloud API integration:
- **Authentication**: Terraform Cloud API token management
- **Request handling**: Formatting, submission, and response processing
- **Error management**: Consistent error handling across all API calls
- **Redirect handling**: Custom handling for Terraform Cloud pre-signed URLs

### Core Components
- **client.py**: `api_request()` main function and `handle_redirect()` for pre-signed URLs

## Implementation Standards

### Request Function Pattern
The `api_request()` function handles all API interactions with:
- **Path/Method**: API endpoint path and HTTP method (GET, POST, PATCH, DELETE)
- **Authentication**: Automatic token management via utils/env.py
- **Parameters**: Query parameters and request body handling
- **Response types**: JSON and text response processing

### Custom Redirect Management
Custom redirect handling (not httpx automatic) provides:
- **Authentication preservation**: Maintains auth headers through redirects
- **Content-type processing**: Handles pre-signed URL responses appropriately
- **Terraform Cloud compatibility**: Required for API pre-signed URL patterns

### Response Handling Standards
- **Success responses**: 200/201 return raw API data; 204 returns `{"status": "success", "status_code": 204}`
- **Error handling**: HTTP status errors, network issues, JSON parsing failures
- **Security**: Never logs tokens/credentials, validates inputs, proper error redaction

## Usage Standards

### Integration Requirements
- **Error handling**: Always use with `@handle_api_errors` decorator from utils/decorators.py
- **Environment management**: Token handling via `get_tfc_token()` from utils/env.py
- **Payload creation**: Convert Pydantic models using utils/payload.py utilities
- **Content downloads**: Set `accept_text=True` for redirect-based content retrieval

## Component Cross-References

### Related Component Guidance
- **Tool Implementation**: [../tools/CLAUDE.md](../tools/CLAUDE.md) for using API client in tool functions
- **Model Development**: [../models/CLAUDE.md](../models/CLAUDE.md) for request/response model patterns
- **Utility Functions**: [../utils/CLAUDE.md](../utils/CLAUDE.md) for payload creation and error handling
- **Documentation**: [../../docs/CLAUDE.md](../../docs/CLAUDE.md) for API documentation standards