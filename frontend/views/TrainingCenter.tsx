import React, { useState } from 'react';
import { Brain, Key, Play, Trash2, Plus, CheckCircle, Clock, AlertCircle } from 'lucide-react';

interface APIKey {
  id: string;
  provider: 'claude' | 'openai' | 'xai' | 'qwen';
  name: string;
  key: string;
  models: string[];
}

interface TrainingSession {
  id: string;
  provider: string;
  model: string;
  targetModel: 'Helix100m';
  corpus: 'English' | 'HLX' | 'Translation';
  epochs: number;
  status: 'queued' | 'running' | 'completed' | 'failed';
  progress?: number;
  startTime?: Date;
  endTime?: Date;
}

const MODEL_CATEGORIES = {
  claude: {
    name: 'Anthropic Claude',
    models: [
      { id: 'claude-sonnet-4.5', name: 'Claude Sonnet 4.5', category: 'Quality & Precision', cost: '$$' },
      { id: 'claude-opus-4.1', name: 'Claude Opus 4.1', category: 'Maximum Capability', cost: '$$$' },
      { id: 'claude-haiku-4', name: 'Claude Haiku 4', category: 'Speed & Efficiency', cost: '$' },
    ],
  },
  openai: {
    name: 'OpenAI',
    models: [
      { id: 'gpt-5.1', name: 'GPT-5.1', category: 'Advanced Reasoning', cost: '$$' },
      { id: 'gpt-4o', name: 'GPT-4o', category: 'Multimodal', cost: '$$' },
    ],
  },
  xai: {
    name: 'xAI',
    models: [
      { id: 'grok-4.1', name: 'Grok 4.1', category: 'Performance & Scale', cost: '$$' },
    ],
  },
  qwen: {
    name: 'Qwen (Local)',
    models: [
      { id: 'qwen3:8b', name: 'Qwen3 8B', category: 'Free Distillation', cost: 'FREE' },
      { id: 'qwen3:4b', name: 'Qwen3 4B', category: 'Free Distillation', cost: 'FREE' },
      { id: 'qwen3:1.7b', name: 'Qwen3 1.7B', category: 'Free Distillation', cost: 'FREE' },
    ],
  },
};

