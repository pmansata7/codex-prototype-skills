# Prototype Create Script

Purpose: create a fresh prototype repo, optionally initialize Git, and install the selected local Codex skills in one command.

## Script

Run:

```bash
python3 scripts/prototype_create.py <target-path>
```

This is the fastest path for a new prototype repo. It creates the target folder, optionally initializes Git, creates lightweight starter files when missing, and then installs skills into `.codex/skills/`.

## Defaults

- git initialization: on
- git branch: `main`
- install mode: `copy`
- skill preset: `core`
- starter `README.md`: created if missing
- starter `.gitignore`: created if missing

## Examples

Create a new repo with the normal copied-skill workflow:

```bash
python3 scripts/prototype_create.py ../prototypes/idea-one
```

Create a repo that links back to the source skills:

```bash
python3 scripts/prototype_create.py ../prototypes/idea-one --mode link --skills core
```

Create a repo without git:

```bash
python3 scripts/prototype_create.py ../prototypes/idea-one --no-git
```

Create a repo with every available skill:

```bash
python3 scripts/prototype_create.py ../prototypes/idea-one --skills all
```

Preview the plan only:

```bash
python3 scripts/prototype_create.py ../prototypes/idea-one --dry-run
```

## Flags

### `--mode`

Passes through to the skill installer:

- `copy`
- `link`
- `sync`

`copy` remains the default.

### `--skills`

Accepts:

- `core`
- `all`
- comma-separated skill names

### `--no-git`

Skip `git init`.

### `--branch`

Set the initial git branch name when initializing the repo.

### `--force`

Allow bootstrapping into an existing non-empty directory and replace installed skills if needed.

### `--no-readme`

Skip creating a starter `README.md`.

### `--no-gitignore`

Skip creating a starter `.gitignore`.

## What It Creates

By default:

- target repo directory
- `.git/`
- `README.md` if missing
- `.gitignore` if missing
- `.codex/skills/`
- `.codex/skills-manifest.json`

## Relationship To `prototype_init.py`

Use:

- `prototype_create.py` when starting a new prototype repo
- `prototype_init.py` when installing, relinking, or refreshing skills in an existing repo
