#!/usr/bin/env python3
"""Patch the public interface and repository prose for release 0.14."""
from __future__ import annotations

import json
import re
from pathlib import Path

from apply_iteration_14 import GENERATED, RELEASE, make_observations, write_ai_document

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
INDEX = ROOT / "docs" / "index.html"
CSS = ROOT / "docs" / "assets" / "site-enhancements.css"
UPDATE_URL = "https://github.com/antlerboy/the-necessary-tangle/" + "issues/" + "2"

SOURCE_PANEL = """        <article class="plain-panel wide cynefin-source-panel">
          <p class="eyebrow">Naturalising sense-making</p>
          <h2>Dave Snowden, Cynefin and source roles</h2>
          <p>The atlas now separates the people, papers, framework, tools, organisation and public source corpora around Cynefin. Dave Snowden's author archive is a primary record of his dated public arguments. Cynefin.io is the project's current collaborative semantic network. Neither source is treated as independent proof of influence, priority or effectiveness.</p>
          <div class="button-row wrap"><a class="button" href="#view=item&id=person_dave_snowden&from=about">Dave Snowden</a><a class="button" href="#view=item&id=method_or_methodology_cynefin_framework&from=about">Cynefin framework</a><a class="button" href="#view=journeys&id=journey_snowden_cynefin_sources_and_practice&step=0">Guided route</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/snowden-cynefin-sources.md" target="_blank" rel="noopener">Source roles</a></div>
        </article>"""

DOT = f'<a class="update-thread-dot" data-update-thread-dot href="{UPDATE_URL}" target="_blank" rel="noopener" aria-label="Open updates"></a>'

