"""
Tests for HLX Claude API Control Layer
Tests authentication, batch operations, test iteration, compile, and status endpoints.
"""

import pytest
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi.testclient import TestClient
from hlx_backend.server import app
from hlx_backend.auth import auth_manager


# Create test client
client = TestClient(app)

# Test token
TEST_TOKEN = "test_token_12345"


class TestAuthentication:
    """Test authentication functionality."""

    def test_status_without_auth_disabled(self):
        """Status endpoint should work without auth when disabled."""
        # Auth disabled by default (no env var set)
        response = client.get("/claude/status")
        assert response.status_code == 200
        data = response.json()
        assert data["backend"] == "running"

    def test_batch_without_token(self):
        """Batch endpoint should work without token when auth disabled."""
        response = client.post(
            "/claude/batch",
            json={
                "operations": [{"type": "collapse", "value": {"@0": 42}}],
                "emit_events": False,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "results" in data


class TestBatchOperations:
    """Test batch operations endpoint."""

    def test_batch_collapse(self):
        """Test collapse operation in batch."""
        response = client.post(
            "/claude/batch",
            json={
                "operations": [{"type": "collapse", "value": {"@0": 42}}],
                "emit_events": False,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["succeeded"] == 1
        assert data["failed"] == 0
        assert data["results"][0]["success"] is True
        assert "handle" in data["results"][0]["result"]
        assert "hash" in data["results"][0]["result"]

    def test_batch_multiple_operations(self):
        """Test multiple operations in single batch."""
        response = client.post(
            "/claude/batch",
            json={
                "operations": [
                    {"type": "collapse", "value": {"@0": 42}},
                    {"type": "collapse", "value": {"@1": "hello"}},
                    {"type": "collapse", "value": {"@2": [1, 2, 3]}},
                ],
                "emit_events": False,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert data["succeeded"] == 3
        assert len(data["results"]) == 3

    def test_batch_with_invalid_operation(self):
        """Test batch with invalid operation type."""
        response = client.post(
            "/claude/batch",
            json={
                "operations": [
                    {"type": "collapse", "value": {"@0": 42}},
                    {"type": "invalid_op"},
                ],
                "emit_events": False,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert data["succeeded"] == 1
        assert data["failed"] == 1
        assert data["results"][1]["success"] is False

    def test_batch_resolve_missing_handle(self):
        """Test resolve operation without handle."""
        response = client.post(
            "/claude/batch",
            json={
                "operations": [{"type": "resolve"}],
                "emit_events": False,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["results"][0]["success"] is False
        assert "handle" in data["results"][0]["error"]

    def test_batch_execute_operation(self):
        """Test execute operation in batch."""
        response = client.post(
            "/claude/batch",
            json={
                "operations": [
                    {
                        "type": "execute",
                        "operation": "hash",
                        "arguments": {"value": {"@0": 42}},
                    }
                ],
                "emit_events": False,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["results"][0]["success"] is True


class TestTestIteration:
    """Test test iteration endpoint."""

    def test_single_iteration(self):
        """Test single iteration cycle."""
        response = client.post(
            "/claude/test-iteration",
            json={
                "test_code": "program test { block init() {} }",
                "expected_output": None,
                "iterations": 1,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["iteration"] == 1
        assert "passed" in data
        assert "output" in data
        assert "all_iterations" in data
        assert len(data["all_iterations"]) == 1

    def test_multiple_iterations(self):
        """Test multiple iteration cycles."""
        response = client.post(
            "/claude/test-iteration",
            json={
                "test_code": "program test { block init() {} }",
                "expected_output": None,
                "iterations": 5,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["iteration"] == 5
        assert len(data["all_iterations"]) == 5
        assert "summary" in data
        assert data["summary"]["total_iterations"] == 5

    def test_iteration_with_expected_output(self):
        """Test iteration with expected output."""
        response = client.post(
            "/claude/test-iteration",
            json={
                "test_code": "program test { block init() {} }",
                "expected_output": {"@0": 42},
                "iterations": 1,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "output" in data


class TestCompile:
    """Test compile endpoint."""

    def test_compile_valid_code(self):
        """Test compilation of valid code."""
        response = client.post(
            "/claude/compile",
            json={
                "code": "program main { block init() { } }",
                "format": "hlxl",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "ast" in data
        assert data["ast"]["type"] == "Program"
        assert data["errors"] == []

    def test_compile_empty_code(self):
        """Test compilation of empty code."""
        response = client.post(
            "/claude/compile",
            json={
                "code": "",
                "format": "hlxl",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert len(data["errors"]) > 0


class TestStatus:
    """Test status endpoint."""

    def test_status_response(self):
        """Test status endpoint returns correct info."""
        response = client.get("/claude/status")
        assert response.status_code == 200
        data = response.json()
        assert data["backend"] == "running"
        assert "hlx_runtime" in data
        assert data["hlx_runtime"] in ["available", "stub"]
        assert "observer" in data
        assert "connections" in data["observer"]
        assert "total_events" in data["observer"]
        assert "capabilities" in data
        assert "collapse" in data["capabilities"]
        assert "batch" in data["capabilities"]
        assert "timestamp" in data

    def test_status_capabilities(self):
        """Test status lists all capabilities."""
        response = client.get("/claude/status")
        data = response.json()
        required_capabilities = [
            "collapse",
            "resolve",
            "execute",
            "batch",
            "test-iteration",
            "compile",
        ]
        for cap in required_capabilities:
            assert cap in data["capabilities"]


class TestRootEndpoint:
    """Test root endpoint includes claude."""

    def test_root_includes_claude_endpoint(self):
        """Test root endpoint lists claude endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "endpoints" in data
        assert "claude" in data["endpoints"]
        assert data["endpoints"]["claude"] == "/claude"


class TestHealthEndpoint:
    """Test health endpoint."""

    def test_health_status(self):
        """Test health endpoint works."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "observer" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
