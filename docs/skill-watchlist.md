# Skill Watchlist

Purpose: define the upstream sources and API surfaces that can invalidate the skills in this repo.

## Review Cadence

Run a drift review:

- before copying these skills into another repo
- weekly if you are actively using them
- after any AI SDK or AI Elements major release
- after any AI SDK migration guide update
- whenever a skill fails validation because a reference or API pattern changed

## Official Sources To Check

### AI SDK

- Main docs: https://ai-sdk.dev/docs
- API reference root: https://ai-sdk.dev/docs/reference/ai-sdk-core
- AI SDK UI `useChat`: https://ai-sdk.dev/docs/reference/ai-sdk-ui/use-chat
- AI SDK UI `useObject`: https://ai-sdk.dev/docs/reference/ai-sdk-ui/use-object
- Versioning / migration guidance: https://ai-sdk.dev/docs/migration-guides/versioning
- 5.x to 6.0 migration: https://ai-sdk.dev/docs/migration-guides/migrate-ai-sdk-5-to-6
- GitHub repo: https://github.com/vercel/ai
- GitHub releases: https://github.com/vercel/ai/releases

### AI Elements

- Main docs: https://elements.ai-sdk.dev/docs
- Component docs: https://elements.ai-sdk.dev/components
- Homepage / examples: https://elements.ai-sdk.dev
- GitHub repo: https://github.com/vercel/ai-elements
- GitHub releases: https://github.com/vercel/ai-elements/releases

### shadcn/ui

- Installation docs: https://ui.shadcn.com/docs/installation
- CLI docs: https://ui.shadcn.com/docs/cli

## High-Risk APIs And Concepts

These are the most likely to change and should be checked first:

- `useChat`
- `experimental_useObject`
- `streamText`
- `Output.object()`
- `convertToModelMessages`
- `toUIMessageStreamResponse()`
- tool UI parts and tool approval flows
- `ToolLoopAgent`
- `createAgentUIStreamResponse`
- `experimental_transcribe`
- `experimental_generateSpeech`
- AI Elements CLI installation commands
- PromptInput compound component API

## What To Record During A Review

For each review, capture:

- review date
- sources checked
- confirmed upstream changes
- impacted skill files
- required edits
- whether the change is safe, medium-risk, or architectural

## Safe-To-Apply Changes

These usually can be made in one maintenance pass after approval:

- renamed helper functions
- route response helper changes
- client hook signature changes
- install command changes
- provider/model default updates
- doc URL changes
- component import name changes

## High-Risk Changes

These require explicit review before editing:

- pattern model changes such as replacing `experimental_useObject`
- route architecture changes
- tool approval model changes
- agent API redesigns
- voice API changes on experimental surfaces
- changes that require a new pattern or invalidate an existing one
