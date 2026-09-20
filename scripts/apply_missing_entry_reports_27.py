#!/usr/bin/env python3
"""Close the public content gap behind all fifteen missing-entry reports."""
from pathlib import Path
import hashlib
import html
import json
import re

from apply_iteration_17 import (
    edge_record,
    enc,
    parse,
    profile_record,
    relation_record,
    source_record,
    upsert,
)
from apply_iteration_09 import graph_metrics, make_ai_observations
from apply_relational_depth_16 import calculate_relational_depth, write_relational_document
from apply_doncaster_lineage import refresh_counts
from apply_overnight_review import quality_result
from refresh_graph_snapshot import calculate, write

ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "sources/missing-entry-reports-2026-09-20/review.json"
DATE = "2026-09-20"
RELEASE = "0.27"
MARK = "missing_entry_reports_20260920"
UPDATE_URL = "https://transduction.systems/updates/2026-09-20/"


def add_source(data, item):
    source = source_record(
        item["id"],
        item["title"],
        "primary_public_record",
        item["url"],
        f'{item["locator"]}: {item["notes"]}',
        [],
        item["publisher"],
        DATE,
    )
    source.update(
        last_checked=DATE,
        review_status="source_scope_checked",
        connection_pass=MARK,
    )
    upsert(data["sources"], [source], "id")


def add_report_source(data, item):
    issue = item["issue"]
    source = source_record(
        f"src_reports27_issue_{issue}",
        f'Missing-entry report #{issue}: {item["title"]}',
        "public_submission",
        f"https://github.com/antlerboy/the-necessary-tangle/issues/{issue}",
        "Public report by David Ing. The report prompted research but is not treated as evidence for its own claims.",
        ["David Ing"],
        "The Necessary Tangle public intake",
        DATE,
        quality="B",
    )
    source.update(
        last_checked=DATE,
        review_status="report_reviewed_against_public_sources",
        connection_pass=MARK,
    )
    upsert(data["sources"], [source], "id")
    return source["id"]


def update_profile(data, item, report_source_id):
    node = next((n for n in data["nodes"] if n["id"] == item["node_id"]), None)
    if not node:
        raise ValueError(f'Missing canonical identity for issue {item["issue"]}: {item["node_id"]}')
    source_ids = list(dict.fromkeys([*item["source_ids"], report_source_id]))
    known_sources = {source["id"] for source in data["sources"]}
    missing_sources = set(source_ids) - known_sources
    if missing_sources:
        raise ValueError(f'Unknown sources for issue {item["issue"]}: {sorted(missing_sources)}')
    node.update(
        label=item["title"],
        description=item["summary"],
        canonical_definition=item["summary"],
        publication_level="profile",
        public_stub_text="",
        source_ids=enc(source_ids),
        review_status="source_scoped_report_review_complete",
        reviewed_by="",
        reviewed_at="",
    )
    profile = profile_record(
        item["node_id"],
        item["summary"],
        item["why"],
        item["distinctions"],
        item["lineage"],
        [],
        [],
        item["practice"],
        item["misreadings"],
        item["checks"],
        source_ids,
        context=(
            f'Reviewed from public report #{item["issue"]}. The report is a research prompt; '
            "the profile retains only claims bounded by the cited records."
        ),
        editorial_note=(
            "Prepared with AI assistance from the named public records and the public report. "
            "The report review is complete; open checks are future research, not missing entry work. "
            "Independent specialist review is not recorded."
        ),
    )
    profile.update(
        title=item["title"],
        last_researched=DATE,
        profile_status="source_scoped_report_review_complete",
        review_status="independent_review_not_recorded",
        reviewed_by="",
        reviewed_at="",
        report_issue=item["issue"],
        report_outcome=item["outcome"],
    )
    upsert(data["profiles"], [profile], "node_id")


