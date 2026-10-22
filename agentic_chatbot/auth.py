"""Authentication Module

Provides JWT token verification and user extraction for FastAPI
endpoints using Supabase JWT secrets.
"""

import logging
import jwt
from fastapi import HTTPException, status, Header
from jwt import PyJWTError
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger("voicebot")

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

if not SUPABASE_JWT_SECRET:
    logger.warning("SUPABASE_JWT_SECRET not set — authenticated endpoints will fail.")


def verify_token(token: str) -> dict:
    """Verify and decode a Supabase JWT token.

    Args:
        token: The raw JWT string (without 'Bearer ' prefix).

    Returns:
        Decoded JWT payload as a dictionary.

    Raises:
        HTTPException: 401 if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Authentication failed: token has expired.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except PyJWTError as e:
        logger.warning(f"Authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


def get_current_user(authorization: str = Header(...)) -> dict:
    """Extract and verify the current user from the Authorization header.

    Args:
        authorization: The Authorization header value (expects 'Bearer <token>').

    Returns:
        Decoded JWT payload containing user claims (sub, email, etc.).

    Raises:
        HTTPException: 401 if the header format is invalid or token is bad.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected: Bearer <token>",
        )
    token = authorization.split(" ", 1)[1]
    payload = verify_token(token)
    return payload