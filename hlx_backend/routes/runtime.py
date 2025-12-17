"""
HLX Runtime API Routes
Endpoints for collapse, resolve, execute operations.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Optional
import sys
from pathlib import Path

# Add parent directory to import hlx_bridge
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from hlx_backend.hlx_bridge import hlx_bridge, HLXError
from hlx_backend.routes.observer import observer_manager

router = APIRouter(prefix="/hlx", tags=["runtime"])


class CollapseRequest(BaseModel):
    value: Any
    emit_event: bool = True


class CollapseResponse(BaseModel):
    handle: str
    hash: str


class ResolveRequest(BaseModel):
    handle: str
    emit_event: bool = True


class ResolveResponse(BaseModel):
    value: Any


class ExecuteRequest(BaseModel):
    operation: str
    arguments: dict
    emit_event: bool = True


class ExecuteResponse(BaseModel):
    result: Any
    handle: Optional[str] = None


@router.post("/collapse", response_model=CollapseResponse)
async def collapse(req: CollapseRequest):
    """
    Collapse a value to a content-addressed handle.

    Example:
        POST /hlx/collapse
        {
            "value": {"@0": 123},
            "emit_event": true
        }

        Response:
        {
            "handle": "&h_abc123...",
            "hash": "abc123..."
        }
    """
    try:
        # Emit observer event
        if req.emit_event:
            await observer_manager.emit("collapse", {
                "operation": "collapse",
                "value": req.value
            })

        # Perform collapse
        handle = hlx_bridge.collapse_value(req.value)
        hash_value = hlx_bridge.compute_hash(req.value)

        # Emit completion event
        if req.emit_event:
            await observer_manager.emit("collapse_complete", {
                "operation": "collapse",
                "handle": handle,
                "hash": hash_value
            })

        return CollapseResponse(handle=handle, hash=hash_value)

    except HLXError as e:
        if req.emit_event:
            await observer_manager.emit("error", {
                "operation": "collapse",
                "error": str(e)
            })
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if req.emit_event:
            await observer_manager.emit("error", {
                "operation": "collapse",
                "error": f"Unexpected error: {str(e)}"
            })
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/resolve", response_model=ResolveResponse)
async def resolve(req: ResolveRequest):
    """
    Resolve a handle to its value.

    Example:
        POST /hlx/resolve
        {
            "handle": "&h_abc123...",
            "emit_event": true
        }

        Response:
        {
            "value": {"@0": 123}
        }
    """
    try:
        # Emit observer event
        if req.emit_event:
            await observer_manager.emit("resolve", {
                "operation": "resolve",
                "handle": req.handle
            })

        # Perform resolve
        value = hlx_bridge.resolve_handle(req.handle)

        # Emit completion event
        if req.emit_event:
            await observer_manager.emit("resolve_complete", {
                "operation": "resolve",
                "handle": req.handle,
                "value": value
            })

        return ResolveResponse(value=value)

    except HLXError as e:
        if req.emit_event:
            await observer_manager.emit("error", {
                "operation": "resolve",
                "error": str(e)
            })
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if req.emit_event:
            await observer_manager.emit("error", {
                "operation": "resolve",
                "error": f"Unexpected error: {str(e)}"
            })
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/execute", response_model=ExecuteResponse)
async def execute(req: ExecuteRequest):
    """
    Execute a general HLX operation.

    Example:
        POST /hlx/execute
        {
            "operation": "hash",
            "arguments": {
                "value": {"@0": 123}
            },
            "emit_event": true
        }

        Response:
        {
            "result": "abc123...",
            "handle": null
        }
    """
    try:
        # Emit observer event
        if req.emit_event:
            await observer_manager.emit("execute", {
                "operation": req.operation,
                "arguments": req.arguments
            })

        # Determine operation
        result = None
        handle = None

        if req.operation == "hash":
            result = hlx_bridge.compute_hash(req.arguments.get("value"))
        elif req.operation == "encode":
            result = hlx_bridge.encode_to_lcb(req.arguments.get("value")).hex()
        elif req.operation == "decode":
            hex_data = req.arguments.get("data")
            binary_data = bytes.fromhex(hex_data)
            result = hlx_bridge.decode_from_lcb(binary_data)
        elif req.operation == "validate_contract":
            result = hlx_bridge.validate_contract(req.arguments.get("contract"))
        else:
            raise ValueError(f"Unknown operation: {req.operation}")

        # Emit completion event
        if req.emit_event:
            await observer_manager.emit("execute_complete", {
                "operation": req.operation,
                "result": result
            })

        return ExecuteResponse(result=result, handle=handle)

    except (HLXError, ValueError) as e:
        if req.emit_event:
            await observer_manager.emit("error", {
                "operation": req.operation,
                "error": str(e)
            })
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if req.emit_event:
            await observer_manager.emit("error", {
                "operation": req.operation,
                "error": f"Unexpected error: {str(e)}"
            })
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/status")
async def get_status():
    """
    Get runtime status.

    Returns:
        dict: Status information
    """
    return {
        "status": "ok",
        "hlx_available": hlx_bridge.available,
        "version": "0.1.0"
    }
