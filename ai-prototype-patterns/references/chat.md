# Chat

Use this when the user wants a conversational assistant and the interaction is primarily message in, message out.

## Route (`src/app/api/chat/route.ts`)

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

## Page (`src/app/page.tsx`)

```tsx
"use client";

import { useState } from "react";
import { useChat } from "@ai-sdk/react";
import {
  Conversation,
  ConversationContent,
  ConversationScrollButton,
} from "@/components/ai-elements/conversation";
import {
  Message,
  MessageContent,
  MessageResponse,
} from "@/components/ai-elements/message";
import {
  PromptInput,
  PromptInputBody,
  PromptInputFooter,
  type PromptInputMessage,
  PromptInputSubmit,
  PromptInputTextarea,
} from "@/components/ai-elements/prompt-input";

export default function ChatPage() {
  const [input, setInput] = useState("");
  const { messages, sendMessage, status, error, regenerate } = useChat({
    api: "/api/chat",
  });

  const handleSubmit = (message: PromptInputMessage) => {
    if (!message.text.trim()) return;
    sendMessage({ text: message.text });
    setInput("");
  };

  return (
    <main className="flex min-h-screen flex-col items-center">
      <div className="mx-auto flex h-screen w-full max-w-3xl flex-col">
        <Conversation className="flex-1 overflow-hidden">
          <ConversationContent className="space-y-4 p-4">
            {messages.map((message) => (
              <Message key={message.id} from={message.role}>
                <MessageContent>
                  {message.parts.map((part, index) => {
                    if (part.type === "text") {
                      return <MessageResponse key={index}>{part.text}</MessageResponse>;
                    }

                    return null;
                  })}
                </MessageContent>
              </Message>
            ))}
          </ConversationContent>
          <ConversationScrollButton />
        </Conversation>

        {error && (
          <div className="flex items-center justify-between border-t border-red-200 bg-red-50 px-4 py-2 text-sm text-red-700">
            <span>{error.message}</span>
            <button onClick={() => regenerate()} className="underline">
              Retry
            </button>
          </div>
        )}

        <div className="border-t p-4">
          <PromptInput onSubmit={handleSubmit}>
            <PromptInputBody>
              <PromptInputTextarea
                value={input}
                onChange={(event) => setInput(event.currentTarget.value)}
                placeholder="Type a message..."
                disabled={status !== "ready"}
              />
            </PromptInputBody>
            <PromptInputFooter>
              <PromptInputSubmit disabled={!input.trim()} status={status} />
            </PromptInputFooter>
          </PromptInput>
        </div>
      </div>
    </main>
  );
}
```

## Notes

- Start by rendering only `text` parts. Add `reasoning`, `sources`, or tool parts when the feature actually needs them.
- Keep the route simple. Add model selection or web search only when the product requires it.
