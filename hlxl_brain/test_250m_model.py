#!/usr/bin/env python3
"""
Test the 250M parameter model with tokenizer compatibility fix.

The 250M model was trained with 115 tokens, but the current tokenizer has 117.
This script handles the mismatch by padding the embeddings.
"""

import sys
from pathlib import Path
import torch
from typing import Dict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tokenizer import create_tokenizer
from model import create_model


def resize_token_embeddings(model, old_vocab_size: int, new_vocab_size: int):
    """Resize token embeddings to match new vocabulary size."""

    # Get old weights
    old_token_emb = model.token_embedding.weight.data
    old_output_proj_weight = model.output_projection.weight.data
    old_output_proj_bias = model.output_projection.bias.data

    # Create new embeddings with larger size
    new_token_emb = torch.nn.Embedding(new_vocab_size, model.d_model)
    new_output_proj = torch.nn.Linear(model.d_model, new_vocab_size)

    # Copy old weights
    new_token_emb.weight.data[:old_vocab_size] = old_token_emb
    new_output_proj.weight.data[:old_vocab_size] = old_output_proj_weight
    new_output_proj.bias.data[:old_vocab_size] = old_output_proj_bias

    # Initialize new tokens with small random values
    torch.nn.init.normal_(new_token_emb.weight.data[old_vocab_size:], mean=0.0, std=0.02)
    torch.nn.init.normal_(new_output_proj.weight.data[old_vocab_size:], mean=0.0, std=0.02)
    new_output_proj.bias.data[old_vocab_size:] = 0.0

    # Replace modules
    model.token_embedding = new_token_emb
    model.output_projection = new_output_proj

    return model


