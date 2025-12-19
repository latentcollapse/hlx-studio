"""
HLXL Brain - LC-R Tokenizer

Ultra-compact character-level tokenizer for LC-R (Latent Collapse Runic) format.
Vocabulary size: <100 tokens (vs. 50k+ for English tokenizers).

LC-R uses Unicode alchemical glyphs and structured notation:
- Primitives: ∅ (null), ⊤ (true), ⊥ (false)
- Contracts: 🜊 (open), 🜁 (field sep), 🜂 (close)
- References: ⟁ (handle prefix), ⊠ (bytes prefix)
- Standard: digits, letters, quotes, punctuation

Target: 100% round-trip accuracy, <1ms encoding/decoding latency.
"""

from typing import List, Dict, Optional
import json


class LCRTokenizer:
    """Character-level tokenizer for LC-R format."""

    # Special tokens
    PAD_TOKEN = "<PAD>"
    BOS_TOKEN = "<BOS>"
    EOS_TOKEN = "<EOS>"
    UNK_TOKEN = "<UNK>"

    # Core LC-R glyphs (alchemical and logical symbols)
    LC_R_GLYPHS = [
        "∅",  # null
        "⊤",  # true
        "⊥",  # false
        "⟁",  # handle prefix (replaces &h_)
        "⊠",  # bytes prefix
        "🜊",  # contract open (replaces {)
        "🜁",  # field separator (replaces :)
        "🜂",  # contract close (replaces })
        "🜃",  # list open (replaces [)
        "🜄",  # list close (replaces ])
        "◇",  # diamond open (object start)
        "◆",  # diamond filled (object end)
        "→",  # arrow (seq2seq separator)
        "λ",  # lambda (greek letter - used in strings)
        "∀",  # for all (universal quantifier)
        "∃",  # exists (existential quantifier)
    ]

    def __init__(self):
        """Initialize tokenizer with compact LC-R vocabulary."""
        # Build vocabulary
        self.vocab: Dict[str, int] = {}
        self.id_to_token: Dict[int, str] = {}

        # Special tokens (IDs 0-3)
        special_tokens = [self.PAD_TOKEN, self.BOS_TOKEN, self.EOS_TOKEN, self.UNK_TOKEN]
        for token in special_tokens:
            idx = len(self.vocab)
            self.vocab[token] = idx
            self.id_to_token[idx] = token

        # LC-R glyphs (IDs 4-11)
        for glyph in self.LC_R_GLYPHS:
            idx = len(self.vocab)
            self.vocab[glyph] = idx
            self.id_to_token[idx] = glyph

        # Digits 0-9 (IDs 12-21)
        for digit in "0123456789":
            idx = len(self.vocab)
            self.vocab[digit] = idx
            self.id_to_token[idx] = digit

        # Common punctuation and structural characters
        punctuation = [
            " ", "\n", "\t",  # Whitespace
            ".", ",", ":", ";",  # Punctuation
            "\"", "'",  # Quotes
            "(", ")", "[", "]", "{", "}",  # Brackets
            "@", "#", "$", "%", "&", "*",  # Symbols
            "+", "-", "=", "/", "\\", "|",  # Operators
            "<", ">", "~", "`", "^", "_",  # More symbols
            "?", "!",  # Sentence endings
        ]
        for char in punctuation:
            if char not in self.vocab:  # Avoid duplicates
                idx = len(self.vocab)
                self.vocab[char] = idx
                self.id_to_token[idx] = char

        # Lowercase letters a-z
        for char in "abcdefghijklmnopqrstuvwxyz":
            idx = len(self.vocab)
            self.vocab[char] = idx
            self.id_to_token[idx] = char

        # Uppercase letters A-Z
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            idx = len(self.vocab)
            self.vocab[char] = idx
            self.id_to_token[idx] = char

        # Store vocab size
        self.vocab_size = len(self.vocab)

        # Cache special token IDs for fast access
        self.pad_token_id = self.vocab[self.PAD_TOKEN]
        self.bos_token_id = self.vocab[self.BOS_TOKEN]
        self.eos_token_id = self.vocab[self.EOS_TOKEN]
        self.unk_token_id = self.vocab[self.UNK_TOKEN]

    def encode(self, text: str, add_special_tokens: bool = False) -> List[int]:
        """
        Encode text to token IDs.

        Args:
            text: Input LC-R text
            add_special_tokens: If True, add BOS/EOS tokens

        Returns:
            List of token IDs
        """
        token_ids = []

        if add_special_tokens:
            token_ids.append(self.bos_token_id)

        for char in text:
            token_id = self.vocab.get(char, self.unk_token_id)
            token_ids.append(token_id)

        if add_special_tokens:
            token_ids.append(self.eos_token_id)

        return token_ids

    def decode(self, token_ids: List[int], skip_special_tokens: bool = True) -> str:
        """
        Decode token IDs to text.

        Args:
            token_ids: List of token IDs
            skip_special_tokens: If True, skip PAD/BOS/EOS tokens

        Returns:
            Decoded text
        """
        special_token_ids = {self.pad_token_id, self.bos_token_id, self.eos_token_id}

        chars = []
        for token_id in token_ids:
            if skip_special_tokens and token_id in special_token_ids:
                continue

            token = self.id_to_token.get(token_id, self.UNK_TOKEN)
            chars.append(token)

        return "".join(chars)

    def encode_batch(self, texts: List[str], add_special_tokens: bool = False) -> List[List[int]]:
        """Encode multiple texts."""
        return [self.encode(text, add_special_tokens) for text in texts]

    def decode_batch(self, token_ids_batch: List[List[int]], skip_special_tokens: bool = True) -> List[str]:
        """Decode multiple sequences."""
        return [self.decode(token_ids, skip_special_tokens) for token_ids in token_ids_batch]

    def save_vocab(self, path: str) -> None:
        """Save vocabulary to JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.vocab, f, ensure_ascii=False, indent=2)

    def load_vocab(self, path: str) -> None:
        """Load vocabulary from JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            self.vocab = json.load(f)

        # Rebuild reverse mapping
        self.id_to_token = {idx: token for token, idx in self.vocab.items()}
        self.vocab_size = len(self.vocab)

        # Rebuild cached IDs
        self.pad_token_id = self.vocab[self.PAD_TOKEN]
        self.bos_token_id = self.vocab[self.BOS_TOKEN]
        self.eos_token_id = self.vocab[self.EOS_TOKEN]
        self.unk_token_id = self.vocab[self.UNK_TOKEN]

    def get_vocab_stats(self) -> Dict[str, int]:
        """Get vocabulary statistics."""
        return {
            "vocab_size": self.vocab_size,
            "special_tokens": 4,
            "lc_r_glyphs": len(self.LC_R_GLYPHS),
            "digits": 10,
            "letters": 52,
            "punctuation": self.vocab_size - 4 - len(self.LC_R_GLYPHS) - 10 - 52,
        }

    def __repr__(self) -> str:
        return f"LCRTokenizer(vocab_size={self.vocab_size})"


# Factory function for easy instantiation
def create_tokenizer() -> LCRTokenizer:
    """Create and return a new LC-R tokenizer instance."""
    return LCRTokenizer()


if __name__ == "__main__":
    # Quick test
    tokenizer = create_tokenizer()
    print(f"✓ Tokenizer initialized: {tokenizer}")
    print(f"✓ Vocabulary stats: {tokenizer.get_vocab_stats()}")

    # Test round-trip
    test_cases = [
        "∅",  # null
        "⊤",  # true
        "⊥",  # false
        "🜊14🜁0 42🜂",  # Contract: {14: {@0: 42}}
        "⟁ast",  # Handle: &h_ast
        "⊠68656c6c6f",  # Bytes: b"hello"
        '"Hello, World!"',  # String
        "42",  # Integer
        "3.14159",  # Float
    ]

    print("\n" + "="*60)
    print("ROUND-TRIP VERIFICATION")
    print("="*60)

    for test in test_cases:
        encoded = tokenizer.encode(test)
        decoded = tokenizer.decode(encoded)
        match = "✓" if test == decoded else "✗"
        print(f"{match} {test:20s} → {encoded[:10]}... → {decoded}")

    print(f"\n✓ Tokenizer ready for testing")
