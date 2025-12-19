"""
HLXL Brain - Training Loop

Minimal training loop for tiny transformer on LC-R corpus.

Features:
- AdamW optimizer with weight decay
- Cosine learning rate schedule with warmup
- Gradient clipping
- Loss logging
- Checkpoint saving
- Validation loop

Target: Train model to generate valid LC-R contracts.
"""

import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts
from torch.utils.data import DataLoader
from pathlib import Path
from typing import Optional, Dict
import json
from datetime import datetime


class HLXLTrainer:
    """
    Trainer for HLXL transformer model.

    Implements standard training loop with:
    - Loss calculation (cross-entropy)
    - Gradient clipping
    - Learning rate scheduling
    - Checkpointing
    - Validation
    """

    def __init__(
        self,
        model,
        train_loader: DataLoader,
        val_loader: DataLoader,
        learning_rate: float = 1e-3,
        weight_decay: float = 0.01,
        max_grad_norm: float = 1.0,
        warmup_steps: int = 100,
        device: Optional[str] = None,
        checkpoint_dir: str = "checkpoints",
        use_amp: bool = False,
    ):
        """
        Initialize trainer.

        Args:
            model: HLXLTransformer model
            train_loader: Training data loader
            val_loader: Validation data loader
            learning_rate: Initial learning rate
            weight_decay: Weight decay for AdamW
            max_grad_norm: Max gradient norm for clipping
            warmup_steps: Number of warmup steps
            device: Device to train on (auto-detect if None)
            checkpoint_dir: Directory to save checkpoints
        """
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.max_grad_norm = max_grad_norm
        self.warmup_steps = warmup_steps
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.use_amp = use_amp

        # Device
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        self.model.to(self.device)

        # Mixed precision scaler
        self.scaler = torch.cuda.amp.GradScaler() if use_amp else None

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
            T_0=len(train_loader),  # Restart every epoch
            T_mult=1,
            eta_min=learning_rate * 0.1,
        )

        # Loss function: Cross-entropy for next token prediction
        # Note: We don't ignore padding in loss calculation since sequences are pre-padded
        self.criterion = nn.CrossEntropyLoss()

        # Training state
        self.global_step = 0
        self.epoch = 0
        self.best_val_loss = float('inf')

        # History
        self.train_losses = []
        self.val_losses = []
        self.learning_rates = []

    def train_epoch(self) -> float:
        """
        Train for one epoch.

        Returns:
            Average training loss for the epoch
        """
        self.model.train()
        total_loss = 0.0
        num_batches = 0

        for batch_idx, (input_ids, labels) in enumerate(self.train_loader):
            # Move to device
            input_ids = input_ids.to(self.device)
            labels = labels.to(self.device)

            # Forward pass with mixed precision
            self.optimizer.zero_grad()

            if self.use_amp:
                with torch.cuda.amp.autocast():
                    logits = self.model(input_ids)
                    # Compute loss
                    loss = self.criterion(
                        logits.view(-1, logits.size(-1)),
                        labels.view(-1),
                    )

                # Backward pass with gradient scaling
                self.scaler.scale(loss).backward()

                # Gradient clipping
                self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(),
                    self.max_grad_norm
                )

                # Optimizer step
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                logits = self.model(input_ids)
                # Compute loss
                loss = self.criterion(
                    logits.view(-1, logits.size(-1)),
                    labels.view(-1),
                )

                # Backward pass
                loss.backward()

                # Gradient clipping
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(),
                    self.max_grad_norm
                )

                # Optimizer step
                self.optimizer.step()

            # Learning rate schedule
            if self.global_step >= self.warmup_steps:
                self.scheduler.step()
            else:
                # Linear warmup
                lr_scale = min(1.0, (self.global_step + 1) / self.warmup_steps)
                for param_group in self.optimizer.param_groups:
                    param_group['lr'] = self.learning_rate * lr_scale

            # Track metrics
            total_loss += loss.item()
            num_batches += 1
            self.global_step += 1

            # Log current learning rate
            current_lr = self.optimizer.param_groups[0]['lr']
            self.learning_rates.append(current_lr)

        avg_loss = total_loss / num_batches
        return avg_loss

    @torch.no_grad()
    def validate(self) -> float:
        """
        Run validation.

        Returns:
            Average validation loss
        """
        self.model.eval()
        total_loss = 0.0
        num_batches = 0

        for input_ids, labels in self.val_loader:
            # Move to device
            input_ids = input_ids.to(self.device)
            labels = labels.to(self.device)

            # Forward pass
            logits = self.model(input_ids)

            # Compute loss
            loss = self.criterion(
                logits.view(-1, logits.size(-1)),
                labels.view(-1),
            )

            total_loss += loss.item()
            num_batches += 1

        avg_loss = total_loss / num_batches
        return avg_loss

    def train(self, num_epochs: int, log_interval: int = 10) -> Dict:
        """
        Train for multiple epochs.

        Args:
            num_epochs: Number of epochs to train
            log_interval: Log every N epochs

        Returns:
            Training history dict
        """
        print(f"Training on {self.device}")
        print(f"Model parameters: {self.model.count_parameters():,}")
        print(f"Train batches: {len(self.train_loader)}")
        print(f"Val batches: {len(self.val_loader)}")
        print()

        for epoch in range(num_epochs):
            self.epoch = epoch

            # Train
            train_loss = self.train_epoch()
            self.train_losses.append(train_loss)

            # Validate
            val_loss = self.validate()
            self.val_losses.append(val_loss)

            # Log
            if (epoch + 1) % log_interval == 0 or epoch == 0 or epoch == num_epochs - 1:
                current_lr = self.optimizer.param_groups[0]['lr']
                print(f"Epoch {epoch+1}/{num_epochs} | "
                      f"Train Loss: {train_loss:.4f} | "
                      f"Val Loss: {val_loss:.4f} | "
                      f"LR: {current_lr:.6f}")

            # Save best checkpoint
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                self.save_checkpoint(f"best_model_epoch{epoch+1}.pt")

            # Save periodic checkpoint
            if (epoch + 1) % 50 == 0:
                self.save_checkpoint(f"checkpoint_epoch{epoch+1}.pt")

        # Save final checkpoint
        self.save_checkpoint("final_model.pt")

        print("\nTraining complete!")
        print(f"Best validation loss: {self.best_val_loss:.4f}")

        return self.get_history()

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
        }

        torch.save(checkpoint, checkpoint_path)

    def load_checkpoint(self, checkpoint_path: str) -> None:
        """Load model checkpoint."""
        checkpoint = torch.load(checkpoint_path, map_location=self.device, weights_only=False)

        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        self.epoch = checkpoint['epoch']
        self.global_step = checkpoint['global_step']
        self.best_val_loss = checkpoint['best_val_loss']
        self.train_losses = checkpoint['train_losses']
        self.val_losses = checkpoint['val_losses']

    def get_history(self) -> Dict:
        """Get training history."""
        return {
            'train_losses': self.train_losses,
            'val_losses': self.val_losses,
            'learning_rates': self.learning_rates,
            'best_val_loss': self.best_val_loss,
            'epochs_trained': self.epoch + 1,
            'global_steps': self.global_step,
        }

    def save_history(self, filepath: str) -> None:
        """Save training history to JSON."""
        history = self.get_history()
        with open(filepath, 'w') as f:
            json.dump(history, f, indent=2)


