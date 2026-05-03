# Provider Defaults

Use AI Gateway by default.

## Default path

Install:

```bash
npm install @ai-sdk/gateway
```

Import and default model:

```typescript
import { gateway } from "@ai-sdk/gateway";

const model = gateway("google/gemini-3-flash-preview");
```

Environment variable:

```env
AI_GATEWAY_API_KEY=your-key-here
```

Use this as the default unless the user explicitly asks for a direct provider.

## Direct Google provider

Install:

```bash
npm install @ai-sdk/google
```

Import and example model:

```typescript
import { google } from "@ai-sdk/google";

const model = google("gemini-3-flash-preview");
```

Environment variable:

```env
GOOGLE_GENERATIVE_AI_API_KEY=your-key-here
```

## Voice extras

For server-side transcription, install Groq:

```bash
npm install @ai-sdk/groq
```

```env
GROQ_API_KEY=your-key-here
```

For text-to-speech playback, also install OpenAI:

```bash
npm install @ai-sdk/openai
```

```env
OPENAI_API_KEY=your-key-here
```

## Notes

- Keep provider choice out of most starter files. Swap only the import and model constructor when the user chooses a different provider.
- The default skill path uses Gemini 3 Flash Preview through AI Gateway because it matches the preferred default model family and keeps provider switching simple.
