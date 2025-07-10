"""Filter models for Terraform Cloud MCP.

This module defines Pydantic models and enums for API response filtering,
providing type-safe configuration and validation for filter operations.

Reference: https://developer.hashicorp.com/terraform/cloud-docs/api-docs
"""

from typing import Set, Optional
from pydantic import Field, field_validator
from enum import Enum

from .base import BaseModelConfig


class OperationType(str, Enum):
    """Operation types for API filtering.

    Defines the type of API operation being performed, which affects
    how responses are filtered:
    - READ: Single resource retrieval operations
    - LIST: Multiple resource listing operations
    - MANAGE: Create, update, delete operations

    See:
        docs/models/filters.md for reference
    """

    READ = "read"
    LIST = "list"
    MANAGE = "manage"


class ResourceType(str, Enum):
    """Known resource types for filtering.

    Defines the Terraform Cloud resource types that have specific
    filtering configurations. Each type has tailored field removal
    rules optimized for token efficiency.

    See:
        docs/models/filters.md for reference
    """

    WORKSPACE = "workspace"
    RUN = "run"
    ORGANIZATION = "organization"
    PROJECT = "project"
    VARIABLE = "variable"
    PLAN = "plan"
    APPLY = "apply"
    STATE_VERSION = "state-version"
    COST_ESTIMATE = "cost-estimate"
    ASSESSMENT = "assessment"
    ACCOUNT = "account"
    GENERIC = "generic"


class FilterConfig(BaseModelConfig):
    """Configuration for filtering a specific resource type.

    Defines which fields should be removed from API responses for different
    operation types to reduce token usage while preserving essential data.

    Attributes:
        always_remove: Fields to always remove regardless of operation type
        read_remove: Additional fields to remove for read operations
        list_remove: Additional fields to remove for list operations
        essential_relationships: Essential relationships to keep for read operations

    Example:
        config = FilterConfig(
            always_remove={"permissions", "actions"},
            list_remove={"created-at", "updated-at"},
            essential_relationships={"organization", "project"}
        )

    See:
        docs/models/filters.md for reference
    """

    always_remove: Set[str] = Field(
        default_factory=set,
        description="Fields to always remove regardless of operation type",
    )
    read_remove: Set[str] = Field(
        default_factory=set,
        description="Additional fields to remove for read operations",
    )
    list_remove: Set[str] = Field(
        default_factory=set,
        description="Additional fields to remove for list operations",
    )
    essential_relationships: Optional[Set[str]] = Field(
        default=None, description="Essential relationships to keep for read operations"
    )

    @field_validator("always_remove", "read_remove", "list_remove")
    @classmethod
    def validate_field_names(cls, v: Set[str]) -> Set[str]:
        """Validate that field names are non-empty strings.

        Args:
            v: Set of field names to validate

        Returns:
            Validated set of field names

        Raises:
            ValueError: If any field names are empty or not strings
        """
        if not v:
            return v

        invalid_fields = {
            field
            for field in v
            if not field or not isinstance(field, str) or not field.strip()
        }
        if invalid_fields:
            raise ValueError(f"Field names must be non-empty strings: {invalid_fields}")

        return v

    @field_validator("essential_relationships")
    @classmethod
    def validate_essential_relationships(
        cls, v: Optional[Set[str]]
    ) -> Optional[Set[str]]:
        """Validate essential relationships if provided.

        Args:
            v: Set of relationship names to validate

        Returns:
            Validated set of relationship names

        Raises:
            ValueError: If any relationship names are empty or not strings
        """
        if v is None:
            return v

        invalid_rels = {
            rel for rel in v if not rel or not isinstance(rel, str) or not rel.strip()
        }
        if invalid_rels:
            raise ValueError(
                f"Relationship names must be non-empty strings: {invalid_rels}"
            )

        return v


class FilterRequest(BaseModelConfig):
    """Request parameters for filtering operations.

    Provides a structured way to specify filtering parameters for API responses,
    including resource type, operation type, and custom field specifications.

    Attributes:
        resource_type: Type of resource being filtered
        operation_type: Type of operation being performed
        custom_fields: Optional custom fields to remove beyond default configuration
        preserve_fields: Optional fields to preserve even if normally filtered

    Example:
        request = FilterRequest(
            resource_type=ResourceType.WORKSPACE,
            operation_type=OperationType.LIST,
            custom_fields={"debug-info", "verbose-logs"}
        )

    See:
        docs/models/filters.md for reference
    """

    resource_type: ResourceType = Field(description="Type of resource being filtered")
    operation_type: OperationType = Field(
        default=OperationType.READ, description="Type of operation being performed"
    )
    custom_fields: Optional[Set[str]] = Field(
        default=None,
        description="Optional custom fields to remove beyond default configuration",
    )
    preserve_fields: Optional[Set[str]] = Field(
        default=None,
        description="Optional fields to preserve even if normally filtered",
    )

    @field_validator("custom_fields", "preserve_fields")
    @classmethod
    def validate_custom_fields(cls, v: Optional[Set[str]]) -> Optional[Set[str]]:
        """Validate custom field specifications.

        Args:
            v: Set of custom field names to validate

        Returns:
            Validated set of custom field names

        Raises:
            ValueError: If any field names are empty or not strings
        """
        if v is None:
            return v

        invalid_fields = {
            field
            for field in v
            if not field or not isinstance(field, str) or not field.strip()
        }
        if invalid_fields:
            raise ValueError(
                f"Custom field names must be non-empty strings: {invalid_fields}"
            )

        return v
