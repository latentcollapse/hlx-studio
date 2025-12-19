#!/usr/bin/env python3
"""
HLXL Brain - Phase 3 Corpus Generator
Generate long-form reasoning examples with extended sequences.

Phase 3 Focus:
- Extended sequences (256-512 tokens vs current 128)
- Context maintenance across operations
- Variable binding and stateful operations
- Conditional logic chains
- Recursive patterns
- Complex multi-step programs

Target: 400+ examples
"""

from typing import List, Tuple
import random


class Phase3CorpusGenerator:
    """Generate Phase 3: Long-form Reasoning corpus."""

    def __init__(self):
        self.examples: List[Tuple[str, str]] = []

    def generate_long_programs(self) -> List[Tuple[str, str]]:
        """Generate long multi-step programs (10-20 operations)."""
        examples = []

        # Data processing pipelines
        pipelines = [
            ("Build a data processing pipeline that loads multiple files, merges them, cleans nulls, validates schema, transforms columns, aggregates by group, and exports to three formats",
             '🜊1000🜁0 "define"🜁1 ⟁pipeline🜁2 🜊1000🜁0 "sequence"🜁1 🜊1000🜁0 "load_many"🜁1 ["data1.csv", "data2.csv", "data3.csv"]🜂🜁2 🜊1000🜁0 "merge"🜁1 ⟁on🜁2 "id"🜂🜁3 🜊1000🜁0 "filter"🜁1 🜊1000🜁0 "not_null"🜁1 ⟁value🜂🜂🜁4 🜊1000🜁0 "validate"🜁1 ⟁schema🜁2 "data.schema.json"🜂🜁5 🜊1000🜁0 "transform"🜁1 ⟁normalize🜁2 ["col1", "col2"]🜂🜁6 🜊1000🜁0 "group_by"🜁1 "category"🜁2 🜊1000🜁0 "sum"🜁1 ⟁revenue🜂🜂🜁7 🜊1000🜁0 "export"🜁1 ["results.csv", "results.json", "results.parquet"]🜂🜂🜂'),

            ("Create an ETL pipeline that extracts from API, transforms JSON, validates fields, enriches with lookups, filters invalid records, deduplicates, sorts, and loads to database",
             '🜊1000🜁0 "pipeline"🜁1 🜊1000🜁0 "extract"🜁1 ⟁api🜁2 "https://api.example.com/data"🜂🜁2 🜊1000🜁0 "parse"🜁1 "json"🜂🜁3 🜊1000🜁0 "validate"🜁1 ["id", "name", "email"]🜂🜁4 🜊1000🜁0 "enrich"🜁1 ⟁lookup🜁2 "users.db"🜂🜁5 🜊1000🜁0 "filter"🜁1 🜊1000🜁0 "is_valid"🜂🜂🜁6 🜊1000🜁0 "deduplicate"🜁1 ⟁by🜁2 "id"🜂🜁7 🜊1000🜁0 "sort"🜁1 ⟁by🜁2 "timestamp"🜂🜁8 🜊1000🜁0 "load"🜁1 ⟁database🜁2 "warehouse.db"🜂🜂'),

            ("Build a file processing workflow that scans directory, filters by pattern, reads each file, extracts metadata, validates format, compresses, backs up to remote, and logs results",
             '🜊1000🜁0 "workflow"🜁1 🜊1000🜁0 "scan"🜁1 "/data/input"🜂🜁2 🜊1000🜁0 "filter"🜁1 "*.log"🜂🜁3 🜊1000🜁0 "map"🜁1 🜊1000🜁0 "sequence"🜁1 🜊1000🜁0 "read"🜁1 ⟁file🜂🜁2 🜊1000🜁0 "extract_metadata"🜂🜁3 🜊1000🜁0 "validate_format"🜁1 "log"🜂🜁4 🜊1000🜁0 "compress"🜁1 "gzip"🜂🜁5 🜊1000🜁0 "backup"🜁1 ⟁remote🜁2 "s3://backups"🜂🜂🜂🜁4 🜊1000🜁0 "log_results"🜁1 "process.log"🜂🜂'),

            ("Create a web scraping pipeline that fetches URLs, parses HTML, extracts links, follows pagination, filters duplicates, downloads images, resizes, and stores metadata",
             '🜊1000🜁0 "scraper"🜁1 🜊1000🜁0 "fetch"🜁1 "https://example.com/start"🜂🜁2 🜊1000🜁0 "parse"🜁1 "html"🜂🜁3 🜊1000🜁0 "extract"🜁1 ⟁links🜂🜁4 🜊1000🜁0 "paginate"🜁1 ⟁max_pages🜁2 10🜂🜁5 🜊1000🜁0 "deduplicate"🜂🜁6 🜊1000🜁0 "download"🜁1 ⟁images🜂🜁7 🜊1000🜁0 "resize"🜁1 800🜁2 600🜂🜁8 🜊1000🜁0 "store"🜁1 ⟁metadata🜁2 "scrape.db"🜂🜂'),

            ("Build a machine learning pipeline that loads dataset, splits train/test, normalizes features, trains model, validates accuracy, tunes hyperparameters, evaluates, and exports model",
             '🜊1000🜁0 "ml_pipeline"🜁1 🜊1000🜁0 "load"🜁1 "dataset.csv"🜂🜁2 🜊1000🜁0 "split"🜁1 ⟁train🜁2 0.8🜁3 ⟁test🜁4 0.2🜂🜁3 🜊1000🜁0 "normalize"🜁1 ⟁features🜂🜁4 🜊1000🜁0 "train"🜁1 ⟁model🜁2 "random_forest"🜂🜁5 🜊1000🜁0 "validate"🜁1 ⟁metric🜁2 "accuracy"🜂🜁6 🜊1000🜁0 "tune"🜁1 ⟁hyperparameters🜂🜁7 🜊1000🜁0 "evaluate"🜁1 ⟁test_set🜂🜁8 🜊1000🜁0 "export"🜁1 "model.pkl"🜂🜂'),
        ]

        examples.extend(pipelines)

        # Complex transformations
        transforms = [
            ("Transform nested JSON by flattening structure, renaming keys, converting types, filtering nulls, grouping by category, computing aggregates, and reshaping to wide format",
             '🜊1000🜁0 "transform"🜁1 🜊1000🜁0 "flatten"🜁1 ⟁json🜂🜁2 🜊1000🜁0 "rename"🜁1 {"old_key": "new_key"}🜂🜁3 🜊1000🜁0 "convert"🜁1 ⟁types🜁2 {"age": "int", "score": "float"}🜂🜁4 🜊1000🜁0 "filter"🜁1 🜊1000🜁0 "not_null"🜂🜂🜁5 🜊1000🜁0 "group_by"🜁1 "category"🜂🜁6 🜊1000🜁0 "aggregate"🜁1 {"sum": ⟁revenue, "mean": ⟁score}🜂🜁7 🜊1000🜁0 "pivot"🜁1 ⟁wide🜂🜂'),

            ("Process time series data by resampling to hourly, interpolating missing values, computing rolling averages, detecting anomalies, smoothing outliers, and forecasting next values",
             '🜊1000🜁0 "timeseries"🜁1 🜊1000🜁0 "resample"🜁1 "1H"🜂🜁2 🜊1000🜁0 "interpolate"🜁1 ⟁method🜁2 "linear"🜂🜁3 🜊1000🜁0 "rolling"🜁1 ⟁window🜁2 24🜁3 ⟁fn🜁4 "mean"🜂🜁4 🜊1000🜁0 "detect_anomalies"🜁1 ⟁threshold🜁2 3.0🜂🜁5 🜊1000🜁0 "smooth"🜁1 ⟁outliers🜂🜁6 🜊1000🜁0 "forecast"🜁1 ⟁steps🜁2 48🜂🜂'),

            ("Analyze text corpus by tokenizing documents, removing stopwords, computing TF-IDF, clustering similar docs, extracting topics, ranking by relevance, and generating summary",
             '🜊1000🜁0 "text_analysis"🜁1 🜊1000🜁0 "tokenize"🜁1 ⟁documents🜂🜁2 🜊1000🜁0 "remove_stopwords"🜁1 ⟁language🜁2 "en"🜂🜁3 🜊1000🜁0 "tfidf"🜂🜁4 🜊1000🜁0 "cluster"🜁1 ⟁k🜁2 5🜂🜁5 🜊1000🜁0 "extract_topics"🜁1 ⟁method🜁2 "lda"🜂🜁6 🜊1000🜁0 "rank"🜁1 ⟁by🜁2 "relevance"🜂🜁7 🜊1000🜁0 "summarize"🜁1 ⟁max_length🜁2 200🜂🜂'),

            ("Process image batch by loading from directory, converting color space, applying filters, detecting edges, segmenting regions, extracting features, classifying content, and saving results",
             '🜊1000🜁0 "image_batch"🜁1 🜊1000🜁0 "load"🜁1 "/images/*.jpg"🜂🜁2 🜊1000🜁0 "convert"🜁1 ⟁colorspace🜁2 "RGB"🜂🜁3 🜊1000🜁0 "filter"🜁1 ⟁gaussian🜁2 5🜂🜁4 🜊1000🜁0 "detect_edges"🜁1 ⟁method🜁2 "canny"🜂🜁5 🜊1000🜁0 "segment"🜁1 ⟁regions🜂🜁6 🜊1000🜁0 "extract_features"🜂🜁7 🜊1000🜁0 "classify"🜁1 ⟁model🜁2 "resnet50"🜂🜁8 🜊1000🜁0 "save"🜁1 "results/"🜂🜂'),
        ]

        examples.extend(transforms)
        return examples

    def generate_stateful_operations(self) -> List[Tuple[str, str]]:
        """Generate stateful operations with counters and accumulators."""
        examples = []

        # Counter patterns
        counters = [
            ("Initialize counter at 0, increment for each valid item, decrement for each invalid, return final count",
             '🜊1000🜁0 "let"🜁1 ⟁count🜁2 0🜁3 🜊1000🜁0 "for_each"🜁1 ⟁items🜁2 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "is_valid"🜁1 ⟁item🜂🜂🜁2 🜊1000🜁0 "increment"🜁1 ⟁count🜂🜁3 🜊1000🜁0 "decrement"🜁1 ⟁count🜂🜂🜂🜁4 🜊1000🜁0 "return"🜁1 ⟁count🜂🜂'),

            ("Create accumulator with initial value, fold over list adding elements, filter sum if exceeds threshold, else return sum",
             '🜊1000🜁0 "let"🜁1 ⟁acc🜁2 0🜁3 🜊1000🜁0 "fold"🜁1 ⟁list🜁2 🜊1000🜁0 "add"🜁1 ⟁acc🜁2 ⟁item🜂🜁3 ⟁acc🜂🜁4 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "gt"🜁1 ⟁acc🜁2 1000🜂🜂🜁2 1000🜁3 ⟁acc🜂🜂'),

            ("Maintain running statistics: count items, sum values, compute mean, track min and max, calculate variance",
             '🜊1000🜁0 "let"🜁1 ⟁stats🜁2 {"count": 0, "sum": 0, "min": ⟁inf, "max": -⟁inf}🜁3 🜊1000🜁0 "for_each"🜁1 ⟁values🜁2 🜊1000🜁0 "update"🜁1 ⟁stats🜁2 🜊1000🜁0 "record"🜁1 {"count": +1, "sum": +⟁value, "min": 🜊1000🜁0 "min"🜁1 ⟁min🜁2 ⟁value🜂, "max": 🜊1000🜁0 "max"🜁1 ⟁max🜁2 ⟁value🜂}🜂🜂🜂🜁4 🜊1000🜁0 "compute"🜁1 ⟁mean🜁2 🜊1000🜁0 "div"🜁1 ⟁sum🜁2 ⟁count🜂🜂🜂'),

            ("Track state machine with transitions: initialize state, process events, transition based on conditions, emit actions, return final state",
             '🜊1000🜁0 "let"🜁1 ⟁state🜁2 "idle"🜁3 🜊1000🜁0 "for_each"🜁1 ⟁events🜁2 🜊1000🜁0 "match"🜁1 ⟁state🜁2 {"idle": 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "eq"🜁1 ⟁event🜁2 "start"🜂🜂🜁2 "running"🜁3 "idle"🜂, "running": 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "eq"🜁1 ⟁event🜁2 "stop"🜂🜂🜁2 "idle"🜁3 "running"🜂}🜂🜂🜂🜁4 🜊1000🜁0 "return"🜁1 ⟁state🜂🜂'),

            ("Build histogram by initializing bins, iterating values, incrementing bin counts, normalizing by total, return distribution",
             '🜊1000🜁0 "let"🜁1 ⟁bins🜁2 [0, 0, 0, 0, 0]🜁3 🜊1000🜁0 "for_each"🜁1 ⟁values🜁2 🜊1000🜁0 "let"🜁1 ⟁bin🜁2 🜊1000🜁0 "floor"🜁1 🜊1000🜁0 "div"🜁1 ⟁value🜁2 10🜂🜂🜁3 🜊1000🜁0 "increment"🜁1 🜊1000🜁0 "at"🜁1 ⟁bins🜁2 ⟁bin🜂🜂🜂🜂🜁4 🜊1000🜁0 "normalize"🜁1 ⟁bins🜁2 🜊1000🜁0 "sum"🜁1 ⟁bins🜂🜂🜂'),
        ]

        examples.extend(counters)

        # Recursive patterns
        recursion = [
            ("Recursively traverse tree: visit node, process value, recurse on left child, recurse on right child, collect results",
             '🜊1000🜁0 "define"🜁1 ⟁traverse🜁2 🜊1000🜁0 "fn"🜁1 ⟁node🜁2 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "is_null"🜁1 ⟁node🜂🜂🜁2 []🜁3 🜊1000🜁0 "concat"🜁1 🜊1000🜁0 "traverse"🜁1 🜊1000🜁0 "get"🜁1 ⟁node🜁2 "left"🜂🜂🜁2 [🜊1000🜁0 "get"🜁1 ⟁node🜁2 "value"🜂]🜁3 🜊1000🜁0 "traverse"🜁1 🜊1000🜁0 "get"🜁1 ⟁node🜁2 "right"🜂🜂🜂🜂🜂🜂'),

            ("Recursively compute factorial: base case if n equals 0 return 1, else return n times factorial of n minus 1",
             '🜊1000🜁0 "define"🜁1 ⟁factorial🜁2 🜊1000🜁0 "fn"🜁1 ⟁n🜁2 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "eq"🜁1 ⟁n🜁2 0🜂🜂🜁2 1🜁3 🜊1000🜁0 "mul"🜁1 ⟁n🜁2 🜊1000🜁0 "factorial"🜁1 🜊1000🜁0 "sub"🜁1 ⟁n🜁2 1🜂🜂🜂🜂🜂🜂'),

            ("Recursively flatten nested lists: if element is list, recursively flatten and concatenate, else wrap in list and return",
             '🜊1000🜁0 "define"🜁1 ⟁flatten🜁2 🜊1000🜁0 "fn"🜁1 ⟁lst🜁2 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "is_empty"🜁1 ⟁lst🜂🜂🜁2 []🜁3 🜊1000🜁0 "let"🜁1 ⟁head🜁2 🜊1000🜁0 "first"🜁1 ⟁lst🜂🜁3 🜊1000🜁0 "let"🜁1 ⟁tail🜁2 🜊1000🜁0 "rest"🜁1 ⟁lst🜂🜁3 🜊1000🜁0 "concat"🜁1 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "is_list"🜁1 ⟁head🜂🜂🜁2 🜊1000🜁0 "flatten"🜁1 ⟁head🜂🜁3 [⟁head]🜂🜁2 🜊1000🜁0 "flatten"🜁1 ⟁tail🜂🜂🜂🜂🜂🜂'),

            ("Recursively search directory tree: for each entry, if directory recurse into it, if file check pattern match, collect all matches",
             '🜊1000🜁0 "define"🜁1 ⟁search🜁2 🜊1000🜁0 "fn"🜁1 ⟁path🜁2 🜊1000🜁0 "let"🜁1 ⟁entries🜁2 🜊1000🜁0 "list"🜁1 ⟁path🜂🜁3 🜊1000🜁0 "flat_map"🜁1 ⟁entries🜁2 🜊1000🜁0 "fn"🜁1 ⟁entry🜁2 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "is_dir"🜁1 ⟁entry🜂🜂🜁2 🜊1000🜁0 "search"🜁1 ⟁entry🜂🜁3 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "matches"🜁1 ⟁entry🜁2 ⟁pattern🜂🜂🜁2 [⟁entry]🜁3 []🜂🜂🜂🜂🜂🜂'),

            ("Recursively merge sorted lists: compare heads, take smaller, recurse on remainder, handle empty base cases",
             '🜊1000🜁0 "define"🜁1 ⟁merge🜁2 🜊1000🜁0 "fn"🜁1 ⟁a🜁2 ⟁b🜁3 🜊1000🜁0 "cond"🜁1 [🜊1000🜁0 "is_empty"🜁1 ⟁a🜂, ⟁b], [🜊1000🜁0 "is_empty"🜁1 ⟁b🜂, ⟁a], [🜊1000🜁0 "lt"🜁1 🜊1000🜁0 "first"🜁1 ⟁a🜂🜁2 🜊1000🜁0 "first"🜁1 ⟁b🜂🜂🜂, 🜊1000🜁0 "cons"🜁1 🜊1000🜁0 "first"🜁1 ⟁a🜂🜁2 🜊1000🜁0 "merge"🜁1 🜊1000🜁0 "rest"🜁1 ⟁a🜂🜁2 ⟁b🜂🜂], ["else", 🜊1000🜁0 "cons"🜁1 🜊1000🜁0 "first"🜁1 ⟁b🜂🜁2 🜊1000🜁0 "merge"🜁1 ⟁a🜁2 🜊1000🜁0 "rest"🜁1 ⟁b🜂🜂🜂]🜂🜂🜂'),
        ]

        examples.extend(recursion)
        return examples

    def generate_conditional_logic(self) -> List[Tuple[str, str]]:
        """Generate complex conditional logic chains."""
        examples = []

        conditions = [
            ("If user is admin then grant full access, elif user is moderator then grant edit access, elif user is member then grant read access, else deny",
             '🜊1000🜁0 "cond"🜁1 [🜊1000🜁0 "eq"🜁1 ⟁role🜁2 "admin"🜂, 🜊1000🜁0 "grant"🜁1 "full_access"🜂], [🜊1000🜁0 "eq"🜁1 ⟁role🜁2 "moderator"🜂, 🜊1000🜁0 "grant"🜁1 "edit_access"🜂], [🜊1000🜁0 "eq"🜁1 ⟁role🜁2 "member"🜂, 🜊1000🜁0 "grant"🜁1 "read_access"🜂], ["else", 🜊1000🜁0 "deny"🜂]🜂'),

            ("Validate input: if empty return error, elif too short return warning, elif contains invalid chars return error, else accept",
             '🜊1000🜁0 "validate"🜁1 🜊1000🜁0 "cond"🜁1 [🜊1000🜁0 "is_empty"🜁1 ⟁input🜂🜂, {"status": "error", "msg": "Input required"}], [🜊1000🜁0 "lt"🜁1 🜊1000🜁0 "len"🜁1 ⟁input🜂🜁2 3🜂🜂, {"status": "warning", "msg": "Too short"}], [🜊1000🜁0 "contains_invalid"🜁1 ⟁input🜂🜂, {"status": "error", "msg": "Invalid characters"}], ["else", {"status": "ok"}]🜂🜂'),

            ("Route request: if GET and path starts with api serve json, elif POST and authenticated process form, elif static file serve file, else 404",
             '🜊1000🜁0 "route"🜁1 🜊1000🜁0 "cond"🜁1 [🜊1000🜁0 "and"🜁1 🜊1000🜁0 "eq"🜁1 ⟁method🜁2 "GET"🜂🜁2 🜊1000🜁0 "starts_with"🜁1 ⟁path🜁2 "/api"🜂🜂, 🜊1000🜁0 "serve_json"🜁1 ⟁response🜂], [🜊1000🜁0 "and"🜁1 🜊1000🜁0 "eq"🜁1 ⟁method🜁2 "POST"🜂🜁2 ⟁authenticated🜂🜂, 🜊1000🜁0 "process_form"🜁1 ⟁data🜂], [🜊1000🜁0 "is_static"🜁1 ⟁path🜂🜂, 🜊1000🜁0 "serve_file"🜁1 ⟁path🜂], ["else", 🜊1000🜁0 "error"🜁1 404🜂]🜂🜂'),

            ("Process payment: if amount exceeds balance return insufficient funds, elif fraud detected return fraud alert, elif daily limit reached return limit exceeded, else process transaction",
             '🜊1000🜁0 "payment"🜁1 🜊1000🜁0 "cond"🜁1 [🜊1000🜁0 "gt"🜁1 ⟁amount🜁2 ⟁balance🜂🜂, {"status": "error", "code": "insufficient_funds"}], [🜊1000🜁0 "detect_fraud"🜁1 ⟁transaction🜂🜂, {"status": "blocked", "code": "fraud_alert"}], [🜊1000🜁0 "ge"🜁1 ⟁daily_total🜁2 ⟁daily_limit🜂🜂, {"status": "error", "code": "limit_exceeded"}], ["else", 🜊1000🜁0 "process"🜁1 ⟁transaction🜂]🜂🜂'),

            ("Classify data: if numeric and positive return category A, elif numeric and negative return category B, elif string and uppercase return category C, elif string and lowercase return category D, else unknown",
             '🜊1000🜁0 "classify"🜁1 🜊1000🜁0 "cond"🜁1 [🜊1000🜁0 "and"🜁1 🜊1000🜁0 "is_numeric"🜁1 ⟁data🜂🜁2 🜊1000🜁0 "gt"🜁1 ⟁data🜁2 0🜂🜂, "category_A"], [🜊1000🜁0 "and"🜁1 🜊1000🜁0 "is_numeric"🜁1 ⟁data🜂🜁2 🜊1000🜁0 "lt"🜁1 ⟁data🜁2 0🜂🜂, "category_B"], [🜊1000🜁0 "and"🜁1 🜊1000🜁0 "is_string"🜁1 ⟁data🜂🜁2 🜊1000🜁0 "is_uppercase"🜁1 ⟁data🜂🜂, "category_C"], [🜊1000🜁0 "and"🜁1 🜊1000🜁0 "is_string"🜁1 ⟁data🜂🜁2 🜊1000🜁0 "is_lowercase"🜁1 ⟁data🜂🜂, "category_D"], ["else", "unknown"]🜂🜂'),
        ]

        examples.extend(conditions)

        # Nested conditionals
        nested = [
            ("Process order: if inventory available then if customer verified then if payment successful then ship order else refund else reject else backorder",
             '🜊1000🜁0 "process_order"🜁1 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "check_inventory"🜁1 ⟁product🜂🜂🜁2 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "verify_customer"🜁1 ⟁customer🜂🜂🜁2 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "process_payment"🜁1 ⟁payment🜂🜂🜁2 🜊1000🜁0 "ship"🜁1 ⟁order🜂🜁3 🜊1000🜁0 "refund"🜁1 ⟁payment🜂🜂🜁3 🜊1000🜁0 "reject"🜁1 "unverified"🜂🜂🜁3 🜊1000🜁0 "backorder"🜁1 ⟁product🜂🜂'),

            ("Authenticate user: if username exists then if password matches then if MFA enabled then if token valid then grant access else deny else grant access else deny else register",
             '🜊1000🜁0 "authenticate"🜁1 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "user_exists"🜁1 ⟁username🜂🜂🜁2 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "password_match"🜁1 ⟁password🜂🜂🜁2 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "mfa_enabled"🜁1 ⟁user🜂🜂🜁2 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "validate_token"🜁1 ⟁token🜂🜂🜁2 🜊1000🜁0 "grant_access"🜂🜁3 🜊1000🜁0 "deny"🜁1 "invalid_token"🜂🜂🜁3 🜊1000🜁0 "grant_access"🜂🜂🜁3 🜊1000🜁0 "deny"🜁1 "wrong_password"🜂🜂🜁3 🜊1000🜁0 "register"🜁1 ⟁username🜂🜂'),

            ("Process file upload: if file size valid then if file type allowed then if virus scan passes then if metadata extracted then store file else reject else quarantine else reject else reject",
             '🜊1000🜁0 "upload"🜁1 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "check_size"🜁1 ⟁file🜁2 ⟁max_size🜂🜂🜁2 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "check_type"🜁1 ⟁file🜁2 ⟁allowed_types🜂🜂🜁2 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "scan"🜁1 ⟁file🜂🜂🜁2 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "extract_metadata"🜁1 ⟁file🜂🜂🜁2 🜊1000🜁0 "store"🜁1 ⟁file🜂🜁3 🜊1000🜁0 "reject"🜁1 "metadata_error"🜂🜂🜁3 🜊1000🜁0 "quarantine"🜁1 ⟁file🜂🜂🜁3 🜊1000🜁0 "reject"🜁1 "invalid_type"🜂🜂🜁3 🜊1000🜁0 "reject"🜁1 "file_too_large"🜂🜂'),
        ]

        examples.extend(nested)
        return examples

    def generate_iteration_patterns(self) -> List[Tuple[str, str]]:
        """Generate iteration patterns with loops and state."""
        examples = []

        loops = [
            ("For each item in list, if item passes filter apply transform and append to results, continue until list exhausted",
             '🜊1000🜁0 "let"🜁1 ⟁results🜁2 []🜁3 🜊1000🜁0 "for_each"🜁1 ⟁list🜁2 🜊1000🜁0 "fn"🜁1 ⟁item🜁2 🜊1000🜁0 "when"🜁1 🜊1000🜁0 "filter"🜁1 ⟁item🜂🜂🜁2 🜊1000🜁0 "append"🜁1 ⟁results🜁2 🜊1000🜁0 "transform"🜁1 ⟁item🜂🜂🜂🜂🜂🜁4 🜊1000🜁0 "return"🜁1 ⟁results🜂🜂'),

            ("While condition true, fetch batch of items, process each item, update progress counter, check condition, repeat",
             '🜊1000🜁0 "let"🜁1 ⟁progress🜁2 0🜁3 🜊1000🜁0 "while"🜁1 🜊1000🜁0 "lt"🜁1 ⟁progress🜁2 ⟁total🜂🜂🜁2 🜊1000🜁0 "sequence"🜁1 🜊1000🜁0 "let"🜁1 ⟁batch🜁2 🜊1000🜁0 "fetch"🜁1 ⟁progress🜁2 ⟁batch_size🜂🜂🜁2 🜊1000🜁0 "for_each"🜁1 ⟁batch🜁2 🜊1000🜁0 "process"🜂🜂🜁3 🜊1000🜁0 "update"🜁1 ⟁progress🜁2 🜊1000🜁0 "add"🜁1 ⟁progress🜁2 ⟁batch_size🜂🜂🜂🜂🜂'),

            ("Iterate with early exit: for each element, check condition, if met return element and break, else continue to next, if exhausted return null",
             '🜊1000🜁0 "for_each"🜁1 ⟁elements🜁2 🜊1000🜁0 "fn"🜁1 ⟁elem🜁2 🜊1000🜁0 "when"🜁1 🜊1000🜁0 "check"🜁1 ⟁elem🜂🜂🜁2 🜊1000🜁0 "return"🜁1 ⟁elem🜂🜂🜂🜂🜁3 🜊1000🜁0 "return"🜁1 ⟁null🜂'),

            ("Nested loops: for each category, for each item in category, for each property of item, validate property, collect all validation results",
             '🜊1000🜁0 "flat_map"🜁1 ⟁categories🜁2 🜊1000🜁0 "fn"🜁1 ⟁category🜁2 🜊1000🜁0 "flat_map"🜁1 🜊1000🜁0 "get"🜁1 ⟁category🜁2 "items"🜂🜁2 🜊1000🜁0 "fn"🜁1 ⟁item🜁2 🜊1000🜁0 "map"🜁1 🜊1000🜁0 "get"🜁1 ⟁item🜁2 "properties"🜂🜁2 🜊1000🜁0 "validate"🜂🜂🜂🜂🜂🜂'),

            ("Parallel iteration: map over list with async function, collect promises, wait for all to complete, aggregate results",
             '🜊1000🜁0 "let"🜁1 ⟁promises🜁2 🜊1000🜁0 "map"🜁1 ⟁list🜁2 🜊1000🜁0 "async"🜁1 🜊1000🜁0 "fetch"🜁1 ⟁item🜂🜂🜂🜁3 🜊1000🜁0 "let"🜁1 ⟁results🜁2 🜊1000🜁0 "await_all"🜁1 ⟁promises🜂🜁3 🜊1000🜁0 "aggregate"🜁1 ⟁results🜂🜂'),
        ]

        examples.extend(loops)

        # Generator patterns
        generators = [
            ("Create lazy sequence generator: yield first element, compute next based on previous, continue infinitely or until condition",
             '🜊1000🜁0 "generator"🜁1 🜊1000🜁0 "let"🜁1 ⟁current🜁2 0🜁3 🜊1000🜁0 "loop"🜁1 🜊1000🜁0 "yield"🜁1 ⟁current🜂🜁2 🜊1000🜁0 "update"🜁1 ⟁current🜁2 🜊1000🜁0 "next"🜁1 ⟁current🜂🜂🜂🜂'),

            ("Stream processing: take items from input stream, transform each item, filter results, yield to output stream, handle backpressure",
             '🜊1000🜁0 "stream"🜁1 🜊1000🜁0 "from"🜁1 ⟁input🜂🜁2 🜊1000🜁0 "map"🜁1 🜊1000🜁0 "transform"🜂🜂🜁3 🜊1000🜁0 "filter"🜁1 🜊1000🜁0 "is_valid"🜂🜂🜁4 🜊1000🜁0 "to"🜁1 ⟁output🜂🜁5 🜊1000🜁0 "with_backpressure"🜁1 1000🜂🜂'),

            ("Range iteration with step: start at begin, step by increment, check if less than end, yield value, continue",
             '🜊1000🜁0 "generator"🜁1 🜊1000🜁0 "let"🜁1 ⟁i🜁2 ⟁begin🜁3 🜊1000🜁0 "while"🜁1 🜊1000🜁0 "lt"🜁1 ⟁i🜁2 ⟁end🜂🜂🜁2 🜊1000🜁0 "sequence"🜁1 🜊1000🜁0 "yield"🜁1 ⟁i🜂🜁2 🜊1000🜁0 "update"🜁1 ⟁i🜁2 🜊1000🜁0 "add"🜁1 ⟁i🜁2 ⟁step🜂🜂🜂🜂🜂'),
        ]

        examples.extend(generators)
        return examples

    def generate_context_maintenance(self) -> List[Tuple[str, str]]:
        """Generate examples requiring context maintenance across operations."""
        examples = []

        context = [
            ("Define variables x, y, z at start, use x in operation 1, use y in operation 2, combine x and y in operation 3, use z in operation 4, return all results",
             '🜊1000🜁0 "let"🜁1 ⟁x🜁2 10🜁3 ⟁y🜁4 20🜁5 ⟁z🜁6 30🜁7 🜊1000🜁0 "sequence"🜁1 🜊1000🜁0 "let"🜁1 ⟁result1🜁2 🜊1000🜁0 "compute"🜁1 ⟁x🜂🜂🜁2 🜊1000🜁0 "let"🜁1 ⟁result2🜁2 🜊1000🜁0 "compute"🜁1 ⟁y🜂🜂🜁3 🜊1000🜁0 "let"🜁1 ⟁result3🜁2 🜊1000🜁0 "combine"🜁1 ⟁x🜁2 ⟁y🜂🜂🜁4 🜊1000🜁0 "let"🜁1 ⟁result4🜁2 🜊1000🜁0 "compute"🜁1 ⟁z🜂🜂🜁5 🜊1000🜁0 "return"🜁1 [⟁result1, ⟁result2, ⟁result3, ⟁result4]🜂🜂🜂'),

            ("Load configuration at beginning, extract database settings, connect to database, extract API settings, configure API client, use both throughout pipeline",
             '🜊1000🜁0 "let"🜁1 ⟁config🜁2 🜊1000🜁0 "load"🜁1 "config.json"🜂🜁3 🜊1000🜁0 "let"🜁1 ⟁db_settings🜁2 🜊1000🜁0 "get"🜁1 ⟁config🜁2 "database"🜂🜁3 🜊1000🜁0 "let"🜁1 ⟁db🜁2 🜊1000🜁0 "connect"🜁1 ⟁db_settings🜂🜁3 🜊1000🜁0 "let"🜁1 ⟁api_settings🜁2 🜊1000🜁0 "get"🜁1 ⟁config🜁2 "api"🜂🜁3 🜊1000🜁0 "let"🜁1 ⟁api🜁2 🜊1000🜁0 "configure"🜁1 ⟁api_settings🜂🜁3 🜊1000🜁0 "pipeline"🜁1 🜊1000🜁0 "sequence"🜁1 🜊1000🜁0 "fetch_from_api"🜁1 ⟁api🜂🜁2 🜊1000🜁0 "store_in_db"🜁1 ⟁db🜂🜂🜂🜂'),

            ("Initialize session with user context, track user actions throughout workflow, update user state after each step, log all actions with user context, cleanup session at end",
             '🜊1000🜁0 "let"🜁1 ⟁session🜁2 🜊1000🜁0 "init_session"🜁1 ⟁user🜂🜁3 🜊1000🜁0 "try"🜁1 🜊1000🜁0 "sequence"🜁1 🜊1000🜁0 "let"🜁1 ⟁action1🜁2 🜊1000🜁0 "do_action"🜁1 "step1"🜂🜂🜁2 🜊1000🜁0 "log"🜁1 ⟁session🜁2 ⟁action1🜂🜁3 🜊1000🜁0 "update_state"🜁1 ⟁session🜁2 ⟁action1🜂🜁4 🜊1000🜁0 "let"🜁1 ⟁action2🜁2 🜊1000🜁0 "do_action"🜁1 "step2"🜂🜂🜁5 🜊1000🜁0 "log"🜁1 ⟁session🜁2 ⟁action2🜂🜁6 🜊1000🜁0 "update_state"🜁1 ⟁session🜁2 ⟁action2🜂🜂🜁2 🜊1000🜁0 "finally"🜁1 🜊1000🜁0 "cleanup"🜁1 ⟁session🜂🜂🜂🜂'),

            ("Build execution plan with dependencies: step A defines result, step B uses result from A, step C uses results from A and B, step D uses result from C",
             '🜊1000🜁0 "let"🜁1 ⟁plan🜁2 🜊1000🜁0 "plan"🜁1 🜊1000🜁0 "step"🜁1 "A"🜁2 🜊1000🜁0 "fn"🜁1 🜊1000🜁0 "compute"🜁1 "value_A"🜂🜂🜂🜁2 🜊1000🜁0 "step"🜁1 "B"🜁2 🜊1000🜁0 "fn"🜁1 ⟁result_A🜁2 🜊1000🜁0 "compute"🜁1 ⟁result_A🜂🜂🜁3 ["A"]🜂🜁3 🜊1000🜁0 "step"🜁1 "C"🜁2 🜊1000🜁0 "fn"🜁1 ⟁result_A🜁2 ⟁result_B🜁3 🜊1000🜁0 "combine"🜁1 ⟁result_A🜁2 ⟁result_B🜂🜂🜁3 ["A", "B"]🜂🜁4 🜊1000🜁0 "step"🜁1 "D"🜁2 🜊1000🜁0 "fn"🜁1 ⟁result_C🜁2 🜊1000🜁0 "finalize"🜁1 ⟁result_C🜂🜂🜁3 ["C"]🜂🜂🜁3 🜊1000🜁0 "execute"🜁1 ⟁plan🜂🜂'),
        ]

        examples.extend(context)
        return examples

    def generate_all(self) -> List[Tuple[str, str]]:
        """Generate all Phase 3 examples."""
        print("Generating Phase 3 corpus...")

        self.examples = []
        self.examples.extend(self.generate_long_programs())
        print(f"  ✓ Long programs: {len([e for e in self.examples if e in self.generate_long_programs()])} examples")

        stateful = self.generate_stateful_operations()
        self.examples.extend(stateful)
        print(f"  ✓ Stateful operations: {len(stateful)} examples")

        conditional = self.generate_conditional_logic()
        self.examples.extend(conditional)
        print(f"  ✓ Conditional logic: {len(conditional)} examples")

        iteration = self.generate_iteration_patterns()
        self.examples.extend(iteration)
        print(f"  ✓ Iteration patterns: {len(iteration)} examples")

        context = self.generate_context_maintenance()
        self.examples.extend(context)
        print(f"  ✓ Context maintenance: {len(context)} examples")

        print(f"\nTotal Phase 3 examples: {len(self.examples)}")
        return self.examples

    def write_corpus(self, filename: str):
        """Write corpus to markdown file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# HLXL Brain - Phase 3: Long-form Reasoning Corpus\n\n")
            f.write("## Training Examples for Extended Sequences and Context Maintenance\n\n")
            f.write(f"Total examples: {len(self.examples)}\n\n")
            f.write("---\n\n")

            for i, (english, lcr) in enumerate(self.examples, 1):
                f.write(f"### Example {i}\n\n")
                f.write(f"**English:**\n{english}\n\n")
                f.write(f"**LC-R:**\n```\n{lcr}\n```\n\n")
                f.write("---\n\n")

        print(f"✓ Corpus written to {filename}")


if __name__ == "__main__":
    generator = Phase3CorpusGenerator()
    examples = generator.generate_all()
    generator.write_corpus("corpus_phase3_longform_reasoning.md")
    print("\nPhase 3 corpus generation complete!")
    print(f"Generated {len(examples)} examples")
    print("\nNext steps:")
    print("1. Review corpus_phase3_longform_reasoning.md")
    print("2. Merge with previous phases: cat corpus_combined_phase2.md corpus_phase3_longform_reasoning.md > corpus_combined_phase3.md")
    print("3. Update training script for Phase 3 (increase seq_length to 256)")
    print("4. Run: python3 train_phase3.py")
