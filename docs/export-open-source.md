# Export Open Source Repo

Purpose: create a clean publishable copy of this repo in a separate destination.

## Script

Run:

```bash
python3 scripts/export_open_source_repo.py . ../codex-prototype-skills-public --repo-name codex-prototype-skills-public
```

The export script copies the public repo surface into a new directory and skips local artifacts such as:

- `.git`
- `.DS_Store`
- `__pycache__/`
- common Python cache directories
- local virtual environments
- build output folders

When `--repo-name` is provided, exact text matches of the source repo folder name are rewritten in copied text files.

## When To Use It

Use this script when:

- preparing a clean public release copy
- testing what the publishable repo surface looks like
- renaming the public repo while keeping this working repo unchanged

## Example Verification

```bash
python3 scripts/export_open_source_repo.py . /tmp/codex-prototype-skills-public-test --repo-name codex-prototype-skills-public --force
cd /tmp/codex-prototype-skills-public-test
python3 scripts/validate_skills.py
```
