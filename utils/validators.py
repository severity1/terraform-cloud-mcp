"""Validation utilities for Terraform Cloud MCP"""

import re
from typing import Tuple

# Validation patterns
# Organization names must be lowercase alphanumeric with hyphens allowed, minimum 3 chars, maximum 60 chars
ORGANIZATION_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,58}[a-z0-9]$")


def validate_organization(organization: str) -> Tuple[bool, str]:
    """
    Validate organization name format according to Terraform Cloud rules

    Args:
        organization: Organization name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not organization:
        return (False, "Organization name is required")

    if not isinstance(organization, str):
        return (False, "Organization name must be a string")

    if not ORGANIZATION_NAME_PATTERN.match(organization):
        return (
            False,
            "Organization name must be lowercase alphanumeric with hyphens allowed, minimum 3 chars, maximum 60 chars",
        )

    return (True, "")
