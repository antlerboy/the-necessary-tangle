#!/usr/bin/env python3
from pathlib import Path
import json
import re
import apply_relational_depth_16 as relational

ROOT = Path(__file__).resolve().parents[1]
RELEASE = "0.17-public-intake-lineage-alpha"
GENERATED = "2026-08-19"
data = json.loads((ROOT / "data" / "public-data.json").read_text(encoding="utf-8"))

path = ROOT / "documentation" / "ai-observations.md"
text = path.read_text(encoding="utf-8")
line = f"Generated for release `{RELEASE}` on {GENERATED}."
updated, count = re.subn(r"Generated for release `[^`]+` on \d{4}-\d{2}-\d{2}\.", line, text, count=1)
if not count:
    lines = text.splitlines()
    insert_at = 1 if lines and lines[0].startswith("#") else 0
    lines.insert(insert_at, "")
    lines.insert(insert_at + 1, line)
    updated = "\n".join(lines)
path.write_text(updated.rstrip() + "\n", encoding="utf-8")

relational.RELEASE = RELEASE
relational.GENERATED = GENERATED
relational.write_relational_document(data)
rel_path = ROOT / "documentation" / "relational-depth.md"
rel_text = rel_path.read_text(encoding="utf-8")
old_cohort = (
    "This release adds typed provisional crosswalks for every SCiO intervention-skill entry; gives the previously reader-isolated concepts, methods, tools and traditions multiple routes into the maintained graph; exposes the Foundational Papers volume contents as documentary statements; connects the Cynefin wiki to its maintaining organisation and the material it presents; and adds slide-level statements from the supplied transformation, convening, organisational-dynamics, VSM, clarity and conversation material."
)
new_cohort = (
    "This release adds a public contribution-and-response layer, an inspectable canon-and-lineage route, richer treatment of Michael C. Jackson, Magnus Ramage, Karen Shipp and Systems Thinkers, and typed connections concerning canon formation, epistemic exclusion, appropriation, recovery and structurelessness. It also incorporates the first structured site submission as a public projection while keeping the GitHub issue as the canonical conversation, and records a bounded second company-knowledge discovery pass without publishing private links or extracts."
)
if old_cohort in rel_text:
    rel_text = rel_text.replace(old_cohort, new_cohort, 1)
rel_path.write_text(rel_text, encoding="utf-8")

ledger_path = ROOT / "documentation" / "feedback-ledger.md"
ledger_text = ledger_path.read_text(encoding="utf-8") if ledger_path.exists() else "# Feedback ledger\n"
heading = "## Release 0.17 — public intake, serendipity and canon visibility"
if heading not in ledger_text:
    ledger_text += (
        "\n\n" + heading + "\n\n"
        "- Public submissions and curator responses: implemented at `/submissions/`, using GitHub Issues as the canonical record.\n"
        "- ‘Surprise me’: implemented across developed and brief substantive entries, excluding stubs and administrative or provenance records.\n"
        "- Canon, traditions and heritage: implemented as a non-inference policy, public visibility audit, typed canon and recovery relations, and a guided route.\n"
        "- Michael C. Jackson, Magnus Ramage, Karen Shipp and *Systems Thinkers*: developed with public institutional and publisher sources.\n"
        "- Company knowledge: a second bounded discovery pass is recorded; public-source replacement continues under issue 8.\n"
        "- Structured submissions checked: one submission found, issue 21, already incorporated in release 0.12 and now surfaced publicly.\n"
    )
ledger_path.write_text(ledger_text.rstrip() + "\n", encoding="utf-8")
print(f"Synced maintained release documents for {RELEASE}")
