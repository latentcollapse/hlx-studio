# Brain Integration Guide - HELIX CLI

## Overview

The HLX Brain (Qwen3 8B + RAG) has been invisibly integrated into the HELIX CLI tab. It acts as a helpful, always-present assistant that provides code explanations, debugging help, and HLX-specific guidance through the RAG corpus.

## Architecture

### Core Components

1. **Brain Client** (`lib/brain-client.ts`)
   - Manages communication with local Brain service or frontier model APIs
   - Supports pluggable backends: Local Brain, Claude, GPT-4
   - Configuration persisted in localStorage
   - All endpoints support dynamic API base selection

2. **AI Context** (`lib/ai-context.ts`)
   - Provides hooks and utilities for backend management
   - `getAIBackendStatus()` - Get current backend health
   - `switchToLocalBrain()` - Switch to default Brain
   - `switchToClaude(apiKey)` - Switch to Claude API
   - `switchToGPT4(apiKey)` - Switch to GPT-4 API
   - Helper functions for validation and display names

3. **AI Backend Settings Modal** (`components/AIBackendSettings.tsx`)
   - Subtle settings button in the CLI header (gear icon)
   - Display current backend status
   - Switch between backends with API key input
   - Visual indicators for backend health
   - Info section explaining RAG and frontier models

4. **Enhanced HELIX CLI** (`views/HelixCLI.tsx`)
   - Brain status indicator in header
   - Auto-detection of AI queries (see Query Detection below)
   - Distinct visual styling for Brain responses (purple accent)
   - Loading indicators for Brain processing
   - Help text showing usage patterns

## Default Behavior

The Brain operates **invisibly by default**:
- Runs with Qwen3 8B + RAG corpus
- No separate tab needed
- Only activated when user explicitly asks
- Zero configuration required
- Can be easily swapped for frontier models via settings

## Query Detection

The system automatically detects when a user wants Brain assistance:

### Auto-Detected AI Queries
- Starts with `?` (question mark): `? what is HLX collapse`
- Starts with `!` (exclamation): `! debug this HLXL code`
- Starts with verb keywords:
  - `explain ...` - Code explanation
  - `debug ...` - Debugging help
  - `help ...` - General assistance
  - `what is ...` - Conceptual questions
  - `how do ...` - Process questions
  - `tell me ...` - Information request
- Contains `[brain]` or `brain:` - Explicit Brain invocation

### Standard Commands
Anything else is treated as a standard HLX command to the Helix orchestrator.

## Backend Configuration

### Default: Local Brain (Qwen3 8B + RAG)
- **Where**: `http://127.0.0.1:58300/brain`
- **Features**:
  - Fast inference (8B model)
  - Private execution (no external APIs)
  - RAG corpus access (HLX-specific knowledge)
  - Optimized for HLX 1:1 determinism
  - No API keys required

### Optional: Claude API
- **Setup**: Provide Claude API key in settings
- **Features**:
  - Frontier model with advanced reasoning
  - External API (privacy trade-off)
  - Higher quality responses for complex queries

### Optional: GPT-4 API
- **Setup**: Provide OpenAI API key in settings
- **Features**:
  - Frontier model with excellent reasoning
  - External API (privacy trade-off)
  - Excellent code analysis

## Storage

Backend configuration is stored in browser localStorage:
```javascript
// Key: 'hlx-studio-ai-backend'
{
  "backend": "local",  // or "claude", "gpt4"
  "apiKey": "sk-...",  // only for frontier models
  "customUrl": "..."   // optional custom endpoint
}
```

## Usage Examples

### Brain Queries
```
? what is HLX collapse
! explain this HLXL code
explain how validation works in HLX
debug: why does this fail?
tell me about content addressing
[brain] what are the benefits of determinism?
```

### Standard Commands
```
execute collapse(value)
query HLX runtime
observe contracts
validate HLXL syntax
```

## API Integration

### Brain Client Functions
All functions use the configured backend automatically:

```typescript
// Ask a question with RAG
await askBrain({
  question: "How do I collapse a value?",
  use_rag: true,
  temperature: 0.7
});

// Get backend status
const status = await getAIBackendStatus();

// Switch backends
switchToLocalBrain();
switchToClaude(apiKey);
switchToGPT4(apiKey);
```

### Backend Status Response
```typescript
interface AIBackendStatus {
  backend: 'local' | 'claude' | 'gpt4';
  isHealthy: boolean;
  model?: string;
  ragEnabled?: boolean;  // local only
  ragDocuments?: number; // local only
}
```

## UI Elements

### Header Status Indicator
- Shows current model and health status
- Green when healthy, yellow when checking/offline
- Updates every 30 seconds

### Settings Button
- Subtle gear icon in top-right of CLI
- Click to open backend configuration modal
- Shows current backend, health status, RAG docs
- Switch backends with one click

