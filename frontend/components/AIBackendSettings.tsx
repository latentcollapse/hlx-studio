import React, { useState, useEffect } from 'react';
import { Settings, X, Check, AlertCircle, Brain, Zap } from 'lucide-react';
import { AIBackend, AIBackendConfig } from '../lib/brain-client';
import {
  getCurrentBackend,
  switchToLocalBrain,
  switchToClaude,
  switchToGPT4,
  getBackendDisplayName,
  validateAPIKey,
  getAIBackendStatus,
  AIBackendStatus,
} from '../lib/ai-context';

interface AIBackendSettingsProps {
  onClose?: () => void;
}

const AIBackendSettings: React.FC<AIBackendSettingsProps> = ({ onClose }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [currentBackend, setCurrentBackend] = useState<AIBackendConfig | null>(null);
  const [status, setStatus] = useState<AIBackendStatus | null>(null);
  const [apiKey, setApiKey] = useState('');
  const [selectedBackend, setSelectedBackend] = useState<AIBackend>('local');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const config = getCurrentBackend();
    setCurrentBackend(config);
    setSelectedBackend(config.backend);
    if (config.apiKey) {
      setApiKey(config.apiKey);
    }
    loadStatus();
  }, []);

  const loadStatus = async () => {
    try {
      const newStatus = await getAIBackendStatus();
      setStatus(newStatus);
    } catch (err) {
      console.error('Failed to load status:', err);
    }
  };

  const handleSwitchBackend = async (newBackend: AIBackend) => {
    setError(null);
    setSuccess(null);
    setLoading(true);

    try {
      if (newBackend === 'local') {
        switchToLocalBrain();
        setSelectedBackend('local');
        setApiKey('');
        setSuccess('Switched to Local Brain (Qwen3 8B + RAG)');
      } else if (newBackend === 'claude') {
        if (!validateAPIKey('claude', apiKey)) {
          setError('Invalid Claude API key. Must start with sk-ant- or sk-');
          setLoading(false);
          return;
        }
        switchToClaude(apiKey);
        setSelectedBackend('claude');
        setSuccess('Switched to Claude API');
      } else if (newBackend === 'gpt4') {
        if (!validateAPIKey('gpt4', apiKey)) {
          setError('Invalid GPT-4 API key. Must start with sk-');
          setLoading(false);
          return;
        }
        switchToGPT4(apiKey);
        setSelectedBackend('gpt4');
        setSuccess('Switched to GPT-4 API');
      }

      await loadStatus();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to switch backend');
    } finally {
      setLoading(false);
    }
  };

  const getBackendIcon = (backend: AIBackend) => {
    switch (backend) {
      case 'local':
        return <Brain className="text-hlx-primary" size={16} />;
      case 'claude':
        return <Zap className="text-orange-400" size={16} />;
      case 'gpt4':
        return <Zap className="text-green-400" size={16} />;
      default:
        return null;
    }
  };

  const getStatusColor = (backend: AIBackend, isActive: boolean) => {
    if (!isActive) return 'border-hlx-border text-hlx-muted hover:text-hlx-text';
    if (status?.backend === backend) {
      return status.isHealthy
        ? 'border-green-500/30 text-green-400 bg-green-500/5'
        : 'border-red-500/30 text-red-400 bg-red-500/5';
    }
    return 'border-hlx-border text-hlx-text';
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="p-2 rounded-lg bg-hlx-surface/30 border border-hlx-border/30 text-hlx-muted hover:text-hlx-text hover:bg-hlx-surface/50 hover:border-hlx-border/50 transition-all"
        title="AI Backend Settings"
      >
        <Settings size={16} />
      </button>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-hlx-panel border border-hlx-border rounded-xl shadow-2xl max-w-2xl w-full">
        {/* Header */}
        <div className="border-b border-hlx-border px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Settings size={20} className="text-hlx-primary" />
            <h2 className="text-xl font-bold text-white">AI Backend Settings</h2>
          </div>
          <button
            onClick={() => {
              setIsOpen(false);
              onClose?.();
            }}
            className="text-hlx-muted hover:text-white transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Status Section */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-hlx-text uppercase tracking-wider">Current Status</h3>
            {status && (
              <div
                className={`p-4 rounded-lg border flex items-start gap-3 ${
                  status.isHealthy
                    ? 'bg-green-500/5 border-green-500/30'
                    : 'bg-yellow-500/5 border-yellow-500/30'
                }`}
              >
                <div
                  className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${
                    status.isHealthy ? 'bg-green-400' : 'bg-yellow-400'
                  }`}
                />
                <div className="flex-1 min-w-0">
                  <p className={`text-sm font-bold ${status.isHealthy ? 'text-green-400' : 'text-yellow-400'}`}>
                    {getBackendDisplayName(status.backend)}
                  </p>
                  {status.isHealthy ? (
                    <p className="text-xs text-hlx-muted mt-1">
                      {status.model}
                      {status.ragEnabled && ` • RAG: ${status.ragDocuments} docs loaded`}
                    </p>
                  ) : (
                    <p className="text-xs text-hlx-muted mt-1">
                      {status.backend === 'local'
                        ? 'Waiting for Brain service...'
                        : 'API key not configured'}
                    </p>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Backend Selection */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-hlx-text uppercase tracking-wider">Available Backends</h3>
            <div className="space-y-2">
              {/* Local Brain */}
              <button
                onClick={() => {
                  setSelectedBackend('local');
                  handleSwitchBackend('local');
                }}
                disabled={loading}
                className={`w-full text-left p-4 rounded-lg border transition-all ${getStatusColor(
                  'local',
                  true
                )} ${currentBackend?.backend === 'local' ? 'ring-1 ring-hlx-primary' : ''}`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3 flex-1">
                    <div className="p-2 rounded bg-hlx-surface/50 flex-shrink-0">
                      <Brain size={16} className="text-hlx-primary" />
                    </div>
                    <div>
                      <p className="font-bold text-sm flex items-center gap-2">
                        Local Brain (Qwen3 8B)
                        {currentBackend?.backend === 'local' && (
                          <Check size={14} className="text-hlx-primary" />
                        )}
                      </p>
                      <p className="text-xs text-hlx-muted mt-1">
                        Fast, private, HLX-aware with RAG corpus access
                      </p>
                    </div>
                  </div>
                </div>
              </button>

              {/* Claude API */}
              <div className={`p-4 rounded-lg border transition-all ${getStatusColor('claude', true)}`}>
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-start gap-3 flex-1">
                    <div className="p-2 rounded bg-hlx-surface/50 flex-shrink-0">
                      <Zap size={16} className="text-orange-400" />
                    </div>
                    <div>
                      <p className="font-bold text-sm flex items-center gap-2">
                        Claude API
                        {currentBackend?.backend === 'claude' && (
                          <Check size={14} className="text-hlx-primary" />
                        )}
                      </p>
                      <p className="text-xs text-hlx-muted mt-1">Frontier model with advanced reasoning</p>
                    </div>
                  </div>
                </div>
                <input
                  type="password"
                  placeholder="sk-ant-..."
                  value={selectedBackend === 'claude' ? apiKey : ''}
                  onChange={(e) => setApiKey(e.target.value)}
                  disabled={loading}
                  className="w-full bg-hlx-bg border border-hlx-border rounded px-3 py-2 text-xs text-white placeholder-hlx-muted focus:outline-none focus:border-hlx-primary transition-colors"
                />
                <button
                  onClick={() => handleSwitchBackend('claude')}
                  disabled={loading || !apiKey}
                  className="mt-2 w-full px-3 py-2 rounded bg-orange-500/10 hover:bg-orange-500/20 border border-orange-500/30 text-orange-400 text-xs font-bold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Switching...' : 'Use Claude'}
                </button>
              </div>

              {/* GPT-4 API */}
              <div className={`p-4 rounded-lg border transition-all ${getStatusColor('gpt4', true)}`}>
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-start gap-3 flex-1">
                    <div className="p-2 rounded bg-hlx-surface/50 flex-shrink-0">
                      <Zap size={16} className="text-green-400" />
                    </div>
                    <div>
                      <p className="font-bold text-sm flex items-center gap-2">
                        GPT-4 API
                        {currentBackend?.backend === 'gpt4' && (
                          <Check size={14} className="text-hlx-primary" />
                        )}
                      </p>
                      <p className="text-xs text-hlx-muted mt-1">OpenAI frontier model</p>
                    </div>
                  </div>
                </div>
                <input
                  type="password"
                  placeholder="sk-..."
                  value={selectedBackend === 'gpt4' ? apiKey : ''}
                  onChange={(e) => setApiKey(e.target.value)}
                  disabled={loading}
                  className="w-full bg-hlx-bg border border-hlx-border rounded px-3 py-2 text-xs text-white placeholder-hlx-muted focus:outline-none focus:border-hlx-primary transition-colors"
                />
                <button
                  onClick={() => handleSwitchBackend('gpt4')}
                  disabled={loading || !apiKey}
                  className="mt-2 w-full px-3 py-2 rounded bg-green-500/10 hover:bg-green-500/20 border border-green-500/30 text-green-400 text-xs font-bold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Switching...' : 'Use GPT-4'}
                </button>
              </div>
            </div>
          </div>

          {/* Messages */}
          {error && (
            <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/30 flex items-start gap-2">
              <AlertCircle size={14} className="text-red-400 mt-0.5 flex-shrink-0" />
              <p className="text-xs text-red-400">{error}</p>
            </div>
          )}
          {success && (
            <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/30 flex items-start gap-2">
              <Check size={14} className="text-green-400 mt-0.5 flex-shrink-0" />
              <p className="text-xs text-green-400">{success}</p>
            </div>
          )}

          {/* Info */}
          <div className="p-3 rounded-lg bg-hlx-surface/30 border border-hlx-border/30 text-xs text-hlx-muted space-y-1">
            <p className="font-bold text-hlx-text mb-2">Default: Local Brain</p>
            <p>
              The Local Brain (Qwen3 8B) is optimized for HLX development with private RAG corpus access.
              It's fast and requires no API keys.
            </p>
            <p className="mt-2">
              Switch to frontier models (Claude/GPT-4) for advanced reasoning, but note that your queries
              will be sent to external APIs.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-hlx-border px-6 py-3 flex justify-end">
          <button
            onClick={() => {
              setIsOpen(false);
              onClose?.();
            }}
            className="px-4 py-2 rounded-lg bg-hlx-primary/10 hover:bg-hlx-primary/20 text-hlx-primary border border-hlx-primary/30 text-sm font-bold transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIBackendSettings;
