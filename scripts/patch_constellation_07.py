#!/usr/bin/env python3
"""Apply the 0.7 constellation interface and participation refinements."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
APP = ROOT / "docs" / "assets" / "app.js"
CSS = ROOT / "docs" / "assets" / "site-enhancements.css"

MAP_CONTROLS = '''
          <div class="constellation-controls" aria-label="Constellation controls">
            <label>Neighbourhood <select id="mapCategory"><option value="">All provisional neighbourhoods</option></select></label>
            <label class="label-toggle"><input id="mapShowLabels" type="checkbox" checked> Show labels</label>
            <div class="zoom-controls" aria-label="Map zoom">
              <button type="button" id="mapZoomOut" aria-label="Zoom out">−</button>
              <span id="mapZoomStatus" aria-live="polite">100%</span>
              <button type="button" id="mapZoomIn" aria-label="Zoom in">+</button>
            </div>
            <p id="mapCategoryNote" class="map-category-note">Neighbourhoods are provisional graph groupings, not canonical schools or categories.</p>
          </div>
'''

MEMBERSHIP = '''
        <article class="plain-panel wide membership-panel">
          <h2>Take part in the tangle</h2>
          <p>The atlas has different participation roles. Contributions remain attributable, reviewable and subject to curator acceptance. Automated assistance requires a named human sponsor.</p>
          <form id="membershipForm" class="membership-grid">
            <label>How would you like to take part?
              <select name="role" required>
                <option value="participant">Participant</option>
                <option value="contributor">Contributor</option>
                <option value="research_collaborator">Research collaborator</option>
                <option value="domain_steward">Domain steward</option>
              </select>
            </label>
            <label>What area or contribution do you have in mind?
              <input name="interest" type="text" placeholder="A concept, source, lineage, correction or coverage area" required>
            </label>
            <button type="submit">Prepare a contribution note</button>
          </form>
          <p id="membershipStatus" class="small" aria-live="polite"></p>
          <p><a href="https://github.com/antlerboy/the-necessary-tangle/issues/new/choose" class="public-contribution-link" target="_blank" rel="noopener">Open a public contribution route →</a></p>
        </article>
'''

APPEND_JS = r'''

/* 0.7 constellation controls: provisional neighbourhoods, zoom and participation. */
(() => {
  const emergentCategories = () => window.TANGLE_DATA?.emergent_categories || [];
  let tangleZoom = 1;

  function zoomMapAt(factor, originX = 50, originY = 50) {
    const svg = document.getElementById('graphSvg');
    if (!svg) return;
    tangleZoom = Math.max(0.55, Math.min(2.5, tangleZoom * factor));
    svg.style.transformOrigin = `${originX}% ${originY}%`;
    svg.style.transform = `scale(${tangleZoom})`;
    const status = document.getElementById('mapZoomStatus');
    if (status) status.textContent = `${Math.round(tangleZoom * 100)}%`;
  }

  function categoryMembers(category) {
    return new Set(category?.member_node_ids || category?.members || []);
  }

  function applyCategory(categoryId) {
    const category = emergentCategories().find((item) => (item.id || item.category_id) === categoryId);
    const members = categoryMembers(category);
    const svg = document.getElementById('graphSvg');
    if (svg) {
      svg.querySelectorAll('[data-node-id], [data-id]').forEach((node) => {
        const id = node.dataset.nodeId || node.dataset.id;
        node.classList.toggle('category-halo', Boolean(category && members.has(id)));
        node.classList.toggle('category-muted', Boolean(category && !members.has(id)));
      });
    }
    const note = document.getElementById('mapCategoryNote');
    if (note) note.textContent = category
      ? `${category.label || category.name || 'Selected neighbourhood'} — provisional graph grouping; inspect the typed lines rather than treating it as a canon.`
      : 'Neighbourhoods are provisional graph groupings, not canonical schools or categories.';
  }

  function initConstellationControls() {
    const select = document.getElementById('mapCategory');
    if (select && !select.dataset.ready) {
      emergentCategories().forEach((category) => {
        const option = document.createElement('option');
        option.value = category.id || category.category_id || '';
        option.textContent = category.label || category.name || option.value;
        select.append(option);
      });
      select.addEventListener('change', () => applyCategory(select.value));
      select.dataset.ready = 'true';
    }

    document.getElementById('mapZoomIn')?.addEventListener('click', () => zoomMapAt(1.15));
    document.getElementById('mapZoomOut')?.addEventListener('click', () => zoomMapAt(1 / 1.15));
    const svg = document.getElementById('graphSvg');
    svg?.addEventListener('wheel', (event) => {
      event.preventDefault();
      const box = svg.getBoundingClientRect();
      const x = box.width ? ((event.clientX - box.left) / box.width) * 100 : 50;
      const y = box.height ? ((event.clientY - box.top) / box.height) * 100 : 50;
      zoomMapAt(event.deltaY < 0 ? 1.08 : 1 / 1.08, x, y);
    }, { passive: false });

    document.getElementById('mapShowLabels')?.addEventListener('change', (event) => {
      document.getElementById('graphSvg')?.classList.toggle('hide-map-labels', !event.target.checked);
    });

    const membershipForm = document.getElementById('membershipForm');
    membershipForm?.addEventListener('submit', (event) => {
      event.preventDefault();
      const form = new FormData(membershipForm);
      const role = String(form.get('role') || 'participant').replaceAll('_', ' ');
      const interest = String(form.get('interest') || '').trim();
      const status = document.getElementById('membershipStatus');
      if (status) status.innerHTML = `Contribution note ready: <strong>${role}</strong>${interest ? ` — ${interest}` : ''}. Continue through <a href="https://github.com/antlerboy/the-necessary-tangle/issues/new/choose" target="_blank" rel="noopener">a public issue form</a>. If automation helped, name the human sponsor.`;
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initConstellationControls);
  else initConstellationControls();
})();
'''

CSS_APPEND = r'''

/* 0.7 constellation controls */
.constellation-controls { display: flex; flex-wrap: wrap; gap: .65rem 1rem; align-items: center; margin: .8rem 0; }
.constellation-controls label { display: flex; gap: .45rem; align-items: center; }
.zoom-controls { display: inline-flex; gap: .45rem; align-items: center; }
#mapZoomStatus { min-width: 3.5rem; text-align: center; font-variant-numeric: tabular-nums; }
.map-category-note { flex-basis: 100%; margin: 0; font-size: .9rem; opacity: .78; }
#graphSvg { transition: transform .16s ease; }
#graphSvg.hide-map-labels text { display: none; }
#graphSvg .category-muted { opacity: .16 !important; }
#graphSvg .category-halo { opacity: 1 !important; filter: drop-shadow(0 0 5px currentColor); }
.membership-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: .8rem; align-items: end; }
.membership-grid label { display: grid; gap: .35rem; }
.public-contribution-link { font-weight: 650; }
'''


def clean(text: str) -> str:
    """Strip trailing whitespace and leave exactly one final newline."""
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    text = text.replace("antlerboy-benjamintaylor.github.io/the-necessary-tangle", "antlerboy.github.io/the-necessary-tangle")
    text = text.replace("github.com/antlerboy-benjamintaylor/the-necessary-tangle", "github.com/antlerboy/the-necessary-tangle")
    text = text.replace("Created and edited by Benjamin P Taylor", "Curated by Benjamin P Taylor")
    text = text.replace("systems, complexity and cybernetics", "systems | cybernetics | complexity")

    if 'id="mapCategory"' not in text:
        match = re.search(r'(<button[^>]+id="mapReset"[^>]*>.*?</button>)', text, re.S)
        if match:
            text = text[:match.end()] + MAP_CONTROLS + text[match.end():]
        else:
            marker = '<div class="map-stage">'
            if marker not in text:
                raise RuntimeError("Could not locate map controls or map stage")
            text = text.replace(marker, MAP_CONTROLS + marker, 1)

    if 'id="membershipForm"' not in text:
        marker = '<form id="contributionForm"'
        pos = text.find(marker)
        if pos < 0:
            raise RuntimeError("Could not locate contribution form")
        text = text[:pos] + MEMBERSHIP + text[pos:]


    INDEX.write_text(clean(text), encoding="utf-8")

    app = APP.read_text(encoding="utf-8")
    if "function zoomMapAt" not in app and "semanticZoomBand" not in app:
        app = app.rstrip() + "\n" + APPEND_JS.strip() + "\n"
    APP.write_text(clean(app), encoding="utf-8")

    css = CSS.read_text(encoding="utf-8") if CSS.exists() else ""
    if ".category-halo" not in css:
        css = css.rstrip() + "\n" + CSS_APPEND.strip() + "\n"
    CSS.write_text(clean(css), encoding="utf-8")

    print("Applied 0.7 constellation interface controls and participation route")


if __name__ == "__main__":
    main()
