#!/usr/bin/env python3
"""
Specialist Brain Training: 50M Parameter Models
MoE System: ASCII and Runic Specialists

Uses specialized corpora for track-specific training:
- ASCII Specialist (LC-T): 70% LC-T, 20% English, 10% LC-R awareness
- Runic Specialist (LC-R): 70% LC-R, 20% English, 10% LC-T awareness

Usage:
    export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
    python3 train_specialist_50m.py --specialist ascii --epochs 100 --batch-size 4
    python3 train_specialist_50m.py --specialist runic --epochs 100 --batch-size 4
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

# 50M model: optimized for balance between capacity and training speed
# 50.03M parameters (tuned to match target)
MODEL_CONFIG_50M = {
    "d_model": 768,
    "nhead": 12,
    "num_layers": 7,
    "dim_feedforward": 3072,
    "dropout": 0.1,
    "max_seq_length": 256,
}

# 100M model: matches successful Coordinator architecture
# 101M parameters - proven to train successfully
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

# Specialist-specific quality prompts
QUALITY_PROMPTS = {
    "ascii": {
        "prompts": [
            ("Represent true", "TRUE"),
            ("Create array", "["),
            ("Store number", "[0x"),
        ],
        "description": "ASCII Specialist (LC-T track)"
    },
    "runic": {
        "prompts": [
            ("Represent true", "⊤"),
            ("Create array", "🜃"),
            ("Store number", "🜁"),
        ],
        "description": "Runic Specialist (LC-R track)"
    }
}


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
            return prompt
    except Exception as e:
        print(f"Warning: Qwen query error: {e}")
        return prompt


# === Model Architecture ===

class TransformerLanguageModel(nn.Module):
    """50M parameter transformer for HLX specialist brains."""

    def __init__(self, vocab_size, d_model=768, nhead=12, num_layers=7,
                 dim_feedforward=3072, dropout=0.1, max_seq_length=256):
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
    """Character-level tokenizer for Helix specialists."""

    def __init__(self):
        # Core ASCII + HLX glyphs
        self.chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,;:!?'\"-()[]{}@#$%&*+=/<>\\|_`~\n\t")
        self.chars.extend(["🜀", "🜁", "🜂", "🜃", "🜄", "🜊", "⟁", "⊤", "⊥", "∅"])

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

class SpecialistDataset(Dataset):
    """Dataset for specialist brain training with specialized corpus."""

    def __init__(self, corpus_path: str, tokenizer: CharTokenizer, seq_length: int = 256, use_qwen: bool = True):
        self.tokenizer = tokenizer
        self.seq_length = seq_length
        self.use_qwen = use_qwen

        # Load corpus
        with open(corpus_path, 'r') as f:
            text = f.read()

        self.examples = []

        # Extract examples from markdown - handles both old and specialized formats
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

            # Extract English descriptions
            if line.startswith('English:'):
                self.examples.append(line.replace('English:', '').strip())
            # Extract format lines (LC-T, LC-R, HLXL, HLX, etc.)
            elif line.startswith('lc_t:') or line.startswith('lc_r:') or \
                 line.startswith('HLXL:') or line.startswith('HLX:'):
                self.examples.append(line.split(':', 1)[1].strip())
            # Accept other content lines
            elif ':' not in line or line.count(':') > 2:  # Not a field label
                self.examples.append(line)

        # Filter empty examples
        self.examples = [e for e in self.examples if e]

        print(f"Loaded {len(self.examples)} examples from {corpus_path}")

        # Optionally augment with Qwen
        if self.use_qwen and len(self.examples) < 100:
            print("Augmenting corpus with Qwen 0.6B variations...")
            augmented = []
            for i, example in enumerate(self.examples[:30]):
                if i % 10 == 0:
                    print(f"  Augmenting {i}/{min(30, len(self.examples))}...")

                qwen_prompt = f"Rewrite this in technical format: {example}"
                qwen_output = query_qwen(qwen_prompt, max_tokens=100)
                if qwen_output and qwen_output != example:
                    augmented.append(qwen_output)

            self.examples.extend(augmented)
            print(f"Augmented to {len(self.examples)} total examples")

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        text = self.examples[idx]

        tokens = self.tokenizer.encode(text)

        if len(tokens) > self.seq_length:
            tokens = tokens[:self.seq_length]
        else:
            tokens = tokens + [self.tokenizer.pad_token_id] * (self.seq_length - len(tokens))

        x = torch.tensor(tokens, dtype=torch.long)

        shifted_tokens = tokens[1:] + [self.tokenizer.pad_token_id]
        y = torch.tensor(shifted_tokens, dtype=torch.long)

        y[y == self.tokenizer.pad_token_id] = -100

        return x, y


# === Training ===

class SpecialistTrainer:
    """Trainer for specialist brains with track-specific quality gates."""

    def __init__(self, model, tokenizer, specialist_type, device, output_dir="checkpoints"):
        self.model = model
        self.tokenizer = tokenizer
        self.specialist_type = specialist_type
        self.device = device
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.best_loss = float('inf')
        self.loss_history = []

    def verify_architecture(self, expected_size="50M"):
        """Verify parameter count matches expected size."""
        param_count = sum(p.numel() for p in self.model.parameters())
        spec_name = QUALITY_PROMPTS[self.specialist_type]["description"]

        print(f"\n{'='*80}")
        print(f"ARCHITECTURE VERIFICATION - {spec_name}")
        print(f"{'='*80}")
        print(f"Total parameters: {param_count:,}")
        print(f"Expected: ~{expected_size}")
        print(f"d_model: {self.model.d_model}")
        print(f"Vocab size: {self.tokenizer.vocab_size}")
        print(f"Specialist type: {self.specialist_type.upper()}")

        # Set validation ranges based on expected size
        if expected_size == "100M":
            min_params, max_params = 95_000_000, 110_000_000
        else:  # 50M
            min_params, max_params = 45_000_000, 55_000_000

        if param_count < min_params or param_count > max_params:
            print(f"WARNING: Parameter count outside {min_params/1e6:.0f}M-{max_params/1e6:.0f}M range!")
        else:
            print(f"✓ Architecture verified")

        print(f"{'='*80}\n")

        return param_count

    def quality_check(self, epoch, checkpoint_path):
        """Run specialist-specific quality validation."""
        print(f"\n{'='*60}")
        print(f"QUALITY GATE: Epoch {epoch} - {self.specialist_type.upper()}")
        print(f"{'='*60}")

        spec_prompts = QUALITY_PROMPTS[self.specialist_type]["prompts"]

        self.model.eval()
        issues = []

        with torch.no_grad():
            for prompt, expected_token in spec_prompts:
                tokens = self.tokenizer.encode(prompt)
                generated = tokens.copy()

                for _ in range(50):
                    if len(generated) >= 256:
                        break

                    input_ids = torch.tensor([generated], dtype=torch.long, device=self.device)
                    logits = self.model(input_ids)
                    next_token_logits = logits[0, -1, :] / 0.8

                    probs = torch.softmax(next_token_logits, dim=-1)
                    next_token = torch.multinomial(probs, num_samples=1).item()

                    if next_token == self.tokenizer.char_to_idx.get('\n', 0):
                        break
                    if next_token == self.tokenizer.pad_token_id:
                        break

                    generated.append(next_token)

                output_text = self.tokenizer.decode(generated)
                generated_only = output_text[len(prompt):]

                print(f"\nPrompt: {prompt}")
                print(f"Expected token: {expected_token}")
                print(f"Output: {generated_only[:100]}...")

                if generated_only.strip() == "":
                    issues.append(f"Empty generation for '{prompt}'")

                unique_chars = set(generated_only.strip().replace(' ', ''))
                if len(unique_chars) < 3 and len(generated_only.strip()) > 5:
                    issues.append("Character collapse detected")

        self.model.train()

        if issues:
            print(f"\n QUALITY GATE FAILED:")
            for issue in issues:
                print(f"  - {issue}")
            print(f"{'='*60}\n")
            return False
        else:
            print(f"\n✓ QUALITY GATE PASSED")
            print(f"{'='*60}\n")
            return True

    def update_watchdog(self, epoch, num_epochs, train_loss, val_loss, status="training"):
        """Update training status."""
        status_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "specialist": self.specialist_type,
            "epoch": epoch,
            "total_epochs": num_epochs,
            "train_loss": train_loss,
            "val_loss": val_loss,
            "progress_pct": (epoch / num_epochs) * 100,
            "status": status,
        }

        status_file = f"training_status_{self.specialist_type}.json"
        with open(status_file, "w") as f:
            json.dump(status_data, f, indent=2)

    def check_abort_conditions(self, train_loss, epoch):
        """Check if training should abort."""
        if train_loss > MAX_LOSS_THRESHOLD:
            print(f"❌ ABORT: Loss diverged ({train_loss:.4f} > {MAX_LOSS_THRESHOLD})")
            return True

        if epoch < 10 and train_loss < MIN_LOSS_THRESHOLD:
            print(f"❌ ABORT: Loss collapsed too early (epoch {epoch}, loss {train_loss:.4f})")
            return True

        if len(self.loss_history) >= 5:
            recent = self.loss_history[-5:]
            if all(recent[i] < recent[i+1] for i in range(4)):
                print(f"❌ ABORT: Loss increasing for 5 consecutive epochs")
                return True

        return False

    def train(self, train_loader, val_loader, num_epochs, lr=1e-4, model_size="50M"):
        """Main training loop."""
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()

        spec_desc = QUALITY_PROMPTS[self.specialist_type]["description"]

        print(f"\n{'='*80}")
        print(f"SPECIALIST BRAIN TRAINING: {spec_desc}")
        print(f"{'='*80}")
        print(f"Architecture: {model_size} parameters")
        print(f"Epochs: {num_epochs}")
        print(f"Learning rate: {lr}")
        print(f"Batch size: {train_loader.batch_size}")
        print(f"{'='*80}\n")

        self.verify_architecture(model_size)

        for epoch in range(1, num_epochs + 1):
            self.model.train()
            epoch_loss = 0

            for batch_idx, (x, y) in enumerate(train_loader):
                x, y = x.to(self.device), y.to(self.device)

                logits = self.model(x)
                loss = criterion(logits.view(-1, self.tokenizer.vocab_size), y.view(-1))

                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                optimizer.step()

                epoch_loss += loss.item()

                if batch_idx % 10 == 0:
                    print(f"Epoch {epoch}/{num_epochs} | Batch {batch_idx}/{len(train_loader)} | Loss: {loss.item():.4f}")

            avg_train_loss = epoch_loss / len(train_loader)
            self.loss_history.append(avg_train_loss)

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
            print(f"EPOCH {epoch}/{num_epochs} - {self.specialist_type.upper()}")
            print(f"{'='*80}")
            print(f"Train Loss: {avg_train_loss:.4f}")
            print(f"Val Loss: {avg_val_loss:.4f}")
            print(f"{'='*80}\n")

            self.update_watchdog(epoch, num_epochs, avg_train_loss, avg_val_loss)

            if self.check_abort_conditions(avg_train_loss, epoch):
                self.update_watchdog(epoch, num_epochs, avg_train_loss, avg_val_loss, status="aborted")
                return False

            checkpoint_path = self.output_dir / f"specialist_{self.specialist_type}_epoch{epoch}.pt"
            torch.save({
                'epoch': epoch,
                'model_state_dict': self.model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'train_loss': avg_train_loss,
                'val_loss': avg_val_loss,
                'specialist_type': self.specialist_type,
            }, checkpoint_path)

            if avg_val_loss < self.best_loss:
                self.best_loss = avg_val_loss
                best_path = self.output_dir / f"specialist_{self.specialist_type}_BEST.pt"
                torch.save(self.model.state_dict(), best_path)
                print(f"✓ Saved new best {self.specialist_type} model (loss: {avg_val_loss:.4f})")

            if epoch in QUALITY_CHECK_EPOCHS:
                if not self.quality_check(epoch, checkpoint_path):
                    print(f"❌ TRAINING ABORTED: Quality gate failed at epoch {epoch}")
                    self.update_watchdog(epoch, num_epochs, avg_train_loss, avg_val_loss, status="quality_failed")
                    return False

        final_path = self.output_dir / f"specialist_{self.specialist_type}_FINAL_epoch{num_epochs}.pt"
        torch.save(self.model.state_dict(), final_path)

        self.update_watchdog(num_epochs, num_epochs, avg_train_loss, avg_val_loss, status="completed")

        print(f"\n{'='*80}")
        print(f"SPECIALIST TRAINING COMPLETED - {self.specialist_type.upper()}")
        print(f"{'='*80}")
        print(f"Best loss: {self.best_loss:.4f}")
        print(f"Final checkpoint: {final_path}")
        print(f"{'='*80}\n")

        return True


# === Main ===

def main():
    parser = argparse.ArgumentParser(description="Specialist Brain Training (50M or 100M)")
    parser.add_argument("--specialist", type=str, required=True, choices=["ascii", "runic"],
                        help="Specialist type: ascii (LC-T) or runic (LC-R)")
    parser.add_argument("--model-size", type=str, default="50m", choices=["50m", "100m"],
                        help="Model size: 50m (~50M params) or 100m (~100M params)")
    parser.add_argument("--epochs", type=int, default=100, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--seq-length", type=int, default=256, help="Sequence length")
    parser.add_argument("--no-qwen-augment", action="store_true", help="Disable Qwen augmentation")

    args = parser.parse_args()

    # Select model configuration
    if args.model_size == "100m":
        model_config = MODEL_CONFIG_100M
        print(f"Using 100M parameter configuration (matches Coordinator)")
    else:
        model_config = MODEL_CONFIG_50M
        print(f"Using 50M parameter configuration")

    # Determine corpus path
    corpus_path = f"corpus_{args.specialist}_specialist.md"
    if not Path(corpus_path).exists():
        print(f"Error: Corpus file not found: {corpus_path}")
        return

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    tokenizer = CharTokenizer()
    print(f"Vocab size: {tokenizer.vocab_size}")

    model = TransformerLanguageModel(
        vocab_size=tokenizer.vocab_size,
        **model_config
    ).to(device)

    dataset = SpecialistDataset(
        corpus_path=corpus_path,
        tokenizer=tokenizer,
        seq_length=args.seq_length,
        use_qwen=not args.no_qwen_augment,
    )

    train_size = int(0.9 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)

    trainer = SpecialistTrainer(model, tokenizer, args.specialist, device)

    success = trainer.train(
        train_loader,
        val_loader,
        args.epochs,
        lr=args.lr,
        model_size="100M" if args.model_size == "100m" else "50M"
    )

    if success:
        print(f"\n✓ {args.specialist.upper()} specialist training complete!")
    else:
        print(f"\n❌ {args.specialist.upper()} specialist training failed.")


if __name__ == "__main__":
    main()
