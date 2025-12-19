# HLX Development Studio

Complete development environment for the HLX language and runtime.

[![Status](https://img.shields.io/badge/status-active-blue)]()
[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()

## Overview

HLX Development Studio is a web-based and native desktop environment for:
- Writing HLXL (HLX Language) code
- Exploring contracts and specifications
- Visualizing system architecture
- Debugging and profiling runtime execution
- Managing AI model training

## Organization

For complete repository structure details, see [REPO_STRUCTURE.md](/home/matt/REPO_STRUCTURE.md).

### Frontend (`frontend/`)
Web application built with React, TypeScript, and Vite.

**Key Features:**
- Dashboard with system overview
- HLXL Playground - Interactive code editor
- Contract Explorer - Browse all contract specifications
- Architecture Visualizer - System design explorer
- Core Runtime Designer - Configure runtime behavior
- Latent Space Designer - Explore latent space operations

**Build & Development:**
```bash
cd frontend
bun install
bun run dev      # Start development server
bun run build    # Production build
```

### Backend (`backend/`)
Backend services including Tauri desktop application.

**Components:**
- **src-tauri/** - Native desktop app (Rust)
- **Python Services** - Corpus loading, API testing, integration

```bash
cd backend/src-tauri
cargo build --release    # Build desktop app
```

### Documentation (`docs/`)
Project documentation and specifications.

### Archive (`_archive/`)
Historical documentation, design phases, and archived specifications.

## Quick Start

### Web Interface

```bash
cd frontend
bun install
bun run dev
# Open http://localhost:5173
```

### Desktop Application

```bash
cd backend/src-tauri
npm install
npm run tauri dev
```

### Python Services

```bash
cd backend
python load_corpus.py      # Load training corpus
pytest test_*.py           # Run integration tests
```

## Key Views

| View | Purpose |
|------|---------|
| **Dashboard** | System statistics and overview |
| **HLXLPlayground** | Interactive HLXL code editor with execution |
| **ContractExplorer** | Browse all contract specifications |
| **HLXVisualizer** | Visual representation of architecture |
| **CoreRuntimeDesigner** | Runtime configuration interface |
| **LatentSpaceDesigner** | Latent space exploration and visualization |
| **BinaryExplainer** | LC-B wire format analyzer |
| **ErrorTaxonomy** | Error types and handling guide |

## Technology Stack

### Frontend
- **Framework** - React 18+
- **Language** - TypeScript
- **Build** - Vite
- **Styling** - Tailwind CSS
- **Package Manager** - Bun

### Backend
- **Desktop** - Tauri + Rust
- **Services** - Python 3.8+
- **APIs** - Claude, Ollama integration

### Testing
- **Unit Tests** - Python unittest/pytest
- **Integration** - End-to-end scenarios

## Architecture

```
hlx-dev-studio/
├── frontend/            # Web UI (React + TypeScript)
│   ├── views/          # Page components
│   ├── components/     # Reusable components
│   ├── services/       # API clients
│   └── utils/          # Utilities
├── backend/            # Services layer
│   ├── src-tauri/      # Native desktop app
│   └── Python APIs/    # Integration services
├── docs/               # Documentation
└── _archive/           # Historical materials
```

## Development

### Code Organization

**Frontend Module Structure:**
```typescript
frontend/
├── views/              # Page-level components
├── components/         # Reusable UI components
├── services/           # API and business logic
├── utils/             # Helper functions
├── config/            # Configuration
└── types.ts           # TypeScript types
```

**Backend Modules:**
```
backend/
├── src-tauri/         # Tauri desktop app
├── load_corpus.py     # Corpus utilities
└── test_*.py          # Integration tests
```

### Running Tests

```bash
# Frontend tests
cd frontend
bun run test

# Backend/Python tests
cd backend
pytest test_*.py -v
```

## Environment Configuration

Frontend environment variables (`.env.local`):
```
VITE_API_URL=http://localhost:3000
VITE_OLLAMA_HOST=http://localhost:11434
```

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### Bun Installation Issues
```bash
# Clear bun cache
bun pm cache rm
bun install --force
```

### Tauri Build Failures
```bash
# Clean build
cd backend/src-tauri
cargo clean
cargo build --release
```

## Contributing

1. Check existing issues and PRs
2. Create feature branch: `git checkout -b feature/name`
3. Make changes and test thoroughly
4. Submit PR with description

## Documentation

- **Frontend Guide** - `frontend/README.md`
- **Backend Guide** - `backend/README.md`
- **Architecture** - See `_archive/` for phase documentation
- **Overall Structure** - `/home/matt/REPO_STRUCTURE.md`

## License

Dual-licensed under MIT or Apache-2.0

## Related Projects

- **HLX Runtime** - Core language and runtime
- **HLX+Vulkan** - GPU compute backend
- **HLX Corpus** - Teaching materials

## Support

For issues and questions:
1. Check documentation
2. Review archived design documents
3. Run tests to verify your setup
4. Check git history for related changes

---

**Version:** 1.1.0 (Active Development)
**Last Updated:** 2025-12-17
