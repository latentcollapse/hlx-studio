#!/usr/bin/env python3
"""
Comprehensive English → HLX comprehension test.
Tests the brain's ability to translate complex English to all HLX formats.

This is a DIFFICULT test with edge cases, ambiguity, and complex patterns.
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Tuple

import torch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from model import HLXLTransformer
from tokenizer import CharTokenizer


class EnglishComprehensionTest:
    """Difficult English comprehension test suite."""

    def __init__(self, model, tokenizer, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.results = []

    def generate(self, prompt: str, max_length: int = 256, temperature: float = 0.7) -> str:
        """Generate HLX output from English prompt."""
        self.model.eval()

        with torch.no_grad():
            # Encode prompt
            tokens = self.tokenizer.encode(prompt, add_special_tokens=True)
            input_ids = torch.tensor([tokens], dtype=torch.long).to(self.device)

            # Generate
            for _ in range(max_length):
                outputs = self.model(input_ids)
                logits = outputs[:, -1, :] / temperature
                probs = torch.softmax(logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)

                # Stop at EOS
                if next_token.item() == self.tokenizer.eos_token_id:
                    break

                input_ids = torch.cat([input_ids, next_token], dim=1)

            # Decode
            generated_tokens = input_ids[0].tolist()
            output = self.tokenizer.decode(generated_tokens)

            return output

    def test_basic_translation(self):
        """Level 1: Basic English → HLX translation."""
        print("\n" + "=" * 80)
        print("LEVEL 1: BASIC TRANSLATION")
        print("=" * 80)

        tests = [
            ("Search for documents", "Should translate to SEARCH operation"),
            ("Filter active users", "Should translate to FILTER operation"),
            ("Map each item to its name", "Should translate to MAP operation"),
            ("Sort users by age", "Should translate to SORT operation"),
            ("Count the items", "Should translate to COUNT operation"),
        ]

        for english, description in tests:
            print(f"\nTest: {english}")
            print(f"Expected: {description}")

            prompt = f"{english} → "
            output = self.generate(prompt, max_length=128, temperature=0.5)

            print(f"Output: {output}")

            self.results.append({
                "level": "basic",
                "english": english,
                "output": output,
                "description": description,
            })

    def test_complex_translation(self):
        """Level 2: Complex English with nested operations."""
        print("\n" + "=" * 80)
        print("LEVEL 2: COMPLEX NESTED OPERATIONS")
        print("=" * 80)

        tests = [
            ("Filter active users and sort by name", "Nested FILTER + SORT"),
            ("Map users to names then count them", "Nested MAP + COUNT"),
            ("Search for documents and filter by date", "Nested SEARCH + FILTER"),
            ("Sort items by priority then take the first 5", "Nested SORT + TAKE"),
        ]

        for english, description in tests:
            print(f"\nTest: {english}")
            print(f"Expected: {description}")

            prompt = f"{english} → "
            output = self.generate(prompt, max_length=256, temperature=0.5)

            print(f"Output: {output}")

            self.results.append({
                "level": "complex",
                "english": english,
                "output": output,
                "description": description,
            })

    def test_ambiguous_translation(self):
        """Level 3: Ambiguous English requiring inference."""
        print("\n" + "=" * 80)
        print("LEVEL 3: AMBIGUOUS TRANSLATION (INFERENCE REQUIRED)")
        print("=" * 80)

        tests = [
            ("Get the active ones", "Must infer FILTER on 'active' status"),
            ("Show me the top results", "Must infer SORT + TAKE"),
            ("Find what I'm looking for", "Must infer SEARCH operation"),
            ("Organize by importance", "Must infer SORT by priority/importance"),
            ("Remove duplicates", "Must infer DISTINCT operation"),
        ]

        for english, description in tests:
            print(f"\nTest: {english}")
            print(f"Expected: {description}")

            prompt = f"{english} → "
            output = self.generate(prompt, max_length=256, temperature=0.7)

            print(f"Output: {output}")

            self.results.append({
                "level": "ambiguous",
                "english": english,
                "output": output,
                "description": description,
            })

    def test_edge_cases(self):
        """Level 4: Edge cases and unusual inputs."""
        print("\n" + "=" * 80)
        print("LEVEL 4: EDGE CASES")
        print("=" * 80)

        tests = [
            ("", "Empty input - should handle gracefully"),
            ("asdfghjkl qwertyuiop", "Nonsense input"),
            ("!!@@## $$%%^^", "Special characters only"),
            ("Search search Search SEARCH", "Repeated words with case variation"),
            ("Do something with the things", "Extremely vague request"),
        ]

        for english, description in tests:
            print(f"\nTest: '{english}'")
            print(f"Expected: {description}")

            prompt = f"{english} → "
            output = self.generate(prompt, max_length=256, temperature=0.7)

            print(f"Output: {output}")

            self.results.append({
                "level": "edge_case",
                "english": english,
                "output": output,
                "description": description,
            })

    def test_multi_format_generation(self):
        """Level 5: Generate in different HLX formats."""
        print("\n" + "=" * 80)
        print("LEVEL 5: MULTI-FORMAT GENERATION")
        print("=" * 80)

        english = "Search for documents"

        # Test HLXL format
        print(f"\nTest: {english} (HLXL format)")
        prompt_hlxl = f"{english} → HLXL: "
        output_hlxl = self.generate(prompt_hlxl, max_length=128, temperature=0.5)
        print(f"HLXL Output: {output_hlxl}")

        # Test LC-R format
        print(f"\nTest: {english} (LC-R format)")
        prompt_lcr = f"{english} → LC-R: "
        output_lcr = self.generate(prompt_lcr, max_length=128, temperature=0.5)
        print(f"LC-R Output: {output_lcr}")

        # Test LC-T format
        print(f"\nTest: {english} (LC-T format)")
        prompt_lct = f"{english} → LC-T: "
        output_lct = self.generate(prompt_lct, max_length=128, temperature=0.5)
        print(f"LC-T Output: {output_lct}")

        # Test LC-B format
        print(f"\nTest: {english} (LC-B format)")
        prompt_lcb = f"{english} → LC-B: "
        output_lcb = self.generate(prompt_lcb, max_length=128, temperature=0.5)
        print(f"LC-B Output: {output_lcb}")

        self.results.append({
            "level": "multi_format",
            "english": english,
            "hlxl": output_hlxl,
            "lc_r": output_lcr,
            "lc_t": output_lct,
            "lc_b": output_lcb,
        })

    def test_reasoning_capability(self):
        """Level 6: Test reasoning about HLX semantics."""
        print("\n" + "=" * 80)
        print("LEVEL 6: REASONING CAPABILITY")
        print("=" * 80)

        tests = [
            ("What operation finds items?", "Should reason about SEARCH"),
            ("How do I get only some items?", "Should reason about FILTER/TAKE"),
            ("Transform each element", "Should reason about MAP"),
            ("Combine two collections", "Should reason about JOIN/MERGE"),
            ("Calculate sum of numbers", "Should reason about REDUCE/SUM"),
        ]

        for english, description in tests:
            print(f"\nTest: {english}")
            print(f"Expected: {description}")

            prompt = f"{english} → "
            output = self.generate(prompt, max_length=256, temperature=0.7)

            print(f"Output: {output}")

            self.results.append({
                "level": "reasoning",
                "english": english,
                "output": output,
                "description": description,
            })

    def run_all_tests(self) -> Dict:
        """Run complete test suite."""
        print("=" * 80)
        print("ENGLISH COMPREHENSION TEST SUITE")
        print("=" * 80)
        print(f"Starting at: {datetime.utcnow().isoformat()}Z")
        print("=" * 80)

        # Run all test levels
        self.test_basic_translation()
        self.test_complex_translation()
        self.test_ambiguous_translation()
        self.test_edge_cases()
        self.test_multi_format_generation()
        self.test_reasoning_capability()

        # Summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Total tests: {len(self.results)}")
        print(f"Levels tested: 6")
        print("=" * 80)

        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_tests": len(self.results),
            "results": self.results,
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Test English comprehension")
    parser.add_argument("--checkpoint", type=str, required=True,
                        help="Path to model checkpoint")
    parser.add_argument("--output", type=str, default="english_comprehension_results.json",
                        help="Output JSON file")

    args = parser.parse_args()

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer = CharTokenizer()

    # Load model
    print(f"Loading model from {args.checkpoint}...")
    checkpoint = torch.load(args.checkpoint, map_location=device)

    # Infer model architecture from checkpoint
    if 'model_state_dict' in checkpoint:
        state_dict = checkpoint['model_state_dict']
    else:
        state_dict = checkpoint

    # Check if this is tiny or 1B model
    total_params = sum(p.numel() for p in state_dict.values())
    print(f"Model size: {total_params:,} parameters")

    if total_params < 1_000_000:
        # Tiny model
        print("Detected: Tiny brain (492K params)")
        model = HLXLTransformer(
            vocab_size=tokenizer.vocab_size,
            d_model=128,
            nhead=4,
            num_layers=2,
            dim_feedforward=512,
            dropout=0.1,
            max_seq_length=256,
        )
    else:
        # 1B model
        print("Detected: 1B brain")
        model = HLXLTransformer(
            vocab_size=tokenizer.vocab_size,
            d_model=2048,
            nhead=16,
            num_layers=20,
            dim_feedforward=8192,
            dropout=0.1,
            max_seq_length=512,
        )

    model.load_state_dict(state_dict)
    model = model.to(device)
    model.eval()

    print(f"✓ Model loaded: {sum(p.numel() for p in model.parameters()):,} parameters")

    # Run tests
    tester = EnglishComprehensionTest(model, tokenizer, device)
    results = tester.run_all_tests()

    # Save results
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Results saved to {args.output}")


if __name__ == "__main__":
    main()
