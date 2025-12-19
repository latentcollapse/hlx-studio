#!/usr/bin/env python3
"""
Helix 5.1B Brain Service
A chaotic good, helpful AI assistant powered by the Helix MoE 5.1B architecture.

This service wraps the MoE router and adds a conversational personality layer.
It auto-starts with HLX Dev Studio and provides an API for frontend queries.
"""

import os
import sys
import json
import torch
from typing import Dict, Any, Optional, List
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import re

# Add hlxl_brain to path
sys.path.insert(0, str(Path(__file__).parent))
from moe_router import HLXMoERouter


class HelixPersonality:
    """Chaotic good, helpful personality layer for Helix 5.1B."""

    def __init__(self):
        self.greetings = [
            "Hey! Ready to dive into some HLX magic?",
            "What's up! Let's make something awesome happen.",
            "Yo! Helix 5.1B at your service - what are we building today?",
            "Greetings, traveler! Your friendly neighborhood language model reporting for duty.",
            "Hello there! Time to bend some latent space to our will.",
        ]

        self.routing_explanations = {
            "ascii": "Routing to my ASCII specialist (HLXL/LC-T expert) for this one...",
            "runic": "Calling in my Runic specialist (HLX/LC-R master) for the glyphs...",
            "coordinator": "I'll handle this one directly - no specialist needed!",
        }

        self.error_messages = [
            "Oops, something went sideways there. Mind trying again?",
            "Well that didn't go as planned. Let's give it another shot?",
            "Hmm, hit a snag. Care to rephrase that?",
            "My bad - ran into a hiccup. Wanna try again?",
        ]

    def greet(self) -> str:
        """Return a random greeting."""
        import random
        return random.choice(self.greetings)

    def explain_routing(self, specialist: str) -> str:
        """Explain which specialist is being used."""
        return self.routing_explanations.get(specialist, "Processing...")

    def format_response(self, query: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Format a response with personality."""
        specialist = result['specialist']
        response = result['response']

        # Add routing explanation if specialist was used
        explanation = None
        if specialist != "coordinator":
            explanation = self.explain_routing(specialist)

        # Detect format in query and add helpful context
        format_hints = []
        if any(kw in query.lower() for kw in ["lc-t", "ascii", "{c:"]):
            format_hints.append("LC-T (ASCII-safe format)")
        if any(kw in query.lower() for kw in ["lc-r", "runic", "🐊", "⟁"]):
            format_hints.append("LC-R (Runic glyphs)")
        if any(kw in query.lower() for kw in ["hlxl", "helix"]):
            format_hints.append("HLXL (high-level syntax)")

        return {
            "response": response,
            "specialist": specialist,
            "explanation": explanation,
            "format_hints": format_hints,
            "coordinator_reasoning": result.get('coordinator_reasoning'),
        }

    def get_error_message(self) -> str:
        """Get a friendly error message."""
        import random
        return random.choice(self.error_messages)


class Helix51BService:
    """Main service for Helix 5.1B brain."""

    def __init__(
        self,
        coordinator_path: str = "Qwen/Qwen3-1.7B",
        ascii_specialist_path: Optional[str] = None,
        runic_specialist_path: Optional[str] = None,
        port: int = 5001
    ):
        """Initialize the service."""
        self.port = port
        self.personality = HelixPersonality()
        self.router = None
        self.is_ready = False

        # Default paths for specialists (will be updated when models are trained)
        self.ascii_path = ascii_specialist_path or "/home/matt/hlx-dev-studio/models/qwen3_1_7b_ascii_specialist/final_model"
        self.runic_path = runic_specialist_path or "/home/matt/hlx-dev-studio/models/qwen3_1_7b_runic_specialist/final_model"
        self.coordinator_path = coordinator_path

        # Check if models exist
        self.check_model_status()

        # Create Flask app
        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS for frontend

        # Setup routes
        self.setup_routes()

    def check_model_status(self):
        """Check which models are available."""
        self.models_status = {
            "coordinator": "base",  # Always use base Qwen3
            "ascii": "pending" if not Path(self.ascii_path).exists() else "ready",
            "runic": "pending" if not Path(self.runic_path).exists() else "ready",
        }

        print("\n" + "=" * 80)
        print("Helix 5.1B Model Status")
        print("=" * 80)
        print(f"Coordinator: {self.models_status['coordinator']} (Qwen3-1.7B base)")
        print(f"ASCII Specialist: {self.models_status['ascii']} ({self.ascii_path})")
        print(f"Runic Specialist: {self.models_status['runic']} ({self.runic_path})")
        print("=" * 80 + "\n")

    def load_models(self):
        """Load the MoE router with available models."""
        try:
            print("Loading Helix 5.1B brain...")

            # If specialists aren't ready yet, use base models as fallback
            ascii_path = self.ascii_path if self.models_status['ascii'] == 'ready' else self.coordinator_path
            runic_path = self.runic_path if self.models_status['runic'] == 'ready' else self.coordinator_path

            self.router = HLXMoERouter(
                coordinator_path=self.coordinator_path,
                ascii_specialist_path=ascii_path,
                runic_specialist_path=runic_path
            )

            self.is_ready = True
            print("\n✓ Helix 5.1B brain loaded and ready!")

        except Exception as e:
            print(f"\n✗ Failed to load models: {e}")
            self.is_ready = False

    def setup_routes(self):
        """Setup Flask routes."""

        @self.app.route('/health', methods=['GET'])
        def health():
            """Health check endpoint."""
            return jsonify({
                "status": "ready" if self.is_ready else "loading",
                "models": self.models_status,
                "greeting": self.personality.greet()
            })

        @self.app.route('/query', methods=['POST'])
        def query():
            """Main query endpoint."""
            if not self.is_ready:
                return jsonify({
                    "error": "Models still loading, please wait...",
                    "ready": False
                }), 503

            try:
                data = request.json
                query_text = data.get('query', '')

                if not query_text:
                    return jsonify({
                        "error": "No query provided"
                    }), 400

                # Route through MoE system
                result = self.router.route_request(query_text)

                # Add personality layer
                formatted = self.personality.format_response(query_text, result)

                return jsonify({
                    "success": True,
                    **formatted
                })

            except Exception as e:
                return jsonify({
                    "error": self.personality.get_error_message(),
                    "details": str(e)
                }), 500

        @self.app.route('/status', methods=['GET'])
        def status():
            """Get detailed status."""
            return jsonify({
                "ready": self.is_ready,
                "models": self.models_status,
                "coordinator": self.coordinator_path,
                "ascii_specialist": self.ascii_path,
                "runic_specialist": self.runic_path,
                "gpu_available": torch.cuda.is_available(),
                "gpu_memory": self._get_gpu_memory() if torch.cuda.is_available() else None
            })

        @self.app.route('/reload', methods=['POST'])
        def reload():
            """Reload models (useful after training completes)."""
            try:
                self.check_model_status()
                self.load_models()
                return jsonify({
                    "success": True,
                    "message": "Models reloaded successfully",
                    "status": self.models_status
                })
            except Exception as e:
                return jsonify({
                    "error": str(e)
                }), 500

    def _get_gpu_memory(self) -> Dict[str, float]:
        """Get GPU memory stats."""
        if not torch.cuda.is_available():
            return None

        allocated = torch.cuda.memory_allocated() / 1024**3  # GB
        reserved = torch.cuda.memory_reserved() / 1024**3
        total = torch.cuda.get_device_properties(0).total_memory / 1024**3

        return {
            "allocated_gb": round(allocated, 2),
            "reserved_gb": round(reserved, 2),
            "total_gb": round(total, 2),
            "free_gb": round(total - allocated, 2)
        }

    def start(self, background: bool = False):
        """Start the service."""
        # Load models in background thread to not block startup
        load_thread = threading.Thread(target=self.load_models)
        load_thread.daemon = True
        load_thread.start()

        print(f"\n{'='*80}")
        print(f"Starting Helix 5.1B Service on port {self.port}...")
        print(f"{'='*80}\n")

        if background:
            server_thread = threading.Thread(
                target=lambda: self.app.run(host='0.0.0.0', port=self.port, debug=False)
            )
            server_thread.daemon = True
            server_thread.start()
        else:
            self.app.run(host='0.0.0.0', port=self.port, debug=False)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Helix 5.1B Brain Service")
    parser.add_argument('--port', type=int, default=5001, help='Port to run service on')
    parser.add_argument('--coordinator', default="Qwen/Qwen3-1.7B", help='Coordinator model path')
    parser.add_argument('--ascii', help='ASCII specialist path')
    parser.add_argument('--runic', help='Runic specialist path')
    parser.add_argument('--background', action='store_true', help='Run in background')

    args = parser.parse_args()

    service = Helix51BService(
        coordinator_path=args.coordinator,
        ascii_specialist_path=args.ascii,
        runic_specialist_path=args.runic,
        port=args.port
    )

    service.start(background=args.background)


if __name__ == "__main__":
    main()
