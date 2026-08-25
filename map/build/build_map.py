#!/usr/bin/env python3
"""Build our map from the Scopus corpus.

    python3 map/build/build_map.py --corpus /path/to/shrunk-corpus

Expects scopus_works.csv and scopus_refs.csv as produced by the shrink step.
Writes map/data/concepts.json and map/data/edges.json.

Nothing from Scopus beyond aggregate counts, DOI handles and years reaches the
public output, and the corpus itself is never committed.
"""
from __future__ import annotations

import argparse, csv, json, re, sys, collections
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vocabulary import SEED, concept_id            # noqa: E402

csv.field_size_limit(2**31 - 1)
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "map" / "data"

# A concept reaches the map on its own literature.
MIN_WORKS = 3
# An edge needs both volume and breadth: enough references, from enough
# different citing works, so one prolific author cannot draw a line.
MIN_EDGE_WEIGHT = 5
MIN_CITING_WORKS = 3

ON_TOPIC = re.compile(
    r"cybernet|general system|systems? theor|systems? approach|systems? research|"
    r"self-organi[sz]|autopoie|requisite variety|homeostat|viable system|"
    r"operational research|operations research|system dynamics|soft systems|"
    r"critical systems|complex(ity)? (system|science|theor)|sense-?making|cynefin|"
    r"systems thinking|systems practice|emergen|resilien|panarchy|"
    r"agent-based|cellular automat|artificial life|network science|complex network|"
    r"nonlinear|non-linear|fractal|dynamical system|scaling law|swarm|synergetic|"
    r"computational social|social simulation|qualitative comparative|case-based|"
    r"econophysic|economic complexity|complexity polic|complexity and (health|education|"
    r"management|psycholog|globali)|applied complexity|philosophy of complexity|"
    r"systems? (biology|science)|data science|big data|multi-?scale",
    re.I,
)
OFF_TOPIC = re.compile(
    r"high energy physics|elementary particle|astrophys|quark|boson|hadron|"
    r"crystal|catalys|alloy|semiconductor|tumou?r|carcinom|clinical trial",
    re.I,
)


def compile_concepts():
    out = []
    for label, aliases, seeded_from in SEED:
        pats = [re.compile(r"(?<![a-z])" + re.escape(a) + r"[a-z]{0,3}(?![a-z])", re.I)
                for a in aliases]
        out.append({"id": concept_id(label), "label": label, "aliases": aliases,
                    "seeded_from": seeded_from, "patterns": pats})
    return out


