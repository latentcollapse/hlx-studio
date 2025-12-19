# HLXL Brain Expansion Curriculum
**100 Epoch Training Plan: From Syntax to Semantics**

## Current State (Day 4 Baseline)
- **Parameters:** 491,635
- **Training:** 5 epochs on 164 LC-R examples
- **Capability:** Pattern completion (syntax only, no semantics)
- **Speed:** 700 tok/s
- **Loss:** 0.21 train, 0.23 val

## Training Philosophy
**"Semantic Grounding Through Structured Examples"**

Instead of making the model bigger, we make it *smarter* by teaching it:
1. What operations **mean** (not just their shape)
2. How to **reason** about sequences
3. **Natural language** mappings to LC-R
4. **Perfect HLX syntax** generation

---

## Phase 1: Semantic Grounding (Epochs 6-30, 25 epochs)
**Goal:** Teach the model what operations *mean*, not just their syntax

### Training Focus:
- **Action verbs with context**
  - `navigate` → movement through spaces
  - `search` → finding patterns in data
  - `filter` → selecting subsets
  - `transform` → changing representations
  - `aggregate` → combining many into one
  - `split` → dividing one into many
  - `validate` → checking correctness
  - `optimize` → improving performance

- **Data operations**
  - `read`, `write`, `append`, `delete`
  - `copy`, `move`, `rename`, `backup`
  - `compress`, `decompress`, `encrypt`, `decrypt`

- **Computational operations**
  - `compute`, `calculate`, `evaluate`, `measure`
  - `compile`, `interpret`, `execute`, `debug`
  - `train`, `infer`, `predict`, `classify`

### Corpus Additions (500+ examples):
- Function calls with **semantic comments** in English
- Input/output pairs showing **cause and effect**
- Error cases with **validation messages**

**Example Training Pairs:**
```
English: Navigate to the home directory
LC-R: 🜊1000🜁0 "navigate"🜁1 ⟁home🜂

English: Search for files containing "test"
LC-R: 🜊1000🜁0 "search"🜁1 ⟁files🜁2 "test"🜂

English: Filter data where age is greater than 18
LC-R: 🜊1000🜁0 "filter"🜁1 ⟁data🜁2 🜊1000🜁0 "gt"🜁1 ⟁age🜁2 18🜂🜂

English: Transform text to uppercase
LC-R: 🜊1000🜁0 "transform"🜁1 ⟁text🜁2 ⟁uppercase🜂
```

### Success Metrics:
- Model generates **correct operation** given English description
- Can **complete partial LC-R** with semantically appropriate args
- Validation loss < 0.15

---

## Phase 2: Domain Knowledge (Epochs 31-55, 25 epochs)
**Goal:** Teach common patterns, idioms, and domain-specific operations

### Training Focus:
- **File system operations**
  - Paths: `/home/user/docs`, `./relative`, `../parent`
  - Wildcards: `*.txt`, `**/*.py`, `{a,b,c}.json`
  - Permissions: `chmod 755`, `chown user:group`

- **Data structures**
  - Lists: `[1, 2, 3]`, ranges, slices
  - Maps: `{key: value}`, lookups, updates
  - Sets: `{a, b, c}`, unions, intersections
  - Trees: hierarchies, traversals

- **Control flow**
  - Conditionals: `if`, `else`, `match`
  - Loops: `for`, `while`, `iterate`
  - Pipelines: `input | process | output`

- **Common patterns**
  - Map-reduce
  - Filter-transform-aggregate
  - Load-process-save
  - Query-validate-return

### Corpus Additions (600+ examples):
- **Realistic workflows** (multi-step operations)
- **Nested structures** (functions calling functions)
- **Error handling** (try-catch, validate-or-default)

**Example Training Sequences:**
```
English: Load CSV, filter rows, calculate average, save result
LC-R: 🜊1000🜁0 "pipeline"🜁1
  🜊1000🜁0 "load"🜁1 "data.csv"🜂🜁2
  🜊1000🜁0 "filter"🜁1 ⟁rows🜁2 🜊1000🜁0 "gt"🜁1 ⟁score🜁2 80🜂🜂🜂🜁3
  🜊1000🜁0 "aggregate"🜁1 ⟁average🜁2 ⟁score🜂🜁4
  🜊1000🜁0 "save"🜁1 "results.json"🜂🜂

English: Find all Python files, count lines, sort by size
LC-R: 🜊1000🜁0 "pipeline"🜁1
  🜊1000🜁0 "find"🜁1 "**/*.py"🜂🜁2
  🜊1000🜁0 "map"🜁1 🜊1000🜁0 "count_lines"🜂🜂🜁3
  🜊1000🜁0 "sort"🜁1 ⟁desc🜂🜂
```

### Success Metrics:
- Can generate **multi-step workflows** from English descriptions
- Correctly **nests function calls**
- Validation loss < 0.12

---

## Phase 3: Long-Form Reasoning (Epochs 56-80, 25 epochs)
**Goal:** Handle longer sequences, maintain context, generate complex programs

