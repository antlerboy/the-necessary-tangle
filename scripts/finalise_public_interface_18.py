#!/usr/bin/env python3
"""Normalise the public shell and remove production-chat residue for release 0.18."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INDEX = DOCS / "index.html"
UPDATE_URL = "https://github.com/antlerboy/the-necessary-tangle/issues/2"
UPDATE_ANCHOR = (
    f'<a class="update-thread-dot" data-update-thread-dot href="{UPDATE_URL}" '
    'target="_blank" rel="noopener" aria-label="Open updates"></a>'
)

REPLACEMENTS = (
    ("As requested", "In this release"),
    ("as requested", "in this release"),
    ("You asked", "The public question asks"),
    ("you asked", "the public question asks"),
    ("Your prompt", "The originating question"),
    ("your prompt", "the originating question"),
    ("This conversation", "The originating research context"),
    ("this conversation", "the originating research context"),
    ("Our conversation", "The originating research context"),
    ("our conversation", "the originating research context"),
)


def public_text_paths() -> list[Path]:
    paths = {
        ROOT / "data" / "public-data.json",
        *DOCS.rglob("*.html"),
        *DOCS.rglob("*.js"),
        *DOCS.rglob("*.css"),
        *DOCS.rglob("*.json"),
        *(ROOT / "documentation").glob("*.md"),
        ROOT / "README.md",
        ROOT / "ACKNOWLEDGEMENTS.md",
        ROOT / "CHANGELOG.md",
        ROOT / "CITATION.cff",
    }
    return sorted((path for path in paths if path.exists()), key=lambda path: str(path))


def sanitise(text: str) -> tuple[str, int]:
    count = 0
    for before, after in REPLACEMENTS:
        occurrences = text.count(before)
        if occurrences:
            text = text.replace(before, after)
            count += occurrences
    return text, count


def normalise_update_dot(index: str) -> str:
    # Remove every old version of the fixed update control before adding one exact,
    # validator-visible anchor. Other issue-2 links become the public contribution route.
    index = re.sub(
        r'<a\b[^>]*(?:data-update-thread-dot|class="[^"]*update-thread-dot[^"]*")[^>]*>\s*</a>',
        "",
        index,
        flags=re.IGNORECASE | re.DOTALL,
    )
    index = index.replace(UPDATE_URL, "#view=contribute")
    index = "\n".join(line.rstrip() for line in index.splitlines()) + "\n"
    if "</body>" not in index:
        raise SystemExit("docs/index.html has no closing body tag")
    return index.replace("</body>", f"  {UPDATE_ANCHOR}\n</body>", 1)


def main() -> None:
    changed_files = 0
    replacements = 0
    for path in public_text_paths():
        text = path.read_text(encoding="utf-8", errors="ignore")
        updated, count = sanitise(text)
        if path == INDEX:
            updated = normalise_update_dot(updated)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed_files += 1
        replacements += count

    index = INDEX.read_text(encoding="utf-8")
    if index.count(UPDATE_ANCHOR) != 1 or index.count(UPDATE_URL) != 1:
        raise SystemExit("The public update route is not exactly singular after normalisation")

    public_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in public_text_paths()
        if path != INDEX
    )
    forbidden = [before.casefold() for before, _ in REPLACEMENTS]
    lower = public_text.casefold()
    remaining = sorted({phrase for phrase in forbidden if phrase in lower})
    if remaining:
        raise SystemExit("Production-chat residue remains: " + ", ".join(remaining))

    print(
        f"Finalised the public shell: one updates dot, {replacements} prose replacements "
        f"across {changed_files} files."
    )


if __name__ == "__main__":
    main()
