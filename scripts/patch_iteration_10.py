#!/usr/bin/env python3
"""Apply release 0.10 interface changes: pathways, distinctions and safer public controls."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
APP = ROOT / "docs" / "assets" / "app.js"
CSS = ROOT / "docs" / "assets" / "site-enhancements.css"

RESOURCE_PATHWAYS = '''
      <section class="resource-pathways" aria-labelledby="resourcePathwaysTitle">
        <div class="section-head"><div><p class="eyebrow">The living field around the atlas</p><h2 id="resourcePathwaysTitle">Communities, capability and a way into the reading</h2></div></div>
        <div class="resource-pathway-grid">
          <a class="resource-pathway-card" href="https://www.syscoi.com/" target="_blank" rel="noopener">
            <span class="eyebrow">Open discussion and source trail</span>
            <strong>Systems Community of Inquiry</strong>
            <span>Follow current writing, arguments, papers, events and the unruly conversation around systems | cybernetics | complexity.</span>
          </a>
          <a class="resource-pathway-card" href="https://www.systemspractice.org/professional-accreditation" target="_blank" rel="noopener">
            <span class="eyebrow">Capability and professional standards</span>
            <strong>SCiO competency and accreditation</strong>
            <span>See what professional systems-practice capability asks of knowledge, methods, intervention skills and reflective judgement.</span>
          </a>
          <a class="resource-pathway-card" href="https://www.systemspractice.org/professional-development" target="_blank" rel="noopener">
            <span class="eyebrow">Training and development</span>
            <strong>SCiO professional development</strong>
            <span>Explore systems approaches, intervention methods, courses and practice-based development from experienced practitioners.</span>
          </a>
          <a class="resource-pathway-card" href="https://www.antlerboy.com/reading-list" target="_blank" rel="noopener">
            <span class="eyebrow">A partial route into the territory</span>
            <strong>Benjamin's reading list</strong>
            <span>Start with the things that bring your mind alive. The list is deliberately partial, practice-facing and open to argument.</span>
          </a>
        </div>
      </section>
'''

SIX_SYSTEMS_SECTION = '''
      <section class="six-systems-section" aria-labelledby="sixSystemsTitle">
        <div class="section-head"><div><p class="eyebrow">A necessary untangling</p><h2 id="sixSystemsTitle">Six systems things which are not the same thing</h2><p>These phrases are routinely blended into one agreeable cloud. Open the distinctions, then challenge them.</p></div><a href="#view=journeys&id=journey_six_systems_things&step=0" class="text-button">Follow the guided route</a></div>
        <div class="six-systems-grid">
          <a href="#view=item&id=tradition_systems_theory&from=home" class="six-system-card"><strong>Systems theory</strong><span>Explanatory traditions. Not one doctrine, and not yet an intervention.</span></a>
          <a href="#view=item&id=practice_systems_practice&from=home" class="six-system-card"><strong>Systems practice</strong><span>Situated inquiry, judgement and action using systems ideas and methods.</span></a>
          <a href="#view=item&id=approach_family_systems_leadership&from=home" class="six-system-card"><strong>Systems leadership</strong><span>Several different ways of exercising authority or influence across a system of concern.</span></a>
          <a href="#view=item&id=approach_family_systems_change&from=home" class="six-system-card"><strong>Systems change</strong><span>Claims about which patterns should change, by whose agency and with what legitimacy.</span></a>
          <a href="#view=item&id=practice_systems_convening&from=home" class="six-system-card"><strong>Systems convening</strong><span>Social-learning leadership across boundaries in a complex landscape.</span></a>
          <a href="#view=item&id=practice_systems_weaving&from=home" class="six-system-card"><strong>Systems weaving</strong><span>Strengthening the relational and network infrastructure for collective action.</span></a>
        </div>
      </section>
'''

ABOUT_DISTINCTIONS = '''
        <article class="plain-panel wide systems-distinction-callout">
          <p class="eyebrow">Words which create false agreement</p>
          <h2>Six systems things which are not the same thing</h2>
          <p>Systems theory, systems practice, systems leadership, systems change, systems convening and systems weaving point to different kinds of explanation, capability, authority and action. They overlap, but merging them makes it impossible to ask what work is actually being proposed, who has power, or what would count as learning.</p>
          <p><a class="button primary" href="#view=journeys&id=journey_six_systems_things&step=0">Follow the guided route</a> <a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/six-systems-things.md" target="_blank" rel="noopener">Read the maintained distinctions</a></p>
        </article>
'''

PUBLICATION_SAFETY_PANEL = '''
        <article class="plain-panel wide publication-safety-panel">
          <p class="eyebrow">Publication controls</p>
          <h2>Public enough to challenge. Bounded enough not to leak the workshop.</h2>
          <p>The detailed working risk register is no longer part of the public release. The public record shows the controls: public-only payloads, source-level provenance, automated scans, curator-controlled releases, licence boundaries and versioned backups.</p>
          <p><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/publication-safety.md" target="_blank" rel="noopener">Read the publication controls</a> <a class="button" href="https://github.com/antlerboy/the-necessary-tangle/security" target="_blank" rel="noopener">Report a security concern</a></p>
        </article>
'''

ABOUT_PUBLICATION_SAFETY = '''
        <article class="plain-panel wide publication-safety-callout">
          <p class="eyebrow">Public by design, not by accident</p>
          <h2>Publication safety</h2>
          <p>Private research may generate leads, but the public release is rebuilt from public data and citations, scanned for private-path and credential patterns, validated, reviewed by the curator and backed up with a checksum. Detailed operational risk notes remain outside the public release.</p>
          <p><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/publication-safety.md" target="_blank" rel="noopener">How publication is controlled</a></p>
        </article>
'''

CSS_APPEND = r'''

/* 0.10 practice distinctions, public pathways and publication controls */
.resource-pathways, .six-systems-section { margin: 2.2rem 0; }
.resource-pathway-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(235px, 1fr)); gap: .85rem; }
.resource-pathway-card { display: grid; align-content: start; gap: .48rem; min-height: 175px; padding: 1.15rem; border: 1px solid var(--line); border-radius: var(--radius); background: linear-gradient(145deg, var(--panel), var(--panel-2)); box-shadow: var(--shadow); color: inherit; text-decoration: none; text-align: left; }
.resource-pathway-card strong { color: var(--accent); font-size: 1.18rem; }
.resource-pathway-card > span:last-child { color: var(--muted); line-height: 1.5; }
.resource-pathway-card:hover, .resource-pathway-card:focus-visible { border-color: var(--accent); transform: translateY(-2px); color: inherit; }
.six-systems-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: .75rem; }
.six-system-card { display: grid; gap: .35rem; padding: 1rem; border-left: 4px solid var(--orange); border-radius: 8px; background: var(--panel-2); color: inherit; text-decoration: none; text-align: left; }
.six-system-card strong { color: var(--accent); font-size: 1.04rem; }
.six-system-card span { color: var(--muted); }
.six-system-card:hover, .six-system-card:focus-visible { background: var(--panel); transform: translateX(2px); color: inherit; }
.systems-distinction-callout { border-left: 5px solid var(--orange); }
.publication-safety-panel, .publication-safety-callout { border-left: 5px solid var(--green); }
'''


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def patch_index() -> None:
    text = INDEX.read_text(encoding="utf-8")

    guided_marker = '<div class="section-head"><div><p class="eyebrow">Begin here</p><h2>Guided questions</h2></div><a href="#view=journeys" class="text-button" data-view-link="journeys">See all journeys</a></div>'
    if 'id="resourcePathwaysTitle"' not in text:
        if guided_marker not in text:
            raise RuntimeError("Could not locate home guided-questions marker")
        text = text.replace(guided_marker, RESOURCE_PATHWAYS + "\n" + guided_marker, 1)

    author_marker = '<section class="author-strip">'
    if 'id="sixSystemsTitle"' not in text:
        if author_marker not in text:
            raise RuntimeError("Could not locate author strip")
        text = text.replace(author_marker, SIX_SYSTEMS_SECTION + "\n      " + author_marker, 1)

    ai_callout_old = "The data now supports observations about the atlas itself: where breadth has outrun depth, where provenance is being mistaken for conceptual connection, which entries carry disproportionate traffic, what the source set makes visible, and what publication risks follow."
    ai_callout_new = "The data now supports observations about the atlas itself: where breadth has outrun depth, where provenance is being mistaken for conceptual connection, which entries carry disproportionate traffic, and what the current source set makes visible or leaves silent."
    text = text.replace(ai_callout_old, ai_callout_new)

    if 'class="plain-panel wide systems-distinction-callout"' not in text:
        ai_card_end = '</article>\n\n<article class="plain-panel"><h2>Current state</h2>'
        if ai_card_end not in text:
            raise RuntimeError("Could not locate About AI card boundary")
        text = text.replace(ai_card_end, '</article>\n\n' + ABOUT_DISTINCTIONS + '\n' + ABOUT_PUBLICATION_SAFETY + '\n<article class="plain-panel"><h2>Current state</h2>', 1)

    risk_pattern = re.compile(
        r'\n\s*<article class="plain-panel wide">\s*<p class="eyebrow">Publication controls</p>\s*<h2>Risks of making the atlas public</h2>.*?</article>',
        re.S,
    )
    if 'class="plain-panel wide publication-safety-panel"' not in text:
        text, count = risk_pattern.subn("\n" + PUBLICATION_SAFETY_PANEL.strip(), text, count=1)
        if count != 1:
            raise RuntimeError("Could not replace public risk register panel")

    # Keep public contributions on visible, structured routes.
    text = re.sub(r'\s*<span class="discreet-note-link">.*?</span>', '', text, flags=re.S)
    text = re.sub(r'\s*<p>\s*<a[^>]*class="curator-notebook-link"[^>]*>.*?</a>\s*</p>', '', text, flags=re.S)

    INDEX.write_text(clean(text), encoding="utf-8")


def patch_app() -> None:
    app = APP.read_text(encoding="utf-8")

    risk_renderer = re.compile(
        r"\n\s*\$\('aiRiskList'\)\.innerHTML = \(report\.public_risks \|\| \[\]\)\.map\(\(risk\) => `.*?`\)\.join\(''\);",
        re.S,
    )
    app = risk_renderer.sub('', app, count=1)

    old_membership = ""
    new_membership = "if (status) status.innerHTML = `Contribution note ready: <strong>${role}</strong>${interest ? ` — ${interest}` : ''}. Continue through <a href=\"https://github.com/antlerboy/the-necessary-tangle/issues/new?template=membership.yml\" target=\"_blank\" rel=\"noopener\">the structured participation form</a>. If automation helped, name the human sponsor.`;"
    if old_membership:
        app = app.replace(old_membership, new_membership)

    APP.write_text(clean(app), encoding="utf-8")


def patch_css() -> None:
    css = CSS.read_text(encoding="utf-8") if CSS.exists() else ""
    if ".resource-pathway-grid" not in css:
        css = css.rstrip() + "\n" + CSS_APPEND.strip() + "\n"
    CSS.write_text(clean(css), encoding="utf-8")


def main() -> None:
    patch_index()
    if APP.exists() and "semanticZoomBand" in APP.read_text(encoding="utf-8"):
        print("Preserved the 0.11 map application while refreshing the 0.10 page and styles")
    else:
        patch_app()
    patch_css()
    print("Applied 0.10 systems distinctions, public pathways and publication-safety interface changes")


if __name__ == "__main__":
    main()
