# Server Workflow

Use this when the server controls the sequence of steps and the model should not decide what to do next.

## Route (`src/app/api/workflow/route.ts`)

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

  const { text: draft } = await generateText({
    model,
    prompt: `You are handling a ${classification.category} request with ${classification.complexity} complexity. Produce a useful response for: ${input}`,
  });

  const { output: quality } = await generateText({
    model,
    output: Output.object({
      schema: z.object({
        score: z.number().min(1).max(10),
        passes: z.boolean(),
      }),
    }),
    prompt: `Score this response from 1-10 and say whether it is ready for the user. Response: ${draft}`,
  });

  return Response.json({ classification, draft, quality });
}
```

## Page Pattern

```tsx
const response = await fetch("/api/workflow", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ input }),
});

const result = await response.json();
```

Render the classification, quality score, and final draft as separate sections so the user can see the workflow output shape.

## Notes

- Use workflows when the server should own the step order.
- Add progress streaming only after the deterministic route shape is correct.
- If the model needs to choose tools or branch repeatedly on its own, move to `agent-loop`.
