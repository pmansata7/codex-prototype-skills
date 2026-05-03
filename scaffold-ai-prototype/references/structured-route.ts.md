# Structured Route Starter

Create `src/app/api/analyze/route.ts`.

```typescript
import { Output, streamText } from "ai";
import { gateway } from "@ai-sdk/gateway";
import { analysisSchema } from "@/lib/schemas/analysis";

export const maxDuration = 30;

export async function POST(req: Request) {
  const { prompt }: { prompt: string } = await req.json();

  const result = streamText({
    model: gateway("google/gemini-3-flash-preview"),
    output: Output.object({ schema: analysisSchema }),
    prompt,
  });

  return result.toTextStreamResponse();
}
```
