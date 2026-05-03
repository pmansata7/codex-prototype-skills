# Agent Loop

Use this when the model must decide which tools to call and in what order across multiple steps.

## Agent (`src/lib/agents/research-agent.ts`)

```typescript
import { ToolLoopAgent, stepCountIs, tool } from "ai";
import { gateway } from "@ai-sdk/gateway";
import { z } from "zod";

export const researchAgent = new ToolLoopAgent({
  model: gateway("google/gemini-3-flash-preview"),
  instructions: "You are a research assistant. Use tools when they materially improve the answer.",
  tools: {
    search_notes: tool({
      description: "Search saved notes by keyword",
      inputSchema: z.object({ query: z.string() }),
      execute: async ({ query }) => ({
        query,
        matches: [`Sample match for ${query}`],
      }),
    }),
  },
  stopWhen: stepCountIs(12),
});
```

## Route (`src/app/api/chat/route.ts`)

```typescript
import { createAgentUIStreamResponse, type UIMessage } from "ai";
import { researchAgent } from "@/lib/agents/research-agent";

export const maxDuration = 60;

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  return createAgentUIStreamResponse({
    agent: researchAgent,
    uiMessages: messages,
  });
}
```

## Page Pattern

Use the same client structure as `tool-calling-chat`, then add renderers for `reasoning` and tool parts.

```tsx
if (part.type === "reasoning") {
  return <MessageResponse key={index}>{part.text}</MessageResponse>;
}
```

## Notes

- Always set a step limit.
- Keep agent tools narrow and inspectable.
- Prefer `tool-calling-chat` or `server-workflow` unless the model truly needs autonomy.
- `ToolLoopAgent` is still experimental. Use it deliberately and keep the surface area small.
