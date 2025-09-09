"""Environment variable management for Terraform Cloud MCP"""

import os
from typing import Optional


def get_tfc_token() -> Optional[str]:
    """Get Terraform Cloud API token from environment."""
    return os.getenv("TFC_TOKEN")


def get_tfc_address() -> str:
    """Get Terraform Cloud/Enterprise address from environment, with default of app.terraform.io."""
    return os.getenv("TFC_ADDRESS", "https://app.terraform.io")


def should_enable_delete_tools() -> bool:
    """Check if delete tools should be enabled."""
    env_value = os.getenv("ENABLE_DELETE_TOOLS", "false").lower().strip()
    return env_value in ("true", "1", "yes", "on")


def should_return_raw_response() -> bool:
    """Check if raw API responses should be returned instead of filtered responses."""
    env_value = os.getenv("ENABLE_RAW_RESPONSE", "false").lower().strip()
    return env_value in ("true", "1", "yes", "on")


def should_enable_read_only_tools() -> bool:
    """Check if only read-only tools should be enabled."""
    env_value = os.getenv("READ_ONLY_TOOLS", "false").lower().strip()
    return env_value in ("true", "1", "yes", "on")
