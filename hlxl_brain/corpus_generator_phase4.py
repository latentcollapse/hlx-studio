#!/usr/bin/env python3
"""
HLXL Brain - Phase 4 Corpus Generator
Generate Perfect HLX + Quality English examples.

Phase 4 Focus:
- Bidirectional English ↔ LC-R translation
- Natural, idiomatic English generation
- Multiple phrasings and style variations
- Perfect HLX family syntax (LC-R, LC-B, HLXL)

Target: 500+ examples
"""

from typing import List, Tuple
import random


class Phase4CorpusGenerator:
    """Generate Phase 4: Perfect HLX + Quality English corpus."""

    def __init__(self):
        self.examples: List[Tuple[str, str]] = []

    def generate_bidirectional_pairs(self) -> List[Tuple[str, str]]:
        """Generate bidirectional English↔LC-R pairs with variations."""
        examples = []

        # Multiple phrasings for same operation
        search_variations = [
            ("Search for documents", '🜊1000🜁0 "search"🜁1 ⟁documents🜂'),
            ("Find documents", '🜊1000🜁0 "search"🜁1 ⟁documents🜂'),
            ("Look up documents", '🜊1000🜁0 "search"🜁1 ⟁documents🜂'),
            ("Locate documents", '🜊1000🜁0 "search"🜁1 ⟁documents🜂'),
            ("Query for documents", '🜊1000🜁0 "search"🜁1 ⟁documents🜂'),
        ]
        examples.extend(search_variations)

        filter_variations = [
            ("Filter items where status is active", '🜊1000🜁0 "filter"🜁1 ⟁items🜁2 🜊1000🜁0 "eq"🜁1 ⟁status🜁2 "active"🜂🜂'),
            ("Select items with active status", '🜊1000🜁0 "filter"🜁1 ⟁items🜁2 🜊1000🜁0 "eq"🜁1 ⟁status🜁2 "active"🜂🜂'),
            ("Keep only active items", '🜊1000🜁0 "filter"🜁1 ⟁items🜁2 🜊1000🜁0 "eq"🜁1 ⟁status🜁2 "active"🜂🜂'),
            ("Show items that are active", '🜊1000🜁0 "filter"🜁1 ⟁items🜁2 🜊1000🜁0 "eq"🜁1 ⟁status🜁2 "active"🜂🜂'),
        ]
        examples.extend(filter_variations)

        transform_variations = [
            ("Convert text to uppercase", '🜊1000🜁0 "transform"🜁1 ⟁text🜁2 ⟁uppercase🜂'),
            ("Change text to uppercase", '🜊1000🜁0 "transform"🜁1 ⟁text🜁2 ⟁uppercase🜂'),
            ("Make text uppercase", '🜊1000🜁0 "transform"🜁1 ⟁text🜁2 ⟁uppercase🜂'),
            ("Transform text to uppercase", '🜊1000🜁0 "transform"🜁1 ⟁text🜁2 ⟁uppercase🜂'),
            ("Uppercase the text", '🜊1000🜁0 "transform"🜁1 ⟁text🜁2 ⟁uppercase🜂'),
        ]
        examples.extend(transform_variations)

        aggregate_variations = [
            ("Calculate the sum of values", '🜊1000🜁0 "aggregate"🜁1 ⟁sum🜁2 ⟁values🜂'),
            ("Add up all values", '🜊1000🜁0 "aggregate"🜁1 ⟁sum🜁2 ⟁values🜂'),
            ("Total the values", '🜊1000🜁0 "aggregate"🜁1 ⟁sum🜁2 ⟁values🜂'),
            ("Sum all values", '🜊1000🜁0 "aggregate"🜁1 ⟁sum🜁2 ⟁values🜂'),
            ("Compute sum of values", '🜊1000🜁0 "aggregate"🜁1 ⟁sum🜁2 ⟁values🜂'),
        ]
        examples.extend(aggregate_variations)

        navigate_variations = [
            ("Go to home directory", '🜊1000🜁0 "navigate"🜁1 ⟁home🜂'),
            ("Navigate to home", '🜊1000🜁0 "navigate"🜁1 ⟁home🜂'),
            ("Move to home directory", '🜊1000🜁0 "navigate"🜁1 ⟁home🜂'),
            ("Change to home directory", '🜊1000🜁0 "navigate"🜁1 ⟁home🜂'),
            ("Switch to home", '🜊1000🜁0 "navigate"🜁1 ⟁home🜂'),
        ]
        examples.extend(navigate_variations)

        return examples

    def generate_natural_english(self) -> List[Tuple[str, str]]:
        """Generate natural, idiomatic English descriptions."""
        examples = []

        # Conversational style
        conversational = [
            ("Let's search the database for users", '🜊1000🜁0 "search"🜁1 ⟁database🜁2 ⟁users🜂'),
            ("I need to filter out invalid records", '🜊1000🜁0 "filter"🜁1 ⟁records🜁2 🜊1000🜁0 "is_valid"🜂🜂'),
            ("Can you sort these by date?", '🜊1000🜁0 "sort"🜁1 ⟁items🜁2 ⟁date🜂'),
            ("Please aggregate the sales data", '🜊1000🜁0 "aggregate"🜁1 ⟁sales🜂'),
            ("I want to transform this to JSON", '🜊1000🜁0 "transform"🜁1 ⟁data🜁2 "json"🜂'),
        ]
        examples.extend(conversational)

        # Task-oriented
        task_oriented = [
            ("Find all files modified today", '🜊1000🜁0 "find"🜁1 ⟁files🜁2 🜊1000🜁0 "modified"🜁1 "today"🜂🜂'),
            ("Get the first 10 results", '🜊1000🜁0 "take"🜁1 10🜁2 ⟁results🜂'),
            ("Remove duplicates from the list", '🜊1000🜁0 "deduplicate"🜁1 ⟁list🜂'),
            ("Merge these two datasets", '🜊1000🜁0 "merge"🜁1 ⟁dataset1🜁2 ⟁dataset2🜂'),
            ("Export results to CSV", '🜊1000🜁0 "export"🜁1 ⟁results🜁2 "csv"🜂'),
        ]
        examples.extend(task_oriented)

        # Question format
        questions = [
            ("What's the average score?", '🜊1000🜁0 "aggregate"🜁1 ⟁mean🜁2 ⟁score🜂'),
            ("How many items are there?", '🜊1000🜁0 "count"🜁1 ⟁items🜂'),
            ("Which records match the criteria?", '🜊1000🜁0 "filter"🜁1 ⟁records🜁2 ⟁criteria🜂'),
            ("Where is the config file?", '🜊1000🜁0 "find"🜁1 "config"🜂'),
            ("When was this last updated?", '🜊1000🜁0 "get"🜁1 ⟁last_updated🜂'),
        ]
        examples.extend(questions)

        # Imperative commands
        imperatives = [
            ("Load the dataset", '🜊1000🜁0 "load"🜁1 ⟁dataset🜂'),
            ("Save to database", '🜊1000🜁0 "save"🜁1 ⟁database🜂'),
            ("Delete old records", '🜊1000🜁0 "delete"🜁1 ⟁old_records🜂'),
            ("Update user preferences", '🜊1000🜁0 "update"🜁1 ⟁user🜁2 ⟁preferences🜂'),
            ("Validate the input", '🜊1000🜁0 "validate"🜁1 ⟁input🜂'),
        ]
        examples.extend(imperatives)

        return examples

    def generate_complex_descriptions(self) -> List[Tuple[str, str]]:
        """Generate complex, detailed English descriptions."""
        examples = []

        complex_ops = [
            ("First filter active users, then sort by registration date, and finally take the top 10",
             '🜊1000🜁0 "sequence"🜁1 🜊1000🜁0 "filter"🜁1 ⟁users🜁2 🜊1000🜁0 "eq"🜁1 ⟁status🜁2 "active"🜂🜂🜁2 🜊1000🜁0 "sort"🜁1 ⟁by🜁2 ⟁registration_date🜂🜁3 🜊1000🜁0 "take"🜁1 10🜂🜂'),

            ("Search the documents collection for entries containing the keyword, excluding archived items",
             '🜊1000🜁0 "filter"🜁1 🜊1000🜁0 "search"🜁1 ⟁documents🜁2 ⟁keyword🜂🜁2 🜊1000🜁0 "not"🜁1 🜊1000🜁0 "eq"🜁1 ⟁archived🜁2 ⟁true🜂🜂🜂'),

            ("Calculate average, minimum, and maximum values from the dataset",
             '🜊1000🜁0 "map"🜁1 ["mean", "min", "max"]🜁2 🜊1000🜁0 "fn"🜁1 ⟁op🜁2 🜊1000🜁0 "aggregate"🜁1 ⟁op🜁2 ⟁dataset🜂🜂🜂'),

            ("Group records by category, then compute sum for each group, and sort by total descending",
             '🜊1000🜁0 "sequence"🜁1 🜊1000🜁0 "group_by"🜁1 ⟁category🜂🜁2 🜊1000🜁0 "map"🜁1 🜊1000🜁0 "aggregate"🜁1 ⟁sum🜂🜂🜁3 🜊1000🜁0 "sort"🜁1 ⟁desc🜂🜂'),

            ("Load data from file, validate schema, transform to normalized format, and save to output",
             '🜊1000🜁0 "pipeline"🜁1 🜊1000🜁0 "load"🜁1 ⟁file🜂🜁2 🜊1000🜁0 "validate"🜁1 ⟁schema🜂🜁3 🜊1000🜁0 "transform"🜁1 ⟁normalize🜂🜁4 🜊1000🜁0 "save"🜁1 ⟁output🜂🜂'),
        ]
        examples.extend(complex_ops)

        return examples

    def generate_style_variations(self) -> List[Tuple[str, str]]:
        """Generate same operation with different styles."""
        examples = []

        # Formal vs informal
        formal_informal = [
            ("Retrieve all documents from the database", '🜊1000🜁0 "get"🜁1 ⟁database🜁2 ⟁documents🜂'),
            ("Grab all docs from the DB", '🜊1000🜁0 "get"🜁1 ⟁database🜁2 ⟁documents🜂'),

            ("Execute a search operation on the users collection", '🜊1000🜁0 "search"🜁1 ⟁users🜂'),
            ("Look through the users", '🜊1000🜁0 "search"🜁1 ⟁users🜂'),

            ("Perform aggregation to calculate statistics", '🜊1000🜁0 "aggregate"🜁1 ⟁stats🜂'),
            ("Crunch the numbers", '🜊1000🜁0 "aggregate"🜁1 ⟁stats🜂'),
        ]
        examples.extend(formal_informal)

        # Technical vs plain
        technical_plain = [
            ("Apply a predicate filter to the dataset", '🜊1000🜁0 "filter"🜁1 ⟁dataset🜁2 ⟁predicate🜂'),
            ("Keep only items that match", '🜊1000🜁0 "filter"🜁1 ⟁dataset🜁2 ⟁predicate🜂'),

            ("Iterate over the collection and apply transformation", '🜊1000🜁0 "map"🜁1 ⟁collection🜁2 ⟁transform🜂'),
            ("Change each item in the list", '🜊1000🜁0 "map"🜁1 ⟁collection🜁2 ⟁transform🜂'),
        ]
        examples.extend(technical_plain)

        return examples

    def generate_reverse_pairs(self) -> List[Tuple[str, str]]:
        """Generate LC-R → English (reverse direction)."""
        examples = []

        reverse = [
            ('🜊1000🜁0 "search"🜁1 ⟁database🜂', "Search the database"),
            ('🜊1000🜁0 "filter"🜁1 ⟁items🜁2 ⟁condition🜂', "Filter items by condition"),
            ('🜊1000🜁0 "aggregate"🜁1 ⟁sum🜁2 ⟁values🜂', "Sum all values"),
            ('🜊1000🜁0 "sort"🜁1 ⟁data🜁2 ⟁asc🜂', "Sort data in ascending order"),
            ('🜊1000🜁0 "map"🜁1 ⟁list🜁2 ⟁fn🜂', "Apply function to each element in list"),
            ('🜊1000🜁0 "reduce"🜁1 ⟁list🜁2 ⟁fn🜁3 ⟁init🜂', "Reduce list using function with initial value"),
            ('🜊1000🜁0 "take"🜁1 10🜁2 ⟁items🜂', "Take first 10 items"),
            ('🜊1000🜁0 "skip"🜁1 5🜁2 ⟁items🜂', "Skip first 5 items"),
            ('🜊1000🜁0 "count"🜁1 ⟁items🜂', "Count number of items"),
            ('🜊1000🜁0 "distinct"🜁1 ⟁list🜂', "Get unique items from list"),
        ]
        examples.extend(reverse)

        return examples

    def generate_contextual_variations(self) -> List[Tuple[str, str]]:
        """Generate variations based on context/domain."""
        examples = []

        # Data science context
        data_science = [
            ("Train the model on the dataset", '🜊1000🜁0 "train"🜁1 ⟁model🜁2 ⟁dataset🜂'),
            ("Evaluate model performance", '🜊1000🜁0 "evaluate"🜁1 ⟁model🜂'),
            ("Split data into train and test sets", '🜊1000🜁0 "split"🜁1 ⟁data🜁2 0.8🜂'),
            ("Normalize features", '🜊1000🜁0 "normalize"🜁1 ⟁features🜂'),
            ("Detect outliers in the data", '🜊1000🜁0 "detect"🜁1 ⟁outliers🜁2 ⟁data🜂'),
        ]
        examples.extend(data_science)

        # Web/API context
        web_api = [
            ("Fetch data from API endpoint", '🜊1000🜁0 "fetch"🜁1 ⟁api🜁2 ⟁endpoint🜂'),
            ("Post JSON to server", '🜊1000🜁0 "post"🜁1 ⟁server🜁2 ⟁json🜂'),
            ("Parse response body", '🜊1000🜁0 "parse"🜁1 ⟁response🜁2 "json"🜂'),
            ("Set request headers", '🜊1000🜁0 "set"🜁1 ⟁headers🜁2 ⟁values🜂'),
            ("Handle error response", '🜊1000🜁0 "handle"🜁1 ⟁error🜁2 ⟁response🜂'),
        ]
        examples.extend(web_api)

        # File system context
        file_system = [
            ("Read file contents", '🜊1000🜁0 "read"🜁1 ⟁file🜂'),
            ("Write data to file", '🜊1000🜁0 "write"🜁1 ⟁file🜁2 ⟁data🜂'),
            ("List directory contents", '🜊1000🜁0 "list"🜁1 ⟁directory🜂'),
            ("Create new directory", '🜊1000🜁0 "mkdir"🜁1 ⟁path🜂'),
            ("Delete file or directory", '🜊1000🜁0 "delete"🜁1 ⟁path🜂'),
        ]
        examples.extend(file_system)

        # Database context
        database = [
            ("Query database table", '🜊1000🜁0 "query"🜁1 ⟁table🜂'),
            ("Insert new record", '🜊1000🜁0 "insert"🜁1 ⟁table🜁2 ⟁record🜂'),
            ("Update existing record", '🜊1000🜁0 "update"🜁1 ⟁table🜁2 ⟁record🜂'),
            ("Delete record by ID", '🜊1000🜁0 "delete"🜁1 ⟁table🜁2 ⟁id🜂'),
            ("Join two tables", '🜊1000🜁0 "join"🜁1 ⟁table1🜁2 ⟁table2🜂'),
        ]
        examples.extend(database)

        return examples

    def generate_all(self) -> List[Tuple[str, str]]:
        """Generate all Phase 4 examples."""
        print("Generating Phase 4 corpus...")

        self.examples = []

        bidirectional = self.generate_bidirectional_pairs()
        self.examples.extend(bidirectional)
        print(f"  ✓ Bidirectional pairs: {len(bidirectional)} examples")

        natural = self.generate_natural_english()
        self.examples.extend(natural)
        print(f"  ✓ Natural English: {len(natural)} examples")

        complex_desc = self.generate_complex_descriptions()
        self.examples.extend(complex_desc)
        print(f"  ✓ Complex descriptions: {len(complex_desc)} examples")

        style_vars = self.generate_style_variations()
        self.examples.extend(style_vars)
        print(f"  ✓ Style variations: {len(style_vars)} examples")

        reverse = self.generate_reverse_pairs()
        self.examples.extend(reverse)
        print(f"  ✓ Reverse pairs (LC-R→English): {len(reverse)} examples")

        contextual = self.generate_contextual_variations()
        self.examples.extend(contextual)
        print(f"  ✓ Contextual variations: {len(contextual)} examples")

        print(f"\nTotal Phase 4 examples: {len(self.examples)}")
        return self.examples

    def write_corpus(self, filename: str):
        """Write corpus to markdown file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# HLXL Brain - Phase 4: Perfect HLX + Quality English Corpus\n\n")
            f.write("## Training Examples for Bidirectional Translation and Natural Language\n\n")
            f.write(f"Total examples: {len(self.examples)}\n\n")
            f.write("---\n\n")

            for i, (english, lcr) in enumerate(self.examples, 1):
                f.write(f"### Example {i}\n\n")
                f.write(f"**English:**\n{english}\n\n")
                f.write(f"**LC-R:**\n```\n{lcr}\n```\n\n")
                f.write("---\n\n")

        print(f"✓ Corpus written to {filename}")


if __name__ == "__main__":
    generator = Phase4CorpusGenerator()
    examples = generator.generate_all()
    generator.write_corpus("corpus_phase4_perfect_hlx_english.md")
    print("\nPhase 4 corpus generation complete!")
    print(f"Generated {len(examples)} examples")
    print("\nNext steps:")
    print("1. Review corpus_phase4_perfect_hlx_english.md")
    print("2. Merge with previous phases: cat corpus_combined_phase3.md corpus_phase4_perfect_hlx_english.md > corpus_combined_phase4.md")
    print("3. Update training script for Phase 4")
    print("4. Run: python3 train_phase4.py")
