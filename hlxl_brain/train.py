#!/usr/bin/env python3
"""
HLXL Brain - Training Script

Run production training on LC-R corpus.

Usage:
    python3 train.py --epochs 100 --batch-size 32 --lr 1e-3

Features:
- Automatic device selection (CPU/CUDA)
- Progress logging
- Checkpoint saving
- Training history visualization
- Best model selection
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
    parser = argparse.ArgumentParser(description="Train HLXL Brain on LC-R corpus")

    # Training hyperparameters
    parser.add_argument("--epochs", type=int, default=100,
                        help="Number of training epochs (default: 100)")
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
                        default="/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md",
                        help="Path to LC-R corpus file")
    parser.add_argument("--seq-length", type=int, default=128,
                        help="Sequence length (default: 128)")
    parser.add_argument("--stride", type=int, default=64,
                        help="Sliding window stride (default: 64)")
    parser.add_argument("--train-ratio", type=float, default=0.8,
                        help="Train/val split ratio (default: 0.8)")

    # Logging and checkpointing
    parser.add_argument("--log-interval", type=int, default=10,
                        help="Log every N epochs (default: 10)")
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints",
                        help="Checkpoint directory (default: checkpoints)")
    parser.add_argument("--save-history", type=str, default="training_history.json",
                        help="Path to save training history (default: training_history.json)")

    # Device
    parser.add_argument("--device", type=str, default=None,
                        help="Device to train on (default: auto-detect)")
    parser.add_argument("--cpu", action="store_true",
                        help="Force CPU training")

    return parser.parse_args()


def main():
    """Main training function."""
    args = parse_args()

    print("="*80)
    print("HLXL BRAIN - TRAINING")
    print("="*80)
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
    print(model)
    print()

    # Create dataloaders
    print("Loading dataset...")
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

    print(f"✓ Dataset loaded:")
    print(f"  - Total examples: {stats['total_examples']}")
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
    print(f"  - Optimizer: AdamW (lr={args.lr}, weight_decay={args.weight_decay})")
    print(f"  - Scheduler: CosineAnnealingWarmRestarts")
    print(f"  - Gradient clipping: {args.max_grad_norm}")
    print(f"  - Warmup steps: {args.warmup_steps}")
    print()

    # Training configuration summary
    print("="*80)
    print("TRAINING CONFIGURATION")
    print("="*80)
    print(f"Epochs: {args.epochs}")
    print(f"Batch size: {args.batch_size}")
    print(f"Learning rate: {args.lr}")
    print(f"Model: {model.count_parameters():,} parameters")
    print(f"Dataset: {stats['train_sequences']} train sequences, {stats['val_sequences']} val sequences")
    print(f"Device: {device}")
    print("="*80)
    print()

    # Start training
    print("Starting training...")
    print()

    try:
        history = trainer.train(
            num_epochs=args.epochs,
            log_interval=args.log_interval,
        )

        print()
        print("="*80)
        print("TRAINING COMPLETE")
        print("="*80)
        print(f"Best validation loss: {history['best_val_loss']:.4f}")
        print(f"Final train loss: {history['train_losses'][-1]:.4f}")
        print(f"Final val loss: {history['val_losses'][-1]:.4f}")
        print(f"Epochs trained: {history['epochs_trained']}")
        print(f"Total steps: {history['global_steps']}")
        print()

        # Save training history
        print(f"Saving training history to {args.save_history}...")
        trainer.save_history(args.save_history)
        print(f"✓ History saved")
        print()

        print("Checkpoints saved in:", args.checkpoint_dir)
        print("  - best_model_*.pt (lowest validation loss)")
        print("  - final_model.pt (last epoch)")
        print()

        # Quick generation test
        print("Testing generation...")
        model.eval()
        prompt = torch.tensor([[tokenizer.bos_token_id]], dtype=torch.long).to(device)
        with torch.no_grad():
            generated = model.generate(prompt, max_new_tokens=20, temperature=0.0)

        generated_text = tokenizer.decode(generated[0].cpu().tolist(), skip_special_tokens=True)
        print(f"Sample generation: {generated_text}")
        print()

        print("="*80)
        print("SUCCESS - Model trained and ready for inference!")
        print("="*80)

    except KeyboardInterrupt:
        print()
        print("="*80)
        print("TRAINING INTERRUPTED")
        print("="*80)
        print("Saving checkpoint...")
        trainer.save_checkpoint("interrupted_model.pt")
        print("✓ Checkpoint saved: interrupted_model.pt")
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
