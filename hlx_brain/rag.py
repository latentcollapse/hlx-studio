"""
RAG (Retrieval-Augmented Generation) System for HLX Corpus

Uses ChromaDB for vector storage and Ollama embeddings for semantic search.
Provides context-aware responses by retrieving relevant HLX documentation.
"""

import chromadb
from chromadb.utils import embedding_functions
import json
import os
from typing import List, Dict, Tuple, Optional


class HLXCorpusRAG:
    """RAG system for HLX documentation and code corpus."""

    def __init__(self,
                 ollama_url: str = "http://localhost:11434",
                 persist_directory: Optional[str] = None):
        """
        Initialize HLX Corpus RAG system.

        Args:
            ollama_url: Ollama server URL for embeddings
            persist_directory: Optional directory to persist ChromaDB data
        """
        self.ollama_url = ollama_url

        # Initialize ChromaDB
        if persist_directory:
            self.client = chromadb.PersistentClient(path=persist_directory)
        else:
            self.client = chromadb.Client()

        # Set up Ollama embedding function
        self.embedding_function = embedding_functions.OllamaEmbeddingFunction(
            url=f"{ollama_url}/api/embeddings",
            model_name="nomic-embed-text"
        )

        # Create or get collection
        try:
            self.collection = self.client.get_collection(
                name="hlx_corpus",
                embedding_function=self.embedding_function
            )
        except:
            self.collection = self.client.create_collection(
                name="hlx_corpus",
                embedding_function=self.embedding_function,
                metadata={"description": "HLX language corpus and documentation"}
            )

    def ingest_corpus(self, corpus_file: str) -> int:
        """
        Ingest HLX corpus from JSON file.

        Args:
            corpus_file: Path to corpus JSON file

        Returns:
            Number of documents ingested

        Raises:
            FileNotFoundError: If corpus file doesn't exist
            json.JSONDecodeError: If corpus file is invalid JSON
        """
        if not os.path.exists(corpus_file):
            raise FileNotFoundError(f"Corpus file not found: {corpus_file}")

        with open(corpus_file, 'r', encoding='utf-8') as f:
            corpus = json.load(f)

        documents = []
        metadatas = []
        ids = []

        # Handle different corpus formats
        if isinstance(corpus, dict) and "sections" in corpus:
            # Format: {"sections": [{...}]}
            for section in corpus["sections"]:
                doc_text = f"{section.get('title', 'Untitled')}\\n\\n{section.get('content', '')}"
                documents.append(doc_text)
                metadatas.append({
                    "section": section.get("id", "unknown"),
                    "title": section.get("title", "Untitled"),
                    "type": "section"
                })
                ids.append(section.get("id", f"section_{len(ids)}"))

        elif isinstance(corpus, dict) and "chapters" in corpus:
            # Format: {"chapters": [{...}]}
            for chapter in corpus["chapters"]:
                doc_text = f"Chapter: {chapter.get('name', 'Untitled')}\\n\\n{chapter.get('content', '')}"
                documents.append(doc_text)
                metadatas.append({
                    "chapter": chapter.get("id", "unknown"),
                    "name": chapter.get("name", "Untitled"),
                    "type": "chapter"
                })
                ids.append(chapter.get("id", f"chapter_{len(ids)}"))

        elif isinstance(corpus, list):
            # Format: [{...}, {...}]
            for idx, item in enumerate(corpus):
                doc_text = item.get("content", str(item))
                documents.append(doc_text)
                metadatas.append({
                    "index": idx,
                    "type": "document"
                })
                ids.append(f"doc_{idx}")

        else:
            # Fallback: treat as single document
            documents.append(json.dumps(corpus, indent=2))
            metadatas.append({"type": "raw_corpus"})
            ids.append("corpus_0")

        # Add to ChromaDB collection
        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

        return len(documents)

    def ingest_markdown(self, markdown_file: str, doc_id: Optional[str] = None) -> bool:
        """
        Ingest a markdown documentation file.

        Args:
            markdown_file: Path to markdown file
            doc_id: Optional custom document ID

        Returns:
            True if successful

        Raises:
            FileNotFoundError: If markdown file doesn't exist
        """
        if not os.path.exists(markdown_file):
            raise FileNotFoundError(f"Markdown file not found: {markdown_file}")

        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        doc_id = doc_id or os.path.basename(markdown_file)

        self.collection.add(
            documents=[content],
            metadatas=[{
                "filename": os.path.basename(markdown_file),
                "type": "markdown",
                "path": markdown_file
            }],
            ids=[doc_id]
        )

        return True

    def retrieve(self, query: str, n_results: int = 5) -> Tuple[List[str], List[Dict]]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            Tuple of (documents, metadatas)
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        documents = results["documents"][0] if results["documents"] else []
        metadatas = results["metadatas"][0] if results["metadatas"] else []

        return documents, metadatas

    def augmented_prompt(self,
                         query: str,
                         n_results: int = 5,
                         system_context: Optional[str] = None) -> str:
        """
        Build RAG prompt with retrieved context.

        Args:
            query: User query
            n_results: Number of context documents to retrieve
            system_context: Optional additional system context

        Returns:
            Augmented prompt with context
        """
        docs, metas = self.retrieve(query, n_results)

        # Build context section
        context_parts = []
        for doc, meta in zip(docs, metas):
            title = meta.get("title") or meta.get("name") or meta.get("filename", "Document")
            context_parts.append(f"## {title}\\n{doc}")

        context = "\\n\\n".join(context_parts)

        # Build full prompt
        system_section = f"\\n\\n{system_context}\\n" if system_context else ""

        prompt = f"""You are an HLX programming expert. Use the following documentation to answer the question.
{system_section}
# HLX Documentation

{context}

# Question

{query}

# Answer

Provide a precise answer based on the documentation above. If the documentation doesn't contain enough information, say so."""

        return prompt

    def clear(self) -> bool:
        """
        Clear all documents from the collection.

        Returns:
            True if successful
        """
        try:
            self.client.delete_collection("hlx_corpus")
            self.collection = self.client.create_collection(
                name="hlx_corpus",
                embedding_function=self.embedding_function,
                metadata={"description": "HLX language corpus and documentation"}
            )
            return True
        except:
            return False

    def count(self) -> int:
        """
        Count number of documents in collection.

        Returns:
            Document count
        """
        return self.collection.count()

    def get_stats(self) -> Dict:
        """
        Get collection statistics.

        Returns:
            Dict with collection stats
        """
        return {
            "name": self.collection.name,
            "count": self.collection.count(),
            "metadata": self.collection.metadata
        }
