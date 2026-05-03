#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIRS = sorted(path for path in ROOT.iterdir() if path.is_dir() and (path / "SKILL.md").exists())
DOC_FILES = [
    ROOT / "docs" / "skill-watchlist.md",
    ROOT / "docs" / "skill-invariants.md",
]

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
REFERENCE_RE = re.compile(r"references/[A-Za-z0-9._/-]+")

STALE_PATTERNS = {
    "handleInputChange": "use local state plus sendMessage or PromptInput callbacks",
    "streamObject(": "use streamText with Output.object() for structured-generation",
    "generateObject(": "use generateText with Output.object()",
    "toDataStreamResponse()": "use toUIMessageStreamResponse() for chat-like routes",
    "Ideation (Claude chat on phone)": "remove Claude-specific workflow wording",
}


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")

    data: dict[str, str] = {}
    current_key: str | None = None
    current_lines: list[str] = []

    for raw_line in match.group(1).splitlines():
        if not raw_line.strip():
            continue
        if re.match(r"^[A-Za-z0-9_-]+:\s*", raw_line):
            if current_key is not None:
                data[current_key] = "\n".join(current_lines).strip()
            key, value = raw_line.split(":", 1)
            current_key = key.strip()
            current_lines = [value.strip()]
        elif current_key is not None:
            current_lines.append(raw_line.rstrip())
        else:
            raise ValueError("invalid frontmatter structure")

    if current_key is not None:
        data[current_key] = "\n".join(current_lines).strip()

    return data


def is_ascii(text: str) -> bool:
    return all(ord(ch) < 128 for ch in text)


errors: list[str] = []

for doc_file in DOC_FILES:
    if not doc_file.exists():
        errors.append(f"{doc_file}: missing required repo maintenance document")
        continue
    doc_text = doc_file.read_text(encoding="utf-8")
    if not is_ascii(doc_text):
        errors.append(f"{doc_file}: contains non-ASCII characters")

watchlist_file = ROOT / "docs" / "skill-watchlist.md"
if watchlist_file.exists():
    watchlist_text = watchlist_file.read_text(encoding="utf-8")
    for required_url in [
        "https://ai-sdk.dev/docs",
        "https://elements.ai-sdk.dev/docs",
        "https://ui.shadcn.com/docs/installation",
    ]:
        if required_url not in watchlist_text:
            errors.append(f"{watchlist_file}: missing tracked source {required_url}")

invariants_file = ROOT / "docs" / "skill-invariants.md"
if invariants_file.exists():
    invariants_text = invariants_file.read_text(encoding="utf-8")
    for required_pattern in [
        "`chat`",
        "`tool-calling-chat`",
        "`generative-ui`",
        "`structured-generation`",
        "`server-workflow`",
        "`agent-loop`",
        "`voice`",
    ]:
        if required_pattern not in invariants_text:
            errors.append(f"{invariants_file}: missing pattern invariant {required_pattern}")

for skill_dir in SKILL_DIRS:
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")

    if not is_ascii(text):
        errors.append(f"{skill_file}: contains non-ASCII characters")

    try:
        frontmatter = parse_frontmatter(text)
    except ValueError as exc:
        errors.append(f"{skill_file}: {exc}")
        continue

    if set(frontmatter.keys()) != {"name", "description"}:
        errors.append(
            f"{skill_file}: frontmatter keys must be exactly name and description, found {sorted(frontmatter.keys())}"
        )

    if frontmatter.get("name") != skill_dir.name:
        errors.append(
            f"{skill_file}: frontmatter name {frontmatter.get('name')!r} does not match folder {skill_dir.name!r}"
        )

    if not frontmatter.get("description"):
        errors.append(f"{skill_file}: missing description")

    for reference in sorted(set(REFERENCE_RE.findall(text))):
        if not (skill_dir / reference).exists():
            errors.append(f"{skill_file}: missing referenced file {reference}")

    for stale, guidance in STALE_PATTERNS.items():
        if stale in text:
            errors.append(f"{skill_file}: stale pattern {stale!r} found; {guidance}")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        errors.append(f"{skill_dir}: missing agents/openai.yaml")
    else:
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        if not is_ascii(yaml_text):
            errors.append(f"{openai_yaml}: contains non-ASCII characters")
        for required in [
            'display_name:',
            'short_description:',
            'default_prompt:',
            'allow_implicit_invocation:',
        ]:
            if required not in yaml_text:
                errors.append(f"{openai_yaml}: missing {required}")
        if f"${skill_dir.name}" not in yaml_text:
            errors.append(f"{openai_yaml}: default_prompt must mention ${skill_dir.name}")

    for path in skill_dir.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        if not is_ascii(content):
            errors.append(f"{path}: contains non-ASCII characters")
        for stale, guidance in STALE_PATTERNS.items():
            if stale in content:
                errors.append(f"{path}: stale pattern {stale!r} found; {guidance}")

if errors:
    print("Skill validation failed:\n")
    for item in errors:
        print(f"- {item}")
    sys.exit(1)

print(f"Validated {len(SKILL_DIRS)} skills successfully.")

