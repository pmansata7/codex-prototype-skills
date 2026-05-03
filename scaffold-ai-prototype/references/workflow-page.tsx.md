# Workflow Page Starter

Create `src/app/page.tsx`.

```tsx
"use client";

import { useState } from "react";

export default function Home() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<null | {
    classification: { category: string; complexity: string };
    result: string;
  }>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const runWorkflow = async () => {
    if (!input.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/workflow", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input }),
      });

      if (!response.ok) {
        throw new Error("Workflow request failed");
      }

      setResult(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Workflow request failed");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-3xl flex-col gap-6 p-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold">Workflow Prototype</h1>
        <p className="text-sm text-muted-foreground">
          Run a deterministic server-side workflow and display the result.
        </p>
      </header>

      <section className="space-y-3">
        <textarea
          value={input}
          onChange={(event) => setInput(event.currentTarget.value)}
          placeholder="Describe the task..."
          className="min-h-40 w-full rounded-lg border p-3"
          disabled={isLoading}
        />
        <button
          type="button"
          onClick={runWorkflow}
          disabled={isLoading || !input.trim()}
          className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          {isLoading ? "Running..." : "Run workflow"}
        </button>
      </section>

      {error && <p className="text-sm text-red-700">{error}</p>}

      {result && (
        <section className="space-y-3 rounded-lg border p-4">
          <p className="text-xs uppercase tracking-wide text-muted-foreground">
            {result.classification.category} / {result.classification.complexity}
          </p>
          <p className="text-sm">{result.result}</p>
        </section>
      )}
    </main>
  );
}
```
