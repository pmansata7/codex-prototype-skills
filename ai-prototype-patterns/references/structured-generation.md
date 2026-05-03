# Structured Generation

Use this when the user submits a bounded input and expects a typed object back.

## Shared Schema (`src/lib/schemas/analysis.ts`)

```typescript
import { z } from "zod";

export const analysisSchema = z.object({
  summary: z.string(),
  confidence: z.number().min(0).max(1),
  actions: z.array(z.string()),
});
```

## Route (`src/app/api/analyze/route.ts`)

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

## Page (`src/app/page.tsx`)

```tsx
"use client";

import { useState } from "react";
import { experimental_useObject as useObject } from "@ai-sdk/react";
import { analysisSchema } from "@/lib/schemas/analysis";

export default function StructuredPage() {
  const [input, setInput] = useState("");
  const { object, submit, isLoading, error } = useObject({
    api: "/api/analyze",
    schema: analysisSchema,
  });

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-3xl flex-col gap-6 p-6">
      <textarea
        value={input}
        onChange={(event) => setInput(event.currentTarget.value)}
        placeholder="Paste content to analyze..."
        className="min-h-40 w-full rounded-lg border p-3"
        disabled={isLoading}
      />
      <button
        type="button"
        onClick={() => submit({ prompt: input })}
        disabled={isLoading || !input.trim()}
        className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
      >
        {isLoading ? "Analyzing..." : "Analyze"}
      </button>

      {error && <p className="text-sm text-red-700">{error.message}</p>}

      {object && (
        <section className="space-y-3 rounded-lg border p-4">
          {object.summary && <p>{object.summary}</p>}
          {object.actions && object.actions.length > 0 && (
            <ul className="list-disc pl-5 text-sm">
              {object.actions.map((action, index) => (
                <li key={index}>{action}</li>
              ))}
            </ul>
          )}
        </section>
      )}
    </main>
  );
}
```

## Notes

- This pattern is not a chat UI. Keep it form -> result.
- The schema is the product contract. Refine the schema before polishing the UI.
- Use field descriptions in the schema when the model needs more guidance.
