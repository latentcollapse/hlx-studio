# HLXL Brain Development: Quality Mandate & Watchdog Protocol

**Purpose:** Prevent agent failure through rigorous standards enforcement
**Principle:** "We don't make claims. We provide raw immutable data."
**Target:** Shipping production-ready Studio brain with zero unverified assertions

---

## Core Principles (Non-Negotiable)

### ✅ REQUIRED Standards

1. **Raw Immutable Data**
   - All results stored as timestamped JSON files
   - Never delete or overwrite measurement data
   - Git commit hash recorded with every benchmark
   - Environment metadata captured automatically

2. **Test-Driven Validation**
   - Code runs BEFORE claiming success
   - All tests pass BEFORE marking complete
   - Actual output captured, not predicted
   - No "expected" or "should" language

3. **Statistical Rigor**
   - Benchmarks include: mean, median, std dev, CI
   - Minimum 100 iterations for micro-ops
   - Warmup phase documented and excluded
   - Outliers detected and reported (not removed)

4. **Environment Capture**
   - Python version, PyTorch version recorded
   - Hardware specs (CPU, RAM, GPU) documented
   - Git state (commit hash, dirty flag) tracked
   - System load and temperature monitored

5. **Incremental Progress**
   - Small, testable steps
   - Each step verified before next
   - Rollback capability maintained
   - Progress checkpoints committed frequently

### ❌ FORBIDDEN Practices

1. **No Predictions**
   - Never say "this will be X% faster" without measuring
   - Never estimate performance without benchmark
   - Never claim success before running code

2. **No Claims Without Data**
   - Every assertion backed by measurement
   - Every optimization verified with before/after
   - Every feature tested with actual execution

3. **No Incomplete Work**
   - Don't mark tasks complete until verified
   - Don't move to next phase with failing tests
   - Don't commit code that doesn't run

4. **No Fake Data**
   - Never generate synthetic benchmark results
   - Never fill in "placeholder" measurements
   - Never estimate when measurement is possible

5. **No Scope Creep**
   - Build what's specified, nothing more
   - No "improvements" beyond requirements
   - No premature optimization
   - No gold-plating

---

## HLXL Brain Specific Standards

### Tokenizer Requirements

**Success Criteria:**
- [ ] 100% round-trip accuracy on LC-R glyphs
- [ ] <1ms encoding/decoding latency
- [ ] Actual test corpus: 400+ examples from LC_R_EXAMPLES
- [ ] Zero errors on edge cases (empty, max length, unicode)

**Failure to Meet:** DO NOT proceed to model training

### Model Training Requirements

**Success Criteria:**
- [ ] Training loss converges (plot saved as PNG)
- [ ] Validation accuracy ≥ 80% on holdout set
- [ ] Training completes in <1 hour on RTX 5060
- [ ] Checkpoint saved with metadata (epoch, loss, accuracy)

**Failure to Meet:** Debug training loop, don't fake convergence

### Inference Requirements

**Success Criteria:**
- [ ] Cold start inference < 2s (measured, not estimated)
- [ ] Warm inference < 1s (measured over 100 requests)
- [ ] Determinism: same input → same output (10/10 trials)
- [ ] Hallucination rate < 10% on handle resolution

**Failure to Meet:** Optimize or document limitation, don't ship broken

### Integration Requirements

**Success Criteria:**
- [ ] API server starts without errors (logs captured)
- [ ] Health endpoint returns 200 OK
- [ ] Studio can query and receive response
- [ ] Graceful fallback to Claude API if brain offline

**Failure to Meet:** Fix integration, don't bypass with workarounds

---

## Watchdog Protocol for Agents

### Before Agent Launch

**Sonnet (Overseer) Checklist:**
1. ✅ Success criteria clearly defined
2. ✅ Verification method specified
3. ✅ Output format documented
4. ✅ Failure conditions listed
5. ✅ Rollback plan established

### During Agent Execution

**Monitor for RED FLAGS:**
- ⚠️ Agent claims success without showing output
- ⚠️ Agent provides "expected" results instead of actual
- ⚠️ Agent skips verification steps
- ⚠️ Agent makes performance claims without benchmarks
- ⚠️ Agent creates placeholder files with TODOs

**Intervention Required If:**
- Agent reports "tests passing" but doesn't show pass count
- Agent says "training complete" but no loss plot
- Agent claims "faster" but no before/after measurements
- Agent marks task done but code doesn't run

### After Agent Completion

**Sonnet (Auditor) Verification:**
1. ✅ Read all generated code
2. ✅ Run all tests independently
3. ✅ Verify claimed measurements exist
4. ✅ Check for unverified assertions
5. ✅ Validate against quality gates

**Reject & Request Revision If:**
- Claims without supporting data files
- Tests not actually executed
- Benchmarks without statistical analysis
- Missing environment metadata
- Code that doesn't run

---

## Quality Gates by Phase

### Phase 1: Tokenizer (Week 1, Day 1-2)

**Entry Criteria:**
- [ ] LC-R glyph vocabulary defined (<100 symbols)
- [ ] Test corpus available (400+ examples)