def add_relations(data, packet):
    if not any(r["relation_type"] == "served_as_president_of" for r in data["relation_types"]):
        upsert(
            data["relation_types"],
            [relation_record(
                "served_as_president_of",
                "documentary",
                "had_president",
                "A dated institutional office-holding record",
                "served as president of",
            )],
            "relation_type",
        )
    known_nodes = {node["id"] for node in data["nodes"]}
    known_sources = {source["id"] for source in data["sources"]}
    for item in packet["relations"]:
        if item["source"] not in known_nodes or item["target"] not in known_nodes:
            raise ValueError(f'Unknown relation endpoint: {item["source"]} -> {item["target"]}')
        if not set(item["source_ids"]) <= known_sources:
            raise ValueError(f'Unknown relation source for {item["source"]} -> {item["target"]}')
        digest = hashlib.sha256(
            f'{item["source"]}|{item["type"]}|{item["target"]}'.encode()
        ).hexdigest()[:20]
        edge = edge_record(
            f"e27_{digest}",
            item["source"],
            item["target"],
            item["type"],
            item["family"],
            item["phrase"],
            item["source_ids"],
            item["locator"],
            item["scope"],
            status="candidate",
            confidence="",
            review_label="Located source statement; independent review not recorded",
        )
        edge.update(reviewed_by="", reviewed_at="", connection_pass=MARK)
        upsert(data["edges"], [edge], "id")


def update_queue(data, packet):
    expected = {item["issue"]: item for item in packet["profiles"]}
    located = set()
    for row in data.get("september_connections", {}).get("queue", []):
        issue = row.get("number")
        if issue not in expected:
            continue
        item = expected[issue]
        if row.get("canonical_id") != item["node_id"]:
            raise ValueError(f'Queue identity mismatch for issue {issue}')
        row.update(
            status="report_review_published",
            latest_review=DATE,
            review_url=UPDATE_URL,
            report_outcome=item["outcome"],
        )
        located.add(issue)
    if located != set(expected):
        raise ValueError(f'Report queue incomplete: {sorted(set(expected) - located)}')


