#!/usr/bin/env python3
"""
HLXL Brain - 1 Billion Parameter All Variants Training

Train on English->(HLXL|LC-R|LC-T|LC-B) translation with scaled 1B architecture.

Features:
- 1.01B parameter model (d_model=2048, layers=20, heads=16, ffn=8192)
- Mixed precision training (FP16) for memory efficiency
- Gradient checkpointing to reduce activation memory
- Gradient accumulation for effective larger batch sizes
- Periodic checkpoint saving

Usage:
    python3 train_all_variants_1b.py --epochs 30 --batch-size 16 --corpus-path corpus_all_variants.md

Memory Requirements:
- Model: ~2 GB (FP16)
- Gradients: ~4 GB
- Optimizer states: ~8 GB (Adam)
- Activations: ~2-4 GB (with gradient checkpointing)
- Total: ~16-20 GB - Should fit on RTX 5060
"""

import argparse
import sys
from pathlib import Path
import torch
import torch.nn as nn
from torch.cuda.amp import autocast, GradScaler
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts
import json
from datetime import datetime
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tokenizer import create_tokenizer
from model import create_model_1b, create_model_100m, create_model_scaled
from data_all_variants import create_all_variants_dataloaders


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="HLXL Brain 1B Parameter All Variants Training")

    # Training hyperparameters
    parser.add_argument("--epochs", type=int, default=30,
                        help="Number of training epochs (default: 30)")
    parser.add_argument("--batch-size", type=int, default=16,
                        help="Batch size (default: 16, reduce if OOM)")
    parser.add_argument("--lr", type=float, default=3e-4,
                        help="Learning rate (default: 3e-4, scaled for larger model)")
    parser.add_argument("--weight-decay", type=float, default=0.01,
                        help="Weight decay (default: 0.01)")
    parser.add_argument("--max-grad-norm", type=float, default=1.0,
                        help="Max gradient norm for clipping (default: 1.0)")
    parser.add_argument("--warmup-steps", type=int, default=200,
                        help="Learning rate warmup steps (default: 200)")
    parser.add_argument("--gradient-accumulation", type=int, default=2,
                        help="Gradient accumulation steps (default: 2)")

    # Dataset
    parser.add_argument("--corpus-path", type=str,
                        default="corpus_all_variants.md",
                        help="Path to corpus (default: corpus_all_variants.md)")
    parser.add_argument("--seq-length", type=int, default=256,
                        help="Sequence length (default: 256)")
    parser.add_argument("--train-ratio", type=float, default=0.8,
                        help="Train/val split ratio (default: 0.8)")
    parser.add_argument("--no-balance", action="store_true",
                        help="Don't balance formats (use all examples)")

    # Model size selection
    parser.add_argument("--model-size", type=str, default="1b",
                        choices=["tiny", "10m", "50m", "100m", "250m", "500m", "1b"],
                        help="Model size: tiny (~500K), 10m, 50m, 100m, 250m, 500m, 1b (default: 1b)")

    # Memory optimization
    parser.add_argument("--no-fp16", action="store_true",
                        help="Disable mixed precision (use FP32)")
    parser.add_argument("--no-gradient-checkpointing", action="store_true",
                        help="Disable gradient checkpointing")

    # Logging and checkpointing
    parser.add_argument("--log-interval", type=int, default=1,
                        help="Log every N epochs (default: 1)")
    parser.add_argument("--sample-interval", type=int, default=5,
                        help="Generate samples every N epochs (default: 5)")
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints",
                        help="Checkpoint directory (default: checkpoints)")
    parser.add_argument("--save-history", type=str, default="training_history_all_variants_1b.json",
                        help="Path to save training history")

    # Device
    parser.add_argument("--device", type=str, default=None,
                        help="Device to train on (default: auto-detect)")
    parser.add_argument("--cpu", action="store_true",
                        help="Force CPU training (not recommended for 1B model)")

    return parser.parse_args()


