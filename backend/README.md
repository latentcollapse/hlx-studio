# Backend

Backend services and Tauri desktop application for HLX Development Studio.

## Contents

- **src-tauri/** - Tauri desktop application
  - **src/** - Rust backend code
  - **Cargo.toml** - Rust dependencies
  - **tauri.conf.json** - Tauri configuration

- **Python Services**
  - **load_corpus.py** - Corpus data loading utilities
  - **test_backend_api.py** - Backend API tests
  - **test_brain.py** - Brain/AI component tests
  - **test_claude_api.py** - Claude API integration tests

## Tauri Desktop App

The Tauri application provides a native desktop interface for HLX Development Studio with:
- Rust backend for performance-critical operations
- Full OS integration (file system access, native menus, etc.)
- Cross-platform support (Windows, macOS, Linux)

### Building

```bash
cd src-tauri
cargo build --release
```

## Python Services

Test and utility scripts for backend functionality:

```bash
# Load corpus data
python load_corpus.py

# Run backend tests
pytest test_backend_api.py
pytest test_brain.py
pytest test_claude_api.py
```
