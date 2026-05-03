#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INCLUDE_FILES = [
    "README.md",
    "LICENSE",
    ".gitattributes",
    ".gitignore",
]
DEFAULT_INCLUDE_DIRS = [
    "docs",
    "scripts",
]
SKIP_NAMES = {
    ".DS_Store",
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "dist",
    "build",
}
TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".yaml",
    ".yml",
    ".txt",
    ".json",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".css",
}


def discover_skill_dirs(source_root: Path) -> list[str]:
    return sorted(
        path.name for path in source_root.iterdir() if path.is_dir() and (path / "SKILL.md").exists()
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy the publishable parts of this skill repo into a new destination."
    )
    parser.add_argument("source", help="Source repo path")
    parser.add_argument("destination", help="Destination repo path")
    parser.add_argument(
        "--repo-name",
        help="Public repo name to rewrite source-repo references in copied text files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing destination directory if it already exists.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the copy plan without writing files.",
    )
    return parser.parse_args()


def build_include_list(source_root: Path) -> list[Path]:
    includes: list[Path] = []

    for name in DEFAULT_INCLUDE_FILES:
        candidate = source_root / name
        if candidate.exists():
            includes.append(candidate)

    for name in DEFAULT_INCLUDE_DIRS:
        candidate = source_root / name
        if candidate.exists():
            includes.append(candidate)

    for name in discover_skill_dirs(source_root):
        includes.append(source_root / name)

    return includes


def ensure_destination(destination: Path, force: bool) -> None:
    if destination.exists() and not destination.is_dir():
        raise ValueError(f"{destination} exists and is not a directory")

    if destination.exists():
        visible_entries = [path for path in destination.iterdir() if path.name not in {".DS_Store"}]
        if visible_entries and not force:
            raise ValueError(f"{destination} is not empty. Re-run with --force to replace it.")
        if visible_entries and force:
            shutil.rmtree(destination)

    destination.mkdir(parents=True, exist_ok=True)


def should_skip(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return any(part in SKIP_NAMES for part in relative.parts)


def copy_path(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns(*SKIP_NAMES),
            dirs_exist_ok=False,
            symlinks=True,
        )
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination, follow_symlinks=False)


def is_probably_text_file(path: Path) -> bool:
    return path.suffix in TEXT_SUFFIXES or path.name in {".gitignore", ".gitattributes"}


def rewrite_repo_references(destination: Path, source_repo_name: str, target_repo_name: str) -> list[str]:
    rewritten: list[str] = []

    for path in sorted(destination.rglob("*")):
        if not path.is_file() or not is_probably_text_file(path):
            continue

        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        updated = original.replace(source_repo_name, target_repo_name)
        if updated == original:
            continue

        path.write_text(updated, encoding="utf-8")
        rewritten.append(str(path.relative_to(destination)))

    return rewritten


def print_plan(
    source_root: Path,
    destination: Path,
    includes: list[Path],
    target_repo_name: str | None,
) -> None:
    print(f"source: {source_root}")
    print(f"destination: {destination}")
    if target_repo_name:
        print(f"repo_name_rewrite: {source_root.name} -> {target_repo_name}")
    print("includes:")
    for path in includes:
        print(f"- {path.relative_to(source_root)}")


def main() -> int:
    args = parse_args()
    source_root = Path(args.source).expanduser().resolve()
    destination = Path(args.destination).expanduser().resolve()

    if not source_root.exists() or not source_root.is_dir():
        print(f"error: source directory does not exist: {source_root}", file=sys.stderr)
        return 2

    if destination == source_root or source_root in destination.parents:
        print(
            f"error: destination must be outside the source repo: {destination}",
            file=sys.stderr,
        )
        return 2

    includes = [path for path in build_include_list(source_root) if not should_skip(path, source_root)]

    if args.dry_run:
        print_plan(source_root, destination, includes, args.repo_name)
        return 0

    try:
        ensure_destination(destination, args.force)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    copied: list[str] = []
    for source_path in includes:
        relative = source_path.relative_to(source_root)
        target_path = destination / relative
        copy_path(source_path, target_path)
        copied.append(str(relative))

    rewritten: list[str] = []
    if args.repo_name:
        rewritten = rewrite_repo_references(destination, source_root.name, args.repo_name)

    print("Copied open-source repo contents successfully.")
    print(f"source: {source_root}")
    print(f"destination: {destination}")
    if args.repo_name:
        print(f"repo_name_rewrite: {source_root.name} -> {args.repo_name}")
    print("copied:")
    for item in copied:
        print(f"- {item}")
    if rewritten:
        print("rewritten:")
        for item in rewritten:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
