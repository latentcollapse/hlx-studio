#!/usr/bin/env python3
"""
HLXL Brain - Model Evaluation Script

Comprehensive evaluation of the trained model across all phases:
- Phase 1: Semantic grounding
- Phase 2: Domain knowledge
- Phase 3: Long-form reasoning
- Phase 4: Perfect HLX + Quality English

Usage:
    python3 evaluate_model.py --checkpoint checkpoints/phase4_final_epoch105.pt
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


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="HLXL Brain Model Evaluation")

    parser.add_argument("--checkpoint", type=str,
                        default="checkpoints/phase4_final_epoch105.pt",
                        help="Path to model checkpoint")
    parser.add_argument("--device", type=str, default=None,
                        help="Device (default: auto-detect)")
    parser.add_argument("--temperature", type=float, default=0.0,
                        help="Sampling temperature (default: 0.0 for greedy)")
    parser.add_argument("--max-tokens", type=int, default=100,
                        help="Max tokens to generate (default: 100)")
    parser.add_argument("--save-results", type=str, default="evaluation_results.json",
                        help="Path to save evaluation results")

    return parser.parse_args()


def generate(model, tokenizer, prompt_text, device, temperature=0.0, max_tokens=100):
    """Generate LC-R from English prompt or vice versa."""
    model.eval()

    # Tokenize prompt
    prompt_ids = tokenizer.encode(prompt_text, add_special_tokens=True)
    prompt = torch.tensor([prompt_ids], dtype=torch.long).to(device)

    with torch.no_grad():
        generated = model.generate(prompt, max_new_tokens=max_tokens, temperature=temperature)

    generated_text = tokenizer.decode(generated[0].cpu().tolist(), skip_special_tokens=False)
    return generated_text


def evaluate_phase1_semantics(model, tokenizer, device, temperature, max_tokens):
    """Evaluate Phase 1: Semantic grounding."""
    print("\n" + "="*80)
    print("PHASE 1 EVALUATION: SEMANTIC GROUNDING")
    print("="*80)

    test_cases = [
        ("Navigate to home directory", "Expected: navigate operation"),
        ("Search for documents", "Expected: search operation"),
        ("Filter active users", "Expected: filter operation"),
        ("Transform text to uppercase", "Expected: transform operation"),
        ("Aggregate sum of values", "Expected: aggregate operation with sum"),
    ]

    results = []
    for i, (prompt, expected) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {prompt}")
        print(f"Expected: {expected}")
        output = generate(model, tokenizer, prompt, device, temperature, max_tokens)
        print(f"Generated: {output[:200]}")
        results.append({"prompt": prompt, "expected": expected, "output": output})

    return results


def evaluate_phase2_domain(model, tokenizer, device, temperature, max_tokens):
    """Evaluate Phase 2: Domain knowledge."""
    print("\n" + "="*80)
    print("PHASE 2 EVALUATION: DOMAIN KNOWLEDGE")
    print("="*80)

    test_cases = [
        ("Read file /etc/config.json", "Expected: file system operation"),
        ("List all files in directory", "Expected: directory operation"),
        ("Query database for users", "Expected: database operation"),
        ("Group records by category and sum", "Expected: data structure + aggregation"),
        ("If condition then action else other", "Expected: conditional logic"),
    ]

    results = []
    for i, (prompt, expected) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {prompt}")
        print(f"Expected: {expected}")
        output = generate(model, tokenizer, prompt, device, temperature, max_tokens)
        print(f"Generated: {output[:200]}")
        results.append({"prompt": prompt, "expected": expected, "output": output})

    return results


def evaluate_phase3_longform(model, tokenizer, device, temperature, max_tokens):
    """Evaluate Phase 3: Long-form reasoning."""
    print("\n" + "="*80)
    print("PHASE 3 EVALUATION: LONG-FORM REASONING")
    print("="*80)

    test_cases = [
        ("Load data, validate, transform, and save", "Expected: multi-step pipeline"),
        ("For each item, if valid then process", "Expected: iteration with conditional"),
        ("Recursively traverse tree and collect values", "Expected: recursive pattern"),
        ("Initialize counter, increment for each match", "Expected: stateful operation"),
        ("Filter users, sort by date, take top 10", "Expected: complex multi-operation"),
    ]

    results = []
    for i, (prompt, expected) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {prompt}")
        print(f"Expected: {expected}")
        output = generate(model, tokenizer, prompt, device, temperature, max_tokens)
        print(f"Generated: {output[:300]}")
        results.append({"prompt": prompt, "expected": expected, "output": output})

    return results


def evaluate_phase4_english(model, tokenizer, device, temperature, max_tokens):
    """Evaluate Phase 4: Perfect HLX + Quality English."""
    print("\n" + "="*80)
    print("PHASE 4 EVALUATION: PERFECT HLX + QUALITY ENGLISH")
    print("="*80)

    # Test multiple phrasings
    print("\n--- Multiple Phrasings Test ---")
    phrasings = [
        "Search for documents",
        "Find documents",
        "Look up documents",
        "Locate documents",
    ]

    phrasing_results = []
    for phrasing in phrasings:
        output = generate(model, tokenizer, phrasing, device, temperature, max_tokens)
        print(f"{phrasing} → {output[:150]}")
        phrasing_results.append({"phrasing": phrasing, "output": output})

    # Test conversational style
    print("\n--- Conversational Style Test ---")
    conversational = [
        "Let's search the database for users",
        "I need to filter out invalid records",
        "Can you sort these by date?",
        "Please aggregate the sales data",
    ]

    conversational_results = []
    for prompt in conversational:
        output = generate(model, tokenizer, prompt, device, temperature, max_tokens)
        print(f"{prompt} → {output[:150]}")
        conversational_results.append({"prompt": prompt, "output": output})

    # Test LC-R → English (reverse direction)
    print("\n--- LC-R → English Test ---")
    lcr_prompts = [
        '🜊1000🜁0 "search"🜁1 ⟁database🜂',
        '🜊1000🜁0 "filter"🜁1 ⟁items🜂',
        '🜊1000🜁0 "aggregate"🜁1 ⟁sum🜁2 ⟁values🜂',
    ]

    reverse_results = []
    for lcr in lcr_prompts:
        output = generate(model, tokenizer, lcr, device, temperature, max_tokens)
        print(f"{lcr} → {output[:150]}")
        reverse_results.append({"lcr": lcr, "output": output})

    return {
        "phrasings": phrasing_results,
        "conversational": conversational_results,
        "reverse": reverse_results
    }


def evaluate_generation_quality(model, tokenizer, device, temperature, max_tokens):
    """Evaluate overall generation quality."""
    print("\n" + "="*80)
    print("GENERATION QUALITY EVALUATION")
    print("="*80)

    test_cases = [
        ("", "Empty prompt (should generate valid LC-R)"),
        ("Filter", "Single word"),
        ("Search database", "Two words"),
        ("Filter active users and sort by date", "Complex multi-op"),
        ("What is the sum of all values?", "Question format"),
    ]

    results = []
    for prompt, description in test_cases:
        print(f"\n{description}")
        print(f"Prompt: '{prompt}'")
        output = generate(model, tokenizer, prompt, device, temperature, max_tokens)
        print(f"Generated: {output[:200]}")

        # Check for valid structure
        has_bos = output.startswith("<BOS>")
        has_glyphs = "🜊" in output and "🜂" in output
        has_eos = "<EOS>" in output

        print(f"Valid structure: BOS={has_bos}, Glyphs={has_glyphs}, EOS={has_eos}")

        results.append({
            "prompt": prompt,
            "description": description,
            "output": output,
            "valid_structure": has_bos and has_glyphs and has_eos
        })

    return results


def main():
    """Main evaluation function."""
    args = parse_args()

    print("="*80)
    print("HLXL BRAIN - COMPREHENSIVE MODEL EVALUATION")
    print("="*80)
    print(f"Checkpoint: {args.checkpoint}")
    print(f"Max tokens: {args.max_tokens}")
    print(f"Temperature: {args.temperature}")
    print()

    # Device selection
    if args.device:
        device = args.device
    else:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"Device: {device}")
    if device == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")
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
        d_model=128,
        nhead=4,
        num_layers=2,
        dim_feedforward=512,
        dropout=0.1,
    )
    print(f"✓ Model created: {model.count_parameters():,} parameters ({model.get_model_size_mb():.2f} MB)")
    print()

    # Load checkpoint
    print(f"Loading checkpoint: {args.checkpoint}")
    checkpoint = torch.load(args.checkpoint, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()

    print(f"✓ Checkpoint loaded")
    print(f"  - Epoch: {checkpoint.get('epoch', 'unknown')}")

    train_loss = checkpoint.get('train_loss', 'unknown')
    train_loss_str = f"{train_loss:.4f}" if isinstance(train_loss, float) else str(train_loss)
    print(f"  - Train loss: {train_loss_str}")

    val_loss = checkpoint.get('val_loss', 'unknown')
    val_loss_str = f"{val_loss:.4f}" if isinstance(val_loss, float) else str(val_loss)
    print(f"  - Val loss: {val_loss_str}")
    print()

    # Run all evaluations
    evaluation_results = {
        "metadata": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "checkpoint": args.checkpoint,
            "device": device,
            "model_parameters": model.count_parameters(),
            "model_size_mb": model.get_model_size_mb(),
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
        }
    }

    # Phase 1: Semantics
    evaluation_results["phase1_semantics"] = evaluate_phase1_semantics(
        model, tokenizer, device, args.temperature, args.max_tokens
    )

    # Phase 2: Domain knowledge
    evaluation_results["phase2_domain"] = evaluate_phase2_domain(
        model, tokenizer, device, args.temperature, args.max_tokens
    )

    # Phase 3: Long-form reasoning
    evaluation_results["phase3_longform"] = evaluate_phase3_longform(
        model, tokenizer, device, args.temperature, args.max_tokens
    )

    # Phase 4: English quality
    evaluation_results["phase4_english"] = evaluate_phase4_english(
        model, tokenizer, device, args.temperature, args.max_tokens
    )

    # Generation quality
    evaluation_results["generation_quality"] = evaluate_generation_quality(
        model, tokenizer, device, args.temperature, args.max_tokens
    )

    # Save results
    print("\n" + "="*80)
    print("SAVING RESULTS")
    print("="*80)
    with open(args.save_results, 'w') as f:
        json.dump(evaluation_results, f, indent=2, ensure_ascii=False)
    print(f"✓ Results saved to {args.save_results}")

    print("\n" + "="*80)
    print("EVALUATION COMPLETE")
    print("="*80)
    print(f"Model: {model.count_parameters():,} parameters ({model.get_model_size_mb():.2f} MB)")
    print(f"Results saved: {args.save_results}")
    print("="*80)


if __name__ == "__main__":
    main()
