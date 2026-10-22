"""Persona Endpoints Module

REST API routes for creating and listing user personas.
Each persona defines a custom bot personality with its own prompt,
language, and accent settings.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from auth import get_current_user
from custom_supabase import insert_persona_to_supabase, get_all_personas_for_user

logger = logging.getLogger("voicebot")

# ==================== Request/Response Models ====================

class CreatePersonaRequest(BaseModel):
    name: str
    description: Optional[str] = None
    icon: str = "🤖"
    custom_prompt: str

class PersonaResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str]
    icon: str
    custom_prompt: str
    knowledge_base: str
    language: str
    accent: str
    created_at: str
    updated_at: str

class PersonaListResponse(BaseModel):
    personas: list[dict]
    total: int
    default_count: int
    user_count: int

# ==================== Router ====================

router = APIRouter(prefix="/personas", tags=["personas"])


@router.post("/create", response_model=PersonaResponse)
async def create_persona(
    persona_data: CreatePersonaRequest,
    user=Depends(get_current_user)
):
    """Create a new custom persona for the authenticated user."""
    try:
        user_id = user['sub']
        
        # Validate required fields
        if not persona_data.name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Persona name cannot be empty"
            )
        
        if not persona_data.custom_prompt.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Custom prompt cannot be empty"
            )
        
        created_persona = await insert_persona_to_supabase(
            name=persona_data.name,
            description=persona_data.description,
            icon=persona_data.icon,
            custom_prompt=persona_data.custom_prompt,
            user_id=user_id
        )
        
        logger.info(f"Persona created for user {user_id[:8]}...: {created_persona['name']}")
        
        return PersonaResponse(**created_persona)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in create_persona: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the persona"
        )


@router.get("/", response_model=PersonaListResponse)
async def get_all_personas(user=Depends(get_current_user)):
    """Retrieve all personas (default + custom) for the authenticated user."""
    try:
        user_id = user['sub']
        result = await get_all_personas_for_user(user_id)
        
        logger.info(
            f"Retrieved {result['total']} personas for user {user_id[:8]}... "
            f"({result['default_count']} default, {result['user_count']} custom)"
        )
        
        return PersonaListResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in get_all_personas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching personas"
        )