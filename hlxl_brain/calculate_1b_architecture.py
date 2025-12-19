#!/usr/bin/env python3
"""
Calculate HLXLTransformer architecture to scale to ~1 billion parameters.
"""

def count_transformer_params(vocab_size, d_model, nhead, num_layers, dim_feedforward, max_seq_length):
    """
    Calculate exact parameter count for HLXLTransformer.

    Parameter breakdown:
    1. Token embeddings: vocab_size × d_model
    2. Position embeddings: max_seq_length × d_model
    3. Per TransformerEncoderLayer:
       - Self-attention:
         - Q, K, V projections: 3 × (d_model × d_model + d_model)
         - Output projection: d_model × d_model + d_model
         - Layer norm 1: 2 × d_model
       - Feed-forward:
         - Linear 1: d_model × dim_feedforward + dim_feedforward
         - Linear 2: dim_feedforward × d_model + d_model
         - Layer norm 2: 2 × d_model
    4. Output projection: d_model × vocab_size + vocab_size
    """

    # Embeddings
    token_embed = vocab_size * d_model
    pos_embed = max_seq_length * d_model

    # Per layer parameters
    # Self-attention (including biases)
    qkv_proj = 3 * (d_model * d_model + d_model)
    attn_out = d_model * d_model + d_model
    ln1 = 2 * d_model

    # Feed-forward (including biases)
    ffn1 = d_model * dim_feedforward + dim_feedforward
    ffn2 = dim_feedforward * d_model + d_model
    ln2 = 2 * d_model

    per_layer = qkv_proj + attn_out + ln1 + ffn1 + ffn2 + ln2

    # Total layers
    all_layers = num_layers * per_layer

    # Output projection
    output_proj = d_model * vocab_size + vocab_size

    # Total
    total = token_embed + pos_embed + all_layers + output_proj

    breakdown = {
        "token_embeddings": token_embed,
        "position_embeddings": pos_embed,
        "transformer_layers": all_layers,
        "per_layer": per_layer,
        "output_projection": output_proj,
        "total": total
    }

    return total, breakdown


def format_params(n):
    """Format parameter count in readable form."""
    if n >= 1e9:
        return f"{n/1e9:.2f}B"
    elif n >= 1e6:
        return f"{n/1e6:.2f}M"
    elif n >= 1e3:
        return f"{n/1e3:.2f}K"
    else:
        return str(n)


# Current tiny model
print("="*80)
print("CURRENT ARCHITECTURE (TINY MODEL)")
print("="*80)
current_config = {
    "vocab_size": 115,
    "d_model": 128,
    "nhead": 4,
    "num_layers": 2,
    "dim_feedforward": 512,
    "max_seq_length": 512,
}
current_params, current_breakdown = count_transformer_params(**current_config)
print(f"Configuration:")
for k, v in current_config.items():
    print(f"  {k}: {v}")
print(f"\nTotal parameters: {current_params:,} ({format_params(current_params)})")
print(f"  - Token embeddings: {current_breakdown['token_embeddings']:,}")
print(f"  - Position embeddings: {current_breakdown['position_embeddings']:,}")
print(f"  - Transformer layers: {current_breakdown['transformer_layers']:,} ({current_config['num_layers']} × {current_breakdown['per_layer']:,})")
print(f"  - Output projection: {current_breakdown['output_projection']:,}")
print()

# Target: ~1B parameters
print("="*80)
print("SCALING TO ~1 BILLION PARAMETERS")
print("="*80)
print()

# Try several configurations
target = 1_000_000_000
print(f"Target: {format_params(target)} parameters")
print()

configs = [
    # Format: (d_model, num_layers, nhead, dim_feedforward_multiplier)
    ("Balanced 20-layer", 2048, 20, 16, 4),
    ("Deep 24-layer", 1792, 24, 14, 4),
    ("Wide 16-layer", 2304, 16, 18, 4),
    ("Ultra-deep 32-layer", 1536, 32, 12, 4),
    ("GPT-2 XL style", 1600, 48, 16, 4),
]

results = []
for name, d_model, num_layers, nhead, ffn_mult in configs:
    dim_feedforward = d_model * ffn_mult

    config = {
        "vocab_size": 115,  # Keep same tokenizer
        "d_model": d_model,
        "nhead": nhead,
        "num_layers": num_layers,
        "dim_feedforward": dim_feedforward,
        "max_seq_length": 512,  # Keep same max length
    }

    params, breakdown = count_transformer_params(**config)
    diff = abs(params - target)
    diff_pct = (diff / target) * 100

    results.append((name, config, params, breakdown, diff_pct))

    print(f"{name}:")
    print(f"  d_model: {d_model}")
    print(f"  num_layers: {num_layers}")
    print(f"  nhead: {nhead}")
    print(f"  dim_feedforward: {dim_feedforward} ({ffn_mult}× d_model)")
    print(f"  Total params: {params:,} ({format_params(params)})")
    print(f"  Difference from target: {diff_pct:.2f}%")
    print()

# Find closest to target
best = min(results, key=lambda x: x[4])
best_name, best_config, best_params, best_breakdown, _ = best

print("="*80)
print("RECOMMENDED CONFIGURATION (CLOSEST TO 1B)")
print("="*80)
print(f"Architecture: {best_name}")
print()
print(f"Configuration:")
for k, v in best_config.items():
    print(f"  {k}: {v}")
print()
print(f"Parameter breakdown:")
print(f"  Token embeddings:     {best_breakdown['token_embeddings']:>15,} ({format_params(best_breakdown['token_embeddings']):>8})")
print(f"  Position embeddings:  {best_breakdown['position_embeddings']:>15,} ({format_params(best_breakdown['position_embeddings']):>8})")
print(f"  Transformer layers:   {best_breakdown['transformer_layers']:>15,} ({format_params(best_breakdown['transformer_layers']):>8})")
print(f"    (per layer:         {best_breakdown['per_layer']:>15,} ({format_params(best_breakdown['per_layer']):>8}))")
print(f"  Output projection:    {best_breakdown['output_projection']:>15,} ({format_params(best_breakdown['output_projection']):>8})")
print(f"  {'─'*40}")
print(f"  TOTAL:                {best_params:>15,} ({format_params(best_params):>8})")
print()
print(f"Scaling factor from current model: {best_params / current_params:.1f}×")
print()

# Model size estimation
fp32_bytes = best_params * 4
fp16_bytes = best_params * 2
print(f"Memory requirements:")
print(f"  FP32: {fp32_bytes / (1024**3):.2f} GB")
print(f"  FP16: {fp16_bytes / (1024**3):.2f} GB")
print()

print("="*80)
print("IMPLEMENTATION NOTES")
print("="*80)
print("""
1. Keep existing architecture structure:
   - Token + position embeddings
   - TransformerEncoderLayer with pre-norm
   - Causal masking for autoregressive generation
   - Output projection to vocabulary

2. Changes needed in create_model():
   - Update default d_model, num_layers, nhead, dim_feedforward
   - All other components remain identical

3. Training considerations:
   - Gradient checkpointing recommended (saves memory)
   - Mixed precision training (FP16) essential
   - Larger batch sizes may need gradient accumulation
   - Learning rate may need adjustment (typically scales with sqrt(d_model))

4. Hardware requirements:
   - Minimum 16GB GPU memory (with FP16 + gradient checkpointing)
   - 24GB+ recommended for comfortable training
   - Consider distributed training for very large batches
""")
