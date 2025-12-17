"""
HLX Brain - Unified AI Assistant Interface

Combines Ollama LLM with RAG system for HLX-aware assistance.
Provides high-level methods for common tasks like code explanation,
debugging, and question answering.
"""

from .ollama_client import OllamaClient
from .rag import HLXCorpusRAG
from typing import Optional, List, Dict


class HLXBrain:
    """
    Unified interface for HLX AI assistance.

    Combines Ollama LLM inference with RAG-based document retrieval
    to provide context-aware, HLX-specific assistance.
    """

    def __init__(self,
                 ollama_url: str = "http://localhost:11434",
                 model: str = "qwen3:8b",
                 persist_directory: Optional[str] = None):
        """
        Initialize HLX Brain.

        Args:
            ollama_url: Ollama server URL
            model: LLM model to use
            persist_directory: Optional directory to persist RAG data
        """
        self.ollama = OllamaClient(base_url=ollama_url, model=model)
        self.rag = HLXCorpusRAG(
            ollama_url=ollama_url,
            persist_directory=persist_directory
        )
        self._corpus_loaded = False

    def ask(self,
            question: str,
            use_rag: bool = True,
            temperature: float = 0.7,
            n_context_docs: int = 5) -> str:
        """
        Ask a question about HLX.

        Args:
            question: User question
            use_rag: Whether to use RAG for context (default: True)
            temperature: LLM sampling temperature
            n_context_docs: Number of context documents to retrieve

        Returns:
            Answer string
        """
        if use_rag and self._corpus_loaded:
            prompt = self.rag.augmented_prompt(question, n_results=n_context_docs)
        else:
            prompt = question

        return self.ollama.generate(prompt, temperature=temperature)

    def explain_code(self,
                     code: str,
                     language: str = "HLXL",
                     use_rag: bool = True) -> str:
        """
        Explain HLX code.

        Args:
            code: Code to explain
            language: Language of code (HLXL, HLX-Lite, etc.)
            use_rag: Whether to use RAG for context

        Returns:
            Explanation string
        """
        question = f"Explain this {language} code:\\n\\n```{language.lower()}\\n{code}\\n```"
        return self.ask(question, use_rag=use_rag, temperature=0.3)

    def debug_code(self,
                   code: str,
                   error_message: Optional[str] = None,
                   language: str = "HLXL") -> str:
        """
        Debug HLX code and suggest fixes.

        Args:
            code: Code with issues
            error_message: Optional error message
            language: Language of code

        Returns:
            Debugging suggestions
        """
        error_section = f"\\n\\nError message: {error_message}" if error_message else ""

        question = f"""Debug this {language} code and suggest fixes:{error_section}

```{language.lower()}
{code}
```

Identify the issues and provide corrected code if possible."""

        return self.ask(question, use_rag=True, temperature=0.3)

    def review_code(self, code: str, language: str = "HLXL") -> str:
        """
        Review HLX code for best practices and potential improvements.

        Args:
            code: Code to review
            language: Language of code

        Returns:
            Code review feedback
        """
        question = f"""Review this {language} code for best practices, potential issues, and improvements:

```{language.lower()}
{code}
```

Provide specific, actionable feedback."""

        return self.ask(question, use_rag=True, temperature=0.5)

    def generate_code(self,
                      description: str,
                      language: str = "HLXL",
                      use_rag: bool = True) -> str:
        """
        Generate HLX code from description.

        Args:
            description: What the code should do
            language: Language to generate (HLXL, HLX-Lite, etc.)
            use_rag: Whether to use RAG for context

        Returns:
            Generated code
        """
        question = f"Write {language} code that: {description}\\n\\nProvide only the code with brief comments."
        return self.ask(question, use_rag=use_rag, temperature=0.7)

    def chat(self,
             messages: List[Dict[str, str]],
             temperature: float = 0.7) -> str:
        """
        Continue a conversation.

        Args:
            messages: Conversation history (list of {role, content} dicts)
            temperature: Sampling temperature

        Returns:
            Response message
        """
        return self.ollama.chat(messages, temperature=temperature)

    def load_corpus(self, corpus_file: str) -> int:
        """
        Load HLX corpus for RAG.

        Args:
            corpus_file: Path to corpus JSON file

        Returns:
            Number of documents loaded

        Raises:
            FileNotFoundError: If corpus file doesn't exist
        """
        count = self.rag.ingest_corpus(corpus_file)
        self._corpus_loaded = True
        return count

    def load_markdown(self, markdown_file: str) -> bool:
        """
        Load markdown documentation for RAG.

        Args:
            markdown_file: Path to markdown file

        Returns:
            True if successful
        """
        success = self.rag.ingest_markdown(markdown_file)
        self._corpus_loaded = True
        return success

    def get_stats(self) -> Dict:
        """
        Get brain statistics.

        Returns:
            Dict with brain stats including RAG collection info
        """
        rag_stats = self.rag.get_stats()

        return {
            "model": self.ollama.model,
            "ollama_url": self.ollama.base_url,
            "ollama_healthy": self.ollama.check_health(),
            "corpus_loaded": self._corpus_loaded,
            "rag_documents": rag_stats.get("count", 0),
            "rag_collection": rag_stats.get("name"),
        }

    def clear_corpus(self) -> bool:
        """
        Clear all corpus data from RAG.

        Returns:
            True if successful
        """
        success = self.rag.clear()
        if success:
            self._corpus_loaded = False
        return success
