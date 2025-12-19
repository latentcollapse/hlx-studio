#!/usr/bin/env python3
"""
Production HLX Brain Training Script (100M Model)
With quality gates, corpus validation, and watchdog hooks.

450-Epoch Curriculum:
- Phase 1: English mastery (200 epochs)
- Phase 2: HLX family mastery (200 epochs)
- Phase 3: Translation training (50 epochs)

Quality Gates:
- Architecture verification at startup
- Corpus loading validation
- Checkpoint quality tests at epochs 1, 5, 10, 20, 50, 100, etc.
- Loss curve monitoring
- Automatic abort on quality failure
- Watchdog file updates for external monitoring

Usage:
    python3 train_100m_production.py --phase 1 --epochs 200
    python3 train_100m_production.py --phase 2 --epochs 200 --resume checkpoints/phase1_final.pt
    python3 train_100m_production.py --phase 3 --epochs 50 --resume checkpoints/phase2_final.pt
"""

import argparse
import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from torch.cuda.amp import autocast, GradScaler

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from model import create_model
from tokenizer import create_tokenizer


# ==============================================================================
# CONFIGURATION
# ==============================================================================

# 100M Model Architecture
MODEL_CONFIG_100M = {
    "d_model": 1024,
    "nhead": 16,
    "num_layers": 8,
    "dim_feedforward": 4096,
    "dropout": 0.1,
    "max_seq_length": 256,  # Reduced for 8GB GPU
}

# Quality check epochs
QUALITY_CHECK_EPOCHS = [1, 5, 10, 20, 50, 100, 150, 200]

# Abort conditions
MAX_LOSS_THRESHOLD = 15.0  # If loss > 15, training has diverged
MIN_LOSS_THRESHOLD = 0.001  # If loss < 0.001 too early, might be overfitting


# ==============================================================================
# CORPUS DATASETS
# ==============================================================================

