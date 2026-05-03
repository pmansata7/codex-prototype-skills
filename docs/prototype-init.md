# Prototype Init Script

Purpose: provide a one-command way to install this repo's Codex skills into a target prototype repo.

## Script

Run:

```bash
python3 scripts/prototype_init.py <target-path>
```

The script installs selected skills into:

```text
<target-path>/.codex/skills/
```

It also writes a manifest to:

```text
<target-path>/.codex/skills-manifest.json
```

If you are starting a brand new idea repo, use `scripts/prototype_create.py` instead. See `docs/prototype-create.md`.

## Defaults

- default mode: `copy`
- default skill preset: `core`

This matches the recommended rapid-prototyping flow for freezing a prototype repo against later edits to the source skill repo.

## Skill Sets

### `core`

Installs the current prototyping chain:

- `spec-to-prototype`
- `scaffold-ai-prototype`
- `ai-prototype-patterns`

### `all`

Installs every skill folder in this repo that contains `SKILL.md`.

Use this when you explicitly want the full local skill surface, including maintenance skills.

## Modes

### `copy`

Copies selected skills into the target repo.

Use when:

- you want a stable per-project snapshot
- you may share or archive the prototype repo
- you do not want later edits in the source skill repo to affect the prototype automatically

Example:

```bash
python3 scripts/prototype_init.py ../prototypes/idea-one
python3 scripts/prototype_init.py ../prototypes/idea-one --mode copy --skills core
```

### `link`

Creates symlinks from the target repo into this repo's skill folders.

Use when:

- you want the fastest local iteration
- you are actively editing the skills in this repo
- you want prototypes to reflect source skill updates immediately

Example:

```bash
python3 scripts/prototype_init.py ../prototypes/idea-one --mode link --skills core
```

### `sync`

Refreshes installed skills by replacing the selected target skill folders with fresh copies from this repo.

Use when:

- you already copied skills into a prototype repo
- the source skill repo changed
- you want to update the prototype's local snapshot deliberately

`sync` always writes normal copied folders, not symlinks.

Example:

```bash
python3 scripts/prototype_init.py ../prototypes/idea-one --mode sync --skills core
```

## Explicit Skill Lists

Instead of a preset, pass a comma-separated list:

```bash
python3 scripts/prototype_init.py ../prototypes/idea-two \
  --skills spec-to-prototype,scaffold-ai-prototype
```

This is useful when future PM, UX, or design skills should be included selectively without changing the current presets.

## Helpful Flags

### `--force`

Overwrite existing installed skill folders for `copy` or `link`.

Example:

```bash
python3 scripts/prototype_init.py ../prototypes/idea-one --mode copy --skills core --force
```

### `--dry-run`

Print the plan without writing anything.

Example:

```bash
python3 scripts/prototype_init.py ../prototypes/idea-one --mode link --dry-run
```

## Suggested Usage

For most real prototypes:

```bash
python3 scripts/prototype_init.py ../prototypes/my-idea
```

Then inside the target repo:

1. use `spec-to-prototype`
2. scaffold with `scaffold-ai-prototype`
3. build with `ai-prototype-patterns`

## Manifest

Each run writes `.codex/skills-manifest.json` with:

- source repo path
- target repo path
- install root
- mode
- selected skills
- selected preset if one was used
- created and updated timestamps

This makes it easier to see how a prototype repo got its local skills and when it was last refreshed.
