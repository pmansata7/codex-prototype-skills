# Voice

Use this when the user speaks, the app transcribes audio, and the result feeds a chat or assistant flow.

## Transcription Route (`src/app/api/transcribe/route.ts`)

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

## Chat Route (`src/app/api/chat/route.ts`)

Use the normal chat route pattern from `references/chat.md`, but keep the system prompt concise and speech-friendly.

## Page Pattern

```tsx
<SpeechInput
  onTranscriptionChange={setInput}
  onAudioRecorded={handleAudioRecorded}
/>
```

Send the transcribed text through the normal `useChat` flow. Keep the first version simple: speech fills the text box, the user reviews it, then sends it.

## Optional TTS

If the product needs spoken responses, add `experimental_generateSpeech` in a separate `/api/speech` route and only then install `@ai-sdk/openai`.

## Notes

- Keep the first voice version text-response only unless the user explicitly wants full speech output.
- `experimental_transcribe` and `experimental_generateSpeech` are still experimental. Isolate them in dedicated routes.
- Voice UIs benefit from shorter system prompts and shorter responses.
