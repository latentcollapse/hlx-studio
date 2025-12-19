#!/usr/bin/env python3
"""
English Generation Test for Helix100m
Tests if trained model generates proper English without Opus failure modes.
"""

import torch
from train_qwen_distillation import TransformerLanguageModel, CharTokenizer, MODEL_CONFIG_100M

def load_model(checkpoint_path: str, device: str = "cuda"):
    """Load trained model from checkpoint."""
    tokenizer = CharTokenizer()
    model = TransformerLanguageModel(
        vocab_size=tokenizer.vocab_size,
        **MODEL_CONFIG_100M
    ).to(device)

    checkpoint = torch.load(checkpoint_path, map_location=device)
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)

    model.eval()
    return model, tokenizer

def generate_text(model, tokenizer, prompt: str, max_length: int = 100, temperature: float = 0.8, device: str = "cuda"):
    """Generate text from prompt."""
    tokens = tokenizer.encode(prompt)
    input_ids = torch.tensor([tokens], dtype=torch.long).to(device)

    generated = tokens.copy()

    with torch.no_grad():
        for _ in range(max_length):
            if len(generated) >= 256:  # Max seq length
                break

            # Get logits
            logits = model(input_ids)
            next_token_logits = logits[0, -1, :] / temperature

            # Sample
            probs = torch.softmax(next_token_logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1).item()

            # Stop on newline or special chars
            if next_token == tokenizer.char_to_idx.get('\n', 0):
                break

            generated.append(next_token)
            input_ids = torch.tensor([generated], dtype=torch.long).to(device)

    return tokenizer.decode(generated)

def test_english_generation(checkpoint_path: str):
    """Test English generation capabilities."""
    print("="*80)
    print("ENGLISH GENERATION TEST")
    print("="*80)
    print(f"Checkpoint: {checkpoint_path}\n")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}\n")

    # Load model
    print("Loading model...")
    model, tokenizer = load_model(checkpoint_path, device)
    print(f"✓ Model loaded ({sum(p.numel() for p in model.parameters())} params)\n")

    # Test prompts
    test_prompts = [
        "Search for",
        "Filter active",
        "The quick brown",
        "Represent nothing",
        "Process user",
        "Execute database",
        "Calculate",
        "Navigate to",
        "Copy",
        "Load config",
    ]

    print("="*80)
    print("GENERATION TESTS")
    print("="*80)

    results = []
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n[{i}/{len(test_prompts)}] Prompt: \"{prompt}\"")

        # Generate
        output = generate_text(model, tokenizer, prompt, max_length=50, temperature=0.7, device=device)

        # Remove prompt
        generated = output[len(prompt):]

        print(f"Generated: \"{generated}\"")

        # Check for failure modes
        parroting = generated.strip() == prompt.strip()
        collapse = len(set(generated.strip())) <= 2 and len(generated) > 5
        scrambled = all(c in "@#$%&*" for c in generated.strip()[:5]) if len(generated) >= 5 else False

        status = "✓ OK"
        if parroting:
            status = "❌ PARROTING"
        elif collapse:
            status = "❌ CHARACTER COLLAPSE"
        elif scrambled:
            status = "❌ SCRAMBLED"

        print(f"Status: {status}")

        results.append({
            'prompt': prompt,
            'generated': generated,
            'status': status,
            'parroting': parroting,
            'collapse': collapse,
            'scrambled': scrambled
        })

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    ok_count = sum(1 for r in results if r['status'] == '✓ OK')
    parroting_count = sum(1 for r in results if r['parroting'])
    collapse_count = sum(1 for r in results if r['collapse'])
    scrambled_count = sum(1 for r in results if r['scrambled'])

    print(f"Total tests: {len(results)}")
    print(f"✓ Passed: {ok_count}/{len(results)}")
    print(f"❌ Parroting: {parroting_count}")
    print(f"❌ Character collapse: {collapse_count}")
    print(f"❌ Scrambled: {scrambled_count}")

    if ok_count == len(results):
        print("\n✓✓✓ ALL TESTS PASSED - No Opus failure modes detected!")
    elif ok_count >= len(results) * 0.8:
        print(f"\n⚠ MOSTLY PASSING ({ok_count}/{len(results)}) - Some failures detected")
    else:
        print(f"\n❌ TRAINING FAILED ({ok_count}/{len(results)}) - Major issues detected")

    print("="*80)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 test_english_generation.py <checkpoint_path>")
        print("Example: python3 test_english_generation.py checkpoints/qwen_distill_BEST.pt")
        sys.exit(1)

    checkpoint_path = sys.argv[1]
    test_english_generation(checkpoint_path)
