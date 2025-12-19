# HLXL Brain - Custom Glyph Manager

## Overview

The Custom Glyph Manager allows anyone using HLX to create and use custom glyphs beyond the standard LC-R character set. This enables users to:

- Design domain-specific symbols
- Create visual identities for system components
- Extend the LC-R vocabulary with custom semantics
- Share glyph sets across projects

## Quick Start

### Register the Brain Glyph

The Valknut brain symbol (🝰) represents Helix Brain's interconnected knowledge and reasoning:

```bash
python3 glyph_manager.py register \
  --name brain \
  --glyph 🝰 \
  --svg assets/brain_glyph.svg \
  --desc "Valknut triple-triangle brain symbol - represents interconnected knowledge and reasoning" \
  --category system
```

### List Registered Glyphs

```bash
python3 glyph_manager.py list
```

Output:
```
================================================================================
REGISTERED GLYPHS
================================================================================
Name                 Glyph      Unicode      Category        SVG
--------------------------------------------------------------------------------
brain                🝰          U+1F770      system          ✓
================================================================================
Total: 1 glyphs
```

### Encode Text with Custom Glyphs

```bash
python3 glyph_manager.py encode "🜊🝰🜁inference🜂"
```

Output shows the brain glyph (🝰) at token ID 115:
```
Token IDs: [9, 115, 10, 71, 76, 68, 67, 80, 67, 76, 65, 67, 11]
                 ^^^
                 Brain glyph
```

## Usage Examples

### Register a Custom Glyph

```bash
# Register with SVG file
python3 glyph_manager.py register \
  --name tensor \
  --glyph 🝱 \
  --svg assets/tensor_glyph.svg \
  --desc "Tensor operation symbol" \
  --category operations

# Register without SVG (text-only)
python3 glyph_manager.py register \
  --name fast \
  --glyph ⚡ \
  --desc "Fast operation indicator" \
  --category modifiers
```

### View Glyph Information

```bash
python3 glyph_manager.py info brain
```

Output:
```
================================================================================
GLYPH: brain
================================================================================
Glyph:       🝰
Unicode:     U+1F770
Category:    system
Description: Valknut triple-triangle brain symbol - represents interconnected knowledge and reasoning
SVG File:    assets/brain_glyph.svg
================================================================================
```

### Encode and Decode

```bash
# Encode LC-R text
python3 glyph_manager.py encode "🜊🝰🜁thinking🜂"

# Decode token IDs back to text
python3 glyph_manager.py decode "9,115,10,71,76,68"
```

### Export and Import Glyph Sets

```bash
# Export your custom glyphs
python3 glyph_manager.py export --output my_glyphs.json

# Import glyphs from another project
python3 glyph_manager.py import other_project_glyphs.json
```

### Filter by Category

```bash
# List only system glyphs
python3 glyph_manager.py list --category system

# List only operation glyphs
python3 glyph_manager.py list --category operations
```

## Integration with HLXL Brain

### Using Custom Glyphs in Training

The glyph manager automatically extends the tokenizer vocabulary:

```python
from glyph_manager import GlyphRegistry, ExtendedTokenizer

# Load custom glyphs
registry = GlyphRegistry()

# Create extended tokenizer
tokenizer = ExtendedTokenizer(registry)

# Use in training
print(f"Vocabulary size: {tokenizer.vocab_size}")  # 115 standard + N custom
```

### Using in Generation

Custom glyphs are automatically available in inference:

```bash
python3 generate.py --prompt "🜊🝰🜁analyze🜂" --max-tokens 50
```

## Glyph Design Guidelines

### Choosing Unicode Codepoints

- **Alchemical Symbols (U+1F700-U+1F77F):** System and operation glyphs
  - 🝰 (U+1F770): Brain/reasoning
  - 🝱 (U+1F771): Tensor operations
  - 🝲 (U+1F772): Matrix operations

- **Geometric Shapes (U+25A0-U+25FF):** Structural elements
  - ◆ (U+25C6): Diamond/node
  - ◇ (U+25C7): Empty node

- **Mathematical Operators (U+2200-U+22FF):** Logical operations
  - ∀ (U+2200): For all
  - ∃ (U+2203): Exists
  - ∇ (U+2207): Gradient