DOT_CSS = """
/* Discreet fixed updates control */
.update-thread-dot {
  position: fixed;
  right: 3px;
  bottom: 3px;
  z-index: 1200;
  display: block;
  width: 17px;
  height: 17px;
  border: 0;
  border-radius: 50%;
  background: var(--accent);
  opacity: .14;
  box-shadow: 0 0 0 1px color-mix(in srgb, var(--paper) 70%, transparent);
  text-decoration: none;
}
.update-thread-dot:hover,
.update-thread-dot:focus-visible {
  opacity: .82;
  outline: 2px solid var(--orange);
  outline-offset: 2px;
}
"""


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def refresh_ai_observations() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    report = make_observations(data)
    data["ai_observations"] = report
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    (ROOT / "docs" / "assets" / "public-data.json").write_text(rendered, encoding="utf-8")
    (ROOT / "docs" / "assets" / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    write_ai_document(report)


def patch_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    text = re.sub(r'\n[ \t]*<a\b(?=[^>]*data-update-thread-dot)[^>]*>.*?</a>[ \t]*(?=\n</body>)', '', text, flags=re.I | re.S)
    text = re.sub(r'\s*<article class="plain-panel wide cynefin-source-panel">.*?</article>', '', text, flags=re.S)

    card = '<a class="start-small-card" href="#view=journeys&id=journey_snowden_cynefin_sources_and_practice&step=0"><span class="eyebrow">Context and sense-making</span><strong>Snowden and Cynefin</strong><span>Framework, papers, tools and the different jobs done by a blog, wiki, publisher and public institution.</span></a>'
    if card not in text:
        marker = '          <a class="start-small-card" href="#view=map&layer=substantive&depth=profiles"><span class="eyebrow">A quieter map</span><strong>Developed entries and substantive lines</strong><span>Begin with the evidence-deepened core before opening the complete provenance graph.</span></a>'
        if marker not in text:
            raise RuntimeError("Could not locate the start-small card marker")
        text = text.replace(marker, marker + "\n          " + card, 1)

    marker = '        <article class="plain-panel wide"><h2>Curatorship and acknowledgements</h2>'
    if marker not in text:
        raise RuntimeError("Could not locate the About-page curatorship marker")
    text = text.replace(marker, SOURCE_PANEL + "\n\n" + marker, 1)

    documentation_old = '<article class="plain-panel wide"><h2>Documentation</h2><p>The method, source policy, data model, maintenance process, governance, coverage programme and current limitations live with the project rather than in detached files.</p><div class="button-row wrap"><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/reading-the-atlas.md" target="_blank" rel="noopener">How to read the atlas</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/editorial-model.md" target="_blank" rel="noopener">Editorial model</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/source-policy.md" target="_blank" rel="noopener">Source policy</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/coverage-programme.md" target="_blank" rel="noopener">Coverage programme</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/roadmap.md" target="_blank" rel="noopener">Roadmap</a></div></article>'
    documentation_new = '<article class="plain-panel wide"><h2>Documentation</h2><p>The method, source policy, data model, maintenance process, governance, coverage programme and current limitations live with the project rather than in detached files.</p><div class="button-row wrap"><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/reading-the-atlas.md" target="_blank" rel="noopener">How to read the atlas</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/editorial-model.md" target="_blank" rel="noopener">Editorial model</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/source-policy.md" target="_blank" rel="noopener">Source policy</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/canonical-source-register.md" target="_blank" rel="noopener">Canonical source roles</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/coverage-programme.md" target="_blank" rel="noopener">Coverage programme</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/roadmap.md" target="_blank" rel="noopener">Roadmap</a></div></article>'
    if documentation_old in text:
        text = text.replace(documentation_old, documentation_new, 1)

    if "</body>" not in text:
        raise RuntimeError("Could not locate closing body tag")
    text = re.sub(r"\s*</body>", "\n\n  " + DOT + "\n</body>", text, count=1)
    INDEX.write_text(clean(text), encoding="utf-8")


def patch_css() -> None:
    text = CSS.read_text(encoding="utf-8")
    text = re.sub(r'\n?/\* Discreet fixed updates control \*/.*?(?=\n/\*|\Z)', '', text, flags=re.S)
    CSS.write_text(clean(text + "\n" + DOT_CSS), encoding="utf-8")


def patch_repository_prose() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data["meta"]
    entries = meta["public_entry_count"]
    profiles = meta["profile_count"]
    sources = meta["source_count"]
    journeys = meta["journey_count"]

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    readme = re.sub(
        r"This is a public alpha\. Release 0\.13 contains \d+ canonical public entries, including \d+ developed profiles, \d+ sources and \d+ guided journeys\.",
        f"This is a public alpha. Release 0.14 contains {entries} canonical public entries, including {profiles} developed profiles, {sources} sources and {journeys} guided journeys.",
        readme,
        count=1,
    )
    readme = readme.replace(
        "The strongest current material is around boundaries and observers; feedback and regulation; variety, viability and the Viable System Model; systems laws, strategy and applied practitioner lineages; recursion; emergence; and self-organisation.",
        "The strongest current material is around boundaries and observers; feedback and regulation; variety, viability and the Viable System Model; systems laws and strategy; context-sensitive sense-making and Cynefin; applied practitioner lineages; recursion; emergence; and self-organisation.",
    )
    source_sentence = "The [Dave Snowden and Cynefin source account](documentation/snowden-cynefin-sources.md) distinguishes the evidential roles of author archive, project wiki, primary papers, publisher records and public institutional applications."
    if source_sentence not in readme:
        readme = readme.replace("\n## Start here\n", "\n" + source_sentence + "\n\n## Start here\n", 1)
    readme_path.write_text(clean(readme), encoding="utf-8")

    citation_path = ROOT / "CITATION.cff"
    citation = citation_path.read_text(encoding="utf-8")
    citation = re.sub(r"^version:.*$", f"version: {RELEASE}", citation, flags=re.M)
    citation = re.sub(r"^date-released:.*$", f"date-released: {GENERATED}", citation, flags=re.M)
    citation_path.write_text(clean(citation), encoding="utf-8")

    changelog_path = ROOT / "CHANGELOG.md"
    changelog = changelog_path.read_text(encoding="utf-8")
    if "## 0.14-snowden-cynefin-alpha" not in changelog:
        entry = """## 0.14-snowden-cynefin-alpha — 11 August 2026

- Added a developed Dave Snowden and Cynefin constellation spanning people, primary works, the Cynefin framework, SenseMaker, naturalising sense-making, anthro-complexity, Estuarine Mapping and distributed ethnography.
- Registered Dave Snowden's author archive and Cynefin.io as canonical first-party sources for different evidential jobs, with explicit limits on claims about influence, priority and effectiveness.
- Added publisher and public-institution records for the principal dated papers, the Harvard Business Review article and the European Commission Joint Research Centre field guide.
- Added a guided route through the work and its source roles.
- Regenerated graph measurements and observations from the current release on every complete build.
"""
        changelog = changelog.replace("# Changelog\n\n", "# Changelog\n\n" + entry, 1)
    changelog_path.write_text(clean(changelog), encoding="utf-8")

    acknowledgements_path = ROOT / "ACKNOWLEDGEMENTS.md"
    acknowledgements = acknowledgements_path.read_text(encoding="utf-8")
    paragraph = "Dave Snowden's work contributes Cynefin, SenseMaker, naturalising sense-making, anthro-complexity, constraint-based strategy and a substantial dated public essay archive. Cynthia F. Kurtz, Mary E. Boone and Alessandro Rancati are represented through their documented collaborations and publications. Cynefin.io contributors maintain a current semantic and method corpus whose value and limits are recorded source by source."
    if paragraph not in acknowledgements:
        marker = "Peter Checkland, Werner Ulrich, Ray Ison, Ed Straw, Raul Espejo, Alfonso Reyes, Donella Meadows, Diana Wright and Barry Oshry provide further practice-facing routes through inquiry, boundary critique, systemic governance, organisational cybernetics, feedback, intervention and whole-system relations."
        if marker not in acknowledgements:
            raise RuntimeError("Could not locate acknowledgements insertion marker")
        acknowledgements = acknowledgements.replace(marker, marker + "\n\n" + paragraph, 1)
    acknowledgements_path.write_text(clean(acknowledgements), encoding="utf-8")


def main() -> None:
    refresh_ai_observations()
    patch_index()
    patch_css()
    patch_repository_prose()
    print("Patched 0.14 Cynefin source framing, observations and discreet updates route")


if __name__ == "__main__":
    main()