def enable_gradient_checkpointing(model):
    """Enable gradient checkpointing on transformer layers to reduce memory."""
    # PyTorch's TransformerEncoder supports gradient checkpointing via checkpoint_sequential
    # For our model, we'll use the built-in checkpoint functionality

    # Enable gradient checkpointing by modifying forward pass behavior
    for layer in model.transformer.layers:
        # Set flag that can be checked during forward pass
        layer.use_checkpoint = True

    # Also, we can use torch.utils.checkpoint directly in a custom forward
    print("Gradient checkpointing enabled (via layer-wise checkpointing)")


def generate_sample(model, tokenizer, device, prompt_text="[HLXL] Search for documents", max_tokens=50, use_fp16=True):
    """Generate a sample from the model.

    Note: The model was trained on format "[FORMAT] English text -> output"
    So prompts should include the arrow to get just the translation.
    """
    model.eval()

    prompt_ids = tokenizer.encode(prompt_text, add_special_tokens=True)
    prompt = torch.tensor([prompt_ids], dtype=torch.long).to(device)

    with torch.no_grad():
        if use_fp16 and device != "cpu":
            with autocast():
                generated = model.generate(prompt, max_new_tokens=max_tokens, temperature=0.0)
        else:
            generated = model.generate(prompt, max_new_tokens=max_tokens, temperature=0.0)

    generated_text = tokenizer.decode(generated[0].cpu().tolist(), skip_special_tokens=False)
    return generated_text


def generate_translation(model, tokenizer, device, english_text, target_format="HLXL", max_tokens=100, use_fp16=True):
    """Generate a translation from English to the target HLX format.

    Args:
        model: The trained model
        tokenizer: The tokenizer
        device: Device to run on
        english_text: The English text to translate
        target_format: One of HLXL, LC-R, LC-T, LC-B
        max_tokens: Maximum tokens to generate
        use_fp16: Whether to use FP16

    Returns:
        The translated output
    """
    model.eval()

    # Format prompt as training data: "[FORMAT] English text -> "
    # Note: Uses Unicode arrow (U+2192) to match training data format
    prompt_text = f"[{target_format}] {english_text} \u2192 "
    prompt_ids = tokenizer.encode(prompt_text, add_special_tokens=True)
    prompt = torch.tensor([prompt_ids], dtype=torch.long).to(device)

    with torch.no_grad():
        if use_fp16 and device != "cpu":
            with autocast():
                generated = model.generate(prompt, max_new_tokens=max_tokens, temperature=0.0)
        else:
            generated = model.generate(prompt, max_new_tokens=max_tokens, temperature=0.0)

    generated_text = tokenizer.decode(generated[0].cpu().tolist(), skip_special_tokens=True)

    # Extract just the output (after the Unicode arrow)
    if " \u2192 " in generated_text:
        output = generated_text.split(" \u2192 ", 1)[1]
        # Clean up - stop at EOS or next format tag
        output = output.split("<EOS>")[0].split("[HLXL]")[0].split("[LC-R]")[0].split("[LC-T]")[0].split("[LC-B]")[0]
        return output.strip()

    return generated_text


