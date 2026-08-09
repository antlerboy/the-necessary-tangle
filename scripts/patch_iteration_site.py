#!/usr/bin/env python3
"""Patch the 0.6 public page with the 0.7 collection, map and membership views."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"

COLLECTIONS_SECTION = '''    <section id="view-collections" class="view">
      <header class="page-head"><p class="eyebrow">Corpora, sources and observed structure</p><h1>Collections and neighbourhoods</h1><p>Browse the full first-pass paper inventory, the Principia Cybernetica constellation, high-value public sources and provisional groupings produced from the current graph.</p></header>

      <section class="collection-block">
        <div class="section-head"><div><p class="eyebrow">Current graph</p><h2>Observed neighbourhoods</h2></div><button class="text-button" data-view-link="map">See them on the map</button></div>
        <p>The names below describe modular clusters in the current evidence graph. They are not timeless schools. Change the coverage or the relation rules and the pattern may change.</p>
        <div id="neighbourhoodSummary" class="diagnostic-strip"></div>
        <div id="neighbourhoodCards" class="card-grid three"></div>
      </section>

      <section class="collection-block">
        <div class="section-head"><div><p class="eyebrow">Complete bibliographic first pass</p><h2>Foundational Papers in Complexity Science</h2></div><a class="text-button" href="https://www.foundationalpapersincomplexityscience.org/tables-of-contents" target="_blank" rel="noopener">Official contents</a></div>
        <p>All 89 historical papers in the four-volume 2024 collection are now itemised. These are bibliographic entries. Most still need a substantive summary, original-publication locator and reviewed connections.</p>
        <div class="collection-controls"><label>Volume<select id="paperVolume"><option value="all">All four volumes</option><option value="1">Volume 1</option><option value="2">Volume 2</option><option value="3">Volume 3</option><option value="4">Volume 4</option></select></label><label>Find a paper<input id="paperSearch" autocomplete="off" placeholder="Author, title or year"></label><span id="paperCount" class="results-line"></span></div>
        <div id="paperCards" class="paper-list"></div>
      </section>

      <section class="collection-block">
        <div class="section-head"><div><p class="eyebrow">Connected first pass</p><h2>Principia Cybernetica</h2></div><a class="text-button" href="https://pespmc1.vub.ac.be/" target="_blank" rel="noopener">Official project site</a></div>
        <p>The project, website, dictionary, people and key concepts are represented separately. The wording records Principia's own programme without turning its self-description into independent proof.</p>
        <div id="principiaCards" class="card-grid three"></div>
      </section>

      <section class="collection-block">
        <div class="section-head"><div><p class="eyebrow">Research infrastructure</p><h2>Canonical public source register</h2></div><a class="text-button" href="https://github.com/antlerboy/the-necessary-tangle/issues/12" target="_blank" rel="noopener">Extend the register</a></div>
        <p>'Canonical' here means high-value for a stated task: archive, bibliography, dictionary, institutional corpus or comparator. It does not mean neutral, complete or true by inclusion.</p>
        <div id="canonicalSourceCards" class="source-register"></div>
      </section>
    </section>'''

MEMBERSHIP_SECTION = '''    <section id="view-membership" class="view">
      <header class="page-head"><p class="eyebrow">Participation by agreement</p><h1>Membership and access</h1><p>Apply for a role in the work. No form grants repository access automatically. The curator decides roles and GitHub permissions after reviewing the person, purpose and proposed contribution.</p></header>

      <div class="role-grid">
        <article class="role-card"><p class="eyebrow">Open</p><h2>Reader</h2><p>Use, question and discuss the atlas. No application or repository access is needed.</p></article>
        <article class="role-card"><p class="eyebrow">Open</p><h2>Proposer</h2><p>Submit corrections, sources, missing entries and challenges through public Issues.</p></article>
        <article class="role-card"><p class="eyebrow">By agreement</p><h2>Research contributor</h2><p>Work through a fork and pull request. Direct write access is not required.</p></article>
        <article class="role-card"><p class="eyebrow">By invitation</p><h2>Reviewer</h2><p>Examine source support, wording, boundaries and uncertainty, then advise the curator.</p></article>
        <article class="role-card"><p class="eyebrow">Exceptional</p><h2>Maintainer</h2><p>Trusted technical or data maintenance with limited repository write access.</p></article>
        <article class="role-card curator"><p class="eyebrow">Accountable role</p><h2>Curator</h2><p>Benjamin P Taylor holds final responsibility for roles, merges, releases and the public account.</p></article>
      </div>

      <div class="membership-layout">
        <form id="membershipForm" class="membership-form">
          <h2>Apply</h2>
          <label>Your name<input name="name" id="membershipName" required></label>
          <label>GitHub username<input name="github" id="membershipGithub" required placeholder="without @"></label>
          <label>Role requested<select name="role" id="membershipRole" required><option value="">Choose one</option><option>Proposer</option><option>Research contributor</option><option>Reviewer</option><option>Maintainer</option></select></label>
          <label>What do you want to contribute?<textarea name="contribution" id="membershipContribution" rows="5" required placeholder="Name the corpus, concept, lineage, technical work or review capacity."></textarea></label>
          <label>How will you check evidence, scope and uncertainty?<textarea name="checks" id="membershipChecks" rows="4" required></textarea></label>
          <label>Public examples or relevant links<input name="examples" id="membershipExamples" type="url" placeholder="https://"></label>
          <label class="checkbox-row"><input type="checkbox" id="membershipUsesAgent" name="uses_agent"> I expect to use an LLM or other automated agent</label>
          <div id="agentFields" class="agent-fields" hidden>
            <label>Tool or model, and what it will do<input name="agent_tool" id="membershipAgentTool"></label>
            <label>Named human sponsor responsible for checking and submitting the work<input name="sponsor" id="membershipSponsor"></label>
          </div>
          <label class="checkbox-row"><input type="checkbox" name="agreement" id="membershipAgreement" required> I accept that public contributions need inspectable sources, disclosed automation, no private material and curator approval.</label>
          <button type="submit" class="primary">Prepare membership application</button>
          <div id="membershipStatus" class="form-status" role="status"></div>
        </form>
        <aside class="plain-panel membership-policy"><h2>What the roles can really do</h2><p>This repository is owned by a personal GitHub account. GitHub supplies only owner and collaborator permissions here; the finer roles above are project roles enforced by process.</p><p>Proposers use Issues. Research contributors normally use forks and pull requests. Maintainer write access is exceptional. Moving the repository to a GitHub organisation would allow enforceable Read, Triage, Write, Maintain and Admin levels.</p><h3>Agents do not become members</h3><p>An LLM or automated tool acts under a named human sponsor. The sponsor discloses the tool, checks the source support and diff, and remains answerable for the submission. No agent receives direct push or auto-merge rights.</p><div class="button-stack"><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/participation-and-access.md" target="_blank" rel="noopener">Participation and access policy</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/AGENTS.md" target="_blank" rel="noopener">Agent contribution protocol</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/issues/10" target="_blank" rel="noopener">Governance issue</a></div></aside>
      </div>
    </section>'''

MAP_CONTROLS = '''        <aside class="map-controls">
          <div class="smart-search" data-search-role="map"><label for="mapSearch">Centre on</label><input id="mapSearch" autocomplete="off" placeholder="Viability"><div class="suggestions" role="listbox" hidden></div></div>
          <label>Layer<select id="mapLayer"><option value="reader">Reader map — substantive public connections</option><option value="provenance">Provenance map — include corpora and documentary links</option><option value="everything">Everything mapped — including outline material</option></select></label>
          <label>View<select id="mapDepth"><option value="1">Immediate connections</option><option value="2">Two steps</option><option value="path">Path and immediate neighbours</option><option value="profiles">All developed entries</option><option value="neighbourhoods">Observed neighbourhoods</option><option value="all">Full selected layer</option></select></label>
          <label>Show connections about<select id="mapFamily"><option value="all">All connection types</option></select></label>
          <label>Labels<select id="mapLabels"><option value="focus">Focus and central entries</option><option value="developed">Developed entries</option><option value="all">Every visible item</option></select></label>
          <label>Colour<select id="mapColour"><option value="type">Entry type</option><option value="neighbourhood">Observed neighbourhood</option></select></label>
          <label class="checkbox-row"><input type="checkbox" id="mapIncludeStubs"> Include outline entries</label>
          <div class="zoom-row" aria-label="Map zoom controls"><button id="mapZoomOut" type="button" aria-label="Zoom out">−</button><button id="mapZoomReset" type="button" aria-label="Reset zoom"><span id="mapZoomLabel">100%</span></button><button id="mapZoomIn" type="button" aria-label="Zoom in">+</button></div>
          <div class="button-row"><button id="mapFit" type="button" class="primary">Fit view</button><button id="mapReset" type="button">Reset map</button></div>
          <p class="small"><strong id="mapCount">0</strong> items and <strong id="mapEdgeCount">0</strong> connections visible. Roll the mouse wheel over the point you want to keep under the pointer; drag the background to pan.</p>
          <div id="mapLegend" class="map-legend"></div>
          <hr>
          <h3>Find a path</h3>
          <div class="smart-search compact" data-search-role="path-from"><label for="pathFrom">From</label><input id="pathFrom" autocomplete="off" placeholder="Boundary"><div class="suggestions" role="listbox" hidden></div></div>
          <div class="smart-search compact" data-search-role="path-to"><label for="pathTo">To</label><input id="pathTo" autocomplete="off" placeholder="Viable System Model"><div class="suggestions" role="listbox" hidden></div></div>
          <button id="findPath" type="button" class="primary full">Find path</button>
          <div id="pathResult" class="path-result"></div>
        </aside>'''


def replace_once(text: str, old: str, new: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Expected marker not found: {old[:80]!r}")
    return text.replace(old, new, 1)


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")

    if 'assets/iteration.css' not in text:
        text = replace_once(
            text,
            '  <link rel="stylesheet" href="assets/site-enhancements.css">',
            '  <link rel="stylesheet" href="assets/site-enhancements.css">\n  <link rel="stylesheet" href="assets/iteration.css">',
        )

    notebook = '    <a class="curator-notebook-link" href="https://github.com/antlerboy/the-necessary-tangle/issues/2" target="_blank" rel="noopener" aria-label="Open the curator\'s running notebook" title="Curator\'s notebook"><span></span></a>\n'
    if 'curator-notebook-link' not in text:
        text = replace_once(text, '  <header class="site-header">\n', '  <header class="site-header">\n' + notebook)

    nav_old = '''    <button data-view="journeys">Guided journeys</button>\n    <button data-view="map">Map</button>'''
    nav_new = '''    <button data-view="journeys">Guided journeys</button>\n    <button data-view="collections">Collections</button>\n    <button data-view="map">Map</button>'''
    text = replace_once(text, nav_old, nav_new)
    nav_old = '''    <button data-view="contribute">Contribute</button>\n    <button data-view="about">About</button>'''
    nav_new = '''    <button data-view="contribute">Contribute</button>\n    <button data-view="membership">Membership</button>\n    <button data-view="about">About</button>'''
    text = replace_once(text, nav_old, nav_new)

    if 'id="view-collections"' not in text:
        text = replace_once(text, '    <section id="view-map" class="view map-view">', COLLECTIONS_SECTION + '\n\n    <section id="view-map" class="view map-view">')

    text = text.replace(
        '<header class="page-head"><p class="eyebrow">Interactive neighbourhoods</p><h1>Map</h1><p>Search for an entry to centre the map. Select an item to refocus. Select a line to inspect the statement, its status and its sources.</p></header>',
        '<header class="page-head"><p class="eyebrow">Reader map, provenance graph and research backlog</p><h1>Map</h1><p>Choose what kind of graph to see. The reader layer privileges substantive public connections; provenance adds corpora and documentary links; everything mapped exposes the untidy research edge.</p></header>',
    )
    text, count = re.subn(r'        <aside class="map-controls">.*?</aside>', MAP_CONTROLS, text, count=1, flags=re.S)
    if count == 0 and MAP_CONTROLS not in text:
        raise RuntimeError("Map controls not found")

    if 'id="view-membership"' not in text:
        text = replace_once(text, '    <section id="view-about" class="view">', MEMBERSHIP_SECTION + '\n\n    <section id="view-about" class="view">')

    text = text.replace(
        '<p class="small">Broad seed coverage, a smaller evidence-deepened core, and an explicit programme for what comes next.</p>',
        '<p class="small">The 89-paper collection is itemised, Principia Cybernetica has a connected first pass, and the graph now reports its own provisional neighbourhoods and large periphery.</p>',
    )
    text = text.replace(
        '<div class="hero-actions"><button class="primary" data-view-link="browse">Explore the atlas</button><button data-view-link="journeys">Follow a guided journey</button><button data-view-link="map">Open the map</button></div>',
        '<div class="hero-actions"><button class="primary" data-view-link="browse">Explore the atlas</button><button data-view-link="collections">Browse collections</button><button data-view-link="map">Open the map</button></div>',
    )
    text = text.replace(
        '<article class="plain-panel"><h2>Current state</h2><p>This is a public alpha. It has broad seed coverage and a smaller evidence-deepened core. The current build reports its entry, source, connection, profile and journey counts on the home page.</p></article>',
        '<article class="plain-panel"><h2>Current state</h2><p>This is a public alpha. Release 0.7 itemises all 89 papers in the named Santa Fe Institute collection, gives Principia Cybernetica a connected first pass, publishes a canonical-source register and exposes provisional graph neighbourhoods.</p></article>',
    )
    text = text.replace(
        '<article class="plain-panel"><h2>Strongest now</h2><p>The deepest connected material is around boundaries and observers; feedback and regulation; variety, viability and the Viable System Model; recursion; emergence; and self-organisation.</p></article>',
        '<article class="plain-panel"><h2>What the graph currently groups</h2><p>The strongest observed neighbourhoods concern feedback, control and learning; recursion, computation and self-reference; viability, variety and organisation; boundaries, information and systemic intervention; and observation, emergence and self-organisation. These groupings are provisional products of the current graph.</p></article>',
    )
    text = text.replace(
        '<article class="plain-panel"><h2>Most incomplete</h2><p>Complexity needs a fuller treatment on its own terms. Human and institutional lineage, teaching, supervision, collaboration, laboratories, conferences and practice transmission remain thin. Many entries still offer orientation rather than a full research profile.</p></article>',
        '<article class="plain-panel"><h2>What the graph exposes</h2><p>Most non-publication entries remain isolated or weakly connected. That is not a discovery of hundreds of separate schools. It is a visible research backlog: missing evidence, missing relation typing and uneven corpus coverage.</p></article>',
    )

    coverage_marker = '''          <a class="coverage-card" href="https://github.com/antlerboy/the-necessary-tangle/issues/8" target="_blank" rel="noopener"><strong>Company knowledge discovery</strong><span>Use private knowledge only to find leads; replace it with public evidence or a proper ‘No public link’ citation.</span></a>'''
    coverage_add = coverage_marker + '''\n          <a class="coverage-card" href="https://github.com/antlerboy/the-necessary-tangle/issues/10" target="_blank" rel="noopener"><strong>Membership and agent contributions</strong><span>Curator-approved roles, named human responsibility and no automatic rights.</span></a>\n          <a class="coverage-card" href="https://github.com/antlerboy/the-necessary-tangle/issues/11" target="_blank" rel="noopener"><strong>Map and observed neighbourhoods</strong><span>Richer layers, usable zoom and a public account of graph structure and isolation.</span></a>\n          <a class="coverage-card" href="https://github.com/antlerboy/the-necessary-tangle/issues/12" target="_blank" rel="noopener"><strong>Principia and canonical sources</strong><span>Connected project mapping and a maintained source register with stated limits.</span></a>'''
    if 'Membership and agent contributions' not in text:
        text = replace_once(text, coverage_marker, coverage_add)

    footer_membership = '<button data-view-link="membership" class="text-button">Membership</button>'
    if footer_membership not in text.split('<footer class="site-footer">', 1)[-1]:
        text = text.replace(
            '<button data-view-link="about" class="text-button">Coverage, method and rights</button>',
            footer_membership + '<button data-view-link="about" class="text-button">Coverage, method and rights</button>',
            1,
        )

    INDEX.write_text(text, encoding="utf-8")
    print("Patched docs/index.html for 0.7 collections, membership and map controls")


if __name__ == "__main__":
    main()
