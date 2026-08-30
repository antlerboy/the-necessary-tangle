#!/usr/bin/env python3
"""Prepare 0.20.3 reader-only HTML changes in the deployment artefact.

The project keeps docs/index.html as the maintained interface source. This script
performs small deterministic release-time edits which must also be present for
non-JavaScript readers and crawlers, and stamps cache-busters on changed reader
scripts. It is intentionally narrow and fails if the expected source text drifts.
"""

from pathlib import Path

INDEX = Path("docs/index.html")

REPLACEMENTS = {
    "This release also develops Peter Checkland, Werner Ulrich, Ray Ison, Ed Straw, Raul Espejo, Alfonso Reyes, Donella Meadows, Diana Wright and Barry Oshry through public primary or official sources, distinct method entries and typed practice relations.":
        "Developed coverage includes Peter Checkland, Werner Ulrich, Ray Ison, Ed Straw, Raul Espejo, Alfonso Reyes, Donella Meadows, Diana Wright and Barry Oshry through public primary or official sources, distinct method entries and typed practice relations.",
    "The requested people and institutions are now resolved through canonical names and search aliases, with their actual source and connection depth exposed. The 32 concepts in the unFIX synthesis each resolve to an atlas entry without treating that AI-assisted list as a settled canon.":
        "Named people and institutions in the post-0.17 coverage pass resolve through canonical names and search aliases, with their actual source and connection depth exposed. The 32 concepts in the unFIX synthesis each resolve to an atlas entry without treating that AI-assisted list as a settled canon.",
    "A field needs distinctions and boundaries. It does not need to pretend those boundaries arrived from nowhere. This release distinguishes coherence from impermeability and demographic inclusion from the harder work of changing who can affect categories, evidence and intellectual lineage.":
        "A field needs distinctions and boundaries. It does not need to pretend those boundaries arrived from nowhere. The editorial model distinguishes coherence from impermeability and demographic inclusion from the harder work of changing who can affect categories, evidence and intellectual lineage.",
    "The atlas now separates the people, papers, framework, tools, organisation and public source corpora around Cynefin. Dave Snowden's author archive is a primary record of his dated public arguments. Cynefin.io is the project's current collaborative semantic network. Neither source is treated as independent proof of influence, priority or effectiveness.":
        "The atlas separates the people, papers, framework, tools, organisation and public source corpora around Cynefin. Dave Snowden's author archive is a primary record of his dated public arguments. Cynefin.io is the project's current collaborative semantic network. Neither source is treated as independent proof of influence, priority or effectiveness.",
    '<script src="assets/site-config.js"></script>':
        '<script src="assets/site-config.js?v=0.20.3-reader-scio"></script>',
    '<script src="assets/site-enhancements.js"></script>':
        '<script src="assets/site-enhancements.js?v=0.20.3-reader-scio"></script>',
}


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    missing = [source for source in REPLACEMENTS if source not in text]
    if missing:
        raise SystemExit(
            "Reader deployment source drifted; expected text was not found:\n- "
            + "\n- ".join(missing)
        )
    for source, target in REPLACEMENTS.items():
        text = text.replace(source, target, 1)
    INDEX.write_text(text, encoding="utf-8")
    print(f"Prepared {INDEX} for 0.20.3 reader deployment")


if __name__ == "__main__":
    main()
