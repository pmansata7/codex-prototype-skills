# Chat Page Starter

Create `src/app/page.tsx`.

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

export default function Home() {
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
        <header className="border-b p-4">
          <h1 className="text-lg font-semibold">AI Prototype</h1>
        </header>

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

This starter is intentionally minimal. `ai-prototype-patterns` adds tools, reasoning, structured renderers, or agent-specific UI later.