def match_concepts(text, concepts):
    if not text:
        return []
    return [c["id"] for c in concepts if any(p.search(text) for p in c["patterns"])]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    corpus = Path(a.corpus).expanduser()
    works_csv, refs_csv = corpus / "scopus_works.csv", corpus / "scopus_refs.csv"
    for p in (works_csv, refs_csv):
        if not p.is_file():
            print(f"Not found: {p}", file=sys.stderr)
            return 2

    concepts = compile_concepts()
    by_id = {c["id"]: c for c in concepts}

    # ---- pass 1: which works belong to which concepts -------------------
    work_concepts: dict[str, list[str]] = {}
    stats = {c["id"]: {"works": 0, "years": [], "exemplars": []} for c in concepts}
    on_topic = total = 0
    for w in csv.DictReader(open(works_csv, encoding="utf-8")):
        total += 1
        title, venue = w["title"], w["source_title"]
        if OFF_TOPIC.search(title) or OFF_TOPIC.search(venue):
            continue
        # The vocabulary is the gate. A work is on topic because it matches a
        # concept we are testing, not because it uses the words this project
        # happens to associate with systems research. The earlier hand-written
        # ON_TOPIC filter decided in advance which literatures could be seen,
        # which made concepts outside its wording - human-computer interaction,
        # constructivism, variety engineering - structurally invisible however
        # much literature they had.
        hits = match_concepts(title, concepts)
        if not hits:
            continue
        on_topic += 1
        work_concepts[w["eid"]] = hits
        yr = int(w["year"]) if w["year"].isdigit() else None
        cited = int(w["cited_by"]) if w["cited_by"].isdigit() else 0
        for cid in hits:
            s = stats[cid]
            s["works"] += 1
            if yr:
                s["years"].append(yr)
            if w["doi"]:
                s["exemplars"].append((cited, w["doi"], title[:120], w["year"]))
    print(f"works: {total:,} scanned, {on_topic:,} on topic, "
          f"{len(work_concepts):,} matched at least one concept")

    # ---- pass 2: citations across concepts ------------------------------
    edge_w: collections.Counter = collections.Counter()
    edge_works: dict[tuple, collections.Counter] = collections.defaultdict(collections.Counter)
    edge_years: dict[tuple, list] = collections.defaultdict(list)
    edge_ev: dict[tuple, list] = collections.defaultdict(list)
    scanned = 0
    for r in csv.DictReader(open(refs_csv, encoding="utf-8")):
        scanned += 1
        if scanned % 2_000_000 == 0:
            print(f"  references scanned: {scanned:,}")
        src = work_concepts.get(r["citing_eid"])
        if not src:
            continue
        tgt = match_concepts(r["ref_raw"], concepts)
        if not tgt:
            continue
        ry = int(r["ref_year"]) if r["ref_year"].isdigit() else None
        for s_id in src:
            for t_id in tgt:
                if s_id == t_id:
                    continue
                k = (s_id, t_id)
                edge_w[k] += 1
                edge_works[k][r["citing_eid"]] += 1
                if ry:
                    edge_years[k].append(ry)
                if r["citing_doi"] and len(edge_ev[k]) < 5:
                    candidate = {
                        "citing_doi": r["citing_doi"],
                        "citing_year": r["citing_year"],
                    }
                    if candidate not in edge_ev[k]:
                        edge_ev[k].append(candidate)
    print(f"references scanned: {scanned:,}")

    # ---- assemble -------------------------------------------------------
    nodes = []
    for c in concepts:
        s = stats[c["id"]]
        ex = sorted(s["exemplars"], key=lambda t: -t[0])[:5]
        nodes.append({
            "id": c["id"], "label": c["label"], "aliases": c["aliases"],
            "seeded_from": c["seeded_from"],
            "work_count": s["works"],
            "first_year": min(s["years"]) if s["years"] else None,
            "last_year": max(s["years"]) if s["years"] else None,
            "exemplar_works": [{"doi": d, "title": t, "year": y, "cited_by": n}
                               for n, d, t, y in ex],
            "status": "evidenced" if s["works"] >= MIN_WORKS else "candidate",
        })

    edges = []
    for k, weight in edge_w.items():
        counts = edge_works[k]
        cw = len(counts)
        # How much of this edge rests on its single busiest citing work? A high
        # share means one paper's reference list is carrying the line.
        top_share = round(max(counts.values()) / weight, 3)
        if weight < MIN_EDGE_WEIGHT or cw < MIN_CITING_WORKS:
            continue
        ys = edge_years[k]
        edges.append({
            "source": k[0], "target": k[1],
            "relation_type": "keyword_labelled_citation_signal",
            "plain_phrase": (
                "records whose titles match the source term contain cited-reference "
                "strings matching the target term"
            ),
            "directed": True,
            "weight": weight, "citing_work_count": cw,
            "top_citing_share": top_share,
            "concentrated": top_share >= 0.5,
            "first_year": min(ys) if ys else None,
            "last_year": max(ys) if ys else None,
            "evidence": edge_ev[k],
            "accuracy_status": "aggregate_signal_not_independently_reproduced",
            "scope_conditions": (
                "Keyword matching in one licensed corpus. Not influence, teaching, "
                "agreement, derivation, importance or a clean citation between two "
                "unambiguous literatures."
            ),
        })
    edges.sort(key=lambda e: -e["weight"])

    OUTP = Path(a.out); OUTP.mkdir(parents=True, exist_ok=True)
    meta = {
        "map": "systems, cybernetics and complexity",
        "built_from": "private Scopus corpus; aggregate counts, DOI handles and years only",
        "thresholds": {"min_works": MIN_WORKS, "min_edge_weight": MIN_EDGE_WEIGHT,
                       "min_citing_works": MIN_CITING_WORKS},
        "concept_count": len(nodes),
        "evidenced_concept_count": sum(1 for n in nodes if n["status"] == "evidenced"),
        "edge_count": len(edges),
        "concept_matched_work_count": on_topic,
    }
    (OUTP / "concepts.json").write_text(
        json.dumps({"meta": meta, "concepts": nodes}, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")
    (OUTP / "edges.json").write_text(
        json.dumps({"meta": meta, "edges": edges}, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(json.dumps(meta, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
