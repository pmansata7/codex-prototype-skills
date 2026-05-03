---
name: ai-prototype-patterns
description: >
  Build or extend AI-powered features in a scaffolded Next.js prototype using
  current AI SDK and AI Elements patterns. Covers chat, tool-calling-chat,
  generative-ui, structured-generation, server-workflow, agent-loop, and voice.
  Use when the user asks to implement, extend, or refactor an AI-powered feature
  after scaffolding.
---

# AI Prototype Patterns

Choose the right implementation pattern for the feature, then use the matching reference file. Keep the code aligned with current AI SDK conventions so the frontend, route handlers, and tool streams stay compatible.

## Current SDK Conventions

Use these rules across every pattern:

- For chat-like UIs, manage the input locally. `useChat` does not own input state anymore.
- For chat, tool, generative UI, agent, and voice routes, accept `UIMessage[]`, convert with `convertToModelMessages`, and return `toUIMessageStreamResponse()`.
- For structured-generation, use `streamText` plus `Output.object()` on the server and `experimental_useObject` on the client.
- For tool calling, define tools with `tool({ inputSchema, ... })` and use `stopWhen: stepCountIs(n)` for multi-step loops.
- Keep each feature on its own route. Do not overload one route with unrelated patterns.
- Share schemas from `src/lib/schemas/` when both the route and the client depend on the same object shape.

## Pattern Selection

| User need | Pattern | Server primitive | Client primitive | Reference |
|---|---|---|---|---|
| Conversational assistant | `chat` | `streamText` | `useChat` | `references/chat.md` |
| Chat with tools or side-effect approvals | `tool-calling-chat` | `streamText` + `tool()` | `useChat` | `references/tool-calling-chat.md` |
| Model chooses UI cards/components | `generative-ui` | `streamText` + UI-rendering tools | `useChat` | `references/generative-ui.md` |
| Typed result object, form in -> object out | `structured-generation` | `streamText` + `Output.object()` | `experimental_useObject` | `references/structured-generation.md` |
| Deterministic multi-step server pipeline | `server-workflow` | `generateText` + `Output.object()` | `fetch` or custom progress UI | `references/server-workflow.md` |
| Autonomous multi-step agent with tools | `agent-loop` | `ToolLoopAgent` or `streamText` + tools | `useChat` | `references/agent-loop.md` |
| Speech in, text or audio out | `voice` | `experimental_transcribe`, `streamText`, optional `experimental_generateSpeech` | `useChat` + speech UI | `references/voice.md` |

## Guardrails

### Choose one primary pattern

Pick one primary pattern for the feature. If the user wants a hybrid, implement the dominant interaction model first and layer the second pattern after the base flow works.

Examples:

- chat plus structured result card -> start with `tool-calling-chat`
- document analysis form plus typed result -> `structured-generation`
- fixed multi-step backend pipeline with status updates -> `server-workflow`
- research assistant that decides which tools to call -> `agent-loop`

### Match the route to the pattern

Use route names that communicate the interaction model:

- `app/api/chat/route.ts`
- `app/api/analyze/route.ts`
- `app/api/workflow/route.ts`
- `app/api/transcribe/route.ts`

### Keep tool contracts stable

For tools and structured outputs, the schema is the contract. Stabilize the schema first, then build the UI against it.

### Prefer the smallest viable pattern

Do not jump to `agent-loop` when `server-workflow` or `tool-calling-chat` is sufficient.

Use this order of preference:

1. `structured-generation` when the output is typed and bounded
2. `server-workflow` when the steps are known in advance
3. `tool-calling-chat` when the user needs conversation plus tools
4. `agent-loop` only when the model must choose and sequence work autonomously

## Verification Expectations

After implementing a pattern, verify at least:

- `npm run build` exits with code 0
- the expected route file exists and exports `POST`
- the page or feature entry point imports the correct client primitive for the pattern
- shared schemas or tools exist where the reference expects them
- one minimal request to the route succeeds with status 200 when the environment is configured

## References

- chat: `references/chat.md`
- tool-calling chat: `references/tool-calling-chat.md`
- generative UI: `references/generative-ui.md`
- structured generation: `references/structured-generation.md`
- server workflow: `references/server-workflow.md`
- agent loop: `references/agent-loop.md`
- voice: `references/voice.md`
