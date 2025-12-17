
import { HLXLite, Handle, LCStream, RuntimeState, RuntimeSnapshot } from './HLXRuntimeTypes';

// =============================================================================
// HLX RUNTIME v1.0.1 - DETERMINISTIC SPEC-COMPLIANT
// =============================================================================

// LC-B Binary Tags (per spec)
const LC_TAGS = {
  INT: 0x01,      // Signed LEB128
  FLOAT: 0x02,    // IEEE 754 Big-Endian Double
  TEXT: 0x03,     // LEB128 Len + UTF-8
  BYTES: 0x04,    // LEB128 Len + Raw
  ARR_START: 0x05,
  ARR_END: 0x06,
  OBJ_START: 0x07, // LEB128 ContractID
  OBJ_END: 0x08,
  HANDLE_REF: 0x09, // LEB128 Len + ASCII
  NULL: 0x00,
  BOOL_TRUE: 0x0A,
  BOOL_FALSE: 0x0B,
} as const;

// LC-T Text Markers
const LC_MARKERS = {
  OBJ_START: '🜊',
  FIELD: '🜁',
  OBJ_END: '🜂',
  ARR_START: '🜃',
  ARR_END: '🜄',
  HANDLE_REF: '🜇',
  STREAM_END: '🜋',
} as const;

// =============================================================================
// BLAKE3-COMPATIBLE DETERMINISTIC HASH (Pure JS Implementation)
// Uses a simplified but deterministic hash for browser compatibility
// Production should use actual BLAKE3 via WASM
// =============================================================================

class DeterministicHasher {
  private static readonly IV = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
  ];

  // BLAKE3-style compression (simplified for determinism)
  static hash(data: Uint8Array): Uint8Array {
    const state = [...this.IV];
    const blockSize = 64;

    // Pad data to block boundary
    const padded = new Uint8Array(Math.ceil((data.length + 9) / blockSize) * blockSize);
    padded.set(data);
    padded[data.length] = 0x80;
    const lenBits = BigInt(data.length) * 8n;
    const view = new DataView(padded.buffer);
    view.setBigUint64(padded.length - 8, lenBits, false);

    // Process blocks
    for (let i = 0; i < padded.length; i += blockSize) {
      const block = padded.slice(i, i + blockSize);
      this.compress(state, block);
    }

    // Output 32 bytes
    const result = new Uint8Array(32);
    const outView = new DataView(result.buffer);
    for (let i = 0; i < 8; i++) {
      outView.setUint32(i * 4, state[i], false);
    }
    return result;
  }

  private static compress(state: number[], block: Uint8Array): void {
    const view = new DataView(block.buffer, block.byteOffset);
    const w = new Array(16);
    for (let i = 0; i < 16; i++) {
      w[i] = view.getUint32(i * 4, false);
    }

    let [a, b, c, d, e, f, g, h] = state;

    for (let i = 0; i < 64; i++) {
      if (i >= 16) {
        const s0 = this.rotr(w[(i - 15) & 15], 7) ^ this.rotr(w[(i - 15) & 15], 18) ^ (w[(i - 15) & 15] >>> 3);
        const s1 = this.rotr(w[(i - 2) & 15], 17) ^ this.rotr(w[(i - 2) & 15], 19) ^ (w[(i - 2) & 15] >>> 10);
        w[i & 15] = (w[(i - 16) & 15] + s0 + w[(i - 7) & 15] + s1) >>> 0;
      }

      const S1 = this.rotr(e, 6) ^ this.rotr(e, 11) ^ this.rotr(e, 25);
      const ch = (e & f) ^ (~e & g);
      const temp1 = (h + S1 + ch + this.K[i] + w[i & 15]) >>> 0;
      const S0 = this.rotr(a, 2) ^ this.rotr(a, 13) ^ this.rotr(a, 22);
      const maj = (a & b) ^ (a & c) ^ (b & c);
      const temp2 = (S0 + maj) >>> 0;

      h = g; g = f; f = e;
      e = (d + temp1) >>> 0;
      d = c; c = b; b = a;
      a = (temp1 + temp2) >>> 0;
    }

    state[0] = (state[0] + a) >>> 0;
    state[1] = (state[1] + b) >>> 0;
    state[2] = (state[2] + c) >>> 0;
    state[3] = (state[3] + d) >>> 0;
    state[4] = (state[4] + e) >>> 0;
    state[5] = (state[5] + f) >>> 0;
    state[6] = (state[6] + g) >>> 0;
    state[7] = (state[7] + h) >>> 0;
  }

  private static rotr(x: number, n: number): number {
    return ((x >>> n) | (x << (32 - n))) >>> 0;
  }

  private static readonly K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
  ];

  static hashToHex(data: Uint8Array): string {
    const hash = this.hash(data);
    return Array.from(hash).map(b => b.toString(16).padStart(2, '0')).join('');
  }

  static hashString(str: string): string {
    const encoder = new TextEncoder();
    return this.hashToHex(encoder.encode(str));
  }
}

