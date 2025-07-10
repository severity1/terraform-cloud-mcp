"""JSON:API payload utilities for Terraform Cloud MCP."""

from typing import Dict, Optional, Set, Any
from pydantic import BaseModel


def create_api_payload(
    resource_type: str,
    model: BaseModel,
    exclude_fields: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    """Creates a JSON:API compliant payload from a Pydantic model."""
    attributes = model.model_dump(
        by_alias=True,
        exclude=exclude_fields or set(),
        exclude_none=True,
    )

    return {"data": {"type": resource_type, "attributes": attributes}}


def add_relationship(
    payload: Dict[str, Any], relation_name: str, resource_type: str, resource_id: str
) -> Dict[str, Any]:
    """Adds a relationship to a JSON:API payload."""
    if "relationships" not in payload["data"]:
        payload["data"]["relationships"] = {}

    payload["data"]["relationships"][relation_name] = {
        "data": {"type": resource_type, "id": resource_id}
    }

    return payload
