"""Response filtering utilities for Terraform Cloud MCP

This module provides smart filtering of API responses to reduce token usage
while preserving essential data for MCP operations.
"""

from typing import Dict, Any, Callable, Union

from ..models.filters import FilterConfig, OperationType, ResourceType, FilterRequest
from ..configs.filter_configs import (
    FILTER_CONFIGS,
    RESOURCE_TYPE_MAP,
    PATH_PATTERNS,
    DATA_TYPE_MAP,
)


def filter_response(
    data: Dict[str, Any],
    resource_type: Union[str, ResourceType],
    operation_type: Union[str, OperationType] = OperationType.READ,
) -> Dict[str, Any]:
    """Filter API response to remove unnecessary fields."""
    if not isinstance(data, dict) or "data" not in data:
        return data

    # Shallow copy response for performance
    filtered_data = data.copy()
    if isinstance(filtered_data["data"], list):
        filtered_data["data"] = [
            item.copy() if isinstance(item, dict) else item
            for item in filtered_data["data"]
        ]
    elif isinstance(filtered_data["data"], dict):
        filtered_data["data"] = filtered_data["data"].copy()
    for key in ("meta", "links"):
        if key in filtered_data:
            filtered_data[key] = filtered_data[key].copy()

    # Normalize types to enums
    if isinstance(resource_type, str):
        normalized_type = RESOURCE_TYPE_MAP.get(resource_type, ResourceType.GENERIC)
    elif isinstance(resource_type, ResourceType):
        normalized_type = resource_type
    else:
        raise ValueError(f"Invalid resource_type: {resource_type}")

    if isinstance(operation_type, str):
        try:
            operation_enum = OperationType(operation_type)
        except ValueError:
            raise ValueError(f"Invalid operation_type: {operation_type}")
    elif isinstance(operation_type, OperationType):
        operation_enum = operation_type
    else:
        raise ValueError(f"Invalid operation_type: {operation_type}")

    # Handle single item or list of items
    if isinstance(filtered_data["data"], list):
        for item in filtered_data["data"]:
            _filter_item_attributes(item, normalized_type, operation_enum)
    else:
        _filter_item_attributes(filtered_data["data"], normalized_type, operation_enum)

    # Filter top-level metadata for list operations
    if operation_enum == OperationType.LIST:
        _filter_list_metadata(filtered_data)

    return filtered_data


def filter_with_request(data: Dict[str, Any], request: FilterRequest) -> Dict[str, Any]:
    """Filter API response using a FilterRequest object."""
    # Apply base filtering
    filtered_data = filter_response(data, request.resource_type, request.operation_type)

    # Apply custom field removals if specified
    if request.custom_fields:
        if isinstance(filtered_data["data"], list):
            for item in filtered_data["data"]:
                _remove_custom_fields(item, request.custom_fields)
        else:
            _remove_custom_fields(filtered_data["data"], request.custom_fields)

    # Restore preserved fields if specified
    if request.preserve_fields:
        # This would require access to original data - placeholder for future implementation
        pass

    return filtered_data


def _filter_item_attributes(
    item: Dict[str, Any], resource_type: ResourceType, operation_type: OperationType
) -> None:
    """Filter individual item attributes in-place."""
    if "attributes" not in item:
        return

    # Shallow copy attributes to avoid modifying original
    if not isinstance(item["attributes"], dict):
        return
    item["attributes"] = item["attributes"].copy()
    attrs = item["attributes"]

    config = FILTER_CONFIGS.get(resource_type, FilterConfig())

    # Build set of fields to remove using Pydantic model
    fields_to_remove = set(config.always_remove)

    if operation_type == OperationType.READ:
        fields_to_remove.update(config.read_remove)
    elif operation_type == OperationType.LIST:
        fields_to_remove.update(config.list_remove)

    # Remove specified fields
    for field in fields_to_remove:
        attrs.pop(field, None)

    # Handle relationships
    if "relationships" in item:
        # Shallow copy relationships to avoid modifying original
        item["relationships"] = item["relationships"].copy()
        _filter_relationships(item["relationships"], resource_type, operation_type)

    # Remove item-level links
    item.pop("links", None)


