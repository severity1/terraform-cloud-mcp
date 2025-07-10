"""Environment variable management for Terraform Cloud MCP"""

import os
from typing import Optional


def get_tfc_token() -> Optional[str]:
    """Get Terraform Cloud API token from environment."""
    return os.getenv("TFC_TOKEN")


def should_enable_delete_tools() -> bool:
    """Check if delete tools should be enabled."""
    env_value = os.getenv("ENABLE_DELETE_TOOLS", "false").lower().strip()
    return env_value in ("true", "1", "yes", "on")


def should_return_raw_response() -> bool:
    """Check if raw API responses should be returned instead of filtered responses."""
    env_value = os.getenv("ENABLE_RAW_RESPONSE", "false").lower().strip()
    return env_value in ("true", "1", "yes", "on")
