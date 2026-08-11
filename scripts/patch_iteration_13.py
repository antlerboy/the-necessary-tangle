#!/usr/bin/env python3
"""Patch the public interface and repository prose for release 0.13."""
from __future__ import annotations

import json
import re
from pathlib import Path

from apply_iteration_09 import graph_metrics
from apply_iteration_13 import make_observations, write_ai_document

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
INDEX = ROOT / "docs" / "index.html"
APP = ROOT / "docs" / "assets" / "app.js"
CSS = ROOT / "docs" / "assets" / "site-enhancements.css"
CONFIG = ROOT / "docs" / "assets" / "site-config.js"

START_SECTION = '''      <section class="start-small-section" aria-labelledby="startSmallTitle">
        <div class="section-head"><div><p class="eyebrow">The whole graph is a lot</p><h2 id="startSmallTitle">Start somewhere smaller</h2><p>Begin with a person, a method, a distinction or one guided route. Open the complete graph only when it serves the question.</p></div></div>
        <div class="start-small-grid">
          <a class="start-small-card" href="#view=item&id=person_ivo_velitchkov&from=home"><span class="eyebrow">Viability and balance</span><strong>Ivo Velitchkov</strong><span>Viable organisation, Essential Balances, requisite inefficiency and explicit semantic graphs.</span></a>
          <a class="start-small-card" href="#view=item&id=person_patrick_hoverstadt&from=home"><span class="eyebrow">Management cybernetics</span><strong>Patrick Hoverstadt</strong><span>The Viable System Model, systems laws, organisation design and relational strategy.</span></a>
          <a class="start-small-card" href="#view=journeys&id=journey_inquiry_governance_and_intervention&step=0"><span class="eyebrow">A guided route</span><strong>Inquiry, governance and intervention</strong><span>Checkland, Ulrich, Espejo, Ison, Meadows, Oshry, Velitchkov and Hoverstadt in one inspectable route.</span></a>
          <a class="start-small-card" href="#view=item&id=person_donella_meadows&from=home"><span class="eyebrow">Feedback and intervention</span><strong>Donella Meadows</strong><span>Thinking in Systems, leverage points and disciplines for acting with nonlinear systems.</span></a>
          <a class="start-small-card" href="#view=map&layer=substantive&depth=profiles"><span class="eyebrow">A quieter map</span><strong>Developed entries and substantive lines</strong><span>Begin with the evidence-deepened core before opening the complete provenance graph.</span></a>
        </div>
      </section>'''

ASK_SECTION = '''    <section id="view-ask" class="view">
      <header class="page-head"><p class="eyebrow">Question-led exploration</p><h1>Ask The Necessary Tangle</h1><p>Write an ordinary question. The atlas identifies likely entries, relevant statements and possible paths, then prepares source-aware context for inspection or copying.</p></header>
      <div class="ask-shell">
        <form id="askForm" class="ask-form"><label for="askQuestion">Your question</label><textarea id="askQuestion" rows="4" placeholder="How does viability relate to autonomy? Why is feedback not the same as homeostasis?"></textarea><button class="primary" type="submit">Search the atlas</button><p class="small">Nothing is sent anywhere automatically. The result stays in the browser unless you choose to copy or discuss it.</p></form>
        <div id="askResults" class="ask-results"><div class="empty-card"><h2>Ask in your own words</h2><p>The atlas will match maintained entries, show relevant connections and prepare source-aware context.</p></div></div>
      </div>
    </section>'''

INTAKE_PANEL = '''        <article class="plain-panel wide proposal-intake-panel">
          <p class="eyebrow">Public proposals, human review</p>
          <h2>How contributions enter the atlas</h2>
          <p>The form prepares a public GitHub issue labelled <code>site-submission</code> and <code>awaiting-curator-review</code>. Research issues and pull requests are also valid routes. No proposal changes the atlas automatically.</p>
          <p>Before publication, proposed material is checked for evidence, identity, duplicate entries, wording, rights, public safety and compatibility with the data model.</p>
          <div class="button-row wrap"><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/issues?q=is%3Aissue+is%3Aopen+label%3Asite-submission" target="_blank" rel="noopener">View the proposal queue</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/contribution-intake.md" target="_blank" rel="noopener">Read the intake rule</a></div>
        </article>'''

