---
name: scaffold-ai-prototype
description: >
  Scaffold a new AI prototype project using Next.js App Router, Vercel AI SDK,
  and AI Elements. Use when the user asks to create, initialize, bootstrap, or
  start a new AI-powered project, prototype, chat app, agent, dashboard, or
  generative UI. This skill handles project creation and starter setup only;
  for feature implementation after scaffolding, use ai-prototype-patterns.
---

# Scaffold AI Prototype

Create a new Next.js prototype with current AI SDK conventions, a pattern-matched starter, and only the components the starter actually needs.

## Defaults

- Create a new project unless the user explicitly asks to scaffold into an existing one.
- Infer the project name from the request when it is obvious. Ask one short question only if the name or target path is missing.
- If `SPEC.md` exists, read its `## AI Pattern` section and scaffold the matching starter.
- Default to AI Gateway with Gemini 3 Flash Preview. See `references/providers.md`.
- Install extra providers only when the chosen starter needs them.

## Steps

### 1. Create the project

Run:

```bash
npx create-next-app@latest <project-name> \
  --typescript --tailwind --app --src-dir --eslint \
  --import-alias "@/*" --use-npm --yes
cd <project-name>
```

Use non-interactive flags so the scaffold is reproducible.

### 2. Install the base dependencies

Run:

```bash
npm install ai @ai-sdk/react zod @ai-sdk/gateway
```

Install additional providers only when needed:

- direct Google provider: `npm install @ai-sdk/google`
- direct Anthropic provider: `npm install @ai-sdk/anthropic`
- direct OpenAI provider: `npm install @ai-sdk/openai`
- voice transcription: `npm install @ai-sdk/groq`
- voice playback: `npm install @ai-sdk/openai`

Use the provider reference for imports, env vars, and default model strings.

### 3. Determine the starter pattern

Use this order:

1. If `SPEC.md` exists, use its primary pattern.
2. Otherwise infer the pattern from the request.
3. Ask the user only if multiple patterns would produce materially different starters.

Use one of these exact pattern names:

- `chat`
- `tool-calling-chat`
- `generative-ui`
- `structured-generation`
- `server-workflow`
- `agent-loop`
- `voice`

### 4. Install the minimum UI surface for the starter

Install only the components the starter actually uses:

| Pattern | Components to install |
|---|---|
| `chat` | `conversation message prompt-input` |
| `tool-calling-chat` | `conversation message prompt-input tool confirmation` |
| `generative-ui` | `conversation message prompt-input tool` |
| `structured-generation` | none required for the starter |
| `server-workflow` | none required for the starter |
| `agent-loop` | `conversation message prompt-input tool reasoning` |
| `voice` | `conversation message prompt-input speech-input` |

Preferred install command:

```bash
npx ai-elements@latest add <components...>
```

Only install a larger component set if the user explicitly asks for it.

### 5. Create the shared app files

Always create these files:

| File | Reference |
|---|---|
| `src/app/layout.tsx` | `references/layout.tsx.md` |
| `src/app/globals.css` | `references/globals.css.md` |
| `.env.local` | `references/providers.md` |

### 6. Create the pattern starter files

Use the starter that matches the chosen pattern:

| Pattern | Files | References |
|---|---|---|
| `chat` | `src/app/api/chat/route.ts`, `src/app/page.tsx` | `references/chat-route.ts.md`, `references/chat-page.tsx.md` |
| `tool-calling-chat` | `src/app/api/chat/route.ts`, `src/app/page.tsx` | `references/chat-route.ts.md`, `references/chat-page.tsx.md` |
| `generative-ui` | `src/app/api/chat/route.ts`, `src/app/page.tsx` | `references/chat-route.ts.md`, `references/chat-page.tsx.md` |
| `agent-loop` | `src/app/api/chat/route.ts`, `src/app/page.tsx` | `references/chat-route.ts.md`, `references/chat-page.tsx.md` |
| `structured-generation` | `src/lib/schemas/analysis.ts`, `src/app/api/analyze/route.ts`, `src/app/page.tsx` | `references/structured-schema.ts.md`, `references/structured-route.ts.md`, `references/structured-page.tsx.md` |
| `server-workflow` | `src/app/api/workflow/route.ts`, `src/app/page.tsx` | `references/workflow-route.ts.md`, `references/workflow-page.tsx.md` |
| `voice` | `src/app/api/chat/route.ts`, `src/app/api/transcribe/route.ts`, `src/app/page.tsx` | `references/voice-chat-route.ts.md`, `references/voice-transcribe-route.ts.md`, `references/voice-page.tsx.md` |

For `tool-calling-chat`, `generative-ui`, and `agent-loop`, the chat starter is intentional. It gives the project the correct route shape and base interaction model; `ai-prototype-patterns` adds the specialized behavior next.

### 7. Create `.env.local`

Add only the environment variables required by the installed providers.

For the default path, start with:

```env
AI_GATEWAY_API_KEY=your-key-here
```

Add `GROQ_API_KEY` for voice transcription and `OPENAI_API_KEY` only if the project also needs text-to-speech.

### 8. Verify the scaffold

Run deterministic checks first:

```bash
npm run build
```

The scaffold is successful when:

- `npm run build` exits with code 0
- the expected starter route file exists
- the expected starter page file exists
- `.env.local` contains the required provider keys
- installed AI Elements components exist under `src/components/ai-elements/` when the starter uses them

Run `npm run dev` only when the user asks for a live check or you need to inspect runtime behavior.

## Output

After scaffolding, the project should contain:

- a Next.js App Router app
- AI SDK core and React packages
- a starter that matches the chosen primary pattern
- provider env var placeholders in `.env.local`
- AI Elements components only where the chosen starter uses them

## After Scaffolding

If `SPEC.md` exists, use it immediately to drive the next implementation steps.

Then switch to `ai-prototype-patterns` to build the real feature set on top of the starter.

## References

- providers and env vars: `references/providers.md`
- chat starter: `references/chat-route.ts.md`, `references/chat-page.tsx.md`
- structured starter: `references/structured-schema.ts.md`, `references/structured-route.ts.md`, `references/structured-page.tsx.md`
- workflow starter: `references/workflow-route.ts.md`, `references/workflow-page.tsx.md`
- voice starter: `references/voice-chat-route.ts.md`, `references/voice-transcribe-route.ts.md`, `references/voice-page.tsx.md`
