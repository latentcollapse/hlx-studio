#!/usr/bin/env python3
"""
Phase 2 Corpus Generator: Domain Knowledge
Generates 600+ training examples teaching domain-specific patterns
"""

import random
from typing import List, Tuple

# Seed for reproducibility
random.seed(42)

class Phase2CorpusGenerator:
    """Generate domain knowledge examples: File systems, data structures, control flow"""

    def __init__(self):
        self.examples = []

    def generate_file_system_operations(self) -> List[Tuple[str, str]]:
        """Generate file system operation examples"""
        examples = []

        # Path operations
        paths = [
            ("/home/user/docs", "🜊1000🜁0 \"navigate\"🜁1 \"/home/user/docs\"🜂"),
            ("./relative/path", "🜊1000🜁0 \"navigate\"🜁1 \"./relative/path\"🜂"),
            ("../parent/folder", "🜊1000🜁0 \"navigate\"🜁1 \"../parent/folder\"🜂"),
            ("/root/system", "🜊1000🜁0 \"navigate\"🜁1 \"/root/system\"🜂"),
        ]

        for path, lcr in paths:
            examples.append((f"Navigate to {path}", lcr))
            examples.append((f"Go to {path}", lcr))
            examples.append((f"Change to {path}", lcr))

        # Wildcard patterns
        wildcards = [
            ("*.txt", "all text files", "🜊1000🜁0 \"find\"🜁1 \"*.txt\"🜂"),
            ("**/*.py", "all Python files recursively", "🜊1000🜁0 \"find\"🜁1 \"**/*.py\"🜂"),
            ("data/*.json", "JSON files in data folder", "🜊1000🜁0 \"find\"🜁1 \"data/*.json\"🜂"),
            ("test_*.js", "test JavaScript files", "🜊1000🜁0 \"find\"🜁1 \"test_*.js\"🜂"),
            ("{a,b,c}.csv", "files a.csv, b.csv, c.csv", "🜊1000🜁0 \"find\"🜁1 \"{a,b,c}.csv\"🜂"),
        ]

        for pattern, desc, lcr in wildcards:
            examples.append((f"Find {pattern}", lcr))
            examples.append((f"Search for {pattern}", lcr))
            examples.append((f"Locate {desc}", lcr))

        # File operations
        file_ops = [
            ("Read config.yaml", "🜊1000🜁0 \"read\"🜁1 \"config.yaml\"🜂"),
            ("Write to output.txt", "🜊1000🜁0 \"write\"🜁1 \"output.txt\"🜁2 ⟁data🜂"),
            ("Copy file.txt to backup.txt", "🜊1000🜁0 \"copy\"🜁1 \"file.txt\"🜁2 \"backup.txt\"🜂"),
            ("Move temp.log to archive.log", "🜊1000🜁0 \"move\"🜁1 \"temp.log\"🜁2 \"archive.log\"🜂"),
            ("Delete old.dat", "🜊1000🜁0 \"delete\"🜁1 \"old.dat\"🜂"),
            ("Rename draft.md to final.md", "🜊1000🜁0 \"rename\"🜁1 \"draft.md\"🜁2 \"final.md\"🜂"),
        ]

        examples.extend(file_ops)

        # Directory operations
        dir_ops = [
            ("Create directory logs", "🜊1000🜁0 \"mkdir\"🜁1 \"logs\"🜂"),
            ("List files in current directory", "🜊1000🜁0 \"ls\"🜁1 \".\"🜂"),
            ("List all files recursively", "🜊1000🜁0 \"ls\"🜁1 \"-R\"🜂"),
            ("Remove empty directory cache", "🜊1000🜁0 \"rmdir\"🜁1 \"cache\"🜂"),
        ]

        examples.extend(dir_ops)

        return examples

    def generate_data_structure_operations(self) -> List[Tuple[str, str]]:
        """Generate data structure examples"""
        examples = []

        # List operations
        list_ops = [
            ("Create empty list", "🜊14🜂"),
            ("Create list with values 1, 2, 3", "🜊14🜁0 1🜁1 2🜁2 3🜂"),
            ("Get first element from list", "🜊1000🜁0 \"get\"🜁1 ⟁list🜁2 0🜂"),
            ("Get last element from list", "🜊1000🜁0 \"get\"🜁1 ⟁list🜁2 -1🜂"),
            ("Append value to list", "🜊1000🜁0 \"append\"🜁1 ⟁list🜁2 ⟁value🜂"),
            ("Prepend value to list", "🜊1000🜁0 \"prepend\"🜁1 ⟁list🜁2 ⟁value🜂"),
            ("Get length of list", "🜊1000🜁0 \"length\"🜁1 ⟁list🜂"),
            ("Slice list from index 1 to 5", "🜊1000🜁0 \"slice\"🜁1 ⟁list🜁2 1🜁3 5🜂"),
            ("Reverse the list", "🜊1000🜁0 \"reverse\"🜁1 ⟁list🜂"),
            ("Sort the list", "🜊1000🜁0 \"sort\"🜁1 ⟁list🜂"),
        ]

        examples.extend(list_ops)

        # Map operations
        map_ops = [
            ("Create empty map", "🜊15🜂"),
            ("Get value for key from map", "🜊1000🜁0 \"get\"🜁1 ⟁map🜁2 \"key\"🜂"),
            ("Set key to value in map", "🜊1000🜁0 \"set\"🜁1 ⟁map🜁2 \"key\"🜁3 ⟁value🜂"),
            ("Check if map has key", "🜊1000🜁0 \"has\"🜁1 ⟁map🜁2 \"key\"🜂"),
            ("Remove key from map", "🜊1000🜁0 \"remove\"🜁1 ⟁map🜁2 \"key\"🜂"),
            ("Get all keys from map", "🜊1000🜁0 \"keys\"🜁1 ⟁map🜂"),
            ("Get all values from map", "🜊1000🜁0 \"values\"🜁1 ⟁map🜂"),
            ("Merge map1 with map2", "🜊1000🜁0 \"merge\"🜁1 ⟁map1🜁2 ⟁map2🜂"),
        ]

        examples.extend(map_ops)

        # Set operations
        set_ops = [
            ("Create set from values a, b, c", "🜊1000🜁0 \"set\"🜁1 🜊14🜁0 ⟁a🜁1 ⟁b🜁2 ⟁c🜂🜂"),
            ("Add element to set", "🜊1000🜁0 \"add\"🜁1 ⟁set🜁2 ⟁element🜂"),
            ("Check if set contains element", "🜊1000🜁0 \"contains\"🜁1 ⟁set🜁2 ⟁element🜂"),
            ("Get union of set1 and set2", "🜊1000🜁0 \"union\"🜁1 ⟁set1🜁2 ⟁set2🜂"),
            ("Get intersection of set1 and set2", "🜊1000🜁0 \"intersection\"🜁1 ⟁set1🜁2 ⟁set2🜂"),
            ("Get difference of set1 and set2", "🜊1000🜁0 \"difference\"🜁1 ⟁set1🜁2 ⟁set2🜂"),
        ]

        examples.extend(set_ops)

        # Type conversions
        conversions = [
            ("Convert list to set", "🜊1000🜁0 \"to_set\"🜁1 ⟁list🜂"),
            ("Convert set to list", "🜊1000🜁0 \"to_list\"🜁1 ⟁set🜂"),
            ("Convert string to number", "🜊1000🜁0 \"to_number\"🜁1 \"42\"🜂"),
            ("Convert number to string", "🜊1000🜁0 \"to_string\"🜁1 42🜂"),
        ]

        examples.extend(conversions)

        return examples

    def generate_control_flow_operations(self) -> List[Tuple[str, str]]:
        """Generate control flow examples"""
        examples = []

        # Conditionals
        conditionals = [
            ("If condition then action",
             "🜊1000🜁0 \"if\"🜁1 ⟁condition🜁2 🜊1000🜁0 \"action\"🜂🜂"),
            ("If x greater than 10 then process",
             "🜊1000🜁0 \"if\"🜁1 🜊1000🜁0 \"gt\"🜁1 ⟁x🜁2 10🜂🜁2 🜊1000🜁0 \"process\"🜂🜂"),
            ("If valid then accept else reject",
             "🜊1000🜁0 \"if\"🜁1 ⟁valid🜁2 🜊1000🜁0 \"accept\"🜂🜁3 🜊1000🜁0 \"reject\"🜂🜂"),
            ("Match value with cases",
             "🜊1000🜁0 \"match\"🜁1 ⟁value🜁2 🜊15🜁0 \"case1\"🜁1 🜊1000🜁0 \"action1\"🜂🜁2 \"case2\"🜁3 🜊1000🜁0 \"action2\"🜂🜂🜂"),
        ]

        examples.extend(conditionals)

        # Loops
        loops = [
            ("For each item in list do process",
             "🜊1000🜁0 \"for_each\"🜁1 ⟁list🜁2 🜊1000🜁0 \"process\"🜁1 ⟁item🜂🜂"),
            ("While condition do action",
             "🜊1000🜁0 \"while\"🜁1 ⟁condition🜁2 🜊1000🜁0 \"action\"🜂🜂"),
            ("Repeat action 5 times",
             "🜊1000🜁0 \"repeat\"🜁1 5🜁2 🜊1000🜁0 \"action\"🜂🜂"),
            ("Iterate from 0 to 10",
             "🜊1000🜁0 \"iterate\"🜁1 0🜁2 10🜁3 🜊1000🜁0 \"process\"🜁1 ⟁i🜂🜂"),
        ]

        examples.extend(loops)

        # Pipelines
        pipelines = [
            ("Load data then filter then save",
             "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"load\"🜁1 \"data.json\"🜂🜁1 🜊1000🜁0 \"filter\"🜁1 ⟁data🜁2 ⟁valid🜂🜁2 🜊1000🜁0 \"save\"🜁1 \"output.json\"🜁2 ⟁result🜂🜂🜂"),
            ("Read, transform, validate, write",
             "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"read\"🜁1 \"input.txt\"🜂🜁1 🜊1000🜁0 \"transform\"🜁1 ⟁data🜁2 ⟁normalize🜂🜁2 🜊1000🜁0 \"validate\"🜁1 ⟁result🜁2 ⟁schema🜂🜁3 🜊1000🜁0 \"write\"🜁1 \"output.txt\"🜁2 ⟁validated🜂🜂🜂"),
            ("Search then sort then limit",
             "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"search\"🜁1 ⟁database🜁2 \"query\"🜂🜁1 🜊1000🜁0 \"sort\"🜁1 ⟁results🜁2 ⟁desc🜂🜁2 🜊1000🜁0 \"limit\"🜁1 ⟁sorted🜁2 10🜂🜂🜂"),
        ]

        examples.extend(pipelines)

        # Error handling
        error_handling = [
            ("Try operation catch error",
             "🜊1000🜁0 \"try\"🜁1 🜊1000🜁0 \"operation\"🜂🜁2 🜊1000🜁0 \"catch\"🜁1 ⟁error🜂🜂"),
            ("Validate input or use default",
             "🜊1000🜁0 \"or\"🜁1 🜊1000🜁0 \"validate\"🜁1 ⟁input🜂🜁2 ⟁default🜂"),
            ("Execute with timeout",
             "🜊1000🜁0 \"timeout\"🜁1 🜊1000🜁0 \"execute\"🜁1 ⟁task🜂🜁2 5000🜂"),
        ]

        examples.extend(error_handling)

        return examples

    def generate_common_patterns(self) -> List[Tuple[str, str]]:
        """Generate common programming patterns"""
        examples = []

        # Map-Reduce
        examples.append((
            "Map transform over list then reduce with sum",
            "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"map\"🜁1 ⟁list🜁2 🜊1000🜁0 \"transform\"🜁1 ⟁item🜂🜂🜁1 🜊1000🜁0 \"reduce\"🜁1 ⟁mapped🜁2 🜊1000🜁0 \"sum\"🜂🜂🜂"
        ))

        # Filter-Map-Reduce
        examples.append((
            "Filter valid items, map to values, sum results",
            "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"filter\"🜁1 ⟁items🜁2 ⟁valid🜂🜁1 🜊1000🜁0 \"map\"🜁1 ⟁filtered🜁2 ⟁get_value🜂🜁2 🜊1000🜁0 \"sum\"🜁1 ⟁values🜂🜂🜂"
        ))

        # Load-Process-Save
        examples.append((
            "Load CSV, filter rows, aggregate by group, save results",
            "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"load\"🜁1 \"data.csv\"🜁2 \"csv\"🜂🜁1 🜊1000🜁0 \"filter\"🜁1 ⟁rows🜁2 🜊1000🜁0 \"gt\"🜁1 ⟁score🜁2 80🜂🜂🜁2 🜊1000🜁0 \"group_by\"🜁1 ⟁filtered🜁2 \"category\"🜂🜁3 🜊1000🜁0 \"save\"🜁1 \"results.json\"🜁2 ⟁grouped🜂🜂🜂"
        ))

        # Query-Transform-Export
        examples.append((
            "Query database, transform records, export to multiple formats",
            "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"query\"🜁1 ⟁database🜁2 \"SELECT * FROM users\"🜂🜁1 🜊1000🜁0 \"transform\"🜁1 ⟁records🜁2 ⟁normalize🜂🜁2 🜊1000🜁0 \"export\"🜁1 ⟁transformed🜁2 🜊14🜁0 \"json\"🜁1 \"csv\"🜁2 \"xml\"🜂🜂🜂🜂"
        ))

        # Parallel processing
        examples.append((
            "Process items in parallel with 4 workers",
            "🜊1000🜁0 \"parallel\"🜁1 ⟁items🜁2 🜊1000🜁0 \"process\"🜁1 ⟁item🜂🜁3 4🜂"
        ))

        # Caching
        examples.append((
            "Execute with cache for 3600 seconds",
            "🜊1000🜁0 \"cache\"🜁1 🜊1000🜁0 \"execute\"🜁1 ⟁task🜂🜁2 3600🜂"
        ))

        # Batch processing
        examples.append((
            "Process items in batches of 100",
            "🜊1000🜁0 \"batch\"🜁1 ⟁items🜁2 100🜁3 🜊1000🜁0 \"process\"🜁1 ⟁batch🜂🜂"
        ))

        return examples

    def generate_realistic_workflows(self) -> List[Tuple[str, str]]:
        """Generate realistic multi-step workflows"""
        examples = []

        # Data ETL
        examples.append((
            "Extract data from API, transform to schema, load into database",
            "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"fetch\"🜁1 \"https://api.example.com/data\"🜂🜁1 🜊1000🜁0 \"transform\"🜁1 ⟁data🜁2 ⟁to_schema🜂🜁2 🜊1000🜁0 \"insert\"🜁1 ⟁database🜁2 ⟁transformed🜂🜂🜂"
        ))

        # File processing
        examples.append((
            "Find all log files, parse errors, group by type, generate report",
            "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"find\"🜁1 \"**/*.log\"🜂🜁1 🜊1000🜁0 \"map\"🜁1 ⟁files🜁2 🜊1000🜁0 \"parse_errors\"🜁1 ⟁file🜂🜂🜁2 🜊1000🜁0 \"group_by\"🜁1 ⟁errors🜁2 \"type\"🜂🜁3 🜊1000🜁0 \"generate_report\"🜁1 ⟁grouped🜂🜂🜂"
        ))

        # Data analysis
        examples.append((
            "Load sales data, filter by date range, calculate metrics, create visualization",
            "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"load\"🜁1 \"sales.csv\"🜂🜁1 🜊1000🜁0 \"filter\"🜁1 ⟁data🜁2 🜊1000🜁0 \"between\"🜁1 ⟁date🜁2 \"2024-01-01\"🜁3 \"2024-12-31\"🜂🜂🜁2 🜊1000🜁0 \"aggregate\"🜁1 ⟁filtered🜁2 🜊15🜁0 \"total\"🜁1 ⟁sum🜁2 \"average\"🜁3 ⟁mean🜂🜂🜁3 🜊1000🜁0 \"visualize\"🜁1 ⟁metrics🜁2 \"chart\"🜂🜂🜂"
        ))

        # API workflow
        examples.append((
            "Authenticate with API, fetch user data, enrich with profile, cache results",
            "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"authenticate\"🜁1 \"api.example.com\"🜁2 ⟁credentials🜂🜁1 🜊1000🜁0 \"fetch\"🜁1 \"/users\"🜁2 ⟁token🜂🜁2 🜊1000🜁0 \"enrich\"🜁1 ⟁users🜁2 ⟁get_profile🜂🜁3 🜊1000🜁0 \"cache\"🜁1 ⟁enriched🜁2 3600🜂🜂🜂"
        ))

        # Validation workflow
        examples.append((
            "Read config, validate schema, check permissions, apply settings",
            "🜊1000🜁0 \"pipeline\"🜁1 🜊14🜁0 🜊1000🜁0 \"read\"🜁1 \"config.yaml\"🜂🜁1 🜊1000🜁0 \"validate\"🜁1 ⟁config🜁2 ⟁schema🜂🜁2 🜊1000🜁0 \"check_permissions\"🜁1 ⟁validated🜂🜁3 🜊1000🜁0 \"apply\"🜁1 ⟁settings🜂🜂🜂"
        ))

        return examples

    def generate_corpus(self) -> Tuple[str, int]:
        """Generate complete Phase 2 corpus"""
        file_system = self.generate_file_system_operations()
        data_structures = self.generate_data_structure_operations()
        control_flow = self.generate_control_flow_operations()
        patterns = self.generate_common_patterns()
        workflows = self.generate_realistic_workflows()

        all_examples = (
            file_system +
            data_structures +
            control_flow +
            patterns +
            workflows
        )

        random.shuffle(all_examples)

        # Format as markdown
        corpus = "# Phase 2: Domain Knowledge Corpus\n\n"
        corpus += f"Total examples: {len(all_examples)}\n\n"
        corpus += "**Coverage:**\n"
        corpus += "- File system operations (paths, wildcards, file ops)\n"
        corpus += "- Data structures (lists, maps, sets, conversions)\n"
        corpus += "- Control flow (conditionals, loops, pipelines, error handling)\n"
        corpus += "- Common patterns (map-reduce, ETL, parallel processing)\n"
        corpus += "- Realistic workflows (multi-step operations)\n\n"
        corpus += "---\n\n"

        for english, lcr in all_examples:
            corpus += f"English: {english}\n"
            corpus += f"LC-R: {lcr}\n\n"

        return corpus, len(all_examples)


if __name__ == "__main__":
    print("Generating Phase 2 corpus...")
    generator = Phase2CorpusGenerator()
    corpus, count = generator.generate_corpus()

    # Write to file
    output_file = "corpus_phase2_domain_knowledge.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(corpus)

    print(f"✓ Generated {count} examples")
    print(f"✓ Saved to {output_file}")
    print(f"\nSample examples:")

    examples = corpus.split("\n\n")[6:11]  # Get first few after header
    for ex in examples:
        if ex.strip() and ex.startswith("English:"):
            print(f"  {ex[:100]}...")
