
import React, { useState } from 'react';
import { Database, Search, Code, Monitor, Cpu, FileText, Layers } from 'lucide-react';

type FilterType = 'ALL' | 'PROJECT' | 'OS_PROFILE' | 'KERNEL_PROFILE' | 'PLAN';

const Archive: React.FC = () => {
  const [activeFilter, setActiveFilter] = useState<FilterType>('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  const filters: { id: FilterType; label: string; icon: React.ReactNode }[] = [
    { id: 'ALL', label: 'ALL', icon: <Layers size={16} /> },
    { id: 'PROJECT', label: 'PROJECT', icon: <Code size={16} /> },
    { id: 'OS_PROFILE', label: 'OS PROFILE', icon: <Monitor size={16} /> },
    { id: 'KERNEL_PROFILE', label: 'KERNEL PROFILE', icon: <Cpu size={16} /> },
    { id: 'PLAN', label: 'PLAN', icon: <FileText size={16} /> },
  ];

  const mockItems = [
    { id: 1, type: 'PROJECT', name: 'hlx-dev-studio', hash: '0x8F2A...', date: 'Dec 14' },
    { id: 2, type: 'OS_PROFILE', name: 'Helinux Base', hash: '0x3B4C...', date: 'Dec 13' },
    { id: 3, type: 'KERNEL_PROFILE', name: 'Custom Kernel 6.8.9', hash: '0x7D1E...', date: 'Dec 12' },
    { id: 4, type: 'PLAN', name: 'HLX v2 Roadmap', hash: '0x9A2F...', date: 'Dec 11' },
    { id: 5, type: 'PROJECT', name: 'lc-compiler', hash: '0x5E8B...', date: 'Dec 10' },
  ];

  const filteredItems = mockItems.filter(item =>
    (activeFilter === 'ALL' || item.type === activeFilter) &&
    (searchQuery === '' || item.name.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="flex h-[calc(100vh-3.5rem)] bg-hlx-bg text-hlx-text font-sans">
      {/* Sidebar */}
      <div className="w-56 border-r border-hlx-border flex flex-col bg-hlx-panel/30">
        {/* Header */}
        <div className="p-4 border-b border-hlx-border flex items-center gap-2">
          <Database size={18} className="text-hlx-primary" />
          <span className="font-bold text-white tracking-wide text-sm">ARCHIVE</span>
        </div>

        {/* Search */}
        <div className="p-3 border-b border-hlx-border">
          <div className="relative">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-hlx-muted" />
            <input
              type="text"
              placeholder="Search items, metadata, tags..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-hlx-surface border border-hlx-border rounded-md pl-9 pr-3 py-2 text-xs focus:border-hlx-primary outline-none transition-all placeholder-hlx-muted text-white"
            />
          </div>
        </div>

        {/* Filters */}
        <div className="p-3">
          <div className="text-[10px] font-bold text-hlx-muted uppercase mb-3 tracking-wider">FILTERS</div>
          <div className="space-y-1">
            {filters.map(filter => (
              <button
                key={filter.id}
                onClick={() => setActiveFilter(filter.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                  activeFilter === filter.id
                    ? 'bg-hlx-primary/20 text-white border border-hlx-primary/30'
                    : 'text-hlx-muted hover:text-white hover:bg-white/5 border border-transparent'
                }`}
              >
                <span className={activeFilter === filter.id ? 'text-hlx-primary' : ''}>{filter.icon}</span>
                {filter.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <div className="h-12 border-b border-hlx-border flex items-center justify-between px-6 bg-hlx-panel/20">
          <span className="text-xs text-hlx-muted">
            {filteredItems.length} ITEMS
          </span>
          <div className="flex items-center gap-2 text-xs text-hlx-muted">
            <span>MODE:</span>
            <span className="text-white">BROWSER</span>
          </div>
        </div>

        {/* Content Grid */}
        <div className="flex-1 p-6 overflow-y-auto">
          {filteredItems.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {filteredItems.map(item => (
                <div
                  key={item.id}
                  className="p-4 rounded-xl border border-hlx-border bg-hlx-panel/50 hover:border-hlx-primary/50 transition-all cursor-pointer group"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className={`p-2 rounded-lg border ${
                      item.type === 'PROJECT' ? 'bg-blue-500/10 border-blue-500/20 text-blue-400' :
                      item.type === 'OS_PROFILE' ? 'bg-green-500/10 border-green-500/20 text-green-400' :
                      item.type === 'KERNEL_PROFILE' ? 'bg-orange-500/10 border-orange-500/20 text-orange-400' :
                      'bg-purple-500/10 border-purple-500/20 text-purple-400'
                    }`}>
                      {item.type === 'PROJECT' ? <Code size={18} /> :
                       item.type === 'OS_PROFILE' ? <Monitor size={18} /> :
                       item.type === 'KERNEL_PROFILE' ? <Cpu size={18} /> :
                       <FileText size={18} />}
                    </div>
                    <span className="text-[10px] font-mono text-hlx-muted">{item.hash}</span>
                  </div>
                  <h4 className="font-semibold text-white text-sm mb-1 group-hover:text-hlx-primary transition-colors">
                    {item.name}
                  </h4>
                  <p className="text-[11px] text-hlx-muted">{item.date}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex items-center justify-center h-full text-hlx-muted text-sm">
              No items found
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Archive;