**Exit Criteria:**
- [ ] tokenizer.py file created and runnable
- [ ] Round-trip test passes: `python test_tokenizer.py`
- [ ] Performance benchmark logged: `benchmarks/tokenizer_perf.json`
- [ ] Zero errors on full corpus

**DO NOT PROCEED if any test fails**

### Phase 2: Model (Week 1, Day 3-4)

**Entry Criteria:**
- [ ] Tokenizer passing all tests
- [ ] PyTorch installed and working
- [ ] Training data prepared (10k examples)

**Exit Criteria:**
- [ ] model.py file created and trains
- [ ] Training loss plot: `benchmarks/training_loss.png`
- [ ] Validation accuracy ≥ 80%
- [ ] Model checkpoint: `checkpoints/hlxl_brain_v1.pt`

**DO NOT PROCEED if training doesn't converge**

### Phase 3: Inference (Week 1, Day 5-7)

**Entry Criteria:**
- [ ] Trained model checkpoint exists
- [ ] Axiom test suite defined

**Exit Criteria:**
- [ ] inference.py runs without errors
- [ ] Latency benchmark: `benchmarks/inference_latency.json`
- [ ] Axiom compliance: `benchmarks/axiom_test_results.json`
- [ ] Determinism verified over 100 runs

**DO NOT PROCEED if inference fails axiom tests**

### Phase 4: Integration (Week 2)

**Entry Criteria:**
- [ ] Inference engine working locally
- [ ] Studio codebase accessible

**Exit Criteria:**
- [ ] API server: `hlxl_brain_server.py` running
- [ ] Health check returns 200: `curl localhost:8000/hlxl/health`
- [ ] Studio can query successfully (screenshot/log)
- [ ] Fallback to Claude API works

**DO NOT DEPLOY if Studio integration fails**

---

## Example: Acceptable vs. Unacceptable Reporting

### ❌ UNACCEPTABLE (Prediction, No Data)

> "The tokenizer should be very fast, probably <1ms for most operations. I expect it to handle the full corpus without issues."

**Problems:**
- "should be" = prediction, not measurement
- "probably" = guess, not verification
- "I expect" = assumption, not test result

### ✅ ACCEPTABLE (Measured, Verified)

> "Tokenizer performance measured over 1000 iterations:
> - Mean: 0.34ms (95% CI: ±0.02ms)
> - Median: 0.32ms
> - Max: 1.2ms (outlier, investigated)
>
> Full corpus test: 400/400 examples passed round-trip (0 errors)
>
> Results saved to: benchmarks/tokenizer_perf_20251218.json
> Git commit: a7d6b60d"

**Why Acceptable:**
- Actual measurements with statistics
- Concrete test results (400/400)
- Data file reference
- Environment metadata (commit hash)

---

## Escalation Protocol

### When Agent Produces Low-Quality Work

1. **First Response:** Reject with specific issues
   ```
   REJECTED: Claims without data

   Issues:
   - Line 15: "training converged" but no loss plot provided
   - Line 32: "inference is fast" but no latency measurement
   - No benchmark files in benchmarks/ directory

   Required:
   - Show actual training loss plot
   - Run and save latency benchmark
   - Provide file paths to all measurement data
   ```

2. **Second Response:** Provide explicit template
   ```
   Use this exact format:

   Training Results:
   - Final loss: [ACTUAL NUMBER]
   - Plot file: [FILE PATH]
   - Convergence epoch: [ACTUAL NUMBER]

   Run this command and paste output:
   ls -lh benchmarks/
   ```

3. **Third Response:** Haiku takeover
   ```
   Spawn Haiku agent with strict checklist to:
   1. Run training from scratch
   2. Capture all outputs
   3. Save all measurements
   4. Verify every claim
   ```

### When Sonnet Misses Issues

**Self-Audit Trigger:**
- If user questions quality
- If tests fail unexpectedly
- If measurements don't make sense
- If integration breaks in production

**Action:**
1. Re-read all agent outputs
2. Verify all claimed measurements exist
3. Re-run all tests independently
4. Update watchdog criteria to catch this class of error

---

## Success Metrics

### For Entire Project

**Quantitative:**
- 0 unverified claims in final deliverables
- 100% test passage rate before marking complete
- <5% variance across benchmark runs
- All measurements include CI and metadata

**Qualitative:**
- User can reproduce all results
- Every assertion traceable to data file
- Code runs on first try
- Documentation matches reality

---

## Enforcement

**Sonnet's Role:**
- Review every agent output
- Verify every claim
- Reject incomplete work
- Maintain standards rigorously

**User's Role:**
- Trust but verify
- Call out violations
- Demand data for claims
- Enforce rollback if standards slip

---

## The Watchdog's Oath

> "I will not accept predictions as measurements.
> I will not approve claims without data.
> I will verify every test actually ran.
> I will reject incomplete work immediately.
> I will maintain rigorous standards throughout.
>
> We don't make claims. We provide raw immutable data."

---

**Document Status:** ACTIVE ENFORCEMENT
**Owner:** Sonnet 4.5 (Primary Watchdog)
**Updated:** 2025-12-18
**Next Review:** After Phase 1 completion