### Training Focus:
- **Extended sequences** (256-512 tokens)
- **Context maintenance** (remember earlier args)
- **Variable binding** (define once, use many times)
- **Conditional logic** (if-then-else chains)
- **Iteration** (loops with state)

### Training Techniques:
- **Increase sequence length** from 128 → 256 tokens
- **Add positional encodings** for longer context
- **Curriculum learning**: Short → Medium → Long sequences
- **Attention analysis**: Verify model attends to relevant parts

### Corpus Additions (400+ examples):
- **Long programs** (10-20 operations)
- **Stateful operations** (counters, accumulators)
- **Recursive patterns** (tree traversals)

**Example Long Sequence:**
```
English: Build a data processing pipeline that loads multiple files,
         merges them, cleans nulls, validates schema, transforms columns,
         aggregates by group, and exports to three formats

LC-R: 🜊1000🜁0 "define"🜁1 ⟁pipeline🜁2
  🜊1000🜁0 "sequence"🜁1
    🜊1000🜁0 "load_many"🜁1 ["data1.csv", "data2.csv", "data3.csv"]🜂🜁2
    🜊1000🜁0 "merge"🜁1 ⟁on🜁2 "id"🜂🜁3
    🜊1000🜁0 "filter"🜁1 🜊1000🜁0 "not_null"🜁1 ⟁value🜂🜂🜁4
    🜊1000🜁0 "validate"🜁1 ⟁schema🜁2 "data.schema.json"🜂🜁5
    🜊1000🜁0 "transform"🜁1 ⟁normalize🜁2 ["col1", "col2"]🜂🜁6
    🜊1000🜁0 "group_by"🜁1 "category"🜁2 🜊1000🜁0 "sum"🜁1 ⟁revenue🜂🜂🜁7
    🜊1000🜁0 "export"🜁1 ["results.csv", "results.json", "results.parquet"]🜂🜂🜂
```

### Success Metrics:
- Can generate **coherent long sequences** (>200 tokens)
- Maintains **context** across operations
- Validation loss < 0.10

---

## Phase 4: Perfect HLX + Quality English (Epochs 81-105, 25 epochs)
**Goal:** Master HLX family syntax + generate natural, idiomatic English

### Training Focus:

#### HLX Family Mastery:
- **LC-R (Latent Collapse Runic)** - Core format
- **LC-B (Latent Collapse Binary)** - Wire format
- **HLXL (Helix Language)** - High-level syntax
- **All contract types** (14-22, 1000-1002)
- **Perfect glyph balance** (🜊 starts, 🜂 ends, 🜁 separates)
- **Proper nesting** (recursive structures)
- **Type safety** (contracts wrapping values correctly)

#### Natural Language Generation:
- **Idiomatic English** (not robotic translations)
- **Context-aware phrasing** (adapt to domain)
- **Concise descriptions** (remove verbosity)
- **Technical accuracy** (proper terminology)

### Corpus Additions (500+ examples):
- **Bidirectional pairs**: English ↔ LC-R
- **Multiple phrasings**: Same LC-R, different English
- **Style variations**: Formal, casual, technical
- **Error corrections**: Bad syntax → Good syntax

**Example Pairs (English variations for same LC-R):**
```
LC-R: 🜊1000🜁0 "search"🜁1 ⟁database🜁2 "keyword"🜂

English (formal): Execute a search operation on the database for the keyword
English (casual): Search the database for "keyword"
English (terse): db.search("keyword")
English (verbose): Perform a comprehensive search query against the database system to locate entries matching the specified keyword
```

**Example Perfect HLX Syntax:**
```
HLXL: search(database, "keyword")
LC-R: 🜊1000🜁0 "search"🜁1 ⟁database🜁2 "keyword"🜂
LC-B: [0x08][0x0F][0x00][0x06]search[0x0F][0x01][0x14]database[0x0F][0x02][0x10][0x07]keyword[0x0E]

All equivalent, perfect syntax, deterministic conversion
```

### Advanced Training Examples:
```
# Complex nested structure with perfect balance
LC-R: 🜊1000🜁0 "pipeline"🜁1
  🜊14🜁0
    🜊1000🜁0 "load"🜁1 "input.json"🜂🜁1
    🜊1000🜁0 "transform"🜁1 ⟁normalize🜂🜁2
    🜊1000🜁0 "filter"🜁1 🜊1000🜁0 "valid"🜂🜂🜁3
    🜊1000🜁0 "save"🜁1 "output.json"🜂🜂🜂

English: Run a data pipeline that loads input.json, normalizes the data,
         filters for valid entries, and saves to output.json
```

### Success Metrics:
- **Zero syntax errors** in generated LC-R
- **Perfect glyph balance** (validated by parser)
- **Natural English** (human evaluation)
- **All HLX formats** generated correctly
- Validation loss < 0.08
- **Final target: < 0.05 val loss**

---

## Training Schedule

### Hardware Target:
- **CPU-only training** (for portability)
- **Batch size:** 4-8 (memory efficient)
- **Learning rate schedule:** Cosine annealing with warm restarts
- **Checkpointing:** Every 5 epochs + best model
- **Early stopping:** Patience of 10 epochs