// =============================================================================
// LEB128 ENCODING (Spec-compliant)
// =============================================================================

function encodeLEB128(value: number): Uint8Array {
  const result: number[] = [];
  let v = value;
  do {
    let byte = v & 0x7f;
    v >>>= 7;
    if (v !== 0) byte |= 0x80;
    result.push(byte);
  } while (v !== 0);
  return new Uint8Array(result);
}

function encodeSignedLEB128(value: number): Uint8Array {
  const result: number[] = [];
  let more = true;
  while (more) {
    let byte = value & 0x7f;
    value >>= 7;
    if ((value === 0 && (byte & 0x40) === 0) || (value === -1 && (byte & 0x40) !== 0)) {
      more = false;
    } else {
      byte |= 0x80;
    }
    result.push(byte);
  }
  return new Uint8Array(result);
}

function decodeLEB128(bytes: Uint8Array, offset: number): { value: number; bytesRead: number } {
  let result = 0;
  let shift = 0;
  let bytesRead = 0;

  while (offset + bytesRead < bytes.length) {
    const byte = bytes[offset + bytesRead];
    result |= (byte & 0x7f) << shift;
    bytesRead++;
    if ((byte & 0x80) === 0) break;
    shift += 7;
    if (shift > 35) throw new Error('E_LC_BINARY_DECODE: Overlong LEB128');
  }

  return { value: result, bytesRead };
}

function decodeSignedLEB128(bytes: Uint8Array, offset: number): { value: number; bytesRead: number } {
  let result = 0;
  let shift = 0;
  let bytesRead = 0;
  let byte: number;

  do {
    if (offset + bytesRead >= bytes.length) throw new Error('E_LC_BINARY_DECODE: Truncated LEB128');
    byte = bytes[offset + bytesRead];
    result |= (byte & 0x7f) << shift;
    shift += 7;
    bytesRead++;
  } while ((byte & 0x80) !== 0);

  // Sign extend if negative
  if (shift < 32 && (byte & 0x40) !== 0) {
    result |= (~0 << shift);
  }

  return { value: result, bytesRead };
}

// =============================================================================
// IEEE 754 BIG-ENDIAN FLOAT ENCODING
// =============================================================================

function encodeFloat64BE(value: number): Uint8Array {
  const buffer = new ArrayBuffer(8);
  const view = new DataView(buffer);
  view.setFloat64(0, value, false); // false = big-endian
  return new Uint8Array(buffer);
}

function decodeFloat64BE(bytes: Uint8Array, offset: number): number {
  const view = new DataView(bytes.buffer, bytes.byteOffset + offset, 8);
  return view.getFloat64(0, false);
}

// =============================================================================
// HLX RUNTIME CLASS
// =============================================================================

export class HLXRuntime {
  private state: RuntimeState;
  private seenFieldIndices: Set<number> = new Set();

  constructor() {
    this.state = {
      handle_table: new Map(),
      handle_lookup: new Map(),
      hash_lookup: new Map(),
      lc_cache: new Map(),
    };
    this.boot();
  }

