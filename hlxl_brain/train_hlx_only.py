#!/usr/bin/env python3
"""
Train tiny brain as HLX-only execution engine (NO English).
This creates a pure HLX-fluent model for token-efficient execution.

Purpose:
- Wipe all English understanding from tiny 492K brain
- Train exclusively on HLX formats (HLXL, LC-R, LC-T, LC-B)
- Create ultra-efficient execution engine
- Maximize HLX fluency with zero English contamination

Usage:
    python3 train_hlx_only.py --epochs 100 --batch-size 16 --lr 5e-4
"""

import argparse
import os
import sys
from datetime import datetime

import torch
from torch.utils.data import Dataset, DataLoader, random_split

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from model import HLXLTransformer
from tokenizer import CharTokenizer
from trainer import Trainer


class HLXOnlyDataset(Dataset):
    """Dataset containing ONLY HLX formats - zero English."""

    def __init__(self, corpus_path: str, tokenizer: CharTokenizer, seq_length: int = 256):
        self.corpus_path = corpus_path
        self.tokenizer = tokenizer
        self.seq_length = seq_length
        self.examples = self._load_hlx_only()

        print(f"Loaded {len(self.examples)} HLX-only examples (NO English)")

    def _load_hlx_only(self):
        """Load ONLY HLX format lines - filter out all English."""
        examples = []

        with open(self.corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                # ONLY accept HLX formats
                if line.startswith("HLXL:"):
                    hlx_code = line[5:].strip()
                    if hlx_code:
                        examples.append(hlx_code)

                elif line.startswith("LC-R:"):
                    lc_r_code = line[5:].strip()
                    if lc_r_code:
                        examples.append(lc_r_code)

                elif line.startswith("LC-T:"):
                    lc_t_code = line[5:].strip()
                    if lc_t_code:
                        examples.append(lc_t_code)

                elif line.startswith("LC-B:"):
                    lc_b_code = line[5:].strip()
                    if lc_b_code:
                        examples.append(lc_b_code)

                # Explicitly reject English lines
                elif line.startswith("English:") or line.startswith("**English:**"):
                    continue  # Skip all English

        return examples

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        """Returns (input_ids, labels) for autoregressive training."""
        hlx_text = self.examples[idx]

        # Encode with special tokens
        tokens = self.tokenizer.encode(hlx_text, add_special_tokens=True)

        # Pad or truncate to seq_length
        if len(tokens) > self.seq_length:
            tokens = tokens[:self.seq_length]
        else:
            tokens = tokens + [self.tokenizer.pad_token_id] * (self.seq_length - len(tokens))

        input_ids = torch.tensor(tokens, dtype=torch.long)
        labels = torch.tensor(tokens, dtype=torch.long)

        return input_ids, labels


def create_hlx_only_dataloaders(
    corpus_path: str,
    tokenizer: CharTokenizer,
    batch_size: int = 16,
    seq_length: int = 256,
    train_ratio: float = 0.8,
):
    """Create train/val dataloaders for HLX-only data."""

    # Load full dataset
    full_dataset = HLXOnlyDataset(corpus_path, tokenizer, seq_length)

    # Split into train/val
    train_size = int(len(full_dataset) * train_ratio)
    val_size = len(full_dataset) - train_size

    train_dataset, val_dataset = random_split(
        full_dataset,
        [train_size, val_size],
        generator=torch.Generator().manual_seed(42)
    )

    print(f"Train: {len(train_dataset)} examples, Val: {len(val_dataset)} examples")

    # Create dataloaders
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


def main():
    parser = argparse.ArgumentParser(description="Train HLX-only execution engine")

    # Data
    parser.add_argument("--corpus-path", type=str, default="corpus_hlx_only.md",
                        help="Path to HLX-only corpus (no English)")

    # Training
    parser.add_argument("--epochs", type=int, default=100,
                        help="Number of training epochs (default: 100)")
    parser.add_argument("--batch-size", type=int, default=16,
                        help="Batch size (default: 16)")
    parser.add_argument("--seq-length", type=int, default=256,
                        help="Sequence length (default: 256)")
    parser.add_argument("--lr", type=float, default=5e-4,
                        help="Learning rate (default: 5e-4)")
    parser.add_argument("--train-ratio", type=float, default=0.8,
                        help="Train/val split ratio (default: 0.8)")

    # Model (tiny architecture - 492K params)
    parser.add_argument("--d-model", type=int, default=128,
                        help="Model dimension (default: 128 for tiny)")
    parser.add_argument("--num-layers", type=int, default=2,
                        help="Number of layers (default: 2 for tiny)")
    parser.add_argument("--num-heads", type=int, default=4,
                        help="Number of attention heads (default: 4)")
    parser.add_argument("--dim-feedforward", type=int, default=512,
                        help="FFN dimension (default: 512)")
    parser.add_argument("--dropout", type=float, default=0.1,
                        help="Dropout rate (default: 0.1)")

    # Checkpointing
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints",
                        help="Checkpoint directory")
    parser.add_argument("--resume-from", type=str, default=None,
                        help="Resume from checkpoint (if retraining existing tiny brain)")

    args = parser.parse_args()

    print("=" * 80)
    print("HLX-ONLY TRAINING: TINY BRAIN EXECUTION ENGINE")
    print("=" * 80)
    print(f"Purpose: Create pure HLX-fluent model with ZERO English")
    print(f"Target: Ultra-efficient execution engine for token savings")
    print(f"Architecture: Tiny ({args.d_model}d, {args.num_layers}L, {args.num_heads}H)")
    print(f"Corpus: {args.corpus_path} (HLX formats only)")
    print(f"Epochs: {args.epochs}")
    print("=" * 80)

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # Create tokenizer
    print("\nInitializing tokenizer...")
    tokenizer = CharTokenizer()
    print(f"Vocabulary size: {tokenizer.vocab_size}")

    # Create dataloaders
    print("\nLoading HLX-only corpus...")
    train_loader, val_loader = create_hlx_only_dataloaders(
        corpus_path=args.corpus_path,
        tokenizer=tokenizer,
        batch_size=args.batch_size,
        seq_length=args.seq_length,
        train_ratio=args.train_ratio,
    )

    # Create model (tiny architecture)
    print("\nCreating tiny brain model...")
    model = HLXLTransformer(
        vocab_size=tokenizer.vocab_size,
        d_model=args.d_model,
        nhead=args.num_heads,
        num_layers=args.num_layers,
        dim_feedforward=args.dim_feedforward,
        dropout=args.dropout,
        max_seq_length=args.seq_length,
    ).to(device)

    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total parameters: {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,}")

    # Verify tiny size (~492K)
    if total_params > 600_000:
        print(f"\nWARNING: Model has {total_params:,} params (expected ~492K for tiny)")
        print("This may not be the tiny brain!")

    # Resume from checkpoint if specified
    start_epoch = 1
    if args.resume_from:
        print(f"\nResuming from checkpoint: {args.resume_from}")
        checkpoint = torch.load(args.resume_from, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        start_epoch = checkpoint.get('epoch', 0) + 1
        print(f"Resuming from epoch {start_epoch}")
        print("NOTE: This will OVERWRITE any English knowledge with pure HLX")

    # Create trainer
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        device=device,
        learning_rate=args.lr,
        checkpoint_dir=args.checkpoint_dir,
    )

    # Training loop
    print("\n" + "=" * 80)
    print("STARTING HLX-ONLY TRAINING")
    print("=" * 80)
    print(f"Training from epoch {start_epoch} to {args.epochs}")
    print("This will create a pure HLX execution engine with NO English capability")
    print("=" * 80 + "\n")

    best_val_loss = float('inf')

    for epoch in range(start_epoch, args.epochs + 1):
        print(f"\n{'=' * 80}")
        print(f"EPOCH {epoch}/{args.epochs}")
        print(f"{'=' * 80}")

        # Train
        train_loss = trainer.train_epoch()
        print(f"Train Loss: {train_loss:.4f}")

        # Validate
        val_loss = trainer.validate()
        print(f"Val Loss: {val_loss:.4f}")

        # Save periodic checkpoint
        if epoch % 10 == 0:
            checkpoint_path = os.path.join(
                args.checkpoint_dir,
                f"tiny_hlx_only_epoch{epoch}.pt"
            )
            trainer.save_checkpoint(checkpoint_path)
            print(f"Saved checkpoint: {checkpoint_path}")

        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_path = os.path.join(
                args.checkpoint_dir,
                f"tiny_hlx_only_BEST_epoch{epoch}.pt"
            )
            trainer.save_checkpoint(best_path)
            print(f"NEW BEST! Saved: {best_path}")

    # Save final model
    final_path = os.path.join(
        args.checkpoint_dir,
        f"tiny_hlx_only_FINAL_epoch{args.epochs}.pt"
    )
    trainer.save_checkpoint(final_path)

    print("\n" + "=" * 80)
    print("HLX-ONLY TRAINING COMPLETE")
    print("=" * 80)
    print(f"Final checkpoint: {final_path}")
    print(f"Best validation loss: {best_val_loss:.4f}")
    print("\nTiny brain is now fluent in pure HLX with ZERO English capability")
    print("Ready to use as token-efficient execution engine!")
    print("=" * 80)


if __name__ == "__main__":
    main()
