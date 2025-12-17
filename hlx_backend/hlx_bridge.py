"""
HLX Runtime Bridge
Bridges FastAPI backend to existing HLX runtime (hlx_runtime module).
"""

import sys
from pathlib import Path

# Add parent directory to path to import hlx_runtime
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from hlx_runtime import ls_collapse as collapse, ls_resolve as resolve, canonical_hash
    from hlx_runtime import encode_lcb as encode, decode_lcb as decode
    from hlx_runtime.errors import HLXError
    from hlx_runtime.contracts import CONTRACT_IDS as CONTRACT_SCHEMAS
    HLX_AVAILABLE = True
except ImportError as e:
    print(f"Warning: HLX runtime not available: {e}")
    HLX_AVAILABLE = False
    # Stub implementations for development
    def collapse(value):
        return f"&h_stub_{hash(str(value))}"
    def resolve(handle):
        return {"error": "HLX runtime not available"}
    def canonical_hash(value):
        return f"stub_{hash(str(value))}"
    def encode(value):
        return b"stub"
    def decode(data):
        return None
    HLXError = Exception
    CONTRACT_SCHEMAS = {}


class HLXBridge:
    """
    Bridge to HLX runtime operations.
    Provides clean API for FastAPI routes.
    """

    def __init__(self):
        self.available = HLX_AVAILABLE
        if not self.available:
            print("[HLXBridge] Warning: Running in stub mode (hlx_runtime not available)")

    def collapse_value(self, value):
        """
        Collapse a value to a handle.

        Args:
            value: Any HLX-compatible value

        Returns:
            str: Content-addressed handle (e.g., "&h_abc123...")
        """
        try:
            return collapse(value)
        except Exception as e:
            raise HLXError(f"Collapse failed: {str(e)}")

    def resolve_handle(self, handle: str):
        """
        Resolve a handle to its value.

        Args:
            handle: Content-addressed handle

        Returns:
            The resolved value
        """
        try:
            return resolve(handle)
        except Exception as e:
            raise HLXError(f"Resolve failed: {str(e)}")

    def compute_hash(self, value):
        """
        Compute canonical hash of a value.

        Args:
            value: Any HLX-compatible value

        Returns:
            str: BLAKE3 hash (hex)
        """
        try:
            return canonical_hash(value)
        except Exception as e:
            raise HLXError(f"Hash computation failed: {str(e)}")

    def encode_to_lcb(self, value):
        """
        Encode value to LC-B binary format.

        Args:
            value: Any HLX-compatible value

        Returns:
            bytes: LC-B encoded data
        """
        try:
            return encode(value)
        except Exception as e:
            raise HLXError(f"LC-B encoding failed: {str(e)}")

    def decode_from_lcb(self, data: bytes):
        """
        Decode LC-B binary data to value.

        Args:
            data: LC-B encoded bytes

        Returns:
            Decoded value
        """
        try:
            return decode(data)
        except Exception as e:
            raise HLXError(f"LC-B decoding failed: {str(e)}")

    def get_contract_schema(self, contract_id: int):
        """
        Get schema for a contract ID.

        Args:
            contract_id: Integer contract ID

        Returns:
            dict: Contract schema
        """
        return CONTRACT_SCHEMAS.get(contract_id, None)

    def validate_contract(self, contract_data: dict):
        """
        Validate a contract structure.

        Args:
            contract_data: Contract dict in form {contract_id: {fields}}

        Returns:
            bool: True if valid
        """
        # Basic validation: check structure
        if not isinstance(contract_data, dict):
            return False
        if len(contract_data) != 1:
            return False

        contract_id = list(contract_data.keys())[0]
        if not isinstance(contract_id, int):
            return False

        # Check if contract exists in schemas
        if contract_id not in CONTRACT_SCHEMAS:
            return False

        return True


# Global bridge instance
hlx_bridge = HLXBridge()
