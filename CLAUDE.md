# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Terraform Cloud MCP Development Guide

## Subtree Discovery System

This project uses Claude Code's automatic subtree discovery for context-aware guidance. Component-specific CLAUDE.md files are automatically loaded when working in their directories:

- **docs/** - Documentation standards and templates
- **terraform_cloud_mcp/tools/** - MCP tools implementation patterns  
- **terraform_cloud_mcp/models/** - Pydantic models and validation
- **terraform_cloud_mcp/utils/** - Utility functions and error handling
- **terraform_cloud_mcp/api/** - API client patterns

## Working Directory Guidance

### When Working on Tool Implementation
- **Directory**: `terraform_cloud_mcp/tools/`
- **Context**: Automatic loading of tools-specific patterns
- **Focus**: MCP function signatures, error handling, API integration

### When Working on Data Models
- **Directory**: `terraform_cloud_mcp/models/`
- **Context**: Automatic loading of model validation patterns
- **Focus**: Pydantic models, validation rules, type definitions

### When Working on Utilities
- **Directory**: `terraform_cloud_mcp/utils/`
- **Context**: Automatic loading of utility function patterns
- **Focus**: Error handling, API helpers, common operations

### When Working on API Client
- **Directory**: `terraform_cloud_mcp/api/`
- **Context**: Automatic loading of API client patterns
- **Focus**: HTTP client, authentication, request handling

### When Working on Documentation
- **Directory**: `docs/`
- **Context**: Automatic loading of documentation standards
- **Focus**: Templates, formatting, structure requirements

## Development Commands

### Quality Checks
- **Format**: `ruff format .`
- **Lint**: `ruff check .`
- **Type Check**: `mypy .`
- **Test**: `pytest`

### Build Commands
- **Install**: `uv pip install -e .`
- **Dev Install**: `uv pip install -e .[dev]`
- **Requirements**: `uv pip compile requirements.in`

## Core Principles

### Decision-Making Process
1. **Use component guidance**: Let subtree discovery load relevant context
2. **Apply documented patterns**: Follow loaded component standards
3. **Avoid code inference**: Use documented criteria only
4. **Validate against patterns**: Check implementation against guidance

### Task Complexity Assessment
- **Simple** (< 2 hours): Direct implementation, minimal planning
- **Medium** (2-8 hours): Use TodoWrite for 3-5 tasks
- **Complex** (> 8 hours): Use subagents (2-6) with comprehensive TodoWrite planning

## Documentation Standards

### Required Documentation Updates
For any new implementation, always update:
- **TASKS.md**: Move features from planned to completed status
- **docs/API_REFERENCES.md**: Mark corresponding API sections as implemented  
- **docs/DEVELOPMENT.md**: Add new patterns if applicable
- **docs/CONTRIBUTING.md**: Update contribution guidelines if new patterns introduced

### Implementation Standards  
- **Use utility functions**: `create_api_payload()`, `query_params()`, `@handle_api_errors`
- **Apply response filtering**: Automatic filtering system in `utils/filters.py` handles all GET requests
- **Follow component patterns**: Apply standards from automatically loaded component CLAUDE.md files
- **Run quality checks**: Format, lint, type check before completion
- **Update relevant documentation**: Maintain consistency across project

### Response Filtering Implementation Context
This MCP server implements audit-safe response filtering with the following constraints:
- **Primary use case**: Audit and compliance scenarios requiring complete data integrity
- **Filtering approach**: Conservative token optimization (5-15% reduction) to preserve audit trails
- **Critical preservation requirements**: 
  - User accountability data (`created-at`, `updated-at`, `version-id`)
  - Security configuration (permissions, auth policies)
  - Change tracking (status timestamps, source information)
  - Operational context (status, timing, progress indicators)
- **Decision principle**: Preserve fields when audit impact is uncertain
- **Implementation location**: `utils/filters.py` with configurations in `configs/filter_configs.py`

## Task Management

### TodoWrite Usage
Use TodoWrite for tasks with:
- Multiple distinct steps (> 2)
- Multiple file changes
- Cross-component coordination
- Medium to complex scope

### Progress Standards  
- Mark todos `in_progress` before starting
- Mark `completed` immediately after finishing
- Update status in real-time
- Provide concise progress updates for major phases

## Memory System Maintenance

### Periodic Review Schedule
- **Monthly**: Review component CLAUDE.md files for outdated patterns
- **After major features**: Update decision matrices and workflow patterns
- **When adding new domains**: Verify subtree discovery optimization
- **Quality check failures**: Review and update development standards

### Maintenance Triggers
- **New implementation patterns**: Update relevant component guidance
- **API changes**: Review model and tool implementation standards  
- **Development workflow changes**: Update quality check commands
- **Documentation structure changes**: Update docs/ guidance
- **Filter configuration changes**: When new API fields appear, assess preservation vs. optimization trade-offs
- **Compliance requirement changes**: Review filter configurations if audit use cases evolve

### Memory Optimization Indicators
- **High context usage**: Review for redundant information across files
- **Frequent cross-referencing**: Consider consolidating related guidance
- **Outdated patterns**: Remove deprecated implementation approaches
- **Missing decision criteria**: Add decision matrices for common scenarios