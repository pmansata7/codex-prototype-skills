# Chat Route Starter

Create `src/app/api/chat/route.ts`.

```typescript
import { convertToModelMessages, streamText, type UIMessage } from "ai";
import { gateway } from "@ai-sdk/gateway";

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: gateway("google/gemini-3-flash-preview"),
    system: "You are a helpful assistant.",
    messages: await convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
```

Swap the provider import and model string only if the project is not using the default path from `references/providers.md`.
