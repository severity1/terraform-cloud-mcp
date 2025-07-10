"""Request utilities for Terraform Cloud MCP."""

from typing import Dict, Any
from pydantic import BaseModel


def query_params(model: BaseModel) -> Dict[str, Any]:
    """Transform Pydantic model fields to API parameters using naming conventions."""
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

            # Handle nested filters (workspace and organization for state versions)
            if name == "filter_workspace_name":
                params["filter[workspace][name]"] = str(value)
            elif name == "filter_organization_name":
                params["filter[organization][name]"] = str(value)
            # Handle two-level filters (permissions)
            elif "_permissions_" in name:
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
