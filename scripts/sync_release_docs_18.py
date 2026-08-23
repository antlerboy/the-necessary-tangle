#!/usr/bin/env python3
"""Synchronise maintained documentation with release 0.18."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "public-data.json").read_text(encoding="utf-8"))
RELEASE = "0.18-navigable-tangle-alpha"
GENERATED = "2026-08-23"
PUBLIC_URL = "https://transduction.systems/"


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.rstrip() + "\n", encoding="utf-8")


def parse(value, fallback=None):
    if fallback is None:
        fallback = []
    if isinstance(value, (list, dict)):
        return value
    if not value:
        return fallback
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return fallback


def ai_observations_document() -> str:
    report = DATA.get("ai_observations", {})
    sections = []
    for item in report.get("observations", []):
        sections.append(
            f"## {item['title']}\n\n"
            f"**Kind:** {item['kind']}\n\n"
            f"**Measurement:** {item['measurement']}\n\n"
            f"**Interpretation:** {item['interpretation']}\n\n"
            f"**Implication:** {item['implication']}\n\n"
            f"**Test:** {item['test']}\n"
        )
    return (
        "# AI observations\n\n"
        f"Generated for release `{RELEASE}` on {GENERATED}.\n\n"
        f"{report.get('method_note', '')}\n\n"
        + "\n".join(sections)
    )


def named_document() -> str:
    review = DATA.get("named_coverage_review", {})
    lines = [
        "# Named practitioner and institution coverage",
        "",
        f"Generated for release `{RELEASE}` on {GENERATED}.",
        "",
        review.get("method", ""),
        "",
        "| Name | Entry | Depth | Sources | Substantive connections | Status |",
        "|---|---|---:|---:|---:|---|",
    ]
    for item in review.get("items", []):
        lines.append(
            f"| {item['name']} | `{item['node_id']}` | {item['publication_level']} | "
            f"{item['public_source_count']} | {item['substantive_connection_count']} | {item['status']} |"
        )
    lines.extend([
        "",
        "‘Research queue’ means the name is now findable and duplicate-resistant, but the atlas does not yet have enough public source and typed-relation work for a developed account. The table completes the indexing and audit task; it does not pretend to complete the scholarship.",
    ])
    return "\n".join(lines)


def unfix_document() -> str:
    coverage = DATA.get("unfix_32_coverage", {})
    lines = [
        "# unFIX 32-concept coverage",
        "",
        f"Generated for release `{RELEASE}` on {GENERATED}.",
        "",
        coverage.get("method", ""),
        "",
        f"**Caution:** {coverage.get('caution', '')}",
        "",
        "| unFIX concept | Canonical atlas entry | Entry depth | Resolution |",
        "|---|---|---|---|",
    ]
    for item in coverage.get("items", []):
        resolution = "new brief entry" if item.get("created_in_0_18") else "existing canonical entry"
        lines.append(f"| {item['concept']} | `{item['node_id']}` | {item['publication_level']} | {resolution} |")
    return "\n".join(lines)


def iteration_document() -> str:
    meta = DATA.get("meta", {})
    named = DATA.get("named_coverage_review", {}).get("items", [])
    named_counts = {status: sum(1 for item in named if item.get("status") == status) for status in ("developed", "represented", "research_queue")}
    return f"""# Release 0.18: navigable tangle

Release: `{RELEASE}`  
Generated: `{GENERATED}`  
Public site: {PUBLIC_URL}

## Outcome

Make the atlas genuinely navigable from search result to entry to map, then incorporate the complete set of post-0.17 feedback without hiding unfinished scholarship.

## Reader-visible changes

- Entries open as a full-screen reading surface rather than a narrow right-hand strip.
- Connections are hoisted directly beneath the definition and summary.
- The map occupies most of the available screen and can be panned from nodes, connections or empty space; a movement threshold distinguishes dragging from selecting.
- ‘Constellation’ view places the selected entry at the centre, direct relations in an inner orbit and two-step relations in an outer orbit. This is question-relative placement, not a ranking of intellectual worth.
- Navigational cards, search suggestions, map nodes, map connections, entry actions and ‘Surprise me’ expose stable links which can be copied or opened in a separate tab.
- The brand mark is a tangle rather than the previous half-star/back-arrow form, and ‘Surprise me’ inherits the site typeface.
- The requested front-page sentence and ‘Find out more about how this works’ route are present.

## Content and source work

