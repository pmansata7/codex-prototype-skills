# Voice Transcription Route Starter

Create `src/app/api/transcribe/route.ts`.

```typescript
import { experimental_transcribe as transcribe } from "ai";
import { groq } from "@ai-sdk/groq";

export async function POST(req: Request) {
  const formData = await req.formData();
  const audio = formData.get("audio");

  if (!(audio instanceof File)) {
    return Response.json({ error: "Missing audio file" }, { status: 400 });
  }

  const bytes = new Uint8Array(await audio.arrayBuffer());

  const result = await transcribe({
    model: groq.transcription("whisper-large-v3-turbo"),
    audio: bytes,
  });

  return Response.json({ text: result.text });
}
```