EXPERTISE_PANEL = '''        <article class="plain-panel wide expertise-callout">
          <p class="eyebrow">People, works and practice</p>
          <h2>Expertise-led development</h2>
          <p><a href="#view=item&id=person_ivo_velitchkov&from=about">Ivo Velitchkov</a> connects viable organisation, <em>Essential Balances</em>, requisite inefficiency, enterprise architecture and explicit semantic graphs. <a href="#view=item&id=person_patrick_hoverstadt&from=about">Patrick Hoverstadt</a> connects the Viable System Model, systems laws, organisation diagnosis and design, <em>Patterns of Strategy</em> and transformation.</p>
          <p>This release also develops Peter Checkland, Werner Ulrich, Ray Ison, Ed Straw, Raul Espejo, Alfonso Reyes, Donella Meadows, Diana Wright and Barry Oshry through public primary or official sources, distinct method entries and typed practice relations.</p>
          <p><a href="#view=journeys&id=journey_inquiry_governance_and_intervention&step=0">Follow inquiry, governance and intervention</a>, <a href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/expertise-additions.md" target="_blank" rel="noopener">inspect the additions</a>, or <a href="#view=ai-observations">open the current AI observations</a>.</p>
        </article>'''

ACKNOWLEDGEMENTS = '''# Acknowledgements

## Curatorship

The Necessary Tangle is curated by [Benjamin P Taylor](https://www.antlerboy.com/). Curatorship means responsibility for boundary choices, relation wording, source standards and publication decisions. It does not imply sole creation of the knowledge represented here.

## Systems practice and professional lineages

The project develops the connected approach of the original SCiO Systems Thinking Body of Knowledge and later competency work. David Ing's emphasis on the constellation of influences around practitioners helped shape the human-lineage layer. Tony Korycki and other SysBoK contributors helped establish the ambition to connect concepts, antecedents, dependent ideas, people and practice.

Ivo Velitchkov's work contributes management cybernetics, viable organisation, *Essential Balances*, requisite inefficiency, enterprise architecture and explicit semantic graphs. Patrick Hoverstadt's work contributes the Viable System Model, systems laws, organisational diagnosis and design, *The Grammar of Systems*, *The Fractal Organization*, *Patterns of Strategy* and transformation practice. Lucy Loh's co-development of *Patterns of Strategy* is represented explicitly.

Peter Checkland, Werner Ulrich, Ray Ison, Ed Straw, Raul Espejo, Alfonso Reyes, Donella Meadows, Diana Wright and Barry Oshry provide further practice-facing routes through inquiry, boundary critique, systemic governance, organisational cybernetics, feedback, intervention and whole-system relations. The authors, editors, teachers and practitioners cited throughout remain responsible for their own work; the atlas's summaries and connections remain open to correction and argument.

## Comparators, maps and archives

Igor Perko's researchers-network work provides a substantial comparator for mapping people and intellectual lineages. Brian Castellani's maps of the complexity sciences and other published maps provide material and challenge. Principia Cybernetica, the Foundational Papers in Complexity Science collection, Monoskop, SysCoI, model.report and professional-body resource guides are treated as distinct sources with different evidential limits.

## Sources, rights and responsibility

Public statements are supported by public sources or complete public bibliographic citations. Private material may identify leads but is not itself published as evidence. Original atlas text, public data and editorial material are licensed under CC BY-SA 4.0 unless otherwise marked; original software uses the MIT licence. Third-party works remain under their own terms.

Benjamin P Taylor remains responsible for the material accepted into each public release. Corrections and rival interpretations belong in the public contribution routes.
'''


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def remove_internal_routes(text: str) -> str:
    text = re.sub(
        r'<a\b(?=[^>]*(?:data-curator-dot|curator-notebook-link|curator-secret-dot|discreet-note-link))[^>]*>.*?</a>',
        '',
        text,
        flags=re.I | re.S,
    )
    text = re.sub(r'<a\b[^>]*href=["\']\s*["\'][^>]*>\s*</a>', '', text, flags=re.I | re.S)
    return text


