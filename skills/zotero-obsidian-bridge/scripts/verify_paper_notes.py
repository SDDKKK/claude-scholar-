#!/usr/bin/env python3
"""Verify Obsidian paper-note schema and Zotero-key coverage."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = (
    "## Claim",
    "## Method",
    "## Evidence",
    "## Limitation",
    "## Direct relevance to repo",
    "## Relation to other papers",
)

ZOTERO_KEY_RE = re.compile(r'^zotero_key:\s*"([A-Z0-9]+)"', re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify paper-note schema and optional Zotero-key coverage."
    )
    parser.add_argument(
        "--papers-dir",
        required=True,
        help="Directory containing canonical paper notes.",
    )
    parser.add_argument(
        "--expected-zotero-keys",
        default="",
        help="Comma-separated Zotero keys expected to be covered.",
    )
    parser.add_argument(
        "--strict-missing-zotero-key",
        action="store_true",
        help="Treat notes without zotero_key as errors. Default behavior skips them.",
    )
    return parser.parse_args()


def load_expected_keys(raw_keys: str) -> list[str]:
    if not raw_keys.strip():
        return []
    return [key.strip() for key in raw_keys.split(",") if key.strip()]


def collect_note_status(
    papers_dir: Path,
    strict_missing_zotero_key: bool,
) -> tuple[dict[str, str], list[str], list[str]]:
    key_to_file: dict[str, str] = {}
    issues: list[str] = []
    skipped_without_key: list[str] = []

    for path in sorted(papers_dir.glob("*.md")):
        text = path.read_text()
        match = ZOTERO_KEY_RE.search(text)
        if not match:
            skipped_without_key.append(path.name)
            if strict_missing_zotero_key:
                issues.append(f"{path.name}: missing zotero_key")
            continue

        zotero_key = match.group(1)
        if zotero_key in key_to_file:
            issues.append(
                f"{path.name}: duplicate zotero_key {zotero_key} also used by {key_to_file[zotero_key]}"
            )
        key_to_file[zotero_key] = path.name

        missing_headings = [heading for heading in REQUIRED_HEADINGS if heading not in text]
        if missing_headings:
            issues.append(
                f"{path.name}: missing headings -> {', '.join(missing_headings)}"
            )

    return key_to_file, issues, skipped_without_key


def main() -> int:
    args = parse_args()
    papers_dir = Path(args.papers_dir).expanduser()
    expected_keys = load_expected_keys(args.expected_zotero_keys)

    if not papers_dir.exists():
        print(f"ERROR: papers dir not found: {papers_dir}")
        return 1

    note_files = list(papers_dir.glob("*.md"))
    key_to_file, issues, skipped_without_key = collect_note_status(
        papers_dir, args.strict_missing_zotero_key
    )

    print(f"Papers dir: {papers_dir}")
    print(f"Paper notes scanned: {len(note_files)}")
    print(f"Notes with zotero_key: {len(key_to_file)}")
    if skipped_without_key:
        print(f"Notes skipped without zotero_key: {len(skipped_without_key)}")

    if expected_keys:
        missing = [key for key in expected_keys if key not in key_to_file]
        extras = sorted(set(key_to_file) - set(expected_keys))
        print(f"Expected Zotero keys: {len(expected_keys)}")
        print(f"Covered Zotero keys: {len(expected_keys) - len(missing)} / {len(expected_keys)}")
        if missing:
            issues.append(f"Missing expected keys: {', '.join(missing)}")
        if extras:
            print(f"Extra zotero_key notes: {', '.join(extras)}")

    if skipped_without_key:
        print("Skipped note files without zotero_key:")
        for name in skipped_without_key:
            print(f"- {name}")

    if issues:
        print("\nISSUES:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("\nOK: schema and coverage checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
