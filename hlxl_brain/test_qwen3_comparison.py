#!/usr/bin/env python3
"""
Compare Qwen3 0.6B vs 1.7B as "bigger brains" for HLXL.
Tests both models against the same prompts to find the best balance of speed vs capability.
"""

import json
import subprocess
import time
from datetime import datetime, timezone
import sys

def test_ollama_inference(model_name, prompt, temperature=0.0):
    """Test inference performance with Ollama model."""
    start_time = time.perf_counter()

    try:
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            timeout=60
        )

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        if result.returncode == 0:
            output = result.stdout.strip()
            tokens_generated = len(output.split())
            tokens_per_second = (tokens_generated / elapsed_ms) * 1000 if elapsed_ms > 0 else 0

            return {
                "success": True,
                "output": output,
                "tokens_generated": tokens_generated,
                "time_ms": round(elapsed_ms, 2),
                "tokens_per_second": round(tokens_per_second, 2),
                "temperature": temperature
            }
        else:
            return {
                "success": False,
                "error": result.stderr,
                "time_ms": round(elapsed_ms, 2)
            }

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Timeout (60s)", "time_ms": 60000}
    except Exception as e:
        return {"success": False, "error": str(e), "time_ms": 0}

def run_comparison_suite():
    """Run comprehensive comparison between Qwen3 0.6B and 1.7B."""

    models = ["qwen3:0.6b", "qwen3:1.7b"]

    test_prompts = [
        {
            "name": "LC-R Simple",
            "prompt": "🜊🜁explain🜁model ⟁transformer🜂",
            "description": "LC-R formatted prompt"
        },
        {
            "name": "Plain English",
            "prompt": "Explain what a transformer model is in one sentence.",
            "description": "Standard English prompt"
        },
        {
            "name": "Code Generation",
            "prompt": "Write a Python function to calculate fibonacci numbers.",
            "description": "Code generation test"
        }
    ]

    results = {
        "benchmark_id": "qwen3_comparison_0.6b_vs_1.7b",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "baseline": {
            "name": "HLXL Tiny Brain",
            "parameters": 491635,
            "size_mb": 1.88,
            "tokens_per_second": 700.4
        },
        "models": {}
    }

    for model in models:
        print(f"\n{'='*60}")
        print(f"Testing {model}")
        print(f"{'='*60}\n")

        model_results = {
            "model": model,
            "test_results": []
        }

        for test in test_prompts:
            print(f"Test: {test['name']}")
            print(f"Prompt: {test['prompt'][:50]}...")

            result = test_ollama_inference(model, test['prompt'], temperature=0.0)

            test_result = {
                "test_name": test['name'],
                "description": test['description'],
                "prompt": test['prompt'],
                **result
            }

            model_results["test_results"].append(test_result)

            if result['success']:
                print(f"  ✓ Tokens: {result['tokens_generated']}")
                print(f"  ✓ Time: {result['time_ms']}ms")
                print(f"  ✓ Speed: {result['tokens_per_second']} tok/s")
            else:
                print(f"  ✗ Failed: {result['error']}")

            print()

        # Calculate averages for this model
        successful_tests = [t for t in model_results["test_results"] if t['success']]
        if successful_tests:
            avg_tokens = sum(t['tokens_generated'] for t in successful_tests) / len(successful_tests)
            avg_time_ms = sum(t['time_ms'] for t in successful_tests) / len(successful_tests)
            avg_speed = sum(t['tokens_per_second'] for t in successful_tests) / len(successful_tests)

            model_results["aggregated_performance"] = {
                "tests_run": len(test_prompts),
                "tests_successful": len(successful_tests),
                "avg_tokens_generated": round(avg_tokens, 2),
                "avg_time_ms": round(avg_time_ms, 2),
                "avg_tokens_per_second": round(avg_speed, 2)
            }

        results["models"][model] = model_results

    # Cross-model comparison
    print(f"\n{'='*60}")
    print("COMPARISON SUMMARY")
    print(f"{'='*60}\n")

    print(f"Baseline: HLXL Tiny Brain")
    print(f"  Speed: 700 tok/s")
    print(f"  Size: 1.88 MB (491K params)")
    print()

    for model in models:
        if model in results["models"] and "aggregated_performance" in results["models"][model]:
            perf = results["models"][model]["aggregated_performance"]
            print(f"{model}:")
            print(f"  Speed: {perf['avg_tokens_per_second']} tok/s")
            print(f"  Avg Time: {perf['avg_time_ms']}ms")
            print(f"  Success Rate: {perf['tests_successful']}/{perf['tests_run']}")

            # Speed comparison
            tiny_brain_speed = 700.4
            speedup_ratio = tiny_brain_speed / perf['avg_tokens_per_second'] if perf['avg_tokens_per_second'] > 0 else float('inf')
            print(f"  vs Tiny Brain: {speedup_ratio:.2f}x slower")
            print()

    # Determine winner
    if "qwen3:0.6b" in results["models"] and "qwen3:1.7b" in results["models"]:
        perf_06b = results["models"]["qwen3:0.6b"].get("aggregated_performance", {})
        perf_17b = results["models"]["qwen3:1.7b"].get("aggregated_performance", {})

        if perf_06b and perf_17b:
            speed_06b = perf_06b.get("avg_tokens_per_second", 0)
            speed_17b = perf_17b.get("avg_tokens_per_second", 0)

            results["winner_analysis"] = {
                "fastest": "qwen3:0.6b" if speed_06b > speed_17b else "qwen3:1.7b",
                "speed_difference": f"{abs(speed_06b - speed_17b):.2f} tok/s",
                "recommendation": "qwen3:0.6b is faster and more efficient" if speed_06b > speed_17b
                                 else "qwen3:1.7b has better capability despite slower speed",
                "note": "0.6B trades capability for speed, 1.7B trades speed for capability"
            }

            print("RECOMMENDATION:")
            print(f"  {results['winner_analysis']['recommendation']}")
            print(f"  Speed difference: {results['winner_analysis']['speed_difference']}")

    # Save results
    output_file = f"benchmarks/qwen3_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    return results

if __name__ == "__main__":
    try:
        results = run_comparison_suite()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
