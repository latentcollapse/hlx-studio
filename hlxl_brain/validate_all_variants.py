#!/usr/bin/env python3
"""
HLXL Brain - Validate All Variants Model

Test the trained model on all four HLX family formats.

Usage:
    python3 validate_all_variants.py
"""

import sys
from pathlib import Path
import torch
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tokenizer import create_tokenizer
from model import create_model


def generate_completion(model, tokenizer, device, prompt_text, max_tokens=80):
    """Generate completion with the arrow separator."""
    model.eval()

    # Include the arrow to signal output generation
    full_prompt = prompt_text + " → "
    prompt_ids = tokenizer.encode(full_prompt, add_special_tokens=True)
    prompt = torch.tensor([prompt_ids], dtype=torch.long).to(device)

    with torch.no_grad():
        generated = model.generate(prompt, max_new_tokens=max_tokens, temperature=0.0)

    generated_text = tokenizer.decode(generated[0].cpu().tolist(), skip_special_tokens=False)

    # Extract output after the last arrow (our prompt separator)
    if " → " in generated_text:
        parts = generated_text.split(" → ")
        output = parts[-1]  # Get the part after the arrow
    else:
        # Fall back to removing the prompt portion
        output = generated_text[len(full_prompt):]

    # Clean output - remove special tokens and padding
    output = output.replace("<pad>", "").replace("<PAD>", "")
    output = output.replace("<EOS>", "").replace("<eos>", "")
    output = output.replace("<BOS>", "").replace("<bos>", "")
    output = output.strip()

    return output


def main():
    """Main validation function."""
    print("="*80)
    print("HLXL BRAIN - ALL VARIANTS VALIDATION")
    print("="*80)
    print()

    # Device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    print()

    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer = create_tokenizer()
    print(f"Tokenizer loaded: {tokenizer.vocab_size} tokens")

    # Load model
    print("Loading model...")
    model = create_model(
        vocab_size=tokenizer.vocab_size,
        d_model=128,
        nhead=4,
        num_layers=2,
        dim_feedforward=512,
        dropout=0.0,  # No dropout for inference
    )

    # Load best checkpoint
    checkpoint_path = "checkpoints/best_model_all_variants.pt"
    if not Path(checkpoint_path).exists():
        checkpoint_path = "checkpoints/all_variants_final_epoch30.pt"

    print(f"Loading checkpoint: {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()

    print(f"Model loaded: {model.count_parameters():,} parameters")
    print()

    # Test cases
    test_cases = [
        # Basic operations
        ("Search for documents", "Basic search operation"),
        ("Filter active users", "Filter operation"),
        ("Navigate to home", "Navigation command"),
        ("Execute command", "Execute operation"),
        ("Read from database", "Read operation"),

        # Data structures
        ("Empty list", "Empty array"),
        ("List of numbers one two three", "Number array"),
        ("User object with name", "Simple object"),
        ("Point with x and y coordinates", "Coordinate object"),

        # Complex operations
        ("Copy source to destination", "Two-argument operation"),
        ("Train model on data", "ML operation"),
        ("Create render pipeline", "GPU operation"),

        # Expressions
        ("Integer literal forty-two", "Literal contract"),
        ("Assign forty-two to x", "Assignment"),
        ("Call function add with one and two", "Function call"),
    ]

    formats = ["HLXL", "LC-R", "LC-T", "LC-B"]

    # Run validation
    print("="*80)
    print("VALIDATION RESULTS")
    print("="*80)
    print()

    results = []

    for english, description in test_cases:
        print(f"English: {english}")
        print(f"  ({description})")

        case_results = {"english": english, "description": description, "outputs": {}}

        for fmt in formats:
            prompt = f"[{fmt}] {english}"
            output = generate_completion(model, tokenizer, device, prompt, max_tokens=100)
            case_results["outputs"][fmt] = output
            print(f"  {fmt}: {output[:80]}")

        results.append(case_results)
        print()

    # Summary statistics
    print("="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    print()

    # Check for glyph preservation in LC-R
    lcr_glyphs = ['🜊', '🜂', '🜁', '🜃', '🜄', '◇', '◆', '⟁', '∅', '⊤', '⊥']
    lcr_glyph_count = 0
    total_lcr = 0

    for result in results:
        lcr_output = result["outputs"].get("LC-R", "")
        total_lcr += 1
        if any(g in lcr_output for g in lcr_glyphs):
            lcr_glyph_count += 1

    print(f"LC-R outputs with glyphs: {lcr_glyph_count}/{total_lcr}")

    # Check for LC-T format correctness
    lct_markers = ['{C:', '@', 'NULL', 'TRUE', 'FALSE']
    lct_correct = 0
    total_lct = 0

    for result in results:
        lct_output = result["outputs"].get("LC-T", "")
        total_lct += 1
        if any(m in lct_output for m in lct_markers):
            lct_correct += 1

    print(f"LC-T outputs with correct markers: {lct_correct}/{total_lct}")

    # Check for LC-B format correctness
    lcb_markers = ['[', '|', '&', '0x']
    lcb_correct = 0
    total_lcb = 0

    for result in results:
        lcb_output = result["outputs"].get("LC-B", "")
        total_lcb += 1
        if any(m in lcb_output for m in lcb_markers):
            lcb_correct += 1

    print(f"LC-B outputs with correct markers: {lcb_correct}/{total_lcb}")

    # Save results
    output_file = "validation_all_variants_results.json"
    with open(output_file, 'w') as f:
        json.dump({
            "test_cases": results,
            "summary": {
                "total_cases": len(results),
                "lcr_glyph_rate": lcr_glyph_count / total_lcr if total_lcr > 0 else 0,
                "lct_correct_rate": lct_correct / total_lct if total_lct > 0 else 0,
                "lcb_correct_rate": lcb_correct / total_lcb if total_lcb > 0 else 0,
            }
        }, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to: {output_file}")
    print()
    print("="*80)
    print("VALIDATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