- Linda Booth Sweeney, *The Noisy Puddle* and *Do Bees Pee?* have source-backed profiles and typed connections. The Massachusetts Center for the Book establishes the 2025 picture-book award; the author's current publication notice establishes the June 2026 publication date for *Do Bees Pee?*.
- All 32 concepts in Jurgen Appelo's unFIX synthesis resolve to canonical entries. Documentary inclusion is recorded without treating the source's AI-assisted list or scores as a settled canon.
- {len(named)} requested people and institutions are canonicalised and searchable: {named_counts['developed']} developed, {named_counts['represented']} represented more briefly and {named_counts['research_queue']} left visibly in the research queue rather than padded with unsupported claims.
- Search aliases include Donna/Donella Meadows, Russ/Russell Ackoff and the supplied misspellings.
- Isolated ‘Damian’ references are expanded to Damian Allen and public-facing prose is scanned for wording which depends on an unseen prompt or conversation.
- AI observations are regenerated for the current graph and the new interaction model.

## Acceptance checks

- `make validate` completes the full historical build and all release validators.
- JavaScript syntax checks pass for the base application and both release overlays.
- Every unFIX concept resolves to a public canonical node.
- Every named item resolves to a public node and exposes actual depth.
- Navigational interactive elements have stable `href` targets; action buttons remain buttons.
- All internal item targets and redirect targets resolve.
- Public output contains no isolated `Damian` reference or banned hidden-conversation phrase.
- Desktop and mobile Playwright smoke tests can pan the map, open a full-screen entry and follow a right-clickable route.

## Deliberate limits

This release completes the submitted tasks as interface, indexing, source and audit work. It does not claim that every named thinker now has an equally deep scholarly profile, nor that the Monoskop, SysCoI, reading-list, Foundational Papers and company-knowledge programmes are exhausted. Those remain measured research programmes rather than invisible promises.
"""


def update_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    heading = f"## {RELEASE} — 23 August 2026"
    if heading in text:
        return
    entry = f"""{heading}

- Replaced narrow entry drawers with a full-screen reading surface and hoisted connections near definitions.
- Reworked map interaction so panning starts from nodes, lines or background; enlarged the canvas and added a question-relative constellation view.
- Made navigational surfaces expose stable URLs for copy, right-click and modified-click behaviour.
- Added source-backed Linda Booth Sweeney, *The Noisy Puddle* and *Do Bees Pee?* material.
- Resolved all 32 concepts in the unFIX comparator to canonical atlas entries with an explicit source-role caution.
- Canonicalised and audited every person and institution named in the post-0.17 feedback, with aliases and honest depth states.
- Added a standalone-language audit, refreshed AI observations, and published named/unFIX coverage tables.

"""
    marker = re.search(r"^## ", text, flags=re.MULTILINE)
    if marker:
        text = text[:marker.start()] + entry + text[marker.start():]
    else:
        text = text.rstrip() + "\n\n" + entry
    path.write_text(text, encoding="utf-8")


def update_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    block = f"""## Release 0.18

Release 0.18 makes the atlas navigable as a reading and map experience: full-screen entries, connections beside definitions, reliable panning, a constellation view and stable URLs for navigational controls. It also adds the Linda Booth Sweeney book updates, resolves the unFIX 32-concept comparator, audits all people and institutions named after 0.17, expands search aliases and refreshes the public AI observations.

Public routes:

- {PUBLIC_URL}
- {PUBLIC_URL}coverage/named/
- {PUBLIC_URL}coverage/unfix-32/

"""
    text = re.sub(r"## Release 0\.17\n.*?(?=\n## |\Z)", block.rstrip(), text, count=1, flags=re.DOTALL)
    if "## Release 0.18" not in text:
        first_heading_end = text.find("\n", text.find("# ")) + 1
        text = text[:first_heading_end] + "\n" + block + text[first_heading_end:]
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_citation() -> None:
    path = ROOT / "CITATION.cff"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^version: .*$", f"version: {RELEASE}", text)
    text = re.sub(r"(?m)^date-released: .*$", f"date-released: {GENERATED}", text)
    text = re.sub(r"(?m)^url: .*$", f"url: {PUBLIC_URL}", text, count=1)
    path.write_text(text, encoding="utf-8")


def update_rules() -> None:
    path = ROOT / "documentation" / "DESIGN_AND_CONTENT_RULES.md"
    text = path.read_text(encoding="utf-8")
    heading = "## Navigational link contract"
    if heading not in text:
        text += f"""

{heading}

Anything whose purpose is to take a reader to another stable atlas state must be an actual link with an `href`, including cards, search suggestions, map nodes, map connections, entry actions and serendipity routes. Plain left-click may be enhanced in place. Copy link, open in new tab, modified-click and browser history must remain coherent. Use buttons only for actions which cannot sensibly be represented as a URL, such as filtering, zooming, copying or submitting a form.

Public prose must stand alone. It must not answer an unseen prompt, refer to a person only by a private-conversation shorthand, or depend on knowledge of the development chat. Feedback and provenance belong in the ledger or source record; definitions and explanations must carry their own context.
"""
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_state() -> None:
    meta = DATA.get("meta", {})
    relational = DATA.get("relational_depth", {}).get("aggregate", {})
    write("documentation/TANGLE_STATE.md", f"""# The Necessary Tangle state

