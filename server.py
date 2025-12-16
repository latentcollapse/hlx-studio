import json
import os
import sys
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List

# Ensure we can import hlx_runtime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hlx_runtime.hlxl_parser import Parser, ContractExpr, ExpressionStatement, StringLiteral, IntegerLiteral, FloatLiteral, ArrayExpr
from hlx_runtime.ui_contracts import UI_CONTRACT_NAMES

# Reverse mapping for debug/display
UI_CONTRACT_IDS = {v: k for k, v in UI_CONTRACT_NAMES.items()}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Project Root for Sandboxing
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HLXL_PATH = os.path.join(os.path.dirname(__file__), "studio.hlxl")

# Mount static files to serve index.css/index.js
app.mount("/static", StaticFiles(directory=os.path.dirname(__file__)), name="static")

class RealCompiler:
    def __init__(self, hlxl_file_path: str):
        self.hlxl_file_path = hlxl_file_path

    def _resolve_literal(self, node):
        if isinstance(node, StringLiteral): return node.value
        if isinstance(node, IntegerLiteral): return node.value
        if isinstance(node, FloatLiteral): return node.value
        return None

    def _ast_to_json(self, node):
        """Recursively converts AST ContractExpr nodes to JSON for the frontend."""
        if isinstance(node, ContractExpr):
            # Basic structure
            contract_name = UI_CONTRACT_IDS.get(node.contract_id, f"UNKNOWN_{node.contract_id}")
            data = {
                "type": contract_name,
                "children": []
            }
            
            # Process fields
            for field_name, field_expr in node.fields.items():
                # If field is 'child' or 'children', we handle recursively
                if field_name in ['child', 'children']:
                    if isinstance(field_expr, ContractExpr):
                        data["children"].append(self._ast_to_json(field_expr))
                    elif isinstance(field_expr, ArrayExpr):
                        for elem in field_expr.elements:
                            if isinstance(elem, ContractExpr):
                                data["children"].append(self._ast_to_json(elem))
                else:
                    # It's a property
                    if isinstance(field_expr, ArrayExpr):
                        # Handle list of strings (e.g., tabs: ["A", "B"])
                        val_list = []
                        for elem in field_expr.elements:
                            val = self._resolve_literal(elem)
                            if val is not None: val_list.append(val)
                        data[field_name] = val_list
                    else:
                        val = self._resolve_literal(field_expr)
                        if val is not None:
                            data[field_name] = val
                        else:
                            data[field_name] = str(field_expr) # Fallback

            return data
        return None

    def compile(self) -> dict:
        if not os.path.exists(self.hlxl_file_path):
            return {"error": "File not found"}

        try:
            with open(self.hlxl_file_path, 'r') as f:
                source = f.read()
            
            # Parse!
            parser = Parser.from_source(source)
            ast = parser.parse()
            
            # Walk AST to find the root UI element (first ExpressionStatement that is a UI Contract)
            root_ui = None
            if hasattr(ast, 'statements'):
                for stmt in ast.statements:
                    if isinstance(stmt, ExpressionStatement) and isinstance(stmt.expression, ContractExpr):
                        # Found a top-level UI contract
                        root_ui = self._ast_to_json(stmt.expression)
                        break 
            
            return root_ui if root_ui else {"error": "No UI Contract found in studio.hlxl"}

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"error": str(e)}

compiler = RealCompiler(HLXL_PATH)

# --- Compiler Endpoints ---

@app.get("/render")
async def render_ui():
    return compiler.compile()

@app.post("/action")
async def handle_action(payload: Dict[str, Any]):
    print(f"Action received: {payload}")
    return {"status": "ok", "received": payload}

# --- File System Endpoints ---

class ReadFileRequest(BaseModel):
    path: str
    
class SaveFileRequest(BaseModel):
    path: str
    content: str

def _get_safe_path(req_path: str):
    # SECURITY: Prevent directory traversal using realpath (resolves all symlinks)
    req_path = req_path.strip("/")
    full_path = os.path.join(PROJECT_ROOT, req_path)

    # Resolve symlinks and relative paths to canonical form
    resolved_path = os.path.realpath(full_path)
    resolved_root = os.path.realpath(PROJECT_ROOT)

    # Ensure resolved path is within project root (with proper separator handling)
    if not (resolved_path == resolved_root or resolved_path.startswith(resolved_root + os.sep)):
        raise HTTPException(403, "Access denied")

    return full_path

