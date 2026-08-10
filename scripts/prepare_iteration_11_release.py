#!/usr/bin/env python3
"""Wire release 0.11 into the durable build and regression gates."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_10 = "0.10-practice-safety-alpha"
RELEASE_11 = "0.11-semantic-map-alpha"


def wire_makefile() -> None:
    path = ROOT / "Makefile"
    text = path.read_text(encoding="utf-8")

    if "\tpython3 scripts/apply_iteration_11.py\n" not in text:
        marker = "\tpython3 scripts/apply_iteration_10.py\n"
        if marker not in text:
            raise RuntimeError("Could not locate apply_iteration_10.py in Makefile")
        text = text.replace(marker, marker + "\tpython3 scripts/apply_iteration_11.py\n", 1)

    if "\tpython3 scripts/patch_iteration_11.py\n" not in text:
        marker = "\tpython3 scripts/patch_iteration_10.py\n"
        if marker not in text:
            raise RuntimeError("Could not locate patch_iteration_10.py in Makefile")
        text = text.replace(marker, marker + "\tpython3 scripts/patch_iteration_11.py\n", 1)

    if "\tpython3 scripts/validate_iteration_11.py\n" not in text:
        marker = "\tpython3 scripts/validate_iteration_10.py\n"
        if marker not in text:
            raise RuntimeError("Could not locate validate_iteration_10.py in Makefile")
        text = text.replace(marker, marker + "\tpython3 scripts/validate_iteration_11.py\n", 1)

    path.write_text(text, encoding="utf-8")


def extend_release_sets() -> None:
    validators = sorted((ROOT / "scripts").glob("validate*.py"))
    for path in validators:
        text = path.read_text(encoding="utf-8")
        original = text

        # Add 0.11 to literal release sets which already admit 0.10.
        for closing in ["}", "]", ")"]:
            old = f'"{RELEASE_10}"{closing}'
            new = f'"{RELEASE_10}", "{RELEASE_11}"{closing}'
            text = text.replace(old, new)

        # The 0.10 validator is a regression gate for its content, not a ban on later releases.
        if path.name == "validate_iteration_10.py":
            text = text.replace(
                f'EXPECTED_RELEASE = "{RELEASE_10}"',
                f'ALLOWED_RELEASES = {{"{RELEASE_10}", "{RELEASE_11}"}}',
            )
            text = text.replace(
                'if meta.get("release") != EXPECTED_RELEASE:\n        errors.append(f"meta.release must be {EXPECTED_RELEASE}")',
                'if meta.get("release") not in ALLOWED_RELEASES:\n        errors.append(f"meta.release must be one of {sorted(ALLOWED_RELEASES)}")',
            )
            text = text.replace(
                "if meta.get('release') != EXPECTED_RELEASE:\n        errors.append(f\"meta.release must be {EXPECTED_RELEASE}\")",
                "if meta.get('release') not in ALLOWED_RELEASES:\n        errors.append(f\"meta.release must be one of {sorted(ALLOWED_RELEASES)}\")",
            )

            # Release 0.10 deliberately removed the dot. Release 0.11 deliberately restores it.
            conditions = [
                'if "/issues/2" in index:',
                "if '/issues/2' in index:",
                'if "issues/2" in index:',
                "if 'issues/2' in index:",
                'if "/issues/2" in public_payload:',
                "if '/issues/2' in public_payload:",
                'if "feedback-dot" in index:',
                "if 'feedback-dot' in index:",
                'if \'class="feedback-dot"\' in index:',
                'if "class=\\\"feedback-dot\\\"" in index:',
            ]
            for condition in conditions:
                if condition in text and f'meta.get("release") == "{RELEASE_10}" and' not in condition:
                    expression = condition[len("if ") : -1]
                    text = text.replace(
                        condition,
                        f'if meta.get("release") == "{RELEASE_10}" and {expression}:',
                    )

            # Some versions used explicit absence assertions.
            text = text.replace(
                "if '/issues/2' not in index:",
                f'if meta.get("release") == "{RELEASE_11}" and \'/issues/2\' not in index:',
            )
            text = text.replace(
                'if "/issues/2" not in index:',
                f'if meta.get("release") == "{RELEASE_11}" and "/issues/2" not in index:',
            )

            if "ALLOWED_RELEASES" not in text or RELEASE_11 not in text:
                raise RuntimeError("Could not make validate_iteration_10.py accept release 0.11")

        if text != original:
            path.write_text(text, encoding="utf-8")


def patch_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    if "## 0.11-semantic-map-alpha" in text:
        return
    entry = "\n".join(
        [
            "## 0.11-semantic-map-alpha — 10 August 2026",
            "",
            "- Restored the discreet bottom-right route to the running-feedback thread.",
            "- Added a complete feedback ledger distinguishing implemented work, first passes and open research programmes.",
            "- Added semantic zoom: adaptive label disclosure, overview minimap, focus trail, double-click neighbourhood focus and hover neighbourhood emphasis.",
            "- Added fullscreen and keyboard map controls plus optional local node arrangement.",
            "- Kept the full graph, typed layers and curator-controlled publication model unchanged.",
            "",
        ]
    ) + "\n"
    first_break = text.find("\n\n")
    text = text[: first_break + 2] + entry + text[first_break + 2 :]
    path.write_text(text, encoding="utf-8")


def patch_roadmap() -> None:
    path = ROOT / "documentation" / "roadmap.md"
    text = path.read_text(encoding="utf-8")
    additions = [
        "- test the semantic-map interaction with real readers before adding a heavier graph library;",
        "- recompute and compare provisional neighbourhoods as the substantive graph changes;",
        "- maintain the running-feedback ledger so first passes are not mistaken for completed coverage;",
        "- deepen the open corpus, archive, comparator, lineage and company-knowledge programmes recorded in the ledger;",
    ]
    if additions[0] not in text:
        marker = "## Later\n"
        if marker not in text:
            raise RuntimeError("Could not locate the Later section in roadmap.md")
        text = text.replace(marker, "\n".join(additions) + "\n\n" + marker, 1)
    path.write_text(text, encoding="utf-8")


def patch_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    note = "- [Running feedback ledger](documentation/feedback-ledger.md) — what was implemented, what received a first pass, and what remains open.\n"
    if note not in text:
        heading = "## Documentation\n"
        if heading in text:
            text = text.replace(heading, heading + "\n" + note, 1)
        else:
            text = text.rstrip() + "\n\n## Documentation\n\n" + note
    path.write_text(text, encoding="utf-8")


def main() -> None:
    wire_makefile()
    extend_release_sets()
    patch_changelog()
    patch_roadmap()
    patch_readme()
    print("Prepared durable release 0.11 and regression gates")


if __name__ == "__main__":
    main()
