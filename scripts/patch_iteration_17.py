#!/usr/bin/env python3
"""Patch the public reader, workflows and release prose for 0.17."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
ASSETS = ROOT / "docs" / "assets"
DATA_PATH = ROOT / "data" / "public-data.json"
RELEASE = "0.17-public-intake-lineage-alpha"
GENERATED = "2026-08-19"
VERSION = "0.17.0-public"
PUBLIC_URL = "https://transduction.systems/"


def clean(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.rstrip().splitlines()) + "\n"


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(clean(value), encoding="utf-8")


def escape(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def patch_index(data: dict) -> None:
    text = INDEX.read_text(encoding="utf-8")
    text = re.sub(r'assets/styles\.css(?:\?v=[^"\']+)?', f"assets/styles.css?v={VERSION}", text, count=1)
    text = re.sub(r'assets/site-enhancements\.css(?:\?v=[^"\']+)?', f"assets/site-enhancements.css?v={VERSION}", text, count=1)
    text = re.sub(r'assets/app\.js(?:\?v=[^"\']+)?', f"assets/app.js?v={VERSION}", text, count=1)

    extra_css = f'  <link rel="stylesheet" href="assets/iteration-17.css?v={VERSION}">'
    if "assets/iteration-17.css" not in text:
        marker = f'  <link rel="stylesheet" href="assets/site-enhancements.css?v={VERSION}">'
        if marker not in text:
            raise RuntimeError("site-enhancements stylesheet marker not found")
        text = text.replace(marker, marker + "\n" + extra_css, 1)

    if 'href="/submissions/"' not in text.split("</nav>", 1)[0]:
        marker = '    <a href="#view=contribute" data-view="contribute">Contribute</a>'
        addition = marker + '\n    <a href="/submissions/" class="static-nav-link">Submissions</a>\n    <button type="button" id="surpriseMeNav" class="surprise-nav">Surprise me</button>'
        if marker not in text:
            raise RuntimeError("main navigation contribution marker not found")
        text = text.replace(marker, addition, 1)

    hero_marker = '<a href="#view=map&layer=all&depth=all" class="button" data-view-link="map" data-map-mode="all">Full public map</a>'
    hero_addition = hero_marker + '<button type="button" id="surpriseMeHero" class="button surprise-me">Surprise me</button><a href="/canon-and-lineage/" class="button">Who gets to count?</a>'
    if 'id="surpriseMeHero"' not in text:
        if hero_marker not in text:
            raise RuntimeError("hero action marker not found")
        text = text.replace(hero_marker, hero_addition, 1)

    old_queue = '<a class="button" href="https://github.com/antlerboy/the-necessary-tangle/issues?q=is%3Aissue+is%3Aopen+label%3Asite-submission" target="_blank" rel="noopener">View the proposal queue</a>'
    new_queue = '<a class="button primary" href="/submissions/">Public submissions and responses</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/issues?q=is%3Aissue+%22Prepared+from+The+Necessary+Tangle%22+sort%3Acreated-desc" target="_blank" rel="noopener">Canonical GitHub record</a>'
    if old_queue in text:
        text = text.replace(old_queue, new_queue, 1)
    elif "/submissions/" not in text:
        raise RuntimeError("proposal queue marker not found")

    canon_panel = '''
        <article class="plain-panel wide canon-lineage-panel">
          <p class="eyebrow">The map is also a confession</p>
          <h2>Canon, lineage and who gets to count</h2>
          <p>A field needs distinctions and boundaries. It does not need to pretend those boundaries arrived from nowhere. This release distinguishes coherence from impermeability and demographic inclusion from the harder work of changing who can affect categories, evidence and intellectual lineage.</p>
          <p>Ethnicity, heritage, religion, gender and nationality are never inferred from names, portraits or geography. Relevant intellectual, institutional, linguistic, geographical and self-described identity context is recorded only with public evidence and a reason for including it.</p>
          <p><a class="button primary" href="/canon-and-lineage/">Open the canon and lineage review</a> <a class="button" href="#view=journeys&id=journey_who_counts_as_a_systems_thinker&step=0">Follow the guided route</a> <a class="button" href="#view=item&id=concept_canon_formation&from=about">Open canon formation</a></p>
        </article>'''
    if "canon-lineage-panel" not in text:
        marker = '<article class="plain-panel wide"><h2>A practitioner-centred origin</h2>'
        at = text.find(marker)
        if at < 0:
            raise RuntimeError("practitioner-centred origin marker not found")
        text = text[:at] + canon_panel + "\n\n        " + text[at:]

    footer_marker = '<a href="#view=contribute" data-view-link="contribute" class="text-button">Submit a correction</a>'
    if 'class="text-button" href="/submissions/"' not in text:
        footer_addition = footer_marker + '<a class="text-button" href="/submissions/">Public submissions</a><button type="button" class="text-button surprise-me footer-surprise">Surprise me</button>'
        if footer_marker not in text:
            raise RuntimeError("footer contribution marker not found")
        text = text.replace(footer_marker, footer_addition, 1)

    extra_script = f'  <script src="assets/iteration-17.js?v={VERSION}"></script>'
    if "assets/iteration-17.js" not in text:
        if "</body>" not in text:
            raise RuntimeError("body closing tag not found")
        text = text.replace("</body>", extra_script + "\n</body>", 1)

    INDEX.write_text(clean(text), encoding="utf-8")


def write_surprise_assets() -> None:
    js = r"""(() => {
  'use strict';
  const DATA = window.TANGLE_DATA || {};
  const redirects = DATA.canonical_redirects || {};
  const canonical = (id) => redirects[id] || id;
  const excludedTypes = new Set(['corpus', 'source', 'evidence', 'claim']);

  function eligible() {
    return (DATA.nodes || []).filter((node) =>
      node.public_visibility === 'public'
      && canonical(node.id) === node.id
      && node.status === 'accepted'
      && ['profile', 'described'].includes(node.publication_level)
      && !excludedTypes.has(node.entity_type)
      && String(node.description || node.canonical_definition || '').trim().length >= 80
    );
  }

  function currentId() {
    const params = new URLSearchParams(window.location.hash.replace(/^#/, ''));
    return params.get('id') || '';
  }

  function randomIndex(length) {
    if (length < 2) return 0;
    if (window.crypto && window.crypto.getRandomValues) {
      const values = new Uint32Array(1);
      window.crypto.getRandomValues(values);
      return values[0] % length;
    }
    return Math.floor(Math.random() * length);
  }

  function surprise() {
    const pool = eligible();
    if (!pool.length) return;
    const current = currentId();
    const alternatives = pool.filter((node) => node.id !== current);
    const choicePool = alternatives.length ? alternatives : pool;
    const node = choicePool[randomIndex(choicePool.length)];
    window.location.hash = `view=item&id=${encodeURIComponent(node.id)}&from=surprise`;
  }

  function attach() {
    document.querySelectorAll('#surpriseMeNav, #surpriseMeHero, .surprise-me').forEach((button) => {
      if (button.dataset.surpriseReady === 'true') return;
      button.dataset.surpriseReady = 'true';
      button.addEventListener('click', surprise);
    });
  }

  document.addEventListener('DOMContentLoaded', attach);
  window.addEventListener('hashchange', attach);
  attach();
})();
"""
    css = r"""/* 0.17 public intake, canon and serendipity */
.main-nav .surprise-nav,
.main-nav .static-nav-link {
  align-self: stretch;
}

.main-nav .surprise-nav {
  appearance: none;
  border: 0;
  border-left: 1px solid var(--line, #d6d0cb);
  border-radius: 0;
  background: transparent;
  color: inherit;
  font: inherit;
  padding: 0.78rem 1rem;
  cursor: pointer;
}

.main-nav .surprise-nav:hover,
.main-nav .surprise-nav:focus-visible {
  background: color-mix(in srgb, currentColor 8%, transparent);
}

.hero-actions button.button,
.footer-surprise {
  font: inherit;
  cursor: pointer;
}

.site-footer .footer-surprise {
  border: 0;
  background: none;
  padding: 0;
}

.canon-lineage-panel {
  border-left: 0.35rem solid var(--accent, #9f161b);
}

.standalone-shell {
  width: min(1120px, calc(100% - 2rem));
  margin: 0 auto;
  padding: 2.5rem 0 5rem;
}

.standalone-head {
  display: grid;
  gap: 1rem;
  margin-bottom: 2rem;
}

.standalone-actions,
.submission-links,
.status-key {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem;
  align-items: center;
}

.submission-grid,
.canon-review-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 290px), 1fr));
  gap: 1rem;
}

