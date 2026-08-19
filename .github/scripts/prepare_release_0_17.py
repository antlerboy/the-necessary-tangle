#!/usr/bin/env python3
from pathlib import Path
import re

SUCCESSOR = '0.17-public-intake-lineage-alpha'
PREDECESSOR = '0.16-grammar-connections-presentation-alpha'

apply_path = Path('scripts/apply_iteration_17.py')
text = apply_path.read_text(encoding='utf-8')
old = '"publication_epistemic_injustice", "Epistemic Injustice", "publication"'
new = '"publication_epistemic_injustice", "Epistemic Injustice: Power and the Ethics of Knowing", "publication"'
if old not in text:
    raise SystemExit('Expected Fricker publication label not found')
apply_path.write_text(text.replace(old, new, 1), encoding='utf-8')

patch17 = Path('scripts/patch_iteration_17.py')
text = patch17.read_text(encoding='utf-8')
marker = '## Current developed route'
replacement = (
    '## Canon and recovery relations\n\n'
    'Release 0.17 makes canon formation and recovery inspectable through typed, source-bearing relations: '
    '`canonised_as`, `excluded_from_canon`, `appropriated_from`, `recovers`, '
    '`participates_in_canon_formation` and `can_exclude`. These lines remain challengeable statements '
    'about particular histories; they are not demographic inference or a new fixed canon.\n\n'
    '## Current developed route'
)
if marker not in text:
    raise SystemExit('Canon document insertion point not found')
patch17.write_text(text.replace(marker, replacement, 1), encoding='utf-8')

ledger = Path('documentation/feedback-ledger.md')
if not ledger.exists():
    ledger.write_text('# Feedback ledger\n', encoding='utf-8')

v13 = Path('scripts/validate_iteration_13.py')
text = v13.read_text(encoding='utf-8')
text, count = re.subn(
    r'expected_date = "2026-08-14" if meta\.get\("release"\) in \{[^\n]+\} else EXPECTED_DATE',
    'expected_date = "2026-08-19" if meta.get("release") == "0.17-public-intake-lineage-alpha" else ("2026-08-14" if meta.get("release") in {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha"} else EXPECTED_DATE)',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('Iteration 0.13 generated-date marker not found')
v13.write_text(text, encoding='utf-8')

v14 = Path('scripts/validate_iteration_14.py')
text = v14.read_text(encoding='utf-8')
old = 'expected_generated = GENERATED if meta.get("release") == RELEASE else FORWARD_GENERATED'
new = 'expected_generated = "2026-08-19" if meta.get("release") == "0.17-public-intake-lineage-alpha" else (GENERATED if meta.get("release") == RELEASE else FORWARD_GENERATED)'
if old not in text:
    raise SystemExit('Iteration 0.14 generated-date marker not found')
v14.write_text(text.replace(old, new, 1), encoding='utf-8')

v15 = Path('scripts/validate_iteration_15.py')
text = v15.read_text(encoding='utf-8')
old = "assert meta['generated']=='2026-08-14'"
new = "assert meta['generated']==('2026-08-19' if meta['release']=='0.17-public-intake-lineage-alpha' else '2026-08-14')"
if old not in text:
    raise SystemExit('Iteration 0.15 generated-date marker not found')
v15.write_text(text.replace(old, new, 1), encoding='utf-8')

map_hotfix = Path('scripts/validate_map_usability_hotfix.py')
text = map_hotfix.read_text(encoding='utf-8')
old = "assert 'assets/app.js?v=0.16.3-visual' in index"
new = "assert 'assets/app.js?v=' in index"
if old not in text:
    raise SystemExit('Map hotfix asset-version marker not found')
map_hotfix.write_text(text.replace(old, new, 1), encoding='utf-8')

release_pattern = re.compile(
    rf"(?P<quote>['\"]){re.escape(PREDECESSOR)}(?P=quote)(?=\s*\}})"
)

def add_successor(match: re.Match[str]) -> str:
    quote = match.group('quote')
    return f'{quote}{PREDECESSOR}{quote}, {quote}{SUCCESSOR}{quote}'

for validator in Path('scripts').glob('validate_*.py'):
    text = validator.read_text(encoding='utf-8')
    text = release_pattern.sub(add_successor, text)
    validator.write_text(text, encoding='utf-8')

sync = Path('scripts/sync_release_docs_17.py')
sync_script = '''#!/usr/bin/env python3
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
updated, count = re.subn(r"Generated for release `[^`]+` on \\d{4}-\\d{2}-\\d{2}\\.", line, text, count=1)
if not count:
    lines = text.splitlines()
    insert_at = 1 if lines and lines[0].startswith("#") else 0
    lines.insert(insert_at, "")
    lines.insert(insert_at + 1, line)
    updated = "\\n".join(lines)
path.write_text(updated.rstrip() + "\\n", encoding="utf-8")

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
print(f"Synced maintained release documents for {RELEASE}")
'''
sync.write_text(sync_script, encoding='utf-8')

makefile = Path('Makefile')
text = makefile.read_text(encoding='utf-8')
marker = '\tpython3 scripts/patch_iteration_17.py\n\tpython3 scripts/build_public_knowledge.py'
replacement = '\tpython3 scripts/patch_iteration_17.py\n\tpython3 scripts/sync_release_docs_17.py\n\tpython3 scripts/build_public_knowledge.py'
if marker not in text:
    raise SystemExit('Makefile 0.17 patch marker not found')
makefile.write_text(text.replace(marker, replacement, 1), encoding='utf-8')
