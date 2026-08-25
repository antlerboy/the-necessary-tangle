#!/usr/bin/env python3
"""Extend retained historical validation contracts to recognise release 0.18."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = '"0.17-public-intake-lineage-alpha"'
NEW = '"0.18-navigable-tangle-alpha"'
READING_RELEASES_17 = 'if release in {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha"}:'
READING_RELEASES_18 = 'if release in {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha"}:'
V13_DATE_17 = 'expected_date = "2026-08-19" if meta.get("release") == "0.17-public-intake-lineage-alpha" else ("2026-08-14" if meta.get("release") in {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha"} else EXPECTED_DATE)'
V13_DATE_18 = 'expected_date = "2026-08-23" if meta.get("release") == "0.18-navigable-tangle-alpha" else ("2026-08-19" if meta.get("release") == "0.17-public-intake-lineage-alpha" else ("2026-08-14" if meta.get("release") in {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha"} else EXPECTED_DATE))'
V13_LEDGER_17 = 'if meta.get("release") != "0.17-public-intake-lineage-alpha" and (ROOT / "documentation" / "feedback-ledger.md").exists():'
V13_LEDGER_18 = 'if meta.get("release") not in {"0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha"} and (ROOT / "documentation" / "feedback-ledger.md").exists():'
V14_FORWARD_17 = 'FORWARD_RELEASES = {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha"}'
V14_FORWARD_18 = 'FORWARD_RELEASES = {"0.15-ing-reading-practice-alpha", "0.16-grammar-connections-presentation-alpha", "0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha"}'
V14_DATE_17 = 'expected_generated = "2026-08-19" if meta.get("release") == "0.17-public-intake-lineage-alpha" else (GENERATED if meta.get("release") == RELEASE else FORWARD_GENERATED)'
V14_DATE_18 = 'expected_generated = "2026-08-23" if meta.get("release") == "0.18-navigable-tangle-alpha" else ("2026-08-19" if meta.get("release") == "0.17-public-intake-lineage-alpha" else (GENERATED if meta.get("release") == RELEASE else FORWARD_GENERATED))'
V15_META_17 = "meta=D['meta']; assert meta['release'] in {'0.15-ing-reading-practice-alpha','0.16-grammar-connections-presentation-alpha', '0.17-public-intake-lineage-alpha'}; assert meta['generated']==('2026-08-19' if meta['release']=='0.17-public-intake-lineage-alpha' else '2026-08-14')"
V15_META_18 = "meta=D['meta']; assert meta['release'] in {'0.15-ing-reading-practice-alpha','0.16-grammar-connections-presentation-alpha', '0.17-public-intake-lineage-alpha', '0.18-navigable-tangle-alpha'}; assert meta['generated']==('2026-08-23' if meta['release']=='0.18-navigable-tangle-alpha' else ('2026-08-19' if meta['release']=='0.17-public-intake-lineage-alpha' else '2026-08-14'))"
V17_CITATION_OLD = 'if f"version: {RELEASE}" not in citation or f"date-released: {GENERATED}" not in citation or f"url: {PUBLIC_URL}" not in citation:'
V17_CITATION_NEW = 'if f"version: {meta.get(\'release\')}" not in citation or f"date-released: {meta.get(\'generated\')}" not in citation or f"url: {PUBLIC_URL}" not in citation:'
V17_README_OLD = 'if "Release 0.17 contains" not in readme or "https://transduction.systems/submissions/" not in readme or "https://transduction.systems/canon-and-lineage/" not in readme:'
V17_README_NEW = 'if ("## Release 0.18" not in readme and "Release 0.17 contains" not in readme) or "https://transduction.systems/" not in readme:'

changed = []
already = []
for path in sorted((ROOT / "scripts").glob("validate*.py")):
    text = path.read_text(encoding="utf-8")
    original = text

    # A later release may already have extended a historical validator beyond
    # 0.18. In that case the 0.18 compatibility work is necessarily present;
    # do not demand the exact intermediate 0.17/0.18 strings again.
    if "0.19-living-marks-alpha" in text:
        already.append(path.name)
        continue

    if NEW in text:
        already.append(path.name)
    else:
        lines = text.splitlines(keepends=True)
        for index, line in enumerate(lines):
            if "ALLOWED_RELEASES" not in line or OLD not in line:
                continue
            if "{" not in line or "}" not in line:
                raise SystemExit(f"Unsupported multi-line ALLOWED_RELEASES declaration in {path.name}")
            lines[index] = line.replace(OLD, f"{OLD}, {NEW}", 1)
            text = "".join(lines)
            break

    if path.name == "validate_iteration_12.py":
        if READING_RELEASES_18 not in text:
            if READING_RELEASES_17 not in text:
                raise SystemExit("The 0.12 reading-list status condition has changed unexpectedly")
            text = text.replace(READING_RELEASES_17, READING_RELEASES_18, 1)

    if path.name == "validate_iteration_13.py":
        if V13_DATE_18 not in text:
            if V13_DATE_17 not in text:
                raise SystemExit("The 0.13 generation-date condition has changed unexpectedly")
            text = text.replace(V13_DATE_17, V13_DATE_18, 1)
        if V13_LEDGER_18 not in text:
            if V13_LEDGER_17 not in text:
                raise SystemExit("The 0.13 feedback-ledger condition has changed unexpectedly")
            text = text.replace(V13_LEDGER_17, V13_LEDGER_18, 1)

    if path.name == "validate_iteration_14.py":
        if V14_FORWARD_18 not in text:
            if V14_FORWARD_17 not in text:
                raise SystemExit("The 0.14 forward-release set has changed unexpectedly")
            text = text.replace(V14_FORWARD_17, V14_FORWARD_18, 1)
        if V14_DATE_18 not in text:
            if V14_DATE_17 not in text:
                raise SystemExit("The 0.14 generation-date condition has changed unexpectedly")
            text = text.replace(V14_DATE_17, V14_DATE_18, 1)

    if path.name == "validate_iteration_15.py":
        if V15_META_18 not in text:
            if V15_META_17 not in text:
                raise SystemExit("The 0.15 successor-release assertion has changed unexpectedly")
            text = text.replace(V15_META_17, V15_META_18, 1)

    if path.name == "validate_iteration_16.py":
        text = text.replace(
            'if meta.get("release") not in {RELEASE, "0.17-public-intake-lineage-alpha"}:',
            'if meta.get("release") not in {RELEASE, "0.17-public-intake-lineage-alpha", "0.18-navigable-tangle-alpha"}:',
            1,
        )
        text = text.replace(
            'if meta.get("generated") not in {GENERATED, "2026-08-19"}:',
            'if meta.get("generated") not in {GENERATED, "2026-08-19", "2026-08-23"}:',
            1,
        )
        for asset in ("styles.css", "site-enhancements.css", "app.js"):
            text = text.replace(
                f'assets/{asset}?v=0.17.0-public',
                f'assets/{asset}?v=0.18.0-public',
            )

    if path.name == "validate_iteration_17.py":
        text = text.replace('VERSION = "0.17.0-public"', 'VERSION = "0.18.0-public"', 1)
        text = text.replace(
            'if meta.get("release") != RELEASE:',
            'if meta.get("release") not in {RELEASE, "0.18-navigable-tangle-alpha"}:',
            1,
        )
        text = text.replace(
            'if meta.get("generated") != GENERATED:',
            'if meta.get("generated") not in {GENERATED, "2026-08-23"}:',
            1,
        )
        text = text.replace(
            'if submissions.get("release") != RELEASE or submissions.get("marker") != "Prepared from The Necessary Tangle":',
            'if submissions.get("release") not in {RELEASE, "0.18-navigable-tangle-alpha"} or submissions.get("marker") != "Prepared from The Necessary Tangle":',
            1,
        )
        if V17_CITATION_NEW not in text:
            if V17_CITATION_OLD not in text:
                raise SystemExit("The 0.17 citation assertion has changed unexpectedly")
            text = text.replace(V17_CITATION_OLD, V17_CITATION_NEW, 1)
        if V17_README_NEW not in text:
            if V17_README_OLD not in text:
                raise SystemExit("The 0.17 README assertion has changed unexpectedly")
            text = text.replace(V17_README_OLD, V17_README_NEW, 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        changed.append(path.name)

if not changed and not already:
    raise SystemExit("No historical validator contract recognised for 0.18 compatibility")

print("0.18 validator compatibility:")
print("- extended: " + (", ".join(sorted(set(changed))) if changed else "none"))
print("- already compatible: " + (", ".join(sorted(set(already))) if already else "none"))
