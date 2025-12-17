#!/usr/bin/env python3
"""
Load HLX corpus into the brain's RAG system.

Ingests all available HLX documentation for context-aware assistance.
"""

import sys
sys.path.insert(0, '/home/matt/hlx-dev-studio')

from hlx_brain import HLXBrain


def main():
    print("Loading HLX corpus into brain...")

    brain = HLXBrain(persist_directory="/home/matt/hlx-dev-studio/.chromadb")

    corpus_files = [
        "/home/matt/hlx-dev-studio/corpus/HLX_CANONICAL_CORPUS_v1.0.0.json",
        "/home/matt/hlx-dev-studio/corpus/HLX_CHAPTER_CORE_v1.0.0.json",
        "/home/matt/hlx-dev-studio/corpus/HLX_CHAPTER_RUNTIME_v1.0.0.json",
        "/home/matt/hlx-dev-studio/corpus/HLX_CHAPTER_EXTENSIONS_v1.0.0.json",
        "/home/matt/hlx-dev-studio/HLX_BOOTSTRAP_CODEX_v1.json"
    ]

    total_docs = 0

    for corpus_file in corpus_files:
        try:
            print(f"\\nLoading {corpus_file.split('/')[-1]}...")
            count = brain.load_corpus(corpus_file)
            print(f"  ✓ Loaded {count} documents")
            total_docs += count
        except Exception as e:
            print(f"  ⚠ Failed: {e}")

    print(f"\\n{'='*60}")
    print(f"Total documents loaded: {total_docs}")
    print(f"{'='*60}")

    # Test retrieval
    print("\\nTesting retrieval: 'What is ls.collapse?'")
    docs, metas = brain.rag.retrieve("What is ls.collapse?", n_results=3)
    for i, (doc, meta) in enumerate(zip(docs, metas), 1):
        print(f"\\n{i}. {meta.get('title', meta.get('section', 'Unknown'))}:")
        print(f"   {doc[:150]}...")

    # Test RAG query
    print("\\n\\nTesting RAG query...")
    answer = brain.ask("Explain the ls.collapse operation in detail.", use_rag=True, temperature=0.3)
    print(f"Answer: {answer[:500]}...")

    print("\\n✓ Corpus loaded successfully!")
    print(f"\\nStats: {brain.get_stats()}")


if __name__ == "__main__":
    main()
