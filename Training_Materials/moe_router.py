#!/usr/bin/env python3
"""
HLX MoE 4.5B Router
Qwen3-1.7B base coordinator + 2× Qwen2.5-1.5B specialists (ASCII + Runic)
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
from pathlib import Path
from typing import Optional, Dict, Any
import re


class HLXMoERouter:
    """Router for HLX Mixture of Experts architecture."""

    def __init__(
        self,
        coordinator_path: str,
        ascii_specialist_path: str,
        runic_specialist_path: str,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        """Initialize the MoE router with all three models."""
        self.device = device
        print("=" * 80)
        print("Initializing HLX MoE 4.5B Router")
        print("=" * 80)

        # 4-bit quantization config for memory efficiency
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )

        # Load coordinator
        print("\n[1/3] Loading Coordinator (Qwen3-1.7B) in 4-bit...")
        self.coordinator_tokenizer = AutoTokenizer.from_pretrained(
            coordinator_path,
            trust_remote_code=True
        )
        self.coordinator = AutoModelForCausalLM.from_pretrained(
            coordinator_path,
            quantization_config=bnb_config if device == "cuda" else None,
            device_map="auto" if device == "cuda" else None,
            trust_remote_code=True,
            torch_dtype=torch.float16 if device == "cpu" else None
        )
        if device == "cpu":
            self.coordinator = self.coordinator.to(device)
        self.coordinator.eval()
        print(f"✓ Coordinator loaded (Qwen3-1.7B base, ~1GB)")

        # Load ASCII specialist
        print("\n[2/3] Loading ASCII Specialist (Helix1B-ASCII) in 4-bit...")
        self.ascii_tokenizer = AutoTokenizer.from_pretrained(
            ascii_specialist_path,
            trust_remote_code=True
        )
        self.ascii_specialist = AutoModelForCausalLM.from_pretrained(
            ascii_specialist_path,
            quantization_config=bnb_config if device == "cuda" else None,
            device_map="auto" if device == "cuda" else None,
            trust_remote_code=True,
            torch_dtype=torch.float16 if device == "cpu" else None
        )
        if device == "cpu":
            self.ascii_specialist = self.ascii_specialist.to(device)
        self.ascii_specialist.eval()
        print(f"✓ ASCII Specialist loaded (~850MB)")

        # Load Runic specialist
        print("\n[3/3] Loading Runic Specialist (Helix1B-Runic) in 4-bit...")
        self.runic_tokenizer = AutoTokenizer.from_pretrained(
            runic_specialist_path,
            trust_remote_code=True
        )
        self.runic_specialist = AutoModelForCausalLM.from_pretrained(
            runic_specialist_path,
            quantization_config=bnb_config if device == "cuda" else None,
            device_map="auto" if device == "cuda" else None,
            trust_remote_code=True,
            torch_dtype=torch.float16 if device == "cpu" else None
        )
        if device == "cpu":
            self.runic_specialist = self.runic_specialist.to(device)
        self.runic_specialist.eval()
        print(f"✓ Runic Specialist loaded (~850MB)")

        print("\n" + "=" * 80)
        print("MoE Router initialized successfully!")
        print("=" * 80)

    def route_request(self, query: str) -> Dict[str, Any]:
        """
        Route a request through the MoE system.

        Args:
            query: User's HLX query

        Returns:
            Dictionary with 'specialist', 'response', 'reasoning'
        """
        # Step 1: Ask coordinator which specialist to use
        coordinator_prompt = f"### Instruction:\n{query}\n\n### Response:\n"

        with torch.no_grad():
            inputs = self.coordinator_tokenizer(
                coordinator_prompt,
                return_tensors="pt"
            ).to(self.coordinator.device)

            outputs = self.coordinator.generate(
                **inputs,
                max_new_tokens=200,
                do_sample=False,
                pad_token_id=self.coordinator_tokenizer.pad_token_id,
                eos_token_id=self.coordinator_tokenizer.eos_token_id
            )

            coordinator_response = self.coordinator_tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )

            # Extract response
            if "### Response:" in coordinator_response:
                coordinator_response = coordinator_response.split("### Response:")[-1].strip()
            else:
                coordinator_response = coordinator_response[len(coordinator_prompt):].strip()

        # Step 2: Determine which specialist (if any) from coordinator's response
        specialist_used = "coordinator"

        # Check if coordinator wants ASCII specialist
        if any(keyword in query.lower() for keyword in ["lc-t", "ascii", "text-safe", "{c:"]):
            specialist_used = "ascii"
            specialist_prompt = f"### Instruction:\n{query}\n\n### Response:\n"

            with torch.no_grad():
                inputs = self.ascii_tokenizer(
                    specialist_prompt,
                    return_tensors="pt"
                ).to(self.ascii_specialist.device)

                outputs = self.ascii_specialist.generate(
                    **inputs,
                    max_new_tokens=200,
                    do_sample=False,
                    pad_token_id=self.ascii_tokenizer.pad_token_id,
                    eos_token_id=self.ascii_tokenizer.eos_token_id
                )

                response = self.ascii_tokenizer.decode(
                    outputs[0],
                    skip_special_tokens=True
                )

                if "### Response:" in response:
                    response = response.split("### Response:")[-1].strip()
                else:
                    response = response[len(specialist_prompt):].strip()

        # Check if coordinator wants Runic specialist
        elif any(keyword in query.lower() for keyword in ["lc-r", "runic", "glyph", "🐊", "⟁", "⊤", "⊥", "∅"]):
            specialist_used = "runic"
            specialist_prompt = f"### Instruction:\n{query}\n\n### Response:\n"

            with torch.no_grad():
                inputs = self.runic_tokenizer(
                    specialist_prompt,
                    return_tensors="pt"
                ).to(self.runic_specialist.device)

                outputs = self.runic_specialist.generate(
                    **inputs,
                    max_new_tokens=200,
                    do_sample=False,
                    pad_token_id=self.runic_tokenizer.pad_token_id,
                    eos_token_id=self.runic_tokenizer.eos_token_id
                )

                response = self.runic_tokenizer.decode(
                    outputs[0],
                    skip_special_tokens=True
                )

                if "### Response:" in response:
                    response = response.split("### Response:")[-1].strip()
                else:
                    response = response[len(specialist_prompt):].strip()

        else:
            # Coordinator handles it
            response = coordinator_response

        return {
            "specialist": specialist_used,
            "response": response,
            "coordinator_reasoning": coordinator_response if specialist_used != "coordinator" else None
        }

    def query(self, text: str, verbose: bool = True) -> str:
        """
        Simple query interface.

        Args:
            text: Query text
            verbose: Print routing information

        Returns:
            Response text
        """
        result = self.route_request(text)

        if verbose:
            print(f"\n{'='*60}")
            print(f"Query: {text}")
            print(f"Routed to: {result['specialist']}")
            if result['coordinator_reasoning']:
                print(f"Coordinator reasoning: {result['coordinator_reasoning'][:100]}...")
            print(f"Response: {result['response']}")
            print(f"{'='*60}\n")

        return result['response']

    def interactive_mode(self):
        """Run interactive query loop."""
        print("\n" + "=" * 80)
        print("HLX MoE Interactive Mode")
        print("Type 'quit' or 'exit' to end session")
        print("=" * 80 + "\n")

        while True:
            try:
                query = input("Query> ").strip()

                if query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break

                if not query:
                    continue

                self.query(query, verbose=True)

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="HLX MoE 3.7B Router")
    parser.add_argument(
        "--coordinator",
        default="Qwen/Qwen3-1.7B",
        help="Path to coordinator model (using base Qwen3-1.7B, not fine-tuned)"
    )
    parser.add_argument(
        "--ascii",
        default="/home/matt/hlx-dev-studio/models/helix_ascii_specialist/final_model",
        help="Path to ASCII specialist model"
    )
    parser.add_argument(
        "--runic",
        default="/home/matt/hlx-dev-studio/models/helix_runic_specialist/final_model",
        help="Path to Runic specialist model"
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Single query to execute (non-interactive)"
    )
    parser.add_argument(
        "--device",
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="Device to use (cuda/cpu)"
    )

    args = parser.parse_args()

    # Initialize router
    router = HLXMoERouter(
        coordinator_path=args.coordinator,
        ascii_specialist_path=args.ascii,
        runic_specialist_path=args.runic,
        device=args.device
    )

    # Execute query or enter interactive mode
    if args.query:
        router.query(args.query, verbose=True)
    else:
        router.interactive_mode()


if __name__ == "__main__":
    main()
