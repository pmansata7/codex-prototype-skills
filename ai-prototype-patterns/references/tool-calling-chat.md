# Tool-Calling Chat

Use this when the user needs conversation plus function calls, retrieval, or side effects.

## Route (`src/app/api/chat/route.ts`)

```typescript
import {
  convertToModelMessages,
  stepCountIs,
  streamText,
  tool,
  type UIMessage,
} from "ai";
import { gateway } from "@ai-sdk/gateway";
import { z } from "zod";

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: gateway("google/gemini-3-flash-preview"),
    system: "You are a helpful assistant with access to tools.",
    messages: await convertToModelMessages(messages),
    tools: {
      lookup_order: tool({
        description: "Look up an order by ID",
        inputSchema: z.object({
          orderId: z.string().describe("Customer order ID"),
        }),
        execute: async ({ orderId }) => ({
          orderId,
          status: "processing",
          eta: "2 business days",
        }),
      }),
    },
    stopWhen: stepCountIs(5),
  });

  return result.toUIMessageStreamResponse();
}
```

## Page (`src/app/page.tsx`)

```tsx
"use client";

import { useState } from "react";
import { useChat } from "@ai-sdk/react";
import { type ToolUIPart } from "ai";
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
import {
  Tool,
  ToolContent,
  ToolHeader,
  ToolInput,
  ToolOutput,
} from "@/components/ai-elements/tool";

type LookupOrderPart = ToolUIPart<{
  lookup_order: {
    input: { orderId: string };
    output: { orderId: string; status: string; eta: string };
  };
}>;

export default function ToolChatPage() {
  const [input, setInput] = useState("");
  const { messages, sendMessage, status } = useChat({ api: "/api/chat" });

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

                    if (part.type === "tool-lookup_order") {
                      const toolPart = part as LookupOrderPart;

                      return (
                        <Tool key={index} defaultOpen={toolPart.state !== "output-available"}>
                          <ToolHeader type={toolPart.type} state={toolPart.state} />
                          <ToolContent>
                            <ToolInput input={toolPart.input} />
                            <ToolOutput
                              output={
                                toolPart.output ? (
                                  <MessageResponse>
                                    Order {toolPart.output.orderId} is {toolPart.output.status}. ETA: {toolPart.output.eta}.
                                  </MessageResponse>
                                ) : undefined
                              }
                              errorText={toolPart.errorText}
                            />
                          </ToolContent>
                        </Tool>
                      );
                    }

                    return null;
                  })}
                </MessageContent>
              </Message>
            ))}
          </ConversationContent>
          <ConversationScrollButton />
        </Conversation>

        <div className="border-t p-4">
          <PromptInput onSubmit={handleSubmit}>
            <PromptInputBody>
              <PromptInputTextarea
                value={input}
                onChange={(event) => setInput(event.currentTarget.value)}
                placeholder="Ask about an order..."
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

- Use `stopWhen` for multi-step tool loops.
- For destructive tools, add `needsApproval` to the tool definition and handle approval with `addToolApprovalResponse` in the client.
- Render tool parts by their exact `tool-<name>` type.
