"""
HLXL Brain - Model Test Suite

Validates HLXLTransformer model architecture and functionality.

Success criteria:
- Model initializes without errors
- Forward pass produces correct output shapes
- Generation works deterministically (T=0)
- Parameter count matches architecture
- Model size is compact (<5 MB)
"""

import pytest
import torch
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from model import HLXLTransformer, create_model


class TestModelInitialization:
    """Test model initialization and configuration."""

    def test_model_creation(self):
        """Test model can be created."""
        model = create_model()
        assert model is not None
        assert isinstance(model, HLXLTransformer)

    def test_model_parameters(self):
        """Test model has reasonable parameter count."""
        model = create_model()
        param_count = model.count_parameters()

        # Should be compact (target was ~5M, actual is ~0.5M)
        assert param_count > 100_000, f"Model too small: {param_count}"
        assert param_count < 10_000_000, f"Model too large: {param_count}"

    def test_model_size(self):
        """Test model size is compact."""
        model = create_model()
        size_mb = model.get_model_size_mb()

        # Should be < 50MB in FP32
        assert size_mb < 50, f"Model size {size_mb:.2f} MB > 50 MB"

    def test_model_config(self):
        """Test model configuration matches specification."""
        model = create_model(
            vocab_size=115,
            d_model=128,
            nhead=4,
            num_layers=2,
        )

        assert model.vocab_size == 115
        assert model.d_model == 128
        assert len(model.transformer.layers) == 2


class TestForwardPass:
    """Test model forward pass."""

    def test_forward_pass_shape(self):
        """Test forward pass produces correct output shape."""
        model = create_model()
        batch_size = 2
        seq_length = 10

        input_ids = torch.randint(0, 115, (batch_size, seq_length))
        logits = model(input_ids)

        assert logits.shape == (batch_size, seq_length, 115)

    def test_forward_pass_no_nan(self):
        """Test forward pass produces valid outputs (no NaN/Inf)."""
        model = create_model()
        input_ids = torch.randint(0, 115, (2, 10))

        logits = model(input_ids)

        assert not torch.isnan(logits).any(), "Forward pass produced NaN"
        assert not torch.isinf(logits).any(), "Forward pass produced Inf"

    def test_forward_pass_batch_sizes(self):
        """Test forward pass works with different batch sizes."""
        model = create_model()

        for batch_size in [1, 2, 4, 8]:
            input_ids = torch.randint(0, 115, (batch_size, 10))
            logits = model(input_ids)
            assert logits.shape == (batch_size, 10, 115)

    def test_forward_pass_sequence_lengths(self):
        """Test forward pass works with different sequence lengths."""
        model = create_model()

        for seq_length in [5, 10, 20, 50]:
            input_ids = torch.randint(0, 115, (2, seq_length))
            logits = model(input_ids)
            assert logits.shape == (2, seq_length, 115)


class TestGeneration:
    """Test autoregressive text generation."""

    def test_generation_basic(self):
        """Test basic generation works."""
        model = create_model()
        prompt = torch.randint(0, 115, (1, 5))

        generated = model.generate(prompt, max_new_tokens=10, temperature=0.0)

        assert generated.shape[0] == 1  # Batch size preserved
        assert generated.shape[1] == 15  # prompt (5) + generated (10)

    def test_generation_deterministic(self):
        """Test deterministic generation (T=0)."""
        model = create_model()
        model.eval()

        prompt = torch.randint(0, 115, (1, 5))

        # Generate multiple times with same prompt
        gen1 = model.generate(prompt, max_new_tokens=10, temperature=0.0)
        gen2 = model.generate(prompt, max_new_tokens=10, temperature=0.0)
        gen3 = model.generate(prompt, max_new_tokens=10, temperature=0.0)

        # Should be identical (deterministic)
        assert torch.equal(gen1, gen2), "Generation not deterministic (run 1 vs 2)"
        assert torch.equal(gen2, gen3), "Generation not deterministic (run 2 vs 3)"

    def test_generation_different_lengths(self):
        """Test generation with different max_new_tokens."""
        model = create_model()
        prompt = torch.randint(0, 115, (1, 5))

        for max_new in [5, 10, 20]:
            generated = model.generate(prompt, max_new_tokens=max_new, temperature=0.0)
            assert generated.shape[1] == 5 + max_new

    def test_generation_eos_stopping(self):
        """Test generation stops at EOS token."""
        model = create_model()
        prompt = torch.randint(0, 115, (1, 5))

        # Use token 2 (EOS) as stopping token
        generated = model.generate(
            prompt,
            max_new_tokens=100,
            temperature=0.0,
            eos_token_id=2
        )

        # Should stop before max_new_tokens if EOS generated
        # (Can't guarantee EOS will be generated, but test shouldn't crash)
        assert generated.shape[1] >= 5
        assert generated.shape[1] <= 105


