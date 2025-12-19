#!/usr/bin/env python3
"""
HLXL Brain - Custom Glyph Manager

Manage custom glyphs for HLX/LC-R format, allowing anyone to:
- Register new glyphs (name, SVG file, Unicode identifier)
- Use custom glyphs in tokenization
- Export glyph sets for sharing

Usage:
    # Register the brain glyph
    python3 glyph_manager.py register --name brain --glyph 🝰 --svg assets/brain_glyph.svg

    # List all registered glyphs
    python3 glyph_manager.py list

    # Use custom glyph in text
    python3 glyph_manager.py encode "🜊🝰🜁inference🜂"

    # Export glyph set
    python3 glyph_manager.py export --output custom_glyphs.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tokenizer import LCRTokenizer


class GlyphRegistry:
    """Registry for custom glyphs."""

    def __init__(self, registry_path: str = "glyph_registry.json"):
        self.registry_path = Path(registry_path)
        self.glyphs: Dict[str, dict] = {}
        self.load()

    def load(self):
        """Load glyph registry from disk."""
        if self.registry_path.exists():
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.glyphs = data.get('glyphs', {})
                print(f"Loaded {len(self.glyphs)} custom glyphs from {self.registry_path}")
        else:
            print(f"No registry found at {self.registry_path}, starting fresh")
            self.glyphs = {}

    def save(self):
        """Save glyph registry to disk."""
        data = {
            'version': '1.0',
            'glyphs': self.glyphs,
        }
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved {len(self.glyphs)} custom glyphs to {self.registry_path}")

    def register(
        self,
        name: str,
        glyph: str,
        svg_path: Optional[str] = None,
        description: Optional[str] = None,
        category: str = "custom",
    ):
        """Register a new custom glyph."""
        # Validate glyph is a single character
        if len(glyph) != 1:
            raise ValueError(f"Glyph must be a single character, got: {glyph}")

        # Check if SVG file exists
        if svg_path:
            svg_file = Path(svg_path)
            if not svg_file.exists():
                raise FileNotFoundError(f"SVG file not found: {svg_path}")

        # Check if glyph already registered
        if name in self.glyphs:
            print(f"Warning: Overwriting existing glyph '{name}'")

        self.glyphs[name] = {
            'name': name,
            'glyph': glyph,
            'unicode': f"U+{ord(glyph):04X}",
            'svg_path': str(svg_path) if svg_path else None,
            'description': description or f"Custom glyph: {name}",
            'category': category,
        }

        self.save()
        print(f"✓ Registered glyph '{name}': {glyph} (U+{ord(glyph):04X})")

    def unregister(self, name: str):
        """Remove a glyph from the registry."""
        if name not in self.glyphs:
            raise KeyError(f"Glyph '{name}' not found in registry")

        glyph_info = self.glyphs.pop(name)
        self.save()
        print(f"✓ Unregistered glyph '{name}': {glyph_info['glyph']}")

    def list_glyphs(self, category: Optional[str] = None) -> List[dict]:
        """List all registered glyphs, optionally filtered by category."""
        glyphs = list(self.glyphs.values())

        if category:
            glyphs = [g for g in glyphs if g['category'] == category]

        return glyphs

    def get_glyph(self, name: str) -> Optional[dict]:
        """Get glyph info by name."""
        return self.glyphs.get(name)

    def get_all_glyphs_string(self) -> str:
        """Get string of all custom glyphs for tokenizer."""
        return ''.join(g['glyph'] for g in self.glyphs.values())

    def export(self, output_path: str):
        """Export glyph set to JSON file for sharing."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.glyphs, f, indent=2, ensure_ascii=False)
        print(f"✓ Exported {len(self.glyphs)} glyphs to {output_path}")

    def import_glyphs(self, import_path: str):
        """Import glyphs from JSON file."""
        with open(import_path, 'r', encoding='utf-8') as f:
            imported = json.load(f)

        count = 0
        for name, glyph_info in imported.items():
            if name not in self.glyphs:
                self.glyphs[name] = glyph_info
                count += 1
            else:
                print(f"Skipping existing glyph: {name}")

        self.save()
        print(f"✓ Imported {count} new glyphs from {import_path}")