  private boot(): void {
    // Bootstrap: Register genesis empty table handle
    const emptyValue = {};
    const emptyHash = this.computeHash(emptyValue);
    const genesisHandle = '&h_empty_0';
    this.state.handle_table.set(emptyHash, emptyValue);
    this.state.handle_lookup.set(genesisHandle, emptyHash);
    this.state.hash_lookup.set(emptyHash, genesisHandle);
  }

  // --- CANONICAL JSON SERIALIZATION ---

  private canonicalize(value: HLXLite): string {
    return JSON.stringify(value, (key, val) => {
      if (val && typeof val === 'object' && !Array.isArray(val) && !(val instanceof Uint8Array)) {
        // Sort keys deterministically
        return Object.keys(val).sort().reduce((acc: Record<string, unknown>, k) => {
          acc[k] = val[k];
          return acc;
        }, {});
      }
      if (val instanceof Uint8Array) {
        // Encode bytes as lowercase hex (per spec)
        return { __bytes__: Array.from(val).map(b => b.toString(16).padStart(2, '0')).join('') };
      }
      return val;
    });
  }

  // --- DETERMINISTIC HASHING ---

  private computeHash(value: HLXLite): string {
    const canonical = this.canonicalize(value);
    return DeterministicHasher.hashString(canonical);
  }

  // --- PUBLIC API: COLLAPSE ---

  public collapse(value: HLXLite, hintTag: string = 'obj'): Handle {
    const hash = this.computeHash(value);

    // Idempotency: same value always returns same handle
    if (this.state.hash_lookup.has(hash)) {
      return this.state.hash_lookup.get(hash)!;
    }

    const handle = `&h_${hintTag}_${hash.substring(0, 8)}`;

    this.state.handle_table.set(hash, value);
    this.state.handle_lookup.set(handle, hash);
    this.state.hash_lookup.set(hash, handle);

    return handle;
  }

  // --- PUBLIC API: RESOLVE ---

  public resolve(handle: Handle): HLXLite {
    const hash = this.state.handle_lookup.get(handle);
    if (!hash) {
      throw new Error(`E_HANDLE_UNRESOLVED: Unknown Handle ${handle}`);
    }
    const val = this.state.handle_table.get(hash);
    if (val === undefined) {
      throw new Error(`E_HANDLE_INVALID: Integrity Failure. Handle ${handle} points to missing hash ${hash}`);
    }
    return val;
  }

  // --- LC-T TEXT ENCODING (Pedagogical) ---

  public encodeLC(value: HLXLite): LCStream {
    if (value === null) return `${LC_MARKERS.OBJ_START}0${LC_MARKERS.OBJ_END}`;

    if (typeof value === 'boolean') {
      return `${LC_MARKERS.OBJ_START}1${LC_MARKERS.FIELD}0${value}${LC_MARKERS.OBJ_END}`;
    }

    if (typeof value === 'number') {
      const cid = Number.isInteger(value) ? 2 : 3;
      return `${LC_MARKERS.OBJ_START}${cid}${LC_MARKERS.FIELD}0${value}${LC_MARKERS.OBJ_END}`;
    }

    if (typeof value === 'string') {
      return `${LC_MARKERS.OBJ_START}4${LC_MARKERS.FIELD}0"${value}"${LC_MARKERS.OBJ_END}`;
    }

    if (value instanceof Uint8Array) {
      const hex = Array.from(value).map(b => b.toString(16).padStart(2, '0')).join('');
      return `${LC_MARKERS.OBJ_START}5${LC_MARKERS.FIELD}0${hex}${LC_MARKERS.OBJ_END}`;
    }

    if (Array.isArray(value)) {
      let stream = LC_MARKERS.ARR_START;
      for (const item of value) {
        stream += this.encodeLC(item);
      }
      stream += LC_MARKERS.ARR_END;
      return stream;
    }

    if (typeof value === 'object') {
      const keys = Object.keys(value);
      let cid = 7;
      let fields = value;

      // Contract wrapper heuristic: { "14": { ... } }
      if (keys.length === 1 && /^\d+$/.test(keys[0])) {
        cid = parseInt(keys[0]);
        fields = value[keys[0]] as Record<string, HLXLite>;
      }

      let stream = `${LC_MARKERS.OBJ_START}${cid}`;

      // Sort field keys by index (strip @ prefix)
      const sortedKeys = Object.keys(fields).sort((a, b) => {
        const idxA = parseInt(a.replace('@', ''));
        const idxB = parseInt(b.replace('@', ''));
        return idxA - idxB;
      });

      for (const k of sortedKeys) {
        const idxStr = k.startsWith('@') ? k.substring(1) : k;
        const fieldValue = (fields as Record<string, HLXLite>)[k];
        stream += `${LC_MARKERS.FIELD}${idxStr}${this.encodeLC(fieldValue)}`;
      }
      stream += LC_MARKERS.OBJ_END;
      return stream;
    }

    return `${LC_MARKERS.OBJ_START}?${LC_MARKERS.OBJ_END}`;
  }

