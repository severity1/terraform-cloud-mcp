"""Environment variable management for Terraform Cloud MCP

This module provides centralized environment variable handling for the
Terraform Cloud MCP server, including validation and type conversion.
"""

import os
from typing import Optional


def get_tfc_token() -> Optional[str]:
    """Get Terraform Cloud API token from environment.

    Returns:
        The TFC_TOKEN environment variable value, or None if not set
    """
    return os.getenv("TFC_TOKEN")


def should_enable_delete_tools() -> bool:
    """Check if delete tools should be enabled.

    Reads the ENABLE_DELETE_TOOLS environment variable and converts it to a boolean.
    Supports standard boolean representations: "true", "false", "1", "0" (case-insensitive).

    Returns:
        True if delete tools should be enabled, False otherwise (default: False)
    """
    env_value = os.getenv("ENABLE_DELETE_TOOLS", "false").lower().strip()
    return env_value in ("true", "1", "yes", "on")