class ExtendedTokenizer(LCRTokenizer):
    """Extended tokenizer with custom glyph support."""

    def __init__(self, registry: GlyphRegistry):
        super().__init__()
        self.registry = registry

        # Add custom glyphs to vocabulary
        custom_glyphs = registry.get_all_glyphs_string()
        for glyph in custom_glyphs:
            if glyph not in self.vocab:
                # Add to end of vocabulary
                token_id = len(self.vocab)
                self.vocab[glyph] = token_id
                self.id_to_token[token_id] = glyph

        print(f"✓ Tokenizer extended with {len(custom_glyphs)} custom glyphs")
        print(f"  Total vocabulary size: {self.vocab_size}")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Manage custom glyphs for HLXL Brain",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Register brain glyph
  python3 glyph_manager.py register --name brain --glyph 🝰 --svg assets/brain_glyph.svg --desc "Valknut brain symbol"

  # List all glyphs
  python3 glyph_manager.py list

  # Encode text with custom glyphs
  python3 glyph_manager.py encode "🜊🝰🜁inference🜂"

  # Export glyph set
  python3 glyph_manager.py export --output my_glyphs.json
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Register command
    register_parser = subparsers.add_parser('register', help='Register a new custom glyph')
    register_parser.add_argument('--name', type=str, required=True,
                                 help='Glyph name (e.g., "brain")')
    register_parser.add_argument('--glyph', type=str, required=True,
                                 help='Unicode glyph character (e.g., "🝰")')
    register_parser.add_argument('--svg', type=str,
                                 help='Path to SVG file')
    register_parser.add_argument('--desc', type=str,
                                 help='Description of the glyph')
    register_parser.add_argument('--category', type=str, default='custom',
                                 help='Glyph category (default: custom)')

    # Unregister command
    unregister_parser = subparsers.add_parser('unregister', help='Remove a glyph from registry')
    unregister_parser.add_argument('name', type=str, help='Glyph name to remove')

    # List command
    list_parser = subparsers.add_parser('list', help='List registered glyphs')
    list_parser.add_argument('--category', type=str,
                            help='Filter by category')

    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode text with custom glyphs')
    encode_parser.add_argument('text', type=str, help='Text to encode')

    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode token IDs to text')
    decode_parser.add_argument('token_ids', type=str,
                              help='Comma-separated token IDs (e.g., "4,15,32")')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export glyph set')
    export_parser.add_argument('--output', type=str, required=True,
                              help='Output JSON file')

    # Import command
    import_parser = subparsers.add_parser('import', help='Import glyph set')
    import_parser.add_argument('input', type=str, help='Input JSON file')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show glyph information')
    info_parser.add_argument('name', type=str, help='Glyph name')

    parser.add_argument('--registry', type=str, default='glyph_registry.json',
                       help='Path to glyph registry file (default: glyph_registry.json)')

    return parser.parse_args()


def cmd_register(registry: GlyphRegistry, args):
    """Handle register command."""
    registry.register(
        name=args.name,
        glyph=args.glyph,
        svg_path=args.svg,
        description=args.desc,
        category=args.category,
    )


def cmd_unregister(registry: GlyphRegistry, args):
    """Handle unregister command."""
    registry.unregister(args.name)


def cmd_list(registry: GlyphRegistry, args):
    """Handle list command."""
    glyphs = registry.list_glyphs(category=args.category)

    if not glyphs:
        print("No glyphs registered")
        return

    print()
    print("="*80)
    print("REGISTERED GLYPHS")
    print("="*80)
    print(f"{'Name':<20} {'Glyph':<10} {'Unicode':<12} {'Category':<15} {'SVG':<20}")
    print("-"*80)

    for glyph_info in sorted(glyphs, key=lambda g: g['name']):
        svg_status = "✓" if glyph_info.get('svg_path') else "-"
        print(f"{glyph_info['name']:<20} {glyph_info['glyph']:<10} "
              f"{glyph_info['unicode']:<12} {glyph_info['category']:<15} {svg_status:<20}")

    print("="*80)
    print(f"Total: {len(glyphs)} glyphs")
    print()


def cmd_encode(registry: GlyphRegistry, args):
    """Handle encode command."""
    tokenizer = ExtendedTokenizer(registry)

    token_ids = tokenizer.encode(args.text, add_special_tokens=False)

    print()
    print("="*80)
    print("ENCODING RESULT")
    print("="*80)
    print(f"Text: {args.text}")
    print(f"Token IDs: {token_ids}")
    print(f"Tokens: {len(token_ids)}")
    print()
    print("Character breakdown:")
    for i, (char, token_id) in enumerate(zip(args.text, token_ids)):
        unicode_code = f"U+{ord(char):04X}"
        print(f"  [{i}] '{char}' → {token_id} ({unicode_code})")
    print("="*80)
    print()


def cmd_decode(registry: GlyphRegistry, args):
    """Handle decode command."""
    tokenizer = ExtendedTokenizer(registry)

    # Parse token IDs
    token_ids = [int(x.strip()) for x in args.token_ids.split(',')]

    decoded = tokenizer.decode(token_ids, skip_special_tokens=False)

    print()
    print("="*80)
    print("DECODING RESULT")
    print("="*80)
    print(f"Token IDs: {token_ids}")
    print(f"Decoded text: {decoded}")
    print("="*80)
    print()


def cmd_export(registry: GlyphRegistry, args):
    """Handle export command."""
    registry.export(args.output)


def cmd_import(registry: GlyphRegistry, args):
    """Handle import command."""
    registry.import_glyphs(args.input)


def cmd_info(registry: GlyphRegistry, args):
    """Handle info command."""
    glyph_info = registry.get_glyph(args.name)

    if not glyph_info:
        print(f"Error: Glyph '{args.name}' not found")
        sys.exit(1)

    print()
    print("="*80)
    print(f"GLYPH: {args.name}")
    print("="*80)
    print(f"Glyph:       {glyph_info['glyph']}")
    print(f"Unicode:     {glyph_info['unicode']}")
    print(f"Category:    {glyph_info['category']}")
    print(f"Description: {glyph_info['description']}")
    if glyph_info.get('svg_path'):
        print(f"SVG File:    {glyph_info['svg_path']}")
    print("="*80)
    print()


def main():
    """Main function."""
    args = parse_args()

    if not args.command:
        print("Error: No command specified")
        print("Run 'python3 glyph_manager.py --help' for usage")
        sys.exit(1)

    # Load registry
    registry = GlyphRegistry(registry_path=args.registry)

    # Dispatch commands
    commands = {
        'register': cmd_register,
        'unregister': cmd_unregister,
        'list': cmd_list,
        'encode': cmd_encode,
        'decode': cmd_decode,
        'export': cmd_export,
        'import': cmd_import,
        'info': cmd_info,
    }

    handler = commands.get(args.command)
    if handler:
        handler(registry, args)
    else:
        print(f"Error: Unknown command '{args.command}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