@app.get("/api/files")
async def list_files(path: str = "."):
    try:
        full_path = _get_safe_path(path)
        if not os.path.isdir(full_path):
            return []
        
        entries = []
        for entry in sorted(os.listdir(full_path)):
            # Skip hidden files
            if entry.startswith("."): continue
            
            entry_path = os.path.join(full_path, entry)
            is_dir = os.path.isdir(entry_path)
            
            # Return relative path from project root
            rel_path = os.path.relpath(entry_path, PROJECT_ROOT)
            
            entries.append({
                "name": entry,
                "path": rel_path,
                "type": "directory" if is_dir else "file"
            })
        
        # Sort directories first
        entries.sort(key=lambda x: (x["type"] != "directory", x["name"]))
        return entries
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/api/read")
async def read_file(request: ReadFileRequest):
    try:
        full_path = _get_safe_path(request.path)
        if not os.path.isfile(full_path):
            raise HTTPException(404, "File not found")
            
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content}
    except UnicodeDecodeError:
         return {"content": "<< Binary File >>"}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/api/save")
async def save_file(request: SaveFileRequest):
    try:
        full_path = _get_safe_path(request.path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(request.content)
        return {"status": "saved", "path": request.path}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/api/compile_model")
async def compile_model(request: ReadFileRequest):
    try:
        # Validate path
        model_path = _get_safe_path(request.path)
        if not model_path.endswith(".onnx"):
            raise HTTPException(400, "Only .onnx files can be compiled")

        # Construct command
        # We assume the tool is at tools/hlx_model_compiler.py relative to PROJECT_ROOT
        tool_path = os.path.join(PROJECT_ROOT, "tools", "hlx_model_compiler.py")
        python_exe = sys.executable # Use current venv python

        # Run Subprocess
        proc = await asyncio.create_subprocess_exec(
            python_exe, tool_path, model_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30.0)
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except:
                pass
            raise HTTPException(504, "Compilation timed out after 30 seconds")
        
        if proc.returncode != 0:
            raise HTTPException(500, f"Compilation failed:\n{stderr.decode()}")

        # Parse the JSON output from the tool
        try:
            result_json = json.loads(stdout.decode())
            
            # Save the contract file next to the model
            contract_path = model_path.replace(".onnx", "_contract.json")
            with open(contract_path, "w") as f:
                json.dump(result_json, f, indent=2)
                
            return {
                "status": "success", 
                "contract_path": os.path.relpath(contract_path, PROJECT_ROOT),
                "data": result_json
            }
        except json.JSONDecodeError:
             raise HTTPException(500, f"Tool output invalid JSON:\n{stdout.decode()}")

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(500, str(e))

# --- Terminal WebSocket ---

import secrets
import time

# SECURITY: Token-based WebSocket authentication
TERMINAL_ENABLED = True  # Re-enabled with authentication
VALID_TOKENS = {}  # token -> expiration_timestamp
TOKEN_EXPIRY_SECONDS = 300  # 5 minutes

class TokenRequest(BaseModel):
    pass

@app.post("/api/terminal_token")
async def get_terminal_token(request: TokenRequest = None):
    """Generate a time-limited auth token for WebSocket terminal access."""
    token = secrets.token_urlsafe(32)
    expiration = time.time() + TOKEN_EXPIRY_SECONDS
    VALID_TOKENS[token] = expiration
    return {"token": token, "expires_in": TOKEN_EXPIRY_SECONDS}

def validate_token(token: str) -> bool:
    """Check if token is valid and not expired."""
    if token not in VALID_TOKENS:
        return False
    if time.time() > VALID_TOKENS[token]:
        del VALID_TOKENS[token]
        return False
    return True

@app.websocket("/ws/terminal")
async def terminal_ws(websocket: WebSocket, token: str = None):
    # SECURITY: Validate token before accepting connection
    if not token or not validate_token(token):
        await websocket.close(code=1008, reason="Unauthorized: Invalid or missing auth token")
        return

    # SECURITY: Consume token after validation (one-time use)
    del VALID_TOKENS[token]

    await websocket.accept()
    shell = "powershell.exe" if sys.platform == "win32" else "bash"
    
    try:
        # Create subprocess
        process = await asyncio.create_subprocess_shell(
            shell,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Pipe stdout/stderr -> WebSocket
        async def pipe_stream(stream, ws):
            while True:
                data = await stream.read(4096)
                if not data: break
                try:
                    await ws.send_bytes(data)
                except Exception:
                    break

        # Pipe WebSocket -> stdin
        async def pipe_ws(ws, proc_stdin):
            try:
                while True:
                    data = await ws.receive_bytes()
                    proc_stdin.write(data)
                    await proc_stdin.drain()
            except WebSocketDisconnect:
                pass
            except Exception:
                pass

        await asyncio.gather(
            pipe_stream(process.stdout, websocket),
            pipe_stream(process.stderr, websocket),
            pipe_ws(websocket, process.stdin)
        )
    except Exception as e:
        print(f"Terminal error: {e}")
    finally:
        if process.returncode is None:
            try:
                process.kill()
            except: pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)