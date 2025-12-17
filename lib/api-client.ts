/**
 * HLX Dev Studio API Client
 * Connects frontend to FastAPI backend (http://127.0.0.1:58300)
 */

const API_BASE = 'http://127.0.0.1:58300';

export interface HLXStatus {
  status: string;
  hlx_available: boolean;
  version: string;
}

export interface CollapseResponse {
  handle: string;
  hash: string;
}

export interface ResolveResponse {
  value: any;
}

export interface ExecuteResponse {
  result: any;
  handle?: string | null;
}

export interface ObserverStats {
  active_connections: number;
  total_events: number;
  event_types: Record<string, number>;
}

/**
 * Check HLX runtime status
 */
export async function getHLXStatus(): Promise<HLXStatus> {
  const response = await fetch(`${API_BASE}/hlx/status`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
}

/**
 * Collapse a value to a handle
 */
export async function collapse(value: any, emit_event: boolean = false): Promise<CollapseResponse> {
  const response = await fetch(`${API_BASE}/hlx/collapse`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ value, emit_event }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/**
 * Resolve a handle to its value
 */
export async function resolve(handle: string, emit_event: boolean = false): Promise<ResolveResponse> {
  const response = await fetch(`${API_BASE}/hlx/resolve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ handle, emit_event }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/**
 * Execute an HLX operation (hash, validate, etc.)
 */
export async function execute(
  operation: string,
  args: Record<string, any>,
  emit_event: boolean = false
): Promise<ExecuteResponse> {
  const response = await fetch(`${API_BASE}/hlx/execute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      operation,
      arguments: args,
      emit_event
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/**
 * Get observer statistics
 */
export async function getObserverStats(): Promise<ObserverStats> {
  const response = await fetch(`${API_BASE}/observer/stats`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
}

/**
 * Connect to observer WebSocket for real-time events
 */
export function connectObserver(onMessage: (event: any) => void): WebSocket {
  const ws = new WebSocket(`ws://127.0.0.1:58300/observer/ws`);

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (e) {
      console.error('Failed to parse observer message:', e);
    }
  };

  ws.onerror = (error) => {
    console.error('Observer WebSocket error:', error);
  };

  return ws;
}

/**
 * Round-trip test: collapse then resolve
 */
export async function roundTrip(value: any): Promise<{
  handle: string;
  hash: string;
  resolved: any;
  matches: boolean;
}> {
  const collapseResult = await collapse(value, false);
  const resolveResult = await resolve(collapseResult.handle, false);

  return {
    handle: collapseResult.handle,
    hash: collapseResult.hash,
    resolved: resolveResult.value,
    matches: JSON.stringify(value) === JSON.stringify(resolveResult.value),
  };
}
