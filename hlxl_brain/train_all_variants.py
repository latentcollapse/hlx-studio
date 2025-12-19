#!/usr/bin/env python3
"""
HLXL Brain - All Variants Training

Train on English→(HLXL|LC-R|LC-T|LC-B) translation for all HLX family formats.

Usage:
    python3 train_all_variants.py --epochs 30
"""

import argparse
import sys
from pathlib import Path
import torch
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tokenizer import create_tokenizer
from model import create_model
from data_all_variants import create_all_variants_dataloaders
from trainer import HLXLTrainer


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="HLXL Brain All Variants Training")

    # Training hyperparameters
    parser.add_argument("--epochs", type=int, default=30,
                        help="Number of training epochs (default: 30)")
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
                        default="corpus_all_variants.md",
                        help="Path to corpus (default: corpus_all_variants.md)")
    parser.add_argument("--seq-length", type=int, default=256,
                        help="Sequence length (default: 256)")
    parser.add_argument("--train-ratio", type=float, default=0.8,
                        help="Train/val split ratio (default: 0.8)")
    parser.add_argument("--no-balance", action="store_true",
                        help="Don't balance formats (use all examples)")

    # Logging and checkpointing
    parser.add_argument("--log-interval", type=int, default=5,
                        help="Log every N epochs (default: 5)")
    parser.add_argument("--sample-interval", type=int, default=5,
                        help="Generate samples every N epochs (default: 5)")
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints",
                        help="Checkpoint directory (default: checkpoints)")
    parser.add_argument("--save-history", type=str, default="training_history_all_variants.json",
                        help="Path to save training history")

    # Device
    parser.add_argument("--device", type=str, default=None,
                        help="Device to train on (default: auto-detect)")
    parser.add_argument("--cpu", action="store_true",
                        help="Force CPU training")

    return parser.parse_args()


def generate_sample(model, tokenizer, device, prompt_text="[HLXL] Search for documents", max_tokens=50):
    """Generate a sample from the model."""
    model.eval()

    prompt_ids = tokenizer.encode(prompt_text, add_special_tokens=True)
    prompt = torch.tensor([prompt_ids], dtype=torch.long).to(device)

    with torch.no_grad():
        generated = model.generate(prompt, max_new_tokens=max_tokens, temperature=0.0)

    generated_text = tokenizer.decode(generated[0].cpu().tolist(), skip_special_tokens=False)
    return generated_text


