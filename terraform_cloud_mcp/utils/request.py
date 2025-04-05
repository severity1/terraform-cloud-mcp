"""Request utilities for Terraform Cloud MCP.

This module provides helper functions for creating and processing
API request parameters consistently across the codebase.
"""

from typing import Dict, Any, Optional, Protocol


class PaginationModel(Protocol):
    """Protocol for models with pagination fields."""

    page_number: int | None
    page_size: int | None


def pagination_params(
    model: PaginationModel, search_field: Optional[str] = "search"
) -> Dict[str, Any]:
    """Creates pagination parameters from a Pydantic request model.

    Works with standard request models that have page_number and page_size fields.

    Args:
        model: Pydantic model with pagination fields
        search_field: Field name to use for search parameter (if present in model)

    Returns:
        Dictionary with formatted pagination parameters

    Example:
        ```python
        request = WorkspaceListRequest(
            organization="example",
            page_number=2,
            page_size=20,
            search="test"
        )
        params = pagination_params(request)
        # Result: {"page[number]": "2", "page[size]": "20", "search": "test"}
        ```
    """
    params = {}

    # Safely add pagination parameters if they exist and are not None
    if hasattr(model, "page_number") and model.page_number is not None:
        params["page[number]"] = str(model.page_number)

    if hasattr(model, "page_size") and model.page_size is not None:
        params["page[size]"] = str(model.page_size)

    # Add search parameter if the field exists and has a value
    if search_field and hasattr(model, search_field) and getattr(model, search_field):
        params[search_field] = getattr(model, search_field)

    return params
