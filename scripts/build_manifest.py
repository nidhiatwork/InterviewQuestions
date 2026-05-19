#!/usr/bin/env python3
"""Regenerate manifest.json from state/state.json + playground/ + visualizers/.

The manifest is consumed by index.html (assets/app.js) to populate the nav and
render question cards. Run this whenever state.json or playground/ changes:

    python scripts/build_manifest.py

It is also invoked at the end of each /dsa-daily Pick run before git push.
"""
from __future__ import annotations

import json
import pathlib
import sys
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "state" / "state.json"
PLAYGROUND_DIR = ROOT / "playground"
VISUALIZERS_DIR = ROOT / "visualizers"
MANIFEST_FILE = ROOT / "manifest.json"

REPO_URL_DEFAULT = "https://github.com/"


def load_state() -> dict:
    if not STATE_FILE.exists():
        sys.exit(f"state.json not found at {STATE_FILE}")
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def has_visualizer(date: str, slug: str) -> bool:
    return (VISUALIZERS_DIR / f"{date}-{slug}.html").exists()


def playground_exists(date: str, slug: str) -> bool:
    return (PLAYGROUND_DIR / f"{date}-{slug}.py").exists()


def build() -> dict:
    state = load_state()
    questions = []
    for q in state.get("askedQuestions", []):
        date = q["date"]
        slug = q["slug"]
        if not playground_exists(date, slug):
            # Skip entries whose .py is missing (legacy or moved files)
            print(f"  skip {date}-{slug}: playground file not found", file=sys.stderr)
            continue
        questions.append({
            "date": date,
            "slug": slug,
            "title": q["title"],
            "leetcodeId": q["leetcodeId"],
            "url": q["url"],
            "dataStructure": q["dataStructure"],
            "difficulty": "Medium",
            "filename": f"{date}-{slug}.py",
            "hasVisualizer": has_visualizer(date, slug),
        })

    # Newest first
    questions.sort(key=lambda x: x["date"], reverse=True)

    repo_url = REPO_URL_DEFAULT
    repo_marker = ROOT / ".repo_url"
    if repo_marker.exists():
        repo_url = repo_marker.read_text(encoding="utf-8").strip()

    return {
        "generatedAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repoUrl": repo_url,
        "questions": questions,
    }


def main() -> int:
    manifest = build()
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST_FILE} ({len(manifest['questions'])} questions)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
