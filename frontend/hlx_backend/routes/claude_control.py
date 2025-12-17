"""
Claude API Control Routes
Endpoints for Claude or other automation to control the HLX Studio.
Provides batch operations, test iteration, compilation, and status endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Any, List, Optional, Dict
import time
import sys
from pathlib import Path

# Add parent directory imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from hlx_backend.hlx_bridge import hlx_bridge, HLXError
from hlx_backend.routes.observer import observer_manager
from hlx_backend.auth import auth_manager

router = APIRouter(prefix="/claude", tags=["claude_control"])


# ============================================================================
# Request/Response Models
# ============================================================================


class BatchOperation(BaseModel):
    """A single operation in a batch."""

    type: str = Field(..., description="Operation type: collapse, resolve, execute")
    value: Optional[Any] = Field(None, description="Value for collapse operations")
    handle: Optional[str] = Field(None, description="Handle for resolve operations")
    operation: Optional[str] = Field(None, description="Operation name for execute")
    arguments: Optional[Dict[str, Any]] = Field(None, description="Arguments for execute")


class BatchRequest(BaseModel):
    """Batch operations request."""

    operations: List[BatchOperation] = Field(..., description="List of operations")
    emit_events: bool = Field(
        True, description="Emit events to observer for each operation"
    )


class BatchResult(BaseModel):
    """Result of a single batch operation."""

    success: bool = Field(..., description="Whether operation succeeded")
    result: Optional[Any] = Field(None, description="Operation result if successful")
    error: Optional[str] = Field(None, description="Error message if failed")
    execution_time: float = Field(..., description="Time taken in seconds")


class BatchResponse(BaseModel):
    """Response from batch operations."""

    results: List[BatchResult] = Field(..., description="Results for each operation")
    total: int = Field(..., description="Total operations")
    succeeded: int = Field(..., description="Number succeeded")
    failed: int = Field(..., description="Number failed")
    total_time: float = Field(..., description="Total time in seconds")


class TestIterationRequest(BaseModel):
    """Test iteration request."""

    test_code: str = Field(..., description="HLX code to test")
    expected_output: Optional[Dict[str, Any]] = Field(
        None, description="Expected output for comparison"
    )
    iterations: int = Field(1, ge=1, le=100, description="Number of iterations")


class IterationResult(BaseModel):
    """Single iteration result."""

    iteration: int = Field(..., description="Iteration number")
    passed: bool = Field(..., description="Whether test passed")
    output: Optional[Any] = Field(None, description="Test output")
    error: Optional[str] = Field(None, description="Error if any")
    execution_time: float = Field(..., description="Execution time in seconds")


class TestIterationResponse(BaseModel):
    """Response from test iteration."""

    iteration: int = Field(..., description="Final iteration number")
    passed: bool = Field(..., description="Overall pass/fail")
    output: Optional[Any] = Field(None, description="Final output")
    execution_time: float = Field(..., description="Time for final iteration")
    all_iterations: List[IterationResult] = Field(..., description="All iteration results")
    summary: Dict[str, Any] = Field(..., description="Summary statistics")


class CompileRequest(BaseModel):
    """Code compilation request."""

    code: str = Field(..., description="HLXL source code")
    format: str = Field("hlxl", description="Code format (hlxl, etc)")


class CompileResponse(BaseModel):
    """Response from compilation."""

    success: bool = Field(..., description="Whether compilation succeeded")
    ast: Optional[Dict[str, Any]] = Field(None, description="Abstract syntax tree")
    lowered: Optional[Dict[str, Any]] = Field(None, description="Lowered IR")
    errors: List[str] = Field(..., description="Compilation errors")


class StatusResponse(BaseModel):
    """System status response."""

    backend: str = Field(..., description="Backend status")
    hlx_runtime: str = Field(..., description="HLX runtime status")
    observer: Dict[str, Any] = Field(..., description="Observer status")
    capabilities: List[str] = Field(..., description="Available capabilities")
    timestamp: str = Field(..., description="Status timestamp")


# ============================================================================
# Endpoint Implementations
# ============================================================================


@router.post("/batch", response_model=BatchResponse)
async def batch_operations(
    request: BatchRequest, token: str = Depends(auth_manager.require_token)
):
    """
    Execute multiple HLX operations in a batch.

    Operations can be: collapse, resolve, execute

    Args:
        request: BatchRequest with list of operations
        token: Authentication token

    Returns:
        BatchResponse with results for each operation
    """
    start_time = time.time()
    results: List[BatchResult] = []
    succeeded = 0
    failed = 0

    for op_idx, op in enumerate(request.operations):
        op_start = time.time()
        result: Optional[Any] = None
        error: Optional[str] = None
        success = False

        try:
            if op.type == "collapse":
                if op.value is None:
                    error = "collapse requires 'value' field"
                else:
                    handle = hlx_bridge.collapse_value(op.value)
                    hash_val = hlx_bridge.compute_hash(op.value)
                    result = {"handle": handle, "hash": hash_val}
                    success = True
                    if request.emit_events:
                        await observer_manager.emit(
                            "batch_operation",
                            {
                                "index": op_idx,
                                "type": "collapse",
                                "handle": handle,
                            },
                        )

            elif op.type == "resolve":
                if not op.handle:
                    error = "resolve requires 'handle' field"
                else:
                    value = hlx_bridge.resolve_handle(op.handle)
                    result = {"value": value}
                    success = True
                    if request.emit_events:
                        await observer_manager.emit(
                            "batch_operation",
                            {"index": op_idx, "type": "resolve", "handle": op.handle},
                        )

            elif op.type == "execute":
                if not op.operation or not op.arguments:
                    error = "execute requires 'operation' and 'arguments' fields"
                else:
                    # Stub implementation for execute
                    result = {
                        "operation": op.operation,
                        "status": "executed (stub)",
                        "arguments": op.arguments,
                    }
                    success = True
                    if request.emit_events:
                        await observer_manager.emit(
                            "batch_operation",
                            {
                                "index": op_idx,
                                "type": "execute",
                                "operation": op.operation,
                            },
                        )

            else:
                error = f"Unknown operation type: {op.type}"

        except HLXError as e:
            error = str(e)
        except Exception as e:
            error = f"Unexpected error: {str(e)}"

        if success:
            succeeded += 1
        else:
            failed += 1

        op_time = time.time() - op_start
        results.append(
            BatchResult(
                success=success, result=result, error=error, execution_time=op_time
            )
        )

    total_time = time.time() - start_time

    return BatchResponse(
        results=results,
        total=len(request.operations),
        succeeded=succeeded,
        failed=failed,
        total_time=total_time,
    )


@router.post("/test-iteration", response_model=TestIterationResponse)
async def test_iteration(
    request: TestIterationRequest, token: str = Depends(auth_manager.require_token)
):
    """
    Run a test iteration cycle (stub implementation).

    In production, this would:
    1. Write test code
    2. Compile it
    3. Execute
    4. Compare with expected output
    5. Report results

    Args:
        request: TestIterationRequest with test code and config
        token: Authentication token

    Returns:
        TestIterationResponse with iteration results
    """
    all_iterations: List[IterationResult] = []
    passed = False
    final_output = None
    final_time = 0.0

    for iteration in range(1, request.iterations + 1):
        iter_start = time.time()

        try:
            # Stub: Just hash the code to simulate execution
            code_hash = hlx_bridge.compute_hash({"code": request.test_code})
            output = {
                "iteration": iteration,
                "code_hash": code_hash,
                "status": "executed (stub)",
            }

            # Check if matches expected (stub logic)
            iter_passed = True
            if request.expected_output:
                iter_passed = code_hash is not None

            final_output = output
            passed = iter_passed

            await observer_manager.emit(
                "test_iteration",
                {
                    "iteration": iteration,
                    "passed": iter_passed,
                    "total_iterations": request.iterations,
                },
            )

        except Exception as e:
            output = None
            passed = False
            final_output = {"error": str(e)}

            await observer_manager.emit(
                "test_iteration_error",
                {
                    "iteration": iteration,
                    "error": str(e),
                    "total_iterations": request.iterations,
                },
            )

        iter_time = time.time() - iter_start
        final_time = iter_time
        all_iterations.append(
            IterationResult(
                iteration=iteration,
                passed=passed,
                output=output,
                error=None if passed else str(final_output),
                execution_time=iter_time,
            )
        )

    # Summary statistics
    passed_count = sum(1 for r in all_iterations if r.passed)
    summary = {
        "total_iterations": request.iterations,
        "passed": passed_count,
        "failed": request.iterations - passed_count,
        "success_rate": passed_count / request.iterations if request.iterations > 0 else 0,
        "average_time": sum(r.execution_time for r in all_iterations) / request.iterations
        if request.iterations > 0
        else 0,
    }

    return TestIterationResponse(
        iteration=request.iterations,
        passed=passed,
        output=final_output,
        execution_time=final_time,
        all_iterations=all_iterations,
        summary=summary,
    )


@router.post("/compile", response_model=CompileResponse)
async def compile_code(
    request: CompileRequest, token: str = Depends(auth_manager.require_token)
):
    """
    Compile HLXL code (stub implementation).

    In production, this would parse HLXL and produce AST and lowered IR.

    Args:
        request: CompileRequest with source code
        token: Authentication token

    Returns:
        CompileResponse with compilation results
    """
    try:
        # Stub implementation: validate code format
        if not request.code or len(request.code) < 5:
            return CompileResponse(
                success=False,
                ast=None,
                lowered=None,
                errors=["Code too short or empty"],
            )

        # Stub: Create fake AST
        ast = {
            "type": "Program",
            "language": request.format,
            "lines": len(request.code.splitlines()),
            "size_bytes": len(request.code),
        }

        lowered = {
            "type": "LoweredIR",
            "operations": 0,
            "status": "stub",
        }

        await observer_manager.emit(
            "compile",
            {
                "format": request.format,
                "code_size": len(request.code),
                "success": True,
            },
        )

        return CompileResponse(
            success=True, ast=ast, lowered=lowered, errors=[]
        )

    except Exception as e:
        await observer_manager.emit(
            "compile_error",
            {"format": request.format, "error": str(e)},
        )

        return CompileResponse(
            success=False,
            ast=None,
            lowered=None,
            errors=[str(e)],
        )


@router.get("/status", response_model=StatusResponse)
async def get_status(token: str = Depends(auth_manager.require_token)):
    """
    Get comprehensive system status.

    Args:
        token: Authentication token

    Returns:
        StatusResponse with current system status
    """
    from datetime import datetime

    runtime_status = "available" if hlx_bridge.available else "stub"

    capabilities = [
        "collapse",
        "resolve",
        "execute",
        "batch",
        "test-iteration",
        "compile",
    ]

    return StatusResponse(
        backend="running",
        hlx_runtime=runtime_status,
        observer={
            "connections": len(observer_manager.connections),
            "total_events": len(observer_manager.event_history),
            "max_history": observer_manager.max_history,
        },
        capabilities=capabilities,
        timestamp=datetime.now().isoformat(),
    )
