# Generative UI

Use this when the model should decide which UI card or component to render, not just what text to return.

## Route (`src/app/api/chat/route.ts`)

```typescript
import {
  convertToModelMessages,
  stepCountIs,
  streamText,
  tool,
  type UIMessage,
} from "ai";
import { gateway } from "@ai-sdk/gateway";
import { z } from "zod";

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: gateway("google/gemini-3-flash-preview"),
    system:
      "Render rich UI through tools when a card, table, or product summary is more useful than plain text.",
    messages: await convertToModelMessages(messages),
    tools: {
      show_product_card: tool({
        description: "Render a product summary card",
        inputSchema: z.object({
          name: z.string(),
          price: z.string(),
          summary: z.string(),
        }),
        execute: async (input) => input,
      }),
    },
    stopWhen: stepCountIs(3),
  });

  return result.toUIMessageStreamResponse();
}
```

## Page Pattern

Render the tool part with a custom component instead of a generic JSON block:

```tsx
if (part.type === "tool-show_product_card" && part.output) {
  return (
    <article key={index} className="rounded-lg border p-4">
      <h3 className="font-semibold">{part.output.name}</h3>
      <p className="text-sm text-muted-foreground">{part.output.summary}</p>
      <p className="mt-2 text-sm font-medium">{part.output.price}</p>
    </article>
  );
}
```

## Notes

- Keep tool outputs UI-shaped. The tool should return the exact fields the component needs.
- Generative UI is still tool calling. The difference is the frontend renders tool results as first-class components.
- If the result is mostly prose, use plain chat instead.
