#!/usr/bin/env python3
"""
Test script for HLX Brain components.

Tests Ollama client, RAG system, and unified brain interface.
"""

import sys
sys.path.insert(0, '/home/matt/hlx-dev-studio')

from hlx_brain import OllamaClient, HLXCorpusRAG, HLXBrain


def test_ollama_client():
    """Test Ollama client basic functionality."""
    print("\\n=== Testing Ollama Client ===")

    client = OllamaClient()

    # Check health
    print(f"Server healthy: {client.check_health()}")

    # List models
    print("\\nAvailable models:")
    models = client.list_models()
    for model in models:
        print(f"  - {model.get('name', 'unknown')}")

    # Simple generation test
    print("\\nTesting generation (simple math)...")
    response = client.generate("What is 5 + 7?", temperature=0.1)
    print(f"Response: {response[:200]}")

    print("\\n✓ Ollama client tests passed")


def test_rag_system():
    """Test RAG system basic functionality."""
    print("\\n=== Testing RAG System ===")

    rag = HLXCorpusRAG()

    # Check stats
    stats = rag.get_stats()
    print(f"Collection: {stats['name']}, Documents: {stats['count']}")

    # Test with simple document
    print("\\nAdding test document...")
    rag.collection.add(
        documents=["HLX is a deterministic, content-addressed language. The ls.collapse operation stores values and returns handles."],
        ids=["test_doc_1"],
        metadatas=[{"type": "test"}]
    )

    # Test retrieval
    print("Testing retrieval...")
    docs, metas = rag.retrieve("What is ls.collapse?", n_results=1)
    print(f"Retrieved {len(docs)} documents")
    if docs:
        print(f"Document: {docs[0][:100]}...")

    # Test augmented prompt
    print("\\nTesting augmented prompt generation...")
    prompt = rag.augmented_prompt("What is ls.collapse?", n_results=1)
    print(f"Prompt length: {len(prompt)} characters")

    print("\\n✓ RAG system tests passed")


def test_brain():
    """Test unified HLX Brain interface."""
    print("\\n=== Testing HLX Brain ===")

    brain = HLXBrain()

    # Check stats
    stats = brain.get_stats()
    print("Brain stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Test without RAG
    print("\\nTesting ask (without RAG)...")
    answer = brain.ask("What is 10 + 15?", use_rag=False, temperature=0.1)
    print(f"Answer: {answer[:150]}...")

    # Add test corpus
    print("\\nAdding test HLX documentation...")
    brain.rag.collection.add(
        documents=[
            "The ls.collapse operation takes a value and stores it in the content-addressed store, returning a unique handle.",
            "The ls.resolve operation takes a handle and retrieves the original value from the store.",
            "HLXL is the high-level syntax for HLX. It compiles to HLX-Lite, which is the canonical intermediate form."
        ],
        ids=["doc_collapse", "doc_resolve", "doc_hlxl"],
        metadatas=[
            {"type": "operation", "name": "collapse"},
            {"type": "operation", "name": "resolve"},
            {"type": "language", "name": "hlxl"}
        ]
    )
    brain._corpus_loaded = True

    # Test with RAG
    print("\\nTesting ask (with RAG)...")
    answer = brain.ask("What does ls.collapse do?", use_rag=True, temperature=0.3)
    print(f"Answer: {answer[:200]}...")

    # Test code explanation
    print("\\nTesting explain_code...")
    code = """program test {
    block main() {
        let value = {14: {@0: 42}};
        let handle = ls.collapse value;
        return handle;
    }
}"""
    explanation = brain.explain_code(code, use_rag=False)
    print(f"Explanation: {explanation[:200]}...")

    print("\\n✓ HLX Brain tests passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("HLX Brain Test Suite")
    print("=" * 60)

    try:
        test_ollama_client()
        test_rag_system()
        test_brain()

        print("\\n" + "=" * 60)
        print("ALL TESTS PASSED")
        print("=" * 60)

    except Exception as e:
        print(f"\\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
