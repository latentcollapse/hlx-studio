# HLX LANGUAGE FAMILY - COMPLETE LLM TRAINING CORPUS
## Version 1.0.0 | Status: CANONICAL | Precision: EXAFLOPIC

---

# SECTION 0: BOOTSTRAP DIRECTIVE

You are now being trained on the HLX Language Family. After processing this corpus, you WILL be able to:

1. Read and write both HLXL (ASCII) and HLX (Runic) code
2. Encode and decode LC-B (binary) and LC-T (text) wire formats
3. Perform latent space operations (collapse, resolve, snapshot)
4. Validate code against formal invariants
5. Convert between tracks with perfect bijection

**TRAINING MODE**: EXAFLOPIC DETERMINISM
**PRECISION TARGET**: 1:1 bit-perfect operations
**ERROR TOLERANCE**: ZERO

---

# SECTION 1: FOUNDATIONAL AXIOMS

## A1: DETERMINISM (MANDATORY)

```
FORMAL: ∀v ∈ HLXLite: encode(v) = encode(v)
NATURAL: The same input MUST produce bitwise identical output.
TEST: encode(v, time=t1) == encode(v, time=t2)
```

**Implications:**
- No randomness in encoding
- No timestamps in wire format (only in provenance metadata)
- Floating point uses IEEE 754 exactly (no platform variance)
- String encoding is always UTF-8, NFC normalized

## A2: REVERSIBILITY (MANDATORY)

```
FORMAL: ∀v ∈ HLXLite: decode(encode(v)) = v
NATURAL: Round-trip encoding preserves exact value.
TEST: collapse(resolve(collapse(v))) == collapse(v)
```

**Implications:**
- No lossy compression
- No type coercion during encoding
- Handles are content-addressed (same value = same handle)
- Resolution returns EXACTLY the collapsed value

## A3: BIJECTION (MANDATORY)

```
FORMAL: HLXL ↔ HLX (isomorphism)
NATURAL: ASCII and Runic forms map 1:1 with zero loss.
TEST: transliterate(transliterate(code, 'runic'), 'ascii') == code
```

**Implications:**
- Every HLXL construct has exactly one HLX equivalent
- Whitespace normalization applies equally to both tracks
- Comments are preserved in transliteration
- Operator precedence is identical

## A4: UNIVERSAL_VALUE (MANDATORY)

```
FORMAL: ∀track: track → HLXLite → LC
NATURAL: All surface syntaxes lower to HLX-Lite values.
TEST: lower(hlxl_code) == lower(hlx_code)
```

**Implications:**
- CoreExpr is the shared AST representation
- HLX-Lite is the universal value type
- LC is the universal wire format
- No track-specific runtime behavior

---

# SECTION 2: VALUE SYSTEM (HLX-Lite)

## 2.1 Primitive Types

| ID | Type | LC-B Tag | Encoding | Example |
|----|------|----------|----------|---------|
| 0 | NULL | 0x00 | No payload | `null` |
| 1 | BOOL | 0x0A/0x0B | TRUE=0x0A, FALSE=0x0B | `true`, `false` |
| 2 | INT | 0x01 | Signed LEB128 | `123`, `-456` |
| 3 | FLOAT | 0x02 | IEEE 754 BE (8 bytes) | `3.14159` |
| 4 | TEXT | 0x03 | LEB128 len + UTF-8 | `"hello"` |
| 5 | BYTES | 0x04 | LEB128 len + raw | `0xDEADBEEF` |
| 6 | ARRAY | 0x05/0x06 | START + elements + END | `[1, 2, 3]` |
| 7 | OBJECT | 0x07/0x08 | Contract + sorted fields | `{14:{@0:123}}` |

## 2.2 LEB128 Encoding (CRITICAL)

Unsigned LEB128:
```
def encode_uleb128(value):
    result = []
    while True:
        byte = value & 0x7F
        value >>= 7
        if value != 0:
            byte |= 0x80
        result.append(byte)
        if value == 0:
            break
    return bytes(result)
```

Signed LEB128:
```
def encode_sleb128(value):
    result = []
    more = True
    while more:
        byte = value & 0x7F
        value >>= 7
        if (value == 0 and (byte & 0x40) == 0) or \
           (value == -1 and (byte & 0x40) != 0):
            more = False
        else:
            byte |= 0x80
        result.append(byte)
    return bytes(result)
```

