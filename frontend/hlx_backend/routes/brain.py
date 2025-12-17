"""
HLX Brain AI Assistant Routes
Endpoints for RAG-augmented question answering, code explanation, debugging, and chat.
Integrates Ollama LLM with RAG system for HLX-aware assistance.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import sys
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from hlx_brain import HLXBrain

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/brain", tags=["brain"])

# ============================================================================
# Singleton Brain Instance
# ============================================================================

# Initialize HLX Brain with default settings
_brain_instance: Optional[HLXBrain] = None
_corpus_loaded = False


def get_brain() -> HLXBrain:
    """
    Get or create the singleton HLXBrain instance.

    Returns:
        HLXBrain: The singleton brain instance
    """
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = HLXBrain(
            persist_directory="/home/matt/hlx-dev-studio/.chromadb"
        )
        logger.info("Initialized HLXBrain with ChromaDB persistence")
    return _brain_instance


async def load_corpus_on_startup():
    """
    Load corpus on application startup if not already loaded.
    Called during application initialization.
    """
    global _corpus_loaded
    if _corpus_loaded:
        return

    brain = get_brain()
    try:
        # Try to load default corpus if it exists
        corpus_path = "/home/matt/hlx-dev-studio/corpus.json"
        from pathlib import Path as PathlibPath
        if PathlibPath(corpus_path).exists():
            count = brain.load_corpus(corpus_path)
            _corpus_loaded = True
            logger.info(f"Loaded {count} documents from corpus on startup")
        else:
            logger.debug(f"Corpus file not found at {corpus_path}")
    except Exception as e:
        logger.warning(f"Failed to load corpus on startup: {e}")


# ============================================================================
# Request/Response Models
# ============================================================================


class AskRequest(BaseModel):
    """Question asking request."""
    question: str = Field(..., description="Question to ask about HLX")
    use_rag: bool = Field(True, description="Use RAG for context-augmented answering")
    temperature: float = Field(
        0.7,
        ge=0.0,
        le=2.0,
        description="LLM sampling temperature (0.0-2.0)"
    )
    n_context_docs: int = Field(
        5,
        ge=1,
        le=20,
        description="Number of context documents to retrieve"
    )


class AskResponse(BaseModel):
    """Question answering response."""
    answer: str = Field(..., description="Answer to the question")


class ExplainRequest(BaseModel):
    """Code explanation request."""
    code: str = Field(..., description="Code to explain")
    language: str = Field(
        "HLXL",
        description="Programming language (HLXL, HLX-Lite, Python, etc.)"
    )


class ExplainResponse(BaseModel):
    """Code explanation response."""
    explanation: str = Field(..., description="Explanation of the code")


class DebugRequest(BaseModel):
    """Code debugging request."""
    code: str = Field(..., description="Code to debug")
    error_message: Optional[str] = Field(
        None,
        description="Error message or stack trace (optional)"
    )
    language: str = Field(
        "HLXL",
        description="Programming language (HLXL, HLX-Lite, Python, etc.)"
    )


class DebugResponse(BaseModel):
    """Code debugging response."""
    suggestions: str = Field(..., description="Debugging suggestions and fixes")


class Message(BaseModel):
    """Single chat message."""
    role: str = Field(..., description="Message role (user, assistant, system)")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Chat conversation request."""
    messages: List[Message] = Field(..., description="Conversation history")
    temperature: float = Field(
        0.7,
        ge=0.0,
        le=2.0,
        description="LLM sampling temperature (0.0-2.0)"
    )


class ChatResponse(BaseModel):
    """Chat conversation response."""
    response: str = Field(..., description="Assistant's response")


class BrainStats(BaseModel):
    """Brain health and statistics."""
    model: str = Field(..., description="LLM model name")
    ollama_url: str = Field(..., description="Ollama server URL")
    ollama_healthy: bool = Field(..., description="Whether Ollama is reachable")
    corpus_loaded: bool = Field(..., description="Whether corpus is loaded")
    rag_documents: int = Field(..., description="Number of documents in RAG")
    rag_collection: Optional[str] = Field(..., description="RAG collection name")


class StatusResponse(BaseModel):
    """Brain status response."""
    status: str = Field("ok", description="Overall status")
    brain: BrainStats = Field(..., description="Brain statistics")


