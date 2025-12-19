#!/usr/bin/env python3
"""
HLXL Brain - Inference CLI

Generate LC-R text from prompts using trained model.

Usage:
    python3 generate.py --prompt "🜊14🜁0" --max-tokens 50
    python3 generate.py --interactive
    python3 generate.py --benchmark

Features:
- Interactive mode for continuous generation
- Batch generation from file
- Benchmark mode for performance testing
- Temperature control for creativity
"""

import argparse
import sys
from pathlib import Path
import torch
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tokenizer import create_tokenizer
from model import create_model


def load_model(checkpoint_path: str, device: str = "cpu"):
    """Load trained model from checkpoint."""
    print(f"Loading model from {checkpoint_path}...")

    # Create tokenizer and model
    tokenizer = create_tokenizer()
    model = create_model(vocab_size=tokenizer.vocab_size)

    # Load checkpoint
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)

    # Handle different checkpoint formats
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
        print(f"✓ Model loaded (epoch {checkpoint.get('epoch', '?')})")
    else:
        model.load_state_dict(checkpoint)
        print(f"✓ Model loaded")

    model.to(device)
    model.eval()

    return model, tokenizer


def generate_text(
    model,
    tokenizer,
    prompt: str,
    max_new_tokens: int = 50,
    temperature: float = 0.0,
    top_k: int = None,
    device: str = "cpu"
):
    """Generate text from prompt."""
    # Encode prompt
    if not prompt:
        # Empty prompt - start with BOS token
        input_ids = torch.tensor([[tokenizer.bos_token_id]], dtype=torch.long)
    else:
        token_ids = tokenizer.encode(prompt, add_special_tokens=True)
        input_ids = torch.tensor([token_ids], dtype=torch.long)

    input_ids = input_ids.to(device)

    # Generate
    with torch.no_grad():
        start_time = time.perf_counter()
        generated = model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_k=top_k,
        )
        end_time = time.perf_counter()

    # Decode
    generated_text = tokenizer.decode(
        generated[0].cpu().tolist(),
        skip_special_tokens=True
    )

    # Calculate stats
    total_tokens = generated.shape[1]
    new_tokens = total_tokens - input_ids.shape[1]
    elapsed_ms = (end_time - start_time) * 1000
    tokens_per_sec = new_tokens / (elapsed_ms / 1000) if elapsed_ms > 0 else 0

    return generated_text, {
        'total_tokens': total_tokens,
        'new_tokens': new_tokens,
        'elapsed_ms': elapsed_ms,
        'tokens_per_sec': tokens_per_sec,
    }


def interactive_mode(model, tokenizer, device: str, temperature: float, max_tokens: int):
    """Interactive generation mode."""
    print()
    print("="*80)
    print("HLXL BRAIN - INTERACTIVE MODE")
    print("="*80)
    print("Enter prompts to generate LC-R text.")
    print("Commands:")
    print("  /temp <value>  - Set temperature (0.0 = deterministic)")
    print("  /tokens <n>    - Set max tokens to generate")
    print("  /quit          - Exit")
    print("="*80)
    print()

    current_temp = temperature
    current_max = max_tokens

    while True:
        try:
            prompt = input("Prompt> ").strip()

            if not prompt:
                continue

            # Handle commands
            if prompt.startswith("/"):
                cmd = prompt.split()[0].lower()

                if cmd == "/quit":
                    print("Goodbye!")
                    break

                elif cmd == "/temp":
                    try:
                        current_temp = float(prompt.split()[1])
                        print(f"Temperature set to {current_temp}")
                    except (IndexError, ValueError):
                        print("Usage: /temp <value>")
                    continue

                elif cmd == "/tokens":
                    try:
                        current_max = int(prompt.split()[1])
                        print(f"Max tokens set to {current_max}")
                    except (IndexError, ValueError):
                        print("Usage: /tokens <number>")
                    continue

                else:
                    print(f"Unknown command: {cmd}")
                    continue

            # Generate
            generated_text, stats = generate_text(
                model, tokenizer, prompt,
                max_new_tokens=current_max,
                temperature=current_temp,
                device=device
            )

            print()
            print(f"Generated: {generated_text}")
            print(f"Stats: {stats['new_tokens']} tokens in {stats['elapsed_ms']:.2f}ms ({stats['tokens_per_sec']:.1f} tok/s)")
            print()

        except KeyboardInterrupt:
            print("\nInterrupted. Type /quit to exit.")
        except EOFError:
            print("\nGoodbye!")
            break


