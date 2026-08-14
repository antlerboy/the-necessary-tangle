#!/usr/bin/env python3
"""Apply the Pass 5 relationship-disclosure refinement idempotently."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "docs" / "assets" / "app.js"
STYLES = ROOT / "docs" / "assets" / "styles.css"


HELPERS = r"""

  function relationshipBasis(edge) {
    const mode = String(edge.assertion_mode || '').toLowerCase();
    const review = String(edge.public_review_label || '').toLowerCase();
    const hasSources = parse(edge.source_ids, []).length > 0;
    if (['inferred', 'candidate'].includes(mode)) {
      return {
        key: 'inference',
        label: mode === 'candidate' ? 'Candidate connection' : 'Inferred connection',
        description: 'This is a proposed or inferred connection, not a source-established statement.'
      };
    }
    if (['interpreted', 'editorial_research_pass'].includes(mode)) {
      return {
        key: 'interpretation',
        label: mode === 'editorial_research_pass' ? 'Editorial synthesis' : 'Curatorial interpretation',
        description: 'The connection is an editorial interpretation of the cited material.'
      };
    }
    if (mode === 'inherited') {
      return {
        key: 'inherited',
        label: 'Inherited record',
        description: 'The connection was inherited from an earlier register and still needs claim-level review.'
      };
    }
    if (mode === 'asserted' && hasSources && /source-established|source-backed|official bibliographic/.test(review)) {
      return {
        key: 'source-established',
        label: 'Source-established',
        description: 'The maintained statement is explicitly established by the linked source record.'
      };
    }
    if (mode === 'asserted' && hasSources) {
      return {
        key: 'sourced',
        label: 'Sourced assertion',
        description: 'The maintained assertion has a linked source; inspect the locator and status to judge its precision.'
      };
    }
    return {
      key: 'maintained',
      label: 'Maintained assertion',
      description: 'The atlas maintains this statement, but no stronger evidence-basis label is available.'
    };
  }

  function relationshipBasisBadge(edge) {
    const basis = relationshipBasis(edge);
    return `<span class="badge connection-basis ${esc(basis.key)}">${esc(basis.label)}</span>`;
  }
"""


STYLE_BLOCK = r"""

