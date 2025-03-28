"""Terraform Cloud MCP - A MCP server for Terraform Cloud"""

from .server import main
import importlib.metadata

__version__ = importlib.metadata.version("terraform-cloud-mcp")

__all__ = ["main"]
