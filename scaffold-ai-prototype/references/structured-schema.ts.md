# Structured Schema Starter

Create `src/lib/schemas/analysis.ts`.

```typescript
import { z } from "zod";

export const analysisSchema = z.object({
  summary: z.string().describe("Two to three sentence summary"),
  scores: z.array(
    z.object({
      label: z.string(),
      value: z.number().min(0).max(10),
    })
  ),
  flaggedSections: z.array(
    z.object({
      originalText: z.string(),
      issue: z.string(),
    })
  ),
  rewriteSuggestions: z.array(
    z.object({
      original: z.string(),
      suggested: z.string(),
    })
  ),
  overallAssessment: z.string(),
});

export type Analysis = z.infer<typeof analysisSchema>;
```
