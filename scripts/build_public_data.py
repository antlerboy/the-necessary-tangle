#!/usr/bin/env python3
"""Normalise and publish The Necessary Tangle public dataset.

The canonical public dataset lives at data/public-data.json. This script is
idempotent: it applies the naming, source and search-hygiene rules, validates
public-source exposure, and writes the browser copies under docs/assets/.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"

PROJECT = "The Necessary Tangle"
SITE_URL = "https://antlerboy-benjamintaylor.github.io/the-necessary-tangle/"
REPO_URL = "https://github.com/antlerboy-benjamintaylor/the-necessary-tangle"

LAW_DESCRIPTIONS = {
    "law_or_principle_law_of_calling": "The Law of Calling says that identifying a system requires drawing a distinction: a boundary separates what is being treated as the system from its environment. The chosen name and boundary shape what can then be noticed and acted upon.",
    "law_or_principle_viability_principle": "The Viability Principle treats continued existence as a dynamic balance: sub-systems need enough autonomy while the whole retains cohesion, and the system needs enough stability while remaining able to adapt over time.",
    "law_or_principle_homeostasis_principle": "The Homeostasis Principle says that a system remains stable only while its essential variables stay within viable limits. Regulation is therefore concerned with keeping those variables inside a tolerable range, not freezing the system in one exact state.",
    "law_or_principle_system_stability_principle": "The System Stability Principle says that something is recognisable as a system only when a pattern of relationships persists across repeated observations. Stability here means persistence of pattern, not the absence of movement.",
    "law_or_principle_law_of_requisite_variety": "The Law of Requisite Variety limits what regulation can achieve: only regulatory variety can counter disturbance variety. The relevant varieties depend on the defined regulation problem, available responses and acceptable outcomes.",
    "law_or_principle_first_circular_causality_principle": "The First Circular Causality Principle concerns positive feedback. Mutually amplifying changes can drive escalation, so similar initial conditions may lead to radically different outcomes once reinforcing loops take hold.",
    "law_or_principle_second_circular_causality_principle": "The Second Circular Causality Principle concerns negative feedback. Mutual correction can drive a system towards an equilibrium across a wide range of starting conditions; the resulting stability may be desirable or obstructive.",
    "law_or_principle_law_of_crossing": "The Law of Crossing says that crossing a system boundary changes state and viewpoint. Defining or observing a system from inside is not equivalent to doing so from outside, and each position permits some distinctions while excluding others.",
    "law_or_principle_network_power_law": "The Network Power Law draws attention to the rapid growth of possible relationships as the number of elements increases. Connectivity may create utility, but it also produces structural complexity faster than simple element counts suggest.",
    "law_or_principle_system_survival_theorem": "The System Survival Theorem says that a system cannot remain viable indefinitely if its relevant environment changes consistently faster than the system can adapt. The comparison must be made at a stated scale and time horizon.",
    "law_or_principle_system_resonance_principle": "The System Resonance Principle proposes that communication and relation are easier where systems share relevant structural or dynamic similarities. Where those similarities are absent, signals are more likely to be lost or transformed in translation.",
    "law_or_principle_power_structuration_theorem": "The Power Structuration Theorem says that agency must be balanced across recursive levels. A whole needs enough power to act as a whole, while its constituent sub-systems need enough autonomy to meet the demands that fall on them.",
    "law_or_principle_conservation_of_adaptation_principle": "The Conservation of Adaptation Principle says that continued existence requires ongoing change in the relationship between a system and its environment. What a system is cannot be separated entirely from the environment in which it persists.",
    "law_or_principle_darkness_principle": "The Darkness Principle says that no system can be known completely. Models are therefore necessary selective constructions, and responsible intervention requires explicit uncertainty rather than a pretence of exhaustive knowledge.",
    "law_or_principle_adams_third_law": "Adams' Third Law warns that selecting components because each appears low-risk in isolation can create a high-risk system. Systemic risk depends on fit, interdependence and context, not merely on the local reliability of parts.",
    "law_or_principle_self_organised_criticality": "Self-Organised Criticality describes systems whose own interactions accumulate tensions or dependencies that make abrupt reorganisation or collapse increasingly likely. The critical condition is produced within the system rather than imposed only from outside.",
    "law_or_principle_complexity_instability_principle": "The Complexity Instability Principle says that systems with too many active or changing interdependencies tend towards instability. Appropriate grouping, modularity and constraints can reduce the number of relationships that must change together.",
    "law_or_principle_order_osmosis_principle": "The Order Osmosis Principle proposes that, where more and less organised systems sit beside one another, people, resources or functions tend to migrate towards the more ordered system. This can further weaken the less stable neighbour.",
    "law_or_principle_first_black_box_principle": "The First Black Box Principle says that it is not always necessary to know a sub-system's internal mechanism in order to understand the function it performs, provided its relevant conditions, inputs and outputs are sufficiently reliable.",
    "law_or_principle_second_black_box_principle": "The Second Black Box Principle says that the possible variety of a sub-system's outputs can sometimes be assessed without opening the box. This permits selective modelling, but only under the conditions for which the observed behaviour holds.",
    "law_or_principle_self_organising_principle": "The Self-Organising Principle concerns the generation of higher-level order through interactions among parts, and the continuing reorganisation of an existing whole. It is not merely a synonym for teams managing themselves.",
    "law_or_principle_law_of_reciprocity_of_connections": "The Law of Reciprocity of Connections says that relationships should be examined as mutual rather than one-way: if A acts on B, B's response changes the situation for A. Actions in connected systems return as consequences.",
    "law_or_principle_redundancy_of_potential_command_principle": "The Redundancy of Potential Command Principle says that effective action in a complex decision network depends on bringing the right information together where and when it is needed. Command potential is therefore distributed rather than fixed permanently in one role.",
    "law_or_principle_root_structuring_theorem": "The Root Structuring Theorem proposes that structural complexity can be reduced by grouping elements into a balanced number of sub-systems at successive levels, with the square-root relationship offered as a guide rather than a universal organisation chart.",
    "law_or_principle_structural_viability_theorem": "The Structural Viability Theorem says that a system and its constituent sub-systems need rates of change fitted to their respective environments. Viability suffers when one recursive level cannot change at the pace demanded of it.",
    "law_or_principle_steady_state_principle": "The Steady State Principle links the equilibrium of a system to the equilibria of its sub-systems and vice versa. A steady state is a maintained dynamic balance, not motionless stasis.",
    "law_or_principle_law_of_sufficient_complexity": "The Law of Sufficient Complexity says that a complex system's behaviour follows from how the system is constituted. Reliable change in behaviour usually requires change to structure, relationships, constraints or inputs, not exhortation alone.",
    "law_or_principle_fractal_principle": "The Fractal Principle proposes that systems tend to reproduce aspects of their own form when they create sub-systems. The claim concerns recurring organisational pattern; it should not be confused with exact mathematical fractal geometry.",
    "law_or_principle_relaxation_time_principle": "The Relaxation Time Principle says that a system repeatedly disturbed before it has recovered may never stabilise. The interval between disturbances therefore matters as much as the severity of each disturbance.",
    "law_or_principle_scaling_stasis_principle": "The Scaling Stasis Principle says that growth usually adds environmental exposure, internal interdependence and constraints. As a system becomes larger and more complex, those constraints can reduce its capacity to adapt.",
    "law_or_principle_conant_ashby_theorem": "The Conant–Ashby theorem states, under the assumptions of the original formal paper, that the simplest optimal regulator must embody a model of what it regulates. Popular uses should not erase those assumptions or turn every useful representation into a proof of optimal control.",
    "law_or_principle_feedback_dominance_theorem": "The Feedback Dominance Theorem says that sufficiently strong feedback can dominate system behaviour across substantial variation in initial input. In such cases, changing the input alone may have little effect on the resulting trajectory.",
    "law_or_principle_principle_of_emergence": "The Principle of Emergence concerns properties or behaviours of a whole that are not properties of its parts in isolation. Understanding them requires attention to organisation, interaction and level, not only decomposition.",
}

PERSON_DESCRIPTIONS = {
    "person_kurt_gödel": "Kurt Gödel was a logician whose work on completeness, incompleteness and set theory transformed mathematical logic. Later systems writers sometimes extend his results metaphorically; those extensions require separate argument.",
    "person_julian_bigelow": "Julian Bigelow was an engineer and mathematician who co-authored the 1943 paper 'Behavior, Purpose and Teleology' with Arturo Rosenblueth and Norbert Wiener, an important precursor to early cybernetics.",
    "person_roger_c_conant": "Roger C. Conant was a cybernetician who co-authored the 1970 good regulator theorem with W. Ross Ashby, linking effective regulation to a model of the system being regulated under stated formal assumptions.",
}

MANUAL_ALIASES = {
    "concept_boundary": ["boundaries", "system boundary", "boundary judgement", "boundary judgment"],
    "concept_feedback": ["feedback loop", "feedback loops"],
    "concept_feedforward": ["feed-forward"],
    "concept_negative_feedback": ["balancing feedback", "error-correcting feedback"],
    "concept_positive_feedback": ["reinforcing feedback", "amplifying feedback"],
    "concept_non_linearity": ["nonlinearity", "non-linear", "nonlinear"],
    "concept_self_organisation": ["self-organization", "self organisation", "self organization"],
    "concept_organisational_recursion": ["organizational recursion"],
    "concept_requisite_variety": ["Ashby's law"],
    "concept_viability": ["system viability", "viable system"],
    "law_or_principle_conant_ashby_theorem": ["good regulator theorem", "Conant-Ashby theorem"],
    "method_or_methodology_viable_system_model_vsm": ["VSM", "viable systems model"],
    "method_or_methodology_soft_systems_methodology_ssm": ["SSM", "soft systems method"],
    "method_or_methodology_critical_systems_heuristics_csh": ["CSH", "critical systems heuristic"],
    "method_or_methodology_system_dynamics": ["SD", "system dynamics modelling", "system dynamics modeling"],
    "method_or_methodology_syntegration_team_syntegrity": ["Team Syntegrity", "Syntegration"],
    "tradition_cybernetics": ["cybernetic", "control and communication"],
}

NEW_SOURCES = [
    {
        "id": "src_salah_grammar_part1_2022",
        "title": "Cybersecurity Lessons from The Grammar of Systems, part 1",
        "source_type": "public_secondary_summary",
        "quality_tier": "C",
        "access": "public",
        "url": "https://www.linkedin.com/pulse/cybersecurity-lessons-from-grammar-systems-order-chaos-osama-salah/",
        "date": "2022-05-16",
        "notes": "Public secondary summary of Grammar of Systems items 1–11. Used as an accessible orientation aid; the book remains the controlling source.",
        "creators": "[\"Osama Salah\"]",
        "publisher": "LinkedIn",
        "licence": "publisher_terms",
        "review_status": "checked",
        "last_checked": "2026-08-09",
        "public_link_status": "public_link",
    },
    {
        "id": "src_salah_grammar_part2_2022",
        "title": "Cybersecurity Lessons from The Grammar of Systems, part 2",
        "source_type": "public_secondary_summary",
        "quality_tier": "C",
        "access": "public",
        "url": "https://www.linkedin.com/pulse/cybersecurity-lessons-from-grammar-systems-order-chaos-osama-salah-1f",
        "date": "2022-05-23",
        "notes": "Public secondary summary of Grammar of Systems items 12–22. Used as an accessible orientation aid; the book remains the controlling source.",
        "creators": "[\"Osama Salah\"]",
        "publisher": "LinkedIn",
        "licence": "publisher_terms",
        "review_status": "checked",
        "last_checked": "2026-08-09",
        "public_link_status": "public_link",
    },
    {
        "id": "src_salah_grammar_part3_2022",
        "title": "Cybersecurity Lessons from The Grammar of Systems, part 3",
        "source_type": "public_secondary_summary",
        "quality_tier": "C",
        "access": "public",
        "url": "https://www.linkedin.com/pulse/cybersecurity-lessons-from-grammar-systems-order-chaos-osama-salah-2f",
        "date": "2022-06-01",
        "notes": "Public secondary summary of Grammar of Systems items 23–33. Used as an accessible orientation aid; the book remains the controlling source.",
        "creators": "[\"Osama Salah\"]",
        "publisher": "LinkedIn",
        "licence": "publisher_terms",
        "review_status": "checked",
        "last_checked": "2026-08-09",
        "public_link_status": "public_link",
    },
]

ALIAS_STOPWORDS = {
    "a", "an", "and", "approach", "analysis", "concept", "evidence", "intervention",
    "law", "method", "methodology", "model", "of", "or", "person", "practice", "principle",
    "skill", "system", "systems", "technology", "the", "theory", "tool", "tradition",
}

PRIVATE_PATTERNS = (
    "sharepoint", "graph.microsoft", "mail.google", "gmail", "sandbox:/", "file://",
    "localhost", "127.0.0.1", "/mnt/data", "redquadrantltd.sharepoint",
)


def parse_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(x) for x in value]
    if not value:
        return []
    try:
        parsed = json.loads(value)
        return [str(x) for x in parsed] if isinstance(parsed, list) else []
    except Exception:
        return []


def norm(value: str) -> str:
    value = value.casefold().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def clean_aliases(node: dict[str, Any]) -> list[str]:
    label_norm = norm(node.get("label", ""))
    label_tokens = set(label_norm.split())
    candidates = parse_list(node.get("aliases")) + MANUAL_ALIASES.get(node["id"], [])
    output: list[str] = []
    seen: set[str] = set()
    for raw in candidates:
        alias = re.sub(r"\s+", " ", raw).strip()
        alias_norm = norm(alias)
        if not alias_norm or alias_norm == label_norm or alias_norm in ALIAS_STOPWORDS:
            continue
        if len(alias_norm) < 3:
            continue
        # Auto-generated single label words add noise; deliberate acronyms and
        # genuine alternate forms survive this check.
        if len(alias_norm.split()) == 1 and alias_norm in label_tokens and not alias.isupper():
            continue
        if alias_norm in seen:
            continue
        seen.add(alias_norm)
        output.append(alias)
    return sorted(output, key=lambda x: (len(x), x.casefold()))


def replace_project_name(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace("The Tangle", PROJECT)
    if isinstance(value, list):
        return [replace_project_name(v) for v in value]
    if isinstance(value, dict):
        return {k: replace_project_name(v) for k, v in value.items()}
    return value


def add_source_id(node: dict[str, Any], source_id: str) -> None:
    ids = parse_list(node.get("source_ids"))
    if source_id not in ids:
        ids.append(source_id)
    node["source_ids"] = json.dumps(ids, ensure_ascii=False)


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    data = replace_project_name(data)

    meta = data.setdefault("meta", {})
    meta.update({
        "project": PROJECT,
        "subtitle": "A living evidence atlas of systems, complexity and cybernetics",
        "tagline": "Every connection must say what it means.",
        "release": "0.5-github-alpha",
        "generated": "2026-08-09",
        "status": "public alpha on GitHub Pages",
        "project_url": SITE_URL,
        "repository_url": REPO_URL,
        "author": "Benjamin P Taylor",
        "source_policy": "Every link on the public site is public. Sources without an open web copy are cited as 'No public link'. Private email, internal documents and private URLs are not published.",
    })

    sources = {s["id"]: s for s in data.get("sources", [])}
    for source in NEW_SOURCES:
        sources[source["id"]] = {**sources.get(source["id"], {}), **source}
    data["sources"] = list(sources.values())

    redirects = data.get("canonical_redirects", {})
    for node in data.get("nodes", []):
        node["aliases"] = json.dumps(clean_aliases(node), ensure_ascii=False)
        if node["id"] in LAW_DESCRIPTIONS:
            node["description"] = LAW_DESCRIPTIONS[node["id"]]
            if node.get("publication_level") == "research_stub":
                node["publication_level"] = "described"
            item_match = re.search(r"item\s+(\d+)", node.get("description", ""), re.I)
            # Source assignment follows the 1–11, 12–22, 23–33 public summaries.
            order = None
            original = next((n for n in data.get("coverage", []) if n.get("node_id") == node["id"]), None)
            # The identifier lists are stable, so use explicit groups below.
            if node["id"] in list(LAW_DESCRIPTIONS)[:11]:
                add_source_id(node, "src_salah_grammar_part1_2022")
            elif node["id"] in list(LAW_DESCRIPTIONS)[11:22]:
                add_source_id(node, "src_salah_grammar_part2_2022")
            else:
                add_source_id(node, "src_salah_grammar_part3_2022")
        if node["id"] in PERSON_DESCRIPTIONS:
            node["description"] = PERSON_DESCRIPTIONS[node["id"]]
            node["publication_level"] = "described"
            if node["id"] == "person_kurt_gödel":
                add_source_id(node, "src_sep_godel_2025")

    # Correct source assignment by law number, independent of dictionary order.
    law_ids = [n["id"] for n in data.get("nodes", []) if n.get("entity_type") == "law_or_principle"]
    number_by_id = {
        "law_or_principle_law_of_calling": 1,
        "law_or_principle_viability_principle": 2,
        "law_or_principle_homeostasis_principle": 3,
        "law_or_principle_system_stability_principle": 4,
        "law_or_principle_law_of_requisite_variety": 5,
        "law_or_principle_first_circular_causality_principle": 6,
        "law_or_principle_second_circular_causality_principle": 7,
        "law_or_principle_law_of_crossing": 8,
        "law_or_principle_network_power_law": 9,
        "law_or_principle_system_survival_theorem": 10,
        "law_or_principle_system_resonance_principle": 11,
        "law_or_principle_power_structuration_theorem": 12,
        "law_or_principle_conservation_of_adaptation_principle": 13,
        "law_or_principle_darkness_principle": 14,
        "law_or_principle_adams_third_law": 15,
        "law_or_principle_self_organised_criticality": 16,
        "law_or_principle_complexity_instability_principle": 17,
        "law_or_principle_order_osmosis_principle": 18,
        "law_or_principle_first_black_box_principle": 19,
        "law_or_principle_second_black_box_principle": 20,
        "law_or_principle_self_organising_principle": 21,
        "law_or_principle_law_of_reciprocity_of_connections": 22,
        "law_or_principle_redundancy_of_potential_command_principle": 23,
        "law_or_principle_root_structuring_theorem": 24,
        "law_or_principle_structural_viability_theorem": 25,
        "law_or_principle_steady_state_principle": 26,
        "law_or_principle_law_of_sufficient_complexity": 27,
        "law_or_principle_fractal_principle": 28,
        "law_or_principle_relaxation_time_principle": 29,
        "law_or_principle_scaling_stasis_principle": 30,
        "law_or_principle_conant_ashby_theorem": 31,
        "law_or_principle_feedback_dominance_theorem": 32,
        "law_or_principle_principle_of_emergence": 33,
    }
    node_map = {n["id"]: n for n in data.get("nodes", [])}
    for node_id, number in number_by_id.items():
        node = node_map[node_id]
        ids = [x for x in parse_list(node.get("source_ids")) if not x.startswith("src_salah_grammar_part")]
        ids.append(f"src_salah_grammar_part{1 if number <= 11 else 2 if number <= 22 else 3}_2022")
        node["source_ids"] = json.dumps(list(dict.fromkeys(ids)), ensure_ascii=False)

    # Recalculate source counts for canonical public entries.
    source_map = {s["id"]: s for s in data["sources"]}
    public_nodes = []
    for node in data.get("nodes", []):
        if node.get("public_visibility") != "public" or redirects.get(node["id"], node["id"]) != node["id"]:
            continue
        ids = parse_list(node.get("source_ids"))
        node["public_source_count"] = sum(1 for sid in ids if source_map.get(sid, {}).get("url"))
        node["no_public_link_count"] = sum(1 for sid in ids if source_map.get(sid) and not source_map[sid].get("url"))
        public_nodes.append(node)

    meta["source_count"] = len(data["sources"])
    meta["public_entry_count"] = len(public_nodes)
    meta["profile_count"] = len(data.get("profiles", []))
    meta["described_entry_count"] = sum(1 for n in public_nodes if n.get("publication_level") != "research_stub")
    meta["stub_entry_count"] = sum(1 for n in public_nodes if n.get("publication_level") == "research_stub")
    meta["public_link_source_count"] = sum(1 for s in data["sources"] if s.get("url"))
    meta["no_public_link_source_count"] = sum(1 for s in data["sources"] if not s.get("url"))

    # Public-source safety check.
    errors: list[str] = []
    for source in data["sources"]:
        url = str(source.get("url") or "")
        lowered = url.casefold()
        if url and not re.match(r"^https?://", url):
            errors.append(f"Non-public URL scheme in source {source['id']}: {url}")
        if any(pat in lowered for pat in PRIVATE_PATTERNS):
            errors.append(f"Private-looking URL in source {source['id']}: {url}")
    if errors:
        raise SystemExit("\n".join(errors))

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    print(
        f"Built {PROJECT}: {meta['public_entry_count']} public entries, "
        f"{meta['source_count']} sources, {meta['stub_entry_count']} outline-only entries."
    )


if __name__ == "__main__":
    main()