def load_250m_model(checkpoint_path: str, device: str = "cuda"):
    """Load 250M model with tokenizer compatibility handling."""

    print("="*80)
    print("LOADING 250M HLX BRAIN WITH TOKENIZER FIX")
    print("="*80)

    # Load checkpoint first to check vocab size
    print(f"\nLoading checkpoint: {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location=device)
    state_dict = checkpoint.get("model_state_dict", checkpoint)

    # Check vocabulary size from checkpoint
    old_vocab_size = state_dict["token_embedding.weight"].shape[0]
    print(f"✓ Checkpoint vocab size: {old_vocab_size}")

    # Create tokenizer
    tokenizer = create_tokenizer()
    new_vocab_size = tokenizer.vocab_size
    print(f"✓ Current tokenizer vocab size: {new_vocab_size}")

    if old_vocab_size == new_vocab_size:
        # No mismatch, load normally
        print("✓ Vocabulary sizes match - loading normally")

        # Infer model architecture from state dict
        d_model = state_dict["token_embedding.weight"].shape[1]

        # Count transformer layers
        num_layers = sum(1 for k in state_dict.keys() if k.startswith("transformer.layers.") and k.endswith(".self_attn.in_proj_weight"))

        # Determine architecture based on d_model
        if d_model == 128:
            # Tiny model
            model = create_model(
                vocab_size=new_vocab_size,
                d_model=128,
                nhead=4,
                num_layers=2,
                dim_feedforward=512,
                dropout=0.1,
            )
        elif d_model == 384:
            # 10M model architecture
            model = create_model(
                vocab_size=new_vocab_size,
                d_model=384,
                nhead=6,
                num_layers=4,
                dim_feedforward=1536,
                dropout=0.1,
            )
        elif d_model == 512:
            # Small model architecture
            model = create_model(
                vocab_size=new_vocab_size,
                d_model=512,
                nhead=8,
                num_layers=12,
                dim_feedforward=2048,
                dropout=0.1,
            )
        elif d_model == 1024:
            # 100M model architecture
            model = create_model(
                vocab_size=new_vocab_size,
                d_model=1024,
                nhead=16,
                num_layers=8,
                dim_feedforward=4096,
                dropout=0.1,
            )
        elif d_model == 1280:
            # 250M model architecture
            model = create_model(
                vocab_size=new_vocab_size,
                d_model=1280,
                nhead=16,
                num_layers=12,
                dim_feedforward=5120,
                dropout=0.1,
            )
        else:
            raise ValueError(f"Unknown model architecture: d_model={d_model}")

        model.load_state_dict(state_dict)
        model.to(device)

    else:
        # Vocabulary mismatch - need to resize
        print(f"⚠ Vocabulary mismatch: {old_vocab_size} → {new_vocab_size}")
        print("Resizing token embeddings...")

        # Infer architecture
        d_model = state_dict["token_embedding.weight"].shape[1]

        # Create model with OLD vocab size first
        if d_model == 384:
            # 10M model
            model = create_model(
                vocab_size=old_vocab_size,  # Use old size initially
                d_model=384,
                nhead=6,
                num_layers=4,
                dim_feedforward=1536,
                dropout=0.1,
            )
        elif d_model == 512:
            # Small model
            model = create_model(
                vocab_size=old_vocab_size,  # Use old size initially
                d_model=512,
                nhead=8,
                num_layers=12,
                dim_feedforward=2048,
                dropout=0.1,
            )
        elif d_model == 1024:
            # 100M model
            model = create_model(
                vocab_size=old_vocab_size,  # Use old size initially
                d_model=1024,
                nhead=16,
                num_layers=8,
                dim_feedforward=4096,
                dropout=0.1,
            )
        elif d_model == 1280:
            # 250M model
            model = create_model(
                vocab_size=old_vocab_size,  # Use old size initially
                d_model=1280,
                nhead=16,
                num_layers=12,
                dim_feedforward=5120,
                dropout=0.1,
            )
        else:
            raise ValueError(f"Unknown model architecture: d_model={d_model}")

        # Load checkpoint with old vocab size
        model.load_state_dict(state_dict)
        model.to(device)

        # Resize embeddings to new vocab size
        model = resize_token_embeddings(model, old_vocab_size, new_vocab_size)
        print(f"✓ Resized embeddings: {old_vocab_size} → {new_vocab_size}")

    model.eval()

    total_params = sum(p.numel() for p in model.parameters())
    print(f"✓ Model loaded: {total_params:,} parameters")
    print(f"✓ Device: {device}")
    print("="*80)

    return model, tokenizer


def quick_test(model, tokenizer, device):
    """Run a quick test to verify model works."""

    print("\n" + "="*80)
    print("QUICK FUNCTIONALITY TEST")
    print("="*80)

    test_prompts = [
        "Search for documents",
        "Filter active users",
        "HLX: search documents",
        "HLXL: SEARCH documents WHERE status = active",
        "LC-R: 🜊1000🜁0 \"search\"🜁1",
    ]

    for prompt in test_prompts:
        print(f"\nPrompt: {prompt}")

        # Encode
        tokens = tokenizer.encode(prompt, add_special_tokens=True)
        input_ids = torch.tensor([tokens], dtype=torch.long).to(device)

        # Generate
        with torch.no_grad():
            generated = model.generate(
                input_ids,
                max_new_tokens=50,
                temperature=0.7
            )

        # Decode
        output = tokenizer.decode(generated[0].cpu().tolist(), skip_special_tokens=True)
        print(f"Output: {output[:150]}...")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Test 250M HLX Brain with tokenizer fix")
    parser.add_argument("--checkpoint", type=str,
                       default="checkpoints/all_variants_10m_final_epoch30.pt",
                       help="Path to checkpoint")
    parser.add_argument("--device", type=str, default="cuda",
                       help="Device to use (cuda/cpu)")
    parser.add_argument("--quick-test", action="store_true", default=True,
                       help="Run quick functionality test")

    args = parser.parse_args()

    # Check if checkpoint exists
    if not Path(args.checkpoint).exists():
        print(f"❌ Checkpoint not found: {args.checkpoint}")
        return 1

    # Determine device
    device = args.device
    if device == "cuda" and not torch.cuda.is_available():
        print("⚠ CUDA not available, falling back to CPU")
        device = "cpu"

    # Load model
    try:
        model, tokenizer = load_250m_model(args.checkpoint, device)
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Quick test
    if args.quick_test:
        try:
            quick_test(model, tokenizer, device)
            print("\n✓ Quick test completed successfully")
        except Exception as e:
            print(f"❌ Quick test failed: {e}")
            import traceback
            traceback.print_exc()
            return 1

    print("\n" + "="*80)
    print("✓ 250M MODEL LOADED AND TESTED SUCCESSFULLY")
    print("="*80)
    print("\nYou can now:")
    print("1. Run comprehensive tests: python3 comprehensive_hlx_test.py --checkpoint <path>")
    print("2. Use this model for HLX translation tasks")
    print("3. Evaluate as potential 'personal intern' for cost savings")

    return 0


if __name__ == "__main__":
    sys.exit(main())
