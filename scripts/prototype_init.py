#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT
DEFAULT_PRESET = "core"
DEFAULT_MODE = "copy"
MANIFEST_RELATIVE_PATH = Path(".codex/skills-manifest.json")
INSTALL_ROOT_RELATIVE_PATH = Path(".codex/skills")
CORE_SKILLS = [
    "spec-to-prototype",
    "scaffold-ai-prototype",
    "ai-prototype-patterns",
]


@dataclass(frozen=True)
class InstallPlan:
    target_repo: Path
    install_root: Path
    manifest_path: Path
    skills: list[str]
    mode: str
    preset: str | None


def discover_all_skills() -> list[str]:
    skills = sorted(
        path.name for path in SKILLS_DIR.iterdir() if path.is_dir() and (path / "SKILL.md").exists()
    )
    return skills


ALL_SKILLS = discover_all_skills()
PRESETS = {
    "core": CORE_SKILLS,
    "all": ALL_SKILLS,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Codex skills into a prototype repo using copy, link, or sync mode."
    )
    parser.add_argument("target", help="Target prototype repo path")
    parser.add_argument(
        "--mode",
        choices=["copy", "link", "sync"],
        default=DEFAULT_MODE,
        help="Install mode. Defaults to copy.",
    )
    parser.add_argument(
        "--skills",
        default=DEFAULT_PRESET,
        help="Skill preset (core, all) or comma-separated skill names. Defaults to core.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing installed skill folders if needed.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned actions without modifying the target repo.",
    )
    return parser.parse_args()


def resolve_skill_selection(raw_value: str) -> tuple[list[str], str | None]:
    normalized = raw_value.strip()
    if not normalized:
        raise ValueError("--skills cannot be empty")

    if normalized in PRESETS:
        return list(PRESETS[normalized]), normalized

    selected = []
    for item in normalized.split(","):
        name = item.strip()
        if not name:
            continue
        selected.append(name)

    if not selected:
        raise ValueError("no skills were selected")

    unknown = [name for name in selected if name not in ALL_SKILLS]
    if unknown:
        available = ", ".join(ALL_SKILLS)
        raise ValueError(f"unknown skill(s): {', '.join(unknown)}. Available skills: {available}")

    deduped = sorted(dict.fromkeys(selected))
    return deduped, None


def build_plan(target_arg: str, mode: str, raw_skills: str) -> InstallPlan:
    target_repo = Path(target_arg).expanduser().resolve()
    install_root = target_repo / INSTALL_ROOT_RELATIVE_PATH
    manifest_path = target_repo / MANIFEST_RELATIVE_PATH
    skills, preset = resolve_skill_selection(raw_skills)
    return InstallPlan(
        target_repo=target_repo,
        install_root=install_root,
        manifest_path=manifest_path,
        skills=skills,
        mode=mode,
        preset=preset,
    )


def remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    shutil.rmtree(path)


def install_skill(source: Path, destination: Path, mode: str, force: bool) -> str:
    if destination.exists() or destination.is_symlink():
        if not force and mode != "sync":
            raise FileExistsError(f"{destination} already exists. Re-run with --force to replace it.")
        remove_existing(destination)

    if mode == "link":
        destination.symlink_to(source, target_is_directory=True)
        return "linked"

    shutil.copytree(source, destination, symlinks=True)
    return "copied"


def load_existing_manifest(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_manifest(plan: InstallPlan, existing_manifest: dict | None) -> None:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    manifest = {
        "source_repo": str(ROOT),
        "target_repo": str(plan.target_repo),
        "install_root": str(plan.install_root),
        "mode": plan.mode,
        "skills": plan.skills,
        "preset": plan.preset,
        "updated_at": now,
    }
    if existing_manifest and "created_at" in existing_manifest:
        manifest["created_at"] = existing_manifest["created_at"]
    else:
        manifest["created_at"] = now
    plan.manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def ensure_target_dirs(plan: InstallPlan) -> None:
    plan.target_repo.mkdir(parents=True, exist_ok=True)
    plan.install_root.mkdir(parents=True, exist_ok=True)


def print_plan(plan: InstallPlan) -> None:
    print(f"target_repo: {plan.target_repo}")
    print(f"install_root: {plan.install_root}")
    print(f"mode: {plan.mode}")
    if plan.preset:
        print(f"preset: {plan.preset}")
    print(f"skills: {', '.join(plan.skills)}")


def main() -> int:
    args = parse_args()

    try:
        plan = build_plan(args.target, args.mode, args.skills)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print_plan(plan)
        return 0

    existing_manifest = load_existing_manifest(plan.manifest_path)
    ensure_target_dirs(plan)

    actions: list[str] = []

    try:
        for skill_name in plan.skills:
            source = ROOT / skill_name
            destination = plan.install_root / skill_name
            action = install_skill(source, destination, plan.mode, args.force)
            actions.append(f"{action}: {skill_name}")
    except FileExistsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    write_manifest(plan, existing_manifest)

    print("Installed skills successfully.")
    print_plan(plan)
    for action in actions:
        print(f"- {action}")
    print(f"manifest: {plan.manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