  // --- LC-B BINARY ENCODING (Canonical) ---

  public encodeLCBinary(value: HLXLite): Uint8Array {
    const chunks: Uint8Array[] = [];

    const encode = (v: HLXLite): void => {
      if (v === null) {
        chunks.push(new Uint8Array([LC_TAGS.NULL]));
        return;
      }

      if (typeof v === 'boolean') {
        chunks.push(new Uint8Array([v ? LC_TAGS.BOOL_TRUE : LC_TAGS.BOOL_FALSE]));
        return;
      }

      if (typeof v === 'number') {
        if (Number.isInteger(v)) {
          chunks.push(new Uint8Array([LC_TAGS.INT]));
          chunks.push(encodeSignedLEB128(v));
        } else {
          chunks.push(new Uint8Array([LC_TAGS.FLOAT]));
          chunks.push(encodeFloat64BE(v));
        }
        return;
      }

      if (typeof v === 'string') {
        const textBytes = new TextEncoder().encode(v);
        chunks.push(new Uint8Array([LC_TAGS.TEXT]));
        chunks.push(encodeLEB128(textBytes.length));
        chunks.push(textBytes);
        return;
      }

      if (v instanceof Uint8Array) {
        chunks.push(new Uint8Array([LC_TAGS.BYTES]));
        chunks.push(encodeLEB128(v.length));
        chunks.push(v);
        return;
      }

      if (Array.isArray(v)) {
        chunks.push(new Uint8Array([LC_TAGS.ARR_START]));
        for (const item of v) {
          encode(item);
        }
        chunks.push(new Uint8Array([LC_TAGS.ARR_END]));
        return;
      }

      if (typeof v === 'object') {
        const keys = Object.keys(v);
        let cid = 7;
        let fields = v;

        // Contract wrapper
        if (keys.length === 1 && /^\d+$/.test(keys[0])) {
          cid = parseInt(keys[0]);
          fields = v[keys[0]] as Record<string, HLXLite>;
        }

        chunks.push(new Uint8Array([LC_TAGS.OBJ_START]));
        chunks.push(encodeLEB128(cid));

        // Sort fields by index, detect duplicates
        const fieldEntries = Object.entries(fields).map(([k, fv]) => {
          const idx = parseInt(k.replace('@', ''));
          return { idx, value: fv };
        }).sort((a, b) => a.idx - b.idx);

        // Check for duplicate field indices
        const seenIndices = new Set<number>();
        for (const entry of fieldEntries) {
          if (seenIndices.has(entry.idx)) {
            throw new Error(`E_CONTRACT_STRUCTURE: Duplicate field index ${entry.idx}`);
          }
          seenIndices.add(entry.idx);
        }

        for (const entry of fieldEntries) {
          chunks.push(encodeLEB128(entry.idx));
          encode(entry.value as HLXLite);
        }

        chunks.push(new Uint8Array([LC_TAGS.OBJ_END]));
        return;
      }
    };

    encode(value);

    // Concatenate all chunks
    const totalLength = chunks.reduce((sum, chunk) => sum + chunk.length, 0);
    const result = new Uint8Array(totalLength);
    let offset = 0;
    for (const chunk of chunks) {
      result.set(chunk, offset);
      offset += chunk.length;
    }
    return result;
  }

  // --- LC-B BINARY DECODING ---

