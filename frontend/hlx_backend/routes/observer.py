"""
Observer WebSocket Endpoint
Real-time event streaming for operation monitoring.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set, Any
import json
import asyncio
from datetime import datetime

router = APIRouter(prefix="/observer", tags=["observer"])


class ObserverManager:
    """
    Manages WebSocket connections and broadcasts events.
    """

    def __init__(self):
        self.connections: Set[WebSocket] = set()
        self.event_history: list = []
        self.max_history = 1000

    async def connect(self, websocket: WebSocket):
        """Register a new WebSocket connection."""
        await websocket.accept()
        self.connections.add(websocket)
        print(f"[Observer] New connection: {id(websocket)}")

        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "timestamp": datetime.now().isoformat(),
            "message": "Connected to HLX Dev Studio Observer"
        })

        # Send recent event history
        if self.event_history:
            await websocket.send_json({
                "type": "history",
                "events": self.event_history[-50:]  # Last 50 events
            })

    async def disconnect(self, websocket: WebSocket):
        """Unregister a WebSocket connection."""
        self.connections.discard(websocket)
        print(f"[Observer] Connection closed: {id(websocket)}")

    async def emit(self, event_type: str, data: Dict[str, Any]):
        """
        Broadcast an event to all connected clients.

        Args:
            event_type: Type of event (e.g., "collapse", "resolve", "error")
            data: Event data
        """
        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }

        # Add to history
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)

        # Broadcast to all connections
        dead_connections = set()
        for websocket in self.connections:
            try:
                await websocket.send_json(event)
            except Exception as e:
                print(f"[Observer] Failed to send to {id(websocket)}: {e}")
                dead_connections.add(websocket)

        # Remove dead connections
        self.connections -= dead_connections

    def get_stats(self) -> Dict[str, Any]:
        """Get observer statistics."""
        return {
            "active_connections": len(self.connections),
            "total_events": len(self.event_history),
            "event_types": self._count_event_types()
        }

    def _count_event_types(self) -> Dict[str, int]:
        """Count events by type."""
        counts = {}
        for event in self.event_history:
            event_type = event.get("type", "unknown")
            counts[event_type] = counts.get(event_type, 0) + 1
        return counts


# Global observer manager instance
observer_manager = ObserverManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time operation monitoring.

    Connect to: ws://localhost:58300/observer/ws

    Event format:
    {
        "type": "collapse" | "resolve" | "execute" | "error" | ...,
        "timestamp": "2025-12-17T03:00:00.000Z",
        "data": { ... }
    }
    """
    await observer_manager.connect(websocket)

    try:
        while True:
            # Keep connection alive, process incoming messages if any
            message = await websocket.receive_text()

            # Parse incoming message
            try:
                data = json.loads(message)
                command = data.get("command")

                if command == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    })
                elif command == "stats":
                    stats = observer_manager.get_stats()
                    await websocket.send_json({
                        "type": "stats",
                        "timestamp": datetime.now().isoformat(),
                        "data": stats
                    })
                elif command == "clear_history":
                    observer_manager.event_history.clear()
                    await websocket.send_json({
                        "type": "history_cleared",
                        "timestamp": datetime.now().isoformat()
                    })

            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "timestamp": datetime.now().isoformat(),
                    "message": "Invalid JSON"
                })

    except WebSocketDisconnect:
        await observer_manager.disconnect(websocket)
    except Exception as e:
        print(f"[Observer] WebSocket error: {e}")
        await observer_manager.disconnect(websocket)


@router.get("/stats")
async def get_stats():
    """
    Get observer statistics.

    Returns:
        dict: Statistics about connections and events
    """
    return observer_manager.get_stats()


@router.get("/events")
async def get_events(limit: int = 50):
    """
    Get recent events from history.

    Args:
        limit: Number of recent events to return (default 50, max 1000)

    Returns:
        list: Recent events
    """
    limit = min(limit, 1000)
    return {
        "events": observer_manager.event_history[-limit:],
        "total": len(observer_manager.event_history)
    }
