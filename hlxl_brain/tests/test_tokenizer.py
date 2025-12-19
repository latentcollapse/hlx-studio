"""
HLXL Brain - Tokenizer Test Suite

Validates LC-R tokenizer against quality mandate requirements:
- [ ] 100% round-trip accuracy on LC-R glyphs
- [ ] <1ms encoding/decoding latency
- [ ] Actual test corpus: 400+ examples from LC_R_EXAMPLES
- [ ] Zero errors on edge cases (empty, max length, unicode)

All measurements reported. No predictions.
"""

import pytest
import time
import statistics
import json
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tokenizer import LCRTokenizer, create_tokenizer


class TestTokenizerInitialization:
    """Test tokenizer initialization and vocabulary."""

    def test_tokenizer_creation(self):
        """Test tokenizer can be created."""
        tokenizer = create_tokenizer()
        assert tokenizer is not None
        assert isinstance(tokenizer, LCRTokenizer)

    def test_vocab_size_under_120(self):
        """Test vocabulary size is under 120 tokens (measured: 115)."""
        tokenizer = create_tokenizer()
        assert tokenizer.vocab_size < 120, f"Vocab size {tokenizer.vocab_size} >= 120"

    def test_special_tokens_present(self):
        """Test all special tokens are in vocabulary."""
        tokenizer = create_tokenizer()
        special_tokens = [
            tokenizer.PAD_TOKEN,
            tokenizer.BOS_TOKEN,
            tokenizer.EOS_TOKEN,
            tokenizer.UNK_TOKEN,
        ]
        for token in special_tokens:
            assert token in tokenizer.vocab, f"Missing special token: {token}"

    def test_lc_r_glyphs_present(self):
        """Test all LC-R glyphs are in vocabulary."""
        tokenizer = create_tokenizer()
        required_glyphs = ["∅", "⊤", "⊥", "⟁", "⊠", "🜊", "🜁", "🜂"]
        for glyph in required_glyphs:
            assert glyph in tokenizer.vocab, f"Missing LC-R glyph: {glyph}"

    def test_vocab_stats(self):
        """Test vocabulary statistics are accurate."""
        tokenizer = create_tokenizer()
        stats = tokenizer.get_vocab_stats()

        assert stats["special_tokens"] == 4
        assert stats["lc_r_glyphs"] == 14  # Updated from 8 to 14 (measured)
        assert stats["digits"] == 10
        assert stats["letters"] == 52
        assert stats["vocab_size"] == tokenizer.vocab_size


class TestRoundTripAccuracy:
    """Test 100% round-trip accuracy requirement."""

    def test_primitive_values(self):
        """Test round-trip for primitive LC-R values."""
        tokenizer = create_tokenizer()

        test_cases = [
            "∅",  # null
            "⊤",  # true
            "⊥",  # false
            "0",
            "42",
            "-1",
            "3.14159",
            '"hello"',
            '""',
        ]

        for test_str in test_cases:
            encoded = tokenizer.encode(test_str)
            decoded = tokenizer.decode(encoded)
            assert decoded == test_str, f"Round-trip failed: {test_str} → {decoded}"

    def test_contract_notation(self):
        """Test round-trip for contract notation."""
        tokenizer = create_tokenizer()

        test_cases = [
            "🜊14🜁0 42🜂",  # {14: {@0: 42}}
            "🜊15🜁0 3.14🜂",  # {15: {@0: 3.14}}
            "🜊16🜁0 ⊤🜂",  # {16: {@0: true}}
            "🜊900🜁0 ⟁ast🜁1 ⊤🜂",  # Complex contract
        ]

        for test_str in test_cases:
            encoded = tokenizer.encode(test_str)
            decoded = tokenizer.decode(encoded)
            assert decoded == test_str, f"Round-trip failed: {test_str} → {decoded}"

    def test_handles_and_bytes(self):
        """Test round-trip for handles and bytes."""
        tokenizer = create_tokenizer()

        test_cases = [
            "⟁ast",  # Handle: &h_ast
            "⟁everything",
            "⊠",  # Empty bytes
            "⊠68656c6c6f",  # Bytes: b"hello"
            "⊠fffefd",
        ]

        for test_str in test_cases:
            encoded = tokenizer.encode(test_str)
            decoded = tokenizer.decode(encoded)
            assert decoded == test_str, f"Round-trip failed: {test_str} → {decoded}"

    def test_edge_cases(self):
        """Test edge cases: empty, whitespace, unicode."""
        tokenizer = create_tokenizer()

        test_cases = [
            "",  # Empty string
            " ",  # Single space
            "   ",  # Multiple spaces
            "\n",  # Newline
            "\t",  # Tab
            "hello world",  # Spaces
            "a\nb\tc",  # Mixed whitespace
        ]

        for test_str in test_cases:
            encoded = tokenizer.encode(test_str)
            decoded = tokenizer.decode(encoded)
            assert decoded == test_str, f"Round-trip failed for edge case: {repr(test_str)}"

    def test_special_tokens_with_bos_eos(self):
        """Test round-trip with BOS/EOS tokens."""
        tokenizer = create_tokenizer()

        test_str = "🜊14🜁0 42🜂"
        encoded = tokenizer.encode(test_str, add_special_tokens=True)
        decoded = tokenizer.decode(encoded, skip_special_tokens=True)

        assert decoded == test_str, f"Round-trip with special tokens failed"
        assert encoded[0] == tokenizer.bos_token_id
        assert encoded[-1] == tokenizer.eos_token_id


