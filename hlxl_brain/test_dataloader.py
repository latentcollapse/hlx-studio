#!/usr/bin/env python3
"""Quick test of seq2seq dataloader"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from tokenizer import create_tokenizer
from data_seq2seq import Seq2SeqDataset

# Create tokenizer
tokenizer = create_tokenizer()
print(f"✓ Tokenizer: {tokenizer.vocab_size} tokens")
print()

# Test dataloader
dataset = Seq2SeqDataset(
    corpus_path="corpus_combined_phase4.md",
    tokenizer=tokenizer,
    seq_length=256,
    split="train",
    train_ratio=0.8,
)

print(f"✓ Dataset: {len(dataset)} train examples")
print()

# Show first 5 examples
print("First 5 training examples:")
print("="*80)
for i in range(min(5, len(dataset))):
    tokens = dataset[i]
    text = tokenizer.decode(tokens.tolist(), skip_special_tokens=False)
    print(f"\n#{i+1}:")
    print(text[:200] + "..." if len(text) > 200 else text)
print()
print("="*80)
