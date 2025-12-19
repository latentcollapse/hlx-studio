"""
HLXL Brain - All Variants Dataset for English→HLX Translation

Extracts English→(HLXL|LC-R|LC-T|LC-B) pairs for multi-format training.

Features:
- Extracts all four format variants from corpus
- Seq2seq format with format indicator: "English text [FORMAT] → output"
- Supports HLXL, LC-R, LC-T, LC-B targets
- Balanced sampling across formats
- Train/validation split
"""

import torch
from torch.utils.data import Dataset, DataLoader
from typing import List, Tuple, Dict, Optional
from pathlib import Path
import random
import re


class AllVariantsDataset(Dataset):
    """
    Dataset for English→HLX translation with all four format variants.

    Training format:
        Input:  "English description [HLXL]" or "[LC-R]" or "[LC-T]" or "[LC-B]"
        Output: Corresponding format output
    """

    FORMAT_TAGS = ["HLXL", "LC-R", "LC-T", "LC-B"]

    def __init__(
        self,
        corpus_path: str,
        tokenizer,
        seq_length: int = 256,
        split: str = "train",
        train_ratio: float = 0.8,
        seed: int = 42,
        balance_formats: bool = True,
    ):
        """
        Initialize all-variants dataset.

        Args:
            corpus_path: Path to corpus file with all format variants
            tokenizer: LCRTokenizer instance
            seq_length: Maximum sequence length
            split: "train" or "val"
            train_ratio: Ratio of examples for training
            seed: Random seed for reproducibility
            balance_formats: Whether to balance examples across formats
        """
        self.corpus_path = Path(corpus_path)
        self.tokenizer = tokenizer
        self.seq_length = seq_length
        self.split = split
        self.train_ratio = train_ratio
        self.seed = seed
        self.balance_formats = balance_formats

        # Load examples
        self.examples_by_format = self._load_examples()

        # Create balanced dataset
        self.all_examples = self._create_balanced_dataset()

        # Split into train/val
        self.train_examples, self.val_examples = self._split_examples()

        # Select appropriate split
        self.examples = self.train_examples if split == "train" else self.val_examples

    def _load_examples(self) -> Dict[str, List[Tuple[str, str]]]:
        """Load all format variants from corpus."""
        if not self.corpus_path.exists():
            raise FileNotFoundError(f"Corpus file not found: {self.corpus_path}")

        examples = {fmt: [] for fmt in self.FORMAT_TAGS}

        with open(self.corpus_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split into example blocks (separated by blank lines)
        lines = content.split('\n')

        current_english = None
        current_formats = {}

        for line in lines:
            line = line.strip()

            # Skip headers and metadata
            if line.startswith('#') or line.startswith('**') or line.startswith('|') or line.startswith('---'):
                continue

            # English line
            if line.startswith("English:"):
                # Save previous example if complete
                if current_english and current_formats:
                    for fmt, output in current_formats.items():
                        if fmt in examples:
                            examples[fmt].append((current_english, output))

                current_english = line[8:].strip()
                current_formats = {}

            # HLXL line
            elif line.startswith("HLXL:"):
                current_formats["HLXL"] = line[5:].strip()

            # LC-R line
            elif line.startswith("LC-R:"):
                current_formats["LC-R"] = line[5:].strip()

            # LC-T line
            elif line.startswith("LC-T:"):
                current_formats["LC-T"] = line[5:].strip()

            # LC-B line
            elif line.startswith("LC-B:"):
                current_formats["LC-B"] = line[5:].strip()

        # Don't forget the last example
        if current_english and current_formats:
            for fmt, output in current_formats.items():
                if fmt in examples:
                    examples[fmt].append((current_english, output))

        # Print statistics
        total = sum(len(v) for v in examples.values())
        print(f"Loaded examples by format:")
        for fmt, exs in examples.items():
            print(f"  {fmt}: {len(exs)} examples")
        print(f"  Total: {total} examples")

        return examples

    def _create_balanced_dataset(self) -> List[Tuple[str, str, str]]:
        """Create balanced dataset with format tags."""
        all_examples = []

        if self.balance_formats:
            # Find minimum count to balance
            min_count = min(len(v) for v in self.examples_by_format.values() if v)

            for fmt, examples in self.examples_by_format.items():
                if not examples:
                    continue

                # Sample up to min_count examples
                sampled = random.Random(self.seed).sample(
                    examples,
                    min(min_count, len(examples))
                )

                for english, output in sampled:
                    all_examples.append((english, output, fmt))
        else:
            # Use all examples
            for fmt, examples in self.examples_by_format.items():
                for english, output in examples:
                    all_examples.append((english, output, fmt))

        # Shuffle
        random.Random(self.seed).shuffle(all_examples)

        return all_examples

    def _split_examples(self) -> Tuple[List, List]:
        """Split examples into train/val sets."""
        split_idx = int(len(self.all_examples) * self.train_ratio)
        train = self.all_examples[:split_idx]
        val = self.all_examples[split_idx:]

        print(f"Train examples: {len(train)}")
        print(f"Val examples: {len(val)}")

        return train, val

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        """
        Get a training example.

        Returns:
            Tuple of (input_ids, labels) tensors
            Format: "[FORMAT] English text → output"

        For autoregressive next-token prediction:
        - input_ids[i] is used to predict labels[i]
        - labels are SHIFTED by 1: labels[i] = token[i+1]
        - Input portion of labels is masked with -100
        - Only output tokens contribute to loss
        """
        english, output, fmt = self.examples[idx]

        # Create seq2seq format with format tag
        # Format: "[HLXL] Search for documents → {1000: {...}}"
        input_part = f"[{fmt}] {english} → "
        full_text = f"{input_part}{output}"

        # Tokenize full sequence
        tokens = self.tokenizer.encode(full_text, add_special_tokens=True)

        # Find where the output starts (after the arrow + space)
        # Tokenize just the input part to find the boundary
        input_tokens = self.tokenizer.encode(input_part, add_special_tokens=True)
        # output_start is the position of the FIRST output token in the original sequence
        output_start = len(input_tokens) - 1  # -1 because EOS is at the end of input_tokens

        # Truncate or pad to seq_length
        if len(tokens) > self.seq_length:
            tokens = tokens[:self.seq_length]
        else:
            tokens = tokens + [self.tokenizer.pad_token_id] * (self.seq_length - len(tokens))

        input_ids = torch.tensor(tokens, dtype=torch.long)

        # Create SHIFTED labels for next-token prediction
        # labels[i] should be what input_ids[i] should predict (i.e., the NEXT token)
        # So labels = tokens[1:] + [PAD]
        shifted_tokens = tokens[1:] + [self.tokenizer.pad_token_id]
        labels = torch.tensor(shifted_tokens, dtype=torch.long)

        # Mask the input portion of labels
        # Position i in labels corresponds to predicting token i+1
        # We want to mask predictions for positions 0 to (output_start - 1)
        # because those are predicting tokens 1 to output_start, which are all input tokens
        # We want to keep labels for positions (output_start - 1) onwards
        # because position (output_start - 1) predicts token output_start (first output token)
        labels[:output_start - 1] = -100

        # Also mask padding tokens in labels
        labels[labels == self.tokenizer.pad_token_id] = -100

        return input_ids, labels


def create_all_variants_dataloaders(
    corpus_path: str,
    tokenizer,
    batch_size: int = 32,
    seq_length: int = 256,
    train_ratio: float = 0.8,
    seed: int = 42,
    balance_formats: bool = True,
) -> Tuple[DataLoader, DataLoader]:
    """
    Create train and validation dataloaders for all-variants training.

    Args:
        corpus_path: Path to corpus file
        tokenizer: LCRTokenizer instance
        batch_size: Batch size
        seq_length: Maximum sequence length
        train_ratio: Train/val split ratio
        seed: Random seed
        balance_formats: Balance examples across formats

    Returns:
        (train_loader, val_loader) tuple
    """
    train_dataset = AllVariantsDataset(
        corpus_path=corpus_path,
        tokenizer=tokenizer,
        seq_length=seq_length,
        split="train",
        train_ratio=train_ratio,
        seed=seed,
        balance_formats=balance_formats,
    )

    val_dataset = AllVariantsDataset(
        corpus_path=corpus_path,
        tokenizer=tokenizer,
        seq_length=seq_length,
        split="val",
        train_ratio=train_ratio,
        seed=seed,
        balance_formats=balance_formats,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,
        pin_memory=True,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=True,
    )

    return train_loader, val_loader


if __name__ == "__main__":
    # Quick test
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from tokenizer import create_tokenizer

    print("Testing AllVariantsDataset...")

    tokenizer = create_tokenizer()

    train_loader, val_loader = create_all_variants_dataloaders(
        corpus_path="../corpus_all_variants.md",
        tokenizer=tokenizer,
        batch_size=4,
        seq_length=256,
    )

    print(f"\nTrain batches: {len(train_loader)}")
    print(f"Val batches: {len(val_loader)}")

    # Test one batch
    batch = next(iter(train_loader))
    input_ids, labels = batch

    print(f"\nBatch shape: {input_ids.shape}")
    print(f"\nSample decoded:")
    for i in range(min(2, len(input_ids))):
        decoded = tokenizer.decode(input_ids[i].tolist(), skip_special_tokens=False)
        print(f"  {i}: {decoded[:150]}...")
