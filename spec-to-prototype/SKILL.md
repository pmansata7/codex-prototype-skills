---
name: spec-to-prototype
description: >
  Convert a rough product idea into an agent-ready SPEC.md with prioritized work
  packages, a dependency graph, and binary success criteria that a coding agent can
  verify itself. Use when the user describes a new idea, wants to spec out a
  prototype, or says something like "I have an idea for..." or "let's spec this
  out". This skill runs before scaffold-ai-prototype: it produces the execution
  plan, scaffolding produces the project.
---

# Spec to Prototype

Convert a plain-language product idea into a structured `SPEC.md` that a coding agent can execute work package by work package. Keep the spec tightly aligned with `scaffold-ai-prototype` and `ai-prototype-patterns` so the next agent can scaffold and build without re-interpreting the plan.

## Workflow Position

```text
ideation
  ->
spec-to-prototype
  ->
scaffold-ai-prototype
  ->
ai-prototype-patterns
```

`ai-prototype-patterns` is required alongside this skill. Use the exact same pattern names and route conventions so the scaffold and implementation skills can follow the spec directly.

## Steps

### 1. Extract the idea before asking questions

Extract these fields from the user's request first:

1. `What`: the core functionality in plain language
2. `Who`: the target user and usage context
3. `Core interaction`: what the user actually does in the UI

Ask follow-up questions only when a missing or ambiguous field would materially change the architecture, starter pattern, or work-package order.

### 2. Choose the primary AI pattern

Use `ai-prototype-patterns` to choose one primary pattern from this exact set:

- `chat`
- `tool-calling-chat`
- `generative-ui`
- `structured-generation`
- `server-workflow`
- `agent-loop`
- `voice`

Choose the primary pattern yourself from the request. Add secondary patterns only when they are a real near-term extension, not a vague future possibility.

### 3. Lock the implementation contract

Write the spec so it matches the implementation primitives expected by the other two skills:

- `chat`, `tool-calling-chat`, `generative-ui`, `agent-loop`, `voice`
  Use `useChat` on the client and a UI-message streaming route on the server.
- `structured-generation`
  Use `streamText` plus `Output.object()` on the server and `experimental_useObject` on the client.
- `server-workflow`
  Use deterministic server-side steps with `generateText` and `Output.object()` where structured classification or evaluation is needed.

Use route and file names that match the chosen pattern unless the user explicitly wants something else:

- chat-like patterns: `src/app/api/chat/route.ts`, `src/app/page.tsx`
- structured generation: `src/app/api/analyze/route.ts`, `src/lib/schemas/*.ts`, `src/app/page.tsx`
- server workflow: `src/app/api/workflow/route.ts`, `src/app/page.tsx`
- voice: `src/app/api/chat/route.ts`, `src/app/api/transcribe/route.ts`, `src/app/page.tsx`

### 4. Generate `SPEC.md`

Write the spec to `./SPEC.md` in the current working directory.

Use `references/spec-template.md` for structure and level of detail.

Create 3-7 work packages. The package set must fit the chosen pattern rather than forcing the same scaffold/API/UI split every time.

Common work-package shapes:

| Pattern | Typical work packages |
|---|---|
| `chat` | scaffold, chat route, chat page, polish/error states |
| `tool-calling-chat` | scaffold, tool definitions, route, tool UI rendering, approval/error states |
| `generative-ui` | scaffold, tool definitions, UI renderer components, chat route/page, safety/error states |
| `structured-generation` | scaffold, schema, analyze route, form/result page, validation/error states |
| `server-workflow` | scaffold, workflow steps, workflow route, results page, validation/error states |
| `agent-loop` | scaffold, shared tools, agent definition, route/page, limits/approval/error states |
| `voice` | scaffold, transcribe route, voice page, chat route, fallback/error states |

Use these baseline package types when they fit:

| WP | Typical coverage | Priority |
|---|---|---|
| WP-1 | Project scaffolding and dependencies | P0 |
| WP-2 | API route(s), tools, schemas, workflow logic | P0 |
| WP-3 | Core UI and primary interaction | P0 |
| WP-4 | Frontend/backend integration | P0 |
| WP-5 | Pattern-specific or product-specific logic | P0 or P1 |
| WP-6 | Validation, loading, error states, edge cases | P1 |
| WP-7 | Polish or secondary features | P2 |

### 5. Write binary success criteria

For each work package, write 2-4 success criteria. Every criterion must be:

- Binary: pass or fail only
- Self-verifiable by the agent: command, test, HTTP request, or file/code inspection
- Specific: tied to exact files, exports, routes, fields, or observable results

Prefer criteria like:

- `npm run build` exits with code 0
- `src/app/api/chat/route.ts` exists and exports `POST`
- `POST /api/analyze` with a minimal valid payload returns status 200
- `src/lib/schemas/analysis.ts` exports the fields `summary`, `scores`, `actions`
- `src/app/page.tsx` imports `experimental_useObject as useObject`

Avoid criteria like:

- "The UI looks clean"
- "Responses are helpful"
- "It works correctly"
- "Performance is acceptable"
- "No console errors appear" unless the spec also defines how that is checked automatically

### 6. Build the dependency graph

Express dependencies explicitly as `WP-X depends on WP-Y`.

Also include a short execution-order graph that makes parallel work obvious.

For many prototypes, UI and backend foundations can proceed in parallel after the scaffold. Do not assume that if the chosen pattern implies a different order.

### 7. Keep notes implementation-relevant

Use `Notes` only for decisions, deferred questions, assumptions, or constraints that matter during implementation.

Do not use `Notes` for generic brainstorming or product commentary.

### 8. Optional experiment logging

Only log the project to an experiments tracker if the current repo already contains one or the user explicitly asks for it.

When an experiments tracker is requested, append a row in this format:

```markdown
| {YYYY-MM-DD} | {slug} | {primary-pattern} | {one-line description} | {absolute project path} | active |
```

If no tracker exists and the user did not ask for one, skip this step.

## `SPEC.md` Format

```markdown
# {Project Title}

> {One-line description of what this is}

## Idea

**What:** {what it does}
**Who:** {who it's for}
**Core interaction:** {what the user actually does}

## AI Pattern

**Primary:** {pattern name}
**Secondary:** {other patterns if applicable, or "none"}

## Work Packages

### WP-1: {Title}
**Priority:** P0
**Dependencies:** none
**Description:** {2-3 sentences on what this work package delivers}

**Success criteria:**
- [ ] {binary criterion 1}
- [ ] {binary criterion 2}
- [ ] {binary criterion 3}

### WP-2: {Title}
**Priority:** P0
**Dependencies:** WP-1
...

## Dependency Graph

{ASCII or text representation of the execution order}

## Notes

{Only implementation-relevant context, decisions, or open questions}
```

## After Saving `SPEC.md`

Tell the user:

1. The spec is saved at `./SPEC.md`
2. They should scaffold the project with the same primary pattern
3. After scaffolding, the agent should execute work packages in dependency order
4. Each success criterion is designed to be checked and ticked off during implementation

## Reference

See `references/spec-template.md` for a complete example spec.
