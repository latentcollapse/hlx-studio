#!/usr/bin/env python3
"""
Quick test script for HLX Dev Studio Backend API
"""

import requests
import json

BASE_URL = "http://127.0.0.1:58300"

print("Testing HLX Dev Studio Backend API...")
print("="*50)

# Test 1: Health check
print("\n1. Testing /health endpoint...")
resp = requests.get(f"{BASE_URL}/health")
print(f"Status: {resp.status_code}")
print(json.dumps(resp.json(), indent=2))

# Test 2: HLX Status
print("\n2. Testing /hlx/status endpoint...")
resp = requests.get(f"{BASE_URL}/hlx/status")
print(f"Status: {resp.status_code}")
print(json.dumps(resp.json(), indent=2))

# Test 3: Collapse
print("\n3. Testing /hlx/collapse endpoint...")
payload = {"value": {"@0": 42}, "emit_event": False}
resp = requests.post(f"{BASE_URL}/hlx/collapse", json=payload)
print(f"Status: {resp.status_code}")
result = resp.json()
print(json.dumps(result, indent=2))

if resp.status_code == 200:
    # Test 4: Resolve
    print("\n4. Testing /hlx/resolve endpoint...")
    handle = result["handle"]
    payload = {"handle": handle, "emit_event": False}
    resp = requests.post(f"{BASE_URL}/hlx/resolve", json=payload)
    print(f"Status: {resp.status_code}")
    print(json.dumps(resp.json(), indent=2))

# Test 5: Execute (hash)
print("\n5. Testing /hlx/execute endpoint (hash)...")
payload = {"operation": "hash", "arguments": {"value": {"@0": 123}}, "emit_event": False}
resp = requests.post(f"{BASE_URL}/hlx/execute", json=payload)
print(f"Status: {resp.status_code}")
print(json.dumps(resp.json(), indent=2))

# Test 6: HLXL status (stub)
print("\n6. Testing /hlxl/status endpoint...")
resp = requests.get(f"{BASE_URL}/hlxl/status")
print(f"Status: {resp.status_code}")
print(json.dumps(resp.json(), indent=2))

# Test 7: Observer stats
print("\n7. Testing /observer/stats endpoint...")
resp = requests.get(f"{BASE_URL}/observer/stats")
print(f"Status: {resp.status_code}")
print(json.dumps(resp.json(), indent=2))

print("\n" + "="*50)
print("✓ Backend API tests complete!")