# ============================================================================
# Endpoints
# ============================================================================


@router.post("/ask", response_model=AskResponse)
async def ask_question(req: AskRequest):
    """
    Ask a question about HLX with optional RAG context.

    Supports both general LLM queries and RAG-augmented answering using
    HLX documentation and corpus.

    Example:
        POST /brain/ask
        {
            "question": "How do I collapse a value in HLX?",
            "use_rag": true,
            "temperature": 0.7,
            "n_context_docs": 5
        }

        Response:
        {
            "answer": "To collapse a value in HLX, you use the collapse function..."
        }
    """
    try:
        brain = get_brain()
        answer = brain.ask(
            question=req.question,
            use_rag=req.use_rag,
            temperature=req.temperature,
            n_context_docs=req.n_context_docs
        )
        return AskResponse(answer=answer)
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to answer question: {str(e)}"
        )


@router.post("/explain", response_model=ExplainResponse)
async def explain_code(req: ExplainRequest):
    """
    Explain provided code.

    Uses the brain to provide detailed explanations of code functionality,
    with HLX-specific context when the language is HLXL.

    Example:
        POST /brain/explain
        {
            "code": "let x = collapse(42);",
            "language": "HLXL"
        }

        Response:
        {
            "explanation": "This HLXL code creates a value bound to x..."
        }
    """
    try:
        brain = get_brain()
        explanation = brain.explain_code(
            code=req.code,
            language=req.language,
            use_rag=True
        )
        return ExplainResponse(explanation=explanation)
    except Exception as e:
        logger.error(f"Error explaining code: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to explain code: {str(e)}"
        )


@router.post("/debug", response_model=DebugResponse)
async def debug_code(req: DebugRequest):
    """
    Debug code and get suggestions for fixes.

    Analyzes code with optional error messages and provides debugging
    suggestions with corrected code examples.

    Example:
        POST /brain/debug
        {
            "code": "let x = collapse(42)\nlet y = x + 1",
            "error_message": "SyntaxError: unexpected token",
            "language": "HLXL"
        }

        Response:
        {
            "suggestions": "The code is missing a semicolon after collapse(42)..."
        }
    """
    try:
        brain = get_brain()
        suggestions = brain.debug_code(
            code=req.code,
            error_message=req.error_message,
            language=req.language
        )
        return DebugResponse(suggestions=suggestions)
    except Exception as e:
        logger.error(f"Error debugging code: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to debug code: {str(e)}"
        )


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Continue a multi-turn conversation with the brain.

    Maintains conversation context through message history for coherent,
    context-aware dialogue.

    Example:
        POST /brain/chat
        {
            "messages": [
                {"role": "user", "content": "What is HLX?"},
                {"role": "assistant", "content": "HLX is a content-addressed..."},
                {"role": "user", "content": "How do I use it?"}
            ],
            "temperature": 0.7
        }

        Response:
        {
            "response": "To use HLX, you first need to..."
        }
    """
    try:
        brain = get_brain()

        # Convert Pydantic Message objects to dicts for the brain
        messages = [{"role": m.role, "content": m.content} for m in req.messages]

        response = brain.chat(
            messages=messages,
            temperature=req.temperature
        )
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat: {str(e)}"
        )


@router.get("/status", response_model=StatusResponse)
async def get_status():
    """
    Get HLX Brain health status and statistics.

    Returns current state of the brain including model info, Ollama health,
    corpus status, and RAG statistics.

    Example:
        GET /brain/status

        Response:
        {
            "status": "ok",
            "brain": {
                "model": "qwen3:8b",
                "ollama_url": "http://localhost:11434",
                "ollama_healthy": true,
                "corpus_loaded": true,
                "rag_documents": 156,
                "rag_collection": "hlx_corpus"
            }
        }
    """
    try:
        brain = get_brain()
        stats = brain.get_stats()

        brain_stats = BrainStats(
            model=stats.get("model", "unknown"),
            ollama_url=stats.get("ollama_url", "unknown"),
            ollama_healthy=stats.get("ollama_healthy", False),
            corpus_loaded=stats.get("corpus_loaded", False),
            rag_documents=stats.get("rag_documents", 0),
            rag_collection=stats.get("rag_collection", None)
        )

        return StatusResponse(status="ok", brain=brain_stats)
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get brain status: {str(e)}"
        )
