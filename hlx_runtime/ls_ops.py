"""
HLX Latent Space Operations
Core operations for the Latent Space (LS) system.
"""

from typing import Any, Dict, Optional, Tuple
from .cas import CASStore, get_cas_store
from .lc_codec import encode_lcb, decode_lcb, encode_lct, compute_hash, canonical_hash
from .contracts import wrap_literal, unwrap_literal, validate_contract


class LSContext:
    def __init__(self, cas_store: CASStore = None):
        self.cas = cas_store or get_cas_store()
        self.handle_counter = 0

    def _generate_handle(self, prefix: str = "val") -> str:
        self.handle_counter += 1
        return f"&h_{prefix}_{self.handle_counter}"

    def collapse(self, value: Any) -> Tuple[str, str]:
        content_hash = self.cas.store(value)
        handle = self._generate_handle()
        self.cas.register_handle(handle, content_hash)
        return handle, content_hash

    def resolve(self, handle: str) -> Tuple[Optional[Any], Optional[str]]:
        return self.cas.get_by_handle(handle)

    def collapse_with_hash(self, value: Any) -> Dict:
        handle, content_hash = self.collapse(value)
        lcb_bytes = encode_lcb(value)
        return {
            'handle': handle,
            'content_hash': content_hash,
            'lc_b_size': len(lcb_bytes),
            'lc_t': encode_lct(value)
        }

    def verify(self, handle: str, expected_hash: str) -> bool:
        content_hash = self.cas.resolve_handle(handle)
        if content_hash is None:
            return False
        return content_hash == expected_hash


def ls_collapse(value: Any, ctx: LSContext = None) -> Dict:
    if ctx is None:
        ctx = LSContext()
    return ctx.collapse_with_hash(value)


def ls_resolve(handle: str, ctx: LSContext = None) -> Tuple[Optional[Any], Optional[str]]:
    if ctx is None:
        ctx = LSContext()
    return ctx.resolve(handle)


def ls_encode(value: Any, mode: str = 'LC-B') -> bytes:
    if mode.upper() == 'LC-T':
        return encode_lct(value).encode('utf-8')
    return encode_lcb(value)


def ls_decode(data: bytes, mode: str = 'LC-B') -> Any:
    if mode.upper() == 'LC-T':
        raise NotImplementedError("LC-T decoding not yet implemented")
    return decode_lcb(data)


def ls_hash(value: Any) -> str:
    return canonical_hash(value)


def ls_validate(value: Any, wrapped: bool = True) -> Tuple[bool, Optional[str]]:
    if wrapped:
        return validate_contract(value)
    try:
        encode_lcb(value)
        return True, None
    except Exception as e:
        return False, str(e)


def ls_wrap(value: Any) -> Dict:
    return wrap_literal(value)


def ls_unwrap(wrapped: Dict) -> Any:
    return unwrap_literal(wrapped)
