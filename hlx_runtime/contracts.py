"""
HLX Contract System
Defines and validates HLX contract structures.
"""

from typing import Any, Dict, List, Optional, Tuple


# Contract type IDs (canonical)
CONTRACT_IDS = {
    'INT_LITERAL': 14,
    'FLOAT_LITERAL': 15,
    'TEXT_LITERAL': 16,
    'BYTES_LITERAL': 17,
    'ARRAY': 18,
    'OBJECT': 19,
    'HANDLE_REF': 20,
    'NULL': 21,
    'BOOL': 22,
    'BLOCK': 100,
    'EXPR': 101,
    'VAR_REF': 102,
    'ASSIGNMENT': 103,
    'FUNCTION_DEF': 104,
    'FUNCTION_CALL': 105,
}

CONTRACT_NAMES = {v: k for k, v in CONTRACT_IDS.items()}

CONTRACT_SCHEMAS = {
    14: {'@0': 'int'},
    15: {'@0': 'float'},
    16: {'@0': 'str'},
    17: {'@0': 'bytes'},
    18: {'@0': 'list'},
    19: {'@0': 'dict'},
    20: {'@0': 'str'},
    21: {},
    22: {'@0': 'bool'},
}


def is_contract_wrapped(value: Any) -> bool:
    if not isinstance(value, dict) or len(value) != 1:
        return False
    key = list(value.keys())[0]
    try:
        int(key)
        return True
    except (ValueError, TypeError):
        return False


def get_contract_id(wrapped: Dict) -> Optional[int]:
    if not is_contract_wrapped(wrapped):
        return None
    return int(list(wrapped.keys())[0])


def get_contract_inner(wrapped: Dict) -> Optional[Dict]:
    if not is_contract_wrapped(wrapped):
        return None
    return wrapped[list(wrapped.keys())[0]]


def wrap_value(contract_id: int, inner: Dict) -> Dict:
    return {str(contract_id): inner}


def wrap_literal(value: Any) -> Dict:
    if value is None:
        return wrap_value(CONTRACT_IDS['NULL'], {})
    elif isinstance(value, bool):
        return wrap_value(CONTRACT_IDS['BOOL'], {'@0': value})
    elif isinstance(value, int):
        return wrap_value(CONTRACT_IDS['INT_LITERAL'], {'@0': value})
    elif isinstance(value, float):
        return wrap_value(CONTRACT_IDS['FLOAT_LITERAL'], {'@0': value})
    elif isinstance(value, str):
        if value.startswith('&h_'):
            return wrap_value(CONTRACT_IDS['HANDLE_REF'], {'@0': value})
        return wrap_value(CONTRACT_IDS['TEXT_LITERAL'], {'@0': value})
    elif isinstance(value, (bytes, bytearray)):
        return wrap_value(CONTRACT_IDS['BYTES_LITERAL'], {'@0': value})
    elif isinstance(value, list):
        return wrap_value(CONTRACT_IDS['ARRAY'], {'@0': [wrap_literal(v) for v in value]})
    elif isinstance(value, dict):
        if is_contract_wrapped(value):
            return value
        return wrap_value(CONTRACT_IDS['OBJECT'], {'@0': {k: wrap_literal(v) for k, v in value.items()}})
    else:
        raise ValueError(f"Cannot wrap type: {type(value)}")


def unwrap_literal(wrapped: Dict) -> Any:
    if not is_contract_wrapped(wrapped):
        return wrapped

    contract_id = get_contract_id(wrapped)
    inner = get_contract_inner(wrapped)

    if contract_id == CONTRACT_IDS['NULL']:
        return None
    elif contract_id == CONTRACT_IDS['BOOL']:
        return inner.get('@0', False)
    elif contract_id == CONTRACT_IDS['INT_LITERAL']:
        return inner.get('@0', 0)
    elif contract_id == CONTRACT_IDS['FLOAT_LITERAL']:
        return inner.get('@0', 0.0)
    elif contract_id == CONTRACT_IDS['TEXT_LITERAL']:
        return inner.get('@0', '')
    elif contract_id == CONTRACT_IDS['BYTES_LITERAL']:
        return inner.get('@0', b'')
    elif contract_id == CONTRACT_IDS['HANDLE_REF']:
        return inner.get('@0', '')
    elif contract_id == CONTRACT_IDS['ARRAY']:
        return [unwrap_literal(item) for item in inner.get('@0', [])]
    elif contract_id == CONTRACT_IDS['OBJECT']:
        return {k: unwrap_literal(v) for k, v in inner.get('@0', {}).items()}
    else:
        return wrapped


def validate_contract(wrapped: Dict) -> Tuple[bool, Optional[str]]:
    if not is_contract_wrapped(wrapped):
        return False, "Value is not contract-wrapped"

    contract_id = get_contract_id(wrapped)
    inner = get_contract_inner(wrapped)

    if contract_id not in CONTRACT_SCHEMAS:
        return True, None

    schema = CONTRACT_SCHEMAS[contract_id]
    for field, expected_type in schema.items():
        if field not in inner:
            return False, f"Missing field '{field}' for contract {contract_id}"

    return True, None
