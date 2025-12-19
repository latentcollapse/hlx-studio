#!/usr/bin/env python3
"""
Helix 0.8B - Integrated Multi-Brain HLX System
================================================

Architecture:
- Qwen3_0.6b: Intent parsing and English understanding (via Ollama)
- Coordinator 100M: HLX format master, cross-format reasoning
- ASCII Specialist 50M: LC-T (text wire format) expert
- Runic Specialist 50M: LC-R (runic wire format) expert

Total Active Parameters: ~201M specialized + 600M intent parser = ~800M

Usage:
    from helix_0_8b import Helix08B

    helix = Helix08B()
    result = helix.english_to_hlx("Search for documents containing 'user'")
"""

import torch
import subprocess
import json
from typing import Dict, Optional, Tuple
from pathlib import Path

from train_qwen_distillation import (
    TransformerLanguageModel,
    CharTokenizer,
    MODEL_CONFIG_100M
)
from train_specialist_50m import MODEL_CONFIG_50M


class Helix08B:
    """
    Helix 0.8B: Multi-brain HLX translation system.

    Designed for local hardware with limited VRAM.
    Optimized for deterministic HLX operations.
    """

    def __init__(
        self,
        coordinator_checkpoint: str = "checkpoints/qwen_distill_FINAL_epoch100.pt",
        ascii_checkpoint: str = "checkpoints/specialist_ascii_BEST.pt",
        runic_checkpoint: Optional[str] = "checkpoints/specialist_runic_BEST.pt",
        device: str = "cuda",
        qwen_model: str = "qwen3:0.6b"
    ):
        """Initialize Helix 0.8B system."""
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.qwen_model = qwen_model

        print("="*80)
        print("HELIX 0.8B INITIALIZATION")
        print("="*80)
        print(f"Device: {self.device}")
        print(f"Intent Parser: {qwen_model} (via Ollama)")
        print()

        # Initialize tokenizer (shared across all models)
        self.tokenizer = CharTokenizer()

        # Load Coordinator 100M
        print("Loading Coordinator 100M...")
        self.coordinator = self._load_model(
            coordinator_checkpoint,
            MODEL_CONFIG_100M,
            "Coordinator"
        )

        # Load ASCII Specialist 50M
        print("Loading ASCII Specialist 50M...")
        self.ascii_specialist = self._load_model(
            ascii_checkpoint,
            MODEL_CONFIG_50M,
            "ASCII Specialist"
        )

        # Load Runic Specialist 50M (optional)
        if runic_checkpoint and Path(runic_checkpoint).exists():
            print("Loading Runic Specialist 50M...")
            self.runic_specialist = self._load_model(
                runic_checkpoint,
                MODEL_CONFIG_50M,
                "Runic Specialist"
            )
        else:
            print("⚠ Runic Specialist not available (checkpoint not found)")
            print("  Will fall back to Coordinator for LC-R format")
            self.runic_specialist = None

        # Verify Qwen availability
        print(f"\nVerifying {qwen_model} availability...")
        if not self._check_qwen_available():
            raise RuntimeError(
                f"{qwen_model} not available. Run: ollama pull {qwen_model}"
            )
        print(f"✓ {qwen_model} ready")

        print("\n" + "="*80)
        print("HELIX 0.8B READY")
        print("="*80)

        coordinator_params = sum(p.numel() for p in self.coordinator.parameters())/1e6
        ascii_params = sum(p.numel() for p in self.ascii_specialist.parameters())/1e6
        runic_params = sum(p.numel() for p in self.runic_specialist.parameters())/1e6 if self.runic_specialist else 0

        total_params = 600 + coordinator_params + ascii_params + runic_params

        print(f"Total Parameters: ~{total_params:.0f}M")
        print(f"  - Intent Parser (Qwen): ~600M")
        print(f"  - Coordinator: {coordinator_params:.1f}M")
        print(f"  - ASCII Specialist: {ascii_params:.1f}M")
        if self.runic_specialist:
            print(f"  - Runic Specialist: {runic_params:.1f}M")
        else:
            print(f"  - Runic Specialist: [NOT LOADED]")
        print("="*80)

    def _load_model(
        self,
        checkpoint_path: str,
        config: Dict,
        name: str
    ) -> TransformerLanguageModel:
        """Load a trained model from checkpoint."""
        model = TransformerLanguageModel(
            vocab_size=self.tokenizer.vocab_size,
            **config
        ).to(self.device)

        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        if 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)

        model.eval()
        param_count = sum(p.numel() for p in model.parameters())
        print(f"✓ {name} loaded ({param_count/1e6:.1f}M params)")

        return model

    def _check_qwen_available(self) -> bool:
        """Check if Qwen model is available in Ollama."""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return self.qwen_model in result.stdout
        except Exception:
            return False

    def _query_qwen(self, prompt: str) -> str:
        """Query Qwen model via Ollama."""
        try:
            result = subprocess.run(
                ['ollama', 'run', self.qwen_model, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {e}"

    def _generate(
        self,
        model: TransformerLanguageModel,
        prompt: str,
        max_length: int = 100,
        temperature: float = 0.7
    ) -> str:
        """Generate text from a model using autoregressive sampling."""
        tokens = self.tokenizer.encode(prompt)
        generated = tokens.copy()

        with torch.no_grad():
            for _ in range(max_length):
                if len(generated) >= 256:  # Max seq length
                    break

                # Get logits
                input_ids = torch.tensor([generated], dtype=torch.long, device=self.device)
                logits = model(input_ids)
                next_token_logits = logits[0, -1, :] / temperature

                # Sample
                probs = torch.softmax(next_token_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1).item()

                # Stop conditions
                if next_token == self.tokenizer.char_to_idx.get('\n', 0):
                    break
                if next_token == self.tokenizer.pad_token_id:
                    break

                generated.append(next_token)

        return self.tokenizer.decode(generated)

    def english_to_hlx(
        self,
        user_request: str,
        target_format: str = "auto",
        verbose: bool = True
    ) -> Dict:
        """
        Convert English request to HLX operation.

        Args:
            user_request: Natural language request
            target_format: "auto", "lc-t", "lc-r", "hlx", or "hlxl"
            verbose: Print intermediate steps

        Returns:
            {
                "intent": str,              # Parsed intent from Qwen
                "coordinator_output": str,  # HLX from coordinator
                "specialist_output": str,   # Final format from specialist
                "format": str,              # Detected/requested format
                "success": bool
            }
        """
        if verbose:
            print("\n" + "="*80)
            print("ENGLISH → HLX PIPELINE")
            print("="*80)
            print(f"Input: {user_request}")
            print()

        # Step 1: Parse intent with Qwen
        if verbose:
            print("[1/3] Parsing intent (Qwen3_0.6b)...")

        intent_prompt = f"""Analyze this request and extract the core HLX operation:

User request: "{user_request}"

Respond with ONLY the operation type and key parameters in this format:
OPERATION: <operation_type>
PARAMS: <key parameters>

Example:
User request: "Search for documents containing 'user'"
OPERATION: Search
PARAMS: target=documents, filter=contains('user')"""

        intent_response = self._query_qwen(intent_prompt)

        if verbose:
            print(f"Intent: {intent_response[:200]}...")
            print()

        # Step 2: Generate HLX with Coordinator
        if verbose:
            print("[2/3] Generating HLX (Coordinator 100M)...")

        coordinator_prompt = f"# {user_request}\n"
        coordinator_output = self._generate(
            self.coordinator,
            coordinator_prompt,
            max_length=150,
            temperature=0.7
        )

        # Remove prompt from output
        coordinator_hlx = coordinator_output[len(coordinator_prompt):].strip()

        if verbose:
            print(f"Coordinator: {coordinator_hlx[:200]}...")
            print()

        # Step 3: Determine format and route to specialist
        if target_format == "auto":
            # Detect format from coordinator output
            if any(c in coordinator_hlx for c in ['⊤', '⊥', '⟁', '🜀']):
                detected_format = "lc-r"
            elif coordinator_hlx.startswith("SEARCH") or coordinator_hlx.startswith("FILTER"):
                detected_format = "lc-t"
            else:
                detected_format = "hlx"
        else:
            detected_format = target_format

        if verbose:
            print(f"[3/3] Specializing to {detected_format.upper()}...")

        # Route to appropriate specialist
        if detected_format == "lc-t":
            specialist = self.ascii_specialist
            specialist_prompt = f"Convert to LC-T: {coordinator_hlx[:100]}"
        elif detected_format == "lc-r":
            if self.runic_specialist:
                specialist = self.runic_specialist
                specialist_prompt = f"Convert to LC-R: {coordinator_hlx[:100]}"
            else:
                # Fallback to coordinator if runic specialist not available
                if verbose:
                    print("⚠ Runic specialist not available, using coordinator fallback")
                specialist = None
                specialist_output = coordinator_hlx
        else:
            # No specialist needed for HLX/HLXL
            specialist = None
            specialist_output = coordinator_hlx

        if specialist:
            specialist_output = self._generate(
                specialist,
                specialist_prompt,
                max_length=100,
                temperature=0.6
            )
            specialist_output = specialist_output[len(specialist_prompt):].strip()

        if verbose:
            print(f"Specialist ({detected_format.upper()}): {specialist_output[:200]}")
            print("="*80)

        return {
            "intent": intent_response,
            "coordinator_output": coordinator_hlx,
            "specialist_output": specialist_output,
            "format": detected_format,
            "success": True
        }

    def batch_translate(
        self,
        requests: list[str],
        target_format: str = "auto"
    ) -> list[Dict]:
        """
        Batch translate multiple requests.

        Args:
            requests: List of English requests
            target_format: Target HLX format

        Returns:
            List of results (same format as english_to_hlx)
        """
        results = []
        for i, request in enumerate(requests, 1):
            print(f"\n[{i}/{len(requests)}] Processing: {request}")
            result = self.english_to_hlx(request, target_format, verbose=False)
            results.append(result)
        return results


def main():
    """Demo Helix 0.8B capabilities."""

    # Initialize system
    helix = Helix08B()

    # Test requests
    test_requests = [
        "Search for documents containing 'user'",
        "Filter active users from the database",
        "Represent true as a boolean",
        "Create an array with values [1, 2, 3]",
        "Execute a database query",
    ]

    print("\n" + "="*80)
    print("HELIX 0.8B DEMO")
    print("="*80)

    for i, request in enumerate(test_requests, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}/{len(test_requests)}")
        print(f"{'='*80}")

        result = helix.english_to_hlx(request, verbose=True)

        print(f"\nResult:")
        print(f"  Format: {result['format']}")
        print(f"  Success: {result['success']}")
        print(f"  Output: {result['specialist_output'][:100]}...")


if __name__ == "__main__":
    main()