### Visual Distinction
- **User messages**: Primary color (blue)
- **Helix responses**: Default surface color
- **Brain responses**: Purple accent color
- **Loading state**: Purple animated dots with "Brain processing..."

### Help Text
Shows below input field:
```
Prefix with ? or ! for Brain assistance. Examples: ? what is HLX collapse
or ! explain this HLXL code
```

## Technical Details

### Message Structure
```typescript
interface Message {
  id: string;
  sender: 'user' | 'helix' | 'brain';
  text: string;
  timestamp: Date;
  source?: 'command' | 'ai';
}
```

### Response Flow
1. User enters query
2. System detects if it's an AI query
3. If Brain query + healthy: Call Brain service
4. Format response with Brain styling
5. Render distinct message bubble

## Behind the Scenes

### Health Monitoring
- Brain status checked on component mount
- Status refreshed every 30 seconds
- Graceful degradation if Brain unavailable
- Clear indicators for offline state

### Error Handling
- Network errors caught and displayed
- Brain unavailability doesn't break CLI
- Falls back to standard Helix responses
- User-friendly error messages

### Performance
- Local queries: ~100-500ms (Qwen3 8B)
- Frontier models: Variable (depends on API)
- RAG retrieval: ~200-300ms additional
- Caching handled by backend

## Configuration Files

### brain-client.ts
```typescript
// Example: Switching backends programmatically
import { switchToClaude } from './lib/ai-context';

switchToClaude('sk-ant-...your-key...');
// Brain client will now use Claude API for all queries
```

### AIBackendSettings.tsx
- Self-contained settings modal
- No external dependencies beyond React + lucide
- Responsive design for all screen sizes
- Real-time status updates

## Future Enhancements

1. **Query History**: Save queries for later reference
2. **Context Window**: Maintain conversation history with Brain
3. **Custom Models**: Support for Ollama custom endpoints
4. **RAG Fine-tuning**: User-provided corpus augmentation
5. **Response Caching**: Cache frequent queries
6. **Batch Processing**: Queue multiple queries efficiently

## Troubleshooting

### Brain Shows as Offline
1. Check if Brain service is running: `ps aux | grep brain`
2. Verify endpoint: `http://127.0.0.1:58300/brain/status`
3. Check console for error messages
4. Restart Brain service if needed

### API Key Not Working
1. Verify key format (Claude starts with `sk-ant-` or `sk-`)
2. Check key validity in provider dashboard
3. Ensure no extra whitespace
4. Try switching back to Local Brain

### Slow Responses
1. Local Brain: Check CPU usage and available memory
2. Frontier Models: Check internet connection and API rate limits
3. RAG queries: May take 200-300ms additional for retrieval

## Security Considerations

- **Local Brain**: Completely private, no external communication
- **Frontier Models**: API keys stored in browser localStorage
  - Consider using session storage for sensitive environments
  - Never commit API keys to version control
  - Use environment variables for CI/CD

## Files Modified/Created

1. **Modified**:
   - `/home/matt/hlx-dev-studio/lib/brain-client.ts` - Added backend config management
   - `/home/matt/hlx-dev-studio/views/HelixCLI.tsx` - Added Brain integration

2. **Created**:
   - `/home/matt/hlx-dev-studio/lib/ai-context.ts` - Backend management hooks
   - `/home/matt/hlx-dev-studio/components/AIBackendSettings.tsx` - Settings modal
   - `/home/matt/hlx-dev-studio/BRAIN_INTEGRATION.md` - This file

## Developer Notes

### Adding New Backend
To add a new AI backend (e.g., LLaMA, Mistral):

1. Update `AIBackend` type in `brain-client.ts`
2. Add case to `getApiBase()` function
3. Add switch case to `ai-context.ts` functions
4. Add UI section in `AIBackendSettings.tsx`
5. Implement API key validation function

### Extending Query Detection
Edit `isAIQuery()` in `HelixCLI.tsx`:
```typescript
const isAIQuery = (text: string): boolean => {
  // Add new patterns here
  return text.startsWith('your-new-prefix') || ...;
};
```

### Customizing Styling
Brain message styling in `HelixCLI.tsx`:
- Change purple colors to your preference
- Adjust animation timing in loading indicator
- Customize message bubble appearance

## Testing

### Manual Testing Checklist
- [ ] Brain responds to `?` prefix queries
- [ ] Brain responds to `!` prefix queries
- [ ] Status indicator shows correct backend
- [ ] Settings modal opens/closes
- [ ] Can switch to Claude API
- [ ] Can switch to GPT-4 API
- [ ] Can switch back to Local Brain
- [ ] Responses display with correct styling
- [ ] Loading indicator animates
- [ ] Brain offline gracefully falls back

### API Testing
```bash
# Test Brain status
curl http://127.0.0.1:58300/brain/status

# Test query
curl -X POST http://127.0.0.1:58300/brain/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"what is HLX?","use_rag":true}'
```
