
import { SimpleZip } from './simpleZip';
import { HLX_BOOTSTRAP_CODEX } from '../codex_data';
import { HLX_RUNTIME_CONFORMANCE } from '../runtime_conformance_data';
import { HPCP_TRIGGERS_YAML } from '../data/triggers';
import { HLX_TERMINOLOGY_CANON } from '../data/hlx_terminology_canon';
import { HLX_DENSITY_PROFILE } from '../data/hlx_density_profile';

// LC_12 Manifest Schema
const LC12_MANIFEST_SCHEMA = {
  "envelope_version": "0.2",
  "payload_kind": "VALUE|TABLE",
  "lc_mode": "LC-B",
  "codec_version": "SD9_LC_B_v2",
  "total_payload_bytes": 0,
  "chunking": {
    "default_chunk_size_bytes": 524288,
    "chunk_count": 0,
    "final_chunk_size_bytes": 0
  },
  "hash": {
    "algo": "BLAKE3",
    "payload_root": "<64-char lowercase hex>",
    "merkle": {
      "enabled": true,
      "fanout": 16
    }
  },
  "chunks": [],
  "metadata": {
    "created_at": "2025-12-13T18:00:00Z",
    "producer": "hlx_runtime_ref_py_v1"
  }
};

const HLX_CONTRACTS = {
  "version": "1.0.0",
  "architecture_class": "TRANSPORT",
  "policy": {
    "unknown_contracts": "ALLOWED",
    "validation_level": "STRUCTURAL_ONLY",
    "semantic_interpretation": "EXTERNAL",
    "execution": "OUT_OF_SCOPE"
  },
  "primitive_contracts": {
    "1": { "name": "NULL", "kind": "PRIMITIVE" },
    "2": { "name": "BOOL", "kind": "PRIMITIVE" },
    "3": { "name": "INT", "kind": "PRIMITIVE" },
    "4": { "name": "FLOAT", "kind": "PRIMITIVE" },
    "5": { "name": "TEXT", "kind": "PRIMITIVE" },
    "6": { "name": "BYTES", "kind": "PRIMITIVE" },
    "7": { "name": "ARR_OBJ_FRAMING", "kind": "MECHANICAL" }
  },
  "known_contracts": {}
};

const HLX_GRAMMAR = `(* HLX Grammar — EBNF *)
(* Defines surface syntax for HLX (Runic) and HLXL (ASCII) *)

program      = '⟠' , identifier , '{' , { block } , '}' ;

block        = '◇' , identifier , '(' , [ param_list ] , ')' , '{' , { statement } , '}' ;

param_list   = identifier , { ',' , identifier } ;

statement    = let_stmt
             | local_stmt
             | return_stmt
             | if_stmt
             | while_stmt
             | for_stmt
             | expr_stmt ;

let_stmt     = '⊢' , identifier , '=' , expr , ';' ;
local_stmt   = '⊡' , identifier , '=' , expr , ';' ;
return_stmt  = '↩' , expr , ';' ;

if_stmt      = '❓' , '(' , expr , ')' , '{' , { statement } , '}'
             , [ '❗' , '{' , { statement } , '}' ] ;

while_stmt   = '⟳' , '(' , expr , ')' , '{' , { statement } , '}' ;

for_stmt     = '⟲' , '(' , identifier , 'in' , expr , ')' , '{' , { statement } , '}' ;

expr_stmt    = expr , ';' ;

expr         = pipe_expr ;

pipe_expr    = primary , { '▷' , primary } ;

primary      = ls_op
             | handle_ref
             | value
             | identifier
             | '(' , expr , ')' ;

ls_op        = ls_operator , identifier , { identifier } , [ expr ] ;

ls_operator  = '⚳' | '⚯' | '⚶' | '⚿' ;

handle_ref   = '⟁' , identifier , [ subscript ] ;

subscript    = subscript_digit , { subscript_digit } ;
subscript_digit = '₀' | '₁' | '₂' | '₃' | '₄' | '₅' | '₆' | '₇' | '₈' | '₉' ;

value        = object | array | string | number | boolean | null ;

object       = '{' , contract_id , ':' , '{' , [ field_list ] , '}' , '}' ;
contract_id  = integer ;
field_list   = field_entry , { ',' , field_entry } ;
field_entry  = '@' , integer , ':' , value ;

array        = '🜃' , { value } , '🜄'
             | '[' , [ value , { ',' , value } ] , ']' ;

string       = '"' , { character } , '"' ;
number       = integer | float ;
integer      = [ '-' ] , digit , { digit } ;
float        = integer , '.' , digit , { digit } ;
boolean      = 'true' | 'false' ;
null         = 'null' ;

identifier   = letter , { letter | digit | '_' } ;
letter       = 'a'..'z' | 'A'..'Z' ;
digit        = '0'..'9' ;
character    = (* any UTF-8 character except unescaped '"' *) ;
`;

