#!/usr/bin/env python3
"""Extract every clickable area from Castellani's current public image map.

The extractor preserves the links exactly as the source publishes them.  It
does not claim that a destination is current, correct, or attached to the right
label.  Differences between ``alt`` and ``title`` are retained as review flags
rather than silently repaired.
"""
from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "comparator-castellani-links.json"
BASE = "https://art-sciencefactory.com/complexity-map_feb09.html"
IMAGE = "https://art-sciencefactory.com/images/MAP-WEB-May2026.jpg"


class AreaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.areas: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() == "area":
            self.areas.append({key.casefold(): value or "" for key, value in attrs})


def normalise_label(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value.casefold()).split())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", help="saved source HTML")
    parser.add_argument("--out", default=str(OUT))
    args = parser.parse_args()

    raw = Path(args.html).read_bytes()
    start = raw.lower().find(b"<html")
    if start < 0:
        raise SystemExit("No HTML document found")

    parsed = AreaParser()
    parsed.feed(raw[start:].decode("latin-1", errors="replace"))
    records = []
    for index, area in enumerate(parsed.areas, start=1):
        href = urljoin(BASE, area.get("href", "").strip())
        scheme = urlparse(href).scheme.casefold()
        if scheme not in {"http", "https"}:
            raise SystemExit(f"Unsafe or unsupported URL scheme in area {index}: {href}")
        alt = area.get("alt", "").strip()
        title = area.get("title", "").strip()
        records.append(
            {
                "source_link_id": f"castellani_2026_{index:03d}",
                "shape": area.get("shape", "rect").casefold(),
                "coords": area.get("coords", ""),
                "href": href,
                "alt": alt,
                "title": title,
                "display_label": alt or title or f"Map link {index}",
                "label_disagreement": bool(
                    alt
                    and title
                    and normalise_label(alt) != normalise_label(title)
                ),
                "link_role": "outbound_reference_from_map_entry",
                "accuracy_status": "source_link_not_independently_checked",
            }
        )

    if len(records) < 300:
        raise SystemExit(f"Expected at least 300 clickable areas; found {len(records)}")
    if any(not record["coords"] for record in records):
        raise SystemExit("At least one clickable area has no coordinates")

    output = {
        "meta": {
            "dataset": "comparator-castellani-links",
            "title": "Map of the Complexity Sciences — current public image map",
            "source_page": BASE,
            "source_image": IMAGE,
            "source_version": "May 2026",
            "checked": "2026-08-25",
            "link_count": len(records),
            "unique_destination_count": len({record["href"] for record in records}),
            "label_disagreement_count": sum(record["label_disagreement"] for record in records),
            "semantics": (
                "Each record is a clickable outward reference attached to a source-map "
                "area. It is not a graph edge, endorsement, or independently verified claim."
            ),
            "preservation_policy": (
                "All source links are retained as published. Obvious label/destination "
                "mismatches are exposed for review rather than silently corrected."
            ),
        },
        "links": records,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Wrote {len(records)} Castellani source links; "
        f"{output['meta']['label_disagreement_count']} alt/title disagreements retained."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