export default function TrainingCenter() {
  const [apiKeys, setApiKeys] = useState<APIKey[]>([]);
  const [trainingQueue, setTrainingQueue] = useState<TrainingSession[]>([]);
  const [showAddKey, setShowAddKey] = useState(false);
  const [showNewSession, setShowNewSession] = useState(false);

  const [newKey, setNewKey] = useState({
    provider: 'claude' as const,
    name: '',
    key: '',
  });

  const [newSession, setNewSession] = useState({
    provider: 'claude',
    model: 'claude-sonnet-4.5',
    corpus: 'English' as const,
    epochs: 200,
  });

  const handleAddKey = () => {
    if (!newKey.name || !newKey.key) return;

    const key: APIKey = {
      id: Date.now().toString(),
      provider: newKey.provider,
      name: newKey.name,
      key: newKey.key,
      models: MODEL_CATEGORIES[newKey.provider].models.map(m => m.id),
    };

    setApiKeys([...apiKeys, key]);
    setNewKey({ provider: 'claude', name: '', key: '' });
    setShowAddKey(false);
  };

  const handleAddSession = () => {
    const session: TrainingSession = {
      id: Date.now().toString(),
      provider: newSession.provider,
      model: newSession.model,
      targetModel: 'Helix100m',
      corpus: newSession.corpus,
      epochs: newSession.epochs,
      status: 'queued',
    };

    setTrainingQueue([...trainingQueue, session]);
    setShowNewSession(false);
  };

  const handleDeleteKey = (id: string) => {
    setApiKeys(apiKeys.filter(k => k.id !== id));
  };

  const handleDeleteSession = (id: string) => {
    setTrainingQueue(trainingQueue.filter(s => s.id !== id));
  };

  const getStatusIcon = (status: TrainingSession['status']) => {
    switch (status) {
      case 'queued': return <Clock className="w-4 h-4 text-yellow-400" />;
      case 'running': return <Play className="w-4 h-4 text-blue-400 animate-pulse" />;
      case 'completed': return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'failed': return <AlertCircle className="w-4 h-4 text-red-400" />;
    }
  };

  return (
    <div className="h-full bg-hlx-bg text-hlx-text p-6 overflow-auto">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-center gap-4">
          <div className="p-3 bg-hlx-primary/10 rounded-lg border border-hlx-primary/20">
            <Brain className="w-6 h-6 text-hlx-primary" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Training Center</h1>
            <p className="text-sm text-hlx-muted">Multi-provider HLX Brain training orchestration</p>
          </div>
        </div>

        {/* API Key Management */}
        <div className="bg-hlx-panel border border-hlx-border rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Key className="w-5 h-5 text-hlx-accent" />
              <h2 className="text-lg font-semibold text-white">API Key Pool</h2>
            </div>
            <button
              onClick={() => setShowAddKey(!showAddKey)}
              className="flex items-center gap-2 px-3 py-1.5 bg-hlx-accent/10 hover:bg-hlx-accent/20 border border-hlx-accent/30 rounded-lg text-hlx-accent text-sm font-medium transition-colors"
            >
              <Plus className="w-4 h-4" />
              Add API Key
            </button>
          </div>

          {/* Add Key Form */}
          {showAddKey && (
            <div className="mb-4 p-4 bg-hlx-surface border border-hlx-border rounded-lg space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-hlx-muted mb-1">Provider</label>
                  <select
                    value={newKey.provider}
                    onChange={(e) => setNewKey({ ...newKey, provider: e.target.value as any })}
                    className="w-full px-3 py-2 bg-hlx-bg border border-hlx-border rounded text-sm text-white focus:border-hlx-accent focus:outline-none"
                  >
                    <option value="claude">Anthropic Claude</option>
                    <option value="openai">OpenAI</option>
                    <option value="xai">xAI</option>
                    <option value="qwen">Qwen (Local)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-hlx-muted mb-1">Key Name</label>
                  <input
                    type="text"
                    value={newKey.name}
                    onChange={(e) => setNewKey({ ...newKey, name: e.target.value })}
                    placeholder="Production Key"
                    className="w-full px-3 py-2 bg-hlx-bg border border-hlx-border rounded text-sm text-white focus:border-hlx-accent focus:outline-none"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs text-hlx-muted mb-1">API Key</label>
                <input
                  type="password"
                  value={newKey.key}
                  onChange={(e) => setNewKey({ ...newKey, key: e.target.value })}
                  placeholder="sk-..."
                  className="w-full px-3 py-2 bg-hlx-bg border border-hlx-border rounded text-sm text-white focus:border-hlx-accent focus:outline-none font-mono"
                />
              </div>
              <div className="flex gap-2">
                <button
                  onClick={handleAddKey}
                  className="px-4 py-2 bg-hlx-accent hover:bg-hlx-accent/80 text-white text-sm font-medium rounded-lg transition-colors"
                >
                  Add Key
                </button>
                <button
                  onClick={() => setShowAddKey(false)}
                  className="px-4 py-2 bg-hlx-surface hover:bg-hlx-border/20 text-hlx-muted text-sm font-medium rounded-lg transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          {/* API Keys List */}
          <div className="space-y-2">
            {apiKeys.length === 0 ? (
              <div className="text-center py-8 text-hlx-muted text-sm">
                No API keys configured. Add keys to enable training.
              </div>
            ) : (
              apiKeys.map(key => (
                <div key={key.id} className="flex items-center justify-between p-3 bg-hlx-surface border border-hlx-border rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-green-400"></div>
                    <div>
                      <div className="text-sm font-medium text-white">{key.name}</div>
                      <div className="text-xs text-hlx-muted">{MODEL_CATEGORIES[key.provider].name} • {key.models.length} models available</div>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDeleteKey(key.id)}
                    className="p-2 hover:bg-red-500/10 rounded-lg transition-colors group"
                  >
                    <Trash2 className="w-4 h-4 text-hlx-muted group-hover:text-red-400" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Available Models */}
        <div className="bg-hlx-panel border border-hlx-border rounded-lg p-6">
          <h2 className="text-lg font-semibold text-white mb-4">Available Models</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(MODEL_CATEGORIES).map(([provider, info]) => {
              const hasKey = apiKeys.some(k => k.provider === provider);
              return (
                <div key={provider} className={`p-4 border rounded-lg ${hasKey ? 'bg-hlx-surface border-hlx-border' : 'bg-hlx-bg border-hlx-border/50 opacity-50'}`}>
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-semibold text-white">{info.name}</h3>
                    {!hasKey && <span className="text-xs text-hlx-muted px-2 py-1 bg-hlx-border/20 rounded">No API Key</span>}
                  </div>
                  <div className="space-y-2">
                    {info.models.map(model => (
                      <div key={model.id} className="flex items-center justify-between text-sm">
                        <div>
                          <div className="text-white font-medium">{model.name}</div>
                          <div className="text-xs text-hlx-muted">{model.category}</div>
                        </div>
                        <span className={`text-xs font-mono px-2 py-1 rounded ${model.cost === 'FREE' ? 'bg-green-500/10 text-green-400' : 'bg-blue-500/10 text-blue-400'}`}>
                          {model.cost}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Training Queue */}
        <div className="bg-hlx-panel border border-hlx-border rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-white">Training Queue</h2>
            <button
              onClick={() => setShowNewSession(!showNewSession)}
              disabled={apiKeys.length === 0}
              className="flex items-center gap-2 px-3 py-1.5 bg-hlx-accent/10 hover:bg-hlx-accent/20 border border-hlx-accent/30 rounded-lg text-hlx-accent text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Plus className="w-4 h-4" />
              New Training Session
            </button>
          </div>

          {/* New Session Form */}
          {showNewSession && (
            <div className="mb-4 p-4 bg-hlx-surface border border-hlx-border rounded-lg space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-hlx-muted mb-1">Provider</label>
                  <select
                    value={newSession.provider}
                    onChange={(e) => {
                      const provider = e.target.value;
                      setNewSession({
                        ...newSession,
                        provider,
                        model: MODEL_CATEGORIES[provider as keyof typeof MODEL_CATEGORIES].models[0].id
                      });
                    }}
                    className="w-full px-3 py-2 bg-hlx-bg border border-hlx-border rounded text-sm text-white focus:border-hlx-accent focus:outline-none"
                  >
                    {apiKeys.map(key => (
                      <option key={key.provider} value={key.provider}>
                        {MODEL_CATEGORIES[key.provider].name}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-hlx-muted mb-1">Model</label>
                  <select
                    value={newSession.model}
                    onChange={(e) => setNewSession({ ...newSession, model: e.target.value })}
                    className="w-full px-3 py-2 bg-hlx-bg border border-hlx-border rounded text-sm text-white focus:border-hlx-accent focus:outline-none"
                  >
                    {MODEL_CATEGORIES[newSession.provider as keyof typeof MODEL_CATEGORIES].models.map(m => (
                      <option key={m.id} value={m.id}>{m.name}</option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-hlx-muted mb-1">Training Corpus</label>
                  <select
                    value={newSession.corpus}
                    onChange={(e) => setNewSession({ ...newSession, corpus: e.target.value as any })}
                    className="w-full px-3 py-2 bg-hlx-bg border border-hlx-border rounded text-sm text-white focus:border-hlx-accent focus:outline-none"
                  >
                    <option value="English">English Mastery (Phase 1)</option>
                    <option value="HLX">HLX Family (Phase 2)</option>
                    <option value="Translation">Translation (Phase 3)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-hlx-muted mb-1">Epochs</label>
                  <input
                    type="number"
                    value={newSession.epochs}
                    onChange={(e) => setNewSession({ ...newSession, epochs: parseInt(e.target.value) })}
                    min="1"
                    max="500"
                    className="w-full px-3 py-2 bg-hlx-bg border border-hlx-border rounded text-sm text-white focus:border-hlx-accent focus:outline-none"
                  />
                </div>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={handleAddSession}
                  className="px-4 py-2 bg-hlx-accent hover:bg-hlx-accent/80 text-white text-sm font-medium rounded-lg transition-colors"
                >
                  Add to Queue
                </button>
                <button
                  onClick={() => setShowNewSession(false)}
                  className="px-4 py-2 bg-hlx-surface hover:bg-hlx-border/20 text-hlx-muted text-sm font-medium rounded-lg transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          {/* Queue List */}
          <div className="space-y-2">
            {trainingQueue.length === 0 ? (
              <div className="text-center py-8 text-hlx-muted text-sm">
                No training sessions queued. Configure a session to begin.
              </div>
            ) : (
              trainingQueue.map((session, index) => (
                <div key={session.id} className="flex items-center justify-between p-4 bg-hlx-surface border border-hlx-border rounded-lg">
                  <div className="flex items-center gap-4">
                    <div className="text-2xl font-bold text-hlx-muted">#{index + 1}</div>
                    {getStatusIcon(session.status)}
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium text-white">{session.model}</span>
                        <span className="text-xs text-hlx-muted">→</span>
                        <span className="text-sm text-hlx-accent">Helix100m</span>
                      </div>
                      <div className="text-xs text-hlx-muted mt-1">
                        {session.corpus} corpus • {session.epochs} epochs • {session.status}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {session.status === 'queued' && (
                      <button
                        onClick={() => handleDeleteSession(session.id)}
                        className="p-2 hover:bg-red-500/10 rounded-lg transition-colors group"
                      >
                        <Trash2 className="w-4 h-4 text-hlx-muted group-hover:text-red-400" />
                      </button>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Info Panel */}
        <div className="bg-hlx-accent/5 border border-hlx-accent/20 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-hlx-accent flex-shrink-0 mt-0.5" />
            <div className="text-sm text-hlx-muted space-y-1">
              <p className="text-white font-medium">Training Notes:</p>
              <ul className="list-disc list-inside space-y-1">
                <li>Qwen models run locally via Ollama (free)</li>
                <li>Training sessions execute sequentially in queue order</li>
                <li>Quality gates run automatically at epochs 1, 5, 10, 20, 50, 100, 150, 200</li>
                <li>Watchdog monitoring runs every 60 seconds during training</li>
                <li>Recommended: Use Qwen for free distillation, then Claude/GPT for refinement</li>
              </ul>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