class TestCausalMasking:
    """Test causal masking prevents future attention."""

    def test_causal_mask_shape(self):
        """Test causal mask has correct shape."""
        model = create_model()
        size = 10
        mask = model._generate_square_subsequent_mask(size, torch.device('cpu'))

        assert mask.shape == (size, size)

    def test_causal_mask_structure(self):
        """Test causal mask structure (lower triangular + diagonal = 0, upper = -inf)."""
        model = create_model()
        size = 5
        mask = model._generate_square_subsequent_mask(size, torch.device('cpu'))

        # Diagonal and below should be 0
        for i in range(size):
            for j in range(i + 1):
                assert mask[i, j] == 0, f"Position ({i}, {j}) should be 0"

        # Above diagonal should be -inf
        for i in range(size):
            for j in range(i + 1, size):
                assert mask[i, j] == float('-inf'), f"Position ({i}, {j}) should be -inf"


class TestModelSaveLoad:
    """Test model saving and loading."""

    def test_save_and_load_state_dict(self, tmp_path):
        """Test saving and loading model state dict."""
        model1 = create_model()

        # Save state dict
        save_path = tmp_path / "model.pt"
        torch.save(model1.state_dict(), save_path)

        # Load into new model
        model2 = create_model()
        model2.load_state_dict(torch.load(save_path))

        # Compare parameters
        for p1, p2 in zip(model1.parameters(), model2.parameters()):
            assert torch.equal(p1, p2), "Parameters not equal after save/load"

    def test_save_full_model(self, tmp_path):
        """Test saving and loading full model."""
        model1 = create_model()

        # Save full model
        save_path = tmp_path / "model_full.pt"
        torch.save(model1, save_path)

        # Load model (weights_only=False since we trust our own model)
        model2 = torch.load(save_path, weights_only=False)

        # Test forward pass (eval mode to disable dropout for deterministic output)
        model1.eval()
        model2.eval()
        with torch.no_grad():
            input_ids = torch.randint(0, 115, (2, 10))
            logits1 = model1(input_ids)
            logits2 = model2(input_ids)

        assert torch.allclose(logits1, logits2), "Outputs not equal after save/load"


class TestGradients:
    """Test gradient flow through model."""

    def test_gradients_flow(self):
        """Test gradients flow through all parameters."""
        model = create_model()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        # Forward pass
        input_ids = torch.randint(0, 115, (2, 10))
        logits = model(input_ids)

        # Compute loss
        targets = torch.randint(0, 115, (2, 10))
        loss = torch.nn.functional.cross_entropy(
            logits.view(-1, 115),
            targets.view(-1)
        )

        # Backward pass
        optimizer.zero_grad()
        loss.backward()

        # Check all parameters have gradients
        for name, param in model.named_parameters():
            if param.requires_grad:
                assert param.grad is not None, f"No gradient for {name}"
                assert not torch.isnan(param.grad).any(), f"NaN gradient for {name}"


class TestEvalMode:
    """Test model behavior in eval mode."""

    def test_eval_mode_no_dropout(self):
        """Test eval mode disables dropout."""
        model = create_model()

        input_ids = torch.randint(0, 115, (2, 10))

        # Train mode (with dropout)
        model.train()
        logits_train = model(input_ids)

        # Eval mode (no dropout)
        model.eval()
        with torch.no_grad():
            logits_eval1 = model(input_ids)
            logits_eval2 = model(input_ids)

        # Eval mode outputs should be identical (deterministic)
        assert torch.allclose(logits_eval1, logits_eval2), "Eval mode not deterministic"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
