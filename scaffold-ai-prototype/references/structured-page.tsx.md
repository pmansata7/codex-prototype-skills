# Structured Page Starter

Create `src/app/page.tsx`.

```tsx
"use client";

import { useState } from "react";
import { experimental_useObject as useObject } from "@ai-sdk/react";
import { analysisSchema } from "@/lib/schemas/analysis";

export default function Home() {
  const [input, setInput] = useState("");
  const { object, submit, isLoading, error } = useObject({
    api: "/api/analyze",
    schema: analysisSchema,
  });

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-3xl flex-col gap-6 p-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold">Structured Analysis</h1>
        <p className="text-sm text-muted-foreground">
          Paste content, run the analysis, and render the typed result as it streams in.
        </p>
      </header>

      <section className="space-y-3">
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
      </section>

      {error && <p className="text-sm text-red-700">{error.message}</p>}

      {object && (
        <section className="space-y-4 rounded-lg border p-4">
          {object.summary && (
            <div>
              <h2 className="font-medium">Summary</h2>
              <p className="text-sm text-muted-foreground">{object.summary}</p>
            </div>
          )}

          {object.scores && object.scores.length > 0 && (
            <div>
              <h2 className="font-medium">Scores</h2>
              <ul className="space-y-2 text-sm">
                {object.scores.map((score, index) => (
                  <li key={index}>
                    {score?.label}: {score?.value}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      )}
    </main>
  );
}
```
