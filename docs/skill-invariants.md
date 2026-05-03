# Skill Invariants

Purpose: define the local conventions that the core skills must preserve unless the repo intentionally changes direction.

## Cross-Skill Invariants

- All three skills must use the same primary pattern names:
  - `chat`
  - `tool-calling-chat`
  - `generative-ui`
  - `structured-generation`
  - `server-workflow`
  - `agent-loop`
  - `voice`
- `spec-to-prototype` must emit plans that `scaffold-ai-prototype` can scaffold directly.
- `scaffold-ai-prototype` must scaffold starters that `ai-prototype-patterns` can extend directly.
- The repo default model path is AI Gateway with Gemini 3 Flash Preview unless intentionally changed.

## Current SDK Conventions

These are the conventions the repo currently expects. If upstream changes require a different approach, update this file and the affected skills together.

### Chat-Like Patterns

For `chat`, `tool-calling-chat`, `generative-ui`, `agent-loop`, and `voice`:

- client uses local input state
- client uses `useChat`
- server accepts `UIMessage[]`
- server uses `convertToModelMessages`
- server returns `toUIMessageStreamResponse()`

### Structured Generation

For `structured-generation`:

- server uses `streamText`
- server uses `Output.object()`
- client uses `experimental_useObject`
- shared schema lives in `src/lib/schemas/`

### Server Workflow

For `server-workflow`:

- server owns step order
- use `generateText` plus `Output.object()` where structured evaluation or classification is needed
- do not use agent loops unless the model must decide the plan itself

### Voice

For `voice`:

- transcription is isolated in `/api/transcribe`
- spoken input still feeds a normal chat-like route
- text-to-speech is optional and isolated in a separate route if added
- experimental voice APIs are treated as high-risk maintenance surfaces

## Skill-Specific Invariants

### spec-to-prototype

- must define binary success criteria
- must avoid subjective acceptance language
- must emit route/file names that match the selected primary pattern

### scaffold-ai-prototype

- must be pattern-aware
- must install only the minimum AI Elements surface for the chosen starter by default
- must centralize provider/model guidance in references instead of scattering it

### ai-prototype-patterns

- must prefer the smallest viable pattern
- must keep reference examples lean and current
- must not mix incompatible route/client primitives across patterns

## Validation Invariants

- every skill folder must contain `agents/openai.yaml`
- all skill markdown and yaml files should stay ASCII-only unless there is a strong reason otherwise
- references linked from a skill body must exist
- stale APIs such as `streamObject(` and `toDataStreamResponse()` should fail validation unless the repo intentionally re-adopts them
