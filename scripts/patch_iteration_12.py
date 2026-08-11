#!/usr/bin/env python3
"""Patch the public interface for release 0.12 practitioner intake and orientation."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
APP = ROOT / "docs" / "assets" / "app.js"
CSS = ROOT / "docs" / "assets" / "site-enhancements.css"

READING_LIST = "https://stream.syscoi.com/2024/10/01/updated-rough-draft-systems-complexity-cybernetics-reading-list/"
QUEUE_URL = "https://github.com/antlerboy/the-necessary-tangle/issues?q=is%3Aissue+is%3Aopen+label%3Asite-submission"

START_SECTION = '''
      <section class="start-small-section" aria-labelledby="startSmallTitle">
        <div class="section-head"><div><p class="eyebrow">The whole graph is a lot</p><h2 id="startSmallTitle">Start somewhere smaller</h2><p>You do not need to swallow the atlas. Start with one person, one distinction or one short route. The full map is there when you want the weather system.</p></div></div>
        <div class="start-small-grid">
          <a class="start-small-card" href="#view=item&id=person_ivo_velitchkov&from=home"><span class="eyebrow">A practitioner constellation</span><strong>Ivo Velitchkov</strong><span>Viability, essential balances, requisite inefficiency and explicit graph semantics.</span></a>
          <a class="start-small-card" href="#view=item&id=concept_viability&from=home"><span class="eyebrow">One distinction</span><strong>Viability is not fitness</strong><span>What must persist, what may vary and what ‘survival of the viable’ does and does not claim.</span></a>
          <a class="start-small-card" href="#view=journeys&id=journey_viability_balance_and_strategy&step=0"><span class="eyebrow">A guided route</span><strong>From viability to balance and strategy</strong><span>Ten steps through Ivo Velitchkov, natural drift, Patrick Hoverstadt and applied systems work.</span></a>
          <a class="start-small-card" href="#view=map&layer=substantive&depth=profiles"><span class="eyebrow">A quieter map</span><strong>Developed entries and substantive lines</strong><span>Begin with the evidence-deepened core before opening the complete provenance graph.</span></a>
        </div>
      </section>
'''

MAP_ORIENTATION = '''
          <div class="map-orientation-panel" id="mapOrientationPanel">
            <p class="eyebrow">Start with less</p>
            <p>The full public map is deliberately untidy. Choose a smaller opening without changing the underlying graph.</p>
            <div class="map-orientation-links">
              <a href="#view=map&layer=substantive&depth=profiles">Developed core</a>
              <a href="#view=map&layer=conceptual&depth=profiles">Conceptual layer</a>
              <a href="#view=journeys&id=journey_viability_balance_and_strategy&step=0">Guided route</a>
              <a href="#view=map&layer=all&depth=all">Everything</a>
            </div>
          </div>
'''

INTAKE_PANEL = f'''
        <article class="plain-panel wide contribution-intake-panel">
          <p class="eyebrow">Public proposals, human review</p>
          <h2>How contributions enter the atlas</h2>
          <p>The form opens a GitHub issue labelled <code>site-submission</code> and <code>awaiting-curator-review</code>. Research issues and pull requests are also valid routes. Nothing changes the atlas automatically.</p>
          <p>Before publication, proposed material is checked for evidence, identity, duplicate entries, wording, rights, public safety and compatibility with the data model.</p>
          <div class="button-row wrap"><a class="button" href="{QUEUE_URL}" target="_blank" rel="noopener">View the proposal queue</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/contribution-intake.md" target="_blank" rel="noopener">Read the intake rule</a></div>
        </article>
'''


ABOUT_FEEDBACK = '''
        <article class="plain-panel wide feedback-people-callout">
          <p class="eyebrow">People, works and practice</p>
          <h2>Practitioner expertise</h2>
          <p><a href="#view=item&id=person_ivo_velitchkov&from=about">Ivo Velitchkov</a> connects viability, <em>Essential Balances</em>, requisite inefficiency, natural drift and <a href="#view=item&id=tool_nodica&from=about">Nodica</a>. <a href="#view=item&id=person_patrick_hoverstadt&from=about">Patrick Hoverstadt</a> connects the Viable System Model, systems laws, <em>The Grammar of Systems II</em>, <em>The Fractal Organisation Manual</em>, <em>Patterns of Strategy</em> and <em>Systems Approaches to Making Change</em>.</p>
          <p>The people, publications, concepts and methods are linked through typed relations and public sources.</p>
        </article>

        <article class="plain-panel wide explicit-semantics-callout">
          <p class="eyebrow">What the lines mean</p>
          <h2>Explicit semantics</h2>
          <p>The atlas uses an explicit relation vocabulary. Each line has a source, target, relation type, relation family, direction, ordinary-language phrase, evidence, scope and review status. ‘Authored’, ‘influenced’, ‘taught’, ‘criticised’, ‘specialises’ and ‘used in practice’ are not interchangeable.</p>
          <p><a href="#view=item&id=concept_explicit_semantics&from=about">Open explicit semantics</a>, <a href="#view=item&id=tool_nodica&from=about">open Nodica</a>, or <a href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/explicit-semantics.md" target="_blank" rel="noopener">read the maintained semantic contract →</a></p>
        </article>
'''


CSS_APPEND = r'''

/* 0.12 practitioner intake and less-scary orientation */
.start-small-section { margin: 2.3rem 0; }
.start-small-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(225px, 1fr)); gap: .85rem; }
.start-small-card { display: grid; align-content: start; gap: .42rem; min-height: 165px; padding: 1.1rem; border: 1px solid var(--line); border-top: 4px solid var(--purple); border-radius: var(--radius); background: var(--panel); box-shadow: var(--shadow); color: inherit; text-decoration: none; }
.start-small-card strong { color: var(--accent); font-size: 1.13rem; }
.start-small-card > span:last-child { color: var(--muted); line-height: 1.48; }
.start-small-card:hover, .start-small-card:focus-visible { border-color: var(--accent); transform: translateY(-2px); color: inherit; }
.map-orientation-panel { display: grid; gap: .45rem; margin: 0 0 .85rem; padding: .85rem; border: 1px solid var(--line); border-left: 4px solid var(--purple); border-radius: 8px; background: var(--panel-2); }
.map-orientation-panel p { margin: 0; }
.map-orientation-links { display: flex; flex-wrap: wrap; gap: .38rem; }
.map-orientation-links a { padding: .38rem .58rem; border: 1px solid var(--line); border-radius: 999px; background: var(--panel); color: var(--accent); font: 700 .75rem/1.2 Arial, sans-serif; text-decoration: none; }
.map-orientation-links a:hover, .map-orientation-links a:focus-visible { border-color: var(--accent); }
.contribution-intake-panel { border-left: 5px solid var(--purple); }
.feedback-people-callout { border-left: 5px solid var(--orange); }
.explicit-semantics-callout { border-left: 5px solid var(--purple); }
.contribution-intake-panel code { overflow-wrap: anywhere; }
@media (max-width: 680px) {
  .start-small-card { min-height: 0; }
  .map-orientation-links { display: grid; grid-template-columns: 1fr 1fr; }
}
'''


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Could not find {label}")
    return text.replace(old, new, 1)


def patch_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    text = text.replace("https://www.antlerboy.com/reading-list", READING_LIST)

    if 'id="startSmallTitle"' not in text:
        marker = '<div class="section-head"><div><p class="eyebrow">Begin here</p><h2>Guided questions</h2>'
        if marker not in text:
            raise RuntimeError("Could not find guided-question opening")
        text = text.replace(marker, START_SECTION + "\n" + marker, 1)

    if 'id="mapOrientationPanel"' not in text:
        marker = '          <div class="smart-search" data-search-role="map">'
        if marker not in text:
            raise RuntimeError("Could not find map search")
        text = text.replace(marker, MAP_ORIENTATION + marker, 1)

    if 'class="plain-panel wide contribution-intake-panel"' not in text:
        marker = '<form id="contributionForm" class="contribution-form">'
        if marker not in text:
            raise RuntimeError("Could not find contribution form")
        text = text.replace(marker, INTAKE_PANEL + marker, 1)

    if 'class="plain-panel wide feedback-people-callout"' not in text:
        marker = '        <article class="plain-panel wide"><h2>A practitioner-centred origin</h2>'
        if marker not in text:
            raise RuntimeError("Could not find practitioner-centred origin")
        text = text.replace(marker, ABOUT_FEEDBACK + "\n" + marker, 1)

    documentation_marker = '<a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/roadmap.md" target="_blank" rel="noopener">Roadmap</a>'
    documentation_new = documentation_marker + '<a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/explicit-semantics.md" target="_blank" rel="noopener">Explicit semantics</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/contribution-intake.md" target="_blank" rel="noopener">Contribution intake</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/reading-list-coverage.md" target="_blank" rel="noopener">Reading-list coverage</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/scio-coverage.md" target="_blank" rel="noopener">SCiO coverage</a>'
    if 'documentation/explicit-semantics.md" target=' not in text:
        text = replace_once(text, documentation_marker, documentation_new, "documentation buttons")

    INDEX.write_text(clean(text), encoding="utf-8")


def patch_app() -> None:
    app = APP.read_text(encoding="utf-8")

    marker_old = '''      '## Contributor',
      values.name || 'GitHub account shown on the issue.',
      '',
      '---',
      `Prepared from The Necessary Tangle ${DATA.meta.release}. The contributor reviewed this text before submitting it.`'''
    marker_new = '''      '## Contributor',
      values.name || 'GitHub account shown on the issue.',
      '',
      '## Intake marker',
      'site-submission',
      '',
      '---',
      `Prepared from The Necessary Tangle ${DATA.meta.release}. The contributor reviewed this text before submitting it.`'''
    if "'## Intake marker'" not in app:
        app = replace_once(app, marker_old, marker_new, "contribution intake marker")

    return_old = '''    const repository = CONFIG.repositoryUrl || DATA.meta.repository_url;
    return `${repository}/issues/new?${new URLSearchParams({ title, body }).toString()}`;'''
    return_new = '''    const repository = CONFIG.repositoryUrl || DATA.meta.repository_url;
    const labels = 'site-submission,awaiting-curator-review';
    return `${repository}/issues/new?${new URLSearchParams({ title, body, labels }).toString()}`;'''
    if "const labels = 'site-submission,awaiting-curator-review';" not in app:
        app = replace_once(app, return_old, return_new, "contribution labels")

    app = app.replace(
        "A GitHub issue has opened in a new tab. Review the wording there, then submit it.",
        "A labelled GitHub issue has opened in a new tab. Review the wording there, then submit it for curator review.",
    )
    APP.write_text(clean(app), encoding="utf-8")


def patch_css() -> None:
    css = CSS.read_text(encoding="utf-8") if CSS.exists() else ""
    if ".start-small-section" not in css:
        css = css.rstrip() + "\n" + CSS_APPEND.strip() + "\n"
    CSS.write_text(clean(css), encoding="utf-8")


def main() -> None:
    patch_index()
    patch_app()
    patch_css()
    print("Patched 0.12 public orientation, explicit semantics and contribution intake")


if __name__ == "__main__":
    main()