def main():
    """Main training function."""
    args = parse_args()

    print("="*80)
    print("HLXL BRAIN - ALL VARIANTS TRAINING")
    print("English → (HLXL | LC-R | LC-T | LC-B)")
    print("="*80)
    print(f"Training on all HLX family formats")
    print(f"Epochs: {args.epochs}")
    print(f"Corpus: {args.corpus_path}")
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
    print(f"Tokenizer created: {tokenizer.vocab_size} tokens")
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
    print(f"Model created: {model.count_parameters():,} parameters ({model.get_model_size_mb():.2f} MB)")
    print()

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
    print(f"Trainer created")
    print()

    # Training configuration summary
    print("="*80)
    print("TRAINING CONFIGURATION")
    print("="*80)
    print(f"Task: English→All HLX Variants Translation")
    print(f"Formats: HLXL, LC-R, LC-T, LC-B")
    print(f"Epochs: {args.epochs}")
    print(f"Batch size: {args.batch_size}")
    print(f"Learning rate: {args.lr}")
    print(f"Model: {model.count_parameters():,} parameters")
    print(f"Dataset: {args.corpus_path}")
    print(f"Device: {device}")
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
        sample = generate_sample(model, tokenizer, device, prompt, max_tokens=30)
        print(f"  {prompt[:20]}... → {sample[:50]}...")
    print()

    # Start training
    print("Starting all-variants training...")
    print()

    best_val_loss = float('inf')

    try:
        for epoch in range(args.epochs):
            current_epoch = epoch + 1

            # Train
            train_loss = trainer.train_epoch()
            trainer.train_losses.append(train_loss)

            # Validate
            val_loss = trainer.validate()
            trainer.val_losses.append(val_loss)

            # Log
            if current_epoch % args.log_interval == 0 or epoch == 0 or epoch == args.epochs - 1:
                current_lr = trainer.optimizer.param_groups[0]['lr']
                print(f"Epoch {current_epoch}/{args.epochs} | "
                      f"Train Loss: {train_loss:.4f} | "
                      f"Val Loss: {val_loss:.4f} | "
                      f"LR: {current_lr:.6f}")

            # Save best checkpoint
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                trainer.best_val_loss = val_loss
                trainer.save_checkpoint(f"best_model_all_variants.pt")

            # Save periodic checkpoint
            if current_epoch % 10 == 0:
                trainer.save_checkpoint(f"checkpoint_all_variants_epoch{current_epoch}.pt")

            # Generate samples
            if current_epoch % args.sample_interval == 0:
                print(f"\n--- Sample Generation (Epoch {current_epoch}) ---")
                for prompt in test_prompts:
                    sample = generate_sample(model, tokenizer, device, prompt, max_tokens=60)
                    print(f"  {prompt}")
                    # Extract output after →
                    if " → " in sample:
                        output = sample.split(" → ", 1)[1]
                    else:
                        output = sample[len(prompt):]
                    print(f"    → {output[:100]}")
                print()

        # Save final checkpoint
        trainer.save_checkpoint(f"all_variants_final_epoch{args.epochs}.pt")

        print()
        print("="*80)
        print("ALL VARIANTS TRAINING COMPLETE")
        print("="*80)
        print(f"Epochs trained: {args.epochs}")
        print(f"Best validation loss: {best_val_loss:.4f}")
        print(f"Final train loss: {trainer.train_losses[-1]:.4f}")
        print(f"Final val loss: {trainer.val_losses[-1]:.4f}")
        print()

        # Save training history
        print(f"Saving training history to {args.save_history}...")
        history = trainer.get_history()
        history['task'] = 'English→All HLX Variants'
        history['formats'] = ['HLXL', 'LC-R', 'LC-T', 'LC-B']
        history['epochs'] = args.epochs
        history['timestamp'] = datetime.now().isoformat()

        with open(args.save_history, 'w') as f:
            json.dump(history, f, indent=2)
        print(f"History saved")
        print()

        # Final generation test for all formats
        print("="*80)
        print("FINAL GENERATION TEST - ALL FORMATS")
        print("="*80)

        test_inputs = [
            "Search for documents",
            "Filter active users",
            "Navigate to home",
        ]

        for english in test_inputs:
            print(f"\nEnglish: {english}")
            for fmt in ["HLXL", "LC-R", "LC-T", "LC-B"]:
                prompt = f"[{fmt}] {english}"
                sample = generate_sample(model, tokenizer, device, prompt, max_tokens=80)
                if " → " in sample:
                    output = sample.split(" → ", 1)[1]
                else:
                    output = sample[len(prompt):]
                # Clean output (remove padding, special tokens)
                output = output.replace("<pad>", "").replace("<eos>", "").strip()
                print(f"  {fmt}: {output[:80]}")

        print()
        print("Checkpoints saved in:", args.checkpoint_dir)
        print("  - best_model_all_variants.pt (lowest validation loss)")
        print("  - checkpoint_all_variants_epoch*.pt (every 10 epochs)")
        print(f"  - all_variants_final_epoch{args.epochs}.pt (end of training)")
        print()

        print("="*80)
        print("SUCCESS - Model trained on all HLX family formats!")
        print("="*80)

    except KeyboardInterrupt:
        print()
        print("="*80)
        print("TRAINING INTERRUPTED")
        print("="*80)
        print("Saving checkpoint...")
        trainer.save_checkpoint("all_variants_interrupted.pt")
        print("Checkpoint saved: all_variants_interrupted.pt")
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
