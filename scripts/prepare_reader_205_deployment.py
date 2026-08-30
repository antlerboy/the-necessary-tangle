#!/usr/bin/env python3
"""Prepare the 0.20.5 reader composition for build and deployment."""
from pathlib import Path

INDEX = Path("docs/index.html")

OLD_AI_NOTE = (
    '<p class="release-note-inline"><strong>Updated for 0.20:</strong> observations now examine comparator link meanings, '
    'partial reconciliation, complete source-link preservation and the evidential ceiling of aggregate maps.</p>'
)
NEW_AI_NOTE = (
    '<p class="release-note-inline"><strong>Updated for 0.20.5:</strong> observations now include release-state drift, '
    'interface accumulation, display-layer isolation, SCiO corpus boundaries and the difference between linking a '
    'source graph and canonising it.</p>'
)


def replace_optional(text: str, old: str, new: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"0.20.5 deployment source drifted; expected text not found: {old[:120]}")
    return text.replace(old, new, 1)


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")

    text = replace_optional(
        text,
        'assets/iteration-20.js?v=0.20.4-rule-position',
        'assets/iteration-20.js?v=0.20.5-header',
    )
    text = replace_optional(
        text,
        '<span id="releaseBadge">Public alpha</span>',
        '<span id="releaseBadge">Release 0.20.5</span>',
    )
    text = replace_optional(text, OLD_AI_NOTE, NEW_AI_NOTE)

    # Make the title stack structural, not something JavaScript invents after
    # first paint. iteration-20.js still moves the asynchronously loaded rule
    # into this stack once the rule source arrives.
    if '<div class="brand-stack">' not in text:
        brand_start = '    <a class="brand" href="#view=home" aria-label="The Necessary Tangle home">'
        brand_end = '    </a>\n    <div class="header-meta">'
        if brand_start not in text or brand_end not in text:
            raise SystemExit("0.20.5 deployment source drifted; header anchors not found")
        text = text.replace(brand_start, '    <div class="brand-stack">\n' + brand_start, 1)
        text = text.replace(brand_end, '    </a>\n    </div>\n    <div class="header-meta">', 1)

    INDEX.write_text(text, encoding="utf-8")
    print(f"Prepared {INDEX} for 0.20.5 release/header/AI state")


if __name__ == "__main__":
    main()
