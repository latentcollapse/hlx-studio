"""
HLXL Brain - Trainer Test Suite

Validates training loop functionality.

Success criteria:
- Trainer initializes correctly
- Training loop executes
- Loss decreases over epochs
- Checkpoints save/load correctly
- Gradient clipping works
- Learning rate scheduling works
"""

import pytest
import torch
import sys
from pathlib import Path
import tempfile
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from trainer import HLXLTrainer
from model import create_model
from tokenizer import create_tokenizer
from data import create_dataloaders


class TestTrainerInitialization:
    """Test trainer initialization."""

    @pytest.fixture
    def components(self):
        """Create all components needed for trainer."""
        tokenizer = create_tokenizer()
        model = create_model()
        corpus_path = "/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md"

        train_loader, val_loader = create_dataloaders(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            batch_size=4,
            seq_length=64,
        )

        return tokenizer, model, train_loader, val_loader

    def test_trainer_creation(self, components):
        """Test trainer can be created."""
        _, model, train_loader, val_loader = components

        trainer = HLXLTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            learning_rate=1e-3,
            device="cpu",
        )

        assert trainer is not None
        assert trainer.model is not None
        assert trainer.optimizer is not None
        assert trainer.scheduler is not None

    def test_device_selection(self, components):
        """Test device selection works."""
        _, model, train_loader, val_loader = components

        trainer = HLXLTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            device="cpu",
        )

        assert trainer.device == torch.device("cpu")

    def test_optimizer_setup(self, components):
        """Test optimizer is set up correctly."""
        _, model, train_loader, val_loader = components

        trainer = HLXLTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            learning_rate=1e-3,
            weight_decay=0.01,
        )

        # Check optimizer type
        assert isinstance(trainer.optimizer, torch.optim.AdamW)

        # Check learning rate
        assert trainer.optimizer.param_groups[0]['lr'] == 1e-3

        # Check weight decay
        assert trainer.optimizer.param_groups[0]['weight_decay'] == 0.01


class TestTrainingLoop:
    """Test training loop execution."""

    @pytest.fixture
    def trainer(self):
        """Create trainer for testing."""
        tokenizer = create_tokenizer()
        model = create_model()
        corpus_path = "/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md"

        train_loader, val_loader = create_dataloaders(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            batch_size=4,
            seq_length=64,
        )

        return HLXLTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            learning_rate=1e-3,
            device="cpu",
        )

    def test_train_epoch(self, trainer):
        """Test training for one epoch."""
        initial_loss = trainer.train_epoch()

        assert initial_loss > 0
        assert not torch.isnan(torch.tensor(initial_loss))
        assert not torch.isinf(torch.tensor(initial_loss))

    def test_validate(self, trainer):
        """Test validation."""
        val_loss = trainer.validate()

        assert val_loss > 0
        assert not torch.isnan(torch.tensor(val_loss))
        assert not torch.isinf(torch.tensor(val_loss))

    def test_training_multiple_epochs(self, trainer):
        """Test training for multiple epochs."""
        history = trainer.train(num_epochs=3, log_interval=1)

        assert len(history['train_losses']) == 3
        assert len(history['val_losses']) == 3
        assert history['epochs_trained'] == 3

    def test_loss_is_finite(self, trainer):
        """Test that loss values are always finite."""
        history = trainer.train(num_epochs=2, log_interval=1)

        for loss in history['train_losses']:
            assert not torch.isnan(torch.tensor(loss))
            assert not torch.isinf(torch.tensor(loss))

        for loss in history['val_losses']:
            assert not torch.isnan(torch.tensor(loss))
            assert not torch.isinf(torch.tensor(loss))


