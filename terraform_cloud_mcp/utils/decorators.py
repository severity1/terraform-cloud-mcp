"""Decorators and utility functions for Terraform Cloud MCP"""

from functools import wraps
from typing import Callable, Any, Dict, Awaitable, cast


def handle_api_errors(
    func: Callable[..., Awaitable[Dict[str, Any]]],
) -> Callable[..., Awaitable[Dict[str, Any]]]:
    """Decorator to handle API errors consistently."""

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            result = await func(*args, **kwargs)
            # Cast ensures type safety when func might return subclass of Dict
            return cast(Dict[str, Any], result)
        except ValueError as e:
            return {"error": str(e)}

    return wrapper
