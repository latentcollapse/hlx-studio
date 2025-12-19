#!/usr/bin/env python3
"""
Qwen 0.6B → Helix100m Distillation Training
FREE COMPUTE EXPERIMENT

Uses local Qwen3:0.6b (Ollama) as teacher to train Helix100m student.
All quality gates and monitoring from production training baked in.

Usage:
    export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
    python3 train_qwen_distillation.py --epochs 100 --batch-size 4

Experiment: See what happens when tiny free Qwen teaches specialized Helix100m.
"""

import argparse
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# === Configuration ===

MODEL_CONFIG_100M = {
    "d_model": 1024,
    "nhead": 16,
    "num_layers": 8,
    "dim_feedforward": 4096,
    "dropout": 0.1,
    "max_seq_length": 256,
}

# Quality gate epochs
QUALITY_CHECK_EPOCHS = [1, 5, 10, 20, 50, 100]

# Loss thresholds
MAX_LOSS_THRESHOLD = 15.0
MIN_LOSS_THRESHOLD = 0.001


# === Ollama Integration ===

def query_qwen(prompt: str, model: str = "qwen3:0.6b", max_tokens: int = 100) -> str:
    """Query local Qwen model via Ollama."""
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Warning: Qwen query failed: {result.stderr}")
            return prompt  # Fallback to input
    except Exception as e:
        print(f"Warning: Qwen query error: {e}")
        return prompt


# === Model Architecture ===

