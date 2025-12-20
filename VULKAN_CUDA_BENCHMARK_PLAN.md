# Vulkan vs CUDA ML Benchmark Suite
## Formal Performance Validation for HLX Substrate

**Date:** 2025-12-20
**Hardware:** RTX 3060 (8GB VRAM)
**Purpose:** Generate hard data for HLX substrate performance claims
**Status:** Planning Phase

---

## Objectives

1. **Validate HLX+Vulkan performance** against CUDA on ML workloads
2. **Generate reproducible benchmarks** for publication and LLC formation
3. **Identify performance characteristics** for HelinuxOS development
4. **Document baseline** for future optimizations

---

## Benchmark Categories

### Category 1: Matrix Operations (Foundation)

**Why:** Core building block of all ML workloads

**Benchmarks:**
1. **GEMM (General Matrix Multiply)**
   - Sizes: 256×256, 512×512, 1024×1024, 2048×2048
   - Precision: FP32, FP16 (if supported)
   - Metrics: GFLOPS, latency (ms), memory bandwidth (GB/s)
   - Baseline: cuBLAS SGEMM, PyTorch matmul

2. **Batched GEMM**
   - Batch sizes: 1, 4, 16, 64
   - Matrix size: 512×512
   - Metrics: Throughput (ops/sec), warm-start latency
   - Tests HLX content-addressed caching advantage

### Category 2: ML Inference Primitives

**Why:** Real-world ML operations

**Benchmarks:**
1. **Convolution (conv2d)**
   - Input: 224×224×3 (ImageNet size)
   - Kernels: 3×3, 5×5, 7×7
   - Channels: 64, 128, 256
   - Metrics: Images/sec, latency, memory usage

2. **Activation Functions**
   - Operations: ReLU, GeLU, Softmax
   - Batch sizes: 1, 16, 64, 256
   - Tensor size: 512×512
   - Metrics: GB/s throughput, latency

3. **Layer Normalization**
   - Sequence lengths: 128, 512, 2048 (transformer sizes)
   - Hidden dim: 768, 1024, 2048
   - Metrics: Tokens/sec, memory efficiency

### Category 3: End-to-End Inference

**Why:** Validate complete pipeline performance

**Benchmarks:**
1. **Helix 5.1B ASCII Specialist**
   - Test set: 100 HLX samples (HLXL/LC-T)
   - Backends: HLX+Vulkan, PyTorch+CUDA
   - Metrics:
     - Inference time per sample (ms)
     - Throughput (samples/sec)
     - Memory usage (peak/average)
     - Accuracy (should be identical)

2. **Small CNN (ResNet-18)**
   - Dataset: 1000 ImageNet validation images
   - Backends: HLX+Vulkan, PyTorch+CUDA
   - Metrics: Images/sec, total time, power usage

### Category 4: Memory Operations

**Why:** Understand memory bottlenecks

**Benchmarks:**
1. **Memory Transfer**
   - CPU→GPU, GPU→CPU
   - Sizes: 1MB, 10MB, 100MB, 1GB
   - Metrics: Bandwidth (GB/s), latency

2. **Memory Allocation**
   - Allocate/free cycles: 1000 iterations
   - Sizes: 1MB, 10MB, 100MB
   - Metrics: Allocation time, fragmentation

### Category 5: Determinism & Caching

**Why:** HLX's unique advantage

**Benchmarks:**
1. **Shader Cache Performance**
   - Test: Load same shader 1000 times
   - Measure: First load (cold) vs subsequent (warm)
   - Expected: HLX shows 10-100× speedup on cache hits

2. **Deterministic Execution**
   - Test: Same input 1000 times
   - Verify: Bit-identical outputs every time
   - Compare: CUDA (expected to fail due to non-deterministic atomics)

---

## Benchmark Implementation

### File Structure
```
/home/matt/hlx-dev-studio/benchmarks/
├── README.md
├── run_all_benchmarks.py           # Master script
├── category1_matrix/
│   ├── gemm_benchmark.py
│   ├── batched_gemm_benchmark.py
│   └── results/
├── category2_ml_primitives/
│   ├── conv2d_benchmark.py
│   ├── activation_benchmark.py
│   ├── layernorm_benchmark.py
│   └── results/
├── category3_inference/
│   ├── helix_5b_benchmark.py
│   ├── resnet18_benchmark.py
│   └── results/
├── category4_memory/
│   ├── memory_transfer_benchmark.py
│   ├── memory_allocation_benchmark.py
│   └── results/
└── category5_determinism/
    ├── cache_benchmark.py
    ├── determinism_benchmark.py
    └── results/
```

### Result Format (JSON)