.submission-card,
.canon-review-card {
  border: 1px solid var(--line, #d6d0cb);
  border-radius: 0.75rem;
  padding: 1.1rem;
  background: var(--panel, #fff);
}

.submission-card h2,
.canon-review-card h2 {
  margin-top: 0.35rem;
}

.submission-status {
  display: inline-flex;
  border: 1px solid currentColor;
  border-radius: 999px;
  padding: 0.18rem 0.55rem;
  font-size: 0.82rem;
  font-weight: 700;
}

.submission-status.incorporated { color: #24643b; }
.submission-status.awaiting-review { color: #8a5a00; }
.submission-status.investigating { color: #355f8a; }
.submission-status.disputed { color: #843d73; }
.submission-status.deferred,
.submission-status.declined { color: #6a5757; }

.projection-note,
.live-status {
  font-size: 0.92rem;
  color: var(--muted, #665f59);
}

.canon-policy {
  max-width: 82ch;
}

.review-status {
  font-weight: 700;
}

@media (max-width: 820px) {
  .main-nav .surprise-nav {
    border-left: 0;
    border-top: 1px solid var(--line, #d6d0cb);
    width: 100%;
    text-align: left;
  }
}
"""
    write(ASSETS / "iteration-17.js", js)
    write(ASSETS / "iteration-17.css", css)


def submission_cards(items: list[dict]) -> str:
    cards = []
    for item in items:
        links = "".join(
            f'<a class="button" href="{escape(link.get("url"))}">{escape(link.get("label"))}</a>'
            for link in item.get("result_links", [])
        )
        status_class = str(item.get("status", "awaiting review")).replace(" ", "-")
        cards.append(f'''<article class="submission-card" data-issue="{escape(item.get('issue_number'))}">
          <span class="submission-status {escape(status_class)}">{escape(item.get('status'))}</span>
          <h2>{escape(item.get('title'))}</h2>
          <p class="small">{escape(item.get('contributor'))} · {escape(item.get('created_at'))}</p>
          <h3>Proposal</h3><p>{escape(item.get('proposal'))}</p>
          <h3>Curator response</h3><p>{escape(item.get('curator_response'))}</p>
          <div class="submission-links"><a class="button primary" href="{escape(item.get('issue_url'))}" target="_blank" rel="noopener">Full public discussion</a>{links}</div>
        </article>''')
    return "\n".join(cards)


def write_submissions_page(data: dict) -> None:
    projection = data["site_submissions"]
    cards = submission_cards(projection.get("items", []))
    fallback_json = json.dumps(projection, ensure_ascii=False).replace("</", "<\\/")
    page = f'''<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Public submissions, curator responses and resulting changes to The Necessary Tangle.">
  <link rel="canonical" href="{PUBLIC_URL}submissions/">
  <title>Submissions and responses — The Necessary Tangle</title>
  <link rel="stylesheet" href="../assets/styles.css?v={VERSION}">
  <link rel="stylesheet" href="../assets/site-enhancements.css?v={VERSION}">
  <link rel="stylesheet" href="../assets/iteration-17.css?v={VERSION}">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header"><a class="brand" href="../#view=home"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span><strong>The Necessary Tangle</strong><small>A living evidence atlas of systems | cybernetics | complexity</small></span></a><div class="header-meta"><span>Public submissions</span><span>Curated by <a href="https://www.antlerboy.com/">Benjamin P Taylor</a></span></div></header>
  <main id="main" class="standalone-shell">
    <header class="standalone-head">
      <p class="eyebrow">Public proposals, public responses</p>
      <h1>Submissions and responses</h1>
      <p class="lede">The website prepares GitHub issues. GitHub remains the canonical public record: proposal, discussion, curator response, status and any resulting atlas entries stay together.</p>
      <p class="projection-note">This page first shows the release snapshot from {escape(projection.get('generated'))}, then tries to refresh from GitHub. A failed refresh does not hide the published record.</p>
      <div class="standalone-actions"><a class="button primary" href="../#view=contribute">Make a contribution</a><a class="button" href="{escape(projection.get('canonical_query_url'))}" target="_blank" rel="noopener">Open the live GitHub register</a><a class="button" href="../#view=home">Back to the atlas</a></div>
      <p id="liveStatus" class="live-status" aria-live="polite">Showing the release snapshot.</p>
    </header>
    <div id="submissionList" class="submission-grid">{cards}</div>
    <section class="plain-panel wide"><h2>Status means a curatorial decision</h2><p>‘Awaiting review’ is not tacit rejection. ‘Incorporated’ does not mean the submitted wording became evidence. Proposals may be investigated, partly incorporated, disputed, deferred or declined, with the reason kept visible.</p><div class="status-key"><span class="submission-status awaiting-review">awaiting review</span><span class="submission-status investigating">investigating</span><span class="submission-status incorporated">incorporated</span><span class="submission-status disputed">disputed</span><span class="submission-status deferred">deferred</span><span class="submission-status declined">declined</span></div></section>
  </main>
  <script id="submissionFallback" type="application/json">{fallback_json}</script>
  <script>
  (() => {{
    'use strict';
    const owner = 'antlerboy';
    const repo = 'the-necessary-tangle';
    const marker = 'Prepared from The Necessary Tangle';
    const list = document.getElementById('submissionList');
    const liveStatus = document.getElementById('liveStatus');
    const fallback = JSON.parse(document.getElementById('submissionFallback').textContent);
    const esc = (value) => String(value || '').replace(/[&<>"']/g, (ch) => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[ch]));
    const section = (body, heading) => {{
      const pattern = new RegExp(`## ${{heading}}\\s*\\n([\\s\\S]*?)(?=\\n## |\\n---|$)`, 'i');
      return (body.match(pattern)?.[1] || '').trim();
    }};
    const status = (issue, comments) => {{
      const labels = (issue.labels || []).map((item) => typeof item === 'string' ? item : item.name);
      const order = ['incorporated','partly-incorporated','disputed','declined','deferred','investigating','awaiting-curator-review'];
      const found = order.find((name) => labels.includes(name));
      if (found) return found.replaceAll('-', ' ').replace('awaiting curator review', 'awaiting review');
      const combined = comments.map((comment) => comment.body || '').join(' ').toLowerCase();
      if (combined.includes('incorporated in release')) return 'incorporated';
      return issue.state === 'open' ? 'awaiting review' : 'deferred';
    }};
    const render = (items) => {{
      list.innerHTML = items.map((item) => {{
        const cls = item.status.replaceAll(' ', '-');
        const resultLinks = (item.result_links || []).map((link) => `<a class="button" href="${{esc(link.url)}}">${{esc(link.label)}}</a>`).join('');
        return `<article class="submission-card"><span class="submission-status ${{esc(cls)}}">${{esc(item.status)}}</span><h2>${{esc(item.title)}}</h2><p class="small">${{esc(item.contributor)}} · ${{esc(item.created_at)}}</p><h3>Proposal</h3><p>${{esc(item.proposal)}}</p><h3>Curator response</h3><p>${{esc(item.curator_response || 'No public curator response yet.')}}</p><div class="submission-links"><a class="button primary" href="${{esc(item.issue_url)}}" target="_blank" rel="noopener">Full public discussion</a>${{resultLinks}}</div></article>`;
      }}).join('');
    }};
    async function refresh() {{
      const query = encodeURIComponent(`repo:${{owner}}/${{repo}} in:body "${{marker}}" is:issue`);
      const response = await fetch(`https://api.github.com/search/issues?q=${{query}}&sort=created&order=desc&per_page=100`, {{headers: {{Accept: 'application/vnd.github+json'}}}});
      if (!response.ok) throw new Error(`GitHub returned ${{response.status}}`);
      const payload = await response.json();
      const fallbackByIssue = new Map((fallback.items || []).map((item) => [Number(item.issue_number), item]));
      const live = await Promise.all((payload.items || []).map(async (issue) => {{
        const commentsResponse = await fetch(issue.comments_url, {{headers: {{Accept: 'application/vnd.github+json'}}}});
        const comments = commentsResponse.ok ? await commentsResponse.json() : [];
        const curator = [...comments].reverse().find((comment) => comment.user?.login === owner);
        const prior = fallbackByIssue.get(Number(issue.number)) || {{}};
        return {{
          issue_number: issue.number,
          title: issue.title,
          contributor: `${{issue.user?.login || 'GitHub contributor'}}`,
          created_at: String(issue.created_at || '').slice(0, 10),
          status: status(issue, comments),
          proposal: section(issue.body || '', 'Proposed change, challenge or question') || prior.proposal || section(issue.body || '', 'Why this matters') || 'Open the issue for the full proposal.',
          curator_response: curator?.body || prior.curator_response || '',
          issue_url: issue.html_url,
          result_links: prior.result_links || []
        }};
      }}));
      render(live.length ? live : fallback.items || []);
      liveStatus.textContent = `Live GitHub register refreshed: ${{live.length}} submission${{live.length === 1 ? '' : 's'}}.`;
    }}
    refresh().catch((error) => {{
      liveStatus.textContent = `Live refresh unavailable; showing the release snapshot. ${{error.message}}.`;
    }});
  }})();
  </script>
</body>
</html>'''
    write(ROOT / "docs" / "submissions" / "index.html", page)


def write_canon_page(data: dict) -> None:
    review = data["canon_visibility_review"]
    cards = []
    for item in review.get("items", []):
        node_id = item.get("node_id")
        title = escape(item.get("name"))
        if node_id:
            title = f'<a href="../#view=item&id={escape(node_id)}&from=canon-review">{title}</a>'
        cards.append(f'''<article class="canon-review-card"><p class="eyebrow review-status">{escape(item.get('status'))}</p><h2>{title}</h2><p>{escape(item.get('next_work'))}</p></article>''')
    page = f'''<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="How The Necessary Tangle handles canon formation, lineage, identity, exclusion and recovery.">
  <link rel="canonical" href="{PUBLIC_URL}canon-and-lineage/">
  <title>Canon and lineage — The Necessary Tangle</title>
  <link rel="stylesheet" href="../assets/styles.css?v={VERSION}">
  <link rel="stylesheet" href="../assets/site-enhancements.css?v={VERSION}">
  <link rel="stylesheet" href="../assets/iteration-17.css?v={VERSION}">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header"><a class="brand" href="../#view=home"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span><strong>The Necessary Tangle</strong><small>A living evidence atlas of systems | cybernetics | complexity</small></span></a><div class="header-meta"><span>Canon and lineage</span><span>Curated by <a href="https://www.antlerboy.com/">Benjamin P Taylor</a></span></div></header>
  <main id="main" class="standalone-shell">
    <header class="standalone-head canon-policy">
      <p class="eyebrow">The map is also a confession</p>
      <h1>Who gets to count as a systems thinker?</h1>
      <p class="lede">The familiar centre of systems | cybernetics | complexity reflects real intellectual history. It also reflects publication, institutions, language, teaching, access, repetition and this curator's choices. Those are part of the system being mapped.</p>
      <p>{escape(review.get('policy'))}</p>
      <div class="standalone-actions"><a class="button primary" href="../#view=journeys&id=journey_who_counts_as_a_systems_thinker&step=0">Follow the guided journey</a><a class="button" href="../#view=item&id=concept_canon_formation&from=canon-page">Canon formation</a><a class="button" href="../#view=item&id=concept_epistemic_closure&from=canon-page">Epistemic closure</a><a class="button" href="../#view=home">Back to the atlas</a></div>
    </header>
    <section class="plain-panel wide"><h2>What changes in the map</h2><p>The relation vocabulary now has places for canonisation, exclusion, appropriation and recovery. Those lines will appear only when evidence supports the particular history. The absence of a line is preferable to a righteous invention.</p><p>Openness is not treated as the automatic cure. Jo Freeman's critique of structurelessness is kept alongside epistemic closure: invisible boundaries and informal authority can be harder to challenge than explicit, revisable ones.</p></section>
    <section><div class="section-head"><div><p class="eyebrow">A visible research queue</p><h2>People named in the current challenge</h2><p>These are not a replacement canon. They are a check on what the present map makes easy or difficult to see.</p></div></div><div class="canon-review-grid">{''.join(cards)}</div></section>
    <section class="plain-panel wide"><h2>The test</h2><p>Not ‘does the map contain a varied row of faces?’ Ask: who can change the boundary; which experiences can perturb it; what counts as evidence; which transmissions are typed; and can the map show how its own categories were made?</p><p><a href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/canon-lineage-and-identity.md" target="_blank" rel="noopener">Read the maintained editorial rule and work programme →</a></p></section>
  </main>
</body>
</html>'''
    write(ROOT / "docs" / "canon-and-lineage" / "index.html", page)


def write_documentation(data: dict) -> None:
    site_doc = f'''# Public submissions and responses

The public page is <https://transduction.systems/submissions/>.

GitHub Issues remains the canonical record. The page is a generated and live-refreshed projection so that a reader can see proposals, statuses, curator responses and resulting entries without knowing GitHub's interface.

## Intake rule

A website submission creates a public issue containing the marker `Prepared from The Necessary Tangle`. Nothing changes the atlas automatically. The curator checks identity, duplication, wording, evidence, rights, public safety and compatibility with the data model.

## Status vocabulary

- awaiting review;
- investigating;
- incorporated;
- partly incorporated;
- disputed;
- deferred;
- declined.

A closed issue is not silently presented as accepted. A contribution which originates a useful change remains attributed even where its wording is not used as evidence.

## Reference implementation

Issue 21 proposed a distinction between viability, fitness and natural drift. Release 0.12 incorporated the underlying distinction after checking independent sources. Release 0.17 surfaces the proposal, public response and resulting entries on the website.

## Automation

The triage workflow creates and maintains the `site-submission` and status labels. The public page also reads the GitHub API at view time, with the numbered-release snapshot as a fallback. This avoids a second editorial database while retaining a usable public page.
'''
    canon_doc = '''# Canon, lineage, identity and visibility

The Necessary Tangle is a map and an intervention in the field it maps. Its centre reflects documented intellectual history, but also institutional visibility, publication, language, teaching, access, repetition and curatorial choice.

## Editorial rule

Record intellectual, institutional, geographical, linguistic and self-described identity context only when:

1. it is publicly sourced;
2. it helps explain the work, its reception or its exclusion;
3. the wording does not infer a sensitive characteristic from a name, portrait, location or presumed group membership;
4. it is distinguished from evidence of authorship, teaching, collaboration, influence or conceptual dependence.

Do not use demographic variety as a substitute for changing the knowledge structure.

## Closure and power

Epistemological closure is not inherently patriarchal. A knowledge system needs distinctions about questions, evidence, categories and relevance. The political questions are who can affect those distinctions, which experiences can perturb the system, who receives credibility, and whether the system can revise its own categories.

Indiscriminate openness is not an automatic cure. Jo Freeman's critique of structurelessness shows that removing formal structure can leave informal power more obscure and less accountable. The design aim is explicit, challengeable and revisable closure.

## Relation types

Release 0.17 registers relation types for:

- `canonised_as`;
- `excluded_from_canon`;
- `appropriated_from`;
- `recovers`;
- `participates_in_canon_formation`.

Registering a relation type does not assert any particular line. Each edge needs evidence appropriate to the exact history.

## Canon and recovery relations

Release 0.17 makes canon formation and recovery inspectable through typed, source-bearing relations: `canonised_as`, `excluded_from_canon`, `appropriated_from`, `recovers`, `participates_in_canon_formation` and `can_exclude`. These lines remain challengeable statements about particular histories; they are not demographic inference or a new fixed canon.

## Current developed route

The first route connects Magnus Ramage, Karen Shipp and *Systems Thinkers* to canon formation; Michael C. Jackson to critical systems thinking and methodological pluralism; Miranda Fricker to epistemic injustice; Jo Freeman to the critique of structurelessness; and systems-lineage documentation to evidence-led recovery.

## Work queue

The public canon review names influences and practitioners whose treatment should be checked, including Allenna Leonard, Angela Espinosa, Nora Bateson, Sandra Janoff, Christine Oliver, Diane Bowling, Isabel Menzies Lyth, Mary Douglas, Elaine Brown, Harish Jose, Taiichi Ohno and Chögyam Trungpa. This is a visibility audit, not a replacement canon. The next step for each is source-backed intellectual and practice context, not a decorative portrait.
'''
    write(ROOT / "documentation" / "site-submissions.md", site_doc)
    write(ROOT / "documentation" / "canon-lineage-and-identity.md", canon_doc)

    company = ROOT / "documentation" / "company-knowledge-discovery-first-pass.md"
    text = company.read_text(encoding="utf-8")
    heading = "## Second bounded pass — 19 August 2026"
    if heading not in text:
        text += f'''

{heading}

A second connected search reviewed the named systems-thinking area and wider company knowledge for books, articles, teaching materials and bibliographic leads. The search returned overlapping versions and working documents rather than a stable catalogue, so it does not justify a claim that every internal file has been exhausted.

The pass strengthened the public replacement queue around:

- the Open University lineage, Magnus Ramage, Karen Shipp and *Systems Thinkers*;
- Michael C. Jackson, critical systems thinking and the Hull programme;
- systems education, competency and apprenticeship material;
- systems-change reading collections and teaching bibliographies;
- metacontextuality, Bongard problems, power, viable organisation, intervention and public-service practice.

Release 0.17 converts the first two groups into public source-backed entries and connections. The remaining groups stay in the public replacement queue. No private URL, internal extract, client material or confidential document has entered the public dataset.

The honest completion statement is therefore: the second pass is complete as a discovery action; exhaustive file-by-file coverage is not established because the connected store does not expose a stable recursive inventory through the available interface. Issue 8 continues to govern public-source replacement.
'''
        company.write_text(clean(text), encoding="utf-8")

    semantics = ROOT / "documentation" / "explicit-semantics.md"
    if semantics.exists():
        text = semantics.read_text(encoding="utf-8")
        heading = "## Canon and recovery relations"
        if heading not in text:
            text += '''

## Canon and recovery relations

Release 0.17 adds controlled vocabulary for `canonised_as`, `excluded_from_canon`, `appropriated_from`, `recovers`, `participates_in_canon_formation` and `can_exclude`. These are deliberately demanding relation types. Identity, resemblance, geography or later admiration is not enough. The edge must state the particular history and carry evidence appropriate to it.
'''
            semantics.write_text(clean(text), encoding="utf-8")

    ledger = ROOT / "documentation" / "feedback-ledger.md"
    if ledger.exists():
        text = ledger.read_text(encoding="utf-8")
        heading = "## Release 0.17 — public intake, serendipity and canon visibility"
        if heading not in text:
            text += f'''

{heading}

- Public submissions and curator responses: implemented at `/submissions/`, using GitHub Issues as the canonical record.
- ‘Surprise me’: implemented across developed and brief substantive entries, excluding stubs and administrative/provenance records.
- Canon, ethnicity, traditions and heritage: implemented as a non-inference policy, public visibility audit, typed canon/recovery relations and guided route.
- Michael C. Jackson, Magnus Ramage, Karen Shipp and *Systems Thinkers*: developed with public institutional and publisher sources.
- Company-knowledge systems folder: second bounded discovery pass completed; public-source replacement continues under issue 8.
- Structured submissions checked: one submission found, issue 21, already incorporated in release 0.12 and now surfaced publicly.
'''
            ledger.write_text(clean(text), encoding="utf-8")


def patch_release_files(data: dict) -> None:
    meta = data["meta"]
    citation = ROOT / "CITATION.cff"
    text = citation.read_text(encoding="utf-8")
    text = re.sub(r"^version:.*$", f"version: {RELEASE}", text, flags=re.M)
    text = re.sub(r"^date-released:.*$", f"date-released: {GENERATED}", text, flags=re.M)
    text = re.sub(r"^url:.*$", f"url: {PUBLIC_URL}", text, flags=re.M)
    citation.write_text(clean(text), encoding="utf-8")

    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    paragraph = (
        f"Release 0.17 contains {meta['public_entry_count']} canonical public entries, "
        f"{meta['profile_count']} developed profiles, {meta['source_count']} sources and "
        f"{meta['journey_count']} guided journeys. It adds a public submissions-and-responses page, "
        "a genuine ‘Surprise me’ route across readable content, and a canon-and-lineage review which "
        "develops Michael C. Jackson, Magnus Ramage, Karen Shipp and *Systems Thinkers* while making "
        "the atlas's own visibility and identity rules explicit."
    )
    if paragraph not in text:
        marker = "This is a public alpha."
        at = text.find(marker)
        if at >= 0:
            end = text.find("\n", at)
            text = text[:end + 1] + "\n" + paragraph + "\n" + text[end + 1:]
        else:
            text = text.replace("# The Necessary Tangle\n", "# The Necessary Tangle\n\n" + paragraph + "\n", 1)
    link_line = "Public contributions and responses are visible at <https://transduction.systems/submissions/>; the canon and lineage review is at <https://transduction.systems/canon-and-lineage/>."
    if link_line not in text:
        text += "\n" + link_line + "\n"
    readme.write_text(clean(text), encoding="utf-8")

    changelog = ROOT / "CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8")
    heading = f"## {RELEASE} — 19 August 2026"
    if heading not in text:
        entry = f'''{heading}

- Added a first-class public submissions-and-responses page backed by visible GitHub issues and curator comments.
- Added a genuine ‘Surprise me’ control which selects from readable substantive entries and preserves ordinary browser history.
- Surfaced the first structured website submission, issue 21, with its incorporated status, response and resulting entries.
- Added a public canon and lineage review, a non-inference rule for identity and heritage, and controlled relations for canonisation, exclusion, appropriation and recovery.
- Developed Magnus Ramage, Karen Shipp, *Systems Thinkers* and Michael C. Jackson through current official and publisher sources.
- Added canon formation, epistemic closure, epistemic injustice, epistemic exclusion, structurelessness, lineage recovery and decolonial systems thinking.
- Added the guided journey ‘Who gets to count as a systems thinker?’.
- Completed a second bounded company-knowledge discovery pass without publishing private links or extracts.
- Extended the site-submission triage workflow with a public status vocabulary and automatic backfill.

'''
        text = text.replace("# Changelog\n\n", "# Changelog\n\n" + entry, 1)
    changelog.write_text(clean(text), encoding="utf-8")

    contributing = ROOT / "CONTRIBUTING.md"
    text = contributing.read_text(encoding="utf-8")
    addition = "Public submissions and curator responses are visible at https://transduction.systems/submissions/. GitHub Issues remain the canonical record."
    if addition not in text:
        text = text.replace("# Contributing", "# Contributing\n\n" + addition, 1)
    contributing.write_text(clean(text), encoding="utf-8")

    acknowledgements = ROOT / "ACKNOWLEDGEMENTS.md"
    text = acknowledgements.read_text(encoding="utf-8")
    paragraph = "Release 0.17 particularly acknowledges Ida Rose Florez for the challenge about closed epistemological systems, patriarchy and the visible canon; Magnus Ramage and Karen Shipp for making the boundary choices in systems history discussable; Michael C. Jackson for the critical systems programme; and Jo Freeman and Miranda Fricker for concepts which sharpen the treatment of structure, power and knowing."
    if paragraph not in text:
        text += "\n\n" + paragraph + "\n"
    acknowledgements.write_text(clean(text), encoding="utf-8")

    roadmap = ROOT / "documentation" / "roadmap.md"
    if roadmap.exists():
        text = roadmap.read_text(encoding="utf-8")
        note = "- [x] Public submissions/responses, serendipitous navigation and the first canon/lineage visibility pass (0.17)."
        if note not in text:
            text += "\n" + note + "\n"
        roadmap.write_text(clean(text), encoding="utf-8")


def write_triage_workflow() -> None:
    workflow = r'''name: Triage structured site submissions

on:
  issues:
    types: [opened, reopened, closed, labeled, unlabeled]
  issue_comment:
    types: [created, edited]
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - ".github/workflows/triage-site-submissions.yml"

permissions:
  issues: write

jobs:
  triage:
    if: >-
      github.event_name == 'workflow_dispatch' ||
      github.event_name == 'push' ||
      contains(github.event.issue.body || '', 'Prepared from The Necessary Tangle')
    runs-on: ubuntu-latest
    steps:
      - name: Create labels and classify the structured queue
        uses: actions/github-script@v8
        with:
          script: |
            const marker = 'Prepared from The Necessary Tangle';
            const labels = [
              {name: 'site-submission', color: '6f4e56', description: 'Structured contribution submitted through The Necessary Tangle site'},
              {name: 'awaiting-curator-review', color: 'd4a72c', description: 'Not yet accepted, rejected or incorporated by the curator'},
              {name: 'investigating', color: '1d76db', description: 'Evidence or implications are being investigated'},
              {name: 'incorporated', color: '2da44e', description: 'Incorporated into a numbered public release'},
              {name: 'partly-incorporated', color: '4c9a5f', description: 'Some but not all of the proposal was incorporated'},
              {name: 'disputed', color: '8250df', description: 'The disagreement remains visible and unresolved'},
              {name: 'deferred', color: '8c6d1f', description: 'Retained for later work rather than decided now'},
              {name: 'declined', color: '6e7781', description: 'Reviewed and not accepted, with the reason kept public'}
            ];
            for (const label of labels) {
              try {
                await github.rest.issues.getLabel({owner: context.repo.owner, repo: context.repo.repo, name: label.name});
              } catch (error) {
                if (error.status !== 404) throw error;
                await github.rest.issues.createLabel({owner: context.repo.owner, repo: context.repo.repo, ...label});
              }
            }

            let issues;
            if (context.eventName === 'issues' || context.eventName === 'issue_comment') {
              issues = [context.payload.issue];
            } else {
              issues = await github.paginate(github.rest.issues.listForRepo, {
                owner: context.repo.owner, repo: context.repo.repo, state: 'all', per_page: 100
              });
            }
            issues = issues.filter(issue => !issue.pull_request && (issue.body || '').includes(marker));
            const terminal = ['incorporated','partly-incorporated','disputed','deferred','declined'];
            for (const issue of issues) {
              const comments = await github.paginate(github.rest.issues.listComments, {
                owner: context.repo.owner, repo: context.repo.repo, issue_number: issue.number, per_page: 100
              });
              const commentText = comments.map(comment => comment.body || '').join('\n').toLowerCase();
              const existing = (issue.labels || []).map(label => typeof label === 'string' ? label : label.name);
              let status = terminal.find(name => existing.includes(name));
              if (commentText.includes('incorporated in release')) status = 'incorporated';
              const add = ['site-submission'];
              if (status) add.push(status);
              else if (issue.state === 'open') add.push('awaiting-curator-review');
              else add.push('deferred');
              await github.rest.issues.addLabels({
                owner: context.repo.owner, repo: context.repo.repo, issue_number: issue.number, labels: add
              });
              if (status && existing.includes('awaiting-curator-review')) {
                await github.rest.issues.removeLabel({
                  owner: context.repo.owner, repo: context.repo.repo, issue_number: issue.number, name: 'awaiting-curator-review'
                });
              }
            }
            core.info(`Classified ${issues.length} structured site submission(s).`);
'''
    write(ROOT / ".github" / "workflows" / "triage-site-submissions.yml", workflow)


def patch_previous_validator() -> None:
    path = ROOT / "scripts" / "validate_iteration_16.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        'if meta.get("release") != RELEASE:\n        errors.append(f"meta.release must be {RELEASE}")',
        'if meta.get("release") not in {RELEASE, "0.17-public-intake-lineage-alpha"}:\n        errors.append(f"meta.release must preserve 0.16 or identify the 0.17 successor")'
    )
    text = text.replace(
        'if meta.get("generated") != GENERATED:\n        errors.append(f"meta.generated must be {GENERATED}")',
        'if meta.get("generated") not in {GENERATED, "2026-08-19"}:\n        errors.append("meta.generated must identify the 0.16 build or its 0.17 successor")'
    )
    text = text.replace(
        'if data.get("ai_observations", {}).get("release") != RELEASE:',
        'if data.get("ai_observations", {}).get("release") != meta.get("release"):'
    )
    text = text.replace(
        'if data.get(inherited, {}).get("release") != RELEASE:',
        'if data.get(inherited, {}).get("release") != meta.get("release"):'
    )
    text = text.replace(
        'f"version: {RELEASE}" not in citation',
        'f"version: {meta.get(\'release\')}" not in citation'
    )
    text = text.replace("assets/styles.css?v=0.16.3-visual", f"assets/styles.css?v={VERSION}")
    text = text.replace("assets/site-enhancements.css?v=0.16.3-visual", f"assets/site-enhancements.css?v={VERSION}")
    text = text.replace("assets/app.js?v=0.16.3-visual", f"assets/app.js?v={VERSION}")
    path.write_text(clean(text), encoding="utf-8")


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if data.get("meta", {}).get("release") != RELEASE:
        raise RuntimeError("apply_iteration_17.py must run before patch_iteration_17.py")
    patch_index(data)
    write_surprise_assets()
    write_submissions_page(data)
    write_canon_page(data)
    write_documentation(data)
    patch_release_files(data)
    write_triage_workflow()
    patch_previous_validator()
    print(f"Patched public reader and release prose for {RELEASE}")


if __name__ == "__main__":
    main()