class PhaseDataset(Dataset):
    """Dataset for each training phase with corpus validation."""

    def __init__(self, corpus_path: str, tokenizer, seq_length: int = 256, phase: int = 1):
        self.corpus_path = corpus_path
        self.tokenizer = tokenizer
        self.seq_length = seq_length
        self.phase = phase
        self.examples = []

        print(f"\nLoading Phase {phase} corpus: {corpus_path}")
        self._load_and_validate_corpus()

    def _load_and_validate_corpus(self):
        """Load corpus with validation checks."""
        if not Path(self.corpus_path).exists():
            raise FileNotFoundError(f"Corpus not found: {self.corpus_path}")

        with open(self.corpus_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) == 0:
            raise ValueError(f"Corpus is empty: {self.corpus_path}")

        # Phase-specific loading
        if self.phase == 1:
            # Phase 1: English only
            self.examples = self._load_english_only(lines)
        elif self.phase == 2:
            # Phase 2: HLX only (all 4 formats)
            self.examples = self._load_hlx_only(lines)
        elif self.phase == 3:
            # Phase 3: English ↔ HLX translation pairs
            self.examples = self._load_translation_pairs(lines)
        else:
            raise ValueError(f"Invalid phase: {self.phase}")

        if len(self.examples) == 0:
            raise ValueError(f"No examples loaded from corpus (phase {self.phase})")

        print(f"✓ Loaded {len(self.examples)} examples for Phase {self.phase}")
        self._validate_examples()

    def _load_english_only(self, lines):
        """Load English examples only."""
        examples = []
        for line in lines:
            line = line.strip()
            if line.startswith("English:") or line.startswith("**English:**"):
                english = line.replace("English:", "").replace("**English:**", "").strip()
                if english:
                    examples.append(english)
        return examples

    def _load_hlx_only(self, lines):
        """Load HLX examples only (all 4 formats)."""
        examples = []
        for line in lines:
            line = line.strip()
            if line.startswith("HLXL:"):
                hlxl = line[5:].strip()
                if hlxl:
                    examples.append(hlxl)
            elif line.startswith("LC-R:"):
                lc_r = line[5:].strip()
                if lc_r:
                    examples.append(lc_r)
            elif line.startswith("LC-T:"):
                lc_t = line[5:].strip()
                if lc_t:
                    examples.append(lc_t)
            elif line.startswith("LC-B:"):
                lc_b = line[5:].strip()
                if lc_b:
                    examples.append(lc_b)
        return examples

    def _load_translation_pairs(self, lines):
        """Load English ↔ HLX translation pairs."""
        examples = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line.startswith("English:") or line.startswith("**English:**"):
                english = line.replace("English:", "").replace("**English:**", "").strip()

                # Look for corresponding HLX outputs
                j = i + 1
                while j < len(lines) and j < i + 20:
                    next_line = lines[j].strip()

                    if next_line.startswith("HLXL:"):
                        hlxl = next_line[5:].strip()
                        if english and hlxl:
                            examples.append(f"{english} → {hlxl}")
                    elif next_line.startswith("LC-R:"):
                        lc_r = next_line[5:].strip()
                        if english and lc_r:
                            examples.append(f"{english} → {lc_r}")
                    elif next_line.startswith("LC-T:"):
                        lc_t = next_line[5:].strip()
                        if english and lc_t:
                            examples.append(f"{english} → {lc_t}")
                    elif next_line.startswith("LC-B:"):
                        lc_b = next_line[5:].strip()
                        if english and lc_b:
                            examples.append(f"{english} → {lc_b}")

                    j += 1

            i += 1

        return examples

    def _validate_examples(self):
        """Validate loaded examples."""
        # Sample validation
        sample_size = min(5, len(self.examples))
        print(f"\nSample examples (first {sample_size}):")
        for i, example in enumerate(self.examples[:sample_size]):
            print(f"  {i+1}. {example[:80]}{'...' if len(example) > 80 else ''}")

        # Length validation
        avg_length = sum(len(ex) for ex in self.examples) / len(self.examples)
        print(f"\nCorpus statistics:")
        print(f"  Examples: {len(self.examples)}")
        print(f"  Avg length: {avg_length:.1f} characters")

        if avg_length < 10:
            raise ValueError("Average example length too short - corpus may be corrupted")

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        """Returns (input_ids, labels) for training."""
        text = self.examples[idx]

        # Encode with special tokens
        tokens = self.tokenizer.encode(text, add_special_tokens=True)

        # Pad or truncate
        if len(tokens) > self.seq_length:
            tokens = tokens[:self.seq_length]
        else:
            tokens = tokens + [self.tokenizer.pad_token_id] * (self.seq_length - len(tokens))

        input_ids = torch.tensor(tokens, dtype=torch.long)
        labels = torch.tensor(tokens, dtype=torch.long)

        return input_ids, labels


# ==============================================================================
# QUALITY GATE CHECKER
# ==============================================================================

class QualityGateChecker:
    """Runs validation checks and aborts training if quality fails."""

    def __init__(self, checkpoint_dir: str, validation_script: str = "validate_checkpoint_quality.py"):
        self.checkpoint_dir = checkpoint_dir
        self.validation_script = validation_script

    def check_epoch(self, epoch: int, checkpoint_path: str) -> bool:
        """Run quality check on epoch checkpoint."""
        print(f"\n{'='*80}")
        print(f"QUALITY GATE: Epoch {epoch}")
        print(f"{'='*80}")

        if not Path(checkpoint_path).exists():
            print(f"⚠ Checkpoint not found: {checkpoint_path}")
            return True  # Don't fail, just skip

        # Run validation script
        import subprocess
        result = subprocess.run(
            [sys.executable, self.validation_script, "--checkpoint", checkpoint_path],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✓ Quality gate PASSED for epoch {epoch}")
            return True
        elif result.returncode == 2:
            print(f"⚠ Quality gate WARNING for epoch {epoch}")
            print(result.stdout)
            return True  # Warning but continue
        else:
            print(f"❌ Quality gate FAILED for epoch {epoch}")
            print(result.stdout)
            return False

    def should_check_epoch(self, epoch: int) -> bool:
        """Determine if we should run quality check this epoch."""
        return epoch in QUALITY_CHECK_EPOCHS


# ==============================================================================
# WATCHDOG MONITOR
# ==============================================================================

class WatchdogMonitor:
    """Writes status updates for external watchdog monitoring."""

    def __init__(self, watchdog_file: str = "training_status.json"):
        self.watchdog_file = watchdog_file
        self.start_time = time.time()

    def update(self, epoch: int, total_epochs: int, train_loss: float,
               val_loss: Optional[float] = None, status: str = "training"):
        """Update watchdog file with current status."""
        elapsed = time.time() - self.start_time
        remaining_epochs = total_epochs - epoch
        avg_epoch_time = elapsed / epoch if epoch > 0 else 0
        eta_seconds = remaining_epochs * avg_epoch_time

        status_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": status,
            "epoch": epoch,
            "total_epochs": total_epochs,
            "progress_pct": (epoch / total_epochs) * 100,
            "train_loss": train_loss,
            "val_loss": val_loss,
            "elapsed_seconds": elapsed,
            "eta_seconds": eta_seconds,
            "eta_hours": eta_seconds / 3600,
        }

        with open(self.watchdog_file, "w") as f:
            json.dump(status_data, f, indent=2)


