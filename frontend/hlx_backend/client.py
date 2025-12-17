"""
HLX Studio Python Client Library
Client for interacting with HLX Dev Studio API.
Designed for use by Claude and other automation tools.
"""

import requests
from typing import Any, List, Dict, Optional
from urllib.parse import urljoin


class HLXStudioClient:
    """
    Python client for HLX Dev Studio API.

    Example usage:
        client = HLXStudioClient(
            base_url='http://127.0.0.1:58300',
            token='your-api-token'
        )

        # Batch operations
        results = client.batch([
            {'type': 'collapse', 'value': {'@0': 42}},
            {'type': 'resolve', 'handle': '&h_...'}
        ])

        # Test iteration
        result = client.test_iteration(
            test_code="program test { ... }",
            expected_output={'@0': 42}
        )
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:58300",
        token: Optional[str] = None,
    ):
        """
        Initialize client.

        Args:
            base_url: Base URL of HLX Studio backend
            token: API token for authentication (optional if disabled)
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        """Setup requests session with headers."""
        if self.token:
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        self.session.headers.update({"Content-Type": "application/json"})

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to API.

        Args:
            method: HTTP method (GET, POST, etc)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters

        Returns:
            Response JSON

        Raises:
            requests.HTTPError: If request fails
        """
        url = urljoin(self.base_url, endpoint)

        if method.upper() == "GET":
            response = self.session.get(url, params=params)
        elif method.upper() == "POST":
            response = self.session.post(url, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()
        return response.json()

    def batch(
        self,
        operations: List[Dict[str, Any]],
        emit_events: bool = True,
    ) -> Dict[str, Any]:
        """
        Execute batch operations.

        Args:
            operations: List of operation dicts
                Each dict should have 'type' and relevant fields
                Types: collapse, resolve, execute
            emit_events: Whether to emit events to observer

        Returns:
            BatchResponse with results

        Example:
            results = client.batch([
                {'type': 'collapse', 'value': {'@0': 42}},
                {'type': 'resolve', 'handle': '&h_abc123'}
            ])
        """
        request_data = {
            "operations": operations,
            "emit_events": emit_events,
        }

        return self._make_request("POST", "/claude/batch", data=request_data)

    def collapse(self, value: Any) -> str:
        """
        Collapse a single value to a handle.

        Args:
            value: Value to collapse

        Returns:
            Content-addressed handle string

        Raises:
            Exception: If collapse fails
        """
        result = self.batch([{"type": "collapse", "value": value}])

        if not result["results"] or not result["results"][0]["success"]:
            error = result["results"][0].get("error", "Unknown error")
            raise Exception(f"Collapse failed: {error}")

        return result["results"][0]["result"]["handle"]

    def resolve(self, handle: str) -> Any:
        """
        Resolve a handle to its value.

        Args:
            handle: Content-addressed handle

        Returns:
            Resolved value

        Raises:
            Exception: If resolve fails
        """
        result = self.batch([{"type": "resolve", "handle": handle}])

        if not result["results"] or not result["results"][0]["success"]:
            error = result["results"][0].get("error", "Unknown error")
            raise Exception(f"Resolve failed: {error}")

        return result["results"][0]["result"]["value"]

    def test_iteration(
        self,
        test_code: str,
        expected_output: Optional[Dict[str, Any]] = None,
        iterations: int = 1,
    ) -> Dict[str, Any]:
        """
        Run test iteration cycle.

        Args:
            test_code: HLX code to test
            expected_output: Expected output for validation
            iterations: Number of iterations (1-100)

        Returns:
            TestIterationResponse with results

        Example:
            result = client.test_iteration(
                test_code="program test { ... }",
                expected_output={'@0': 42},
                iterations=5
            )
        """
        if not 1 <= iterations <= 100:
            raise ValueError("iterations must be between 1 and 100")

        request_data = {
            "test_code": test_code,
            "expected_output": expected_output,
            "iterations": iterations,
        }

        return self._make_request("POST", "/claude/test-iteration", data=request_data)

    def compile(self, code: str, format: str = "hlxl") -> Dict[str, Any]:
        """
        Compile HLXL code.

        Args:
            code: Source code to compile
            format: Code format (default: hlxl)

        Returns:
            CompileResponse with AST and lowered IR

        Example:
            result = client.compile("program main { ... }")
        """
        request_data = {
            "code": code,
            "format": format,
        }

        return self._make_request("POST", "/claude/compile", data=request_data)

    def status(self) -> Dict[str, Any]:
        """
        Get system status.

        Returns:
            StatusResponse with current system state

        Example:
            status = client.status()
            print(f"Backend: {status['backend']}")
            print(f"HLX Runtime: {status['hlx_runtime']}")
        """
        return self._make_request("GET", "/claude/status")

    def health(self) -> Dict[str, Any]:
        """
        Get backend health status.

        Returns:
            Health status dict
        """
        return self._make_request("GET", "/health")
