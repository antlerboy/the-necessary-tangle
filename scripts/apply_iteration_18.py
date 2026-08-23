#!/usr/bin/env python3
"""Apply release 0.18: navigable entries, map usability and feedback coverage."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from apply_iteration_09 import graph_metrics
from apply_iteration_17 import (
    edge_record,
    enc,
    find_node,
    node_record,
    parse,
    profile_record,
    relation_record,
    source_record,
    upsert,
)
from apply_relational_depth_16 import calculate_relational_depth

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"
RELEASE = "0.18-navigable-tangle-alpha"
GENERATED = "2026-08-23"
PUBLIC_URL = "https://transduction.systems/"


def slug(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
    return text or "entry"


def find_any(data: dict[str, Any], names: list[str], fallback: str | None = None) -> str | None:
    for name in names:
        found = find_node(data, name)
        if found:
            return found
    return fallback


def merge_aliases(node: dict[str, Any], aliases: list[str]) -> None:
    current = [str(item).strip() for item in parse(node.get("aliases"), []) if str(item).strip()]
    node["aliases"] = enc(list(dict.fromkeys([*current, *aliases])))


def merge_tags(node: dict[str, Any], tags: list[str]) -> None:
    current = [str(item).strip() for item in parse(node.get("set_tags"), []) if str(item).strip()]
    node["set_tags"] = enc(list(dict.fromkeys([*current, *tags])))


def public_node(data: dict[str, Any], node_id: str | None) -> dict[str, Any] | None:
    if not node_id:
        return None
    return next((node for node in data.get("nodes", []) if node.get("id") == node_id), None)


def ensure_node(
    data: dict[str, Any],
    names: list[str],
    node_id: str,
    label: str,
    entity_type: str,
    description: str,
    source_ids: list[str],
    tags: list[str],
    *,
    aliases: list[str] | None = None,
    level: str = "described",
    x: float = 0.0,
    y: float = 0.0,
) -> str:
    found = find_any(data, names)
    if found:
        if found != node_id:
            data.setdefault("canonical_redirects", {})[node_id] = found
        node = public_node(data, found)
        if node:
            merge_aliases(node, aliases or names[1:])
            merge_tags(node, ["release_0_18", *tags])
            current_sources = parse(node.get("source_ids"), [])
            node["source_ids"] = enc(list(dict.fromkeys([*current_sources, *source_ids])))
            if node.get("publication_level") == "research_stub" and level in {"described", "profile"}:
                node["publication_level"] = level
            if not str(node.get("description", "")).strip() or str(node.get("description", "")).startswith("Named in"):
                node["description"] = description
                node["canonical_definition"] = description
            node["public_source_count"] = max(int(node.get("public_source_count") or 0), len(parse(node.get("source_ids"), [])))
        return found
    record = node_record(
        node_id,
        label,
        entity_type,
        description,
        source_ids,
        x,
        y,
        tags,
        aliases=aliases or names[1:],
        level=level,
    )
    record["inclusion_reason"] = "post_0_17_feedback_coverage"
    upsert(data.setdefault("nodes", []), [record], "id")
    return node_id


def ensure_relation_type(data: dict[str, Any], record: dict[str, str]) -> None:
    upsert(data.setdefault("relation_types", []), [record], "relation_type")


def tidy_conversational_fragments(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: tidy_conversational_fragments(item) for key, item in value.items()}
    if isinstance(value, list):
        return [tidy_conversational_fragments(item) for item in value]
    if not isinstance(value, str):
        return value
    text = value
    text = re.sub(r"\bDamian\b(?!\s+Allen\b)", "Damian Allen", text)
    replacements = {
        "as requested": "for this public account",
        "you asked": "the public research question asks",
        "your prompt": "the originating research question",
        "the user's prompt": "the originating research question",
        "the user asked": "the originating research question asks",
    }
    for old, new in replacements.items():
        text = re.sub(re.escape(old), new, text, flags=re.IGNORECASE)
    return text


UNFIX_CONCEPTS: list[tuple[str, list[str], str]] = [
    ("System archetypes", ["Systems archetypes"], "Recurring structures that help explain repeated patterns of behaviour in systems."),
    ("Viable System Model", ["VSM", "Viable System Model (VSM)"], "Stafford Beer's recursive model of the functions required for organisational viability."),
    ("Causal loop diagrams", ["Causal loop diagram", "CLD", "Causal Loop Diagrams"], "Diagrams used to represent reinforcing and balancing feedback relationships."),
    ("Mental models", ["Mental model"], "Working assumptions and representations through which people interpret situations and act."),
    ("Holism", ["Holistic thinking"], "Attention to wholes, relations and emergent properties rather than isolated parts alone."),
    ("Systems mapping", ["System mapping", "Systems maps"], "Visual inquiry into elements, relations, boundaries and patterns in a situation."),
    ("System dynamics", ["System Dynamics"], "A modelling tradition using stocks, flows, feedback and simulation to study behaviour over time."),
    ("Systemic intervention", ["Systems intervention"], "Purposeful action informed by explicit boundary judgements and an account of systemic consequences."),
    ("Boundary", ["Boundaries", "System boundary"], "A distinction that marks what an inquiry treats as inside, outside or relevant."),
    ("Interconnectedness", ["Interconnection"], "The condition in which changes propagate through relations among parts and contexts."),
    ("Hierarchy", ["Hierarchies", "Nested hierarchy"], "An ordering of levels or recursively nested systems and subsystems."),
    ("Leverage points", ["Leverage point"], "Places where intervention can alter system structure or behaviour, with effects that vary greatly by depth."),
    ("Feedback", ["Feedback loops", "Feedback loop"], "Information about effects returned into a process so that subsequent action can change."),
    ("Resilience", ["System resilience"], "Capacity to absorb disturbance, reorganise and continue functions or identity judged important."),
    ("Unintended consequences", ["Unintended consequence"], "Effects of action that were not intended, often arising through delayed or indirect relations."),
    ("System", ["Systems"], "A set of distinctions through which interrelated elements and a whole are treated as relevant to an inquiry."),
    ("Emergence", ["Emergent properties"], "Patterns or properties arising from interaction that are not located in any single component."),
    ("Dynamic complexity", ["Dynamical complexity"], "Behaviour shaped by interacting feedbacks, delays, accumulations and change through time."),
    ("Self-organisation", ["Self-organization", "Self organisation", "Self organization"], "The production of ordered patterns through local interaction without a single directing centre."),
    ("Nonlinearity", ["Non-linearity", "Nonlinear dynamics"], "Relationships in which effects are not proportional to causes and may depend on state or history."),
    ("Adaptation", ["Adaptive change"], "Changes in action, structure or capability in relation to conditions and consequences."),
    ("Network theory", ["Network science"], "Study of how nodes, ties and network structure shape possible dynamics."),
    ("Phase transition", ["Phase transitions"], "A qualitative change of system state associated with a shift in conditions or parameters."),
    ("Chaos theory", ["Deterministic chaos"], "Study of deterministic dynamics whose sensitivity makes long-term prediction sharply limited."),
    ("Attractor", ["Attractors"], "A state or pattern towards which a dynamical system tends over time."),
    ("Fitness landscape", ["Fitness landscapes"], "A representation linking possible configurations with measures of reproductive or adaptive success."),
    ("Scaling laws", ["Scaling law"], "Regular relations describing how properties change with size or scale."),
    ("Power law", ["Power laws"], "A relation in which one quantity varies as a power of another, often producing heavy-tailed distributions."),
    ("Self-organised criticality", ["Self-organized criticality", "SOC"], "A proposed process in which interacting systems approach states where small events can have effects across many scales."),
    ("Fractal", ["Fractals", "Fractal geometry"], "A structure or pattern showing related form across different scales."),
    ("Agent-based modelling", ["Agent-based modeling", "ABM"], "Simulation of heterogeneous agents and their interactions to examine aggregate patterns."),
    ("Edge of chaos", ["The edge of chaos"], "A contested metaphor and hypothesis concerning adaptive behaviour near a transition between ordered and disordered dynamics."),
]


NAMED_COVERAGE: list[tuple[str, list[str]]] = [
    ("Philip Boxer", ["Philip Boxer"]),
    ("Sandra Janoff", ["Sandra Janoff"]),
    ("Marvin Weisbord", ["Marv Weisbord", "Marvin R. Weisbord", "Weisbord"]),
    ("Peter Block", ["Peter Block"]),
    ("C. West Churchman", ["West Churchman", "C West Churchman", "Churchman"]),
    ("Ludwig von Bertalanffy", ["von Bertalanffy", "Bertalanffy"]),
    ("Norbert Wiener", ["Wiener"]),
    ("Jay W. Forrester", ["Jay Forrester", "Forrester"]),
    ("Russell L. Ackoff", ["Russell Ackoff", "Russ Ackoff", "Ackoff"]),
    ("Donella H. Meadows", ["Donella Meadows", "Donna Meadows", "Meadows"]),
    ("Alasdair MacIntyre", ["MacIntyre", "Alasdair MacInyre"]),
    ("Ludwig Wittgenstein", ["Wittgenstein"]),
    ("George Spencer-Brown", ["G. Spencer-Brown", "Spencer Brown", "Spencer-Brown"]),
    ("The Tavistock Institute of Human Relations", ["Tavistock Institute", "The Tavistock Institute"]),
    ("NTL Institute", ["NTL", "National Training Laboratories", "NTL Institute for Applied Behavioral Science"]),
    ("Peter Checkland", ["Checkland"]),
    ("Niklas Luhmann", ["Luhmann", "Luhann"]),
    ("Louis H. Kauffman", ["Louis Kauffman", "L. H. Kauffman"]),
    ("Stuart Kauffman", ["Stuart A. Kauffman"]),
    ("Warren S. McCulloch", ["Warren McCulloch", "McCulloch"]),
    ("John von Neumann", ["von Neumann"]),
    ("Margaret Mead", ["Mead"]),
    ("James Lovelock", ["Lovelock"]),
    ("Lynn Margulis", ["Margulis"]),
    ("Anatol Rapoport", ["Rapoport", "Rapaport"]),
    ("Kenneth E. Boulding", ["Kenneth Boulding", "Boulding"]),
    ("Fritjof Capra", ["Capra"]),
    ("Ilya Prigogine", ["Prigogine"]),
    ("Walter Pitts", ["Pitts"]),
    ("Frank Rosenblatt", ["Rosenblatt"]),
    ("Heinz von Foerster", ["von Foerster", "Heinz Von Foerster"]),
    ("Robert Axelrod", ["Axelrod"]),
    ("Albert-László Barabási", ["Albert-Laszlo Barabasi", "Albert Barabasi", "Barabasi"]),
    ("Nicholas A. Christakis", ["Nicholas Christakis", "Christakis"]),
    ("Edgar Morin", ["Morin"]),
    ("Paul Cilliers", ["Cilliers"]),
    ("Linda Booth Sweeney", ["Linda Sweeney", "Linda B. Sweeney", "Dr Linda Booth Sweeney"]),
]


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    sources = [
        source_record(
            "src_linda_booth_sweeney_profile_2026",
            "Meet Linda Booth Sweeney",
            "official_author_profile",
            "https://www.lindaboothsweeney.com/meet-linda-booth-sweeney",
            "Author-maintained profile establishing Booth Sweeney's systems education, writing, leadership laboratories and listed publications. It records her own account rather than an independent evaluation.",
            ["Linda Booth Sweeney"],
            "Toggle Labs",
            "checked 2026-08-23",
        ),
        source_record(
            "src_massbook_noisy_puddle_award_2025",
            "Massachusetts Book Awards — previous winners",
            "official_award_record",
            "https://www.massbook.org/previous-winners",
            "Official Massachusetts Center for the Book record listing The Noisy Puddle as the 2025 Picture Book / Early Reader winner.",
            ["Massachusetts Center for the Book"],
            "Massachusetts Center for the Book",
            "2025",
        ),
        source_record(
            "src_linda_noisy_puddle_2026",
            "The Noisy Puddle",
            "official_author_book_page",
            "https://www.lindaboothsweeney.com/the-noisy-puddle",
            "Author-maintained page describing the book's treatment of the seasonal ecology and interrelationships of a vernal pool.",
            ["Linda Booth Sweeney", "Miki Sato"],
            "Toggle Labs",
            "checked 2026-08-23",
        ),
        source_record(
            "src_linda_do_bees_pee_2026",
            "Do Bees Pee?",
            "official_author_publication_notice",
            "https://www.lindaboothsweeney.com/meet-linda-booth-sweeney",
            "Author-maintained publication notice listing Do Bees Pee? with HarperCollins and a June 2026 publication date, and relating it to closed-loop ecological processes and circular-economy learning.",
            ["Linda Booth Sweeney"],
            "Toggle Labs / HarperCollins",
            "2026",
        ),
        source_record(
            "src_unfix_32_key_concepts_2024",
            "32 Key Concepts in Systems Thinking and Complexity Theory",
            "first_party_synthesis",
            "https://unfix.com/blog/32-key-concepts",
            "Jurgen Appelo's unFIX synthesis of 32 concepts. The page states that the list and prevalence scores were generated with several large language models and checked against the author's experience; it is a useful comparator, not a neutral or exhaustive canon.",
            ["Jurgen Appelo"],
            "unFIX",
            "2024-07-15",
            quality="B",
        ),
        source_record(
            "src_tangle_issue2_post017_usability_2026",
            "Running feedback after release 0.17",
            "public_curator_feedback",
            "https://github.com/antlerboy/the-necessary-tangle/issues/2",
            "Public feedback record for the 0.18 usability, language, search, named-coverage and source additions. It establishes the design requirement, not the truth of external content claims.",
            ["Benjamin P Taylor", "Roger James", "parcadei"],
            "The Necessary Tangle",
            "2026-08",
            quality="B",
        ),
    ]
    upsert(data.setdefault("sources", []), sources, "id")

    ensure_relation_type(data, relation_record(
        "includes_in_synthesis",
        "classification",
        "included_in_synthesis",
        "The source must explicitly include the target concept in the named synthesis.",
        "includes in its synthesis",
    ))
    ensure_relation_type(data, relation_record(
        "received_award",
        "historical",
        "awarded_to",
        "An official award record must identify the work and award.",
        "received",
    ))
    ensure_relation_type(data, relation_record(
        "teaches_through",
        "practice",
        "used_by_to_teach",
        "A first-party or independent source must document the educational use and its subject.",
        "teaches systems ideas through",
    ))
    if not any(item.get("relation_type") == "illustrates" for item in data.get("relation_types", [])):
        ensure_relation_type(data, relation_record(
            "illustrates", "practice", "illustrated_by",
            "A source or explicit curatorial interpretation must state the example and its limits.",
            "illustrates",
        ))
    if not any(item.get("relation_type") == "introduces" for item in data.get("relation_types", [])):
        ensure_relation_type(data, relation_record(
            "introduces", "practice", "introduced_by",
            "A source must explicitly present the target idea as part of the work's educational purpose.",
            "introduces",
        ))

    linda_id = ensure_node(
        data,
        ["Linda Booth Sweeney", "Linda Sweeney"],
        "person_linda_booth_sweeney",
        "Linda Booth Sweeney",
        "person",
        "A systems educator, writer and strategist whose work makes systems thinking usable through games, leadership laboratories, visual practice and books for adults and children.",
        ["src_linda_booth_sweeney_profile_2026"],
        ["systems-education", "systems-literacy", "practice"],
        aliases=["Linda Sweeney", "Linda B. Sweeney", "Dr Linda Booth Sweeney"],
        level="profile",
        x=0.05,
        y=0.46,
    )
    noisy_id = ensure_node(
        data,
        ["The Noisy Puddle"],
        "publication_the_noisy_puddle",
        "The Noisy Puddle",
        "publication",
        "A picture book about the seasonal ecology of a vernal pool, using close observation of changing relations among habitat and species.",
        ["src_linda_noisy_puddle_2026", "src_massbook_noisy_puddle_award_2025"],
        ["systems-literacy", "ecology", "children"],
        level="profile",
        x=0.11,
        y=0.49,
    )
    bees_id = ensure_node(
        data,
        ["Do Bees Pee?", "Do Bees Pee"],
        "publication_do_bees_pee",
        "Do Bees Pee?",
        "publication",
        "A 2026 children's book using questions about animal waste to introduce ecological cycles, reuse and circular-economy thinking.",
        ["src_linda_do_bees_pee_2026"],
        ["systems-literacy", "circular-economy", "children"],
        aliases=["Do Bees Pee"],
        level="profile",
        x=0.14,
        y=0.46,
    )
    interconnected_id = ensure_node(
        data,
        ["Interconnectedness", "Interconnection"],
        "concept_interconnectedness",
        "Interconnectedness",
        "concept",
        "The condition in which elements and contexts affect one another through relations, so that consequences can propagate beyond the point of action.",
        ["src_unfix_32_key_concepts_2024"],
        ["systems", "relations"],
        level="described",
    )
    circular_id = ensure_node(
        data,
        ["Circular economy", "Circular economy thinking"],
        "concept_circular_economy",
        "Circular economy",
        "concept",
        "An approach to economic activity which seeks to retain value, circulate materials and reduce waste rather than depend on linear extraction and disposal.",
        ["src_linda_do_bees_pee_2026"],
        ["sustainability", "systems-practice"],
        level="described",
    )

    upsert(data.setdefault("profiles", []), [
        profile_record(
            linda_id,
            "Linda Booth Sweeney makes systems ideas learnable through embodied exercises, stories, visualisation and leadership practice across adult and children's education.",
            "Her work is a route from abstract systems vocabulary into experiences which let people notice interdependence, feedback, delay and unintended effects for themselves.",
            [
                "Systems literacy is treated as a capability developed through practice, not as a list of definitions.",
                "First-party descriptions establish her intent and current work; they do not by themselves establish independent effectiveness claims.",
            ],
            ["MIT organisational-learning and system-dynamics settings", "systems education", "learning through games and stories"],
            ["systems thinking", "experiential learning", "systems literacy"],
            ["The Systems Thinking Playbook", "The Climate Change Playbook", "The Noisy Puddle", "Do Bees Pee?"],
            ["systems learning games", "leadership laboratories", "children's systems education"],
            ["Accessible explanation is not the same as simplification without limits."],
            ["Add independent studies of use and outcomes where available."],
            ["src_linda_booth_sweeney_profile_2026", "src_massbook_noisy_puddle_award_2025", "src_linda_noisy_puddle_2026", "src_linda_do_bees_pee_2026"],
        ),
        profile_record(
            noisy_id,
            "The Noisy Puddle follows the changing ecology of a vernal pool and makes a web of seasonal interdependence observable to younger readers.",
            "It offers an example of systems literacy through attention to relations and change rather than through formal systems terminology.",
            ["The book is a literary and educational work, not evidence for a general theory of ecosystems."],
            ["nature writing", "children's science education", "systems literacy"],
            ["ecology", "interconnectedness", "observation through time"],
            ["classroom and family inquiry into living relations"],
            ["systems education through story"],
            ["An award establishes recognition, not educational effectiveness."],
            ["Add classroom studies or educator accounts beyond promotional material."],
            ["src_linda_noisy_puddle_2026", "src_massbook_noisy_puddle_award_2025"],
        ),
        profile_record(
            bees_id,
            "Do Bees Pee? uses questions about animal waste and ecological reuse to introduce closed-loop processes and circular-economy thinking.",
            "It extends Booth Sweeney's systems-literacy work into the material cycles through which one organism's output becomes another process's resource.",
            ["The June 2026 publication fact and framing are established by the author's current publication notice."],
            ["children's science communication", "ecological cycles", "circular economy"],
            ["material cycles", "interdependence", "waste as resource"],
            ["systems literacy for younger readers"],
            ["question-led learning", "circular-economy education"],
            ["A closed loop is a useful model, not a claim that material systems have no losses or externalities."],
            ["Add the publisher record and independent reviews after publication where available."],
            ["src_linda_do_bees_pee_2026"],
        ),
    ], "node_id")

    authored_type = "authored"
    if not any(item.get("relation_type") == authored_type for item in data.get("relation_types", [])):
        ensure_relation_type(data, relation_record(authored_type, "documentary", "authored_by", "A publication or official author record.", "authored"))
    linda_edges = [
        edge_record("e18_linda_authored_noisy_puddle", linda_id, noisy_id, authored_type, "documentary", "authored", ["src_linda_noisy_puddle_2026"], "Book page and creator credit", "Authorship of the book text; illustration is separately credited to Miki Sato."),
        edge_record("e18_linda_authored_do_bees_pee", linda_id, bees_id, authored_type, "documentary", "authored", ["src_linda_do_bees_pee_2026"], "Publication notice", "Authorship and current publication notice."),
        edge_record("e18_linda_teaches_through_noisy", linda_id, noisy_id, "teaches_through", "practice", "teaches systems ideas through", ["src_linda_booth_sweeney_profile_2026", "src_linda_noisy_puddle_2026"], "For Children & Educators; book description", "The relation records the author's stated systems-literacy practice, not a measured learning outcome."),
        edge_record("e18_noisy_interconnectedness", noisy_id, interconnected_id, "illustrates", "practice", "illustrates", ["src_linda_noisy_puddle_2026"], "Book description: web of interrelationships", "Curatorial interpretation of the book's explicit treatment of ecological interrelationships.", mode="interpreted", confidence="0.88", review_label="curatorial interpretation"),
        edge_record("e18_bees_circular_economy", bees_id, circular_id, "introduces", "practice", "introduces", ["src_linda_do_bees_pee_2026"], "Author publication notice", "The author explicitly frames the book as an introduction to sustainability and circular-economy thinking."),
        edge_record("e18_noisy_award", noisy_id, noisy_id, "received_award", "historical", "received the 2025 Massachusetts Picture Book / Early Reader award", ["src_massbook_noisy_puddle_award_2025"], "2025 Picture Book / Early Reader", "Self-edge placeholder removed below; award is retained as profile/source metadata."),
    ]
    # Do not publish a self-edge merely to encode an award; the source and profile carry it.
    linda_edges = [edge for edge in linda_edges if edge["source"] != edge["target"]]
    upsert(data.setdefault("edges", []), linda_edges, "id")

    appelo_id = ensure_node(
        data,
        ["Jurgen Appelo", "Jürgen Appelo"],
        "person_jurgen_appelo",
        "Jurgen Appelo",
        "person",
        "An author and organisation-design practitioner associated with Management 3.0 and unFIX, including a public synthesis of systems-thinking and complexity concepts.",
        ["src_unfix_32_key_concepts_2024"],
        ["organisation-design", "systems-synthesis"],
        aliases=["Jürgen Appelo"],
        level="described",
        x=0.29,
        y=0.36,
    )
    unfix_id = ensure_node(
        data,
        ["32 Key Concepts in Systems Thinking and Complexity Theory", "unFIX 32 key concepts"],
        "publication_unfix_32_key_concepts",
        "32 Key Concepts in Systems Thinking and Complexity Theory",
        "publication",
        "A 2024 unFIX visual and explanatory synthesis which places 32 systems-thinking and complexity concepts on a relative continuum. Its author states that AI systems produced the initial synthesis and prevalence estimates, followed by editorial checking.",
        ["src_unfix_32_key_concepts_2024"],
        ["comparator", "systems-thinking", "complexity"],
        aliases=["unFIX 32 key concepts", "32 key concepts"],
        level="profile",
        x=0.34,
        y=0.36,
    )
    upsert(data.setdefault("profiles", []), [profile_record(
        unfix_id,
        "The unFIX 32-concept synthesis is a public comparator: it offers a broad route into familiar systems and complexity terms while making its AI-assisted production method explicit.",
        "It is useful for testing atlas coverage and search language. It is not evidence that the selected concepts, definitions or prevalence scores form a settled canon.",
        [
            "Inclusion in the list is documentary evidence about the unFIX synthesis, not independent evidence of intellectual importance.",
            "The systems-thinking/complexity scores are editorial and AI-assisted estimates, not measurements of a defined literature corpus.",
        ],
        ["management and organisation design", "AI-assisted synthesis", "systems and complexity popularisation"],
        ["systems thinking", "complexity theory", "public discourse synthesis"],
        ["coverage audit", "search aliases", "comparison with a typed evidence graph"],
        ["orientation for readers", "comparison of concept coverage"],
        ["A colourful map is not automatically a genealogy, taxonomy or source-backed relation graph."],
        ["Retain disagreement about labels and placement; do not copy the list's boundary as the atlas boundary."],
        ["src_unfix_32_key_concepts_2024"],
    )], "node_id")
    upsert(data.setdefault("edges", []), [edge_record(
        "e18_appelo_authored_unfix32", appelo_id, unfix_id, authored_type, "documentary", "authored", ["src_unfix_32_key_concepts_2024"], "Page byline", "Authorship of the public unFIX synthesis."
    )], "id")

    coverage_items: list[dict[str, Any]] = []
    concept_edges: list[dict[str, Any]] = []
    for index, (label, aliases, description) in enumerate(UNFIX_CONCEPTS):
        candidates = [label, *aliases]
        node_id = find_any(data, candidates)
        created = False
        if not node_id:
            node_id = ensure_node(
                data,
                candidates,
                f"concept_unfix_{slug(label)}",
                label,
                "concept",
                description,
                ["src_unfix_32_key_concepts_2024"],
                ["unfix-32", "systems-complexity-comparator"],
                aliases=aliases,
                level="described",
                x=-0.45 + (index % 8) * 0.13,
                y=0.56 + (index // 8) * 0.09,
            )
            created = True
        node = public_node(data, node_id)
        if node:
            merge_aliases(node, aliases)
            merge_tags(node, ["unfix-32", "release_0_18"])
        edge_id = f"e18_unfix32_{slug(label)}"
        concept_edges.append(edge_record(
            edge_id,
            unfix_id,
            node_id,
            "includes_in_synthesis",
            "classification",
            "includes in its synthesis",
            ["src_unfix_32_key_concepts_2024"],
            f"Heading: {label}",
            "This line records inclusion in Jurgen Appelo's named 32-concept synthesis. It does not endorse the definition, score or placement as a field consensus.",
        ))
        coverage_items.append({
            "concept": label,
            "node_id": node_id,
            "entry_label": node.get("label") if node else label,
            "created_in_0_18": created,
            "publication_level": node.get("publication_level") if node else "missing",
            "source_id": "src_unfix_32_key_concepts_2024",
        })
    upsert(data.setdefault("edges", []), concept_edges, "id")
    data["unfix_32_coverage"] = {
        "release": RELEASE,
        "source_id": "src_unfix_32_key_concepts_2024",
        "method": "Map each named concept to a canonical public entry by maintained name or alias; create a brief source-bounded entry only where no match exists.",
        "caution": "The source is an AI-assisted first-party synthesis and comparator, not a neutral canon or proof of influence.",
        "items": coverage_items,
    }

    # Make every named item findable, then record its actual depth rather than claiming uniform completion.
    generic_source = "src_tangle_issue2_post017_usability_2026"
    named_rows: list[dict[str, Any]] = []
    for label, aliases in NAMED_COVERAGE:
        node_id = find_any(data, [label, *aliases])
        if not node_id:
            entity_type = "organisation" if label in {"The Tavistock Institute of Human Relations", "NTL Institute"} else "person"
            node_id = ensure_node(
                data,
                [label, *aliases],
                f"{entity_type}_{slug(label)}",
                label,
                entity_type,
                f"Named in the public 0.18 coverage audit. A source-specific profile and typed lineage remain required before stronger claims are made about {label}.",
                [generic_source],
                ["named-coverage-audit", "research-queue"],
                aliases=aliases,
                level="research_stub",
            )
        node = public_node(data, node_id)
        if node:
            merge_aliases(node, aliases)
            merge_tags(node, ["named-coverage-audit", "release_0_18"])
        profile = next((item for item in data.get("profiles", []) if item.get("node_id") == node_id), None)
        substantive = [edge for edge in data.get("edges", []) if (edge.get("source") == node_id or edge.get("target") == node_id) and edge.get("relation_family") not in {"classification", "documentary", "evidence", "legacy"}]
        named_rows.append({
            "name": label,
            "node_id": node_id,
            "publication_level": node.get("publication_level") if node else "missing",
            "has_profile": bool(profile),
            "public_source_count": int(node.get("public_source_count") or 0) if node else 0,
            "substantive_connection_count": len(substantive),
            "aliases": aliases,
            "status": "developed" if profile and node and node.get("publication_level") == "profile" else "represented" if node and node.get("publication_level") != "research_stub" else "research_queue",
        })
    data["named_coverage_review"] = {
        "release": RELEASE,
        "request_source_id": generic_source,
        "method": "Resolve canonical names and aliases, expose actual profile/source/connection depth, and leave unsupported biographical or lineage claims out of the public graph.",
        "items": named_rows,
    }

    # Remove hidden-conversation residue from public-facing data fields while preserving source titles and URLs.
    for key in ("nodes", "profiles", "journeys", "claims", "emergent_categories", "ai_observations"):
        if key in data:
            data[key] = tidy_conversational_fragments(data[key])

    metrics = graph_metrics(data)
    data["relational_depth"] = calculate_relational_depth(data)
    aggregate = data["relational_depth"].get("aggregate", {})
    substantive_families = {"conceptual", "historical", "influence", "practice", "contestation", "human", "identity"}
    substantive_edges = [edge for edge in data.get("edges", []) if edge.get("relation_family") in substantive_families]
    substantive_nodes = {endpoint for edge in substantive_edges for endpoint in (edge.get("source"), edge.get("target")) if endpoint}
    public_ids = {node.get("id") for node in data.get("nodes", []) if node.get("public_visibility") == "public" and data.get("canonical_redirects", {}).get(node.get("id"), node.get("id")) == node.get("id")}
    named_counts = {status: sum(1 for item in named_rows if item["status"] == status) for status in ("developed", "represented", "research_queue")}
    alias_count = sum(len(parse(node.get("aliases"), [])) for node in data.get("nodes", []) if node.get("id") in public_ids)
    data["ai_observations"] = {
        "release": RELEASE,
        "generated": GENERATED,
        "method_note": "Measurements come from the generated public graph. Interpretations concern this atlas and its current source and interface choices; they are not measurements of the field itself.",
        "metrics": {
            "public_entries": metrics.get("public_entries"),
            "developed_profiles": len(data.get("profiles", [])),
            "typed_edges": len(data.get("edges", [])),
            "substantive_edges": len(substantive_edges),
            "substantive_connected_nodes": len(substantive_nodes & public_ids),
            "substantive_isolated_nodes": len(public_ids - substantive_nodes),
            "sources": len(data.get("sources", [])),
            "connected_nodes_outside_neighbourhoods": max(0, len(substantive_nodes & public_ids) - len({node for category in data.get("emergent_categories", []) for node in category.get("member_node_ids", category.get("members", []))})),
            "maintained_aliases": alias_count,
            "named_coverage_developed": named_counts["developed"],
            "named_coverage_represented": named_counts["represented"],
            "named_coverage_research_queue": named_counts["research_queue"],
            "unfix_concepts_resolved": len(coverage_items),
        },
        "observations": [
            {
                "kind": "interface measurement plus epistemic interpretation",
                "title": "Navigation changes what appears important",
                "measurement": f"The 0.18 interface gives every entry a full-screen reading surface and a constellation view with one selected centre, direct relations and two-step relations.",
                "interpretation": "A centre chosen for a question is not the centre of the field. Interface focus and graph degree can manufacture apparent intellectual importance.",
                "implication": "The map labels the selected entry as a temporary star and treats inner and outer orbits as question-relative positions.",
                "test": "Change the selected entry and layer. A reader should see the constellation reorganise without being told that the new centre is canonically primary.",
            },
            {
                "kind": "search measurement plus data-quality interpretation",
                "title": "Names are part of the knowledge model",
                "measurement": f"The public graph now maintains {alias_count} aliases, including Donna/Donella Meadows, Russ/Russell Ackoff and common misspellings named in feedback.",
                "interpretation": "A technically present entry is practically absent when readers cannot find it using the name they know.",
                "implication": "Aliases are canonical routing data, while ambiguous surnames remain separate where collapsing them would merge people.",
                "test": "Search for Donna Meadows, Russ Ackoff, MacInyre, Luhann, Rapaport and Barabasi and check that each resolves without creating duplicate entries.",
            },
            {
                "kind": "coverage measurement plus editorial caution",
                "title": "Named coverage is now visible but remains uneven",
                "measurement": f"Of {len(named_rows)} requested people and institutions, {named_counts['developed']} are developed, {named_counts['represented']} are represented more briefly and {named_counts['research_queue']} remain explicitly in the research queue.",
                "interpretation": "Making a name searchable completes an indexing task, not a scholarly account. Source and connection depth still determine what can responsibly be said.",
                "implication": "The public coverage table exposes the difference instead of turning a requested canon into invented uniform depth.",
                "test": "Each research-queue entry should gain a public source and typed lineage before stronger claims or prominent routes are added.",
            },
            {
                "kind": "source-role analysis",
                "title": "A comparator is not a canon",
                "measurement": f"All {len(coverage_items)} concepts in the unFIX synthesis resolve to canonical atlas entries; the source page states that AI systems produced the initial synthesis and prevalence estimates.",
                "interpretation": "The list is valuable evidence of a contemporary vocabulary and popular synthesis, but not independent proof of the concepts' definitions, frequency or importance.",
                "implication": "The atlas records documentary inclusion with one typed relation and keeps the source's method and limits beside it.",
                "test": "Readers should be able to compare the list with the atlas without mistaking a score or visual position for a supported historical or logical relation.",
            },
            {
                "kind": "content audit observation",
                "title": "Public prose must carry its own context",
                "measurement": "The 0.18 build scans public-facing data and pages for isolated first names and phrases which answer an unseen prompt or conversation.",
                "interpretation": "A public knowledge object cannot depend on the private circumstances of its drafting. Hidden conversational context is a form of missing provenance.",
                "implication": "Names are expanded, requirements are restated as standalone claims and feedback remains in the public ledger rather than leaking into definitions.",
                "test": "A reader arriving at any entry by direct link should understand every sentence without knowing the development conversation.",
            },
            {
                "kind": "interaction design observation",
                "title": "Links are commitments about possible movement",
                "measurement": "Navigational cards, search suggestions, surprise routes, map nodes, map connections and entry actions now expose stable href targets; plain left-click behaviour remains enhanced in place.",
                "interpretation": "A control which looks like a link but cannot be copied, opened in a new tab or inspected conceals the structure of the atlas.",
                "implication": "Navigation uses links; buttons are reserved for actions whose result cannot sensibly exist as a URL.",
                "test": "Right-click or modified-click each navigational surface and confirm that the destination remains coherent in a separate tab.",
            },
        ],
    }
    meta = data.setdefault("meta", {})
    meta.update({
        "release": RELEASE,
        "generated": GENERATED,
        "project_url": PUBLIC_URL,
        "public_entry_count": metrics.get("public_entries"),
        "profile_count": len(data.get("profiles", [])),
        "source_count": len(data.get("sources", [])),
        "journey_count": len(data.get("journeys", [])),
        "reader_connected_entry_count": aggregate.get("reader_connected_entries"),
        "unfix_coverage_count": len(coverage_items),
        "named_coverage_count": len(named_rows),
        "map_interaction_contract": "navigable-map-v2",
    })

    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DOCS_ASSETS / "unfix-32-coverage.json").write_text(json.dumps(data["unfix_32_coverage"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DOCS_ASSETS / "named-coverage-review.json").write_text(json.dumps(data["named_coverage_review"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Applied {RELEASE}: {metrics.get('public_entries')} public entries, {len(data.get('profiles', []))} profiles")


if __name__ == "__main__":
    main()
