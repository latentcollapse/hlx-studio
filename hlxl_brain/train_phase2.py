#!/usr/bin/env python3
"""
HLXL Brain - Phase 1 Continued Training Script

Train Phase 2: Domain Knowledge (Epochs 6-30)

This script resumes from the Day 4 checkpoint and trains on the expanded corpus
with 388 new semantic grounding examples.

Usage:
    python3 train_phase1.py --epochs 25 --batch-size 32 --lr 1e-3

Features:
- Resume from existing checkpoint
- Start epoch tracking
- Phase identification
- Sample generation every 5 epochs
- Live loss monitoring
"""

import argparse
import sys
from pathlib import Path
import torch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tokenizer import create_tokenizer
from model import create_model
from data import create_dataloaders
from trainer import HLXLTrainer


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="HLXL Brain Phase 1 Training")

    # Phase-specific arguments
    parser.add_argument("--resume", type=str, default="checkpoints/phase1_final_epoch30.pt",
                        help="Path to checkpoint to resume from (default: checkpoints/phase1_final_epoch30.pt)")
    parser.add_argument("--start-epoch", type=int, default=6,
                        help="Starting epoch number (default: 6 for Phase 1)")
    parser.add_argument("--phase", type=str, default="Phase 2: Domain Knowledge",
                        help="Phase name for logging")

    # Training hyperparameters
    parser.add_argument("--epochs", type=int, default=25,
                        help="Number of training epochs (default: 25)")
    parser.add_argument("--batch-size", type=int, default=32,
                        help="Batch size (default: 32)")
    parser.add_argument("--lr", type=float, default=1e-3,
                        help="Learning rate (default: 1e-3)")
    parser.add_argument("--weight-decay", type=float, default=0.01,
                        help="Weight decay (default: 0.01)")
    parser.add_argument("--max-grad-norm", type=float, default=1.0,
                        help="Max gradient norm for clipping (default: 1.0)")
    parser.add_argument("--warmup-steps", type=int, default=100,
                        help="Learning rate warmup steps (default: 100)")

    # Model architecture
    parser.add_argument("--d-model", type=int, default=128,
                        help="Model dimension (default: 128)")
    parser.add_argument("--num-layers", type=int, default=2,
                        help="Number of transformer layers (default: 2)")
    parser.add_argument("--nhead", type=int, default=4,
                        help="Number of attention heads (default: 4)")
    parser.add_argument("--dim-feedforward", type=int, default=512,
                        help="FFN dimension (default: 512)")
    parser.add_argument("--dropout", type=float, default=0.1,
                        help="Dropout rate (default: 0.1)")

    # Dataset
    parser.add_argument("--corpus-path", type=str,
                        default="corpus_combined_phase2.md",
                        help="Path to combined corpus (default: corpus_combined_phase2.md)")
    parser.add_argument("--seq-length", type=int, default=128,
                        help="Sequence length (default: 128)")
    parser.add_argument("--stride", type=int, default=64,
                        help="Sliding window stride (default: 64)")
    parser.add_argument("--train-ratio", type=float, default=0.8,
                        help="Train/val split ratio (default: 0.8)")

    # Logging and checkpointing
    parser.add_argument("--log-interval", type=int, default=5,
                        help="Log every N epochs (default: 5)")
    parser.add_argument("--sample-interval", type=int, default=5,
                        help="Generate samples every N epochs (default: 5)")
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints",
                        help="Checkpoint directory (default: checkpoints)")
    parser.add_argument("--save-history", type=str, default="training_history_phase2.json",
                        help="Path to save training history (default: training_history_phase2.json)")

    # Device
    parser.add_argument("--device", type=str, default=None,
                        help="Device to train on (default: auto-detect)")
    parser.add_argument("--cpu", action="store_true",
                        help="Force CPU training")

    return parser.parse_args()


def generate_sample(model, tokenizer, device, prompt_text="", max_tokens=50):
    """Generate a sample from the model."""
    model.eval()

    if prompt_text:
        # Tokenize prompt
        prompt_ids = tokenizer.encode(prompt_text, add_special_tokens=True)
        prompt = torch.tensor([prompt_ids], dtype=torch.long).to(device)
    else:
        # Start with BOS token
        prompt = torch.tensor([[tokenizer.bos_token_id]], dtype=torch.long).to(device)

    with torch.no_grad():
        generated = model.generate(prompt, max_new_tokens=max_tokens, temperature=0.0)

    generated_text = tokenizer.decode(generated[0].cpu().tolist(), skip_special_tokens=False)
    return generated_text


