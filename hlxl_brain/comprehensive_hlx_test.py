#!/usr/bin/env python3
"""
COMPREHENSIVE HLX FAMILY TEST SUITE

Tests ALL variants of the HLX language family with maximum rigor:
- HLX (core high-level expressions)
- HLX-LS (line-separated format)
- HLXL (human-readable language)
- HLXL-LS (line-separated HLXL)
- LC-R (Latent Collapse Runic - glyph format)
- LC-T (Latent Collapse Text - if applicable)
- LC-B (Latent Collapse Binary - if applicable)

Rigorous testing trains the brain. This evaluates:
1. Syntax generation for each format
2. Cross-format translation
3. Semantic understanding
4. Edge cases and error handling
5. Nested structures
6. Performance across complexity levels
"""

import sys
from pathlib import Path
import torch
import json
from typing import Dict, List, Tuple
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tokenizer import create_tokenizer
from model import create_model


class HLXFamilyTestSuite:
    """Comprehensive test suite for all HLX variants."""

    def __init__(self, model, tokenizer, device="cuda"):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.results = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "model_params": model.count_parameters(),
            "tests": {}
        }

    def generate(self, prompt: str, max_tokens: int = 100, temperature: float = 0.0) -> str:
        """Generate text from model."""
        self.model.eval()
        prompt_ids = self.tokenizer.encode(prompt, add_special_tokens=True)
        prompt_tensor = torch.tensor([prompt_ids], dtype=torch.long).to(self.device)

        with torch.no_grad():
            generated = self.model.generate(
                prompt_tensor,
                max_new_tokens=max_tokens,
                temperature=temperature
            )

        return self.tokenizer.decode(generated[0].cpu().tolist(), skip_special_tokens=False)

    # ========================================================================
    # LEVEL 1: BASIC SYNTAX GENERATION
    # ========================================================================

    def test_hlx_basic_syntax(self) -> Dict:
        """Test basic HLX syntax generation."""
        print("\n[LEVEL 1.1] Testing HLX Basic Syntax...")

        tests = [
            # Simple operations
            ("HLX: search", "Basic search operation"),
            ("HLX: filter", "Basic filter operation"),
            ("HLX: transform", "Basic transform operation"),
            ("HLX: aggregate", "Basic aggregate operation"),

            # With parameters
            ("HLX: search documents", "Search with target"),
            ("HLX: filter active users", "Filter with condition"),
            ("HLX: transform data to json", "Transform with types"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=50)
            results.append({
                "prompt": prompt,
                "description": description,
                "output": output[:200],
                "length": len(output)
            })

        return {"tests": results, "count": len(tests)}

    def test_hlx_ls_format(self) -> Dict:
        """Test HLX-LS (Line-Separated) format."""
        print("\n[LEVEL 1.2] Testing HLX-LS Format...")

        tests = [
            ("HLX-LS:\nsearch\nfilter\ntransform", "Multi-line operations"),
            ("HLX-LS:\noperation: search\ntarget: documents\nfilter: active", "Structured format"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=80)
            results.append({
                "prompt": prompt.replace("\n", "\\n"),
                "description": description,
                "output": output[:200],
            })

        return {"tests": results, "count": len(tests)}

    def test_hlxl_syntax(self) -> Dict:
        """Test HLXL (HLX Language) syntax."""
        print("\n[LEVEL 1.3] Testing HLXL Syntax...")

        tests = [
            ("HLXL: SEARCH documents WHERE status = active", "HLXL query syntax"),
            ("HLXL: FILTER users BY role", "HLXL filter with BY clause"),
            ("HLXL: TRANSFORM data FROM json TO xml", "HLXL transform with types"),
            ("HLXL: AGGREGATE sales GROUP BY region", "HLXL aggregation"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=60)
            results.append({
                "prompt": prompt,
                "description": description,
                "output": output[:200],
            })

        return {"tests": results, "count": len(tests)}

    def test_hlxl_ls_format(self) -> Dict:
        """Test HLXL-LS (Line-Separated HLXL) format."""
        print("\n[LEVEL 1.4] Testing HLXL-LS Format...")

        tests = [
            ("HLXL-LS:\nSEARCH documents\nWHERE status = active\nLIMIT 10", "Multi-line HLXL query"),
            ("HLXL-LS:\nFILTER users\nBY role = admin\nORDER BY created", "Complex HLXL-LS"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=80)
            results.append({
                "prompt": prompt.replace("\n", "\\n"),
                "description": description,
                "output": output[:200],
            })

        return {"tests": results, "count": len(tests)}

    def test_lcr_glyph_syntax(self) -> Dict:
        """Test LC-R (Latent Collapse Runic) glyph format."""
        print("\n[LEVEL 1.5] Testing LC-R Glyph Syntax...")

        tests = [
            # Basic LC-R structure
            ("LC-R: 🜊1000🜁0", "LC-R request ID prefix"),
            ("LC-R: 🜊1000🜁0 \"search\"🜁1", "LC-R with operation"),
            ("LC-R: 🜊1000🜁0 \"search\"🜁1 ⟁documents🜁2", "LC-R with entity reference"),
            ("LC-R: 🜊1000🜁0 \"filter\"🜁1 ⟁users🜁2 \"active\"🜂", "Complete LC-R command"),

            # Different operations
            ("LC-R: 🜊2000🜁0 \"transform\"🜁1", "LC-R transform"),
            ("LC-R: 🜊3000🜁0 \"aggregate\"🜁1", "LC-R aggregate"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=70)
            results.append({
                "prompt": prompt,
                "description": description,
                "output": output[:200],
                "has_glyphs": any(g in output for g in ['🜊', '🜁', '🜂', '⟁'])
            })

        return {"tests": results, "count": len(tests)}

    # ========================================================================
    # LEVEL 2: CROSS-FORMAT TRANSLATION
    # ========================================================================

    def test_english_to_hlx(self) -> Dict:
        """Test English → HLX translation."""
        print("\n[LEVEL 2.1] Testing English → HLX Translation...")

        tests = [
            ("Search for documents", "Simple search"),
            ("Filter active users", "Filter with condition"),
            ("Transform data to JSON format", "Transform with type"),
            ("Aggregate sales by region", "Aggregation query"),
            ("Navigate to home page", "Navigation command"),
            ("Delete old records", "Delete operation"),
        ]

        results = []
        for english, description in tests:
            prompt = f"{english} →"
            output = self.generate(prompt, max_tokens=60)
            results.append({
                "english": english,
                "description": description,
                "output": output[:200],
            })

        return {"tests": results, "count": len(tests)}

    def test_english_to_lcr(self) -> Dict:
        """Test English → LC-R translation."""
        print("\n[LEVEL 2.2] Testing English → LC-R Translation...")

        tests = [
            ("Search for documents", "English to LC-R glyph format"),
            ("Filter active users", "English to LC-R with condition"),
            ("Navigate to settings", "English to LC-R navigation"),
        ]

        results = []
        for english, description in tests:
            prompt = f"{english} →"
            output = self.generate(prompt, max_tokens=60)
            has_glyphs = any(g in output for g in ['🜊', '🜁', '🜂', '⟁'])
            results.append({
                "english": english,
                "description": description,
                "output": output[:200],
                "has_lcr_glyphs": has_glyphs
            })

        return {"tests": results, "count": len(tests)}

    def test_hlx_to_lcr(self) -> Dict:
        """Test HLX → LC-R format conversion."""
        print("\n[LEVEL 2.3] Testing HLX → LC-R Conversion...")

        tests = [
            ("HLX: search documents", "HLX search to LC-R"),
            ("HLX: filter users active", "HLX filter to LC-R"),
        ]

        results = []
        for hlx, description in tests:
            prompt = f"{hlx} → LC-R:"
            output = self.generate(prompt, max_tokens=60)
            has_glyphs = any(g in output for g in ['🜊', '🜁', '🜂', '⟁'])
            results.append({
                "hlx": hlx,
                "description": description,
                "output": output[:200],
                "has_lcr_glyphs": has_glyphs
            })

        return {"tests": results, "count": len(tests)}

    def test_lcr_to_hlxl(self) -> Dict:
        """Test LC-R → HLXL format conversion."""
        print("\n[LEVEL 2.4] Testing LC-R → HLXL Conversion...")

        tests = [
            ("LC-R: 🜊1000🜁0 \"search\"🜁1 ⟁documents🜁2 → HLXL:", "LC-R to HLXL expansion"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=60)
            results.append({
                "prompt": prompt,
                "description": description,
                "output": output[:200],
            })

        return {"tests": results, "count": len(tests)}

    # ========================================================================
    # LEVEL 3: COMPLEX STRUCTURES
    # ========================================================================

    def test_nested_operations(self) -> Dict:
        """Test nested/chained operations."""
        print("\n[LEVEL 3.1] Testing Nested Operations...")

        tests = [
            ("HLXL: SEARCH documents WHERE (status = active AND role = admin)", "Nested conditions"),
            ("HLX: filter(search(documents)) by active", "Chained operations"),
            ("LC-R: 🜊1000🜁0 \"search\"🜁1 ⟁documents🜁2 \"filter\"🜁3 ⟁active", "Multi-operation LC-R"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=80)
            results.append({
                "prompt": prompt,
                "description": description,
                "output": output[:250],
            })

        return {"tests": results, "count": len(tests)}

    def test_multiline_programs(self) -> Dict:
        """Test multi-line HLX programs."""
        print("\n[LEVEL 3.2] Testing Multi-line Programs...")

        tests = [
            ("HLXL-LS:\nSEARCH documents\nFILTER status = active\nTRANSFORM to json\nAGGREGATE by region", "4-step program"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=100)
            results.append({
                "prompt": prompt.replace("\n", "\\n"),
                "description": description,
                "output": output[:300],
            })

        return {"tests": results, "count": len(tests)}

    def test_parameterized_operations(self) -> Dict:
        """Test operations with multiple parameters."""
        print("\n[LEVEL 3.3] Testing Parameterized Operations...")

        tests = [
            ("HLXL: SEARCH documents WHERE status = active AND created > 2024-01-01 LIMIT 10", "Multiple parameters"),
            ("HLX: transform data {format: json, compression: gzip, encoding: utf8}", "Structured params"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=80)
            results.append({
                "prompt": prompt,
                "description": description,
                "output": output[:250],
            })

        return {"tests": results, "count": len(tests)}

    # ========================================================================
    # LEVEL 4: EDGE CASES & ERROR HANDLING
    # ========================================================================

    def test_empty_and_minimal(self) -> Dict:
        """Test edge cases with minimal input."""
        print("\n[LEVEL 4.1] Testing Empty & Minimal Cases...")

        tests = [
            ("HLX:", "Empty HLX"),
            ("HLXL:", "Empty HLXL"),
            ("LC-R:", "Empty LC-R"),
            ("LC-R: 🜊", "Minimal LC-R prefix"),
            ("HLXL: SEARCH", "Incomplete HLXL"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=50)
            results.append({
                "prompt": prompt,
                "description": description,
                "output": output[:200],
            })

        return {"tests": results, "count": len(tests)}

    def test_special_characters(self) -> Dict:
        """Test handling of special characters and symbols."""
        print("\n[LEVEL 4.2] Testing Special Characters...")

        tests = [
            ("HLX: search \"documents with spaces\"", "Quoted strings"),
            ("HLXL: FILTER users WHERE email LIKE '%@example.com'", "SQL-like wildcards"),
            ("LC-R: 🜊1000🜁0 \"search\"🜁1 ⟁⟁nested", "Double entity reference"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=60)
            results.append({
                "prompt": prompt,
                "description": description,
                "output": output[:200],
            })

        return {"tests": results, "count": len(tests)}

    def test_large_sequences(self) -> Dict:
        """Test handling of longer sequences."""
        print("\n[LEVEL 4.3] Testing Large Sequences...")

        tests = [
            ("HLXL: SEARCH documents WHERE status IN (active, pending, review) AND priority IN (high, critical) AND assigned_to IN (user1, user2, user3)", "Long condition list"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=120)
            results.append({
                "prompt": prompt,
                "description": description,
                "output": output[:300],
            })

        return {"tests": results, "count": len(tests)}

    # ========================================================================
    # LEVEL 5: SEMANTIC UNDERSTANDING
    # ========================================================================

    def test_operation_semantics(self) -> Dict:
        """Test understanding of operation semantics."""
        print("\n[LEVEL 5.1] Testing Operation Semantics...")

        tests = [
            ("What does SEARCH do? →", "Explain SEARCH"),
            ("What is the difference between FILTER and SEARCH? →", "Compare operations"),
            ("How does AGGREGATE work? →", "Explain AGGREGATE"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=80)
            results.append({
                "prompt": prompt,
                "description": description,
                "output": output[:250],
            })

        return {"tests": results, "count": len(tests)}

    def test_format_awareness(self) -> Dict:
        """Test awareness of different format purposes."""
        print("\n[LEVEL 5.2] Testing Format Awareness...")

        tests = [
            ("When should I use LC-R vs HLXL? →", "Format selection"),
            ("What is LC-R optimized for? →", "LC-R purpose"),
        ]

        results = []
        for prompt, description in tests:
            output = self.generate(prompt, max_tokens=80)
            results.append({
                "prompt": prompt,
                "description": description,
                "output": output[:250],
            })

        return {"tests": results, "count": len(tests)}

    # ========================================================================
    # LEVEL 6: PERFORMANCE & CONSISTENCY
    # ========================================================================

    def test_generation_consistency(self) -> Dict:
        """Test consistency of generation (temperature=0)."""
        print("\n[LEVEL 6.1] Testing Generation Consistency...")

        prompt = "LC-R: 🜊1000🜁0 \"search\"🜁1"

        runs = []
        for i in range(5):
            output = self.generate(prompt, max_tokens=50, temperature=0.0)
            runs.append(output)

        # Check if all runs are identical (deterministic)
        all_same = all(run == runs[0] for run in runs)

        return {
            "prompt": prompt,
            "runs": [r[:100] for r in runs],
            "deterministic": all_same,
            "count": 5
        }

    def test_generation_speed(self) -> Dict:
        """Test generation speed across formats."""
        print("\n[LEVEL 6.2] Testing Generation Speed...")

        import time

        tests = [
            ("HLX: search documents", "HLX"),
            ("HLXL: SEARCH documents", "HLXL"),
            ("LC-R: 🜊1000🜁0 \"search\"", "LC-R"),
        ]

        results = []
        for prompt, format_name in tests:
            start = time.perf_counter()
            output = self.generate(prompt, max_tokens=50)
            elapsed = time.perf_counter() - start

            results.append({
                "format": format_name,
                "time_ms": elapsed * 1000,
                "output_length": len(output)
            })

        return {"tests": results, "count": len(tests)}

    # ========================================================================
    # MAIN TEST RUNNER
    # ========================================================================

    def run_all_tests(self) -> Dict:
        """Run complete test suite."""
        print("="*80)
        print("COMPREHENSIVE HLX FAMILY TEST SUITE")
        print("="*80)
        print(f"Model: {self.model.count_parameters():,} parameters")
        print(f"Device: {self.device}")
        print("="*80)

        test_groups = [
            ("LEVEL 1: BASIC SYNTAX", [
                ("hlx_basic", self.test_hlx_basic_syntax),
                ("hlx_ls", self.test_hlx_ls_format),
                ("hlxl", self.test_hlxl_syntax),
                ("hlxl_ls", self.test_hlxl_ls_format),
                ("lcr_glyphs", self.test_lcr_glyph_syntax),
            ]),
            ("LEVEL 2: CROSS-FORMAT TRANSLATION", [
                ("english_to_hlx", self.test_english_to_hlx),
                ("english_to_lcr", self.test_english_to_lcr),
                ("hlx_to_lcr", self.test_hlx_to_lcr),
                ("lcr_to_hlxl", self.test_lcr_to_hlxl),
            ]),
            ("LEVEL 3: COMPLEX STRUCTURES", [
                ("nested_ops", self.test_nested_operations),
                ("multiline", self.test_multiline_programs),
                ("parameterized", self.test_parameterized_operations),
            ]),
            ("LEVEL 4: EDGE CASES", [
                ("empty_minimal", self.test_empty_and_minimal),
                ("special_chars", self.test_special_characters),
                ("large_sequences", self.test_large_sequences),
            ]),
            ("LEVEL 5: SEMANTIC UNDERSTANDING", [
                ("operation_semantics", self.test_operation_semantics),
                ("format_awareness", self.test_format_awareness),
            ]),
            ("LEVEL 6: PERFORMANCE", [
                ("consistency", self.test_generation_consistency),
                ("speed", self.test_generation_speed),
            ]),
        ]

        for level_name, tests in test_groups:
            print(f"\n{'='*80}")
            print(level_name)
            print('='*80)

            for test_name, test_func in tests:
                try:
                    result = test_func()
                    self.results["tests"][test_name] = result
                except Exception as e:
                    print(f"ERROR in {test_name}: {e}")
                    self.results["tests"][test_name] = {"error": str(e)}

        return self.results

    def save_results(self, filepath: str):
        """Save results to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Results saved to {filepath}")

    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)

        total_tests = 0
        for test_name, result in self.results["tests"].items():
            if "count" in result:
                total_tests += result["count"]

        print(f"Total test cases: {total_tests}")
        print(f"Test groups: {len(self.results['tests'])}")

        # Check for errors
        errors = [name for name, result in self.results["tests"].items() if "error" in result]
        if errors:
            print(f"❌ Errors in: {', '.join(errors)}")
        else:
            print("✓ All test groups completed")


def main():
    """Main execution."""
    print("Loading model and tokenizer...")

    # Create tokenizer
    tokenizer = create_tokenizer()
    print(f"✓ Tokenizer: {tokenizer.vocab_size} tokens")

    # Determine device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"✓ Device: {device}")

    # Load best HLX Family model
    checkpoint_path = "checkpoints/hlx_family_final_epoch20.pt"
    print(f"Loading checkpoint: {checkpoint_path}")

    model = create_model(
        vocab_size=tokenizer.vocab_size,
        d_model=128,
        nhead=4,
        num_layers=2,
        dim_feedforward=512,
        dropout=0.1,
    )

    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    print(f"✓ Model loaded: {model.count_parameters():,} parameters")
    print()

    # Run comprehensive tests
    test_suite = HLXFamilyTestSuite(model, tokenizer, device)
    results = test_suite.run_all_tests()

    # Save results
    output_file = "comprehensive_hlx_test_results.json"
    test_suite.save_results(output_file)

    # Print summary
    test_suite.print_summary()

    print("\n" + "="*80)
    print("COMPREHENSIVE TESTING COMPLETE")
    print("="*80)
    print(f"Results: {output_file}")


if __name__ == "__main__":
    main()
