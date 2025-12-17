"""
Authentication Module for HLX Dev Studio API
Simple token-based authentication for Claude control endpoints.
"""

import os
from typing import Optional
from functools import wraps
from fastapi import HTTPException, Header, status


class TokenAuth:
    """
    Simple token-based authentication.
    Uses environment variable HLX_API_TOKEN for validation.
    """

    def __init__(self):
        """Initialize authentication with token from environment."""
        self.token = os.getenv("HLX_API_TOKEN", "")
        self.enabled = bool(self.token)
        if self.enabled:
            print(f"[Auth] Token authentication enabled (token length: {len(self.token)})")
        else:
            print("[Auth] Token authentication disabled (set HLX_API_TOKEN env var to enable)")

    def validate_token(self, token: Optional[str]) -> bool:
        """
        Validate a provided token.

        Args:
            token: Token to validate

        Returns:
            bool: True if token is valid, False otherwise
        """
        if not self.enabled:
            return True  # Auth disabled, allow all

        if not token:
            return False

        return token == self.token

    def get_bearer_token(self, authorization: Optional[str] = None) -> Optional[str]:
        """
        Extract bearer token from Authorization header.

        Args:
            authorization: Authorization header value

        Returns:
            str: Token if valid format, None otherwise
        """
        if not authorization:
            return None

        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        return parts[1]

    async def require_token(self, authorization: Optional[str] = Header(None)) -> str:
        """
        FastAPI dependency for token validation.

        Args:
            authorization: Authorization header from request

        Returns:
            str: Valid token

        Raises:
            HTTPException: If token invalid or missing
        """
        if not self.enabled:
            return "disabled"  # Auth disabled, return placeholder

        token = self.get_bearer_token(authorization)
        if not token or not self.validate_token(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return token


# Global auth instance
auth_manager = TokenAuth()