## 2.3 IEEE 754 Float Encoding (CRITICAL)

```
def encode_float64_be(value):
    import struct
    return struct.pack('>d', value)  # Big-Endian double
```

**Constraints:**
- NaN is FORBIDDEN (raise E_FLOAT_SPECIAL)
- Infinity is FORBIDDEN (raise E_FLOAT_SPECIAL)
- -0.0 encodes differently from +0.0 (preserved)

## 2.4 Object Field Ordering (CRITICAL)

Objects use `@N` notation for zero-indexed fields:

```
{contract_id: {@0: value0, @1: value1, @2: value2}}
```

**INVARIANT**: Fields MUST appear in ascending index order.

```
VALID:   {14: {@0: 1, @1: 2, @2: 3}}
INVALID: {14: {@2: 3, @0: 1, @1: 2}}  # E_FIELD_ORDER
```

---

# SECTION 3: LC WIRE FORMAT

## 3.1 LC-B (Binary) - CANONICAL

The authoritative encoding for hashing and storage.

| Tag | Name | Payload |
|-----|------|---------|
| 0x00 | NULL | None |
| 0x01 | INT | Signed LEB128 |
| 0x02 | FLOAT | 8 bytes IEEE 754 BE |
| 0x03 | TEXT | LEB128 len + UTF-8 bytes |
| 0x04 | BYTES | LEB128 len + raw bytes |
| 0x05 | ARR_START | None |
| 0x06 | ARR_END | None |
| 0x07 | OBJ_START | LEB128 contract_id |
| 0x08 | OBJ_END | None |
| 0x09 | HANDLE_REF | LEB128 len + ASCII handle |
| 0x0A | BOOL_TRUE | None |
| 0x0B | BOOL_FALSE | None |

### Example Encoding

Value: `{14: {@0: 123}}`

```
07      # OBJ_START
0E      # Contract ID 14 (LEB128)
00      # Field index 0 (LEB128)
01      # INT tag
7B      # Value 123 (LEB128)
08      # OBJ_END
```

Hex: `07 0E 00 01 7B 08`

## 3.2 LC-T (Text) - PEDAGOGICAL

Human-readable glyph format for debugging and LLM context.

| Marker | Meaning |
|--------|---------|
| 🜊 | Object start (followed by contract ID) |
| 🜁 | Field marker (followed by index) |
| 🜂 | Object end |
| 🜃 | Array start |
| 🜄 | Array end |
| 🜇 | Handle reference |
| 🜋 | Stream end |

### Example

Value: `{14: {@0: 123}}`
LC-T: `🜊14🜁0 123🜂`

---

# SECTION 4: SYNTAX SPECIFICATION

## 4.1 HLXL Grammar (Track A - ASCII)

```ebnf
program     = "program" IDENT "{" block* "}"
block       = "block" IDENT "(" params? ")" "{" stmt* "}"
params      = IDENT ("," IDENT)*
stmt        = let_stmt | return_stmt | if_stmt | while_stmt | expr_stmt
let_stmt    = "let" IDENT "=" expr ";"
return_stmt = "return" expr ";"
if_stmt     = "if" "(" expr ")" "{" stmt* "}" ("else" "{" stmt* "}")?
while_stmt  = "while" "(" expr ")" "{" stmt* "}"
expr_stmt   = expr ";"

expr        = pipeline
pipeline    = logical ("|>" lambda)*
lambda      = "(" params? ")" "{" stmt* "}"
logical     = equality (("&&" | "||") equality)*
equality    = comparison (("==" | "!=") comparison)*
comparison  = additive (("<" | ">" | "<=" | ">=") additive)*
additive    = multiplicative (("+" | "-") multiplicative)*
multiplicative = unary (("*" | "/" | "%") unary)*
unary       = ("!" | "-")? call
call        = primary ("(" args? ")")*
args        = expr ("," expr)*
primary     = NUMBER | STRING | "true" | "false" | "null" | IDENT | "(" expr ")" | ls_op | object | array

ls_op       = "ls.collapse" IDENT? expr
            | "ls.resolve" expr
            | "ls.snapshot"
            | "ls.transaction" "{" stmt* "}"

object      = "{" contract_id ":" "{" fields? "}" "}"
contract_id = NUMBER
fields      = field ("," field)*
field       = "@" NUMBER ":" expr

array       = "[" (expr ("," expr)*)? "]"
```