def write_update_page(packet):
    rows = []
    for item in packet["profiles"]:
        entry = f'/#view=item&amp;id={item["node_id"]}'
        issue = f'https://github.com/antlerboy/the-necessary-tangle/issues/{item["issue"]}'
        outcome = "; ".join(
            part.strip().replace("_", " ")
            for part in item["outcome"].split(";")
        )
        rows.append(
            "<tr><td>"
            f'<a href="{entry}">{html.escape(item["title"])}</a>'
            "</td><td>"
            f'<a href="{issue}">#{item["issue"]}</a>'
            "</td><td>"
            f"{html.escape(outcome)}"
            "</td></tr>"
        )
    body = "".join(rows)
    page = f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fifteen missing-entry reports reviewed | The Necessary Tangle</title><link rel="canonical" href="{UPDATE_URL}"><style>body{{font:18px/1.65 Georgia,serif;max-width:960px;margin:auto;padding:24px;background:#faf8f3;color:#292621}}h1{{line-height:1.15}}a{{color:#9a302c;overflow-wrap:anywhere}}table{{border-collapse:collapse;width:100%}}th,td{{text-align:left;vertical-align:top;border-bottom:1px solid #cfc8bb;padding:.75em}}.note{{padding:1em;border-left:3px solid #9a302c;background:#f0ece3}}nav{{display:flex;gap:1em;flex-wrap:wrap}}@media(max-width:650px){{table,tbody,tr,td{{display:block}}thead{{display:none}}td{{border:0;padding:.25em}}tr{{display:block;border-bottom:1px solid #cfc8bb;padding:.75em 0}}}}</style></head><body><nav><a href="/">Atlas</a><a href="/updates/">Updates</a><a href="/reading-list.html">Reading</a></nav><main><h1>Fifteen missing-entry reports reviewed</h1><p>20 September 2026 · Release 0.27</p><p>Every open report titled <em>Missing entry</em> now resolves to a visible, source-scoped atlas profile. The review keeps located contributions and institutional roles, qualifies overstatement, and records the claims which still need publication-level research.</p><h2>How these appeared to be missing</h2><p>The entries themselves had already been created. Seven received profiles in release 0.24. Eight had thinner entries from the earlier source-connection pass. The intake queue recorded this distinction internally, but the GitHub reports remained open because deeper claims were pending. Nothing on the public site or in the issue titles showed that work clearly. This release makes the state visible and treats an open research question as different from a missing entry.</p><table><thead><tr><th>Entry</th><th>Report</th><th>Review outcome</th></tr></thead><tbody>{body}</tbody></table><h2>Editorial boundary</h2><p class="note">A submission is a reason to investigate, not evidence for itself. Office-holding does not prove intellectual importance. Co-location does not prove influence. Mention does not prove lineage. Claims left in each profile's open checks can be researched later without keeping the entry classified as missing.</p><h2>Process correction</h2><p>Future missing-entry intake must show one of three reader-visible states: no canonical identity; an identity with a thin entry; or a source-scoped profile. Once the third state is published, the report closes and any deeper research moves to a separately named task.</p></main></body></html>\n'''
    out = ROOT / "docs/updates/2026-09-20/index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8", newline="\n")


def patch_public_files(packet, metrics):
    marker = "missing-entry-reports-27"
    section = (
        '<section><h2>20 September missing-entry report review</h2>'
        '<p><a href="/updates/2026-09-20/">Fifteen reports now resolve to source-scoped profiles</a></p></section>'
    )
    for filename in ["docs/updates/index.html", "docs/reading-list.html"]:
        path = ROOT / filename
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            rf"<!-- {marker} -->.*?<!-- /{marker} -->",
            "",
            text,
            flags=re.S,
        )
        if "</main>" not in text:
            raise ValueError(f"Missing main landmark: {filename}")
        text = text.replace(
            "</main>",
            f"<!-- {marker} -->{section}<!-- /{marker} --></main>",
            1,
        )
        path.write_text(text, encoding="utf-8", newline="\n")
    sitemap = ROOT / "docs/sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    if UPDATE_URL not in text:
        text = text.replace(
            "</urlset>",
            f"<url><loc>{UPDATE_URL}</loc><lastmod>{DATE}</lastmod></url></urlset>",
        )
    sitemap.write_text(text, encoding="utf-8", newline="\n")
    index = ROOT / "docs/index.html"
    text = index.read_text(encoding="utf-8")
    text = re.sub(r"assets/app.js\?v=[^\"\s]+", "assets/app.js?v=0.27", text)
    text = re.sub(r"assets/public-data.js\?v=[^\"\s]+", "assets/public-data.js?v=0.27", text)
    text = re.sub(r"(<span id=\"releaseBadge\">)Release [^<]+", r"\g<1>Release 0.27", text)
    index.write_text(text, encoding="utf-8", newline="\n")
    note = (
        "Release 0.27 reviews all fifteen open missing-entry reports from issues 69–86. "
        "Every report now resolves to a public profile with evidence boundaries, report provenance, "
        "and explicit open checks. Seven bounded office or contribution statements were added; no "
        "teacher–student, generic influence, priority, or effectiveness relation was inferred. "
        f"Current atlas: {metrics['public_entries']} public entries. See {UPDATE_URL}."
    )
    destinations = [
        ("README.md", "## Release 0.27"),
        ("CHANGELOG.md", "## 0.27 - 20 September 2026"),
        ("documentation/TANGLE_STATE.md", "## Missing-entry report closure, 20 September 2026"),
    ]
    for filename, heading in destinations:
        path = ROOT / filename
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r"\n*" + re.escape(heading) + r"\n.*?(?=\n## |\Z)",
            "",
            text,
            flags=re.S,
        )
        path.write_text(text.rstrip() + f"\n\n{heading}\n\n{note}\n", encoding="utf-8", newline="\n")
    citation = ROOT / "CITATION.cff"
    text = citation.read_text(encoding="utf-8")
    text = re.sub(r"^version:.*$", f"version: {RELEASE}", text, flags=re.M)
    text = re.sub(r"^date-released:.*$", f"date-released: {DATE}", text, flags=re.M)
    citation.write_text(text, encoding="utf-8", newline="\n")


