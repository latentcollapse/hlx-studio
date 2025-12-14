"""
HLX Deterministic Toolchain
Encoding, decoding, validation, and hashing utilities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_file
from hlx_runtime import (
    encode_lcb, decode_lcb, encode_lct,
    compute_hash, canonical_hash, verify_bijection,
    validate_contract, is_contract_wrapped,
    wrap_literal, unwrap_literal,
    E_LC_PARSE, E_VALIDATION_FAIL, E_INVALID_INPUT,
    LCEncodeError, LCDecodeError,
)
import base64
import io
import zipfile

app = Flask(__name__)


def encode_payload(payload, mode: str = 'LC-B') -> tuple:
    """Encode payload to LC-B or LC-T format."""
    try:
        if mode.upper() == 'LC-T':
            result = encode_lct(payload).encode('utf-8')
        else:
            result = encode_lcb(payload)
        return result, None
    except LCEncodeError as e:
        return None, str(e)


def decode_payload(data: bytes, mode: str = 'LC-B'):
    """Decode LC-B or LC-T data."""
    try:
        if mode.upper() == 'LC-T':
            raise NotImplementedError("LC-T decoding not yet implemented")
        return decode_lcb(data), None
    except LCDecodeError as e:
        return None, str(e)


def validate_payload(data: bytes) -> tuple:
    """
    Validate payload against HLX conformance rules.
    Returns (is_valid, message)
    """
    # 1. Check decodability
    try:
        decoded = decode_lcb(data)
    except LCDecodeError as e:
        return False, f"Decode failed: {e}"

    # 2. Verify bijection (encode->decode->encode produces same bytes)
    if not verify_bijection(decoded):
        return False, "Bijection check failed - encoding is non-deterministic"

    # 3. Contract validation if applicable
    if isinstance(decoded, dict) and is_contract_wrapped(decoded):
        valid, err = validate_contract(decoded)
        if not valid:
            return False, f"Contract validation failed: {err}"

    return True, "Payload conforms to HLX specification"


def generate_hash(data: bytes) -> str:
    """Generate authoritative BLAKE3/SHA256 hash."""
    return compute_hash(data)


def create_deterministic_zip(payload) -> bytes:
    """Create a deterministic ZIP archive with LC-B payload."""
    lcb_bytes = encode_lcb(payload)
    content_hash = compute_hash(lcb_bytes)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Fixed timestamp for determinism (Unix epoch)
        info = zipfile.ZipInfo('payload.lcb', date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, lcb_bytes)

        # Include manifest
        manifest = {
            "version": "1.0.1",
            "format": "LC-B",
            "hash_algorithm": "BLAKE3",
            "payload_hash": content_hash,
            "payload_size": len(lcb_bytes)
        }
        manifest_info = zipfile.ZipInfo('manifest.json', date_time=(1980, 1, 1, 0, 0, 0))
        import json
        zf.writestr(manifest_info, json.dumps(manifest, indent=2, sort_keys=True))

    return zip_buffer.getvalue()


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/hlx/tool/encode', methods=['POST'])
def handle_encode():
    """
    POST /hlx/tool/encode
    Body: JSON payload
    Query: ?mode=LC-B|LC-T|ZIP (default: LC-B)
    """
    payload = request.get_json()
    if not payload:
        return jsonify({"error": E_INVALID_INPUT}), 400

    mode = request.args.get('mode', 'LC-B').upper()

    if mode == 'ZIP':
        # Return deterministic ZIP file
        zip_bytes = create_deterministic_zip(payload)
        return send_file(
            io.BytesIO(zip_bytes),
            mimetype='application/zip',
            as_attachment=True,
            download_name='payload.hlx.zip'
        )

    encoded, error = encode_payload(payload, mode)
    if error:
        return jsonify({"error": E_LC_PARSE, "message": error}), 400

    content_hash = compute_hash(encoded)

    if mode == 'LC-T':
        return jsonify({
            "encoded_data": encoded.decode('utf-8'),
            "format": "LC-T",
            "hash": content_hash
        })
    else:
        return jsonify({
            "encoded_data": base64.b64encode(encoded).decode('ascii'),
            "format": "LC-B",
            "encoding": "base64",
            "hash": content_hash,
            "size_bytes": len(encoded)
        })


@app.route('/hlx/tool/decode', methods=['POST'])
def handle_decode():
    """
    POST /hlx/tool/decode
    Body: {encoded_data: base64} or raw for LC-T
    Query: ?mode=LC-B|LC-T
    """
    mode = request.args.get('mode', 'LC-B').upper()

    try:
        if mode == 'LC-B':
            data = request.get_json()
            if not data or 'encoded_data' not in data:
                return jsonify({"error": E_INVALID_INPUT}), 400
            encoded = base64.b64decode(data['encoded_data'])
        else:
            encoded = request.get_data()

        decoded, error = decode_payload(encoded, mode)
        if error:
            return jsonify({"error": E_LC_PARSE, "message": error}), 400

        return jsonify({"decoded_payload": decoded})

    except Exception as e:
        return jsonify({"error": E_LC_PARSE, "message": str(e)}), 400


@app.route('/hlx/tool/validate', methods=['POST'])
def handle_validate():
    """
    POST /hlx/tool/validate
    Body: {encoded_data: base64}
    """
    data = request.get_json()
    if not data or 'encoded_data' not in data:
        return jsonify({"error": E_INVALID_INPUT}), 400

    try:
        encoded = base64.b64decode(data['encoded_data'])
    except ValueError:
        return jsonify({"error": E_INVALID_INPUT, "message": "Invalid base64"}), 400

    is_valid, message = validate_payload(encoded)

    return jsonify({
        "status": "PASS" if is_valid else "FAIL",
        "message": message,
        "hash": compute_hash(encoded) if is_valid else None
    }), 200 if is_valid else 400


@app.route('/hlx/tool/hash', methods=['POST'])
def handle_hash():
    """
    POST /hlx/tool/hash
    Body: raw bytes or {data: base64}
    """
    content_type = request.content_type or ''

    if 'application/json' in content_type:
        data = request.get_json()
        if data and 'data' in data:
            raw = base64.b64decode(data['data'])
        elif data and 'payload' in data:
            # Hash the LC-B encoding of a JSON payload
            raw = encode_lcb(data['payload'])
        else:
            return jsonify({"error": E_INVALID_INPUT}), 400
    else:
        raw = request.get_data()

    if not raw:
        return jsonify({"error": E_INVALID_INPUT}), 400

    return jsonify({
        "hash_algorithm": "BLAKE3",
        "hash": generate_hash(raw),
        "input_size": len(raw)
    })


@app.route('/hlx/tool/wrap', methods=['POST'])
def handle_wrap():
    """POST /hlx/tool/wrap - wrap primitive in contract notation"""
    payload = request.get_json()
    if payload is None:
        return jsonify({"error": E_INVALID_INPUT}), 400

    wrapped = wrap_literal(payload.get('value', payload))
    return jsonify({"wrapped": wrapped})


@app.route('/hlx/tool/unwrap', methods=['POST'])
def handle_unwrap():
    """POST /hlx/tool/unwrap - unwrap contract notation"""
    payload = request.get_json()
    if not payload:
        return jsonify({"error": E_INVALID_INPUT}), 400

    unwrapped = unwrap_literal(payload)
    return jsonify({"unwrapped": unwrapped})


@app.route('/hlx/tool/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "hlx-toolchain",
        "version": "1.0.1"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