def main():
    """Main training function."""
    args = parse_args()

    print("="*80)
    print("HLXL BRAIN - PHASE 1 CONTINUED TRAINING")
    print("="*80)
    print(f"Phase: {args.phase}")
    print(f"Starting epoch: {args.start_epoch}")
    print(f"Training epochs: {args.epochs} (epochs {args.start_epoch}-{args.start_epoch + args.epochs - 1})")
    print()

    # Device selection
    if args.cpu:
        device = "cpu"
    elif args.device:
        device = args.device
    else:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"Device: {device}")
    if device == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"CUDA Version: {torch.version.cuda}")
    print()

    # Create tokenizer
    print("Creating tokenizer...")
    tokenizer = create_tokenizer()
    print(f"✓ Tokenizer created: {tokenizer.vocab_size} tokens")
    print()

    # Create model
    print("Creating model...")
    model = create_model(
        vocab_size=tokenizer.vocab_size,
        d_model=args.d_model,
        nhead=args.nhead,
        num_layers=args.num_layers,
        dim_feedforward=args.dim_feedforward,
        dropout=args.dropout,
    )
    print(f"✓ Model created: {model.count_parameters():,} parameters ({model.get_model_size_mb():.2f} MB)")
    print()

    # Create dataloaders
    print("Loading expanded dataset...")
    train_loader, val_loader = create_dataloaders(
        corpus_path=args.corpus_path,
        tokenizer=tokenizer,
        batch_size=args.batch_size,
        seq_length=args.seq_length,
        stride=args.stride,
        train_ratio=args.train_ratio,
    )

    # Get dataset stats
    from data import LCRDataset
    dataset = LCRDataset(
        corpus_path=args.corpus_path,
        tokenizer=tokenizer,
        seq_length=args.seq_length,
        stride=args.stride,
        split="train",
        train_ratio=args.train_ratio,
    )
    stats = dataset.get_stats()

    print(f"✓ Expanded dataset loaded:")
    print(f"  - Total examples: {stats['total_examples']} (164 original + 388 new)")
    print(f"  - Train examples: {stats['train_examples']}")
    print(f"  - Val examples: {stats['val_examples']}")
    print(f"  - Train sequences: {stats['train_sequences']}")
    print(f"  - Val sequences: {stats['val_sequences']}")
    print(f"  - Sequence length: {stats['seq_length']}")
    print(f"  - Train batches: {len(train_loader)}")
    print(f"  - Val batches: {len(val_loader)}")
    print()

    # Create trainer
    print("Creating trainer...")
    trainer = HLXLTrainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        learning_rate=args.lr,
        weight_decay=args.weight_decay,
        max_grad_norm=args.max_grad_norm,
        warmup_steps=args.warmup_steps,
        device=device,
        checkpoint_dir=args.checkpoint_dir,
    )
    print(f"✓ Trainer created")
    print()

    # Load checkpoint if specified
    if args.resume and Path(args.resume).exists():
        print(f"Loading checkpoint from {args.resume}...")
        trainer.load_checkpoint(args.resume)
        print(f"✓ Checkpoint loaded")
        print(f"  - Previous epochs: {trainer.epoch + 1}")
        print(f"  - Previous steps: {trainer.global_step}")
        print(f"  - Best val loss: {trainer.best_val_loss:.4f}")
        print(f"  - Previous train loss: {trainer.train_losses[-1]:.4f}")
        print(f"  - Previous val loss: {trainer.val_losses[-1]:.4f}")
        print()

        # Adjust epoch numbering for Phase 1
        trainer.epoch = args.start_epoch - 1  # Will start from start_epoch
    else:
        print(f"⚠ Checkpoint not found at {args.resume}, starting from scratch")
        print()

    # Training configuration summary
    print("="*80)
    print("TRAINING CONFIGURATION")
    print("="*80)
    print(f"Phase: {args.phase}")
    print(f"Epochs: {args.epochs} (epochs {args.start_epoch}-{args.start_epoch + args.epochs - 1})")
    print(f"Batch size: {args.batch_size}")
    print(f"Learning rate: {args.lr}")
    print(f"Model: {model.count_parameters():,} parameters")
    print(f"Dataset: {stats['train_sequences']} train sequences, {stats['val_sequences']} val sequences")
    print(f"Device: {device}")
    print(f"Corpus: {args.corpus_path}")
    print("="*80)
    print()

    # Generate initial sample
    print("Generating baseline sample (before Phase 1 training)...")
    sample = generate_sample(model, tokenizer, device, max_tokens=30)
    print(f"Sample: {sample[:200]}...")
    print()

    # Start training
    print("Starting Phase 1 training...")
    print()

    try:
        for epoch in range(args.epochs):
            current_epoch = args.start_epoch + epoch

            # Train
            train_loss = trainer.train_epoch()
            trainer.train_losses.append(train_loss)

            # Validate
            val_loss = trainer.validate()
            trainer.val_losses.append(val_loss)

            # Log
            if (epoch + 1) % args.log_interval == 0 or epoch == 0 or epoch == args.epochs - 1:
                current_lr = trainer.optimizer.param_groups[0]['lr']
                print(f"Epoch {current_epoch}/{args.start_epoch + args.epochs - 1} | "
                      f"Train Loss: {train_loss:.4f} | "
                      f"Val Loss: {val_loss:.4f} | "
                      f"LR: {current_lr:.6f}")

            # Save best checkpoint
            if val_loss < trainer.best_val_loss:
                trainer.best_val_loss = val_loss
                trainer.save_checkpoint(f"best_model_phase2_epoch{current_epoch}.pt")

            # Save periodic checkpoint
            if (epoch + 1) % 5 == 0:
                trainer.save_checkpoint(f"checkpoint_epoch{current_epoch}.pt")

            # Generate sample
            if (epoch + 1) % args.sample_interval == 0:
                print(f"\n--- Sample Generation (Epoch {current_epoch}) ---")
                sample = generate_sample(model, tokenizer, device, max_tokens=30)
                print(f"Sample: {sample[:200]}")
                print()

        # Save final Phase 1 checkpoint
        trainer.save_checkpoint("phase2_final_epoch55.pt")

        print()
        print("="*80)
        print("PHASE 1 TRAINING COMPLETE")
        print("="*80)
        print(f"Phase: {args.phase}")
        print(f"Epochs trained: {args.start_epoch} → {args.start_epoch + args.epochs - 1}")
        print(f"Best validation loss: {trainer.best_val_loss:.4f}")
        print(f"Final train loss: {trainer.train_losses[-1]:.4f}")
        print(f"Final val loss: {trainer.val_losses[-1]:.4f}")
        print()

        # Save training history
        print(f"Saving training history to {args.save_history}...")
        history = trainer.get_history()
        history['phase'] = args.phase
        history['start_epoch'] = args.start_epoch
        history['end_epoch'] = args.start_epoch + args.epochs - 1

        import json
        with open(args.save_history, 'w') as f:
            json.dump(history, f, indent=2)
        print(f"✓ History saved")
        print()

        # Final generation test
        print("Generating final sample...")
        sample = generate_sample(model, tokenizer, device, max_tokens=50)
        print(f"Sample: {sample[:300]}")
        print()

        print("Checkpoints saved in:", args.checkpoint_dir)
        print("  - best_model_phase2_epoch*.pt (lowest validation loss)")
        print("  - checkpoint_epoch*.pt (every 5 epochs)")
        print("  - phase2_final_epoch55.pt (end of Phase 1)")
        print()

        print("="*80)
        print("SUCCESS - Phase 1 complete! Ready for Phase 2 or evaluation.")
        print("="*80)

    except KeyboardInterrupt:
        print()
        print("="*80)
        print("TRAINING INTERRUPTED")
        print("="*80)
        print("Saving checkpoint...")
        trainer.save_checkpoint("phase2_interrupted.pt")
        print("✓ Checkpoint saved: phase2_interrupted.pt")
        print()
        sys.exit(1)

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
