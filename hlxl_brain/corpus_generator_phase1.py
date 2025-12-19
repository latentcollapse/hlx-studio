#!/usr/bin/env python3
"""
Phase 1 Corpus Generator: Semantic Grounding
Generates 500+ training examples teaching operations with meaning
"""

import random
from typing import List, Tuple

# Seed for reproducibility
random.seed(42)

class Phase1CorpusGenerator:
    """Generate semantic grounding examples: English → LC-R pairs"""

    def __init__(self):
        self.operations = self._define_operations()
        self.examples = []

    def _define_operations(self) -> dict:
        """Define operations with semantic templates"""
        return {
            # Navigation & Movement
            "navigate": {
                "args": ["location"],
                "templates": [
                    ("Navigate to {0}", "🜊1000🜁0 \"navigate\"🜁1 ⟁{0}🜂"),
                    ("Go to {0}", "🜊1000🜁0 \"navigate\"🜁1 ⟁{0}🜂"),
                    ("Move to {0}", "🜊1000🜁0 \"navigate\"🜁1 ⟁{0}🜂"),
                ],
                "locations": ["home", "docs", "downloads", "desktop", "root", "parent", "workspace", "project"]
            },

            # Search & Query
            "search": {
                "args": ["target", "query"],
                "templates": [
                    ("Search {0} for {1}", "🜊1000🜁0 \"search\"🜁1 ⟁{0}🜁2 \"{1}\"🜂"),
                    ("Find {1} in {0}", "🜊1000🜁0 \"search\"🜁1 ⟁{0}🜁2 \"{1}\"🜂"),
                    ("Look for {1} in {0}", "🜊1000🜁0 \"search\"🜁1 ⟁{0}🜁2 \"{1}\"🜂"),
                ],
                "targets": ["files", "database", "logs", "documents", "code", "memory", "cache"],
                "queries": ["error", "test", "config", "data", "user", "admin", "log", "debug"]
            },

            # Filtering & Selection
            "filter": {
                "args": ["data", "condition"],
                "templates": [
                    ("Filter {0} where {1}", "🜊1000🜁0 \"filter\"🜁1 ⟁{0}🜁2 ⟁{1}🜂"),
                    ("Select from {0} where {1}", "🜊1000🜁0 \"filter\"🜁1 ⟁{0}🜁2 ⟁{1}🜂"),
                    ("Keep items from {0} that match {1}", "🜊1000🜁0 \"filter\"🜁1 ⟁{0}🜁2 ⟁{1}🜂"),
                ],
                "data": ["records", "entries", "items", "rows", "documents", "objects"],
                "conditions": ["valid", "active", "recent", "pending", "complete", "failed"]
            },

            # Transformation
            "transform": {
                "args": ["input", "operation"],
                "templates": [
                    ("Transform {0} using {1}", "🜊1000🜁0 \"transform\"🜁1 ⟁{0}🜁2 ⟁{1}🜂"),
                    ("Convert {0} to {1}", "🜊1000🜁0 \"transform\"🜁1 ⟁{0}🜁2 ⟁{1}🜂"),
                    ("Apply {1} to {0}", "🜊1000🜁0 \"transform\"🜁1 ⟁{0}🜁2 ⟁{1}🜂"),
                ],
                "inputs": ["text", "data", "image", "audio", "format", "structure"],
                "operations": ["uppercase", "lowercase", "normalize", "sanitize", "encode", "decode", "compress"]
            },

            # Aggregation
            "aggregate": {
                "args": ["operation", "field"],
                "templates": [
                    ("Calculate {0} of {1}", "🜊1000🜁0 \"aggregate\"🜁1 ⟁{0}🜁2 ⟁{1}🜂"),
                    ("Compute {0} for {1}", "🜊1000🜁0 \"aggregate\"🜁1 ⟁{0}🜁2 ⟁{1}🜂"),
                    ("Get {0} of {1}", "🜊1000🜁0 \"aggregate\"🜁1 ⟁{0}🜁2 ⟁{1}🜂"),
                ],
                "operations": ["sum", "average", "count", "min", "max", "median", "total"],
                "fields": ["value", "score", "count", "price", "quantity", "weight", "size"]
            },

            # Data Operations - Read
            "read": {
                "args": ["source"],
                "templates": [
                    ("Read from {0}", "🜊1000🜁0 \"read\"🜁1 \"{0}\"🜂"),
                    ("Load {0}", "🜊1000🜁0 \"read\"🜁1 \"{0}\"🜂"),
                    ("Open {0}", "🜊1000🜁0 \"read\"🜁1 \"{0}\"🜂"),
                ],
                "sources": ["data.json", "config.yaml", "users.csv", "log.txt", "database", "cache", "file.dat"]
            },

            # Data Operations - Write
            "write": {
                "args": ["destination", "content"],
                "templates": [
                    ("Write {1} to {0}", "🜊1000🜁0 \"write\"🜁1 \"{0}\"🜁2 ⟁{1}🜂"),
                    ("Save {1} to {0}", "🜊1000🜁0 \"write\"🜁1 \"{0}\"🜁2 ⟁{1}🜂"),
                    ("Store {1} in {0}", "🜊1000🜁0 \"write\"🜁1 \"{0}\"🜁2 ⟁{1}🜂"),
                ],
                "destinations": ["output.json", "results.txt", "data.csv", "log.txt", "cache", "database"],
                "contents": ["data", "results", "output", "logs", "metrics", "config"]
            },

            # Computational
            "compute": {
                "args": ["expression"],
                "templates": [
                    ("Compute {0}", "🜊1000🜁0 \"compute\"🜁1 ⟁{0}🜂"),
                    ("Calculate {0}", "🜊1000🜁0 \"compute\"🜁1 ⟁{0}🜂"),
                    ("Evaluate {0}", "🜊1000🜁0 \"compute\"🜁1 ⟁{0}🜂"),
                ],
                "expressions": ["result", "metric", "score", "value", "total", "difference", "ratio"]
            },

            # Validation
            "validate": {
                "args": ["data", "schema"],
                "templates": [
                    ("Validate {0} against {1}", "🜊1000🜁0 \"validate\"🜁1 ⟁{0}🜁2 ⟁{1}🜂"),
                    ("Check {0} using {1}", "🜊1000🜁0 \"validate\"🜁1 ⟁{0}🜁2 ⟁{1}🜂"),
                    ("Verify {0} matches {1}", "🜊1000🜁0 \"validate\"🜁1 ⟁{0}🜁2 ⟁{1}🜂"),
                ],
                "data": ["input", "data", "config", "schema", "format"],
                "schemas": ["schema", "spec", "definition", "contract", "rules"]
            },

            # Execution
            "execute": {
                "args": ["command"],
                "templates": [
                    ("Execute {0}", "🜊1000🜁0 \"execute\"🜁1 ⟁{0}🜂"),
                    ("Run {0}", "🜊1000🜁0 \"execute\"🜁1 ⟁{0}🜂"),
                    ("Perform {0}", "🜊1000🜁0 \"execute\"🜁1 ⟁{0}🜂"),
                ],
                "commands": ["command", "task", "job", "operation", "action", "process"]
            },
        }

    def generate_basic_operations(self) -> List[Tuple[str, str]]:
        """Generate examples for each operation type"""
        examples = []

        for op_name, op_config in self.operations.items():
            templates = op_config["templates"]

            # Generate examples for each template
            for template_english, template_lcr in templates:
                # Get appropriate value lists
                if op_name == "navigate":
                    for loc in op_config["locations"]:
                        english = template_english.format(loc)
                        lcr = template_lcr.format(loc)
                        examples.append((english, lcr))

                elif op_name == "search":
                    for target in op_config["targets"]:
                        for query in op_config["queries"][:3]:  # Limit combinations
                            english = template_english.format(target, query)
                            lcr = template_lcr.format(target, query)
                            examples.append((english, lcr))

                elif op_name == "filter":
                    for data in op_config["data"]:
                        for cond in op_config["conditions"][:3]:
                            english = template_english.format(data, cond)
                            lcr = template_lcr.format(data, cond)
                            examples.append((english, lcr))

                elif op_name == "transform":
                    for inp in op_config["inputs"]:
                        for oper in op_config["operations"][:3]:
                            english = template_english.format(inp, oper)
                            lcr = template_lcr.format(inp, oper)
                            examples.append((english, lcr))

                elif op_name == "aggregate":
                    for oper in op_config["operations"]:
                        for field in op_config["fields"][:3]:
                            english = template_english.format(oper, field)
                            lcr = template_lcr.format(oper, field)
                            examples.append((english, lcr))

                elif op_name == "read":
                    for source in op_config["sources"]:
                        english = template_english.format(source)
                        lcr = template_lcr.format(source)
                        examples.append((english, lcr))

                elif op_name == "write":
                    for dest in op_config["destinations"]:
                        for content in op_config["contents"][:2]:
                            english = template_english.format(dest, content)
                            lcr = template_lcr.format(dest, content)
                            examples.append((english, lcr))

                elif op_name == "compute":
                    for expr in op_config["expressions"]:
                        english = template_english.format(expr)
                        lcr = template_lcr.format(expr)
                        examples.append((english, lcr))

                elif op_name == "validate":
                    for data in op_config["data"]:
                        for schema in op_config["schemas"][:2]:
                            english = template_english.format(data, schema)
                            lcr = template_lcr.format(data, schema)
                            examples.append((english, lcr))

                elif op_name == "execute":
                    for cmd in op_config["commands"]:
                        english = template_english.format(cmd)
                        lcr = template_lcr.format(cmd)
                        examples.append((english, lcr))

        return examples

    def generate_composite_operations(self) -> List[Tuple[str, str]]:
        """Generate examples with multiple operations combined"""
        examples = []

        # Pattern: Read → Transform → Write
        examples.extend([
            ("Load data.json, normalize it, and save to output.json",
             "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"read\"🜁1 \"data.json\"🜂🜁1 🜊1000🜁0 \"transform\"🜁1 ⟁data🜁2 ⟁normalize🜂🜁2 🜊1000🜁0 \"write\"🜁1 \"output.json\"🜁2 ⟁result🜂🜂🜂"),

            ("Read config.yaml, validate against schema, and save if valid",
             "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"read\"🜁1 \"config.yaml\"🜂🜁1 🜊1000🜁0 \"validate\"🜁1 ⟁config🜁2 ⟁schema🜂🜁2 🜊1000🜁0 \"write\"🜁1 \"validated.yaml\"🜁2 ⟁config🜂🜂🜂"),
        ])

        # Pattern: Search → Filter → Aggregate
        examples.extend([
            ("Search logs for errors, filter recent ones, and count them",
             "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"search\"🜁1 ⟁logs🜁2 \"error\"🜂🜁1 🜊1000🜁0 \"filter\"🜁1 ⟁results🜁2 ⟁recent🜂🜁2 🜊1000🜁0 \"aggregate\"🜁1 ⟁count🜁2 ⟁total🜂🜂🜂"),

            ("Find documents containing 'test', filter by date, and compute average size",
             "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"search\"🜁1 ⟁documents🜁2 \"test\"🜂🜁1 🜊1000🜁0 \"filter\"🜁1 ⟁results🜁2 ⟁recent🜂🜁2 🜊1000🜁0 \"aggregate\"🜁1 ⟁average🜁2 ⟁size🜂🜂🜂"),
        ])

        return examples

    def generate_corpus(self) -> str:
        """Generate complete Phase 1 corpus"""
        basic = self.generate_basic_operations()
        composite = self.generate_composite_operations()

        all_examples = basic + composite
        random.shuffle(all_examples)

        # Format as markdown
        corpus = "# Phase 1: Semantic Grounding Corpus\n\n"
        corpus += f"Total examples: {len(all_examples)}\n\n"
        corpus += "---\n\n"

        for english, lcr in all_examples:
            corpus += f"English: {english}\n"
            corpus += f"LC-R: {lcr}\n\n"

        return corpus, len(all_examples)


if __name__ == "__main__":
    print("Generating Phase 1 corpus...")
    generator = Phase1CorpusGenerator()
    corpus, count = generator.generate_corpus()

    # Write to file
    output_file = "corpus_phase1_semantic_grounding.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(corpus)

    print(f"✓ Generated {count} examples")
    print(f"✓ Saved to {output_file}")
    print(f"\nSample examples:")

    examples = corpus.split("\n\n")[2:7]  # Get first few
    for ex in examples:
        if ex.strip():
            print(f"  {ex[:100]}...")
