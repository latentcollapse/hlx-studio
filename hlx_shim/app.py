"""
HLX Shim Layer API
Translates between legacy systems and HLX-native encoding.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from hlx_runtime import (
    encode_lcb, decode_lcb, encode_lct,
    compute_hash, canonical_hash,
    E_LC_PARSE, E_CONTRACT_STRUCTURE, E_ENV_PAYLOAD_HASH_MISMATCH, E_INVALID_INPUT,
    validate_contract, wrap_literal, is_contract_wrapped,
    LCEncodeError, LCDecodeError,
)
import base64

app = Flask(__name__)


def shim_encode(payload: dict, mode: str = 'LC-B') -> bytes:
    """
    Encode a structured payload to LC-T or LC-B format.
    Uses proper HLX LC encoding (not JSON).
    """
    if mode.upper() == 'LC-T':
        return encode_lct(payload).encode('utf-8')
    else:
        return encode_lcb(payload)


def shim_decode(encoded_data: bytes, mode: str = 'LC-B') -> dict:
    """
    Decode LC-B or LC-T data back to structured payload.
    """
    if mode.upper() == 'LC-T':
        raise NotImplementedError("LC-T decoding not yet implemented")
    return decode_lcb(encoded_data)


def shim_validate(encoded_data: bytes, expected_hash: str = None) -> tuple:
    """
    Validate payload structure and integrity.
    Returns (is_valid, error_code, error_message)
    """
    # 1. Try to decode
    try:
        decoded = decode_lcb(encoded_data)
    except LCDecodeError as e:
        return False, E_LC_PARSE, str(e)

    # 2. Contract validation (if wrapped)
    if isinstance(decoded, dict) and is_contract_wrapped(decoded):
        valid, err = validate_contract(decoded)
        if not valid:
            return False, E_CONTRACT_STRUCTURE, err

    # 3. Hash validation (if provided)
    if expected_hash:
        actual_hash = compute_hash(encoded_data)
        if actual_hash != expected_hash:
            return False, E_ENV_PAYLOAD_HASH_MISMATCH, f"Expected {expected_hash}, got {actual_hash}"

    return True, None, None


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/hlx/shim/encode', methods=['POST'])
def handle_encode():
    """
    POST /hlx/shim/encode
    Body: JSON payload
    Query: ?mode=LC-B|LC-T (default: LC-B)
    Returns: base64-encoded LC-B or UTF-8 LC-T
    """
    payload = request.get_json()
    if not payload:
        return jsonify({"error": E_INVALID_INPUT, "message": "Invalid JSON input"}), 400

    mode = request.args.get('mode', 'LC-B').upper()

    try:
        encoded = shim_encode(payload, mode)
        content_hash = compute_hash(encoded)

        if mode == 'LC-B':
            return jsonify({
                "encoded_data": base64.b64encode(encoded).decode('ascii'),
                "encoding": "base64",
                "format": "LC-B",
                "hash": content_hash,
                "size_bytes": len(encoded)
            })
        else:
            return jsonify({
                "encoded_data": encoded.decode('utf-8'),
                "encoding": "utf-8",
                "format": "LC-T",
                "hash": content_hash
            })

    except LCEncodeError as e:
        return jsonify({"error": E_LC_PARSE, "message": str(e)}), 400


@app.route('/hlx/shim/decode', methods=['POST'])
def handle_decode():
    """
    POST /hlx/shim/decode
    Body: base64-encoded LC-B data (or raw for LC-T)
    Query: ?mode=LC-B|LC-T
    """
    mode = request.args.get('mode', 'LC-B').upper()

    try:
        if mode == 'LC-B':
            # Expect JSON with base64 data
            data = request.get_json()
            if not data or 'encoded_data' not in data:
                return jsonify({"error": E_INVALID_INPUT, "message": "Missing encoded_data field"}), 400
            encoded = base64.b64decode(data['encoded_data'])
        else:
            encoded = request.get_data()

        decoded = shim_decode(encoded, mode)
        return jsonify({"decoded_data": decoded})

    except (LCDecodeError, ValueError) as e:
        return jsonify({"error": E_LC_PARSE, "message": str(e)}), 400


@app.route('/hlx/shim/validate', methods=['POST'])
def handle_validate():
    """
    POST /hlx/shim/validate
    Body: JSON with {encoded_data: base64}
    Header: X-HLX-Hash (optional)
    """
    data = request.get_json()
    if not data or 'encoded_data' not in data:
        return jsonify({"error": E_INVALID_INPUT, "message": "Missing encoded_data field"}), 400

    try:
        encoded = base64.b64decode(data['encoded_data'])
    except ValueError:
        return jsonify({"error": E_INVALID_INPUT, "message": "Invalid base64"}), 400

    expected_hash = request.headers.get('X-HLX-Hash')
    is_valid, err_code, err_msg = shim_validate(encoded, expected_hash)

    if not is_valid:
        return jsonify({"status": "FAIL", "error": err_code, "message": err_msg}), 400

    return jsonify({
        "status": "PASS",
        "hash": compute_hash(encoded),
        "size_bytes": len(encoded)
    })


@app.route('/hlx/shim/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "hlx-shim", "version": "1.0.1"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