  public decodeLCBinary(bytes: Uint8Array): HLXLite {
    let pos = 0;

    const decode = (): HLXLite => {
      if (pos >= bytes.length) throw new Error('E_LC_BINARY_DECODE: Unexpected end of stream');

      const tag = bytes[pos++];

      switch (tag) {
        case LC_TAGS.NULL:
          return null;

        case LC_TAGS.BOOL_TRUE:
          return true;

        case LC_TAGS.BOOL_FALSE:
          return false;

        case LC_TAGS.INT: {
          const { value, bytesRead } = decodeSignedLEB128(bytes, pos);
          pos += bytesRead;
          return value;
        }

        case LC_TAGS.FLOAT: {
          if (pos + 8 > bytes.length) throw new Error('E_LC_BINARY_DECODE: Truncated float');
          const value = decodeFloat64BE(bytes, pos);
          pos += 8;
          return value;
        }

        case LC_TAGS.TEXT: {
          const { value: len, bytesRead } = decodeLEB128(bytes, pos);
          pos += bytesRead;
          if (pos + len > bytes.length) throw new Error('E_LC_BINARY_DECODE: Truncated text');
          const textBytes = bytes.slice(pos, pos + len);
          pos += len;
          return new TextDecoder().decode(textBytes);
        }

        case LC_TAGS.BYTES: {
          const { value: len, bytesRead } = decodeLEB128(bytes, pos);
          pos += bytesRead;
          if (pos + len > bytes.length) throw new Error('E_LC_BINARY_DECODE: Truncated bytes');
          const data = bytes.slice(pos, pos + len);
          pos += len;
          return data;
        }

        case LC_TAGS.ARR_START: {
          const items: HLXLite[] = [];
          while (pos < bytes.length && bytes[pos] !== LC_TAGS.ARR_END) {
            items.push(decode());
          }
          if (pos >= bytes.length) throw new Error('E_LC_BINARY_DECODE: Unclosed array');
          pos++; // consume ARR_END
          return items;
        }

        case LC_TAGS.OBJ_START: {
          const { value: cid, bytesRead } = decodeLEB128(bytes, pos);
          pos += bytesRead;

          const fields: Record<string, HLXLite> = {};
          const seenIndices = new Set<number>();
          let lastIdx = -1;

          while (pos < bytes.length && bytes[pos] !== LC_TAGS.OBJ_END) {
            const { value: fieldIdx, bytesRead: idxBytes } = decodeLEB128(bytes, pos);
            pos += idxBytes;

            // Check for duplicate field indices
            if (seenIndices.has(fieldIdx)) {
              throw new Error(`E_CONTRACT_STRUCTURE: Duplicate field index ${fieldIdx}`);
            }
            seenIndices.add(fieldIdx);

            // Check field ordering
            if (fieldIdx <= lastIdx) {
              throw new Error(`E_FIELD_ORDER: Field ${fieldIdx} out of order (after ${lastIdx})`);
            }
            lastIdx = fieldIdx;

            const fieldValue = decode();
            fields[`@${fieldIdx}`] = fieldValue;
          }

          if (pos >= bytes.length) throw new Error('E_LC_BINARY_DECODE: Unclosed object');
          pos++; // consume OBJ_END

          return { [cid.toString()]: fields };
        }

        case LC_TAGS.HANDLE_REF: {
          const { value: len, bytesRead } = decodeLEB128(bytes, pos);
          pos += bytesRead;
          if (pos + len > bytes.length) throw new Error('E_LC_BINARY_DECODE: Truncated handle');
          const handleBytes = bytes.slice(pos, pos + len);
          pos += len;
          const handleStr = new TextDecoder().decode(handleBytes);
          return { HANDLE_REF: handleStr };
        }

        default:
          throw new Error(`E_LC_BINARY_DECODE: Unknown tag 0x${tag.toString(16).padStart(2, '0')}`);
      }
    };

    const result = decode();

    // Check for trailing bytes
    if (pos < bytes.length) {
      throw new Error('E_LC_BINARY_DECODE: Trailing bytes after value');
    }

    return result;
  }

  // --- LC-T TEXT DECODING ---