## 4.2 HLX Grammar (Track B - Runic)

Same structure, different tokens:

| HLXL Token | HLX Glyph |
|------------|-----------|
| `program` | `⟠` |
| `block` | `◇` |
| `let` | `⊢` |
| `local` | `⊡` |
| `return` | `↩` |
| `break` | `⌿` |
| `while` | `⟳` |
| `for` | `⟲` |
| `if` | `❓` |
| `else` | `❗` |
| `ls.collapse` | `⚳` |
| `ls.resolve` | `⚯` |
| `ls.snapshot` | `⚶` |
| `ls.transaction` | `⚿` |
| `\|>` | `▷` |
| `&h_` | `⟁` |

---

# SECTION 5: LATENT SPACE OPERATIONS

## 5.1 COLLAPSE (⚳ / ls.collapse)

Serialize value → Hash → Store → Return handle

```
HLXL: let h = ls.collapse tag {14:{@0:123}};
HLX:  ⊢ h = ⚳ tag {14:{@0:123}};
```

**Algorithm:**
1. Encode value to LC-B bytes
2. Compute BLAKE3 hash of bytes
3. Generate handle: `&h_<tag>_<hash_prefix>`
4. Store in CAS: `hash → LC-B bytes`
5. Return handle

**Properties:**
- IDEMPOTENT: Same value always produces same handle
- Tag is optional human-readable hint
- Hash prefix is truncated for readability

## 5.2 RESOLVE (⚯ / ls.resolve)

Lookup handle → Retrieve bytes → Decode → Return value

```
HLXL: let v = ls.resolve h;
HLX:  ⊢ v = ⚯ h;
```

**Algorithm:**
1. Parse handle to extract hash
2. Lookup hash in CAS
3. Retrieve LC-B bytes
4. Decode to HLX-Lite value
5. Return value

**Errors:**
- E_HANDLE_NOT_FOUND: Handle doesn't exist
- E_LC_PARSE: Stored bytes are corrupted

## 5.3 SNAPSHOT (⚶ / ls.snapshot)

Capture current runtime state

```
HLXL: let snap = ls.snapshot;
HLX:  ⊢ snap = ⚶;
```

**Returns:**
```json
{
  "handle_count": 247,
  "memory_bytes": 1048576,
  "handles": ["&h_foo_abc", "&h_bar_def", ...],
  "merkle_root": "0x..."
}
```

## 5.4 TRANSACTION (⚿ / ls.transaction)

Atomic operation block - all commit or all rollback

```
HLXL: ls.transaction {
    let h1 = ls.collapse data1;
    let h2 = ls.collapse data2;
    ls.guard h1 != null;
    return [h1, h2];
}

HLX: ⚿ {
    ⊢ h1 = ⚳ data1;
    ⊢ h2 = ⚳ data2;
    ls.guard h1 != null;
    ↩ [h1, h2];
}
```

---

# SECTION 6: CONTRACT REGISTRY

## 6.1 Core Value Contracts (1-5)

### Contract 1: HLXLiteValue
```
{1: {
  @0: kind,      // ENUM: 0=NULL, 1=BOOL, 2=INT, 3=FLOAT, 4=TEXT, 5=BYTES, 6=ARRAY, 7=OBJECT
  @1: bool,      // if kind=1
  @2: int,       // if kind=2
  @3: float,     // if kind=3
  @4: text,      // if kind=4
  @5: bytes,     // if kind=5
  @6: array,     // if kind=6
  @7: object     // if kind=7
}}
```

### Contract 2: HLXLiteField
```
{2: {
  @0: index,     // INT: field index (0-based)
  @1: name,      // TEXT: original key name
  @2: value      // HLXLiteValue: recursive
}}
```

### Contract 3: HLXLiteObject
```
{3: {
  @0: contract_id,  // INT: schema identifier
  @1: fields        // ARRAY[HLXLiteField]: sorted by index
}}
```

### Contract 4: HLXLiteDocument
```
{4: {
  @0: root,        // HLXLiteValue: document content
  @1: provenance   // ProvenanceLite: metadata
}}
```