```json
{
  "benchmark_id": "gemm_1024_fp32",
  "timestamp": "2025-12-20T12:00:00Z",
  "hardware": {
    "gpu": "NVIDIA GeForce RTX 3060",
    "vram": "8GB",
    "driver": "550.120",
    "cuda_version": "12.4",
    "vulkan_version": "1.3.275"
  },
  "backends": {
    "hlx_vulkan": {
      "mean_time_ms": 12.34,
      "std_time_ms": 0.45,
      "min_time_ms": 11.89,
      "max_time_ms": 13.21,
      "gflops": 1234.56,
      "memory_mb": 48.2,
      "runs": 100
    },
    "pytorch_cuda": {
      "mean_time_ms": 11.87,
      "std_time_ms": 0.38,
      "min_time_ms": 11.42,
      "max_time_ms": 12.65,
      "gflops": 1287.34,
      "memory_mb": 52.1,
      "runs": 100
    }
  },
  "comparison": {
    "vulkan_vs_cuda_ratio": 1.04,
    "percentage_of_cuda": "96.2%",
    "verdict": "Within 5% of CUDA (excellent)"
  }
}
```

---

## Success Criteria

### Tier 1: Acceptable (MVP for LLC formation)
- **Matrix ops:** Within 90% of CUDA performance
- **ML primitives:** Within 85% of CUDA performance
- **Inference:** Within 90% of CUDA performance
- **Determinism:** 100% reproducible (CUDA cannot match this)

### Tier 2: Competitive (Industry-ready)
- **Matrix ops:** Within 95% of CUDA performance
- **ML primitives:** Within 90% of CUDA performance
- **Inference:** Within 95% of CUDA performance
- **Memory:** Match or exceed CUDA bandwidth

### Tier 3: Superior (Game-changer)
- **Cache hits:** 10-100× faster than CUDA recompilation
- **Determinism:** 100% reproducible, CUDA 0%
- **Power:** Lower power consumption than CUDA

---

## Execution Plan

### Phase 1: Infrastructure (1-2 days)
- [ ] Create benchmark directory structure
- [ ] Write master benchmark runner
- [ ] Implement result logging (JSON + CSV)
- [ ] Set up power monitoring (nvidia-smi)

### Phase 2: Core Benchmarks (2-3 days)
- [ ] Category 1: Matrix operations
- [ ] Category 2: ML primitives
- [ ] Category 4: Memory operations

### Phase 3: Inference Benchmarks (2-3 days)
- [ ] Helix 5.1B specialist inference
- [ ] ResNet-18 inference
- [ ] End-to-end pipeline validation

### Phase 4: Determinism Proofs (1 day)
- [ ] Cache performance validation
- [ ] Deterministic execution tests
- [ ] CUDA comparison (show non-determinism)

### Phase 5: Analysis & Documentation (1 day)
- [ ] Generate summary report
- [ ] Create performance graphs
- [ ] Write findings paper
- [ ] Update repo with verified claims

**Total:** 7-10 days for complete formal validation

---

## Power Monitoring

### Tools
```bash
# Monitor GPU power during benchmarks
nvidia-smi --query-gpu=power.draw,utilization.gpu,memory.used \
  --format=csv -l 1 > benchmark_power.csv

# Compare total energy consumption
# HLX advantage: Fewer recompilations = lower total energy
```

---

## Reproducibility

### Docker Container (Future)
```dockerfile
FROM nvidia/cuda:12.4-base-ubuntu22.04
RUN apt-get update && apt-get install -y \
    vulkan-tools \
    vulkan-validationlayers-dev \
    python3-pip
COPY benchmarks/ /benchmarks/
RUN pip install -r /benchmarks/requirements.txt
CMD ["python3", "/benchmarks/run_all_benchmarks.py"]
```

### Published Results
- All raw JSON results committed to repo
- CSV summary for easy analysis
- Graphs (PNG) showing comparisons
- Full reproduction instructions

---

## Claims We Can Make (After Benchmarks)

**IF we achieve 90-95% CUDA performance:**
- "HLX+Vulkan achieves 90-95% of CUDA performance on ML workloads"
- "Near-CUDA performance with 100% deterministic execution"
- "Portable across NVIDIA/AMD/Intel GPUs via Vulkan"

**IF we achieve cache speedups:**
- "10-100× faster warm-start inference via content-addressed caching"
- "Zero kernel recompilation overhead on repeated operations"

**IF we achieve determinism:**
- "100% reproducible ML inference (bit-identical results)"
- "CUDA cannot guarantee determinism due to non-associative floating-point ops"

---

## Next Steps

1. **Finish ASCII specialist training** (~20 minutes to epoch 100)
2. **Save checkpoint and evaluate accuracy** on test set
3. **Build Category 1 benchmarks** (matrix ops, 1 day)
4. **Run baseline CUDA benchmarks** (establish ground truth)
5. **Implement HLX+Vulkan backend** for each benchmark
6. **Compare and document** results with hard data

---

**Status:** Ready to begin implementation
**Priority:** High (required for LLC formation and publication)
**Owner:** Matt + Claude
**Timeline:** Start after training completes, complete within 10 days
