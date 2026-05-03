#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import prototype_init as installer

DEFAULT_GIT_BRANCH = "main"
DEFAULT_README_TEMPLATE = """# {name}

Prototype repo bootstrapped from `codex-prototype-skills`.
"""

DEFAULT_GITIGNORE = """# Local env
.env
.env.local

# Node
node_modules/

# Next.js
.next/
out/

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# OS
.DS_Store
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new prototype repo folder, optionally initialize git, and install Codex skills."
    )
    parser.add_argument("target", help="Target prototype repo path")
    parser.add_argument(
        "--mode",
        choices=["copy", "link", "sync"],
        default=installer.DEFAULT_MODE,
        help="Skill install mode. Defaults to copy.",
    )
    parser.add_argument(
        "--skills",
        default=installer.DEFAULT_PRESET,
        help="Skill preset (core, all) or comma-separated skill names. Defaults to core.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow bootstrapping into an existing repo directory and replace installed skills if needed.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned actions without modifying the target repo.",
    )
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Skip git initialization.",
    )
    parser.add_argument(
        "--branch",
        default=DEFAULT_GIT_BRANCH,
        help="Git default branch name when initializing a repo. Defaults to main.",
    )
    parser.add_argument(
        "--no-readme",
        action="store_true",
        help="Skip creating a starter README.md when one does not exist.",
    )
    parser.add_argument(
        "--no-gitignore",
        action="store_true",
        help="Skip creating a starter .gitignore when one does not exist.",
    )
    return parser.parse_args()


def ensure_target_directory(target_repo: Path, force: bool) -> None:
    if target_repo.exists() and not target_repo.is_dir():
        raise ValueError(f"{target_repo} exists and is not a directory")

    if target_repo.exists():
        visible_entries = [path for path in target_repo.iterdir() if path.name not in {".DS_Store"}]
        if visible_entries and not force:
            raise ValueError(f"{target_repo} is not empty. Re-run with --force to continue.")
    else:
        target_repo.mkdir(parents=True, exist_ok=True)


def write_file_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def init_git_repo(target_repo: Path, branch: str) -> None:
    git_dir = target_repo / ".git"
    if git_dir.exists():
        return
    subprocess.run(
        ["git", "init", "-b", branch],
        cwd=target_repo,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def main() -> int:
    args = parse_args()

    try:
        plan = installer.build_plan(args.target, args.mode, args.skills)
        target_repo = plan.target_repo
        ensure_target_directory(target_repo, args.force)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"target_repo: {target_repo}")
        print(f"git_init: {'no' if args.no_git else 'yes'}")
        if not args.no_git:
            print(f"git_branch: {args.branch}")
        print(f"create_readme: {'no' if args.no_readme else 'if-missing'}")
        print(f"create_gitignore: {'no' if args.no_gitignore else 'if-missing'}")
        installer.print_plan(plan)
        return 0

    created_items: list[str] = []

    if not args.no_readme:
        if write_file_if_missing(
            target_repo / "README.md",
            DEFAULT_README_TEMPLATE.format(name=target_repo.name),
        ):
            created_items.append("created: README.md")

    if not args.no_gitignore:
        if write_file_if_missing(target_repo / ".gitignore", DEFAULT_GITIGNORE):
            created_items.append("created: .gitignore")

    if not args.no_git:
        try:
            init_git_repo(target_repo, args.branch)
            created_items.append(f"initialized git: branch {args.branch}")
        except FileNotFoundError:
            print("error: git is not available on PATH", file=sys.stderr)
            return 1
        except subprocess.CalledProcessError as exc:
            print(exc.stderr.strip() or "error: git init failed", file=sys.stderr)
            return 1

    init_argv = [
        str(plan.target_repo),
        "--mode",
        args.mode,
        "--skills",
        args.skills,
    ]
    if args.force:
        init_argv.append("--force")

    init_args = installer.parse_args.__globals__["argparse"].Namespace(
        target=str(plan.target_repo),
        mode=args.mode,
        skills=args.skills,
        force=args.force,
        dry_run=False,
    )

    try:
        init_plan = installer.build_plan(init_args.target, init_args.mode, init_args.skills)
        existing_manifest = installer.load_existing_manifest(init_plan.manifest_path)
        installer.ensure_target_dirs(init_plan)

        actions: list[str] = []
        for skill_name in init_plan.skills:
            source = installer.ROOT / skill_name
            destination = init_plan.install_root / skill_name
            action = installer.install_skill(source, destination, init_plan.mode, init_args.force)
            actions.append(f"{action}: {skill_name}")
        installer.write_manifest(init_plan, existing_manifest)
    except FileExistsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print("Created prototype repo successfully.")
    print(f"target_repo: {target_repo}")
    for item in created_items:
        print(f"- {item}")
    installer.print_plan(init_plan)
    for action in actions:
        print(f"- {action}")
    print(f"manifest: {init_plan.manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
