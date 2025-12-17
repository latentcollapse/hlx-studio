# Brain Integration Quick Start Guide

## What's New?

The HLX Brain (Qwen3 8B + RAG) is now **invisibly integrated** into the HELIX CLI tab. No separate tab, no complexity - just natural AI assistance when you need it.

## User Guide

### Starting the CLI

1. Open Helix Studio normally
2. Click the **HELIX** tab
3. You'll see Brain status in the header (green dot = healthy)

### Using the Brain

#### Option 1: Question Mark (Simple)
```
? what is HLX collapse
? explain determinism
? how do I validate contracts
```

#### Option 2: Exclamation (Emphasis)
```
! debug my HLXL code
! what's wrong here
! help me understand this
```

#### Option 3: Natural Language
Start with these verbs and the system auto-detects:
```
explain how contracts work
debug this validation error
help me with HLX basics
what is content addressing
how do I structure a contract
tell me about RAG
```

#### Option 4: Explicit Tag
```
[brain] what's the best practice for collapse?
brain: explain this code snippet
```

#### Standard Commands (No Brain)
Just type normally for HLX commands:
```
execute collapse(myValue)
query runtime status
validate HLXL syntax
```

### Settings

Click the **gear icon** in the top-right to:
- See current Brain status
- Switch to Claude API (add key)
- Switch to GPT-4 API (add key)
- Switch back to Local Brain
- View health indicators

### Visual Indicators

**Header Status Badge**:
- Green dot + "Local Brain (Qwen3 8B)" = Ready
- Yellow dot = Checking/Starting up
- Red/Missing = Brain offline (falls back gracefully)

**Message Bubbles**:
- **User**: Blue accent (your questions)
- **Helix**: Gray (orchestrator responses)
- **Brain**: Purple accent (AI responses)

**Loading**: Purple animated dots + "Brain processing..."

## Default Setup (No Configuration Needed)

✓ Local Brain (Qwen3 8B) - enabled by default
✓ RAG corpus - automatically loaded
✓ Privacy - all processing local
✓ Speed - sub-second to ~1s responses
✓ Cost - free, no API keys required

## Optional: Use Frontier Models

Click Settings gear → Enter API key:

### Claude API
```
Key format: sk-ant-... or sk-...
Best for: Advanced reasoning, complex code analysis
Privacy: Sends queries to Anthropic servers
Cost: Pay per token
```

### GPT-4 API
```
Key format: sk-...
Best for: Excellent code analysis, detailed explanations
Privacy: Sends queries to OpenAI servers
Cost: Pay per token
```

## Examples

### Scenario 1: Quick Question
```
User: ? what does collapse do in HLX
Brain: Returns explanation using RAG corpus
```

### Scenario 2: Code Help
```
User: ! explain this HLXL code
Brain: Analyzes code and provides HLX-specific guidance
```

### Scenario 3: Debugging
```
User: debug: why is my validation failing?
Brain: Suggests fixes with HLX best practices
```

### Scenario 4: Learning
```
User: tell me about content addressing
Brain: Explains concepts with examples from corpus
```

### Scenario 5: Normal Commands
```
User: execute collapse(value)
Helix: Processes command normally (no Brain)
```

## FAQ

### Q: Will the Brain always run?
**A**: No. Brain is only used when you prefix with `?`, `!`, or use trigger words. Standard HLX commands go directly to the orchestrator.

### Q: Is my data private?
**A**: Yes, by default. Local Brain keeps everything private. If you switch to Claude/GPT-4, your queries go to those providers' APIs.

### Q: Can I switch back to Local Brain?
**A**: Anytime. Click Settings → "Use Local Brain (Qwen3 8B)" button.

### Q: What if Brain is offline?
**A**: Falls back gracefully. You'll see a status indicator, but the CLI still works. Standard HLX commands execute normally.

### Q: Can I use the RAG corpus with frontier models?
**A**: Currently, RAG is local-only (Qwen3 feature). Frontier models get context from their training data instead.

