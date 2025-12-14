"""
HLX LC Codec - Latent Collapse Binary/Text Encoding
Deterministic 1:1 bijective encoding for HLX values.
"""

import struct
import hashlib
from typing import Any, Dict, List, Tuple, Union, Optional

LC_TAGS = {
    'NULL': 0x00, 'INT': 0x01, 'FLOAT': 0x02, 'TEXT': 0x03,
    'BYTES': 0x04, 'ARR_START': 0x05, 'ARR_END': 0x06,
    'OBJ_START': 0x07, 'OBJ_END': 0x08, 'HANDLE_REF': 0x09,
    'BOOL_TRUE': 0x0A, 'BOOL_FALSE': 0x0B,
}

TAG_NAMES = {v: k for k, v in LC_TAGS.items()}


class LCCodecError(Exception):
    pass

class LCEncodeError(LCCodecError):
    pass

class LCDecodeError(LCCodecError):
    pass


def encode_uleb128(value: int) -> bytes:
    if value < 0:
        raise LCEncodeError("ULEB128 cannot encode negative values")
    result = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value != 0:
            byte |= 0x80
        result.append(byte)
        if value == 0:
            break
    return bytes(result)


def decode_uleb128(data: bytes, offset: int = 0) -> Tuple[int, int]:
    result, shift, size = 0, 0, 0
    while offset + size < len(data):
        byte = data[offset + size]
        size += 1
        result |= (byte & 0x7F) << shift
        if (byte & 0x80) == 0:
            break
        shift += 7
    return result, size


def encode_sleb128(value: int) -> bytes:
    result = bytearray()
    more = True
    while more:
        byte = value & 0x7F
        value >>= 7
        if (value == 0 and (byte & 0x40) == 0) or (value == -1 and (byte & 0x40) != 0):
            more = False
        else:
            byte |= 0x80
        result.append(byte)
    return bytes(result)


def decode_sleb128(data: bytes, offset: int = 0) -> Tuple[int, int]:
    result, shift, size = 0, 0, 0
    while offset + size < len(data):
        byte = data[offset + size]
        size += 1
        result |= (byte & 0x7F) << shift
        shift += 7
        if (byte & 0x80) == 0:
            if shift < 64 and (byte & 0x40):
                result |= -(1 << shift)
            break
    return result, size


def encode_float64_be(value: float) -> bytes:
    return struct.pack('>d', value)


def decode_float64_be(data: bytes, offset: int = 0) -> Tuple[float, int]:
    return struct.unpack('>d', data[offset:offset + 8])[0], 8


class LCBinaryEncoder:
    def __init__(self):
        self.buffer = bytearray()

    def encode(self, value: Any) -> bytes:
        self.buffer = bytearray()
        self._encode_value(value)
        return bytes(self.buffer)

    def _encode_value(self, value: Any):
        if value is None:
            self.buffer.append(LC_TAGS['NULL'])
        elif isinstance(value, bool):
            self.buffer.append(LC_TAGS['BOOL_TRUE'] if value else LC_TAGS['BOOL_FALSE'])
        elif isinstance(value, int):
            self.buffer.append(LC_TAGS['INT'])
            self.buffer.extend(encode_sleb128(value))
        elif isinstance(value, float):
            self.buffer.append(LC_TAGS['FLOAT'])
            self.buffer.extend(encode_float64_be(value))
        elif isinstance(value, str):
            if value.startswith('&h_'):
                self.buffer.append(LC_TAGS['HANDLE_REF'])
            else:
                self.buffer.append(LC_TAGS['TEXT'])
            encoded = value.encode('utf-8')
            self.buffer.extend(encode_uleb128(len(encoded)))
            self.buffer.extend(encoded)
        elif isinstance(value, (bytes, bytearray)):
            self.buffer.append(LC_TAGS['BYTES'])
            self.buffer.extend(encode_uleb128(len(value)))
            self.buffer.extend(value)
        elif isinstance(value, list):
            self.buffer.append(LC_TAGS['ARR_START'])
            self.buffer.extend(encode_uleb128(len(value)))
            for item in value:
                self._encode_value(item)
            self.buffer.append(LC_TAGS['ARR_END'])
        elif isinstance(value, dict):
            self.buffer.append(LC_TAGS['OBJ_START'])
            sorted_keys = sorted(value.keys())
            self.buffer.extend(encode_uleb128(len(sorted_keys)))
            for key in sorted_keys:
                if not isinstance(key, str):
                    raise LCEncodeError(f"Keys must be strings, got {type(key)}")
                key_bytes = key.encode('utf-8')
                self.buffer.extend(encode_uleb128(len(key_bytes)))
                self.buffer.extend(key_bytes)
                self._encode_value(value[key])
            self.buffer.append(LC_TAGS['OBJ_END'])
        else:
            raise LCEncodeError(f"Cannot encode type: {type(value)}")


