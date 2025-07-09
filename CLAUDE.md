# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Terraform Cloud MCP Development Guide

## Component Architecture

This project uses a hierarchical guidance system through component-specific CLAUDE.md files:

- **[docs/CLAUDE.md](docs/CLAUDE.md)** - Documentation standards and templates
- **[terraform_cloud_mcp/tools/CLAUDE.md](terraform_cloud_mcp/tools/CLAUDE.md)** - MCP tools implementation patterns
- **[terraform_cloud_mcp/models/CLAUDE.md](terraform_cloud_mcp/models/CLAUDE.md)** - Pydantic models and validation
- **[terraform_cloud_mcp/utils/CLAUDE.md](terraform_cloud_mcp/utils/CLAUDE.md)** - Utility functions and error handling
- **[terraform_cloud_mcp/api/CLAUDE.md](terraform_cloud_mcp/api/CLAUDE.md)** - API client patterns

## Core Principles

**Decision-Making**: Always use documented criteria from component CLAUDE.md files - never base decisions on code inference alone.

**Subagent Usage**: Use 2-6 subagents for complex tasks with specific roles:
- **Researcher**: Pattern analysis and documentation research
- **Architect**: System design and feature planning  
- **Implementer**: Code development and integration
- **Tester/Reviewer**: Quality assurance and validation

## Role-Based Guidance

### Researcher Tasks
Consult these components for analysis work:
- [terraform_cloud_mcp/tools/CLAUDE.md](terraform_cloud_mcp/tools/CLAUDE.md) for domain boundary analysis
- [terraform_cloud_mcp/models/CLAUDE.md](terraform_cloud_mcp/models/CLAUDE.md) for existing patterns
- [docs/CLAUDE.md](docs/CLAUDE.md) for documentation standards

### Architect Tasks  
Consult these components for design work:
- [terraform_cloud_mcp/tools/CLAUDE.md](terraform_cloud_mcp/tools/CLAUDE.md) for function signatures
- [terraform_cloud_mcp/models/CLAUDE.md](terraform_cloud_mcp/models/CLAUDE.md) for model hierarchies
- [terraform_cloud_mcp/utils/CLAUDE.md](terraform_cloud_mcp/utils/CLAUDE.md) for utility integration

### Implementer Tasks
Use all component CLAUDE.md files following the implementation workflow below.

## Implementation Workflow

### Tool Development Process
1. **Planning**: Consult component CLAUDE.md files per role guidance above
2. **Models**: Follow [terraform_cloud_mcp/models/CLAUDE.md](terraform_cloud_mcp/models/CLAUDE.md)
3. **Implementation**: Follow [terraform_cloud_mcp/tools/CLAUDE.md](terraform_cloud_mcp/tools/CLAUDE.md)
4. **Documentation**: Follow [docs/CLAUDE.md](docs/CLAUDE.md)
5. **Quality**: Apply standards from component CLAUDE.md files

### Development Standards
Component CLAUDE.md files provide comprehensive guidance for:
- **Build Commands & Quality Checks**: Development setup and validation
- **Implementation Patterns**: Code style, error handling, and conventions  
- **Documentation Templates**: Multi-layer documentation requirements

## Subagent Quick Reference

### Task Startup Checklist
1. **Identify role**: Researcher, Architect, or Implementer
2. **Consult components**: Use Role-Based Guidance above to find relevant CLAUDE.md files
3. **Apply criteria**: Use documented patterns, not code inference
4. **Validate patterns**: Reference existing code only to confirm documented guidance

## Task Management

### Complexity Assessment
- **Simple** (< 2 hours): Direct implementation, minimal planning
- **Medium** (2-8 hours): Use TodoWrite for 3-5 tasks  
- **Complex** (> 8 hours): Use subagents (2-6) with comprehensive TodoWrite planning

### TodoWrite Requirements
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