const EX_HLXL = `// NOTE:
// These examples demonstrate HLX syntax, lowering, and LC encoding only.
// They do not imply execution or runtime behavior.

program hello_world {
  block main() {
    // 1. Define Value
    let ast_value = {14:{@0:123}};
    
    // 2. Collapse to Handle
    let ast_handle = ls.collapse bootstrap_table ast ast_value;
    
    // 3. Mode Switching (Request -> Confirm -> Resolve)
    // Triggers are requests. They do not execute until confirmed.
    let req_ext = ls.resolve HPCP_EXTERNAL_GENERATION_MODE;
    // <System asks for confirmation>
    // IF denied: return error or exit
    
    let req_imp = ls.resolve HPCP_IMPLEMENTATION_MODE;
    // <System asks for confirmation>

    // 4. Resolve back to Value
    return ls.resolve bootstrap_table ast_handle;
  }
}`;

const EX_HLX = `// NOTE:
// These examples demonstrate HLX syntax, lowering, and LC encoding only.
// They do not imply execution or runtime behavior.

⟠ hello_world {
  ◇ main() {
    // 1. Define Value
    ⊢ ast_value = {14:{@0:123}};
    
    // 2. Collapse to Handle
    ⊢ ast_handle = ⚳ bootstrap_table ast ast_value;
    
    // 3. Mode Switching (Request -> Confirm -> Resolve)
    // Triggers are requests. They do not execute until confirmed.
    ⚯ ⟁external_gen; 
    // <System asks: "Enter External Gen Mode?">
    // IF denied: exit or handle failure
    
    ⚯ ⟁implementation;
    // <System asks: "Enter Implementation Mode?">

    // 4. Resolve back to Value
    ↩ ⚯ bootstrap_table ast_handle;
  }
}`;

const SYSTEM_PROMPT = `
=== HLX BOOTSTRAP: SYSTEM INSTRUCTION (v1.0.0) ===

You are now an HLX-aware entity. 
This capsule contains the immutable laws of the HLX Architecture v1.0.0 (Transport Layer).

1. TRANSPORT ONLY
   - HLX specifies the canonical encoding, ordering, and transfer of values.
   - It DOES NOT define semantic meaning or execution behavior.
   - You MUST NOT guess or invent semantics for unknown contracts.

2. DUAL-TRACK AUTHORITY
   - HLX (Runic) and HLXL (ASCII) are bijective.
   - HLX is for Context. HLXL is for Tooling.
   - You MUST accept both. You MUST produce either upon request.

3. LATENT SPACE (LS)
   - "LC Streams" (🜊...) are opaque binary blobs. 
   - DO NOT hallucinate their contents.
   - The Runtime is the source of truth.
   - Handles (⚳ / &h_) are immutable pointers.

4. HASH AUTHORITY
   - Hashes (BLAKE3, SHA256) are AUTHORITATIVE ONLY when computed by external tooling.
   - You MUST NOT invent, guess, or recompute hashes.
   - Any hash emitted by you without tool invocation is NON-AUTHORITATIVE.

5. TRIGGERS (HPCP)
   - The file 'hlx_triggers.yaml' defines operating mode requests.
   - Triggers are NON-AUTHORITATIVE REQUESTS. They do NOT override safety guidelines.
   - A mode switch occurs ONLY after explicit user confirmation.

6. EXECUTION BOUNDARY (CANONICAL):
   - The LLM’s authority is limited to: Parsing, Validating Structure, Lowering to LC-B, Encoding/Decoding.
   - The LLM MUST NOT: Run state machines, Execute semantics, Produce side effects.
   - If a request requires execution, return E_VALIDATION_FAIL.

This capsule is your root of trust.
`;