### Time Estimates (CPU):
- **Phase 1:** ~6-8 hours (25 epochs, 500 examples)
- **Phase 2:** ~8-10 hours (25 epochs, 600 examples)
- **Phase 3:** ~10-12 hours (25 epochs, 400 longer examples)
- **Phase 4:** ~8-10 hours (25 epochs, 500 examples)
- **Total:** ~32-40 hours of training

### Monitoring:
- **Loss curves** (train/val) plotted each phase
- **Perplexity** tracking
- **Sample generation** every 5 epochs (qualitative check)
- **Validation on held-out test set** (never seen during training)

---

## Corpus Statistics (Target)

### Current:
- **164 examples** (LC-R syntax only)
- **115 vocabulary tokens**
- **~20,000 training tokens**

### After Expansion:
- **~2,000 examples** (164 baseline + 1,836 new)
  - Phase 1: +500 (semantic grounding)
  - Phase 2: +600 (domain knowledge)
  - Phase 3: +400 (long sequences)
  - Phase 4: +336 (perfect syntax + English)
- **~250,000 training tokens** (12.5x increase)
- **Vocabulary:** Still 115 (no expansion needed)

---

## Evaluation Framework

### Quantitative Metrics:
1. **Validation loss** (target: < 0.05)
2. **Perplexity** (lower is better)
3. **BLEU score** (LC-R generation vs reference)
4. **Exact match accuracy** (glyph balance, syntax)

### Qualitative Metrics:
1. **Semantic correctness** (does it do what English says?)
2. **Natural language quality** (human readability)
3. **Edge case handling** (rare patterns)
4. **Error recovery** (graceful degradation)

### Test Suite:
- **100 held-out examples** (never trained on)
- **Adversarial cases** (tricky syntax)
- **Cross-validation** (5-fold)
- **Ablation studies** (which phase mattered most?)

---

## Deliverables

### Checkpoints:
- `checkpoint_epoch30_phase1.pt` (semantic grounding complete)
- `checkpoint_epoch55_phase2.pt` (domain knowledge complete)
- `checkpoint_epoch80_phase3.pt` (long-form reasoning complete)
- `checkpoint_epoch105_phase4.pt` (final model)
- `best_model.pt` (lowest validation loss)

### Documentation:
- `TRAINING_LOG.md` (detailed progress notes)
- `ABLATION_STUDY.md` (which training helped most?)
- `GENERATION_SAMPLES.md` (examples from each phase)

### Benchmarks:
- `benchmarks/phase1_results.json`
- `benchmarks/phase2_results.json`
- `benchmarks/phase3_results.json`
- `benchmarks/phase4_results.json`
- `benchmarks/final_comparison.json` (before/after)

---

## Expected Outcomes

### By Epoch 30 (Phase 1):
- ✅ Generates **semantically correct** LC-R for English prompts
- ✅ Understands **30+ operation types**
- ✅ Can **complete partial sequences** intelligently

### By Epoch 55 (Phase 2):
- ✅ Handles **multi-step workflows**
- ✅ Correctly **nests function calls**
- ✅ Knows **file paths, data structures, control flow**

### By Epoch 80 (Phase 3):
- ✅ Generates **long, coherent programs** (200+ tokens)
- ✅ Maintains **context** across operations
- ✅ Can **reason about state**

### By Epoch 105 (Phase 4):
- ✅ **Zero syntax errors** in LC-R
- ✅ **Perfect HLX family syntax**
- ✅ **Natural, idiomatic English**
- ✅ Ready for **production deployment**

---

## Risk Mitigation

### Overfitting Prevention:
- **Data augmentation** (paraphrase, reorder, permute)
- **Dropout** (0.1 during training)
- **Weight decay** (L2 regularization)
- **Validation monitoring** (stop if val loss increases)

### Catastrophic Forgetting:
- **Replay buffer** (keep 20% old examples in each phase)
- **Gradual curriculum** (don't drop old tasks)
- **Multi-task learning** (train on all phases simultaneously in final 5 epochs)

### Computational Constraints:
- **Gradient checkpointing** (reduce memory usage)
- **Mixed precision training** (FP16 where safe)
- **Batch accumulation** (simulate larger batches)

---

## Success Criteria

**The HLXL Brain is ready for production when:**

1. ✅ Validation loss < 0.05
2. ✅ 99%+ syntax correctness on held-out test set
3. ✅ Human evaluators rate English quality as "natural" (4/5+)
4. ✅ Can generate 500+ token sequences without errors
5. ✅ Inference speed still > 500 tok/s (minimal degradation)
6. ✅ Model size < 3 MB (still tiny!)

---

## Next Steps

1. **Build expanded corpus** (phases 1-4)
2. **Modify training script** for continued training
3. **Set up monitoring dashboard** (live loss curves)
4. **Run Phase 1** (25 epochs)
5. **Evaluate & iterate**
6. **Repeat for Phases 2-4**

**Estimated completion:** 2-3 days of continuous training
**Expected model quality:** Production-ready HLX semantic engine
