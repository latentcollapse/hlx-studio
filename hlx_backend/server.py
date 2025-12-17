"""
HLX Dev Studio Backend Server
FastAPI server exposing HLX runtime operations.

Port: 58300 (local-only)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hlx_backend.routes import runtime, observer, hlxl, claude_control
from hlx_backend.auth import auth_manager

# Create FastAPI app
app = FastAPI(
    title="HLX Dev Studio API",
    description="Backend API for HLX Dev Studio - exposes HLX runtime operations and Claude control",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration (local only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:1420",  # Tauri dev port
        "http://localhost:5173",  # Vite dev port
        "tauri://localhost",      # Tauri production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(runtime.router)
app.include_router(observer.router)
app.include_router(hlxl.router)
app.include_router(claude_control.router)


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "name": "HLX Dev Studio API",
        "version": "0.1.0",
        "status": "ok",
        "endpoints": {
            "docs": "/docs",
            "runtime": "/hlx",
            "observer": "/observer/ws",
            "hlxl": "/hlxl",
            "claude": "/claude"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    from hlx_backend.hlx_bridge import hlx_bridge
    from hlx_backend.routes.observer import observer_manager

    return {
        "status": "healthy",
        "hlx_runtime": "available" if hlx_bridge.available else "stub",
        "observer": {
            "active_connections": len(observer_manager.connections),
            "total_events": len(observer_manager.event_history)
        }
    }


def start_server(host: str = "127.0.0.1", port: int = 58300):
    """
    Start the FastAPI server.

    Args:
        host: Host to bind to (default: 127.0.0.1 - local only)
        port: Port to bind to (default: 58300)
    """
    print(f"""
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q   HLX Dev Studio Backend Server              Q
Q   Version: 0.1.0                              Q
Q   Port: {port}                                  Q
Q   Local-only: {host}                    Q
ZPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP]

API Documentation: http://{host}:{port}/docs
WebSocket Observer: ws://{host}:{port}/observer/ws

Press Ctrl+C to stop
""")

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )


if __name__ == "__main__":
    start_server()