def refresh_ai_observations() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    report = make_observations(graph_metrics(data), data)
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
    text = remove_internal_routes(text)
    text, count = re.subn(
        r'\s*<section class="start-small-section".*?</section>',
        "\n\n" + START_SECTION,
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise RuntimeError("Could not replace the start-small section")
    text, count = re.subn(
        r'\s*<section id="view-ask" class="view">.*?</section>\s*\n\s*<section id="view-contribute"',
        "\n\n" + ASK_SECTION + '\n\n    <section id="view-contribute"',
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise RuntimeError("Could not replace the Ask view")
    # Older release patchers may recreate their panels on every build. Remove all
    # old and current variants, then insert exactly one durable 0.13 panel.
    text = re.sub(
        r'\s*<article class="plain-panel wide (?:contribution-intake-panel|proposal-intake-panel)">.*?</article>',
        '',
        text,
        flags=re.S,
    )
    form_marker = '<form id="contributionForm" class="contribution-form">'
    if form_marker not in text:
        raise RuntimeError("Could not locate the contribution form")
    text = text.replace(form_marker, INTAKE_PANEL + "\n" + form_marker, 1)

    text = re.sub(
        r'\s*<article class="plain-panel wide (?:feedback-people-callout|expertise-callout)">.*?</article>',
        '',
        text,
        flags=re.S,
    )
    origin_marker = '<article class="plain-panel wide"><h2>A practitioner-centred origin</h2>'
    if origin_marker not in text:
        raise RuntimeError("Could not locate the practitioner-centred origin panel")
    text = text.replace(origin_marker, EXPERTISE_PANEL + "\n\n        " + origin_marker, 1)
    text = re.sub(
        r'<p>[^<]*tools have assisted research organisation, data processing and software prototyping.*?</p>',
        '',
        text,
        flags=re.I | re.S,
    )
    text = text.replace(
        '<p class="eyebrow">Machine-assisted second-order observation</p>',
        '<p class="eyebrow">Second-order observation</p>',
    )
    text = text.replace(
        'What becomes visible when a language model reads the public graph as data, interface and editorial argument. Counts are reproducible. Interpretations are proposals for challenge, not autonomous facts.',
        'What becomes visible when the public graph is analysed as data, interface and editorial argument. Counts are reproducible. Interpretations are proposals for challenge, not autonomous facts.',
    )
    text = text.replace(
        "Each observation separates a measurement from an interpretation, an implication and a test. The useful question is not whether ‘AI agrees’, but whether the evidence supports a better next move.",
        "Each observation separates a measurement from an interpretation, an implication and a test. The useful question is whether the evidence supports a better next move.",
    )
    text = text.replace(
        '<h2>Public enough to challenge. Bounded enough not to leak the workshop.</h2>',
        '<h2>Public evidence, bounded release</h2>',
    )
    text = text.replace(
        'The detailed working risk register is no longer part of the public release. The public record shows the controls: public-only payloads, source-level provenance, automated scans, curator-controlled releases, licence boundaries and versioned backups.',
        'The public record shows the controls: public-only payloads, source-level provenance, automated scans, curator-controlled releases, licence boundaries and versioned backups.',
    )
    if any(marker in text for marker in ('data-curator-dot=', 'curator-secret-dot', 'curator-notebook-link', 'discreet-note-link')):
        raise RuntimeError("Obsolete hidden working route remains in the public page")
    if text.count('class="plain-panel wide proposal-intake-panel"') != 1:
        raise RuntimeError("The public page must contain exactly one proposal-intake panel")
    if text.count('class="plain-panel wide expertise-callout"') != 1:
        raise RuntimeError("The public page must contain exactly one expertise panel")
    text = re.sub(r"\n{3,}", "\n\n", text)
    INDEX.write_text(clean(text), encoding="utf-8")


def patch_app() -> None:
    text = APP.read_text(encoding="utf-8")
    action_pattern = re.compile(
        r'      <div class="context-actions">.*?</div>\n      <p class="small">.*?</p>',
        flags=re.S,
    )
    match = action_pattern.search(text)
    if not match:
        raise RuntimeError("Could not locate the question action block")
    button_ids = re.findall(r'<button id="([^"]+)"', match.group(0))
    retired_ids = [button_id for button_id in button_ids if button_id != "copyAskContext"]
    replacement = '''      <div class="context-actions">
        <button id="copyAskContext" class="primary">Copy atlas context</button>
        <a class="button" href="${esc(CONFIG.discussionsUrl || `${CONFIG.repositoryUrl}/discussions`)}" target="_blank" rel="noopener">Discuss the question</a>
      </div>
      <p class="small">The site does not send your question anywhere. You may copy the prepared public context or open a public discussion.</p>'''
    text = action_pattern.sub(replacement, text, count=1)
    for retired_id in retired_ids:
        text = re.sub(
            rf"\n\s*\$\('{re.escape(retired_id)}'\)\.addEventListener\('click', async \(\) => \{{.*?\n\s*\}}\);",
            '',
            text,
            count=1,
            flags=re.S,
        )
    APP.write_text(clean(text), encoding="utf-8")


def patch_config() -> None:
    text = CONFIG.read_text(encoding="utf-8")
    text = re.sub(r'^\s*[A-Za-z0-9_]*chat[A-Za-z0-9_]*Url:.*?\n', '', text, flags=re.M | re.I)
    CONFIG.write_text(clean(text), encoding="utf-8")


def patch_css() -> None:
    text = CSS.read_text(encoding="utf-8")
    text = re.sub(r'^\.curator-secret-dot.*?\n', '', text, flags=re.M)
    text = re.sub(r'^\.curator-notebook-link.*?\n', '', text, flags=re.M)
    text = re.sub(r'^\.discreet-note-link.*?\n', '', text, flags=re.M)
    text = text.replace('.map-minimap-shell, .curator-secret-dot {', '.map-minimap-shell {')
    text = text.replace('.contribution-intake-panel', '.proposal-intake-panel')
    text = text.replace('.feedback-people-callout', '.expertise-callout')
    if any(marker in text for marker in ('curator-secret-dot', 'curator-notebook-link', 'discreet-note-link')):
        raise RuntimeError("Internal-route CSS remains")
    text = re.sub(r"\n{3,}", "\n\n", text)
    CSS.write_text(clean(text), encoding="utf-8")


def patch_repository_prose() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme = re.sub(
        r"^- question-led exploration.*$",
        "- question-led exploration and inspectable, copyable public context;",
        readme,
        count=1,
        flags=re.M,
    )
    readme = readme.replace(
        "Site-generated issues are labelled and reconciled with the running feedback and standing research issues before release; see",
        "Site-generated issues are labelled and reviewed alongside research issues and pull requests before release; see",
    )
    (ROOT / "README.md").write_text(clean(readme), encoding="utf-8")

    (ROOT / "ACKNOWLEDGEMENTS.md").write_text(ACKNOWLEDGEMENTS, encoding="utf-8")

    citation_path = ROOT / "CITATION.cff"
    citation = citation_path.read_text(encoding="utf-8")
    citation = re.sub(r"^version:.*$", "version: 0.13-expertise-observations-alpha", citation, flags=re.M)
    citation = re.sub(r"^date-released:.*$", "date-released: 2026-08-11", citation, flags=re.M)
    citation_path.write_text(clean(citation), encoding="utf-8")

    changelog_path = ROOT / "CHANGELOG.md"
    changelog = changelog_path.read_text(encoding="utf-8")
    if "## 0.13-expertise-observations-alpha" not in changelog:
        entry = """## 0.13-expertise-observations-alpha — 11 August 2026

- Added developed entries for Peter Checkland, Werner Ulrich, Ray Ison, Ed Straw, Raul Espejo, Alfonso Reyes, Donella Meadows, Diana Wright and Barry Oshry, with primary or official public sources.
- Deepened Soft Systems Methodology and Critical Systems Heuristics and added boundary critique, systemic governance, Viplan, leverage points and the Organic Systems Framework.
- Added a guided route through inquiry, governance and intervention and new typed practice relations across the expertise layer.
- Regenerated AI observations from current graph measures as part of the build.
- Expanded Ivo Velitchkov and Patrick Hoverstadt through their work, expertise, publications and practice relations.

"""
        changelog = changelog.replace("# Changelog\n\n", "# Changelog\n\n" + entry, 1)
    neutral_012 = """## 0.12-practitioner-intake-alpha — 10 August 2026

- Added developed entries for Ivo Velitchkov, Patrick Hoverstadt and their principal works, with explicit human, documentary, conceptual and practice relations.
- Distinguished viability from evolutionary fitness and added natural drift as a scoped, contestable theoretical account supported by independent public sources.
- Added developed coverage of *Essential Balances*, requisite inefficiency, *The Grammar of Systems II*, *The Fractal Organisation Manual*, *Patterns of Strategy*, *Critical Systems Thinking: A Practitioner’s Guide*, *Opening the Box*, *Systems Approaches to Making Change* and *Navigating Complexity*.
- Added an explicit semantic contract and documented Nodica as a public graph-visualisation comparator rather than an implementation dependency.
- Added structured proposal intake across labelled site submissions, research issues and pull requests.
- Added a smaller start route and a guided journey from viability through balance and strategy.
- Registered further reading-list, professional-practice and source-mining work without claiming those programmes complete.

"""
    changelog = re.sub(
        r"## 0\.12-practitioner-intake-alpha.*?(?=## 0\.11-visual-map-alpha)",
        neutral_012,
        changelog,
        count=1,
        flags=re.S,
    )
    changelog = changelog.replace(
        "- Reframed Ivo Velitchkov and Patrick Hoverstadt through their work, expertise, publications and practice relations.",
        "- Expanded Ivo Velitchkov and Patrick Hoverstadt through their work, expertise, publications and practice relations.",
    )
    changelog = re.sub(r"^- Removed public links and prose tied to .*?\n", "", changelog, count=1, flags=re.M)
    changelog = re.sub(
        r"^- Moved the curator .*? operational link\.$",
        "- Added a discreet public route for corrections and dialogue.",
        changelog,
        count=1,
        flags=re.M,
    )
    changelog = re.sub(
        r"^- Restored the curator.*$",
        "- Added whole-to-detail map controls and strengthened public contribution routes.",
        changelog,
        count=1,
        flags=re.M,
    )
    changelog_path.write_text(clean(changelog), encoding="utf-8")

    roadmap_path = ROOT / "documentation" / "roadmap.md"
    roadmap_path.write_text(
        """# Roadmap

## Current priorities

- deepen high-traffic bridge concepts with rival definitions, scope conditions and primary sources;
- connect methods and intervention skills to documented cases, teaching and consequences;
- complete item-level audits of the maintained reading list and SCiO curriculum;
- resolve initial-only people before adding interpretive or lineage relations;
- compare prior maps, source corpora and reproducible graph neighbourhoods without treating one partition as natural;
- improve human and institutional histories of teaching, mentoring, collaboration, laboratories and conferences;
- replace discovery-only records with public evidence or complete public bibliographic citations;
- test the smaller starting routes and map with readers unfamiliar with the field;
- publish stable releases with archived data, change summaries and reproducible builds.

## Later

- add a question-led companion grounded in the public release;
- test RDF or JSON-LD export without losing relation meaning, direction, evidence, status or scope;
- establish a wider curatorial group with named review responsibilities;
- compare espoused schools, source corpora and observed neighbourhoods side by side.
""",
        encoding="utf-8",
    )

    expansion = ROOT / "documentation" / "expansion-08.md"
    if expansion.exists():
        expansion_text = expansion.read_text(encoding="utf-8")
        expansion_text = re.sub(
            r"\n## Curator notes\n.*$",
            "\n## Public contribution routes\n\nCorrections, sources and challenges enter through the repository's public issue and pull-request routes. Nothing changes the atlas automatically.\n",
            expansion_text,
            flags=re.S,
        )
        expansion.write_text(clean(expansion_text), encoding="utf-8")

    for legacy in (ROOT / "documentation").glob("public-knowledge-for-*.md"):
        legacy.unlink()


def main() -> None:
    refresh_ai_observations()
    patch_index()
    patch_app()
    patch_config()
    patch_css()
    patch_repository_prose()
    print("Patched 0.13 expertise-led public framing and removed internal working references")


if __name__ == "__main__":
    main()