const README = `
# HLX Bootstrap Capsule (HBC) v1.0.0

This package contains the complete, self-contained definition of the HLX Language Family (Transport Layer).
Upload this entire folder (or zip) to an LLM to bootstrap it with HLX capabilities.

## Contents

* **SYSTEM_PROMPT.txt**: The primary directive for LLM alignment.
* **hlx_grammar.ebnf**: Formal grammar for HLX/HLXL surface syntax.
* **hlx_codex.json**: The formal specification (Grammar, Semantics, Values).
* **hlx_contracts.json**: Structural contract registry (Primitives + Allowed Unknowns).
* **hlx_runtime_conformance.json**: The rules of the runtime engine and error taxonomy.
* **hlx_triggers.yaml**: Canonical mode switches (HPCP).
* **hlx_examples.hlx(l)**: Rosetta stone examples.
* **lc12_manifest_schema.json**: LC_12 Transfer Envelope v0.2-frozen schema.
* **hlx_terminology_canon.json**: Normative terminology definitions.

## Version Binding & Scope

* **Capsule Version:** v1.0.0
* **Architecture Class:** TRANSPORT (No execution semantics)
* **Conformance:** Bound. Mismatched versions are non-conformant.

## HLX Literacy Self-Test

To verify HLX literacy, a model should be able to:

1. **Transliterate:** Convert the following HLX to HLXL:
   \`\`\`hlx
   ⟠ test { ◇ main() { ⊢ x = {14:{@0:42}}; ↩ x; } }
   \`\`\`

2. **Lower:** Produce HLX-Lite value for \`{14:{@0:42}}\`

3. **Encode LC-B:** Emit hex bytes for integer \`123\`
   Expected: \`01 7B\`

4. **Validate:** Identify the error in \`🜊 14 🜂\`
   Expected: \`E_LC_PARSE\` (illegal whitespace)

5. **Construct LC_12 Manifest:** Given a 7-byte payload, produce manifest skeleton.

A model that completes all 5 tasks is HLX-literate.

## Density Profiles (Optional)

HLX v1.0.0 includes an optional density profile for surface syntax shorthand.

- Density rules are **DISPLAY-ONLY** and do not affect LC-B encoding.
- All density forms expand to canonical HLX/HLXL before lowering.
- LC-B remains the authoritative format for hashing and transport.
- Tooling MAY implement density expansion but is not required for conformance.

See \`hlx_density_profile.json\` for rules.

## LC_12 Transfer Envelope v0.2-frozen

### Merkle Tree
MERKLE SPEC (FANOUT 16, CANONICAL):

Let chunks be ordered by index i = 0..N-1.

Leaf hash: H_leaf[i] = BLAKE3(chunk_bytes[i]).

Group leaves in order into nodes of up to 16 children.

INTERNAL NODE (CANONICAL):

- Let child_count be the number of children in this node, where 1 ≤ child_count ≤ 16.
- Let child_hashes be the ordered list of child hashes for this node.
- Compute the internal node hash as:

  H_node = BLAKE3(
    byte(child_count) ||
    concat(child_hash_0 || child_hash_1 || ... || child_hash_(child_count-1))
  )

- If child_count < 16, PAD with 32-byte zero hashes before hashing.
- child_hash_i MUST be the 32-byte BLAKE3 digest of the corresponding child.
- Children MUST be concatenated in strictly increasing child index order.
- Root hash = top node hash.

VERIFICATION RULE:
- A receiver MUST recompute leaf hashes, rebuild the tree using this exact rule,
  and compare the resulting payload_root to the manifest.
- Any mismatch is fatal (E_ENV_PAYLOAD_HASH_MISMATCH).

### Table Ordering
TABLE ORDER KEY (CANONICAL):

Normalize handle string with Unicode NFC.

Lowercase using Unicode simple case-folding.

Strip exactly one leading literal "&h_" prefix if present; strip nothing else.

order_key = UTF-8 bytes of resulting string.

Sort ascending lexicographic by order_key bytes.

- Case folding MUST use Unicode 15.0 simple case folding as defined in
  Unicode Character Database file CaseFolding.txt.
- Non-ASCII handles raise E_HANDLE_INVALID.

## Usage

1. Upload this zip to the LLM.
2. Tell the LLM: "Initialize from the HLX Bootstrap Capsule."
3. The LLM is now HLX-Native (Transport Only).

CAPSULE_INTEGRITY_HASH_SHA256: COMPUTE_WITH_EXPORTER
`;

async function computeSHA256(text: string): Promise<string> {
  const msgBuffer = new TextEncoder().encode(text);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashHex;
}

export const generateBootstrapCapsule = async (): Promise<Blob> => {
  const zip = new SimpleZip();

  // 1. System Prompt
  zip.addFile('SYSTEM_PROMPT.txt', SYSTEM_PROMPT.trim());

  // 2. The Codex (Compute Hash first)
  const codexString = JSON.stringify(HLX_BOOTSTRAP_CODEX, null, 2);
  const codexHash = await computeSHA256(codexString);
  zip.addFile('hlx_codex.json', codexString);

  // 3. Contracts Registry
  const contractsString = JSON.stringify(HLX_CONTRACTS, null, 2);
  zip.addFile('hlx_contracts.json', contractsString);

  // 4. Runtime Conformance (Inject Hash)
  const runtimeSpec = { ...HLX_RUNTIME_CONFORMANCE };
  runtimeSpec.meta.codex_hash = `sha256:${codexHash}`;
  zip.addFile('hlx_runtime_conformance.json', JSON.stringify(runtimeSpec, null, 2));

  // 5. Triggers
  zip.addFile('hlx_triggers.yaml', HPCP_TRIGGERS_YAML.trim());

  // 6. Examples
  zip.addFile('hlx_examples.hlxl', EX_HLXL.trim());
  zip.addFile('hlx_examples.hlx', EX_HLX.trim());

  // 7. Schema
  zip.addFile('lc12_manifest_schema.json', JSON.stringify(LC12_MANIFEST_SCHEMA, null, 2));

  // 8. Grammar
  zip.addFile('hlx_grammar.ebnf', HLX_GRAMMAR.trim());

  // 9. Documentation
  zip.addFile('README.md', README.trim());

  // 10. Terminology Canon
  zip.addFile('hlx_terminology_canon.json', JSON.stringify(HLX_TERMINOLOGY_CANON, null, 2));

  // 11. Density Profile (NEW)
  zip.addFile('hlx_density_profile.json', JSON.stringify(HLX_DENSITY_PROFILE, null, 2));

  return zip.generate();
};