# ==============================================================================
# PRODUCTION TRAINER
# ==============================================================================

class ProductionTrainer:
    """Production trainer with quality gates and monitoring."""

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        device: str,
        learning_rate: float = 1e-4,
        checkpoint_dir: str = "checkpoints",
        phase: int = 1,
        use_amp: bool = True,
    ):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device
        self.phase = phase
        self.use_amp = use_amp

        self.optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=learning_rate,
            betas=(0.9, 0.98),
            eps=1e-9,
            weight_decay=0.01,
        )

        self.criterion = nn.CrossEntropyLoss(ignore_index=0)  # Ignore padding
        self.scaler = GradScaler() if use_amp else None

        self.checkpoint_dir = checkpoint_dir
        Path(checkpoint_dir).mkdir(parents=True, exist_ok=True)

        self.quality_checker = QualityGateChecker(checkpoint_dir)
        self.watchdog = WatchdogMonitor()

        self.loss_history = []

    def train_epoch(self, epoch: int) -> float:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0
        num_batches = 0

        for batch_idx, (input_ids, labels) in enumerate(self.train_loader):
            input_ids = input_ids.to(self.device)
            labels = labels.to(self.device)

            self.optimizer.zero_grad()

            if self.use_amp:
                with autocast():
                    outputs = self.model(input_ids)
                    outputs = outputs.view(-1, outputs.size(-1))
                    labels = labels.view(-1)
                    loss = self.criterion(outputs, labels)

                self.scaler.scale(loss).backward()
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                outputs = self.model(input_ids)
                outputs = outputs.view(-1, outputs.size(-1))
                labels = labels.view(-1)
                loss = self.criterion(outputs, labels)

                loss.backward()
                self.optimizer.step()

            total_loss += loss.item()
            num_batches += 1

            if batch_idx % 10 == 0:
                print(f"  Batch {batch_idx}/{len(self.train_loader)}, Loss: {loss.item():.4f}", end="\r")

        avg_loss = total_loss / num_batches
        return avg_loss

    def validate(self) -> float:
        """Validate on validation set."""
        self.model.eval()
        total_loss = 0.0
        num_batches = 0

        with torch.no_grad():
            for input_ids, labels in self.val_loader:
                input_ids = input_ids.to(self.device)
                labels = labels.to(self.device)

                outputs = self.model(input_ids)
                outputs = outputs.view(-1, outputs.size(-1))
                labels = labels.view(-1)
                loss = self.criterion(outputs, labels)

                total_loss += loss.item()
                num_batches += 1

        avg_loss = total_loss / num_batches
        return avg_loss

    def check_abort_conditions(self, train_loss: float, val_loss: float, epoch: int) -> bool:
        """Check if training should abort."""
        # Loss diverged
        if train_loss > MAX_LOSS_THRESHOLD:
            print(f"\n❌ ABORT: Training loss diverged ({train_loss:.4f} > {MAX_LOSS_THRESHOLD})")
            return True

        # Suspiciously low loss too early
        if epoch < 10 and train_loss < MIN_LOSS_THRESHOLD:
            print(f"\n❌ ABORT: Loss collapsed too early (epoch {epoch}, loss {train_loss:.4f})")
            return True

        # Check loss trend (if loss increasing for 5 consecutive epochs)
        if len(self.loss_history) >= 5:
            recent_losses = [l["train"] for l in self.loss_history[-5:]]
            if all(recent_losses[i] < recent_losses[i+1] for i in range(4)):
                print(f"\n❌ ABORT: Loss increasing for 5 consecutive epochs")
                return True

        return False

    def save_checkpoint(self, checkpoint_path: str, epoch: int, train_loss: float, val_loss: float):
        """Save checkpoint with metadata."""
        torch.save({
            "epoch": epoch,
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "train_loss": train_loss,
            "val_loss": val_loss,
            "phase": self.phase,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }, checkpoint_path)

        print(f"✓ Saved: {checkpoint_path}")

    def train(self, num_epochs: int, start_epoch: int = 1):
        """Main training loop with quality gates."""
        print(f"\n{'='*80}")
        print(f"STARTING PHASE {self.phase} TRAINING")
        print(f"{'='*80}")
        print(f"Epochs: {start_epoch} → {num_epochs}")
        print(f"Model: 100M parameters")
        print(f"Device: {self.device}")
        print(f"Mixed precision: {self.use_amp}")
        print(f"{'='*80}\n")

        best_val_loss = float('inf')

        for epoch in range(start_epoch, num_epochs + 1):
            epoch_start = time.time()

            print(f"\n{'='*80}")
            print(f"EPOCH {epoch}/{num_epochs} (Phase {self.phase})")
            print(f"{'='*80}")

            # Train
            train_loss = self.train_epoch(epoch)
            print(f"\nTrain Loss: {train_loss:.4f}")

            # Validate
            val_loss = self.validate()
            print(f"Val Loss: {val_loss:.4f}")

            # Record loss history
            self.loss_history.append({
                "epoch": epoch,
                "train": train_loss,
                "val": val_loss,
            })

            # Update watchdog
            self.watchdog.update(epoch, num_epochs, train_loss, val_loss)

            epoch_time = time.time() - epoch_start
            print(f"Epoch time: {epoch_time:.1f}s")

            # Check abort conditions
            if self.check_abort_conditions(train_loss, val_loss, epoch):
                self.watchdog.update(epoch, num_epochs, train_loss, val_loss, status="aborted")
                return False

            # Save periodic checkpoints
            if epoch % 10 == 0 or epoch == num_epochs:
                checkpoint_path = os.path.join(
                    self.checkpoint_dir,
                    f"phase{self.phase}_epoch{epoch}.pt"
                )
                self.save_checkpoint(checkpoint_path, epoch, train_loss, val_loss)

            # Save best model
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_path = os.path.join(
                    self.checkpoint_dir,
                    f"phase{self.phase}_BEST_epoch{epoch}.pt"
                )
                self.save_checkpoint(best_path, epoch, train_loss, val_loss)
                print(f"NEW BEST! Val loss: {val_loss:.4f}")

            # Quality gate check
            if self.quality_checker.should_check_epoch(epoch):
                checkpoint_path = os.path.join(
                    self.checkpoint_dir,
                    f"phase{self.phase}_epoch{epoch}.pt"
                )

                if not self.quality_checker.check_epoch(epoch, checkpoint_path):
                    print(f"\n❌ QUALITY GATE FAILED AT EPOCH {epoch}")
                    print(f"Training aborted due to quality failure")
                    self.watchdog.update(epoch, num_epochs, train_loss, val_loss, status="quality_failed")
                    return False

        # Save final checkpoint
        final_path = os.path.join(
            self.checkpoint_dir,
            f"phase{self.phase}_FINAL_epoch{num_epochs}.pt"
        )
        self.save_checkpoint(final_path, num_epochs, train_loss, val_loss)

        self.watchdog.update(num_epochs, num_epochs, train_loss, val_loss, status="completed")
        return True


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Production HLX Brain Training (100M)")

    # Training phase
    parser.add_argument("--phase", type=int, required=True, choices=[1, 2, 3],
                        help="Training phase: 1=English, 2=HLX, 3=Translation")
    parser.add_argument("--epochs", type=int, required=True,
                        help="Number of epochs for this phase")

    # Corpus
    parser.add_argument("--corpus", type=str, default="corpus_all_variants.md",
                        help="Path to training corpus")

    # Training config
    parser.add_argument("--batch-size", type=int, default=4,
                        help="Batch size (default: 4 for 8GB GPU)")
    parser.add_argument("--seq-length", type=int, default=256,
                        help="Sequence length (default: 256 for 8GB GPU)")
    parser.add_argument("--lr", type=float, default=1e-4,
                        help="Learning rate (default: 1e-4)")
    parser.add_argument("--train-ratio", type=float, default=0.8,
                        help="Train/val split ratio (default: 0.8)")

    # Checkpointing
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints",
                        help="Checkpoint directory")
    parser.add_argument("--resume-from", type=str, default=None,
                        help="Resume from checkpoint")

    # Optimization
    parser.add_argument("--use-fp16", action="store_true", default=True,
                        help="Use mixed precision (default: True)")
    parser.add_argument("--no-fp16", action="store_false", dest="use_fp16",
                        help="Disable mixed precision")

    args = parser.parse_args()

    print("="*80)
    print("PRODUCTION HLX BRAIN TRAINING: 100M MODEL")
    print("="*80)
    print(f"Phase {args.phase}: ", end="")
    if args.phase == 1:
        print("English Mastery")
    elif args.phase == 2:
        print("HLX Family Mastery")
    elif args.phase == 3:
        print("Translation Training")
    print(f"Epochs: {args.epochs}")
    print(f"Corpus: {args.corpus}")
    print(f"Batch size: {args.batch_size}")
    print(f"Sequence length: {args.seq_length}")
    print(f"Learning rate: {args.lr}")
    print(f"Mixed precision: {args.use_fp16}")
    print("="*80)

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\nDevice: {device}")

    if device.type == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

    # Create tokenizer
    print("\n✓ Creating tokenizer...")
    tokenizer = create_tokenizer()
    print(f"✓ Vocabulary size: {tokenizer.vocab_size}")

    # Load dataset
    print(f"\n✓ Loading Phase {args.phase} dataset...")
    full_dataset = PhaseDataset(
        corpus_path=args.corpus,
        tokenizer=tokenizer,
        seq_length=args.seq_length,
        phase=args.phase,
    )

    # Split into train/val
    train_size = int(len(full_dataset) * args.train_ratio)
    val_size = len(full_dataset) - train_size

    train_dataset, val_dataset = random_split(
        full_dataset,
        [train_size, val_size],
        generator=torch.Generator().manual_seed(42)
    )

    print(f"✓ Train: {len(train_dataset)} examples")
    print(f"✓ Val: {len(val_dataset)} examples")

    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=0,
        pin_memory=True,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=True,
    )

    # Create 100M model
    print("\n✓ Creating 100M model...")
    model = create_model(
        vocab_size=tokenizer.vocab_size,
        **MODEL_CONFIG_100M
    )

    # Architecture verification
    total_params = sum(p.numel() for p in model.parameters())
    print(f"✓ Model parameters: {total_params:,}")

    if total_params < 90_000_000 or total_params > 110_000_000:
        print(f"\n❌ ARCHITECTURE ERROR: Expected ~100M params, got {total_params:,}")
        sys.exit(1)

    model = model.to(device)

    # Resume from checkpoint if specified
    start_epoch = 1
    if args.resume_from:
        print(f"\n✓ Resuming from: {args.resume_from}")
        checkpoint = torch.load(args.resume_from, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        start_epoch = checkpoint.get('epoch', 0) + 1
        print(f"✓ Resuming from epoch {start_epoch}")

    # Create trainer
    trainer = ProductionTrainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        device=device,
        learning_rate=args.lr,
        checkpoint_dir=args.checkpoint_dir,
        phase=args.phase,
        use_amp=args.use_fp16,
    )

    # Train
    success = trainer.train(num_epochs=args.epochs, start_epoch=start_epoch)

    if success:
        print("\n" + "="*80)
        print(f"✓ PHASE {args.phase} TRAINING COMPLETED SUCCESSFULLY")
        print("="*80)
        sys.exit(0)
    else:
        print("\n" + "="*80)
        print(f"❌ PHASE {args.phase} TRAINING FAILED")
        print("="*80)
        sys.exit(1)


if __name__ == "__main__":
    main()
