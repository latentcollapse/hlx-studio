"""
HLX Brain - AI-powered assistant for HLX Development Studio

Components:
- ollama_client: Client for Ollama LLM inference
- rag: Retrieval-Augmented Generation system with ChromaDB
- brain: Unified interface for HLX-aware AI assistance
"""

from .ollama_client import OllamaClient
from .rag import HLXCorpusRAG
from .brain import HLXBrain

__all__ = ['OllamaClient', 'HLXCorpusRAG', 'HLXBrain']
