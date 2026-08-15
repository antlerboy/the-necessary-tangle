#!/usr/bin/env python3
"""Validate the concise operating spine for bounded AI-assisted work."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


required_files = [
    "AGENTS.md",
    "documentation/TANGLE_STATE.md",
    "documentation/DESIGN_AND_CONTENT_RULES.md",
    "documentation/NEXT_WORK.md",
    "documentation/WORK_PROTOCOL.md",
    "documentation/WORK_TICKET_TEMPLATE.md",
]

missing = [path for path in required_files if not (ROOT / path).is_file()]
if missing:
    raise SystemExit("Work-spine validation failed; missing: " + ", ".join(missing))

agents = read("AGENTS.md")
state = read("documentation/TANGLE_STATE.md")
rules = read("documentation/DESIGN_AND_CONTENT_RULES.md")
next_work = read("documentation/NEXT_WORK.md")
protocol = read("documentation/WORK_PROTOCOL.md")
template = read("documentation/WORK_TICKET_TEMPLATE.md")
index = read("docs/index.html")
readme = read("README.md")

checks = {
    "orientation remains concise": len(agents.encode("utf-8")) <= 8_000,
    "orientation points to state": "documentation/TANGLE_STATE.md" in agents,
    "orientation points to rules": "documentation/DESIGN_AND_CONTENT_RULES.md" in agents,
    "orientation points to next work": "documentation/NEXT_WORK.md" in agents,
    "state records verification date": "Last verified:" in state,
    "state records public site": "https://transduction.systems/" in state,
    "state names machine snapshot": "data/relationship-quality.json" in state,
    "rules prohibit generic relations": "generic ‘related to’" in rules,
    "rules preserve magic dot": 'aria-label="Open updates"' in rules,
    "site still contains magic dot": 'aria-label="Open updates"' in index,
    "next work has status": "Status:" in next_work,
    "next work has outcome": "## Outcome" in next_work,
    "next work has scope boundaries": all(
        heading in next_work for heading in ("## In scope", "## Out of scope")
    ),
    "next work has acceptance checks": "## Acceptance checks" in next_work,
    "next work has stop conditions": "## Stop conditions" in next_work,
    "next work has model route": "## Model route" in next_work,
    "protocol routes all surfaces": all(word in protocol for word in ("Chat", "Work", "Codex")),
    "protocol routes all model tiers": all(word in protocol for word in ("Luna", "Terra", "Sol")),
    "protocol limits passes": "Three passes are the maximum" in protocol,
    "protocol separates research and build": "research and build work in separate contexts" in protocol,
    "template has one deliverable": "## Primary deliverable" in template,
    "template has human gate": "Human review point:" in template,
    "readme exposes operating spine": "documentation/WORK_PROTOCOL.md" in readme,
}

failed = [label for label, ok in checks.items() if not ok]
if failed:
    raise SystemExit("Work-spine validation failed: " + ", ".join(failed))

print(f"Work-spine validation passed ({len(checks)} checks).")
