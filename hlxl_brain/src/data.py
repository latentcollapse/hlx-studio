"""
HLXL Brain - LC-R Dataset

Character-level dataset for training on LC-R corpus.

Features:
- Load corpus from markdown file
- Sequence chunking with stride
- Padding/truncation
- Train/validation split
- Efficient batching

Target: Support 164 corpus examples for training.
"""

import torch
from torch.utils.data import Dataset, DataLoader
from typing import List, Tuple, Optional
from pathlib import Path
import random


class LCRDataset(Dataset):
    """
    Character-level dataset for LC-R text sequences.

    Loads corpus examples and creates training sequences with
    sliding window approach.
    """

    def __init__(
        self,
        corpus_path: str,
        tokenizer,
        seq_length: int = 128,
        stride: int = 64,
        split: str = "train",
        train_ratio: float = 0.8,
        seed: int = 42,
    ):
        """
        Initialize LC-R dataset.

        Args:
            corpus_path: Path to LC-R corpus file
            tokenizer: LCRTokenizer instance
            seq_length: Maximum sequence length
            stride: Stride for sliding window
            split: "train" or "val"
            train_ratio: Ratio of examples for training
            seed: Random seed for reproducibility
        """
        self.corpus_path = Path(corpus_path)
        self.tokenizer = tokenizer
        self.seq_length = seq_length
        self.stride = stride
        self.split = split
        self.train_ratio = train_ratio
        self.seed = seed

        # Load and split corpus
        self.examples = self._load_corpus()
        self.train_examples, self.val_examples = self._split_corpus()

        # Create sequences with sliding window
        self.sequences = self._create_sequences()

    def _load_corpus(self) -> List[str]:
        """Load LC-R examples from corpus file."""
        if not self.corpus_path.exists():
            raise FileNotFoundError(f"Corpus file not found: {self.corpus_path}")

        examples = []
        with open(self.corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("LC-R: "):
                    lc_r_value = line[6:].strip()
                    if lc_r_value:
                        examples.append(lc_r_value)

        if not examples:
            raise ValueError(f"No LC-R examples found in {self.corpus_path}")

        return examples

    def _split_corpus(self) -> Tuple[List[str], List[str]]:
        """Split corpus into train/val sets."""
        # Shuffle with fixed seed for reproducibility
        random.seed(self.seed)
        shuffled = self.examples.copy()
        random.shuffle(shuffled)

        # Split
        split_idx = int(len(shuffled) * self.train_ratio)
        train = shuffled[:split_idx]
        val = shuffled[split_idx:]

        return train, val

    def _create_sequences(self) -> List[List[int]]:
        """
        Create training sequences with sliding window.

        For each example, extract overlapping sequences of length seq_length
        using stride. This increases dataset size and helps model learn
        local patterns.
        """
        sequences = []

        # Select split
        examples = self.train_examples if self.split == "train" else self.val_examples

        for example in examples:
            # Encode example
            token_ids = self.tokenizer.encode(example, add_special_tokens=True)

            # If example is shorter than seq_length, just use it as-is
            if len(token_ids) <= self.seq_length:
                sequences.append(token_ids)
            else:
                # Sliding window to create multiple sequences
                for start_idx in range(0, len(token_ids) - self.seq_length + 1, self.stride):
                    end_idx = start_idx + self.seq_length
                    sequence = token_ids[start_idx:end_idx]
                    sequences.append(sequence)

        return sequences

    def __len__(self) -> int:
        """Return number of sequences in dataset."""
        return len(self.sequences)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Get a single training example.

        Returns:
            input_ids: Input sequence (seq_length,)
            labels: Target sequence (seq_length,) - shifted by 1
        """
        sequence = self.sequences[idx]

        # Pad if needed
        if len(sequence) < self.seq_length:
            padding = [self.tokenizer.pad_token_id] * (self.seq_length - len(sequence))
            sequence = sequence + padding

        # Convert to tensors
        sequence_tensor = torch.tensor(sequence, dtype=torch.long)

        # For language modeling: input = sequence, labels = sequence shifted by 1
        # input:  [BOS, tok1, tok2, tok3, ...]
        # labels: [tok1, tok2, tok3, EOS, ...]
        input_ids = sequence_tensor[:-1]  # Remove last token
        labels = sequence_tensor[1:]      # Remove first token

        return input_ids, labels

    def get_stats(self) -> dict:
        """Get dataset statistics."""
        train_seqs = len(LCRDataset(
            self.corpus_path,
            self.tokenizer,
            self.seq_length,
            self.stride,
            split="train",
            train_ratio=self.train_ratio,
            seed=self.seed,
        ).sequences)

        val_seqs = len(LCRDataset(
            self.corpus_path,
            self.tokenizer,
            self.seq_length,
            self.stride,
            split="val",
            train_ratio=self.train_ratio,
            seed=self.seed,
        ).sequences)

        return {
            "total_examples": len(self.examples),
            "train_examples": len(self.train_examples),
            "val_examples": len(self.val_examples),
            "train_sequences": train_seqs,
            "val_sequences": val_seqs,
            "seq_length": self.seq_length,
            "stride": self.stride,
        }


def create_dataloaders(
    corpus_path: str,
    tokenizer,
    batch_size: int = 32,
    seq_length: int = 128,
    stride: int = 64,
    train_ratio: float = 0.8,
    num_workers: int = 0,
    seed: int = 42,
) -> Tuple[DataLoader, DataLoader]:
    """
    Create train and validation dataloaders.

    Args:
        corpus_path: Path to LC-R corpus file
        tokenizer: LCRTokenizer instance
        batch_size: Batch size for training
        seq_length: Maximum sequence length
        stride: Stride for sliding window
        train_ratio: Ratio of examples for training
        num_workers: Number of workers for data loading
        seed: Random seed

    Returns:
        train_loader, val_loader
    """
    train_dataset = LCRDataset(
        corpus_path=corpus_path,
        tokenizer=tokenizer,
        seq_length=seq_length,
        stride=stride,
        split="train",
        train_ratio=train_ratio,
        seed=seed,
    )

    val_dataset = LCRDataset(
        corpus_path=corpus_path,
        tokenizer=tokenizer,
        seq_length=seq_length,
        stride=stride,
        split="val",
        train_ratio=train_ratio,
        seed=seed,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True if torch.cuda.is_available() else False,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True if torch.cuda.is_available() else False,
    )

    return train_loader, val_loader


if __name__ == "__main__":
    # Quick test
    from tokenizer import create_tokenizer

    tokenizer = create_tokenizer()
    corpus_path = "/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md"

    # Create dataset
    dataset = LCRDataset(
        corpus_path=corpus_path,
        tokenizer=tokenizer,
        seq_length=128,
        stride=64,
        split="train",
    )

    print(f"✓ Dataset created: {len(dataset)} sequences")
    print(f"✓ Statistics: {dataset.get_stats()}")

    # Test batching
    train_loader, val_loader = create_dataloaders(
        corpus_path=corpus_path,
        tokenizer=tokenizer,
        batch_size=4,
    )

    print(f"✓ Train batches: {len(train_loader)}")
    print(f"✓ Val batches: {len(val_loader)}")

    # Test single batch
    input_ids, labels = next(iter(train_loader))
    print(f"✓ Batch shapes: input {input_ids.shape}, labels {labels.shape}")

    print(f"\n✓ Dataset ready for training")