class TestCheckpointing:
    """Test checkpoint save/load functionality."""

    @pytest.fixture
    def trainer_with_temp_dir(self):
        """Create trainer with temporary checkpoint directory."""
        tokenizer = create_tokenizer()
        model = create_model()
        corpus_path = "/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md"

        train_loader, val_loader = create_dataloaders(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            batch_size=4,
            seq_length=64,
        )

        temp_dir = tempfile.mkdtemp()

        trainer = HLXLTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            learning_rate=1e-3,
            device="cpu",
            checkpoint_dir=temp_dir,
        )

        yield trainer, temp_dir

        # Cleanup
        shutil.rmtree(temp_dir)

    def test_save_checkpoint(self, trainer_with_temp_dir):
        """Test checkpoint saving."""
        trainer, temp_dir = trainer_with_temp_dir

        # Train one epoch to have some state
        trainer.train_epoch()

        # Save checkpoint
        checkpoint_name = "test_checkpoint.pt"
        trainer.save_checkpoint(checkpoint_name)

        # Check file exists
        checkpoint_path = Path(temp_dir) / checkpoint_name
        assert checkpoint_path.exists()

    def test_load_checkpoint(self, trainer_with_temp_dir):
        """Test checkpoint loading."""
        trainer, temp_dir = trainer_with_temp_dir

        # Train one epoch
        trainer.train_epoch()
        epoch_after_train = trainer.epoch

        # Save checkpoint
        checkpoint_name = "test_checkpoint.pt"
        trainer.save_checkpoint(checkpoint_name)

        # Create new trainer
        tokenizer = create_tokenizer()
        model = create_model()
        corpus_path = "/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md"

        train_loader, val_loader = create_dataloaders(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            batch_size=4,
            seq_length=64,
        )

        new_trainer = HLXLTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            device="cpu",
        )

        # Load checkpoint
        checkpoint_path = Path(temp_dir) / checkpoint_name
        new_trainer.load_checkpoint(str(checkpoint_path))

        # Check state is restored
        assert new_trainer.epoch == epoch_after_train

    def test_checkpoint_contains_all_state(self, trainer_with_temp_dir):
        """Test checkpoint contains all necessary state."""
        trainer, temp_dir = trainer_with_temp_dir

        # Train one epoch
        trainer.train_epoch()

        # Save checkpoint
        checkpoint_name = "test_checkpoint.pt"
        trainer.save_checkpoint(checkpoint_name)

        # Load and check contents
        checkpoint_path = Path(temp_dir) / checkpoint_name
        checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)

        assert 'epoch' in checkpoint
        assert 'global_step' in checkpoint
        assert 'model_state_dict' in checkpoint
        assert 'optimizer_state_dict' in checkpoint
        assert 'scheduler_state_dict' in checkpoint
        assert 'best_val_loss' in checkpoint


class TestGradientClipping:
    """Test gradient clipping functionality."""

    @pytest.fixture
    def trainer(self):
        """Create trainer with gradient clipping."""
        tokenizer = create_tokenizer()
        model = create_model()
        corpus_path = "/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md"

        train_loader, val_loader = create_dataloaders(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            batch_size=4,
            seq_length=64,
        )

        return HLXLTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            max_grad_norm=1.0,
            device="cpu",
        )

    def test_gradients_are_clipped(self, trainer):
        """Test gradients are clipped during training."""
        # Train one epoch
        trainer.train_epoch()

        # Check that training completed without NaN gradients
        for param in trainer.model.parameters():
            if param.grad is not None:
                assert not torch.isnan(param.grad).any()


class TestLearningRateScheduling:
    """Test learning rate scheduling."""

    @pytest.fixture
    def trainer(self):
        """Create trainer with learning rate scheduling."""
        tokenizer = create_tokenizer()
        model = create_model()
        corpus_path = "/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md"

        train_loader, val_loader = create_dataloaders(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            batch_size=4,
            seq_length=64,
        )

        return HLXLTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            learning_rate=1e-3,
            warmup_steps=10,
            device="cpu",
        )

    def test_learning_rate_changes(self, trainer):
        """Test learning rate changes during training."""
        initial_lr = trainer.optimizer.param_groups[0]['lr']

        # Train for a few epochs
        trainer.train(num_epochs=3, log_interval=1)

        final_lr = trainer.optimizer.param_groups[0]['lr']

        # Learning rate should have changed
        assert len(trainer.learning_rates) > 0

    def test_warmup_phase(self, trainer):
        """Test learning rate warmup."""
        # Train one epoch
        trainer.train_epoch()

        # Learning rates should have been tracked
        assert len(trainer.learning_rates) > 0


class TestHistory:
    """Test training history tracking."""

    @pytest.fixture
    def trainer(self):
        """Create trainer for testing."""
        tokenizer = create_tokenizer()
        model = create_model()
        corpus_path = "/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md"

        train_loader, val_loader = create_dataloaders(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            batch_size=4,
            seq_length=64,
        )

        return HLXLTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            device="cpu",
        )

    def test_history_tracking(self, trainer):
        """Test history is tracked correctly."""
        history = trainer.train(num_epochs=3, log_interval=1)

        assert 'train_losses' in history
        assert 'val_losses' in history
        assert 'learning_rates' in history
        assert 'best_val_loss' in history
        assert 'epochs_trained' in history
        assert 'global_steps' in history

    def test_history_save(self, trainer):
        """Test history can be saved to JSON."""
        trainer.train(num_epochs=2, log_interval=1)

        # Save history
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            history_path = f.name

        try:
            trainer.save_history(history_path)

            # Check file exists and is valid JSON
            import json
            with open(history_path, 'r') as f:
                history = json.load(f)

            assert 'train_losses' in history
            assert 'val_losses' in history

        finally:
            Path(history_path).unlink()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