class Trainer1B:
    """
    Trainer for 1B parameter HLXL transformer model.

    Features:
    - Mixed precision (FP16) training
    - Gradient accumulation
    - Gradient checkpointing support
    - Memory-efficient training loop
    """

    def __init__(
        self,
        model,
        train_loader,
        val_loader,
        learning_rate=3e-4,
        weight_decay=0.01,
        max_grad_norm=1.0,
        warmup_steps=200,
        gradient_accumulation_steps=2,
        device="cuda",
        checkpoint_dir="checkpoints",
        use_fp16=True,
    ):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.max_grad_norm = max_grad_norm
        self.warmup_steps = warmup_steps
        self.gradient_accumulation_steps = gradient_accumulation_steps
        self.device = torch.device(device)
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.use_fp16 = use_fp16 and device != "cpu"

        # Move model to device
        self.model.to(self.device)

        # Optimizer: AdamW with weight decay
        self.optimizer = AdamW(
            self.model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay,
            betas=(0.9, 0.999),
            eps=1e-8,
        )

        # Learning rate scheduler: Cosine annealing with warm restarts
        self.scheduler = CosineAnnealingWarmRestarts(
            self.optimizer,
            T_0=len(train_loader) // gradient_accumulation_steps,  # Restart every epoch
            T_mult=1,
            eta_min=learning_rate * 0.1,
        )

        # Loss function
        self.criterion = nn.CrossEntropyLoss()

        # Mixed precision scaler
        self.scaler = GradScaler() if self.use_fp16 else None

        # Training state
        self.global_step = 0
        self.epoch = 0
        self.best_val_loss = float('inf')

        # History
        self.train_losses = []
        self.val_losses = []
        self.learning_rates = []

    def train_epoch(self) -> float:
        """Train for one epoch with mixed precision and gradient accumulation."""
        self.model.train()
        total_loss = 0.0
        num_batches = 0
        accumulated_loss = 0.0

        self.optimizer.zero_grad()

        for batch_idx, (input_ids, labels) in enumerate(self.train_loader):
            # Move to device
            input_ids = input_ids.to(self.device)
            labels = labels.to(self.device)

            # Forward pass with mixed precision
            if self.use_fp16:
                with autocast():
                    logits = self.model(input_ids)
                    loss = self.criterion(
                        logits.view(-1, logits.size(-1)),
                        labels.view(-1),
                    )
                    loss = loss / self.gradient_accumulation_steps

                # Backward pass with scaler
                self.scaler.scale(loss).backward()
            else:
                logits = self.model(input_ids)
                loss = self.criterion(
                    logits.view(-1, logits.size(-1)),
                    labels.view(-1),
                )
                loss = loss / self.gradient_accumulation_steps
                loss.backward()

            accumulated_loss += loss.item() * self.gradient_accumulation_steps

            # Optimizer step every gradient_accumulation_steps
            if (batch_idx + 1) % self.gradient_accumulation_steps == 0:
                # Gradient clipping
                if self.use_fp16:
                    self.scaler.unscale_(self.optimizer)

                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(),
                    self.max_grad_norm
                )

                # Optimizer step
                if self.use_fp16:
                    self.scaler.step(self.optimizer)
                    self.scaler.update()
                else:
                    self.optimizer.step()

                self.optimizer.zero_grad()

                # Learning rate schedule
                if self.global_step >= self.warmup_steps:
                    self.scheduler.step()
                else:
                    # Linear warmup
                    lr_scale = min(1.0, (self.global_step + 1) / self.warmup_steps)
                    for param_group in self.optimizer.param_groups:
                        param_group['lr'] = self.learning_rate * lr_scale

                # Track metrics
                total_loss += accumulated_loss
                num_batches += 1
                self.global_step += 1
                accumulated_loss = 0.0

                # Log current learning rate
                current_lr = self.optimizer.param_groups[0]['lr']
                self.learning_rates.append(current_lr)

        # Handle any remaining accumulated gradients
        if accumulated_loss > 0:
            if self.use_fp16:
                self.scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)
            if self.use_fp16:
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                self.optimizer.step()
            self.optimizer.zero_grad()
            total_loss += accumulated_loss
            num_batches += 1
            self.global_step += 1

        avg_loss = total_loss / max(num_batches, 1)
        return avg_loss

    @torch.no_grad()
    def validate(self) -> float:
        """Run validation with mixed precision."""
        self.model.eval()
        total_loss = 0.0
        num_batches = 0

        for input_ids, labels in self.val_loader:
            input_ids = input_ids.to(self.device)
            labels = labels.to(self.device)

            if self.use_fp16:
                with autocast():
                    logits = self.model(input_ids)
                    loss = self.criterion(
                        logits.view(-1, logits.size(-1)),
                        labels.view(-1),
                    )
            else:
                logits = self.model(input_ids)
                loss = self.criterion(
                    logits.view(-1, logits.size(-1)),
                    labels.view(-1),
                )

            total_loss += loss.item()
            num_batches += 1

        avg_loss = total_loss / max(num_batches, 1)
        return avg_loss

    def save_checkpoint(self, filename: str) -> None:
        """Save model checkpoint."""
        checkpoint_path = self.checkpoint_dir / filename

        checkpoint = {
            'epoch': self.epoch,
            'global_step': self.global_step,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'best_val_loss': self.best_val_loss,
            'train_losses': self.train_losses,
            'val_losses': self.val_losses,
            'model_config': {
                'd_model': self.model.d_model,
                'vocab_size': self.model.vocab_size,
                'max_seq_length': self.model.max_seq_length,
                'num_layers': len(self.model.transformer.layers),
            },
        }

        if self.scaler is not None:
            checkpoint['scaler_state_dict'] = self.scaler.state_dict()

        torch.save(checkpoint, checkpoint_path)
        print(f"  Checkpoint saved: {checkpoint_path}")

    def get_history(self):
        """Get training history."""
        return {
            'train_losses': self.train_losses,
            'val_losses': self.val_losses,
            'learning_rates': self.learning_rates,
            'best_val_loss': self.best_val_loss,
            'epochs_trained': self.epoch + 1,
            'global_steps': self.global_step,
        }