class TransformerLanguageModel(nn.Module):
    """Helix100m: 100M parameter transformer for HLX specialization."""

    def __init__(self, vocab_size, d_model=1024, nhead=16, num_layers=8,
                 dim_feedforward=4096, dropout=0.1, max_seq_length=256):
        super().__init__()

        self.d_model = d_model
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = nn.Embedding(max_seq_length, d_model)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True,
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        self.fc_out = nn.Linear(d_model, vocab_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        seq_len = x.size(1)
        positions = torch.arange(0, seq_len, device=x.device).unsqueeze(0)

        x = self.embedding(x) + self.pos_encoding(positions)
        x = self.dropout(x)

        x = self.transformer(x)
        logits = self.fc_out(x)

        return logits


# === Tokenizer ===

class CharTokenizer:
    """Simple character-level tokenizer for Helix100m."""

    def __init__(self):
        # Core ASCII + HLX glyphs
        self.chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,;:!?'\"-()[]{}@#$%&*+=/<>\\|_`~\n\t")
        self.chars.extend(["🜀", "🜁", "🜂", "🜃", "🜄", "🜊", "⟁"])  # HLX glyphs

        # Add special PAD token at the end
        self.pad_token = "<PAD>"
        self.chars.append(self.pad_token)

        self.char_to_idx = {ch: idx for idx, ch in enumerate(self.chars)}
        self.idx_to_char = {idx: ch for idx, ch in enumerate(self.chars)}
        self.pad_token_id = self.char_to_idx[self.pad_token]
        self.vocab_size = len(self.chars)

    def encode(self, text):
        return [self.char_to_idx.get(ch, 0) for ch in text]

    def decode(self, indices):
        return ''.join([self.idx_to_char.get(idx, '') for idx in indices if idx != self.pad_token_id])


# === Dataset ===

class QwenDistillationDataset(Dataset):
    """Dataset that uses Qwen to augment English corpus."""

    def __init__(self, corpus_path: str, tokenizer: CharTokenizer, seq_length: int = 256, use_qwen: bool = True):
        self.tokenizer = tokenizer
        self.seq_length = seq_length
        self.use_qwen = use_qwen

        # Load corpus
        with open(corpus_path, 'r') as f:
            text = f.read()

        # Extract all non-comment, non-empty lines from corpus
        # Handles both old format (## English:) and canonical format (mixed content)
        self.examples = []

        for line in text.split('\n'):
            line = line.strip()

            # Skip empty lines and comment-only lines
            if not line or line.startswith('#'):
                continue

            # Skip pure metadata lines
            if line.startswith('**'):
                continue

            # Skip code blocks and special markers
            if any(line.startswith(x) for x in ['```', '|', '---']):
                continue

            # Accept all other lines as training examples
            # This includes English descriptions, HLXL code, HLX contracts, etc.
            self.examples.append(line)

        print(f"Loaded {len(self.examples)} English examples from corpus")

        # Optionally augment with Qwen
        if self.use_qwen:
            print("Augmenting corpus with Qwen 0.6B variations...")
            augmented = []
            for i, example in enumerate(self.examples[:50]):  # Augment first 50 for speed
                if i % 10 == 0:
                    print(f"  Augmenting {i}/{min(50, len(self.examples))}...")

                # Get Qwen variation
                qwen_prompt = f"Rewrite this sentence in a different way: {example}"
                qwen_output = query_qwen(qwen_prompt, max_tokens=100)
                if qwen_output and qwen_output != example:
                    augmented.append(qwen_output)

            self.examples.extend(augmented)
            print(f"Augmented to {len(self.examples)} total examples")

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        text = self.examples[idx]

        # Tokenize
        tokens = self.tokenizer.encode(text)

        # Truncate or pad to seq_length
        if len(tokens) > self.seq_length:
            tokens = tokens[:self.seq_length]
        else:
            # CRITICAL FIX #1: Use pad_token_id instead of 0 (which is 'a')
            tokens = tokens + [self.tokenizer.pad_token_id] * (self.seq_length - len(tokens))

        # Input IDs (for model input)
        x = torch.tensor(tokens, dtype=torch.long)

        # CRITICAL FIX #2: Create SHIFTED labels for next-token prediction
        # labels[i] should be what input[i] predicts (i.e., token[i+1])
        shifted_tokens = tokens[1:] + [self.tokenizer.pad_token_id]
        y = torch.tensor(shifted_tokens, dtype=torch.long)

        # CRITICAL FIX #3: Mask padding tokens in labels with -100
        # This prevents model from training on padding tokens
        y[y == self.tokenizer.pad_token_id] = -100

        return x, y


# === Training ===

class QwenDistillationTrainer:
    """Bulletproof trainer with all quality gates."""

    def __init__(self, model, tokenizer, device, output_dir="checkpoints"):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.best_loss = float('inf')
        self.loss_history = []

    def verify_architecture(self):
        """Verify 100M parameter count."""
        param_count = sum(p.numel() for p in self.model.parameters())
        print(f"\n{'='*80}")
        print("ARCHITECTURE VERIFICATION")
        print(f"{'='*80}")
        print(f"Total parameters: {param_count:,}")
        print(f"Expected: ~100M (target: 101,533,813)")
        print(f"d_model: {self.model.d_model}")
        print(f"Vocab size: {self.tokenizer.vocab_size}")

        if param_count < 90_000_000 or param_count > 110_000_000:
            print(f"❌ WARNING: Parameter count outside 90M-110M range!")
        else:
            print(f"✓ Architecture verified")

        print(f"{'='*80}\n")

        return param_count

    def quality_check(self, epoch, checkpoint_path):
        """Run quality validation on checkpoint."""
        print(f"\n{'='*60}")
        print(f"QUALITY GATE: Epoch {epoch}")
        print(f"{'='*60}")

        # Simple generation test
        test_prompts = [
            "Search for documents",
            "Filter active users",
            "The quick brown fox",
        ]

        self.model.eval()
        issues = []

        with torch.no_grad():
            for prompt in test_prompts:
                # Encode prompt
                tokens = self.tokenizer.encode(prompt)
                generated = tokens.copy()

                # Autoregressive generation (proper)
                for _ in range(50):  # Generate up to 50 new tokens
                    if len(generated) >= 256:  # Max seq length
                        break

                    # Get logits for current sequence
                    input_ids = torch.tensor([generated], dtype=torch.long, device=self.device)
                    logits = self.model(input_ids)

                    # Take only the LAST token's logits (next-token prediction)
                    next_token_logits = logits[0, -1, :] / 0.8  # temperature

                    # Sample from distribution
                    probs = torch.softmax(next_token_logits, dim=-1)
                    next_token = torch.multinomial(probs, num_samples=1).item()

                    # Stop on newline or PAD token
                    if next_token == self.tokenizer.char_to_idx.get('\n', 0):
                        break
                    if next_token == self.tokenizer.pad_token_id:
                        break

                    generated.append(next_token)

                # Decode full output
                output_text = self.tokenizer.decode(generated)

                # Remove prompt from output
                generated_only = output_text[len(prompt):]

                print(f"\nPrompt: {prompt}")
                print(f"Output: {generated_only[:100]}...")

                # Check for parroting
                if generated_only.strip() == "":
                    issues.append("Empty generation")

                # Check for character collapse
                unique_chars = set(generated_only.strip().replace(' ', ''))
                if len(unique_chars) < 3 and len(generated_only.strip()) > 5:
                    issues.append("Character collapse detected")

        self.model.train()

        if issues:
            print(f"\n❌ QUALITY GATE FAILED:")
            for issue in issues:
                print(f"  - {issue}")
            print(f"{'='*60}\n")
            return False
        else:
            print(f"\n✓ QUALITY GATE PASSED")
            print(f"{'='*60}\n")
            return True

    def update_watchdog(self, epoch, num_epochs, train_loss, val_loss, status="training"):
        """Update training status for watchdog."""
        status_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "epoch": epoch,
            "total_epochs": num_epochs,
            "train_loss": train_loss,
            "val_loss": val_loss,
            "progress_pct": (epoch / num_epochs) * 100,
            "eta_hours": 0,  # TODO: Calculate
            "status": status,
        }

        with open("training_status.json", "w") as f:
            json.dump(status_data, f, indent=2)

    def check_abort_conditions(self, train_loss, epoch):
        """Check if training should abort."""
        # Loss diverged
        if train_loss > MAX_LOSS_THRESHOLD:
            print(f"❌ ABORT: Loss diverged ({train_loss:.4f} > {MAX_LOSS_THRESHOLD})")
            return True

        # Loss collapsed too early
        if epoch < 10 and train_loss < MIN_LOSS_THRESHOLD:
            print(f"❌ ABORT: Loss collapsed too early (epoch {epoch}, loss {train_loss:.4f})")
            return True

        # Loss increasing for 5 epochs
        if len(self.loss_history) >= 5:
            recent = self.loss_history[-5:]
            if all(recent[i] < recent[i+1] for i in range(4)):
                print(f"❌ ABORT: Loss increasing for 5 consecutive epochs")
                return True

        return False

    def train(self, train_loader, val_loader, num_epochs, lr=1e-4):
        """Main training loop with quality gates."""
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()

        print(f"\n{'='*80}")
        print("QWEN DISTILLATION TRAINING - FREE COMPUTE EXPERIMENT")
        print(f"{'='*80}")
        print(f"Teacher: Qwen3:0.6b (local, free)")
        print(f"Student: Helix100m (specialized)")
        print(f"Epochs: {num_epochs}")
        print(f"Learning rate: {lr}")
        print(f"Batch size: {train_loader.batch_size}")
        print(f"{'='*80}\n")

        # Verify architecture
        self.verify_architecture()

        for epoch in range(1, num_epochs + 1):
            self.model.train()
            epoch_loss = 0

            for batch_idx, (x, y) in enumerate(train_loader):
                x, y = x.to(self.device), y.to(self.device)

                # Forward
                logits = self.model(x)
                loss = criterion(logits.view(-1, self.tokenizer.vocab_size), y.view(-1))

                # Backward
                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                optimizer.step()

                epoch_loss += loss.item()

                if batch_idx % 10 == 0:
                    print(f"Epoch {epoch}/{num_epochs} | Batch {batch_idx}/{len(train_loader)} | Loss: {loss.item():.4f}")

            avg_train_loss = epoch_loss / len(train_loader)
            self.loss_history.append(avg_train_loss)

            # Validation
            self.model.eval()
            val_loss = 0
            with torch.no_grad():
                for x, y in val_loader:
                    x, y = x.to(self.device), y.to(self.device)
                    logits = self.model(x)
                    loss = criterion(logits.view(-1, self.tokenizer.vocab_size), y.view(-1))
                    val_loss += loss.item()

            avg_val_loss = val_loss / len(val_loader) if len(val_loader) > 0 else avg_train_loss

            print(f"\n{'='*80}")
            print(f"EPOCH {epoch}/{num_epochs} COMPLETE")
            print(f"{'='*80}")
            print(f"Train Loss: {avg_train_loss:.4f}")
            print(f"Val Loss: {avg_val_loss:.4f}")
            print(f"{'='*80}\n")

            # Update watchdog
            self.update_watchdog(epoch, num_epochs, avg_train_loss, avg_val_loss)

            # Check abort conditions
            if self.check_abort_conditions(avg_train_loss, epoch):
                self.update_watchdog(epoch, num_epochs, avg_train_loss, avg_val_loss, status="aborted")
                return False

            # Save checkpoint
            checkpoint_path = self.output_dir / f"qwen_distill_epoch{epoch}.pt"
            torch.save({
                'epoch': epoch,
                'model_state_dict': self.model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'train_loss': avg_train_loss,
                'val_loss': avg_val_loss,
            }, checkpoint_path)

            # Best model
            if avg_val_loss < self.best_loss:
                self.best_loss = avg_val_loss
                best_path = self.output_dir / "qwen_distill_BEST.pt"
                torch.save(self.model.state_dict(), best_path)
                print(f"✓ Saved new best model (loss: {avg_val_loss:.4f})")

            # Quality gate
            if epoch in QUALITY_CHECK_EPOCHS:
                if not self.quality_check(epoch, checkpoint_path):
                    print(f"❌ TRAINING ABORTED: Quality gate failed at epoch {epoch}")
                    self.update_watchdog(epoch, num_epochs, avg_train_loss, avg_val_loss, status="quality_failed")
                    return False

        # Final checkpoint
        final_path = self.output_dir / f"qwen_distill_FINAL_epoch{num_epochs}.pt"
        torch.save(self.model.state_dict(), final_path)

        self.update_watchdog(num_epochs, num_epochs, avg_train_loss, avg_val_loss, status="completed")

        print(f"\n{'='*80}")
        print("TRAINING COMPLETED SUCCESSFULLY")
        print(f"{'='*80}")
        print(f"Best loss: {self.best_loss:.4f}")
        print(f"Final checkpoint: {final_path}")
        print(f"{'='*80}\n")

        return True