class LCBinaryDecoder:
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def decode(self) -> Any:
        return self._decode_value()

    def _read_byte(self) -> int:
        if self.offset >= len(self.data):
            raise LCDecodeError("Unexpected end of data")
        byte = self.data[self.offset]
        self.offset += 1
        return byte

    def _read_uleb128(self) -> int:
        value, size = decode_uleb128(self.data, self.offset)
        self.offset += size
        return value

    def _read_sleb128(self) -> int:
        value, size = decode_sleb128(self.data, self.offset)
        self.offset += size
        return value

    def _read_bytes(self, count: int) -> bytes:
        if self.offset + count > len(self.data):
            raise LCDecodeError("Unexpected end of data")
        result = self.data[self.offset:self.offset + count]
        self.offset += count
        return result

    def _decode_value(self) -> Any:
        tag = self._read_byte()

        if tag == LC_TAGS['NULL']:
            return None
        elif tag == LC_TAGS['BOOL_TRUE']:
            return True
        elif tag == LC_TAGS['BOOL_FALSE']:
            return False
        elif tag == LC_TAGS['INT']:
            return self._read_sleb128()
        elif tag == LC_TAGS['FLOAT']:
            value, _ = decode_float64_be(self.data, self.offset)
            self.offset += 8
            return value
        elif tag == LC_TAGS['TEXT']:
            length = self._read_uleb128()
            return self._read_bytes(length).decode('utf-8')
        elif tag == LC_TAGS['BYTES']:
            length = self._read_uleb128()
            return self._read_bytes(length)
        elif tag == LC_TAGS['HANDLE_REF']:
            length = self._read_uleb128()
            return self._read_bytes(length).decode('utf-8')
        elif tag == LC_TAGS['ARR_START']:
            count = self._read_uleb128()
            result = [self._decode_value() for _ in range(count)]
            if self._read_byte() != LC_TAGS['ARR_END']:
                raise LCDecodeError("Expected ARR_END")
            return result
        elif tag == LC_TAGS['OBJ_START']:
            count = self._read_uleb128()
            result = {}
            prev_key = None
            for _ in range(count):
                key_length = self._read_uleb128()
                key = self._read_bytes(key_length).decode('utf-8')
                if prev_key is not None and key <= prev_key:
                    raise LCDecodeError(f"Keys not sorted: {prev_key} >= {key}")
                prev_key = key
                result[key] = self._decode_value()
            if self._read_byte() != LC_TAGS['OBJ_END']:
                raise LCDecodeError("Expected OBJ_END")
            return result
        else:
            raise LCDecodeError(f"Unknown tag: 0x{tag:02x}")


RUNIC_GLYPHS = {
    'COLLAPSE': '\U0001F71A', 'INT': '\u16C7', 'FLOAT': '\u16DE',
    'TEXT': '\u16A6', 'BYTES': '\u16B2', 'ARRAY': '\u16C8',
    'OBJECT': '\u16DF', 'HANDLE': '\u16B9', 'NULL': '\u16C9',
    'TRUE': '\u16CF', 'FALSE': '\u16A0',
}


def encode_lct(value: Any) -> str:
    if value is None:
        return RUNIC_GLYPHS['NULL']
    elif isinstance(value, bool):
        return RUNIC_GLYPHS['TRUE'] if value else RUNIC_GLYPHS['FALSE']
    elif isinstance(value, int):
        return f"{RUNIC_GLYPHS['INT']}{value}"
    elif isinstance(value, float):
        return f"{RUNIC_GLYPHS['FLOAT']}{value}"
    elif isinstance(value, str):
        if value.startswith('&h_'):
            return f"{RUNIC_GLYPHS['HANDLE']}{value}"
        escaped = value.replace('\\', '\\\\').replace('"', '\\"')
        return f'{RUNIC_GLYPHS["TEXT"]}"{escaped}"'
    elif isinstance(value, (bytes, bytearray)):
        return f"{RUNIC_GLYPHS['BYTES']}[{value.hex()}]"
    elif isinstance(value, list):
        items = [encode_lct(item) for item in value]
        return f"{RUNIC_GLYPHS['ARRAY']}[{', '.join(items)}]"
    elif isinstance(value, dict):
        pairs = [f'"{k}":{encode_lct(value[k])}' for k in sorted(value.keys())]
        return f"{RUNIC_GLYPHS['OBJECT']}{{{', '.join(pairs)}}}"
    else:
        raise LCEncodeError(f"Cannot encode to LC-T: {type(value)}")


def encode_lcb(value: Any) -> bytes:
    return LCBinaryEncoder().encode(value)


def decode_lcb(data: bytes) -> Any:
    return LCBinaryDecoder(data).decode()


def compute_hash(data: bytes) -> str:
    try:
        import blake3
        return blake3.blake3(data).hexdigest()
    except ImportError:
        return hashlib.sha256(data).hexdigest()


def canonical_hash(value: Any) -> str:
    return compute_hash(encode_lcb(value))


def verify_bijection(value: Any) -> bool:
    encoded = encode_lcb(value)
    decoded = decode_lcb(encoded)
    return encode_lcb(decoded) == encoded


def wrap_contract(contract_id: int, value: Any) -> Dict:
    return {str(contract_id): {"@0": value}}


def unwrap_contract(wrapped: Dict) -> Tuple[int, Any]:
    if len(wrapped) != 1:
        raise LCDecodeError("Contract must have exactly one key")
    contract_id_str = list(wrapped.keys())[0]
    contract_id = int(contract_id_str)
    inner = wrapped[contract_id_str]
    if "@0" not in inner:
        raise LCDecodeError("Contract inner must have @0 field")
    return contract_id, inner["@0"]
