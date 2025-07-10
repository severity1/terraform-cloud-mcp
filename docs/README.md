# Terraform Cloud MCP Documentation

This directory contains supplementary documentation for the Terraform Cloud MCP project.

## Structure

### Core Documentation
- `FILTERING_SYSTEM.md` - Audit-safe response filtering system (5-15% token reduction, 100% audit compliance)
- `DEVELOPMENT.md` - Comprehensive development guidelines and coding standards
- `API_REFERENCES.md` - Terraform Cloud API documentation links with implementation status
- `CONTRIBUTING.md` - Guidelines for contributing to the project

### Model Documentation
The `models/` directory contains documentation for each model type:
- `account.md` - Account model documentation
- `apply.md` - Apply model documentation
- `assessment_result.md` - Assessment result model documentation
- `cost_estimate.md` - Cost estimate model documentation
- `organization.md` - Organization model documentation  
- `plan.md` - Plan model documentation
- `project.md` - Project model documentation
- `run.md` - Run model documentation
- `state_versions.md` - State version model documentation
- `state_version_outputs.md` - State version outputs model documentation
- `variables.md` - Variables and variable sets model documentation
- `workspace.md` - Workspace model documentation

### Tool Documentation
The `tools/` directory contains reference documentation for each tool:
- `account.md` - Account tool reference documentation
- `apply.md` - Apply management tool reference documentation
- `assessment_results.md` - Assessment results tool reference documentation
- `cost_estimate.md` - Cost estimate tools reference documentation
- `organization.md` - Organization tools reference documentation
- `plan.md` - Plan management tool reference documentation
- `project.md` - Project management tool reference documentation
- `run.md` - Run tools reference documentation
- `state_versions.md` - State version management tool reference documentation
- `state_version_outputs.md` - State version outputs tool reference documentation
- `variables.md` - Variables and variable sets tool reference documentation
- `workspace.md` - Workspace tools reference documentation

### Conversation Examples
The `conversations/` directory contains example conversations and usage scenarios:
- `account.md` - Account management conversation examples
- `apply-management-conversation.md` - Apply management conversation examples
- `assessment-results-conversation.md` - Assessment results conversation examples
- `cost-estimate-conversation.md` - Cost estimation conversation examples
- `organization-entitlements-conversation.md` - Organization entitlements conversation examples
- `organizations-management-conversation.md` - Organization management conversation examples
- `plan-management-conversation.md` - Plan management conversation examples
- `project-management-conversation.md` - Project management conversation examples
- `runs-management-conversation.md` - Run management conversation examples
- `state_management.md` - State management conversation examples
- `variables-conversation.md` - Variables management conversation examples
- `workspace-management-conversation.md` - Workspace management conversation examples

## Documentation Philosophy
1. Code docstrings contain essential information about purpose, fields, parameters, and return values
2. Tool documentation provides context, API references, and usage guidance
3. Model examples illustrate how to work with data structures
4. Development standards and patterns are consolidated in DEVELOPMENT.md
5. Conversation examples demonstrate practical application scenarios
6. This structure keeps the codebase clean while maintaining comprehensive documentation