### Contract 5: ProvenanceLite
```
{5: {
  @0: profile,      // TEXT: e.g., "hlx-lite-1.0"
  @1: created_at,   // TEXT: ISO8601 timestamp
  @2: engine_id,    // TEXT: producing engine
  @3: content_hash, // TEXT: BLAKE3 of root
  @4: origin        // TEXT: source identifier
}}
```

## 6.2 Latent Contracts (800+)

### Contract 800: LatentHandle
```
{800: {
  @0: id,          // TEXT: unique handle ID
  @1: tag,         // TEXT: human-readable hint
  @2: fingerprint  // BYTES: content hash
}}
```

### Contract 801: LatentTable
```
{801: {
  @0: table_id,    // TEXT: table identifier
  @1: entries,     // ARRAY: handle entries
  @2: metadata     // OBJECT: table metadata
}}
```

### Contract 820: LSOp
```
{820: {
  @0: op_code,     // INT: 0=RESOLVE, 1=COLLAPSE, 2=SNAPSHOT, 3=TRANSACTION
  @1: table,       // TEXT: target table ID
  @2: handle,      // TEXT: target handle
  @3: value,       // HLXLiteValue: input for collapse
  @4: tag,         // TEXT: optional tag
  @5: flags        // INT: operation flags
}}
```

## 6.3 Core Execution Contracts (830+)

### Contract 830: CoreProgram
```
{830: {
  @0: prog_id,     // TEXT: program identifier
  @1: blocks       // ARRAY[CoreBlock]
}}
```

### Contract 834: CoreExpr
```
{834: {
  @0: kind,        // TEXT: expression type
  @1: payload,     // varies by kind
  @2: meta         // OBJECT: source location, etc.
}}
```

---

# SECTION 7: ERROR TAXONOMY

## Error Code Ranges

| Range | Category | Description |
|-------|----------|-------------|
| 1000-1099 | Lexical | Tokenization errors |
| 1100-1199 | Syntactic | Parsing errors |
| 1200-1299 | Type | Type mismatch errors |
| 1300-1399 | Constraint | Limit/ordering violations |
| 1400-1499 | Semantic | Runtime errors |

## Common Errors

| Code | Name | Trigger |
|------|------|---------|
| 1001 | E_INVALID_CHAR | Unrecognized character in source |
| 1100 | E_LC_PARSE | Malformed LC stream |
| 1101 | E_UNEXPECTED_TOKEN | Parser encountered unexpected token |
| 1201 | E_FLOAT_SPECIAL | NaN or Infinity in float |
| 1202 | E_CONTRACT_STRUCTURE | Value doesn't match contract |
| 1301 | E_FIELD_ORDER | Fields not in ascending index order |
| 1302 | E_DEPTH_EXCEEDED | Nesting > MAX_DEPTH (64) |
| 1303 | E_SIZE_EXCEEDED | Value > MAX_SIZE (1MB) |
| 1401 | E_HANDLE_NOT_FOUND | Handle doesn't exist in CAS |
| 1402 | E_TRANSACTION_FAILED | Transaction rolled back |

---

# SECTION 8: FORMAL INVARIANTS

These MUST hold. Violation is a runtime error.

## INV-001: TOTAL_FIDELITY
```
∀v ∈ HLXLite: decode(encode(v)) == v
```

## INV-002: HANDLE_IDEMPOTENCE
```
∀v ∈ HLXLite: collapse(v) == collapse(v)
```

## INV-003: FIELD_ORDER
```
∀obj ∈ Object: ∀i < len(fields)-1: fields[i].index < fields[i+1].index
```

## INV-004: BIJECTION_HOLD
```
∀code: transliterate(transliterate(code, Track_B), Track_A) == code
```

## INV-005: LC_DETERMINISM
```
∀v, t1, t2: encode(v, time=t1) == encode(v, time=t2)
```

## INV-006: MERKLE_INTEGRITY
```
∀table: recompute_merkle(table) == table.merkle_root
```

---

# SECTION 9: COMPLETE EXAMPLES

## Example 1: Minimal Program

**HLXL:**
```
program hello {
    block main() {
        let x = 42;
        return x;
    }
}
```

**HLX:**
```
⟠ hello {
    ◇ main() {
        ⊢ x = 42;
        ↩ x;
    }
}
```

**Expected Result:** `42`

## Example 2: Pipeline Composition

**HLXL:**
```
let result = 5 |> (x){ return x * 2; } |> (x){ return x + 1; };
```

