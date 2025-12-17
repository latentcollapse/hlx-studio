
// =============================================================================
// HLX RUNTIME TYPES
// =============================================================================

export type Handle = string;   // e.g., "&h_a1b2c3d4"
export type LCStream = string; // e.g., "🜊..."

// HLX-Lite Value Types (Recursive)
export type HLXLite =
  | null
  | boolean
  | number
  | string
  | Uint8Array // Bytes
  | HLXLite[]
  | { [key: string]: HLXLite }; // Object

export interface RuntimeState {
  handle_table: Map<string, HLXLite>;    // Hash -> Value
  handle_lookup: Map<Handle, string>;    // HandleID -> Hash
  hash_lookup: Map<string, Handle>;      // Hash -> HandleID (Idempotency)
  lc_cache: Map<string, LCStream>;       // Hash -> LCStream
}

export interface RuntimeSnapshot {
  handle_count: number;
  memory_usage_approx_bytes: number;
  handles: string[];
}
