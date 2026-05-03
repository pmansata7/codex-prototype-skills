# codex-prototype-skills

Version-controlled Codex skills for taking AI product ideas from spec to scaffold to implementation, plus a maintenance skill for keeping the repo aligned with fast-moving AI SDK and AI Elements changes.

## Purpose

This repo is the source of truth for a small, opinionated skill chain:

1. `spec-to-prototype`
   Turn a rough product idea into an execution-ready `SPEC.md` with ordered work packages, dependency graph, and binary success criteria.
2. `scaffold-ai-prototype`
   Scaffold a Next.js + AI SDK starter that matches the primary pattern in the spec.
3. `ai-prototype-patterns`
   Implement or extend the feature using the right AI SDK pattern.
4. `refresh-ai-sdk-skills`
   Audit this repo against official AI SDK, AI Elements, and shadcn/ui docs and recommend or apply maintenance updates after approval.

This repo is for centralizing, reviewing, and versioning the skills. Install, link, or sync them into target repos with `scripts/prototype_init.py` or your normal `npx skills` workflow.

## Repo Layout

- `spec-to-prototype/`
- `scaffold-ai-prototype/`
- `ai-prototype-patterns/`
- `refresh-ai-sdk-skills/`
- `docs/`
  - `skill-watchlist.md`: upstream sources and high-risk APIs to monitor
  - `skill-invariants.md`: local conventions that all skills must preserve
  - `rapid-prototyping-setup.md`: recommended repo and skill distribution model for fast prototype work
  - `prototype-create.md`: usage guide for one-command repo bootstrap plus skill install
  - `prototype-init.md`: usage guide for the one-command local skill installer
- `scripts/`
  - `validate_skills.py`: repo-local skill validation
  - `prototype_create.py`: create a prototype repo, optionally initialize git, and install selected skills
  - `prototype_init.py`: install selected skills into a target repo using copy, link, or sync mode

## Current Defaults

- Default provider path: AI Gateway
- Default model family: Gemini 3 Flash Preview
- Pattern vocabulary shared across the repo:
  - `chat`
  - `tool-calling-chat`
  - `generative-ui`
  - `structured-generation`
  - `server-workflow`
  - `agent-loop`
  - `voice`

## Recommended Workflow

### New prototype

1. Use `spec-to-prototype` to generate `SPEC.md`.
2. Use `scaffold-ai-prototype` to scaffold the starter that matches the spec's primary pattern.
3. Use `ai-prototype-patterns` to implement the real feature set.

For repo setup and skill installation:

- read [docs/rapid-prototyping-setup.md](docs/rapid-prototyping-setup.md)
- use [docs/prototype-create.md](docs/prototype-create.md)
- use [docs/prototype-init.md](docs/prototype-init.md)

### Maintenance

1. Use `refresh-ai-sdk-skills` when upstream SDK or component APIs may have changed.
2. Review the proposed drift report.
3. Approve edits.
4. Re-run validation.

## Validation

Run:

```bash
python scripts/validate_skills.py
```

The validator checks:

- required skill frontmatter
- `agents/openai.yaml` presence
- missing reference files
- stale API patterns the repo no longer allows
- required maintenance docs in `docs/`
- shared pattern invariants
- ASCII-only repo docs and skill files

## Prototype Setup

For the default copied-skill workflow:

```bash
python3 scripts/prototype_create.py ../prototypes/my-idea
```

Common variants:

```bash
python3 scripts/prototype_create.py ../prototypes/my-idea --mode link --skills core
python3 scripts/prototype_create.py ../prototypes/my-idea --skills all
python3 scripts/prototype_init.py ../prototypes/my-idea --mode link --skills core
python3 scripts/prototype_init.py ../prototypes/my-idea --mode sync --skills core
python3 scripts/prototype_init.py ../prototypes/my-idea --skills all
```

Use `prototype_create.py` for new repos and `prototype_init.py` for existing repos. Use `core` for the main prototyping chain and `all` when you want every skill in this repo installed into the target project.

## Export A Public Copy

To create a clean copy of this repo for open-sourcing in a separate destination:

```bash
python3 scripts/export_open_source_repo.py . ../codex-prototype-skills --repo-name codex-prototype-skills
```

The export script copies the publishable top-level files plus all skill folders, while skipping local repo artifacts such as `.git`, `.DS_Store`, and `__pycache__/`. When `--repo-name` is provided, it also rewrites exact source-repo name references in copied UTF-8 text files.

## Maintenance Policy

This repo assumes AI SDK and AI Elements can drift quickly.

Use these files to keep the skill set current:

- `docs/skill-watchlist.md`
- `docs/skill-invariants.md`
- `refresh-ai-sdk-skills/`

Run a maintenance review:

- before copying these skills into another repo
- weekly during active use
- after major AI SDK or AI Elements releases
- after migration-guide updates

## Notes

- The skills are intentionally opinionated and optimized for Codex use, not generic prompt libraries.
- The references under each skill are part of the implementation contract and should be updated together with the skill body.
- If upstream SDK changes force a pattern change, update all affected skills and `docs/skill-invariants.md` in the same pass.
