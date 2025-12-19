#!/usr/bin/env python3
"""
Test Qwen2.5 1.5B model as a "bigger brain" for HLXL.
Compares performance and capabilities to the tiny HLXL Brain (491K params).
"""

import json
import subprocess
import time
from datetime import datetime, timezone
import sys

def get_ollama_model_info(model_name):
    """Get model specifications from Ollama."""
    try:
        result = subprocess.run(
            ["ollama", "show", model_name, "--modelfile"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            params = {}
            for line in lines:
                if 'parameter' in line.lower() or 'from' in line.lower():
                    params[line.split()[0]] = ' '.join(line.split()[1:])
            return params
        return {}
    except Exception as e:
        return {"error": str(e)}

def test_ollama_inference(model_name, prompt, temperature=0.0, max_tokens=50):
    """Test inference performance with Ollama model."""
    start_time = time.perf_counter()

    try:
        # Run ollama with JSON output for easier parsing
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
            # Count tokens (approximate - split on whitespace)
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
        return {
            "success": False,
            "error": "Inference timeout (60s)",
            "time_ms": 60000
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "time_ms": 0
        }

def run_test_suite():
    """Run comprehensive test suite on Qwen2.5 1.5B."""
    model_name = "qwen2.5:1.5b"

    print(f"=== Testing {model_name} as 'Bigger Brain' ===\n")

    # Test prompts (LC-R style and plain English)
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
        "benchmark_id": "qwen25_1.5b_bigger_brain_test",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": model_name,
        "model_info": get_ollama_model_info(model_name),
        "comparison_target": {
            "name": "HLXL Tiny Brain",
            "parameters": 491635,
            "size_mb": 1.88,
            "tokens_per_second": 700.4,
            "vocab_size": 115
        },
        "test_results": []
    }

    for test in test_prompts:
        print(f"Test: {test['name']}")
        print(f"Prompt: {test['prompt'][:60]}...")

        result = test_ollama_inference(
            model_name,
            test['prompt'],
            temperature=0.0,
            max_tokens=50
        )

        test_result = {
            "test_name": test['name'],
            "description": test['description'],
            "prompt": test['prompt'],
            **result
        }

        results["test_results"].append(test_result)

        if result['success']:
            print(f"✓ Tokens: {result['tokens_generated']}")
            print(f"✓ Time: {result['time_ms']}ms")
            print(f"✓ Speed: {result['tokens_per_second']} tok/s")
            print(f"  Output preview: {result['output'][:100]}...")
        else:
            print(f"✗ Failed: {result['error']}")

        print()

    # Calculate averages
    successful_tests = [t for t in results["test_results"] if t['success']]
    if successful_tests:
        avg_tokens = sum(t['tokens_generated'] for t in successful_tests) / len(successful_tests)
        avg_time_ms = sum(t['time_ms'] for t in successful_tests) / len(successful_tests)
        avg_speed = sum(t['tokens_per_second'] for t in successful_tests) / len(successful_tests)

        results["aggregated_performance"] = {
            "tests_run": len(test_prompts),
            "tests_successful": len(successful_tests),
            "avg_tokens_generated": round(avg_tokens, 2),
            "avg_time_ms": round(avg_time_ms, 2),
            "avg_tokens_per_second": round(avg_speed, 2)
        }

        # Comparison to tiny brain
        tiny_brain_speed = 700.4
        speedup_ratio = tiny_brain_speed / avg_speed if avg_speed > 0 else float('inf')

        results["comparison_analysis"] = {
            "tiny_brain_faster_by": f"{speedup_ratio:.2f}x",
            "qwen_param_advantage": f"{(1.5e9 / 491635):.0f}x more parameters",
            "note": "Tiny brain optimized for speed, Qwen optimized for capability"
        }

    # Save results
    output_file = f"benchmarks/qwen25_1.5b_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"=== Summary ===")
    if successful_tests:
        print(f"Successful tests: {len(successful_tests)}/{len(test_prompts)}")
        print(f"Average speed: {results['aggregated_performance']['avg_tokens_per_second']} tok/s")
        print(f"Average time: {results['aggregated_performance']['avg_time_ms']}ms")
        print(f"\nComparison:")
        print(f"  Tiny Brain: 700 tok/s (491K params, 1.88 MB)")
        print(f"  Qwen 1.5B: {results['aggregated_performance']['avg_tokens_per_second']} tok/s (~1.5B params, 986 MB)")
        print(f"  Speed ratio: {results['comparison_analysis']['tiny_brain_faster_by']}")

    print(f"\nResults saved to: {output_file}")

    return results

if __name__ == "__main__":
    try:
        results = run_test_suite()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