### Q: How much does the Local Brain cost?
**A**: Nothing. It runs locally. Your only cost is the compute resources on your machine.

### Q: What if I need more than Local Brain's capabilities?
**A**: Switch to Claude or GPT-4 via Settings. They're frontier models with broader knowledge, but you pay per token.

## Keyboard Shortcuts

- **Enter** - Send query
- **Shift+Enter** - New line in input (future)
- **?** prefix - Ask Brain
- **!** prefix - Ask Brain (emphasis)

## Status Indicators

| Indicator | Meaning | Action |
|-----------|---------|--------|
| 🟢 Green dot + Model name | Brain ready | Use normally |
| 🟡 Yellow dot | Brain starting | Wait a moment |
| 🔴 Red dot or missing | Brain offline | Use standard commands or check service |

## What You Can Ask

### Code & HLX
- "explain this HLXL code"
- "how do I collapse a value?"
- "what's the best way to structure contracts?"
- "debug this validation error"

### Concepts
- "what is content addressing?"
- "explain determinism in HLX"
- "how does the orchestrator work?"
- "what are the benefits of 1:1 mapping?"

### Best Practices
- "what are HLX naming conventions?"
- "how should I organize my contracts?"
- "what's the proper error handling pattern?"
- "how do I optimize performance?"

### Troubleshooting
- "why is my code failing?"
- "what does this error mean?"
- "how do I fix this issue?"
- "is there a better way to do this?"

## System Architecture (For Developers)

### Files
- `lib/brain-client.ts` - Brain API client with backend switching
- `lib/ai-context.ts` - Backend management hooks
- `components/AIBackendSettings.tsx` - Settings modal
- `views/HelixCLI.tsx` - Enhanced CLI with Brain integration
- `BRAIN_INTEGRATION.md` - Full technical documentation

### Storage
Backend preference saved to browser localStorage:
```json
{
  "backend": "local",
  "apiKey": "sk-..."
}
```

### Endpoints
- **Local Brain**: `http://127.0.0.1:58300/brain`
- **Your Custom**: Via settings (if configured)

## Troubleshooting

### Brain won't respond
1. Check status indicator (should be green)
2. Click settings to verify Brain is selected
3. Try standard command to verify CLI works
4. Check console for error messages

### Brain seems slow
1. Local Brain is normal ~1s for complex queries
2. RAG retrieval adds ~200-300ms
3. Frontier models depend on internet speed
4. Try simpler query for quick response

### Want to switch backends
1. Click gear icon (settings)
2. Select desired backend
3. Enter API key if needed
4. Click "Use [Backend]"

### Lost my API key
1. Click settings
2. Paste new key
3. Click "Use [Backend]" to save

## Tips & Tricks

### Speed Up Queries
- Use shorter, more specific questions
- Skip unnecessary context
- Local Brain is fastest for most tasks

### Better Answers
- Include code samples for debugging
- Specify HLX-specific context
- Ask follow-up questions in chat

### Privacy First
- Stick with Local Brain for sensitive code
- Use frontier models only when needed
- Clear credentials if sharing machine

### RAG Power
- Ask questions about HLX fundamentals (corpus has docs)
- Local Brain has specialized HLX knowledge
- Frontier models have broader general knowledge

## What Gets Sent Where?

### Local Brain (Default)
- ✓ Stays on your machine
- ✓ Never sent anywhere
- ✓ Completely private
- ✓ No internet needed

### Claude API
- Query text sent to Anthropic
- Response text returned
- Anthropic's privacy policy applies
- API key used for authentication

### GPT-4 API
- Query text sent to OpenAI
- Response text returned
- OpenAI's privacy policy applies
- API key used for authentication

## Next Steps

1. **Try it out**: Use Brain by prefixing `? what is HLX?`
2. **Explore RAG**: Ask about HLX concepts
3. **Read full docs**: See BRAIN_INTEGRATION.md for advanced usage
4. **Customize**: Switch backends in settings as needed

---

**That's it!** Brain is now ready to help. No setup required. Just start asking questions.