  public decodeLC(stream: LCStream): HLXLite {
    let pos = 0;

    const consume = (char: string): void => {
      if (stream[pos] !== char) {
        throw new Error(`E_LC_PARSE: Expected '${char}' at ${pos}, got '${stream[pos] || 'EOF'}'`);
      }
      pos++;
    };

    const parseValue = (): HLXLite => {
      // Check for array
      if (stream[pos] === LC_MARKERS.ARR_START) {
        consume(LC_MARKERS.ARR_START);
        const items: HLXLite[] = [];
        while (pos < stream.length && stream[pos] !== LC_MARKERS.ARR_END) {
          items.push(parseValue());
        }
        consume(LC_MARKERS.ARR_END);
        return items;
      }

      consume(LC_MARKERS.OBJ_START);

      // Parse Contract ID
      let cidStr = '';
      while (pos < stream.length && /[0-9]/.test(stream[pos])) {
        cidStr += stream[pos++];
      }
      const cid = parseInt(cidStr);

      // Primitives
      if (cid === 0) {
        consume(LC_MARKERS.OBJ_END);
        return null;
      }

      if (cid === 1 || cid === 2 || cid === 3 || cid === 4) {
        consume(LC_MARKERS.FIELD);
        consume('0');
        let valStr = '';
        while (pos < stream.length && stream[pos] !== LC_MARKERS.OBJ_END) {
          valStr += stream[pos++];
        }
        consume(LC_MARKERS.OBJ_END);

        if (cid === 1) return valStr === 'true';
        if (cid === 2) return parseInt(valStr);
        if (cid === 3) return parseFloat(valStr);
        if (cid === 4) return valStr.replace(/^"|"$/g, '');
      }

      // Complex types
      const fields: Record<string, HLXLite> = {};
      const seenIndices = new Set<number>();

      while (pos < stream.length && stream[pos] === LC_MARKERS.FIELD) {
        consume(LC_MARKERS.FIELD);
        let fieldIdxStr = '';
        while (/[0-9]/.test(stream[pos])) {
          fieldIdxStr += stream[pos++];
        }
        const fieldIdx = parseInt(fieldIdxStr);

        // Check for duplicates
        if (seenIndices.has(fieldIdx)) {
          throw new Error(`E_CONTRACT_STRUCTURE: Duplicate field index ${fieldIdx}`);
        }
        seenIndices.add(fieldIdx);

        const val = parseValue();
        fields[`@${fieldIdx}`] = val;
      }
      consume(LC_MARKERS.OBJ_END);

      return { [cid.toString()]: fields };
    };

    return parseValue();
  }

  // --- STORE/EXPORT ---

  public storeLC(stream: LCStream): Handle {
    const val = this.decodeLC(stream);
    return this.collapse(val, 'stream');
  }

  public exportLC(handle: Handle): LCStream {
    try {
      const val = this.resolve(handle);
      return this.encodeLC(val);
    } catch {
      return `${LC_MARKERS.OBJ_START}ERR${LC_MARKERS.OBJ_END}`;
    }
  }

  // --- SNAPSHOT ---

  public snapshot(): RuntimeSnapshot {
    const handles = Array.from(this.state.handle_lookup.keys());
    let size = 0;
    this.state.handle_table.forEach(v => {
      size += this.canonicalize(v).length;
    });

    return {
      handle_count: handles.length,
      memory_usage_approx_bytes: size,
      handles
    };
  }

  // --- INVARIANT VERIFICATION ---

  public verifyBijection(value: HLXLite): boolean {
    const encoded = this.encodeLC(value);
    const decoded = this.decodeLC(encoded);
    const reencoded = this.encodeLC(decoded);
    return encoded === reencoded;
  }

  public verifyBinaryBijection(value: HLXLite): boolean {
    const encoded = this.encodeLCBinary(value);
    const decoded = this.decodeLCBinary(encoded);
    const reencoded = this.encodeLCBinary(decoded);
    return this.arraysEqual(encoded, reencoded);
  }

  private arraysEqual(a: Uint8Array, b: Uint8Array): boolean {
    if (a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) {
      if (a[i] !== b[i]) return false;
    }
    return true;
  }
}
