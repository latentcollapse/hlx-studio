"""
HLXL Brain - Seq2Seq Dataset for English→HLX Translation

Properly extracts English→(HLXL|LC-R) pairs for translation training.

Features:
- Extracts paired examples from corpus
- Seq2seq format: "English text → HLX output"
- Handles both HLXL and LC-R targets
- Train/validation split
- Efficient batching
"""

import torch
from torch.utils.data import Dataset, DataLoader
from typing import List, Tuple, Dict
from pathlib import Path
import random
import re


class Seq2SeqDataset(Dataset):
    """
    Seq2seq dataset for English→HLX translation.

    Training format:
        Input:  "English description"
        Output: "HLXL code" or "LC-R glyphs"
    """

    def __init__(
        self,
        corpus_path: str,
        tokenizer,
        seq_length: int = 256,
        split: str = "train",
        train_ratio: float = 0.8,
        seed: int = 42,
    ):
        """
        Initialize seq2seq dataset.

        Args:
            corpus_path: Path to corpus file
            tokenizer: LCRTokenizer instance
            seq_length: Maximum sequence length
            split: "train" or "val"
            train_ratio: Ratio of examples for training
            seed: Random seed for reproducibility
        """
        self.corpus_path = Path(corpus_path)
        self.tokenizer = tokenizer
        self.seq_length = seq_length
        self.split = split
        self.train_ratio = train_ratio
        self.seed = seed

        # Load and split examples
        self.pairs = self._load_pairs()
        self.train_pairs, self.val_pairs = self._split_pairs()

        # Select appropriate split
        self.examples = self.train_pairs if split == "train" else self.val_pairs

    def _load_pairs(self) -> List[Tuple[str, str]]:
        """Load English→HLX pairs from corpus."""
        if not self.corpus_path.exists():
            raise FileNotFoundError(f"Corpus file not found: {self.corpus_path}")

        pairs = []

        with open(self.corpus_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Look for English lines (from Phase 4)
            if line.startswith("English:") or line.startswith("**English:**"):
                english = line.replace("English:", "").replace("**English:**", "").strip()

                # Find corresponding HLX output (HLXL or LC-R)
                hlx_output = None
                j = i + 1

                while j < len(lines) and j < i + 20:  # Look ahead max 20 lines
                    next_line = lines[j].strip()

                    # Phase 4 format: LC-R in code blocks
                    if next_line.startswith("**LC-R:**") or next_line == "```":
                        # Extract from code block
                        if lines[j+1].strip():
                            hlx_output = lines[j+1].strip()
                            if hlx_output.startswith("```"):
                                hlx_output = None
                            break

                    # Standard format: HLXL: or LC-R: lines
                    if next_line.startswith("HLXL:"):
                        hlx_output = next_line[5:].strip()
                        break

                    if next_line.startswith("LC-R:"):
                        hlx_output = next_line[5:].strip()
                        break

                    j += 1

                if english and hlx_output:
                    pairs.append((english, hlx_output))

            # Also extract HLXL pairs without English (for pure HLX learning)
            elif line.startswith("HLXL:"):
                hlxl = line[5:].strip()
                # Look for LC-R on next line
                if i + 1 < len(lines) and lines[i+1].strip().startswith("LC-R:"):
                    lcr = lines[i+1].strip()[5:].strip()
                    # Add HLXL→LC-R pair
                    if hlxl and lcr:
                        pairs.append((hlxl, lcr))

            i += 1

        if not pairs:
            raise ValueError(f"No translation pairs found in {self.corpus_path}")

        print(f"✓ Loaded {len(pairs)} translation pairs")
        return pairs

    def _split_pairs(self) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        """Split pairs into train/val sets."""
        random.seed(self.seed)
        shuffled = self.pairs.copy()
        random.shuffle(shuffled)

        split_idx = int(len(shuffled) * self.train_ratio)
        train = shuffled[:split_idx]
        val = shuffled[split_idx:]

        return train, val

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        """
        Get a training example as seq2seq format.

        Returns:
            Tuple of (input_ids, labels) tensors, both of shape (seq_length,)
            input_ids: [BOS] input text [→] output text [EOS] [PAD] ...
            labels: same as input_ids (for next-token prediction)
        """
        input_text, output_text = self.examples[idx]

        # Create seq2seq format: "input → output"
        # Using → (U+2192) as separator token
        full_text = f"{input_text} → {output_text}"

        # Tokenize
        tokens = self.tokenizer.encode(full_text, add_special_tokens=True)

        # Truncate or pad to seq_length
        if len(tokens) > self.seq_length:
            tokens = tokens[:self.seq_length]
        else:
            # Pad with PAD token
            tokens = tokens + [self.tokenizer.pad_token_id] * (self.seq_length - len(tokens))

        # For language modeling, input_ids and labels are the same
        # The model learns next-token prediction: given tokens[0:i], predict tokens[i+1]
        input_ids = torch.tensor(tokens, dtype=torch.long)
        labels = torch.tensor(tokens, dtype=torch.long)

        return input_ids, labels


def create_seq2seq_dataloaders(
    corpus_path: str,
    tokenizer,
    batch_size: int = 32,
    seq_length: int = 256,
    train_ratio: float = 0.8,
    seed: int = 42,
) -> Tuple[DataLoader, DataLoader]:
    """
    Create train and validation dataloaders for seq2seq training.

    Args:
        corpus_path: Path to corpus file
        tokenizer: LCRTokenizer instance
        batch_size: Batch size
        seq_length: Maximum sequence length
        train_ratio: Train/val split ratio
        seed: Random seed

    Returns:
        (train_loader, val_loader) tuple
    """
    train_dataset = Seq2SeqDataset(
        corpus_path=corpus_path,
        tokenizer=tokenizer,
        seq_length=seq_length,
        split="train",
        train_ratio=train_ratio,
        seed=seed,
    )

    val_dataset = Seq2SeqDataset(
        corpus_path=corpus_path,
        tokenizer=tokenizer,
        seq_length=seq_length,
        split="val",
        train_ratio=train_ratio,
        seed=seed,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,  # Single-threaded for simplicity
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
