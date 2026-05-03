---
name: refresh-ai-sdk-skills
description: >
  Audit this repo's skills against current official AI SDK, AI Elements, and
  shadcn/ui docs, then recommend or apply updates needed to keep the skills
  current. Use when the user asks to check for SDK drift, refresh the skill repo,
  review upstream changes, or update skills after AI SDK or AI Elements releases.
---

# Refresh AI SDK Skills

Audit the skill repo against current official docs, identify drift, and update the affected skills only after the user approves the proposed edits.

## Required Inputs

Use these local repo files first:

- `docs/skill-watchlist.md`
- `docs/skill-invariants.md`
- `scripts/validate_skills.py`

These files define what to check, what must remain true locally, and what the repo already validates automatically.

## Sources Policy

Use official sources only:

- `ai-sdk.dev`
- `elements.ai-sdk.dev`
- `ui.shadcn.com`
- official GitHub repos and release pages for `vercel/ai` and `vercel/ai-elements`

Do not use blogs, tutorials, Reddit, or third-party summaries for maintenance decisions.

## Workflow

### 1. Validate the repo before browsing

Run:

```bash
python scripts/validate_skills.py
```

If validation already fails, separate:

- local regressions
- likely upstream drift

Do not assume every failure is caused by upstream changes.

### 2. Review the watchlist and invariants

Read the watchlist and invariants before checking the web.

This determines:

- which upstream sources to inspect
- which APIs are high-risk
- which local conventions must stay aligned across all three skills

### 3. Check official upstream changes

Use the sources in `docs/skill-watchlist.md`.

Prioritize:

1. migration guides and versioning pages
2. hook and streaming API references
3. AI Elements install/setup docs
4. GitHub releases for AI SDK and AI Elements

Record concrete changes with dates.

### 4. Map upstream changes to local impact

For each confirmed change, identify:

- impacted skill(s)
- impacted files
- severity
- whether the change is:
  - safe mechanical update
  - medium-risk behavioral update
  - architectural change

### 5. Present a drift report first

Before editing, give the user:

- sources checked
- confirmed changes
- impacted files
- proposed edits
- anything you are inferring from the docs

If there are no confirmed upstream changes that affect the repo, say so explicitly and stop.

### 6. Edit only after approval

After the user approves:

- update affected skill bodies
- update affected references
- update `docs/skill-invariants.md` if the repo's local standard must change
- update `docs/skill-watchlist.md` if new upstream pages or release sources should be tracked
- update validation scripts if a stale-pattern rule must change

### 7. Re-validate

After edits, run:

```bash
python scripts/validate_skills.py
```

Summarize:

- what changed
- what was validated
- what still needs manual judgment

## Change Classes

### Safe mechanical updates

Examples:

- renamed helpers
- updated install commands
- import path changes
- doc URL replacements
- provider/model default updates

These are usually good candidates for a single approval batch.

### Medium-risk updates

Examples:

- changed hook return shapes
- changed tool-part rendering expectations
- changed route helper usage
- migration from one recommended primitive to another without changing the pattern map

Explain these clearly before editing.

### Architectural updates

Examples:

- a pattern should be removed or replaced
- the route shape for a pattern changes fundamentally
- the structured-generation client/server contract changes
- agent or voice APIs move enough to alter the skill boundaries

For architectural updates, update all affected skills and `docs/skill-invariants.md` together.

## Success Criteria

A maintenance pass is complete when:

- confirmed upstream changes are cited from official sources
- proposed edits are clearly scoped before editing
- approved edits are applied consistently across the repo
- `python scripts/validate_skills.py` passes

## References

- `references/drift-review-template.md`
- `references/official-sources.md`
