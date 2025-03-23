"""Decorators and utility functions for Terraform Cloud MCP"""

from functools import wraps
from typing import Callable, Any, Dict, Awaitable, cast


def handle_api_errors(
    func: Callable[..., Awaitable[Dict[str, Any]]],
) -> Callable[..., Awaitable[Dict[str, Any]]]:
    """Decorator to handle API errors consistently.

    This decorator wraps API functions to catch ValueError exceptions
    and return them as standardized error responses.

    Args:
        func: The async function to wrap

    Returns:
        Wrapped function that catches ValueErrors and returns error dictionaries
    """

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            result = await func(*args, **kwargs)
            return cast(Dict[str, Any], result)
        except ValueError as e:
            return {"error": str(e)}

    return wrapper