def _filter_relationships(
    relationships: Dict[str, Any],
    resource_type: ResourceType,
    operation_type: OperationType,
) -> None:
    """Filter relationships in-place."""
    config = FILTER_CONFIGS.get(resource_type, FilterConfig())
    essential_rels = config.essential_relationships

    if operation_type == OperationType.READ and essential_rels:
        # Keep only essential relationships
        keys_to_remove = [k for k in relationships.keys() if k not in essential_rels]
        for key in keys_to_remove:
            relationships.pop(key, None)

    # Remove links from all remaining relationships
    for key, rel_data in relationships.items():
        if isinstance(rel_data, dict):
            # Shallow copy individual relationship to avoid modifying original
            relationships[key] = rel_data.copy()
            relationships[key].pop("links", None)

    # Remove empty relationships
    if not relationships:
        return


def _remove_custom_fields(item: Dict[str, Any], custom_fields: set[str]) -> None:
    """Remove custom fields from an item."""
    if "attributes" not in item or not isinstance(item["attributes"], dict):
        return

    attrs = item["attributes"]
    for field in custom_fields:
        attrs.pop(field, None)


def _filter_list_metadata(data: Dict[str, Any]) -> None:
    """Filter list response metadata and pagination links in-place."""
    # Filter metadata
    if "meta" in data:
        meta = data["meta"]
        if "pagination" in meta and isinstance(meta["pagination"], dict):
            pagination = meta["pagination"]
            meta["pagination"] = {
                "current-page": pagination.get("current-page"),
                "total-pages": pagination.get("total-pages"),
                "total-count": pagination.get("total-count"),
            }
        if "status-counts" in meta and isinstance(meta["status-counts"], dict):
            status_counts = meta["status-counts"]
            if "total" in status_counts:
                meta["status-counts"] = {"total": status_counts["total"]}
            else:
                meta.pop("status-counts", None)

    # Filter pagination links
    if "links" in data and isinstance(data["links"], dict):
        links = data["links"]
        essential_links = {
            k: links[k] for k in ["next", "prev", "first", "last"] if k in links
        }
        data["links"] = essential_links


def get_response_filter(resource_type: Union[str, ResourceType]) -> Callable:
    """Get the appropriate filter function for a resource type."""

    def resource_filter(
        data: Dict[str, Any],
        operation_type: Union[str, OperationType] = OperationType.READ,
    ) -> Dict[str, Any]:
        return filter_response(data, resource_type, operation_type)

    return resource_filter


def should_filter_response(path: str, method: str) -> bool:
    """Determine if a response should be filtered based on the API path and method."""
    # Only filter GET requests
    if method.upper() != "GET":
        return False

    # Don't filter log or download endpoints
    skip_terms = ["log", "download", "json-output", "content"]
    return not any(term in path.lower() for term in skip_terms)


def detect_resource_type(path: str, data: Dict[str, Any]) -> ResourceType:
    """Detect resource type from API path and response data."""
    # Path-based detection
    for pattern, resource_type in PATH_PATTERNS:
        if pattern in path:
            return resource_type

    # Data-based fallback
    if isinstance(data, dict) and "data" in data:
        data_item = data["data"]
        if isinstance(data_item, list) and data_item:
            data_type = data_item[0].get("type", "unknown")
        elif isinstance(data_item, dict):
            data_type = data_item.get("type", "unknown")
        else:
            return ResourceType.GENERIC

        if data_type in DATA_TYPE_MAP:
            return DATA_TYPE_MAP[data_type]

        for resource_type in ResourceType:
            if resource_type.value == data_type:
                return resource_type

    return ResourceType.GENERIC


def detect_operation_type(path: str, method: str) -> OperationType:
    """Detect operation type from API path and method."""
    if method.upper() == "GET":
        id_prefixes = ["ws-", "run-", "org-", "prj-", "var-"]
        has_resource_id = any(
            segment.startswith(prefix)
            for segment in path.split("/")
            for prefix in id_prefixes
        )
        return OperationType.READ if has_resource_id else OperationType.LIST
    return OperationType.MANAGE
