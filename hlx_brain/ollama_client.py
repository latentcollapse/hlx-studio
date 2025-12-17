"""
Ollama Client for HLX Brain

Provides Python interface to Ollama's REST API for LLM inference.
Supports both streaming and non-streaming responses.
"""

import requests
import json
from typing import List, Dict, Optional


class OllamaClient:
    """Client for interacting with Ollama LLM server."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen3:8b"):
        """
        Initialize Ollama client.

        Args:
            base_url: Ollama server URL (default: http://localhost:11434)
            model: Model name to use (default: qwen3:8b)
        """
        self.base_url = base_url
        self.model = model

    def generate(self,
                 prompt: str,
                 system: Optional[str] = None,
                 temperature: float = 0.7,
                 stream: bool = False) -> str:
        """
        Generate text from a prompt.

        Args:
            prompt: The input prompt
            system: Optional system prompt for context
            temperature: Sampling temperature (0.0-1.0)
            stream: Whether to stream the response

        Returns:
            Generated text response

        Raises:
            requests.RequestException: If API call fails
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": {"temperature": temperature}
        }

        if system:
            payload["system"] = system

        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()

        if stream:
            # For streaming, we'd need to handle chunks
            # For now, just return the full response
            return response.json()["response"]
        else:
            result = response.json()
            return result.get("response", "")

    def chat(self,
             messages: List[Dict[str, str]],
             temperature: float = 0.7,
             stream: bool = False) -> str:
        """
        Chat completion with message history.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
                     Example: [{"role": "user", "content": "Hello"}]
            temperature: Sampling temperature (0.0-1.0)
            stream: Whether to stream the response

        Returns:
            Generated response message content

        Raises:
            requests.RequestException: If API call fails
        """
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": {"temperature": temperature}
        }

        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()
        return result.get("message", {}).get("content", "")

    def embed(self, text: str, model: str = "nomic-embed-text") -> List[float]:
        """
        Generate embeddings for text.

        Args:
            text: Text to embed
            model: Embedding model to use (default: nomic-embed-text)

        Returns:
            List of embedding values (vector)

        Raises:
            requests.RequestException: If API call fails
        """
        url = f"{self.base_url}/api/embeddings"
        payload = {
            "model": model,
            "prompt": text
        }

        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()
        return result.get("embedding", [])

    def list_models(self) -> List[Dict]:
        """
        List available models on the Ollama server.

        Returns:
            List of model information dicts

        Raises:
            requests.RequestException: If API call fails
        """
        url = f"{self.base_url}/api/tags"
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        result = response.json()
        return result.get("models", [])

    def check_health(self) -> bool:
        """
        Check if Ollama server is healthy and responsive.

        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except:
            return False
