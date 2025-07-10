# CLAUDE.md for configs/

This file provides guidance about configuration management for the Terraform Cloud MCP implementation.

## Context Activation
This guidance activates when:
- Working in `terraform_cloud_mcp/configs/` directory
- Creating/editing configuration files (*.py)
- Implementing configuration-driven functionality
- Adding new resource type configurations

**Companion directories**: utils/ (for usage), models/ (for validation)

## Configuration Architecture

The configs directory provides centralized configuration data to maintain consistency and enable easy maintenance:

### Core Configurations
- **filter_configs.py**: Response filtering configurations for token optimization

## Filter Configuration Standards

### Resource Type Configurations
When adding new resource types, add filter configurations to `FILTER_CONFIGS`:
- **always_remove**: Fields always filtered regardless of operation type
- **read_remove**: Fields filtered only for READ operations (detailed views)
- **list_remove**: Fields filtered only for LIST operations (pagination views)
- **essential_relationships**: Relationships to preserve (optional)

### Detection Pattern Standards
Update detection patterns when adding new API endpoints:
- **PATH_PATTERNS**: Add new path patterns in specificity order (most specific first)
- **DATA_TYPE_MAP**: Add fallback mappings for response data type detection
- **RESOURCE_TYPE_MAP**: Add string-to-enum conversions for new resource types

### Configuration Maintenance
When implementing new tools or API endpoints:
- **Review API responses**: Check for verbose/unnecessary fields that impact token usage
- **Test filtering effectiveness**: Ensure essential operational data is preserved
- **Update configurations**: Add new resource types or modify existing filter rules
- **Validate detection**: Ensure new endpoints are correctly detected and mapped

### MCP Context Preservation Requirements
As an MCP server for Terraform Cloud, filter configurations must preserve essential context:
- **Never filter essential fields**: Resource IDs, names, status, operational URLs, permissions
- **Preserve operational context**: Status information, timing data, progress indicators
- **Maintain relationships**: Resource connections and hierarchical data
- **Keep user-relevant data**: Configuration settings, decision support information
- **Conservative READ filtering**: Detailed views need comprehensive context
- **Selective LIST filtering**: Lists can be more aggressively filtered for identification

## Implementation Guidelines

### New Resource Type Process
1. **Add to models**: Define `ResourceType` enum value in `models/filters.py`
2. **Create filter config**: Add `FilterConfig` entry in `FILTER_CONFIGS` 
3. **Update detection**: Add path patterns and type mappings as needed
4. **Test filtering**: Verify correct resource detection and appropriate filtering

### Configuration Quality Standards
- **Specificity ordering**: More specific patterns before general ones in `PATH_PATTERNS`
- **Conservative filtering**: Only remove fields that don't impact functionality
- **Documentation**: Document reasoning for field removal decisions
- **Testing**: Validate filter effectiveness after configuration changes

### Maintenance Triggers
Update configurations when:
- **New API endpoints**: Add detection patterns and filter rules
- **API response changes**: Review existing filter configurations
- **Token usage optimization**: Identify new fields for filtering
- **Performance issues**: Optimize filter configurations for better efficiency