"""
Linguistic PDF Bot — Entry Point

This module serves as the application entry point. The main application
logic lives in app.py with modular service files.

Run with: uvicorn main:app --reload --port 8000

Module structure:
- config.py:             Environment variables & model configuration
- app.py:                FastAPI application, middleware, and routes
- websocket_handler.py:  WebSocket connection & voice pipeline handling
- llm_service.py:        LangGraph agent graph construction
- rag_service.py:        Qdrant vector store & document search tool
- document_service.py:   PDF upload, parsing & chunking
- audio_services.py:     Groq ASR & Murf TTS integration
- auth.py:               JWT authentication middleware
- custom_supabase.py:    Supabase client for user/session data
- custom_endpoints.py:   REST API routes for persona management
"""

from app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)