# === Main ===

def main():
    parser = argparse.ArgumentParser(description="Qwen 0.6B → Helix100m Distillation Training")
    parser.add_argument("--epochs", type=int, default=100, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--seq-length", type=int, default=256, help="Sequence length")
    parser.add_argument("--corpus", type=str, default="corpus_all_variants.md", help="Corpus path")
    parser.add_argument("--no-qwen-augment", action="store_true", help="Disable Qwen augmentation")

    args = parser.parse_args()

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Tokenizer
    tokenizer = CharTokenizer()
    print(f"Vocab size: {tokenizer.vocab_size}")

    # Model
    model = TransformerLanguageModel(
        vocab_size=tokenizer.vocab_size,
        **MODEL_CONFIG_100M
    ).to(device)

    # Dataset
    dataset = QwenDistillationDataset(
        corpus_path=args.corpus,
        tokenizer=tokenizer,
        seq_length=args.seq_length,
        use_qwen=not args.no_qwen_augment,
    )

    # Split train/val
    train_size = int(0.9 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)

    # Trainer
    trainer = QwenDistillationTrainer(model, tokenizer, device)

    # Train
    success = trainer.train(train_loader, val_loader, args.epochs, lr=args.lr)

    if success:
        print("\n✓ Experiment complete! Check checkpoints/ for trained model.")
    else:
        print("\n❌ Training failed. Check logs for details.")


if __name__ == "__main__":
    main()
