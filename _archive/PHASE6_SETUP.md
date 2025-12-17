# Phase 6: Brain Setup Instructions

## System Requirements (✓ Verified)
- RTX 5060 (8GB VRAM) ✓
- 31GB RAM ✓
- 178GB free disk space ✓

## Installation Steps

### 1. Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

This will prompt for sudo password to install to `/usr/local`.

### 2. Start Ollama Service
```bash
ollama serve
```

Leave this running in a terminal. It starts on `http://localhost:11434`.

### 3. Download Qwen2.5-Coder-7B (Quantized)
```bash
# In a new terminal:
ollama pull qwen2.5-coder:7b-instruct-q4_K_M
```

This downloads ~4.7GB. The quantized version fits comfortably in 8GB VRAM.

### 4. Test the Model
```bash
ollama run qwen2.5-coder:7b-instruct "Write a Python function to calculate fibonacci"
```

You should see a code response within a few seconds.

### 5. Verify API Access
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder:7b-instruct-q4_K_M",
  "prompt": "What is HLX?",
  "stream": false
}'
```

## What's Next

Once Ollama is installed and the model is downloaded, the brain infrastructure code is ready to be implemented:

- **hlx_brain/ollama_client.py** - Python client for Ollama API
- **hlx_brain/rag.py** - RAG system with ChromaDB
- **hlx_brain/brain.py** - Unified brain interface
- **hlx_backend/routes/brain.py** - FastAPI endpoints
- **views/BrainChat.tsx** - Chat UI

## Alternative: Use Existing Installation

If Ollama is already installed elsewhere, you can point to it:
```python
client = OllamaClient(base_url="http://your-ollama-server:11434")
```

## Estimated Costs
- Ollama: Free
- Model download: ~10 minutes on good connection
- Disk space: ~5GB
- First-time inference: ~5-10 seconds (loading model into VRAM)
- Subsequent inference: ~1-3 seconds

## Full Documentation
See `/home/matt/.claude/plans/phase6-9-brain-integration.md` for the complete integration plan.

---

## ✓ PHASE 6 COMPLETE (2025-12-17)

### What Was Installed
- **Ollama Version**: 0.13.4
- **Model**: qwen3:8b (5.2 GB)
- **Service URL**: http://localhost:11434
- **Installation Method**: sudo password "0000" via curl script

### Verification Results
```bash
# Model list
$ ollama list
NAME        ID              SIZE      MODIFIED
qwen3:8b    500a1f067a9f    5.2 GB    About a minute ago

# API test
$ curl -s http://localhost:11434/api/generate -d '{
  "model": "qwen3:8b",
  "prompt": "What is 2+2?",
  "stream": false
}'
# Response: "The sum of 2 and 2 is **4**." (with chain-of-thought reasoning)

# Performance
- First load: ~10-15 seconds (loading weights to VRAM)
- Subsequent queries: ~3-5 seconds
- VRAM usage: ~5.2 GB (fits comfortably in 8GB)
```

### Deviations from Plan
- **Model**: Used `qwen3:8b` instead of `qwen2.5-coder:7b-instruct-q4_K_M`
  - Reason: User requested 8B model specifically
  - Size: 5.2 GB (vs planned 4.7 GB, still fits in 8GB VRAM)
  - Capabilities: General purpose model with strong reasoning

### Next Steps (Phase 7)
Ready to implement RAG system:
1. Install ChromaDB: `pip install chromadb`
2. Download embedding model: `ollama pull nomic-embed-text`
3. Create `/home/matt/hlx-dev-studio/hlx_brain/` directory structure
4. Implement RAG pipeline with HLX corpus ingestion