if __name__ == "__main__":
    # Quick test
    from model import create_model
    from tokenizer import create_tokenizer
    from data import create_dataloaders

    print("Testing trainer...")

    # Create components
    tokenizer = create_tokenizer()
    model = create_model()
    corpus_path = "/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md"

    train_loader, val_loader = create_dataloaders(
        corpus_path=corpus_path,
        tokenizer=tokenizer,
        batch_size=4,
        seq_length=64,
    )

    # Create trainer
    trainer = HLXLTrainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        learning_rate=1e-3,
        device="cpu",
    )

    print(f"✓ Trainer initialized")
    print(f"✓ Device: {trainer.device}")
    print(f"✓ Optimizer: AdamW with {len(list(model.parameters()))} parameter groups")
    print(f"✓ Scheduler: CosineAnnealingWarmRestarts")

    # Train for 2 epochs
    print(f"\nRunning 2 epoch test...")
    history = trainer.train(num_epochs=2, log_interval=1)

    print(f"✓ Training completed")
    print(f"✓ Train loss: {history['train_losses'][-1]:.4f}")
    print(f"✓ Val loss: {history['val_losses'][-1]:.4f}")

    # Test checkpoint save/load
    trainer.save_checkpoint("test_checkpoint.pt")
    print(f"✓ Checkpoint saved")

    # Test history save
    trainer.save_history("test_history.json")
    print(f"✓ History saved")

    print(f"\n✓ Trainer ready for production training")