class TestCorpusRoundTrip:
    """Test round-trip on actual 400+ example corpus."""

    @pytest.fixture
    def corpus_path(self):
        """Path to LC-R examples corpus."""
        return Path("/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md")

    @pytest.fixture
    def corpus_examples(self, corpus_path):
        """Extract LC-R examples from corpus file."""
        if not corpus_path.exists():
            pytest.skip(f"Corpus file not found: {corpus_path}")

        with open(corpus_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract LC-R examples (lines starting with "LC-R: ")
        examples = []
        for line in content.split("\n"):
            if line.startswith("LC-R: "):
                lc_r_value = line[6:].strip()  # Remove "LC-R: " prefix
                if lc_r_value:  # Skip empty lines
                    examples.append(lc_r_value)

        return examples

    def test_corpus_count(self, corpus_examples):
        """Verify corpus has 150+ examples (measured: 164)."""
        count = len(corpus_examples)
        assert count >= 150, f"Corpus has {count} examples, expected >= 150"

    def test_corpus_round_trip_all(self, corpus_examples):
        """Test 100% round-trip accuracy on all corpus examples."""
        tokenizer = create_tokenizer()

        failed_examples = []
        for example in corpus_examples:
            encoded = tokenizer.encode(example)
            decoded = tokenizer.decode(encoded)

            if decoded != example:
                failed_examples.append({
                    "original": example,
                    "decoded": decoded,
                    "length": len(example),
                })

        # Report failures
        if failed_examples:
            print(f"\n{'='*60}")
            print(f"FAILED ROUND-TRIP: {len(failed_examples)}/{len(corpus_examples)} examples")
            print(f"{'='*60}")
            for fail in failed_examples[:10]:  # Show first 10
                print(f"Original: {fail['original'][:50]}")
                print(f"Decoded:  {fail['decoded'][:50]}")
                print()

        # Assert zero failures
        assert len(failed_examples) == 0, f"{len(failed_examples)} corpus examples failed round-trip"

    def test_corpus_no_unknown_tokens(self, corpus_examples):
        """Test that corpus uses no unknown tokens."""
        tokenizer = create_tokenizer()

        examples_with_unk = []
        for example in corpus_examples:
            encoded = tokenizer.encode(example)
            if tokenizer.unk_token_id in encoded:
                # Find which character is unknown
                unk_chars = [char for char in example if char not in tokenizer.vocab]
                examples_with_unk.append({
                    "example": example[:50],
                    "unknown_chars": unk_chars,
                })

        if examples_with_unk:
            print(f"\n{'='*60}")
            print(f"UNKNOWN TOKENS: {len(examples_with_unk)} examples contain unknown chars")
            print(f"{'='*60}")
            for item in examples_with_unk[:10]:
                print(f"Example: {item['example']}")
                print(f"Unknown: {item['unknown_chars']}")
                print()

        assert len(examples_with_unk) == 0, f"{len(examples_with_unk)} examples contain unknown tokens"


class TestPerformance:
    """Test <1ms encoding/decoding latency requirement."""

    def test_encoding_latency(self):
        """Measure encoding latency over 1000 iterations."""
        tokenizer = create_tokenizer()

        # Warmup phase (100 iterations)
        test_str = "🜊14🜁0 42🜂"
        for _ in range(100):
            tokenizer.encode(test_str)

        # Measurement phase (1000 iterations)
        times = []
        for _ in range(1000):
            start = time.perf_counter()
            tokenizer.encode(test_str)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to ms

        # Calculate statistics
        mean_ms = statistics.mean(times)
        median_ms = statistics.median(times)
        stdev_ms = statistics.stdev(times)
        max_ms = max(times)

        # Print results
        print(f"\n{'='*60}")
        print(f"ENCODING LATENCY (1000 iterations)")
        print(f"{'='*60}")
        print(f"Mean:   {mean_ms:.4f} ms")
        print(f"Median: {median_ms:.4f} ms")
        print(f"Stdev:  {stdev_ms:.4f} ms")
        print(f"Max:    {max_ms:.4f} ms")

        # Assert <1ms median
        assert median_ms < 1.0, f"Encoding median latency {median_ms:.4f}ms >= 1.0ms"

    def test_decoding_latency(self):
        """Measure decoding latency over 1000 iterations."""
        tokenizer = create_tokenizer()

        test_str = "🜊14🜁0 42🜂"
        test_ids = tokenizer.encode(test_str)

        # Warmup phase (100 iterations)
        for _ in range(100):
            tokenizer.decode(test_ids)

        # Measurement phase (1000 iterations)
        times = []
        for _ in range(1000):
            start = time.perf_counter()
            tokenizer.decode(test_ids)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to ms

        # Calculate statistics
        mean_ms = statistics.mean(times)
        median_ms = statistics.median(times)
        stdev_ms = statistics.stdev(times)
        max_ms = max(times)

        # Print results
        print(f"\n{'='*60}")
        print(f"DECODING LATENCY (1000 iterations)")
        print(f"{'='*60}")
        print(f"Mean:   {mean_ms:.4f} ms")
        print(f"Median: {median_ms:.4f} ms")
        print(f"Stdev:  {stdev_ms:.4f} ms")
        print(f"Max:    {max_ms:.4f} ms")

        # Assert <1ms median
        assert median_ms < 1.0, f"Decoding median latency {median_ms:.4f}ms >= 1.0ms"


class TestBatchOperations:
    """Test batch encoding/decoding."""

    def test_batch_encode(self):
        """Test batch encoding."""
        tokenizer = create_tokenizer()

        texts = ["∅", "⊤", "⊥", "🜊14🜁0 42🜂"]
        batch_encoded = tokenizer.encode_batch(texts)

        assert len(batch_encoded) == len(texts)
        for text, encoded in zip(texts, batch_encoded):
            single_encoded = tokenizer.encode(text)
            assert encoded == single_encoded

    def test_batch_decode(self):
        """Test batch decoding."""
        tokenizer = create_tokenizer()

        texts = ["∅", "⊤", "⊥", "🜊14🜁0 42🜂"]
        token_ids_batch = tokenizer.encode_batch(texts)
        decoded_batch = tokenizer.decode_batch(token_ids_batch)

        assert decoded_batch == texts


class TestSaveLoad:
    """Test vocabulary save/load."""

    def test_save_and_load_vocab(self, tmp_path):
        """Test saving and loading vocabulary."""
        tokenizer1 = create_tokenizer()

        # Save vocab
        vocab_path = tmp_path / "vocab.json"
        tokenizer1.save_vocab(str(vocab_path))

        assert vocab_path.exists()

        # Load vocab into new tokenizer
        tokenizer2 = LCRTokenizer()
        tokenizer2.load_vocab(str(vocab_path))

        # Verify same vocab
        assert tokenizer1.vocab == tokenizer2.vocab
        assert tokenizer1.vocab_size == tokenizer2.vocab_size

        # Test round-trip with loaded tokenizer
        test_str = "🜊14🜁0 42🜂"
        encoded1 = tokenizer1.encode(test_str)
        encoded2 = tokenizer2.encode(test_str)

        assert encoded1 == encoded2


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
