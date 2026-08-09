#!/usr/bin/env python3
"""Apply public-release metadata, corpus registrations and canonical URLs.

The base enrichment script remains intentionally focused on entry descriptions and
search hygiene. This small, idempotent pass records release-level decisions that
change more often: ownership, public wording, licensing and named corpus work.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"

RELEASE = "0.6-feedback-alpha"
GENERATED = "2026-08-09"
PROJECT_URL = "https://antlerboy.github.io/the-necessary-tangle/"
REPOSITORY_URL = "https://github.com/antlerboy/the-necessary-tangle"
AUTHOR_URL = "https://www.antlerboy.com/"
LICENCE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"

CORPUS_SOURCES: list[dict[str, Any]] = [
    {
        "id": "src_foundational_papers_complexity_science",
        "title": "Foundational Papers in Complexity Science",
        "source_type": "public_compendium",
        "quality_tier": "B",
        "access": "public",
        "url": "https://www.fondationborel.org/wp-content/uploads/2018/04/Foundation-Papers-in-Complexity-Science.pdf",
        "date": "2018",
        "notes": "Named comparison and ingestion corpus. The public PDF is registered now; item-level inventory, summaries, source tracing and mapping are tracked in issue 3.",
        "creators": "[\"David C. Krakauer (editor)\"]",
        "publisher": "Santa Fe Institute; public mirror hosted by Fondation Borel",
        "licence": "source_terms",
        "review_status": "registered_for_corpus_pass",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_monoskop_relevant_corpus",
        "title": "Monoskop — relevant systems | cybernetics | complexity corpus",
        "source_type": "public_reference_corpus",
        "quality_tier": "C",
        "access": "public",
        "url": "https://monoskop.org/",
        "date": "",
        "notes": "Public discovery and reference corpus. Relevance, original-source replacement, copyright and boundary decisions are tracked in issue 4; inclusion here does not imply that the whole site has been ingested.",
        "creators": "[\"Monoskop contributors\"]",
        "publisher": "Monoskop",
        "licence": "source_terms",
        "review_status": "registered_for_corpus_pass",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_syscoi_stream_archive",
        "title": "Systems Community of Inquiry public archive",
        "source_type": "public_community_archive",
        "quality_tier": "C",
        "access": "public",
        "url": "https://stream.syscoi.com/",
        "date": "2018–",
        "notes": "Evidence of curation, circulation, interpretation and discussion. It is a discovery and historical source, not automatic proof of intellectual influence or priority. Structured archive work is tracked in issue 5.",
        "creators": "[\"Benjamin P Taylor\", \"David Ing\", \"community contributors\"]",
        "publisher": "Systems Community of Inquiry",
        "licence": "source_terms",
        "review_status": "registered_for_archive_pass",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_model_report_archive",
        "title": "Preserved model.report archive",
        "source_type": "public_community_archive",
        "quality_tier": "C",
        "access": "public",
        "url": "https://syscoi.com/model.report/model.report/newest.html",
        "date": "2014–2018",
        "notes": "Preserved static archive of the earlier model.report community. Use requires care about missing functionality, deleted material and the difference between posting, discussion, collaboration and influence. Structured archive work is tracked in issue 5.",
        "creators": "[\"Scott Fortmann-Roe\", \"Gene Bellinger\", \"Benjamin P Taylor\", \"model.report contributors\"]",
        "publisher": "Systems Community of Inquiry archive",
        "licence": "source_terms",
        "review_status": "registered_for_archive_pass",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_castellani_map_complexity_sciences",
        "title": "Map of the Complexity Sciences",
        "source_type": "public_comparator_map",
        "quality_tier": "C",
        "access": "public",
        "url": "https://commons.wikimedia.org/wiki/File:Map_of_the_Complexity_Sciences.svg",
        "date": "2012",
        "notes": "Brian Castellani's conceptual and historical map is registered as a major comparator. Its purpose, categories, boundaries and kinds of line will be analysed in issue 6.",
        "creators": "[\"Brian Castellani\"]",
        "publisher": "Wikimedia Commons",
        "licence": "CC BY-SA 3.0",
        "review_status": "registered_for_comparator_pass",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_taylor_castellani_critique_2019",
        "title": "Why I hope we could do better than the Castellani complexity map",
        "source_type": "public_editorial_critique",
        "quality_tier": "C",
        "access": "public",
        "url": "https://stream.syscoi.com/2019/12/21/why-i-hope-we-could-do-better-than-the-castellani-complexity-map/",
        "date": "2019-12-21",
        "notes": "Benjamin P Taylor's public critique is evidence of the design problem and the curator's position, not independent validation of The Necessary Tangle. It is paired with the original comparator in issue 6.",
        "creators": "[\"Benjamin P Taylor\"]",
        "publisher": "Systems Community of Inquiry",
        "licence": "source_terms",
        "review_status": "registered_for_comparator_pass",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
]

CORPUS_REGISTER = [
    {
        "id": "corpus_foundational_complexity_papers",
        "label": "Foundational Papers in Complexity Science",
        "status": "registered_not_yet_itemised",
        "issue_url": f"{REPOSITORY_URL}/issues/3",
        "source_ids": ["src_foundational_papers_complexity_science"],
        "completion_test": "Readable item-level contents guide, summaries, links, mapped concepts and people, and explicit omissions.",
    },
    {
        "id": "corpus_monoskop",
        "label": "Relevant Monoskop material",
        "status": "registered_not_yet_systematically_reviewed",
        "issue_url": f"{REPOSITORY_URL}/issues/4",
        "source_ids": ["src_monoskop_relevant_corpus"],
        "completion_test": "Documented search scope, admissions, exclusions, original-source replacements and remaining work.",
    },
    {
        "id": "corpus_syscoi_model_report",
        "label": "SysCoI and model.report archives",
        "status": "registered_not_yet_systematically_ingested",
        "issue_url": f"{REPOSITORY_URL}/issues/5",
        "source_ids": ["src_syscoi_stream_archive", "src_model_report_archive"],
        "completion_test": "Repeatable archival ingestion with typed provenance and no confusion of circulation with influence.",
    },
    {
        "id": "corpus_comparator_maps",
        "label": "Prior maps and bodies of knowledge",
        "status": "registered_comparator_pass_pending",
        "issue_url": f"{REPOSITORY_URL}/issues/6",
        "source_ids": ["src_castellani_map_complexity_sciences", "src_taylor_castellani_critique_2019"],
        "completion_test": "Public comparison of purpose, boundary, categories, lines, evidence, strengths and failures.",
    },
    {
        "id": "corpus_practitioner_lineage",
        "label": "Practitioner influence constellations",
        "status": "relation_model_and_pilots_pending",
        "issue_url": f"{REPOSITORY_URL}/issues/7",
        "source_ids": [],
        "completion_test": "Gold-standard practitioner constellations with separately evidenced teaching, collaboration, citation and influence.",
    },
    {
        "id": "corpus_company_knowledge",
        "label": "Company-knowledge discovery",
        "status": "private_discovery_pass_pending",
        "issue_url": f"{REPOSITORY_URL}/issues/8",
        "source_ids": [],
        "completion_test": "No private material published; useful leads replaced by public evidence or proper No-public-link citations.",
    },
]


def upsert_sources(
    existing: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    """Merge registered corpora without creating duplicate URLs.

    The base dataset already contains some of these sources under earlier IDs.
    Return a requested-ID to canonical-ID map so the corpus register always
    points at the source record that actually survives the merge.
    """
    by_id = {source.get("id"): dict(source) for source in existing if source.get("id")}
    id_by_url = {
        str(source.get("url") or "").rstrip("/"): source.get("id")
        for source in existing
        if source.get("id") and source.get("url")
    }
    canonical_id_by_requested_id: dict[str, str] = {}

    for source in CORPUS_SOURCES:
        url_key = str(source.get("url") or "").rstrip("/")
        target_id = id_by_url.get(url_key) or source["id"]
        canonical_id_by_requested_id[source["id"]] = target_id
        merged = {**by_id.get(target_id, {}), **source, "id": target_id}
        by_id[target_id] = merged
        if url_key:
            id_by_url[url_key] = target_id

    return list(by_id.values()), canonical_id_by_requested_id


def resolved_corpus_register(canonical_ids: dict[str, str]) -> list[dict[str, Any]]:
    register: list[dict[str, Any]] = []
    for corpus in CORPUS_REGISTER:
        resolved = dict(corpus)
        resolved["source_ids"] = [
            canonical_ids.get(source_id, source_id) for source_id in corpus.get("source_ids", [])
        ]
        register.append(resolved)
    return register


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = data.setdefault("meta", {})
    meta.update(
        {
            "project": "The Necessary Tangle",
            "subtitle": "A living evidence atlas of systems | cybernetics | complexity",
            "tagline": "Every connection must say what it means.",
            "release": RELEASE,
            "generated": GENERATED,
            "status": "public alpha on GitHub Pages",
            "author": "Benjamin P Taylor",
            "author_role": "curator",
            "author_url": AUTHOR_URL,
            "project_url": PROJECT_URL,
            "repository_url": REPOSITORY_URL,
            "content_licence": "CC BY-SA 4.0",
            "content_licence_url": LICENCE_URL,
            "coverage_status": "Broad seed coverage; evidence depth remains uneven. See the public coverage programme and linked issues.",
            "source_policy": "Public links are used where they exist. Published material without an open copy is cited as 'No public link'. Private research may identify leads, but private URLs and extracts are not published.",
        }
    )

    data["sources"], canonical_source_ids = upsert_sources(data.get("sources", []))
    data["corpus_register"] = resolved_corpus_register(canonical_source_ids)

    meta["source_count"] = len(data["sources"])
    meta["public_link_source_count"] = sum(1 for source in data["sources"] if source.get("url"))
    meta["no_public_link_source_count"] = sum(1 for source in data["sources"] if not source.get("url"))
    meta["corpus_register_count"] = len(data["corpus_register"])

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    print(
        f"Applied {RELEASE}: {meta.get('public_entry_count')} public entries, "
        f"{meta['source_count']} sources and {meta['corpus_register_count']} named coverage programmes."
    )


if __name__ == "__main__":
    main()
