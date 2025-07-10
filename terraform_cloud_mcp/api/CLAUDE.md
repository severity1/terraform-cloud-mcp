# CLAUDE.md for api/

This file provides guidance about the Terraform Cloud API client implementation.

## Context Activation
This guidance activates when:
- Working in `terraform_cloud_mcp/api/` directory
- Creating/editing API client files (*.py)
- Implementing HTTP request handling or authentication
- Adding redirect management or response processing

**Companion directories**: tools/ (for usage), models/ (for requests), utils/ (for helpers)

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
- **Response filtering**: Automatic filtering applied to GET requests returning JSON data
- **Error handling**: HTTP status errors, network issues, JSON parsing failures  
- **Security**: Never logs tokens/credentials, validates inputs, proper error redaction

## Usage Standards

### Integration Requirements
- **Error handling**: Always use with `@handle_api_errors` decorator from utils/decorators.py
- **Environment management**: Token handling via `get_tfc_token()` from utils/env.py
- **Payload creation**: Convert Pydantic models using utils/payload.py utilities
- **Content downloads**: Set `accept_text=True` for redirect-based content retrieval

## Development Standards

### Quality Checks
- **Format**: `ruff format .`
- **Lint**: `ruff check .`
- **Type Check**: `mypy .`
- **Test**: `pytest`

### API Client Requirements
- All functions must include proper error handling and consistent response format
- Apply security guidelines for token and credential management
- Follow established patterns for request formatting and response processing
- Test with comprehensive coverage of success, error, and edge cases

### Integration Guidelines

### Tool Integration
When API client is used in tools:
- Always use with `@handle_api_errors` decorator
- Apply proper payload creation using utility functions
- Handle redirects appropriately for content downloads
- Use centralized token management

### Model Integration
When API client works with models:
- Convert Pydantic models using payload utilities
- Apply proper request validation before API calls
- Handle model validation errors appropriately
- Ensure proper type safety throughout request pipeline

### Utility Integration
When API client works with utilities:
- Use environment management for token handling
- Apply payload creation utilities for JSON:API compliance
- Use error handling decorators consistently
- Apply security practices for sensitive data

## Implementation Workflow

### API Client Enhancement Process
1. **Define request patterns**: Follow established function signatures
2. **Implement authentication**: Use centralized token management
3. **Add error handling**: Apply consistent response formats
4. **Handle redirects**: Use custom redirect management where needed
5. **Test thoroughly**: Cover success, error, network, and redirect scenarios
6. **Update documentation**: Implementation status tracking

### Quality Validation Checklist
For each API client enhancement:
- [ ] Function includes proper authentication and error handling
- [ ] Custom redirect handling applied where needed for TFC pre-signed URLs
- [ ] Security guidelines followed for token and credential management
- [ ] Quality checks passed: format, lint, type check
- [ ] Tests cover all scenarios: success, error, network issues, redirects
- [ ] Documentation updated: implementation status tracking