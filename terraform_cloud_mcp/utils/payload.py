"""JSON:API payload utilities for Terraform Cloud MCP.

This module provides helper functions for creating JSON:API compliant payloads
for Terraform Cloud API requests, reducing code duplication and improving consistency.
"""

from typing import Dict, Optional, Set, Any
from pydantic import BaseModel


def create_api_payload(
    resource_type: str,
    model: BaseModel,
    exclude_fields: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    """Creates a JSON:API compliant payload from a Pydantic model.

    Extracts attributes from a model using the project's standard Pydantic pattern
    and formats them according to the JSON:API specification.

    Args:
        resource_type: The JSON:API resource type (e.g., "workspaces")
        model: Pydantic model containing the attributes
        exclude_fields: Fields to exclude from attributes

    Returns:
        JSON:API formatted payload dictionary

    Example:
        ```python
        request = WorkspaceCreateRequest(name="example", organization="org")
        payload = create_api_payload(
            "workspaces",
            request,
            exclude_fields={"organization"}
        )
        ```
    """
    attributes = model.model_dump(
        by_alias=True,
        exclude=exclude_fields or set(),
        exclude_none=True,
    )

    return {"data": {"type": resource_type, "attributes": attributes}}


def add_relationship(
    payload: Dict[str, Any], relation_name: str, resource_type: str, resource_id: str
) -> Dict[str, Any]:
    """Adds a relationship to a JSON:API payload.

    Args:
        payload: Existing JSON:API payload dict
        relation_name: Name of the relationship (e.g., "workspace")
        resource_type: Related resource type (e.g., "workspaces")
        resource_id: ID of the related resource

    Returns:
        Updated payload with the relationship added

    Example:
        ```python
        payload = create_api_payload("runs", run_request)
        payload = add_relationship(
            payload,
            "workspace",
            "workspaces",
            workspace_id
        )
        ```
    """
    if "relationships" not in payload["data"]:
        payload["data"]["relationships"] = {}

    payload["data"]["relationships"][relation_name] = {
        "data": {"type": resource_type, "id": resource_id}
    }

    return payload