### SVG File Format

Create clean, minimal SVG files:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg width="320" height="300" viewBox="400 40 330 300"
     xmlns="http://www.w3.org/2000/svg">
  <!-- Your path elements here -->
  <path d="..." style="fill:#b3b3b3;stroke:#000000;..."/>
</svg>
```

**Requirements:**
- Monochrome or limited palette (2-3 colors)
- Clear at small sizes (16x16 to 64x64 pixels)
- Single viewBox (no transforms or groups)
- File size < 10KB

### Naming Conventions

- **Name:** lowercase_with_underscores (e.g., `brain`, `tensor_multiply`)
- **Category:** system | operations | modifiers | structures | domain_specific
- **Description:** Clear, concise explanation of semantic meaning

## Brain Glyph (🝰)

### Design

The brain glyph uses the **Valknut** symbol - a Norse triple-triangle interlocked pattern representing:

- **Interconnected Knowledge:** Three triangles represent data, algorithms, and reasoning
- **Holistic Intelligence:** Interlocking structure shows integration of components
- **Norse Heritage:** Valknut symbolizes Odin's wisdom and knowledge-seeking

### Usage in HLX

The brain glyph can be used to:

1. **Mark Brain Operations:** `🜊🝰🜁operation🜁model ⟁brain🜂`
2. **UI Indicator:** Display when Studio Brain is active/thinking
3. **Documentation:** Visual identity for HLXL Brain components
4. **Logging:** Prefix log messages from Brain inference

### SVG Source

The clean Valknut design is available at `assets/brain_glyph.svg` (320x300px, triple-triangle interlocked pattern).

## Registry File Format

The glyph registry (`glyph_registry.json`) stores all custom glyphs:

```json
{
  "version": "1.0",
  "glyphs": {
    "brain": {
      "name": "brain",
      "glyph": "🝰",
      "unicode": "U+1F770",
      "svg_path": "assets/brain_glyph.svg",
      "description": "Valknut triple-triangle brain symbol - represents interconnected knowledge and reasoning",
      "category": "system"
    }
  }
}
```

## Commands Reference

```bash
# Register
python3 glyph_manager.py register --name NAME --glyph CHAR [--svg FILE] [--desc TEXT] [--category CAT]

# Unregister
python3 glyph_manager.py unregister NAME

# List
python3 glyph_manager.py list [--category CAT]

# Info
python3 glyph_manager.py info NAME

# Encode
python3 glyph_manager.py encode TEXT

# Decode
python3 glyph_manager.py decode TOKEN_IDS

# Export
python3 glyph_manager.py export --output FILE

# Import
python3 glyph_manager.py import FILE
```

## Advanced Usage

### Programmatic Access

```python
from glyph_manager import GlyphRegistry, ExtendedTokenizer

# Create registry
registry = GlyphRegistry()

# Register glyph programmatically
registry.register(
    name="custom",
    glyph="🝲",
    svg_path="path/to/custom.svg",
    description="Custom operation",
    category="operations"
)

# Get glyph info
glyph_info = registry.get_glyph("custom")
print(f"Glyph: {glyph_info['glyph']}")

# Create extended tokenizer
tokenizer = ExtendedTokenizer(registry)

# Encode with custom glyphs
token_ids = tokenizer.encode("🜊🝲🜁compute🜂")
```

### Sharing Glyph Sets

```bash
# Export project glyphs
python3 glyph_manager.py export --output hlx_system_glyphs.json

# Share file with team
# Team members import:
python3 glyph_manager.py import hlx_system_glyphs.json
```

## Files Created

- `glyph_manager.py` - Main CLI tool (389 lines)
- `glyph_registry.json` - Registry of custom glyphs
- `assets/brain_glyph.svg` - Valknut brain symbol SVG

## Next Steps

1. **Create domain-specific glyphs** for your HLX application
2. **Share glyph sets** with your team via export/import
3. **Design visual identity** using custom glyphs in UI
4. **Extend tokenizer** with semantic symbols for your domain

---

**Created:** 2025-12-18
**Part of:** HLXL Brain - Custom inference engine for HLX/LC-R format
**License:** MIT