/* Pass 5: disclose relationship basis without adding lines to the map canvas. */
.connection-basis { line-height: 1.15; white-space: normal; }
.connection-basis.source-established,
.connection-basis.sourced { background: color-mix(in srgb, var(--blue) 16%, var(--panel)); color: var(--blue); }
.connection-basis.interpretation { background: color-mix(in srgb, var(--purple) 18%, var(--panel)); color: color-mix(in srgb, var(--purple) 78%, var(--text)); }
.connection-basis.inference { background: color-mix(in srgb, var(--orange) 16%, var(--panel)); color: var(--orange); }
.connection-basis.inherited,
.connection-basis.maintained { border: 1px solid var(--line); background: transparent; color: var(--muted); }
.relationship-key { margin: .45rem 0 .2rem; padding: .55rem .65rem; border-left: 3px solid var(--purple); background: var(--panel-2); border-radius: 0 8px 8px 0; }
.relation-statement .connection-basis { margin: .45rem .25rem .15rem 0; }
.relation-inspection-basis { padding: .75rem; background: var(--panel-2); border-radius: 10px; }
.relation-inspection-basis p { margin: .25rem 0; }
"""


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Pass 5 patch anchor missing: {label}")
    return text.replace(old, new, 1)


def patch_app() -> None:
    text = APP.read_text(encoding="utf-8")
    helper_anchor = "\n  function relationFamilyLabel(value) {"
    if "function relationshipBasis(edge)" not in text:
        if helper_anchor not in text:
            raise RuntimeError("Pass 5 helper anchor missing")
        text = text.replace(helper_anchor, HELPERS + helper_anchor, 1)

    text = replace_once(
        text,
        '<span class="badge ${[\'accepted\', \'corroborated\'].includes(edge.claim_status) ? \'supported\' : \'provisional\'}">${esc(edge.public_review_label || publicStatusLabel(edge.claim_status))}</span><br>',
        '<span class="badge ${[\'accepted\', \'corroborated\'].includes(edge.claim_status) ? \'supported\' : \'provisional\'}">${esc(edge.public_review_label || publicStatusLabel(edge.claim_status))}</span> ${relationshipBasisBadge(edge)}<br>',
        "entry relationship basis",
    )

    text = replace_once(
        text,
        '<p class="small">Choose either named item to make it the new centre. Choose ‘Inspect this connection’ for wording, status and sources.</p>\n      ${relations.map((edge) => `<div class="relation-statement">${relationStatement(edge)}<br><button class="text-button inspect-edge" data-edge="${esc(edge.id)}">Inspect this connection</button></div>`).join(\'\')}',
        '<p class="small">Choose either named item to make it the new centre. Choose ‘Inspect this connection’ for wording, status and sources.</p>\n      <p class="small relationship-key"><strong>Evidence basis:</strong> badges distinguish sourced assertions, curatorial interpretation and inference. Dashed lines remain provisional.</p>\n      ${relations.map((edge) => `<div class="relation-statement">${relationStatement(edge)}<br>${relationshipBasisBadge(edge)}<br><button class="text-button inspect-edge" data-edge="${esc(edge.id)}">Inspect this connection</button></div>`).join(\'\')}',
        "map relationship basis",
    )

    text = replace_once(
        text,
        "    const direction = String(edge.directed).toLowerCase() === 'true' || edge.directed === true\n      ? `Read this from left to right: ${sourceNode?.label || edge.source} ${edge.plain_phrase || edge.relation_type} ${targetNode?.label || edge.target}.`\n      : 'This connection is treated as undirected.';\n    const html =",
        "    const direction = String(edge.directed).toLowerCase() === 'true' || edge.directed === true\n      ? `Read this from left to right: ${sourceNode?.label || edge.source} ${edge.plain_phrase || edge.relation_type} ${targetNode?.label || edge.target}.`\n      : 'This connection is treated as undirected.';\n    const basis = relationshipBasis(edge);\n    const locator = String(edge.source_locator || '').trim();\n    const html =",
        "edge inspector variables",
    )

    text = replace_once(
        text,
        '        <span class="badge ${[\'accepted\', \'corroborated\'].includes(edge.claim_status) ? \'supported\' : \'provisional\'}">${esc(edge.public_review_label || publicStatusLabel(edge.claim_status))}</span>\n        <span class="badge">Confidence: ${esc(edge.confidence || \'not stated\')}</span>',
        '        <span class="badge ${[\'accepted\', \'corroborated\'].includes(edge.claim_status) ? \'supported\' : \'provisional\'}">${esc(edge.public_review_label || publicStatusLabel(edge.claim_status))}</span>\n        ${relationshipBasisBadge(edge)}\n        <span class="badge">Confidence: ${esc(edge.confidence || \'not stated\')}</span>',
        "inspector basis badge",
    )

    text = replace_once(
        text,
        '        <p><strong>Connection type:</strong> ${esc(relationDefinition?.plain_phrase || edge.plain_phrase || titleCase(edge.relation_type))}</p>\n      </section>\n      <section class="entry-section"><h2>Sources</h2>',
        '        <p><strong>Connection type:</strong> ${esc(relationDefinition?.plain_phrase || edge.plain_phrase || titleCase(edge.relation_type))}</p>\n        <div class="relation-inspection-basis">\n          <p><strong>Evidence basis:</strong> ${esc(basis.label)}. ${esc(basis.description)}</p>\n          <p><strong>Stored assertion mode:</strong> ${esc(titleCase(edge.assertion_mode || \'not stated\'))}</p>\n          <p><strong>Claim-level locator:</strong> ${esc(locator || \'No claim-level locator is recorded.\')}</p>\n        </div>\n      </section>\n      <section class="entry-section"><h2>Sources</h2>',
        "inspector evidence disclosure",
    )

    APP.write_text(text, encoding="utf-8")


def patch_styles() -> None:
    text = STYLES.read_text(encoding="utf-8")
    if "Pass 5: disclose relationship basis" not in text:
        text = text.rstrip() + STYLE_BLOCK + "\n"
    STYLES.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    patch_app()
    patch_styles()
    print("Applied Pass 5 relationship-disclosure refinement.")