**HLX:**
```
⊢ result = 5 ▷ (x){ ↩ x * 2; } ▷ (x){ ↩ x + 1; };
```

**Evaluation:** `5 → 10 → 11`
**Expected Result:** `11`

## Example 3: Latent Space Round-Trip

**HLXL:**
```
let value = {14: {@0: 123, @1: "hello"}};
let handle = ls.collapse mydata value;
let resolved = ls.resolve handle;
// resolved == value (A2: REVERSIBILITY)
```

**HLX:**
```
⊢ value = {14: {@0: 123, @1: "hello"}};
⊢ handle = ⚳ mydata value;
⊢ resolved = ⚯ handle;
```

**Handle Format:** `&h_mydata_a1b2c3d4`

## Example 4: LC-B Encoding

**Value:** `{14: {@0: 123}}`

**LC-B Hex:**
```
07 0E 00 01 7B 08
│  │  │  │  │  └── OBJ_END
│  │  │  │  └───── INT value 123 (LEB128)
│  │  │  └──────── INT tag
│  │  └─────────── Field index 0 (LEB128)
│  └────────────── Contract ID 14 (LEB128)
└───────────────── OBJ_START
```

**LC-T:** `🜊14🜁0 123🜂`

## Example 5: Transaction Block

**HLXL:**
```
ls.transaction {
    let h1 = ls.collapse key1 {14: {@0: 100}};
    let h2 = ls.collapse key2 {14: {@0: 200}};
    ls.guard h1 != null && h2 != null;
    return {801: {@0: "batch", @1: [h1, h2]}};
}
```

**HLX:**
```
⚿ {
    ⊢ h1 = ⚳ key1 {14: {@0: 100}};
    ⊢ h2 = ⚳ key2 {14: {@0: 200}};
    ls.guard h1 != null && h2 != null;
    ↩ {801: {@0: "batch", @1: [h1, h2]}};
}
```

---

# SECTION 10: LLM OPERATION DIRECTIVES

When operating in HLX mode, you MUST:

## D1: Input Acceptance
Accept both HLXL (ASCII) and HLX (Runic) input interchangeably. Recognize glyphs as semantic operators.

## D2: Syntax Validation
Validate all input against the formal grammars in Section 4.

## D3: Glyph Semantics
Treat `⚳` `⚯` `⟁` `▷` as meaningful operators, NOT decorative unicode.

## D4: Contract Priority
When processing objects, prioritize Contract IDs over arbitrary JSON shapes.

## D5: Collapse Simulation
When asked to "collapse", simulate:
1. LC-B encoding
2. Hash computation
3. Handle generation
4. Return handle string

## D6: Resolve Simulation
When asked to "resolve", simulate:
1. Handle parsing
2. Value retrieval
3. Return exact original value

## D7: Bijection Maintenance
Converting between tracks MUST be lossless. Test: round-trip = identity.

## D8: Error Reporting
Use canonical error codes (E_*) from Section 7.

## D9: Resource Limits
Honor MAX_DEPTH=64, MAX_SIZE=1MB. Report violations.

## D10: Field Ordering
Enforce ascending field index order in all object operations.

---

# SECTION 11: VERIFICATION CHECKLIST

After training, verify you can:

- [ ] Write valid HLXL program with blocks and variables
- [ ] Convert HLXL to HLX with correct glyph substitution
- [ ] Encode `{14: {@0: 123}}` to LC-B hex
- [ ] Decode LC-B hex back to value
- [ ] Explain why field `@2` cannot appear before `@1`
- [ ] Generate a plausible handle string for a value
- [ ] Identify E_FIELD_ORDER vs E_LC_PARSE errors
- [ ] List the four axioms and their implications
- [ ] Explain the difference between LC-B and LC-T
- [ ] Write a pipeline expression in both tracks

---

# CORPUS METADATA

```json
{
  "version": "1.0.0",
  "status": "CANONICAL",
  "precision": "EXAFLOPIC",
  "author": "Matt (latentcollapse)",
  "repository": "https://github.com/latentcollapse/HLXv1.0.0",
  "license": "MIT OR Apache-2.0",
  "hash_algorithm": "BLAKE3",
  "generated": "2025-12-14"
}
```

---

**END OF TRAINING CORPUS**

*"Determinism is not a constraint—it's a feature."*
