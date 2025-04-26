"""Request utilities for Terraform Cloud MCP.

This module provides helper functions for creating and processing
API request parameters consistently across the codebase.
"""

from typing import Dict, Any
from pydantic import BaseModel


def query_params(model: BaseModel) -> Dict[str, Any]:
    """Transform Pydantic model fields to API parameters using naming conventions.

    Creates a complete set of query parameters from a request model using
    consistent naming conventions for parameter types:
    - Pagination: 'page_number' -> 'page[number]'
    - Filters: 'filter_name' -> 'filter[name]'
    - Search: 'search_term' -> 'search[term]'
    - Query: 'query_email' -> 'q[email]', 'query_name' -> 'q[name]'
    - Direct params: Direct mapping for 'q', 'search', etc.

    Args:
        model: Pydantic model with parameter fields

    Returns:
        Dictionary with all formatted API parameters

    Example:
        ```python
        request = ProjectListRequest(
            organization="example",
            page_number=2,
            page_size=20,
            filter_names="test",
            q="search term"
        )
        params = query_params(request)
        # Result: {
        #   "page[number]": "2",
        #   "page[size]": "20",
        #   "filter[names]": "test",
        #   "q": "search term"
        # }
        ```
    """
    params = {}
    routing_fields = {
        "organization",
        "workspace_name",
        "workspace_id",
        "run_id",
        "plan_id",
        "apply_id",
        "project_id",
    }

    # Use model_dump for reliable field access
    model_dict = model.model_dump(exclude_none=True)

    for name, value in model_dict.items():
        # Skip routing fields that aren't query parameters
        if name in routing_fields:
            continue

        # Pagination parameters
        if name.startswith("page_"):
            field_name = name.replace("page_", "")
            params[f"page[{field_name}]"] = str(value)

        # Filter parameters
        elif name.startswith("filter_"):
            # Skip empty string filters
            if value == "":
                continue

            # Handle two-level filters (permissions)
            if "_permissions_" in name:
                parts = name.replace("filter_permissions_", "").split("_")
                field_name = "-".join(parts)
                params[f"filter[permissions][{field_name}]"] = (
                    "true" if value is True else str(value)
                )
            else:
                field_name = name.replace("filter_", "").replace("_", "-")
                params[f"filter[{field_name}]"] = (
                    "true" if value is True else str(value)
                )

        # Search parameters
        elif name.startswith("search_"):
            if value not in ("", None):
                field_name = name.replace("search_", "")
                params[f"search[{field_name}]"] = str(value)

        # Organization query parameters
        elif name.startswith("query_"):
            if value not in ("", None):
                field_name = name.replace("query_", "")
                params[f"q[{field_name}]"] = str(value)

        # Direct parameters
        elif name in ("q", "search", "sort"):
            # Only add non-empty string parameters
            if value not in ("", None):
                params[name] = str(value)

    return params