Release: `{RELEASE}`  
Generated: `{GENERATED}`  
Live site: {PUBLIC_URL}

## Current public graph

- Public entries: {meta.get('public_entry_count')}
- Developed profiles: {meta.get('profile_count')}
- Registered sources: {meta.get('source_count')}
- Guided journeys: {meta.get('journey_count')}
- Entries with reader connections: {relational.get('reader_connected_entries')}
- Reader relationship statements: {relational.get('reader_statements')}
- unFIX comparator concepts resolved: {meta.get('unfix_coverage_count')}
- Requested people and institutions audited: {meta.get('named_coverage_count')}

## Reader experience

The default route is question-led. Search and cards open a full-screen entry; its named connections are visible near the definition; ‘Place in the tangle’ opens a centred constellation. The complete map remains available for extent and gaps, but is not presented as a page to read all at once.

Map centrality, orbit and focus describe the current public graph and the reader's question. They are not judgements of intellectual importance.

## Publication state

The full historical build, release-specific validators and JavaScript checks are the publication gate. Public outputs are generated from public data, and release 0.18 includes standalone-language, internal-link and navigational-link checks.

## Known depth limits

The named coverage audit makes every requested item findable and reports actual depth. Research-queue entries still require public source and typed-lineage work. Existing long programmes for Foundational Papers, Monoskop, SysCoI/model.report, prior maps, practitioner constellations, the reading list and company-knowledge discovery remain open and measured.
""")


def update_next_work() -> None:
    write("documentation/NEXT_WORK.md", """# Next work

Status: **Awaiting curator selection — release 0.18 is complete and no implementation packet is active.**

The next bounded decision is whether to deepen the thinnest entries in the named-coverage audit, continue a previously defined corpus programme, or run observed-user testing on the new map and full-screen entry flow.

## Candidate one: named source and lineage depth

Choose a small cohort of research-queue names from `documentation/named-practitioner-coverage.md`. Add public primary or institutional sources, a responsible profile and typed relations. Do not turn the whole list into one unbounded research pass.

## Candidate two: observed navigation test

Ask several readers to find an entry, inspect a connection, place it in the constellation, open a related entry in a new tab and return to their original route. Record failures as reproducible tasks rather than general design reactions.

## Candidate three: existing corpus programme

Select one bounded section of Foundational Papers, Monoskop, SysCoI/model.report, the reading list or company-knowledge discovery. Preserve the difference between inventory, description, developed profile and critical comparison.

No production change is authorised by this holding packet. Use `documentation/WORK_TICKET_TEMPLATE.md` for the next selected outcome.
""")


def update_ledger() -> None:
    path = ROOT / "documentation" / "feedback-ledger.md"
    text = path.read_text(encoding="utf-8") if path.exists() else "# Feedback ledger\n"
    heading = "## Release 0.18 — navigability, standalone prose and named coverage"
    if heading not in text:
        text += f"""

{heading}

- Narrow result drawer: replaced by a full-screen reading surface.
- Connections too far down: moved beside the definition and entry orientation.
- Map difficult to pan and too small: panning now starts from nodes, lines or background; the canvas is larger and the inspector no longer squeezes it.
- Personalised author/principle map: implemented as a constellation view with selected star, inner orbit and outer orbit, while explicitly rejecting centrality as intellectual worth.
- Right-click/open-in-new-tab: navigational surfaces now expose stable `href` targets and the rule is part of the design contract.
- ‘Surprise me’ typeface and link semantics: corrected.
- Hero wording and explanation link: added.
- Brand mark: replaced with a tangle mark.
- Linda Booth Sweeney: source-backed profile and updates for *The Noisy Puddle* and *Do Bees Pee?* added.
- Named people and institutions: canonical names, aliases and actual depth published at `/coverage/named/`.
- Donna/Donella Meadows, Russ/Russell Ackoff and supplied misspellings: added as aliases without duplicating canonical entries.
- unFIX 32 concepts: all resolve to atlas entries and are published as a comparator at `/coverage/unfix-32/`.
- Hidden-conversation prose: isolated Damian references expanded to Damian Allen and a standalone-language validator added.
- AI observations: regenerated for the current graph, aliases, coverage and interface.
- Long corpus programmes: not falsely closed; their measured work remains in the coverage programme.
"""
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    write("documentation/ai-observations.md", ai_observations_document())
    write("documentation/named-practitioner-coverage.md", named_document())
    write("documentation/unfix-32-coverage.md", unfix_document())
    write("documentation/iteration-18-usability-and-coverage.md", iteration_document())
    update_changelog()
    update_readme()
    update_citation()
    update_rules()
    update_state()
    update_next_work()
    update_ledger()
    print(f"Synced maintained documentation for {RELEASE}")


if __name__ == "__main__":
    main()
