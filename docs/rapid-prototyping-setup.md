# Rapid Prototyping Setup

Purpose: define a fast local workflow for using this repo's skills across many prototype ideas without losing a single source of truth.

## Recommendation

Use this repo as the canonical skill source, keep prototype projects separate by default, and expose only the needed skills into each prototype repo.

Recommended default:

1. Keep `codex-prototype-skills` as the source of truth.
2. Create one repo per serious prototype idea.
3. In each prototype repo, add a project-local `.codex/skills/` view that points to only the needed skills from this repo.

This keeps setup fast, avoids maintaining multiple divergent copies, and still lets each prototype have explicit local skill availability.

## Why This Fits The Current Repo

This repo is already optimized as a maintained source:

- skills are versioned independently at the repo root
- `docs/skill-invariants.md` defines cross-skill contracts
- `docs/skill-watchlist.md` defines maintenance cadence
- `scripts/validate_skills.py` assumes this repo layout

Moving the maintained source into this repo's own `.codex/` folder would make the repo less clear and would fight the current validator and docs structure.

## Option Review

### Option A: one new repo per idea

Best default when:

- you have several ideas in flight
- prototypes may need different patterns such as `voice` or `agent-loop`
- you want to throw projects away freely
- you want each `SPEC.md` and scaffold to stay focused

Benefits:

- least context bleed between ideas
- easier to delete, archive, or share
- clean spec-to-scaffold-to-build flow per prototype
- safer when different ideas need different dependencies

Tradeoff:

- slightly more setup per idea unless repo creation is scripted

### Option B: one shared playground repo for all prototypes

Useful only for very short-lived spikes.

Benefits:

- fastest possible start for a tiny experiment
- no repeated repo creation

Tradeoffs:

- ideas bleed into each other quickly
- `SPEC.md`, routes, env vars, and dependencies become messy
- different patterns collide over time
- harder to know which files belong to which experiment

This is not the best default if you already have multiple serious ideas.

## Skill Distribution Models

### Model 1: global-only skills

Keep the skills installed once globally and rely on that install everywhere.

Best for:

- absolute fastest start
- solo local use
- cases where reproducibility matters less than speed

Risk:

- project behavior depends on hidden machine state
- it is harder to know which skill version a given prototype used

### Model 2: copied per-repo skills

Copy the relevant skills into each prototype repo.

Best for:

- reproducibility
- freezing a prototype against later skill edits
- sharing the repo with someone else

Risk:

- skills drift unless you remember to refresh them

### Model 3: project-local linked view of central skills

Expose selected skills into each prototype repo's `.codex/skills/` from this repo, ideally via symlink or a tiny sync step.

Best for:

- one maintained version of the skills
- repo-local visibility of what a prototype can use
- fast iteration while the skills are still evolving

Risk:

- changes in `codex-prototype-skills` affect active prototypes immediately

This is the recommended default while the skills are still being refined.

## Practical Default

Use two lanes:

- `scratch` lane: one disposable playground repo for 10-30 minute experiments
- `prototype` lane: one repo per real idea once it survives the first spike

Workflow:

1. Quick spike in a playground only if you are testing a narrow interaction.
2. If the idea still looks promising, create a fresh repo.
3. Generate `SPEC.md` with `spec-to-prototype`.
4. Expose only the needed skills for that repo.
5. Scaffold and build.

## What To Do For This Repo

Do not move the maintained source into a root-level `.codex/` folder here.

Instead:

- keep the current root skill folders as the source of truth
- keep using `scripts/validate_skills.py` here
- add a lightweight install or sync workflow for target repos

## Suggested Local Setup

### Canonical repo

- `codex-prototype-skills/` remains the home for authoring, validation, and maintenance
- use `scripts/prototype_create.py` for one-command new repo setup
- use `scripts/prototype_init.py` to push or refresh selected skills in existing repos

### Prototype repos

For each new idea:

1. create a new repo
2. add `.codex/skills/`
3. link or copy only the needed skills:
   - `spec-to-prototype`
   - `scaffold-ai-prototype`
   - `ai-prototype-patterns`
   - `refresh-ai-sdk-skills` only when maintaining the skill source repo

For one-command setup, see `docs/prototype-create.md` and `docs/prototype-init.md`.

### Pattern-based inclusion

Use the smallest set that matches the prototype:

- all new ideas: `spec-to-prototype`, `scaffold-ai-prototype`, `ai-prototype-patterns`
- maintenance on this repo: add `refresh-ai-sdk-skills`
- do not copy every skill into every repo just because it exists

## Decision Summary

1. Keep this repo as the single maintained source of truth.
2. Do not convert this repo itself into the canonical `.codex/` store.
3. Prefer a new repo per real prototype idea.
4. Use project-local access to a selected subset of skills from this repo.
5. Keep one disposable playground only for very short spikes, not as the default home for all prototypes.
