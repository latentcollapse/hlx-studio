"""
HLX-Native State Server
Authoritative runtime for HLX state management with Merkle integrity.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from hlx_runtime import (
    encode_lcb, decode_lcb, encode_lct,
    compute_hash, canonical_hash,
    CASStore, get_cas_store,
    StateTable, MerkleTree,
    validate_contract, is_contract_wrapped,
    E_HANDLE_UNRESOLVED, E_INVALID_INPUT, E_ENV_PAYLOAD_HASH_MISMATCH,
    E_CAS_READ_FAIL, E_CAS_WRITE_FAIL,
    LCDecodeError,
)
import base64

app = Flask(__name__)

# Initialize CAS and State Table
CAS_ROOT = os.path.join(os.path.dirname(__file__), "cas")
cas_store = CASStore(CAS_ROOT)
state_table = StateTable()


def resolve_handle(handle: str):
    """Resolve a handle to its stored value."""
    if not handle.startswith('&h_'):
        return None, "E_INVALID_HANDLE_FORMAT"

    content_hash = cas_store.resolve_handle(handle)
    if not content_hash:
        return None, E_HANDLE_UNRESOLVED

    value = cas_store.retrieve(content_hash)
    if value is None:
        return None, E_CAS_READ_FAIL

    return {"value": value, "content_hash": content_hash}, None


def update_state(handle: str, value) -> tuple:
    """Store value and register handle."""
    if not handle.startswith('&h_'):
        return None, "E_INVALID_HANDLE_FORMAT"

    # Contract validation
    if isinstance(value, dict) and is_contract_wrapped(value):
        valid, err = validate_contract(value)
        if not valid:
            return None, f"E_CONTRACT_VIOLATION: {err}"

    try:
        content_hash = cas_store.store_with_handle(handle, value)
        state_table.set(handle, value)
        return content_hash, None
    except Exception as e:
        return None, f"{E_CAS_WRITE_FAIL}: {str(e)}"


def collapse_state(handle: str):
    """Get canonical LC-B representation of a handle's value."""
    content_hash = cas_store.resolve_handle(handle)
    if not content_hash:
        return None, E_HANDLE_UNRESOLVED

    value = cas_store.retrieve(content_hash)
    if value is None:
        return None, E_CAS_READ_FAIL

    lcb_bytes = encode_lcb(value)
    lct_str = encode_lct(value)

    return {
        "handle": handle,
        "content_hash": content_hash,
        "lc_b": base64.b64encode(lcb_bytes).decode('ascii'),
        "lc_t": lct_str,
        "size_bytes": len(lcb_bytes)
    }, None


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/hlx/state/query', methods=['GET'])
def handle_query():
    """GET /hlx/state/query?handle=&h_xxx"""
    handle = request.args.get('handle')
    if not handle:
        return jsonify({"error": E_INVALID_INPUT, "message": "Missing handle parameter"}), 400

    result, error = resolve_handle(handle)
    if error:
        return jsonify({"error": error, "handle": handle}), 404

    return jsonify({"handle": handle, **result})


@app.route('/hlx/state/update', methods=['POST'])
def handle_update():
    """
    POST /hlx/state/update
    Body: {handle: "&h_xxx", value: {...}}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": E_INVALID_INPUT}), 400

    handle = data.get('handle')
    value = data.get('value')

    if not handle or value is None:
        return jsonify({"error": E_INVALID_INPUT, "message": "Missing handle or value"}), 400

    content_hash, error = update_state(handle, value)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "status": "updated",
        "handle": handle,
        "content_hash": content_hash,
        "state_root": state_table.get_state_hash()
    }), 201


@app.route('/hlx/state/resolve', methods=['GET'])
def handle_resolve():
    """GET /hlx/state/resolve?handle=&h_xxx - same as query"""
    return handle_query()


@app.route('/hlx/state/collapse', methods=['GET'])
def handle_collapse():
    """GET /hlx/state/collapse?handle=&h_xxx - get canonical LC-B form"""
    handle = request.args.get('handle')
    if not handle:
        return jsonify({"error": E_INVALID_INPUT}), 400

    result, error = collapse_state(handle)
    if error:
        return jsonify({"error": error, "handle": handle}), 404

    return jsonify(result)


@app.route('/hlx/state/snapshot', methods=['GET'])
def handle_snapshot():
    """GET /hlx/state/snapshot - get full state snapshot"""
    snapshot = state_table.snapshot()
    return jsonify({
        "snapshot": snapshot,
        "integrity_valid": state_table.verify_integrity()
    })


@app.route('/hlx/state/merkle', methods=['GET'])
def handle_merkle():
    """GET /hlx/state/merkle - get Merkle tree info"""
    state_table.rebuild_merkle()
    return jsonify({
        "merkle_root": state_table.get_state_hash(),
        "entry_count": len(state_table.entries),
        "fanout": MerkleTree.FANOUT
    })


@app.route('/hlx/state/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "hlx-state-server",
        "version": "1.0.1",
        "entry_count": len(state_table.entries)
    })


if __name__ == '__main__':
    os.makedirs(CAS_ROOT, exist_ok=True)
    app.run(host='0.0.0.0', port=5002, debug=True)
