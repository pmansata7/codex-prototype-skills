# Workflow Route Starter

Create `src/app/api/workflow/route.ts`.

```typescript
import { generateText, Output } from "ai";
import { gateway } from "@ai-sdk/gateway";
import { z } from "zod";

const classificationSchema = z.object({
  category: z.enum(["technical", "business", "creative"]),
  complexity: z.enum(["simple", "moderate", "complex"]),
});

export async function POST(req: Request) {
  const { input }: { input: string } = await req.json();
  const model = gateway("google/gemini-3-flash-preview");

  const { output: classification } = await generateText({
    model,
    output: Output.object({ schema: classificationSchema }),
    prompt: `Classify this request: ${input}`,
  });

  const { text: result } = await generateText({
    model,
    prompt: `You are handling a ${classification.category} request with ${classification.complexity} complexity. Produce a useful response for: ${input}`,
  });

  return Response.json({ classification, result });
}
```

This starter is intentionally deterministic and simple. Use `ai-prototype-patterns` when you need richer progress streaming or multi-stage workflow UIs.
