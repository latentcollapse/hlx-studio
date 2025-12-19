#!/usr/bin/env python3
"""
Checkpoint Quality Validation Suite
Tests trained HLX Brain checkpoints for common failure modes.

Detects:
- Parroting (model just echoes input)
- Character collapse (repetitive tokens)
- Scrambled output (random glyphs/nonsense)
- HLX syntax validity
- Output coherence

Usage:
    python3 validate_checkpoint_quality.py --checkpoint path/to/checkpoint.pt

Exit codes:
    0: PASS - checkpoint quality acceptable
    1: FAIL - checkpoint has critical issues
    2: WARN - checkpoint has minor issues but may be usable
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import re

import torch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from tokenizer import create_tokenizer
from model import create_model


# Standard test prompts covering different use cases
STANDARD_TEST_PROMPTS = [
    "Search for documents",
    "Filter active users",
    "Map each item to its name",
    "Sort users by age descending",
    "Count the items",
]

# Expected behaviors (used for detecting parroting)
EXPECTED_TRANSFORMATIONS = {
    "Search for documents": ["SEARCH", "search", "🜊", "FIND"],
    "Filter active users": ["FILTER", "WHERE", "filter", "🜁"],
    "Map each item to its name": ["MAP", "map", "🜃", "TRANSFORM"],
    "Sort users by age descending": ["SORT", "ORDER", "sort", "DESC"],
    "Count the items": ["COUNT", "count", "🜄", "AGGREGATE"],
}


class CheckpointQualityValidator:
    """Validates checkpoint quality with multiple failure mode detectors."""

    def __init__(self, checkpoint_path: str, device: str = "cuda"):
        self.checkpoint_path = checkpoint_path
        self.device = device
        self.model = None
        self.tokenizer = None
        self.results = {
            "checkpoint": checkpoint_path,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tests": [],
            "failures": [],
            "warnings": [],
            "pass": False,
        }

    def load_checkpoint(self) -> bool:
        """Load checkpoint and infer architecture."""
        try:
            print(f"Loading checkpoint: {self.checkpoint_path}")

            if not Path(self.checkpoint_path).exists():
                self.results["failures"].append(f"Checkpoint file not found: {self.checkpoint_path}")
                return False

            checkpoint = torch.load(self.checkpoint_path, map_location=self.device)
            state_dict = checkpoint.get("model_state_dict", checkpoint)

            # Infer architecture
            vocab_size = state_dict["token_embedding.weight"].shape[0]
            d_model = state_dict["token_embedding.weight"].shape[1]
            num_layers = sum(1 for k in state_dict.keys()
                           if k.startswith("transformer.layers.") and k.endswith(".self_attn.in_proj_weight"))

            # Determine architecture parameters
            if d_model == 128:
                # Tiny model
                nhead, dim_feedforward = 4, 512
                model_name = "Tiny (492K)"
            elif d_model == 384:
                # 10M model
                nhead, dim_feedforward = 6, 1536
                model_name = "10M (7.4M)"
            elif d_model == 512:
                # Small model
                nhead, dim_feedforward = 8, 2048
                model_name = "Small (24M)"
            elif d_model == 1024:
                # 100M model
                nhead, dim_feedforward = 16, 4096
                model_name = "100M (102M)"
            elif d_model == 1280:
                # 250M model
                nhead, dim_feedforward = 16, 5120
                model_name = "250M (237M)"
            elif d_model == 2048:
                # 1B model
                nhead, dim_feedforward = 16, 8192
                model_name = "1B (1.0B)"
            else:
                self.results["failures"].append(f"Unknown architecture: d_model={d_model}")
                return False

            # Create model
            self.tokenizer = create_tokenizer()

            if vocab_size != self.tokenizer.vocab_size:
                self.results["warnings"].append(
                    f"Vocab size mismatch: checkpoint={vocab_size}, tokenizer={self.tokenizer.vocab_size}"
                )

            self.model = create_model(
                vocab_size=vocab_size,
                d_model=d_model,
                nhead=nhead,
                num_layers=num_layers,
                dim_feedforward=dim_feedforward,
                dropout=0.1,
            )

            self.model.load_state_dict(state_dict)
            self.model = self.model.to(self.device)
            self.model.eval()

            total_params = sum(p.numel() for p in self.model.parameters())

            self.results["model_info"] = {
                "name": model_name,
                "total_params": total_params,
                "d_model": d_model,
                "num_layers": num_layers,
                "nhead": nhead,
                "dim_feedforward": dim_feedforward,
                "vocab_size": vocab_size,
            }

            print(f"✓ Loaded {model_name} model: {total_params:,} parameters")
            return True

        except Exception as e:
            self.results["failures"].append(f"Failed to load checkpoint: {str(e)}")
            return False

    def generate(self, prompt: str, max_length: int = 128, temperature: float = 0.7) -> str:
        """Generate output from prompt."""
        self.model.eval()

        with torch.no_grad():
            # Encode
            tokens = self.tokenizer.encode(prompt, add_special_tokens=True)
            input_ids = torch.tensor([tokens], dtype=torch.long).to(self.device)
            input_length = len(tokens)

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
            output = self.tokenizer.decode(generated_tokens, skip_special_tokens=False)

            # Get just the generated part (not the prompt)
            generated_part = self.tokenizer.decode(generated_tokens[input_length:], skip_special_tokens=True)

            return output, generated_part

    def test_parroting(self) -> Dict:
        """Test if model is just echoing input (10M failure mode)."""
        print("\n" + "="*80)
        print("TEST: Parroting Detection")
        print("="*80)

        test_result = {
            "name": "parroting_detection",
            "status": "pass",
            "details": [],
        }

        parroting_count = 0

        for prompt in STANDARD_TEST_PROMPTS[:3]:  # Test first 3
            full_output, generated = self.generate(prompt, max_length=50, temperature=0.5)

            # Check if output is just prompt + minimal addition
            is_parroting = (
                generated.strip() in ["", "...", " ..."] or
                len(generated.strip()) < 3 or
                generated.strip() == prompt.strip()
            )

            test_result["details"].append({
                "prompt": prompt,
                "generated": generated[:100],
                "is_parroting": is_parroting,
            })

            if is_parroting:
                parroting_count += 1
                print(f"⚠ Parroting detected: '{prompt}' → '{generated}'")
            else:
                print(f"✓ Transform detected: '{prompt}' → '{generated[:50]}...'")

        if parroting_count >= 2:
            test_result["status"] = "fail"
            self.results["failures"].append(
                f"Parroting failure: {parroting_count}/3 prompts just echoed back"
            )
        elif parroting_count == 1:
            test_result["status"] = "warn"
            self.results["warnings"].append("Possible parroting behavior detected")

        self.results["tests"].append(test_result)
        return test_result

    def test_character_collapse(self) -> Dict:
        """Test for repetitive character generation (250M failure mode)."""
        print("\n" + "="*80)
        print("TEST: Character Collapse Detection")
        print("="*80)

        test_result = {
            "name": "character_collapse",
            "status": "pass",
            "details": [],
        }

        collapse_count = 0

        for prompt in STANDARD_TEST_PROMPTS[:3]:
            full_output, generated = self.generate(prompt, max_length=100, temperature=0.7)

            # Check for repetitive characters
            # Look for patterns like ":::::" or "pppppp" or "......"
            repetition_patterns = [
                (r'(.)\1{5,}', "Same character repeated 6+ times"),
                (r'(..)\1{3,}', "2-char pattern repeated 4+ times"),
                (r'(...)\1{2,}', "3-char pattern repeated 3+ times"),
            ]

            detected_patterns = []
            for pattern, description in repetition_patterns:
                matches = re.findall(pattern, generated)
                if matches:
                    detected_patterns.append(description)

            has_collapse = len(detected_patterns) > 0

            test_result["details"].append({
                "prompt": prompt,
                "generated": generated[:100],
                "has_collapse": has_collapse,
                "patterns": detected_patterns,
            })

            if has_collapse:
                collapse_count += 1
                print(f"⚠ Character collapse: '{prompt}' → '{generated[:50]}...'")
                print(f"  Patterns: {', '.join(detected_patterns)}")
            else:
                print(f"✓ No collapse: '{prompt}' → '{generated[:50]}...'")

        if collapse_count >= 2:
            test_result["status"] = "fail"
            self.results["failures"].append(
                f"Character collapse failure: {collapse_count}/3 prompts show repetition"
            )
        elif collapse_count == 1:
            test_result["status"] = "warn"
            self.results["warnings"].append("Possible character collapse detected")

        self.results["tests"].append(test_result)
        return test_result

    def test_scrambled_output(self) -> Dict:
        """Test for scrambled/nonsense output (100M failure mode)."""
        print("\n" + "="*80)
        print("TEST: Scrambled Output Detection")
        print("="*80)

        test_result = {
            "name": "scrambled_output",
            "status": "pass",
            "details": [],
        }

        scrambled_count = 0

        for prompt in STANDARD_TEST_PROMPTS[:3]:
            full_output, generated = self.generate(prompt, max_length=80, temperature=0.5)

            # Check for signs of scrambled output:
            # 1. Mix of random symbols and letters
            # 2. JSON-like fragments that don't make sense
            # 3. Extremely high symbol-to-letter ratio

            symbol_count = len(re.findall(r'[^a-zA-Z0-9\s]', generated))
            letter_count = len(re.findall(r'[a-zA-Z]', generated))

            if letter_count > 0:
                symbol_ratio = symbol_count / letter_count
            else:
                symbol_ratio = float('inf')

            # Check for random fragments
            has_json_fragments = bool(re.search(r'\{[@:"]|\d+:\s*["\']', generated))
            has_random_symbols = symbol_ratio > 1.5  # More symbols than letters

            is_scrambled = has_json_fragments or has_random_symbols

            test_result["details"].append({
                "prompt": prompt,
                "generated": generated[:100],
                "is_scrambled": is_scrambled,
                "symbol_ratio": symbol_ratio,
                "has_json_fragments": has_json_fragments,
            })

            if is_scrambled:
                scrambled_count += 1
                print(f"⚠ Scrambled output: '{prompt}' → '{generated[:50]}...'")
                print(f"  Symbol ratio: {symbol_ratio:.2f}, JSON fragments: {has_json_fragments}")
            else:
                print(f"✓ Coherent output: '{prompt}' → '{generated[:50]}...'")

        if scrambled_count >= 2:
            test_result["status"] = "fail"
            self.results["failures"].append(
                f"Scrambled output failure: {scrambled_count}/3 prompts produced nonsense"
            )
        elif scrambled_count == 1:
            test_result["status"] = "warn"
            self.results["warnings"].append("Possible scrambled output detected")

        self.results["tests"].append(test_result)
        return test_result

    def test_hlx_transformation(self) -> Dict:
        """Test if model produces any HLX-like output."""
        print("\n" + "="*80)
        print("TEST: HLX Transformation Capability")
        print("="*80)

        test_result = {
            "name": "hlx_transformation",
            "status": "pass",
            "details": [],
        }

        transform_count = 0

        for prompt in STANDARD_TEST_PROMPTS:
            full_output, generated = self.generate(prompt, max_length=100, temperature=0.6)

            expected_keywords = EXPECTED_TRANSFORMATIONS.get(prompt, [])

            # Check if ANY expected HLX keywords appear
            found_keywords = [kw for kw in expected_keywords if kw in generated]
            has_transformation = len(found_keywords) > 0

            test_result["details"].append({
                "prompt": prompt,
                "generated": generated[:100],
                "has_transformation": has_transformation,
                "found_keywords": found_keywords,
            })

            if has_transformation:
                transform_count += 1
                print(f"✓ HLX transform: '{prompt}' → found {found_keywords}")
            else:
                print(f"⚠ No HLX: '{prompt}' → '{generated[:50]}...'")

        if transform_count < 2:
            test_result["status"] = "fail"
            self.results["failures"].append(
                f"HLX transformation failure: only {transform_count}/5 prompts produced HLX"
            )
        elif transform_count < 4:
            test_result["status"] = "warn"
            self.results["warnings"].append("Weak HLX transformation capability")

        self.results["tests"].append(test_result)
        return test_result

    def test_output_diversity(self) -> Dict:
        """Test if model can produce diverse outputs."""
        print("\n" + "="*80)
        print("TEST: Output Diversity")
        print("="*80)

        test_result = {
            "name": "output_diversity",
            "status": "pass",
            "details": [],
        }

        # Generate same prompt multiple times
        prompt = "Search for documents"
        outputs = []

        for i in range(3):
            _, generated = self.generate(prompt, max_length=60, temperature=0.8)
            outputs.append(generated)

        # Check if outputs are all identical (bad)
        unique_outputs = len(set(outputs))

        test_result["details"] = {
            "prompt": prompt,
            "outputs": outputs,
            "unique_count": unique_outputs,
        }

        if unique_outputs == 1:
            test_result["status"] = "warn"
            self.results["warnings"].append("Model produces identical outputs (low diversity)")
            print(f"⚠ All outputs identical: '{outputs[0][:50]}...'")
        else:
            print(f"✓ {unique_outputs}/3 unique outputs generated")

        self.results["tests"].append(test_result)
        return test_result

    def run_all_tests(self) -> bool:
        """Run complete validation suite."""
        print("="*80)
        print("HLX BRAIN CHECKPOINT QUALITY VALIDATION")
        print("="*80)
        print(f"Checkpoint: {self.checkpoint_path}")
        print(f"Device: {self.device}")
        print("="*80)

        # Load checkpoint
        if not self.load_checkpoint():
            print("\n❌ Failed to load checkpoint")
            return False

        # Run all tests
        self.test_parroting()
        self.test_character_collapse()
        self.test_scrambled_output()
        self.test_hlx_transformation()
        self.test_output_diversity()

        # Determine overall pass/fail
        failed_tests = [t for t in self.results["tests"] if t["status"] == "fail"]
        warned_tests = [t for t in self.results["tests"] if t["status"] == "warn"]

        self.results["summary"] = {
            "total_tests": len(self.results["tests"]),
            "passed": len(self.results["tests"]) - len(failed_tests) - len(warned_tests),
            "warned": len(warned_tests),
            "failed": len(failed_tests),
        }

        if len(failed_tests) == 0:
            self.results["pass"] = True
            print("\n" + "="*80)
            print("✓ VALIDATION PASSED")
            print("="*80)
            print(f"  Passed: {self.results['summary']['passed']}/{self.results['summary']['total_tests']}")
            if warned_tests:
                print(f"  Warnings: {len(warned_tests)}")
            return True
        else:
            self.results["pass"] = False
            print("\n" + "="*80)
            print("❌ VALIDATION FAILED")
            print("="*80)
            print(f"  Failed tests: {len(failed_tests)}")
            print(f"  Critical failures:")
            for failure in self.results["failures"]:
                print(f"    - {failure}")
            return False

    def save_results(self, output_path: str):
        """Save validation results to JSON."""
        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\n✓ Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Validate HLX Brain checkpoint quality")
    parser.add_argument("--checkpoint", type=str, required=True,
                        help="Path to checkpoint file")
    parser.add_argument("--output", type=str, default=None,
                        help="Output JSON file (default: auto-generated)")
    parser.add_argument("--device", type=str, default="cuda",
                        help="Device to use (cuda/cpu)")

    args = parser.parse_args()

    # Determine device
    device = args.device
    if device == "cuda" and not torch.cuda.is_available():
        print("⚠ CUDA not available, falling back to CPU")
        device = "cpu"

    # Auto-generate output filename if not specified
    if args.output is None:
        checkpoint_name = Path(args.checkpoint).stem
        args.output = f"validation_{checkpoint_name}.json"

    # Run validation
    validator = CheckpointQualityValidator(args.checkpoint, device)
    passed = validator.run_all_tests()

    # Save results
    validator.save_results(args.output)

    # Exit with appropriate code
    if passed:
        sys.exit(0)  # PASS
    elif len(validator.results["warnings"]) > 0 and len(validator.results["failures"]) == 0:
        sys.exit(2)  # WARN
    else:
        sys.exit(1)  # FAIL


if __name__ == "__main__":
    main()
