
export const HLX_DENSITY_PROFILE = {
  "document": "HLX Density Profile",
  "version": "1.0.0",
  "status": "DISPLAY_ONLY",
  "authority": "NON_CANONICAL",
  "scope": [
    "HLX surface syntax",
    "HLXL surface syntax",
    "LC-R"
  ],
  "non_scope": [
    "LC-B encoding",
    "LC_12 envelopes",
    "Hashing",
    "Runtime semantics"
  ],
  "invariant": "All density forms MUST expand to canonical HLX/HLXL before lowering to LC.",
  "rules": [
    {
      "id": "DENSITY_SINGLE_FIELD_OBJECT",
      "surface_form": "{C:V}",
      "expands_to": "{C:{@0:V}}",
      "validation": "ADVISORY",
      "notes": [
        "Valid only when contract C has exactly one field.",
        "Parsers MAY enforce using hlx_contracts.json.",
        "Parsers MUST NOT reject if metadata unavailable."
      ]
    },
    {
      "id": "DENSITY_EMPTY_ARRAY_RUNIC",
      "surface_form": "∅ᵃ",
      "expands_to": "🜃🜄",
      "track": "HLX only",
      "transliteration": "N/A — expands before track conversion"
    },
    {
      "id": "DENSITY_EMPTY_OBJECT_RUNIC",
      "surface_form": "∅ᵒ(C)",
      "expands_to": "{C:{}}",
      "track": "HLX only",
      "transliteration": "N/A — expands before track conversion",
      "note": "C is the explicit contract ID"
    }
  ],
  "reversibility": {
    "required": true,
    "statement": "Any density form MUST be losslessly reversible to its canonical expanded form.",
    "failure_error": "E_CANONICALIZATION_FAIL"
  }
};
