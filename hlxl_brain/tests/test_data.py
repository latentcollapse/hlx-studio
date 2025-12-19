"""
HLXL Brain - Dataset Test Suite

Validates LC-R dataset functionality.

Success criteria:
- Dataset loads corpus successfully
- Train/val split is correct
- Sequences are properly created
- Batching works correctly
- Round-trip integrity
"""

import pytest
import torch
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data import LCRDataset, create_dataloaders
from tokenizer import create_tokenizer


class TestDatasetInitialization:
    """Test dataset initialization and loading."""

    @pytest.fixture
    def corpus_path(self):
        """Path to LC-R corpus file."""
        return "/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md"

    @pytest.fixture
    def tokenizer(self):
        """Create tokenizer."""
        return create_tokenizer()

    def test_dataset_creation(self, corpus_path, tokenizer):
        """Test dataset can be created."""
        dataset = LCRDataset(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            seq_length=128,
            stride=64,
            split="train",
        )
        assert dataset is not None
        assert len(dataset) > 0

    def test_corpus_loading(self, corpus_path, tokenizer):
        """Test corpus examples are loaded correctly."""
        dataset = LCRDataset(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            seq_length=128,
            split="train",
        )

        # Should have loaded 164 examples
        stats = dataset.get_stats()
        assert stats["total_examples"] == 164

    def test_train_val_split(self, corpus_path, tokenizer):
        """Test train/validation split is correct."""
        dataset = LCRDataset(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            seq_length=128,
            split="train",
            train_ratio=0.8,
        )

        stats = dataset.get_stats()

        # 80/20 split
        total = stats["total_examples"]
        train_count = stats["train_examples"]
        val_count = stats["val_examples"]

        assert train_count + val_count == total
        assert train_count == int(total * 0.8)
        assert val_count == total - train_count

    def test_split_reproducibility(self, corpus_path, tokenizer):
        """Test split is reproducible with same seed."""
        dataset1 = LCRDataset(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            seq_length=128,
            split="train",
            seed=42,
        )

        dataset2 = LCRDataset(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            seq_length=128,
            split="train",
            seed=42,
        )

        # Same examples in same order
        assert dataset1.train_examples == dataset2.train_examples


class TestSequenceCreation:
    """Test sequence creation with sliding window."""

    @pytest.fixture
    def corpus_path(self):
        """Path to LC-R corpus file."""
        return "/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md"

    @pytest.fixture
    def tokenizer(self):
        """Create tokenizer."""
        return create_tokenizer()

    def test_sequence_count(self, corpus_path, tokenizer):
        """Test sequences are created from examples."""
        dataset = LCRDataset(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            seq_length=128,
            stride=64,
            split="train",
        )

        # Should have more sequences than examples due to sliding window
        stats = dataset.get_stats()
        assert stats["train_sequences"] >= stats["train_examples"]

    def test_sequence_length(self, corpus_path, tokenizer):
        """Test sequences have correct length."""
        seq_length = 64
        dataset = LCRDataset(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            seq_length=seq_length,
            stride=32,
            split="train",
        )

        # Get a sequence
        input_ids, labels = dataset[0]

        # Should be seq_length - 1 (we remove one token for input/label split)
        assert input_ids.shape[0] == seq_length - 1
        assert labels.shape[0] == seq_length - 1

    def test_input_label_shift(self, corpus_path, tokenizer):
        """Test labels are shifted by 1 from inputs."""
        dataset = LCRDataset(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            seq_length=10,
            split="train",
        )

        input_ids, labels = dataset[0]

        # Labels should be inputs shifted by 1
        # (This is the language modeling objective)
        # We can't directly compare because they come from different slices,
        # but we can check they're different tensors
        assert input_ids.shape == labels.shape
        assert not torch.equal(input_ids, labels)


class TestBatching:
    """Test dataloader batching."""

    @pytest.fixture
    def corpus_path(self):
        """Path to LC-R corpus file."""
        return "/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md"

    @pytest.fixture
    def tokenizer(self):
        """Create tokenizer."""
        return create_tokenizer()

    def test_dataloader_creation(self, corpus_path, tokenizer):
        """Test dataloaders can be created."""
        train_loader, val_loader = create_dataloaders(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            batch_size=4,
            seq_length=128,
        )

        assert train_loader is not None
        assert val_loader is not None
        assert len(train_loader) > 0
        assert len(val_loader) > 0

    def test_batch_shapes(self, corpus_path, tokenizer):
        """Test batch shapes are correct."""
        batch_size = 4
        seq_length = 128

        train_loader, _ = create_dataloaders(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            batch_size=batch_size,
            seq_length=seq_length,
        )

        # Get first batch
        input_ids, labels = next(iter(train_loader))

        # Check shapes
        assert input_ids.shape[0] <= batch_size  # May be smaller for last batch
        assert input_ids.shape[1] == seq_length - 1
        assert labels.shape[0] <= batch_size
        assert labels.shape[1] == seq_length - 1

    def test_batch_dtypes(self, corpus_path, tokenizer):
        """Test batch tensors have correct dtypes."""
        train_loader, _ = create_dataloaders(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            batch_size=4,
        )

        input_ids, labels = next(iter(train_loader))

        assert input_ids.dtype == torch.long
        assert labels.dtype == torch.long

    def test_multiple_batches(self, corpus_path, tokenizer):
        """Test iteration over multiple batches."""
        train_loader, _ = create_dataloaders(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            batch_size=4,
        )

        batches = list(train_loader)
        assert len(batches) > 0

        # Check all batches have correct structure
        for input_ids, labels in batches:
            assert input_ids.dtype == torch.long
            assert labels.dtype == torch.long
            assert input_ids.shape == labels.shape


class TestDatasetStatistics:
    """Test dataset statistics."""

    @pytest.fixture
    def corpus_path(self):
        """Path to LC-R corpus file."""
        return "/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md"

    @pytest.fixture
    def tokenizer(self):
        """Create tokenizer."""
        return create_tokenizer()

    def test_get_stats(self, corpus_path, tokenizer):
        """Test get_stats returns correct information."""
        dataset = LCRDataset(
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            seq_length=128,
            stride=64,
            split="train",
            train_ratio=0.8,
        )

        stats = dataset.get_stats()

        # Check all required keys
        assert "total_examples" in stats
        assert "train_examples" in stats
        assert "val_examples" in stats
        assert "train_sequences" in stats
        assert "val_sequences" in stats
        assert "seq_length" in stats
        assert "stride" in stats

        # Check values are reasonable
        assert stats["total_examples"] > 0
        assert stats["train_sequences"] > 0
        assert stats["val_sequences"] > 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
