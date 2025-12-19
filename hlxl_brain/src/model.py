"""
HLXL Brain - Tiny Transformer Model

Compact transformer architecture optimized for LC-R (Latent Collapse Runic) format.

Architecture:
- Vocabulary: 115 tokens (LC-R glyphs + ASCII)
- Embedding: 128-dim
- Layers: 2x TransformerEncoder
- Attention heads: 4
- FFN dim: 512
- Total parameters: ~5M

Target: <1s inference, deterministic output (T=0), HLX-fluent generation.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple
import math


class HLXLTransformer(nn.Module):
    """
    Tiny transformer model for HLX/LC-R text generation.

    Designed for:
    - Fast inference on consumer hardware
    - Deterministic output (greedy decoding)
    - HLX pattern recognition and generation
    """

    def __init__(
        self,
        vocab_size: int = 115,
        d_model: int = 128,
        nhead: int = 4,
        num_layers: int = 2,
        dim_feedforward: int = 512,
        dropout: float = 0.1,
        max_seq_length: int = 512,
    ):
        """
        Initialize HLXL transformer model.

        Args:
            vocab_size: Size of vocabulary (default: 115 for LC-R)
            d_model: Embedding dimension (default: 128)
            nhead: Number of attention heads (default: 4)
            num_layers: Number of transformer layers (default: 2)
            dim_feedforward: FFN hidden dimension (default: 512)
            dropout: Dropout rate (default: 0.1)
            max_seq_length: Maximum sequence length (default: 512)
        """
        super().__init__()

        self.vocab_size = vocab_size
        self.d_model = d_model
        self.max_seq_length = max_seq_length

        # Token embeddings
        self.token_embedding = nn.Embedding(vocab_size, d_model)

        # Positional embeddings (learned)
        self.position_embedding = nn.Embedding(max_seq_length, d_model)

        # Transformer encoder layers
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True,
            norm_first=True,  # Pre-norm for better stability
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        # Output projection
        self.output_projection = nn.Linear(d_model, vocab_size)

        # Initialize weights
        self._init_weights()

    def _init_weights(self):
        """Initialize weights with Xavier/Kaiming initialization."""
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Forward pass.

        Args:
            input_ids: Token IDs, shape (batch_size, seq_length)
            attention_mask: Attention mask, shape (batch_size, seq_length)

        Returns:
            Logits, shape (batch_size, seq_length, vocab_size)
        """
        batch_size, seq_length = input_ids.shape

        # Token embeddings
        token_embeds = self.token_embedding(input_ids)  # (B, L, d_model)

        # Positional embeddings
        positions = torch.arange(seq_length, device=input_ids.device)
        position_embeds = self.position_embedding(positions)  # (L, d_model)

        # Combine embeddings
        embeddings = token_embeds + position_embeds  # (B, L, d_model)

        # Create causal mask (prevent attending to future tokens)
        causal_mask = self._generate_square_subsequent_mask(seq_length, input_ids.device)

        # Transformer forward pass
        hidden_states = self.transformer(
            embeddings,
            mask=causal_mask,
            src_key_padding_mask=attention_mask if attention_mask is not None else None,
        )

        # Project to vocabulary
        logits = self.output_projection(hidden_states)  # (B, L, vocab_size)

        return logits

    def _generate_square_subsequent_mask(self, size: int, device: torch.device) -> torch.Tensor:
        """
        Generate causal mask to prevent attending to future tokens.

        Args:
            size: Sequence length
            device: Device for tensor

        Returns:
            Causal mask, shape (size, size)
        """
        mask = torch.triu(torch.ones(size, size, device=device), diagonal=1)
        mask = mask.masked_fill(mask == 1, float('-inf'))
        return mask

    def generate(
        self,
        input_ids: torch.Tensor,
        max_new_tokens: int = 50,
        temperature: float = 0.0,
        top_k: Optional[int] = None,
        eos_token_id: Optional[int] = None,
    ) -> torch.Tensor:
        """
        Generate text autoregressively.

        Args:
            input_ids: Prompt token IDs, shape (batch_size, prompt_length)
            max_new_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 = greedy/deterministic)
            top_k: Top-k sampling (None = disabled)
            eos_token_id: End-of-sequence token ID to stop generation

        Returns:
            Generated token IDs, shape (batch_size, prompt_length + generated_length)
        """
        self.eval()

        with torch.no_grad():
            for _ in range(max_new_tokens):
                # Get predictions for next token
                logits = self.forward(input_ids)  # (B, L, vocab_size)
                next_token_logits = logits[:, -1, :]  # (B, vocab_size)

                # Apply temperature
                if temperature > 0:
                    next_token_logits = next_token_logits / temperature

                # Apply top-k filtering
                if top_k is not None:
                    indices_to_remove = next_token_logits < torch.topk(next_token_logits, top_k)[0][..., -1, None]
                    next_token_logits[indices_to_remove] = float('-inf')

                # Sample or greedy decode
                if temperature == 0:
                    # Greedy decoding (deterministic)
                    next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)  # (B, 1)
                else:
                    # Sample from distribution
                    probs = F.softmax(next_token_logits, dim=-1)
                    next_token = torch.multinomial(probs, num_samples=1)  # (B, 1)

                # Append to sequence
                input_ids = torch.cat([input_ids, next_token], dim=1)

                # Check for EOS token
                if eos_token_id is not None and (next_token == eos_token_id).all():
                    break

                # Check max sequence length
                if input_ids.shape[1] >= self.max_seq_length:
                    break

        return input_ids

    def count_parameters(self) -> int:
        """Count total trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def get_model_size_mb(self) -> float:
        """Get model size in megabytes (FP32)."""
        param_count = self.count_parameters()
        # 4 bytes per parameter (FP32)
        size_bytes = param_count * 4
        size_mb = size_bytes / (1024 ** 2)
        return size_mb

    def __repr__(self) -> str:
        params = self.count_parameters()
        size_mb = self.get_model_size_mb()
        return (
            f"HLXLTransformer(\n"
            f"  vocab_size={self.vocab_size},\n"
            f"  d_model={self.d_model},\n"
            f"  layers={len(self.transformer.layers)},\n"
            f"  parameters={params:,},\n"
            f"  size={size_mb:.2f} MB\n"
            f")"
        )


def create_model(
    vocab_size: int = 115,
    d_model: int = 128,
    nhead: int = 4,
    num_layers: int = 2,
    dim_feedforward: int = 512,
    dropout: float = 0.1,
) -> HLXLTransformer:
    """
    Factory function to create HLXL transformer model.

    Args:
        vocab_size: Vocabulary size (default: 115 for LC-R)
        d_model: Model dimension (default: 128)
        nhead: Attention heads (default: 4)
        num_layers: Transformer layers (default: 2)
        dim_feedforward: FFN dimension (default: 512)
        dropout: Dropout rate (default: 0.1)

    Returns:
        Initialized HLXLTransformer model
    """
    model = HLXLTransformer(
        vocab_size=vocab_size,
        d_model=d_model,
        nhead=nhead,
        num_layers=num_layers,
        dim_feedforward=dim_feedforward,
        dropout=dropout,
    )
    return model


def create_model_1b(vocab_size: int = 115, dropout: float = 0.1, max_seq_length: int = 512) -> HLXLTransformer:
    """
    Factory function to create 1 billion parameter HLXLTransformer.

    Architecture (1,008,685,171 parameters = 1.01B):
    - d_model: 2048 (16x larger than tiny model)
    - nhead: 16 (4x larger than tiny model)
    - num_layers: 20 (10x larger than tiny model)
    - dim_feedforward: 8192 (16x larger than tiny model)

    Memory requirements:
    - FP32: ~3.75 GB
    - FP16: ~1.88 GB
    - With gradients + optimizer: ~16-20 GB (recommend FP16 + gradient checkpointing)

    Args:
        vocab_size: Vocabulary size (default: 115 for LC-R)
        dropout: Dropout rate (default: 0.1)
        max_seq_length: Maximum sequence length (default: 512)

    Returns:
        Initialized HLXLTransformer model with ~1B parameters
    """
    model = HLXLTransformer(
        vocab_size=vocab_size,
        d_model=2048,
        nhead=16,
        num_layers=20,
        dim_feedforward=8192,
        dropout=dropout,
        max_seq_length=max_seq_length,
    )
    return model


def create_model_100m(vocab_size: int = 115, dropout: float = 0.1, max_seq_length: int = 512) -> HLXLTransformer:
    """
    Factory function to create ~100 million parameter HLXLTransformer.

    Architecture (~100M parameters):
    - d_model: 1024 (8x larger than tiny model)
    - nhead: 8 (2x larger than tiny model)
    - num_layers: 8 (4x larger than tiny model)
    - dim_feedforward: 4096 (8x larger than tiny model)

    Memory requirements:
    - FP32: ~400 MB
    - FP16: ~200 MB
    - With gradients + optimizer: ~2-3 GB (fits easily on 8GB GPU)

    Args:
        vocab_size: Vocabulary size (default: 115 for LC-R)
        dropout: Dropout rate (default: 0.1)
        max_seq_length: Maximum sequence length (default: 512)

    Returns:
        Initialized HLXLTransformer model with ~100M parameters
    """
    model = HLXLTransformer(
        vocab_size=vocab_size,
        d_model=1024,
        nhead=8,
        num_layers=8,
        dim_feedforward=4096,
        dropout=dropout,
        max_seq_length=max_seq_length,
    )
    return model


def create_model_scaled(
    vocab_size: int = 115,
    target_params: str = "100m",
    dropout: float = 0.1,
    max_seq_length: int = 512
) -> HLXLTransformer:
    """
    Factory function to create a scaled HLXLTransformer with specified parameter count.

    Available sizes:
    - "tiny": ~500K params (original - fits anywhere)
    - "10m": ~10M params (small - fits on any GPU)
    - "50m": ~50M params (medium - fits on 4GB+ GPU)
    - "100m": ~100M params (large - fits on 8GB GPU)
    - "250m": ~250M params (fits on 12GB+ GPU)
    - "500m": ~500M params (fits on 16GB+ GPU)
    - "1b": ~1B params (fits on 24GB+ GPU)

    Args:
        vocab_size: Vocabulary size (default: 115)
        target_params: Target parameter count as string
        dropout: Dropout rate (default: 0.1)
        max_seq_length: Maximum sequence length (default: 512)

    Returns:
        Initialized HLXLTransformer model
    """
    configs = {
        "tiny": {"d_model": 128, "nhead": 4, "num_layers": 2, "dim_feedforward": 512},
        "10m": {"d_model": 384, "nhead": 6, "num_layers": 4, "dim_feedforward": 1536},
        "50m": {"d_model": 768, "nhead": 8, "num_layers": 6, "dim_feedforward": 3072},
        "100m": {"d_model": 1024, "nhead": 8, "num_layers": 8, "dim_feedforward": 4096},
        "250m": {"d_model": 1280, "nhead": 10, "num_layers": 12, "dim_feedforward": 5120},
        "500m": {"d_model": 1536, "nhead": 12, "num_layers": 16, "dim_feedforward": 6144},
        "1b": {"d_model": 2048, "nhead": 16, "num_layers": 20, "dim_feedforward": 8192},
    }

    if target_params not in configs:
        raise ValueError(f"Unknown target_params: {target_params}. Available: {list(configs.keys())}")

    config = configs[target_params]

    model = HLXLTransformer(
        vocab_size=vocab_size,
        d_model=config["d_model"],
        nhead=config["nhead"],
        num_layers=config["num_layers"],
        dim_feedforward=config["dim_feedforward"],
        dropout=dropout,
        max_seq_length=max_seq_length,
    )
    return model


if __name__ == "__main__":
    # Quick test
    model = create_model()
    print(f"✓ Model initialized: {model}")

    # Test forward pass
    batch_size = 2
    seq_length = 10
    dummy_input = torch.randint(0, 115, (batch_size, seq_length))

    logits = model(dummy_input)
    print(f"✓ Forward pass: input {dummy_input.shape} → logits {logits.shape}")

    # Test generation
    prompt = torch.randint(0, 115, (1, 5))
    generated = model.generate(prompt, max_new_tokens=10, temperature=0.0)
    print(f"✓ Generation: prompt {prompt.shape} → generated {generated.shape}")

    print(f"\n✓ Model ready for training")
