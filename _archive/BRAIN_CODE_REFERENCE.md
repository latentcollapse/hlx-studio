# Brain Integration - Code Reference

Quick reference for key code snippets and APIs.

## Core Functions

### Backend Configuration (lib/ai-context.ts)

#### Get Current Backend Status
```typescript
import { getAIBackendStatus } from './lib/ai-context';

const status = await getAIBackendStatus();
// Returns:
// {
//   backend: 'local' | 'claude' | 'gpt4',
//   isHealthy: boolean,
//   model?: string,
//   ragEnabled?: boolean,
//   ragDocuments?: number
// }
```

#### Switch Backends
```typescript
import {
  switchToLocalBrain,
  switchToClaude,
  switchToGPT4
} from './lib/ai-context';

// Use Local Brain (default)
switchToLocalBrain();

// Use Claude
switchToClaude('sk-ant-...');

// Use GPT-4
switchToGPT4('sk-...');
```

### Querying the Brain (lib/brain-client.ts)

#### Ask a Question
```typescript
import { askBrain } from './lib/brain-client';

const response = await askBrain({
  question: "What is HLX collapse?",
  use_rag: true,           // Use RAG corpus (local only)
  temperature: 0.7,         // LLM temperature
});
```

#### Explain Code
```typescript
import { explainCode } from './lib/brain-client';

const explanation = await explainCode({
  code: "let x = collapse(value);",
  language: "HLXL"
});
```

#### Debug Code
```typescript
import { debugCode } from './lib/brain-client';

const suggestions = await debugCode({
  code: "let x = collapse(42)\nlet y = x + 1",
  error_message: "SyntaxError: unexpected token",
  language: "HLXL"
});
```

#### Multi-turn Chat
```typescript
import { chatBrain } from './lib/brain-client';

const response = await chatBrain({
  messages: [
    { role: 'user', content: 'What is HLX?' },
    { role: 'assistant', content: 'HLX is a content-addressed...' },
    { role: 'user', content: 'How do I use it?' }
  ],
  temperature: 0.7
});
```

#### Get Brain Status
```typescript
import { getBrainStatus } from './lib/brain-client';

const status = await getBrainStatus();
// Returns:
// {
//   model: string,
//   ollama_url: string,
//   ollama_healthy: boolean,
//   corpus_loaded: boolean,
//   rag_documents: number,
//   rag_collection: string
// }
```

## UI Components

### Using AIBackendSettings Modal
```typescript
import AIBackendSettings from '../components/AIBackendSettings';

<AIBackendSettings
  onClose={() => {
    // Called when modal closes
    // Can refresh status here
  }}
/>
```

### Using in HelixCLI
```typescript
import { getAIBackendStatus } from '../lib/ai-context';

// In component
const [aiStatus, setAiStatus] = useState<AIBackendStatus | null>(null);

useEffect(() => {
  const loadStatus = async () => {
    const status = await getAIBackendStatus();
    setAiStatus(status);
  };
  loadStatus();
}, []);

// Render status badge
{aiStatus && (
  <div className="status-badge">
    {aiStatus.isHealthy ? '✓ Ready' : '○ Offline'}
    {aiStatus.model}
  </div>
)}
```

## Query Detection

### Detecting AI Queries
```typescript
const isAIQuery = (text: string): boolean => {
  const lower = text.toLowerCase();
  return (
    text.startsWith('?') ||
    text.startsWith('!') ||
    text.startsWith('explain ') ||
    text.startsWith('debug ') ||
    text.startsWith('help ') ||
    text.startsWith('what is ') ||
    text.startsWith('how do ') ||
    text.startsWith('tell me ') ||
    lower.includes('brain:') ||
    lower.includes('[brain]')
  );
};
```

### Using Query Detection
```typescript
const handleSend = async () => {
  const isAI = isAIQuery(input);

  if (isAI && aiStatus?.isHealthy) {
    // Send to Brain
    const response = await askBrain({
      question: input.replace(/^[?!]\s*/, ''),
      use_rag: true
    });
  } else {
    // Send to Helix orchestrator
    const response = await executeHelixCommand(input);
  }
};
```

## Storage & Configuration

### Managing Backend Config
```typescript
import {
  getBackendConfig,
  setBackendConfig
} from './lib/brain-client';

// Get current config
const config = getBackendConfig();
console.log(config.backend); // 'local' | 'claude' | 'gpt4'

// Save new config
setBackendConfig({
  backend: 'claude',
  apiKey: 'sk-ant-...'
});

// Switch back to local
setBackendConfig({
  backend: 'local'
});
```

### localStorage Schema
```javascript
// Stored as JSON in localStorage['hlx-studio-ai-backend']
{
  "backend": "local" | "claude" | "gpt4",
  "apiKey": "sk-...",           // optional
  "customUrl": "http://..."     // optional
}
```

## Error Handling

### Catching Brain Errors
```typescript
import { BrainApiError } from './lib/brain-client';

try {
  const response = await askBrain({
    question: "What is collapse?"
  });
} catch (error) {
  if (error instanceof BrainApiError) {
    console.error(`Brain error (${error.status}): ${error.message}`);
    console.error('Details:', error.details);
  } else {
    console.error('Unknown error:', error);
  }
}
```