def benchmark_mode(model, tokenizer, device: str):
    """Benchmark generation performance."""
    print()
    print("="*80)
    print("HLXL BRAIN - BENCHMARK MODE")
    print("="*80)
    print()

    test_prompts = [
        "",
        "∅",
        "⊤",
        "🜊14🜁0",
        "🜊900🜁0 ⟁ast🜁1 ⊤🜂",
    ]

    test_lengths = [10, 50, 100]

    results = []

    for prompt in test_prompts:
        for max_tokens in test_lengths:
            print(f"Testing: prompt='{prompt[:20]}...' max_tokens={max_tokens}")

            # Warmup
            for _ in range(3):
                generate_text(model, tokenizer, prompt, max_tokens, device=device)

            # Benchmark (10 runs)
            times = []
            for _ in range(10):
                _, stats = generate_text(model, tokenizer, prompt, max_tokens, device=device)
                times.append(stats['elapsed_ms'])

            avg_ms = sum(times) / len(times)
            min_ms = min(times)
            max_ms = max(times)
            avg_tok_per_sec = max_tokens / (avg_ms / 1000)

            results.append({
                'prompt': prompt[:20],
                'max_tokens': max_tokens,
                'avg_ms': avg_ms,
                'min_ms': min_ms,
                'max_ms': max_ms,
                'tokens_per_sec': avg_tok_per_sec,
            })

            print(f"  Avg: {avg_ms:.2f}ms ({avg_tok_per_sec:.1f} tok/s)")

    print()
    print("="*80)
    print("BENCHMARK RESULTS")
    print("="*80)
    print(f"{'Prompt':<20} {'Tokens':<10} {'Avg (ms)':<12} {'Min (ms)':<12} {'Max (ms)':<12} {'Tok/s':<10}")
    print("-"*80)

    for r in results:
        print(f"{r['prompt']:<20} {r['max_tokens']:<10} {r['avg_ms']:<12.2f} {r['min_ms']:<12.2f} {r['max_ms']:<12.2f} {r['tokens_per_sec']:<10.1f}")

    print("="*80)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate LC-R text with HLXL Brain")

    # Model loading
    parser.add_argument("--checkpoint", type=str, default="checkpoints/final_model.pt",
                        help="Path to model checkpoint (default: checkpoints/final_model.pt)")
    parser.add_argument("--device", type=str, default=None,
                        help="Device to use (default: auto-detect)")
    parser.add_argument("--cpu", action="store_true",
                        help="Force CPU inference")

    # Generation modes
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Interactive mode")
    parser.add_argument("--benchmark", action="store_true",
                        help="Benchmark mode")

    # Single generation
    parser.add_argument("--prompt", "-p", type=str, default="",
                        help="Prompt for generation")
    parser.add_argument("--max-tokens", type=int, default=50,
                        help="Maximum tokens to generate (default: 50)")
    parser.add_argument("--temperature", "-t", type=float, default=0.0,
                        help="Temperature (0.0 = deterministic) (default: 0.0)")
    parser.add_argument("--top-k", type=int, default=None,
                        help="Top-k sampling (default: None)")

    return parser.parse_args()


def main():
    """Main inference function."""
    args = parse_args()

    # Device selection
    if args.cpu:
        device = "cpu"
    elif args.device:
        device = args.device
    else:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    print("="*80)
    print("HLXL BRAIN - INFERENCE")
    print("="*80)
    print(f"Device: {device}")
    print()

    # Load model
    try:
        model, tokenizer = load_model(args.checkpoint, device)
        print(f"✓ Model ready: {model.count_parameters():,} parameters")
        print()
    except FileNotFoundError:
        print(f"Error: Checkpoint not found: {args.checkpoint}")
        print()
        print("Available checkpoints:")
        checkpoint_dir = Path(args.checkpoint).parent
        if checkpoint_dir.exists():
            for ckpt in checkpoint_dir.glob("*.pt"):
                print(f"  - {ckpt}")
        else:
            print("  No checkpoints found. Train a model first with: python3 train.py")
        sys.exit(1)

    # Run mode
    if args.benchmark:
        benchmark_mode(model, tokenizer, device)

    elif args.interactive:
        interactive_mode(model, tokenizer, device, args.temperature, args.max_tokens)

    else:
        # Single generation
        print(f"Prompt: {args.prompt if args.prompt else '(empty)'}")
        print(f"Max tokens: {args.max_tokens}")
        print(f"Temperature: {args.temperature}")
        print()

        generated_text, stats = generate_text(
            model, tokenizer, args.prompt,
            max_new_tokens=args.max_tokens,
            temperature=args.temperature,
            top_k=args.top_k,
            device=device
        )

        print("="*80)
        print("GENERATED TEXT")
        print("="*80)
        print(generated_text)
        print("="*80)
        print()
        print(f"Tokens: {stats['new_tokens']} generated in {stats['elapsed_ms']:.2f}ms")
        print(f"Speed: {stats['tokens_per_sec']:.1f} tokens/sec")
        print()


if __name__ == "__main__":
    main()