def main():
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    if packet["release"] != RELEASE or packet["date"] != DATE:
        raise ValueError("Packet release identity does not match the applying script")
    issues = [item["issue"] for item in packet["profiles"]]
    expected = [69, 70, 72, 73, 74, 75, 76, 77, 80, 81, 82, 83, 84, 85, 86]
    if issues != expected or len({item["node_id"] for item in packet["profiles"]}) != 15:
        raise ValueError("The bounded fifteen-report cohort changed")
    data = json.loads((ROOT / "data/public-data.json").read_text(encoding="utf-8"))
    for source in packet["new_sources"]:
        add_source(data, source)
    for item in packet["profiles"]:
        report_source_id = add_report_source(data, item)
        update_profile(data, item, report_source_id)
    add_relations(data, packet)
    update_queue(data, packet)
    data[MARK] = {
        "release": RELEASE,
        "date": DATE,
        "url": UPDATE_URL,
        "issues": issues,
        "profiles": [item["node_id"] for item in packet["profiles"]],
        "source_rule": packet["editorial_rule"],
        "independent_review": "not_recorded",
    }
    sources = {source["id"]: source for source in data["sources"]}
    for node in data["nodes"]:
        linked = [sources[sid] for sid in parse(node.get("source_ids")) if sid in sources]
        node["public_source_count"] = sum(s.get("public_link_status") == "public_link" for s in linked)
        node["no_public_link_count"] = sum(s.get("public_link_status") != "public_link" for s in linked)
    refresh_counts(data)
    data["meta"].update(
        release=RELEASE,
        generated=DATE,
        release_digest_url=UPDATE_URL,
        iteration_focus="All fifteen missing-entry reports reviewed and made visible",
        release_note="Every missing-entry report now resolves to a source-scoped profile; deeper research is separated from entry status.",
        node_count=len(data["nodes"]),
        edge_count=len(data["edges"]),
        source_count=len(data["sources"]),
        profile_count=len(data["profiles"]),
    )
    data["relational_depth"] = calculate_relational_depth(data)
    data["relational_depth"].update(release=RELEASE, generated=DATE)
    data["graph_snapshot"] = calculate(data)
    metrics = graph_metrics(data)
    depth = data["relational_depth"]["aggregate"]
    data["meta"].update(
        public_entry_count=metrics["public_entries"],
        described_entry_count=metrics["public_entries"],
        reader_connected_entry_count=depth["reader_connected_entries"],
        semantic_connected_entry_count=depth["semantic_connected_entries"],
        unconnected_entry_count=depth["connection_bands"].get("unconnected", 0),
        semantic_gap_entry_count=metrics["public_entries"] - depth["semantic_connected_entries"],
        public_link_source_count=sum(s.get("public_link_status") == "public_link" for s in data["sources"]),
        no_public_link_source_count=sum(s.get("public_link_status") == "no_public_link" for s in data["sources"]),
    )
    for band in ["rich", "developing", "thin"]:
        data["meta"][f"{band}_entry_count"] = depth["connection_bands"].get(band, 0)
    for key in ["reading_list_inventory", "reading_list_coverage", "core_systems_practice"]:
        data[key]["release"] = RELEASE
    data["ai_observations"].update(release=RELEASE, generated=DATE, metrics=metrics)
    upsert(data["ai_observations"]["observations"], make_ai_observations(metrics)["observations"], "id")
    write(data)
    quality = quality_result(data)
    quality.update(release=RELEASE, generated=DATE)
    for key in ["adversarial_review", "doncaster_lineage_review"]:
        quality[key] = data[key]
    for filename in ["data/relationship-quality.json", "docs/assets/relationship-quality.json"]:
        (ROOT / filename).write_text(
            json.dumps(quality, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    write_relational_document(data)
    write_update_page(packet)
    patch_public_files(packet, metrics)
    print(f"Applied release {RELEASE}: {len(issues)} reports, {len(packet['relations'])} bounded statements")


if __name__ == "__main__":
    main()