### Graceful Degradation
```typescript
// Check Brain health before querying
const status = await getAIBackendStatus();

if (status.isHealthy) {
  // Safe to query Brain
  const response = await askBrain({ question: '...' });
} else {
  // Brain offline, fall back to standard command
  console.log('Brain offline, using standard command handler');
}
```

## Message Structure

### Message Interface
```typescript
interface Message {
  id: string;                        // Unique identifier
  sender: 'user' | 'helix' | 'brain'; // Message source
  text: string;                      // Message content
  timestamp: Date;                   // When sent
  source?: 'command' | 'ai';         // Internal classification
}
```

### Creating Messages
```typescript
const userMessage: Message = {
  id: Date.now().toString(),
  sender: 'user',
  text: userInput,
  timestamp: new Date()
};

const brainMessage: Message = {
  id: (Date.now() + 1).toString(),
  sender: 'brain',
  text: response,
  timestamp: new Date(),
  source: 'ai'
};
```

## Display & Styling

### Brain Message Styling
```tsx
{/* Purple accent for Brain */}
<div className="bg-purple-500/5 border-purple-500/20 text-white">
  {message.text}
</div>
```

### Status Indicator Styling
```tsx
{/* Green when healthy */}
<div className={`
  px-3 py-1 rounded-full border text-xs
  ${aiStatus?.isHealthy
    ? 'bg-green-500/5 border-green-500/30 text-green-400'
    : 'bg-yellow-500/5 border-yellow-500/30 text-yellow-400'
  }`}>
  {aiStatus?.isHealthy ? '✓' : '○'} {aiStatus?.model}
</div>
```

### Loading Indicator
```tsx
{/* Purple animated dots */}
<div className="flex gap-1">
  <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce"
       style={{ animationDelay: '0ms' }} />
  <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce"
       style={{ animationDelay: '150ms' }} />
  <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce"
       style={{ animationDelay: '300ms' }} />
</div>
<span className="text-xs text-purple-300 ml-2">Brain processing...</span>
```

## Advanced Usage

### Custom Backend URL
```typescript
import { setBackendConfig } from './lib/brain-client';

// Point to custom Ollama instance
setBackendConfig({
  backend: 'local',
  customUrl: 'http://custom-server:5000/api'
});
```

### Validation Helper
```typescript
import { validateAPIKey } from './lib/ai-context';

if (!validateAPIKey('claude', apiKey)) {
  console.error('Invalid Claude API key');
  return;
}

switchToClaude(apiKey);
```

### Backend Display Names
```typescript
import { getBackendDisplayName } from './lib/ai-context';

const displayName = getBackendDisplayName('claude');
// Returns: "Claude API"

const displayName = getBackendDisplayName('local');
// Returns: "Local Brain (Qwen3 8B)"
```

## Integration Patterns

### In React Components
```typescript
import { useState, useEffect } from 'react';
import { getAIBackendStatus } from '../lib/ai-context';
import { askBrain } from '../lib/brain-client';

export function MyComponent() {
  const [status, setStatus] = useState(null);
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getAIBackendStatus().then(setStatus);
  }, []);

  const query = async (question: string) => {
    if (!status?.isHealthy) return;

    setLoading(true);
    try {
      const answer = await askBrain({ question, use_rag: true });
      setResponse(answer);
    } catch (error) {
      setResponse(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {status?.isHealthy ? '✓ Ready' : '○ Offline'}
      <button onClick={() => query('What is HLX?')}>Ask Brain</button>
      {loading && <p>Loading...</p>}
      {response && <p>{response}</p>}
    </div>
  );
}
```

### Error Boundary Pattern
```typescript
async function safeBrainQuery(question: string): Promise<string> {
  try {
    const status = await getAIBackendStatus();

    if (!status.isHealthy) {
      return 'Brain is currently offline';
    }

    return await askBrain({ question, use_rag: true });
  } catch (error) {
    console.error('Brain query failed:', error);
    return 'Failed to process query. Please try again.';
  }
}
```

## Common Patterns

### Conditional Rendering Based on Backend
```typescript
if (aiStatus?.backend === 'local') {
  // Show RAG-specific UI
  <div>RAG: {aiStatus.ragDocuments} documents</div>
} else if (aiStatus?.backend === 'claude') {
  // Show Claude-specific UI
  <div>Using Claude API</div>
}
```

### Switching with Confirmation
```typescript
const handleSwitch = async (newBackend: AIBackend) => {
  const confirmed = window.confirm(
    `Switch to ${getBackendDisplayName(newBackend)}?`
  );

  if (confirmed) {
    if (newBackend === 'local') {
      switchToLocalBrain();
    } else if (newBackend === 'claude') {
      switchToClaude(apiKey);
    }
  }
};
```

### Auto-retry on Failure
```typescript
async function askBrainWithRetry(
  question: string,
  maxRetries = 3
): Promise<string> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await askBrain({ question });
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
  throw new Error('Max retries exceeded');
}
```

---

## See Also

- **BRAIN_INTEGRATION.md** - Full technical documentation
- **BRAIN_QUICKSTART.md** - User guide and examples
- **IMPLEMENTATION_SUMMARY.md** - Architecture and design decisions

## File Locations

- `lib/brain-client.ts` - Brain API client
- `lib/ai-context.ts` - Backend management
- `components/AIBackendSettings.tsx` - Settings UI
- `views/HelixCLI.tsx` - CLI integration
