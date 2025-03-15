"""Authentication models for Terraform Cloud"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class AuthResult:
    """Result of an authentication operation"""
    success: bool
    message: str
    user_name: Optional[str] = None
