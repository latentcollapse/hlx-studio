import React, { useState, useEffect, useRef } from 'react';
import { Eye, Pause, Play, Trash2, Activity } from 'lucide-react';
import { connectObserver } from '../lib/api-client';

interface ObserverEvent {
  id: string;
  timestamp: string;
  type: string;
  data?: any;
}

type FilterType = 'All' | 'Collapse' | 'Resolve' | 'Execute';

const ObserverView: React.FC = () => {
  const [events, setEvents] = useState<ObserverEvent[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isAutoScroll, setIsAutoScroll] = useState(true);
  const [activeFilter, setActiveFilter] = useState<FilterType>('All');
  const [eventCount, setEventCount] = useState(0);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const eventCounterRef = useRef(0);

  useEffect(() => {
    // Connect to WebSocket
    try {
      wsRef.current = connectObserver((event) => {
        const newEvent: ObserverEvent = {
          id: `event-${eventCounterRef.current++}`,
          timestamp: new Date().toLocaleTimeString('en-US', { hour12: false }),
          type: event.type || 'unknown',
          data: event.data || event,
        };

        setEvents((prev) => [newEvent, ...prev.slice(0, 999)]);
        setEventCount((prev) => prev + 1);
      });

      wsRef.current.onopen = () => {
        setIsConnected(true);
      };

      wsRef.current.onclose = () => {
        setIsConnected(false);
      };
    } catch (e) {
      console.error('Failed to connect to observer:', e);
    }

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Auto-scroll to top when new events arrive
  useEffect(() => {
    if (isAutoScroll && scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = 0;
    }
  }, [events, isAutoScroll]);

  const filters: { id: FilterType; label: string; color: string }[] = [
    { id: 'All', label: 'All', color: 'bg-white/5 border-white/10 text-white' },
    { id: 'Collapse', label: 'Collapse', color: 'bg-blue-500/10 border-blue-500/30 text-blue-400' },
    { id: 'Resolve', label: 'Resolve', color: 'bg-purple-500/10 border-purple-500/30 text-purple-400' },
    { id: 'Execute', label: 'Execute', color: 'bg-green-500/10 border-green-500/30 text-green-400' },
  ];

  const getEventTypeColor = (type: string): string => {
    const normalized = type.toLowerCase().replace('_', ' ').split(' ')[0];
    if (normalized.includes('collapse')) return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
    if (normalized.includes('resolve')) return 'bg-purple-500/10 text-purple-400 border-purple-500/20';
    if (normalized.includes('execute')) return 'bg-green-500/10 text-green-400 border-green-500/20';
    if (normalized.includes('connection')) return 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20';
    return 'bg-gray-500/10 text-gray-400 border-gray-500/20';
  };

  const filteredEvents = events.filter((event) => {
    if (activeFilter === 'All') return true;
    const eventType = event.type.toLowerCase();
    return eventType.includes(activeFilter.toLowerCase());
  });

  const handleClearLog = () => {
    setEvents([]);
  };

  const formatEventData = (data: any): string => {
    if (typeof data === 'string') return data;
    if (typeof data === 'object') {
      if (data.handle) return `Handle: ${data.handle}`;
      if (data.value !== undefined) return `Value: ${JSON.stringify(data.value).substring(0, 50)}`;
      return JSON.stringify(data).substring(0, 50);
    }
    return String(data);
  };

  return (
    <div className="flex h-[calc(100vh-3.5rem)] bg-[#050208] text-hlx-text font-sans flex-col">
      {/* Header */}
      <div className="h-16 border-b border-hlx-border/30 flex items-center justify-between px-6 bg-gradient-to-r from-[#0a0612]/50 to-[#050208]/50 backdrop-blur-sm flex-shrink-0">
        <div className="flex items-center gap-3">
          <Eye className="text-hlx-primary w-5 h-5" />
          <h1 className="font-bold text-white text-base tracking-wide">Observer</h1>
        </div>

        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full animate-pulse ${isConnected ? 'bg-green-400' : 'bg-red-400'}`}></div>
            <span className={`text-xs font-semibold uppercase tracking-wide ${isConnected ? 'text-green-400' : 'text-red-400'}`}>
              {isConnected ? 'CONNECTED' : 'DISCONNECTED'}
            </span>
          </div>

          <div className="h-4 w-px bg-hlx-border/30"></div>

          <span className="text-xs text-hlx-muted font-mono">
            {eventCount} events
          </span>

          <button
            onClick={handleClearLog}
            className="flex items-center gap-1.5 px-2 py-1.5 rounded-md bg-red-500/10 border border-red-500/20 text-red-400 hover:bg-red-500/20 transition-all text-xs font-semibold tracking-wide"
          >
            <Trash2 size={14} />
            Clear
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="h-12 border-b border-hlx-border/30 flex items-center px-6 gap-2 bg-hlx-panel/10 flex-shrink-0">
        <span className="text-xs text-hlx-muted font-semibold uppercase tracking-wide mr-2">Filter:</span>
        <div className="flex gap-1.5">
          {filters.map((filter) => (
            <button
              key={filter.id}
              onClick={() => setActiveFilter(filter.id)}
              className={`px-2.5 py-1.5 rounded-md text-xs font-semibold tracking-wide border transition-all ${
                activeFilter === filter.id
                  ? `${filter.color}`
                  : 'bg-white/5 border-white/10 text-hlx-muted hover:text-white'
              }`}
            >
              {filter.label}
            </button>
          ))}
        </div>
      </div>

      {/* Event Log */}
      <div
        ref={scrollContainerRef}
        className="flex-1 overflow-y-auto bg-[#050208] p-4 space-y-1 custom-scrollbar"
      >
        {filteredEvents.length > 0 ? (
          <div className="space-y-1">
            {filteredEvents.map((event) => (
              <div
                key={event.id}
                className={`p-3 rounded-lg border font-mono text-xs transition-all hover:bg-white/5 ${getEventTypeColor(event.type)}`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-start gap-3 flex-1 min-w-0">
                    <span className="text-hlx-muted flex-shrink-0">{event.timestamp}</span>
                    <span className="font-semibold flex-shrink-0">
                      [{event.type.toUpperCase()}]
                    </span>
                    <span className="text-hlx-muted truncate">
                      {formatEventData(event.data)}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-hlx-muted">
            <Activity className="w-12 h-12 opacity-20 mb-3" />
            <p className="text-sm">
              {events.length === 0 ? 'Waiting for events...' : 'No events match filter'}
            </p>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="h-12 border-t border-hlx-border/30 flex items-center justify-between px-6 bg-hlx-panel/10 flex-shrink-0">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsAutoScroll(!isAutoScroll)}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-xs font-semibold tracking-wide transition-all border ${
              isAutoScroll
                ? 'bg-green-500/10 border-green-500/20 text-green-400'
                : 'bg-orange-500/10 border-orange-500/20 text-orange-400'
            }`}
          >
            {isAutoScroll ? (
              <>
                <Play size={14} />
                Auto-scroll ON
              </>
            ) : (
              <>
                <Pause size={14} />
                Auto-scroll OFF
              </>
            )}
          </button>
        </div>

        <span className="text-xs text-hlx-muted font-mono">
          ws://127.0.0.1:58300/observer/ws
        </span>
      </div>
    </div>
  );
};

export default ObserverView;