def main():
    """Main training function."""
    args = parse_args()

    # Model size configurations for display
    model_configs = {
        "tiny": {"d_model": 128, "num_layers": 2, "nhead": 4, "dim_feedforward": 512},
        "10m": {"d_model": 384, "num_layers": 4, "nhead": 6, "dim_feedforward": 1536},
        "50m": {"d_model": 768, "num_layers": 6, "nhead": 8, "dim_feedforward": 3072},
        "100m": {"d_model": 1024, "num_layers": 8, "nhead": 8, "dim_feedforward": 4096},
        "250m": {"d_model": 1280, "num_layers": 12, "nhead": 10, "dim_feedforward": 5120},
        "500m": {"d_model": 1536, "num_layers": 16, "nhead": 12, "dim_feedforward": 6144},
        "1b": {"d_model": 2048, "num_layers": 20, "nhead": 16, "dim_feedforward": 8192},
    }
    selected_config = model_configs[args.model_size]

    print("="*80)
    print(f"HLXL BRAIN - {args.model_size.upper()} PARAMETER ALL VARIANTS TRAINING")
    print("English -> (HLXL | LC-R | LC-T | LC-B)")
    print("="*80)
    print(f"Model size: {args.model_size}")
    print(f"  d_model: {selected_config['d_model']}")
    print(f"  num_layers: {selected_config['num_layers']}")
    print(f"  nhead: {selected_config['nhead']}")
    print(f"  dim_feedforward: {selected_config['dim_feedforward']}")
    print()
    print(f"Training configuration:")
    print(f"  Epochs: {args.epochs}")
    print(f"  Batch size: {args.batch_size}")
    print(f"  Gradient accumulation: {args.gradient_accumulation}")
    print(f"  Effective batch size: {args.batch_size * args.gradient_accumulation}")
    print(f"  Learning rate: {args.lr}")
    print(f"  Mixed precision (FP16): {not args.no_fp16}")
    print(f"  Corpus: {args.corpus_path}")
    print()

    # Device selection
    if args.cpu:
        device = "cpu"
        print("WARNING: Training 1B model on CPU will be extremely slow!")
    elif args.device:
        device = args.device
    else:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"Device: {device}")
    if device == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"CUDA Version: {torch.version.cuda}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    print()

    # Create tokenizer
    print("Creating tokenizer...")
    tokenizer = create_tokenizer()
    print(f"Tokenizer created: {tokenizer.vocab_size} tokens")
    print()

    # Create model with specified size
    print(f"Creating {args.model_size} parameter model...")
    model = create_model_scaled(vocab_size=tokenizer.vocab_size, target_params=args.model_size, dropout=0.1)
    param_count = model.count_parameters()
    print(f"Model created: {param_count:,} parameters ({param_count/1e9:.3f}B)")
    print(f"Model size: {model.get_model_size_mb():.2f} MB (FP32)")
    print()

    # Enable gradient checkpointing if requested
    if not args.no_gradient_checkpointing and device != "cpu":
        enable_gradient_checkpointing(model)

    # Create dataloaders
    print("Loading all-variants dataset...")
    train_loader, val_loader = create_all_variants_dataloaders(
        corpus_path=args.corpus_path,
        tokenizer=tokenizer,
        batch_size=args.batch_size,
        seq_length=args.seq_length,
        train_ratio=args.train_ratio,
        balance_formats=not args.no_balance,
    )

    print(f"Dataset loaded")
    print(f"  - Train batches: {len(train_loader)}")
    print(f"  - Val batches: {len(val_loader)}")
    print()

    # Create trainer
    print("Creating trainer...")
    trainer = Trainer1B(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        learning_rate=args.lr,
        weight_decay=args.weight_decay,
        max_grad_norm=args.max_grad_norm,
        warmup_steps=args.warmup_steps,
        gradient_accumulation_steps=args.gradient_accumulation,
        device=device,
        checkpoint_dir=args.checkpoint_dir,
        use_fp16=not args.no_fp16,
    )
    print(f"Trainer created")
    print()

    # Training configuration summary
    print("="*80)
    print("STARTING TRAINING")
    print("="*80)
    print(f"Task: English->All HLX Variants Translation ({args.model_size.upper()} Model)")
    print(f"Formats: HLXL, LC-R, LC-T, LC-B")
    print(f"Epochs: {args.epochs}")
    print(f"Batch size: {args.batch_size} (effective: {args.batch_size * args.gradient_accumulation})")
    print(f"Learning rate: {args.lr}")
    print(f"Mixed precision: {'Yes (FP16)' if not args.no_fp16 else 'No (FP32)'}")
    print(f"Parameters: {param_count:,} ({param_count/1e9:.3f}B)")
    print("="*80)
    print()

    # Test prompts for each format
    test_prompts = [
        "[HLXL] Search for documents",
        "[LC-R] Search for documents",
        "[LC-T] Search for documents",
        "[LC-B] Search for documents",
    ]

    # Generate initial samples
    print("Generating baseline samples (before training)...")
    for prompt in test_prompts[:2]:
        sample = generate_sample(model, tokenizer, device, prompt, max_tokens=30, use_fp16=not args.no_fp16)
        print(f"  {prompt[:30]}... -> {sample[:50]}...")
    print()

    # Training loop
    print(f"Starting {args.model_size} model training...")
    print()

    best_val_loss = float('inf')
    start_time = time.time()

    try:
        for epoch in range(args.epochs):
            epoch_start = time.time()
            current_epoch = epoch + 1
            trainer.epoch = epoch

            # Train
            train_loss = trainer.train_epoch()
            trainer.train_losses.append(train_loss)

            # Validate
            val_loss = trainer.validate()
            trainer.val_losses.append(val_loss)

            epoch_time = time.time() - epoch_start

            # Log
            if current_epoch % args.log_interval == 0 or epoch == 0 or epoch == args.epochs - 1:
                current_lr = trainer.optimizer.param_groups[0]['lr']

                # GPU memory stats
                if device == "cuda":
                    mem_used = torch.cuda.max_memory_allocated() / 1024**3
                    mem_reserved = torch.cuda.memory_reserved() / 1024**3
                    mem_str = f" | GPU: {mem_used:.1f}/{mem_reserved:.1f} GB"
                else:
                    mem_str = ""

                print(f"Epoch {current_epoch:02d}/{args.epochs} | "
                      f"Train: {train_loss:.4f} | "
                      f"Val: {val_loss:.4f} | "
                      f"LR: {current_lr:.2e} | "
                      f"Time: {epoch_time:.1f}s{mem_str}")

            # Save best checkpoint
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                trainer.best_val_loss = val_loss
                trainer.save_checkpoint(f"best_model_all_variants_{args.model_size}.pt")

            # Save periodic checkpoint every 10 epochs
            if current_epoch % 10 == 0:
                trainer.save_checkpoint(f"checkpoint_all_variants_{args.model_size}_epoch{current_epoch}.pt")

            # Generate samples
            if current_epoch % args.sample_interval == 0:
                print(f"\n--- Sample Generation (Epoch {current_epoch}) ---")
                sample_english = "Represent nothing"
                for fmt in ["HLXL", "LC-R", "LC-T", "LC-B"]:
                    output = generate_translation(model, tokenizer, device, sample_english, fmt, max_tokens=50, use_fp16=not args.no_fp16)
                    print(f"  [{fmt}] {sample_english} -> {output[:60]}")
                print()

        # Save final checkpoint
        trainer.save_checkpoint(f"all_variants_{args.model_size}_final_epoch{args.epochs}.pt")

        total_time = time.time() - start_time

        print()
        print("="*80)
        print(f"{args.model_size.upper()} MODEL ALL VARIANTS TRAINING COMPLETE")
        print("="*80)
        print(f"Model: {param_count:,} parameters ({param_count/1e9:.3f}B)")
        print(f"Epochs trained: {args.epochs}")
        print(f"Total time: {total_time/60:.1f} minutes ({total_time/3600:.2f} hours)")
        print(f"Average time per epoch: {total_time/args.epochs:.1f} seconds")
        print()
        print(f"Best validation loss: {best_val_loss:.4f}")
        print(f"Final train loss: {trainer.train_losses[-1]:.4f}")
        print(f"Final val loss: {trainer.val_losses[-1]:.4f}")
        print()

        # Save training history
        print(f"Saving training history to {args.save_history}...")
        history = trainer.get_history()
        history['task'] = f'English->All HLX Variants ({args.model_size.upper()} Model)'
        history['model_size'] = args.model_size
        history['formats'] = ['HLXL', 'LC-R', 'LC-T', 'LC-B']
        history['epochs'] = args.epochs
        history['model_params'] = param_count
        history['total_time_seconds'] = total_time
        history['timestamp'] = datetime.now().isoformat()
        history['config'] = {
            'd_model': selected_config['d_model'],
            'num_layers': selected_config['num_layers'],
            'nhead': selected_config['nhead'],
            'dim_feedforward': selected_config['dim_feedforward'],
            'batch_size': args.batch_size,
            'gradient_accumulation': args.gradient_accumulation,
            'learning_rate': args.lr,
            'mixed_precision': not args.no_fp16,
        }

        with open(args.save_history, 'w') as f:
            json.dump(history, f, indent=2)
        print(f"History saved")
        print()

        # Final generation test for all formats
        print("="*80)
        print("FINAL GENERATION TEST - ALL FORMATS")
        print("="*80)

        test_inputs = [
            "Represent nothing",
            "Represent true",
            "Number forty-two",
            "Pi constant",
            "Search for documents",
        ]

        for english in test_inputs:
            print(f"\nEnglish: {english}")
            for fmt in ["HLXL", "LC-R", "LC-T", "LC-B"]:
                output = generate_translation(model, tokenizer, device, english, fmt, max_tokens=80, use_fp16=not args.no_fp16)
                print(f"  {fmt}: {output[:80]}")

        print()
        print("Checkpoints saved in:", args.checkpoint_dir)
        print(f"  - best_model_all_variants_{args.model_size}.pt (lowest validation loss)")
        print(f"  - checkpoint_all_variants_{args.model_size}_epoch*.pt (every 10 epochs)")
        print(f"  - all_variants_{args.model_size}_final_epoch{args.epochs}.pt (end of training)")
        print()

        print("="*80)
        print(f"SUCCESS - {args.model_size.upper()} Model trained on all HLX family formats!")
        print("="*80)

    except KeyboardInterrupt:
        print()
        print("="*80)
        print("TRAINING INTERRUPTED")
        print("="*80)
        print("Saving checkpoint...")
        trainer.save_checkpoint(f"all_variants_{args.model_size}_interrupted.pt")
        print(f"Checkpoint saved: all_variants_{args.model_size}_interrupted.pt")
        print()
        sys.exit(1)

    except RuntimeError as e:
        if "out of memory" in str(e).lower():
            print()
            print("="*80)
            print("OUT OF MEMORY ERROR")
            print("="*80)
            print(f"Error: {e}")
            print()
            print("Suggestions:")
            print("  1. Use smaller model: --model-size 100m or --model-size 50m")
            print("  2. Reduce batch size: --batch-size 8 or --batch-size 4")
            print("  3. Increase gradient accumulation: --gradient-accumulation 4")
            print("  4. Ensure mixed precision is enabled (remove --no-fp16)")
            print("  5. Try on a GPU with more memory (1B needs 24GB+)")
            print()
            sys.exit(1)
        else:
            raise

    except Exception as e:
        print()
        print("="*80)
        print("TRAINING FAILED")
        print("="*80)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
