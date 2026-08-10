# Iteration 0.9 data observations

Release analysed: `0.8-expansion-alpha`

## Scale and depth

- Public entries: 407
- Developed profiles: 28 (6.9%)
- Sources: 86 (73 with public links)
- Typed public edges: 535
- Substantive edges: 168 (31.4%)

### Entry types

- person: 142
- publication: 94
- concept: 52
- intervention_skill: 47
- law_or_principle: 33
- method_or_methodology: 17
- tool: 11
- tradition: 5
- approach_family: 1
- comparator_corpus: 1
- corpus: 1
- organisation: 1
- practice: 1
- technology: 1

## Connectivity

- Substantively connected nodes: 136
- Substantively isolated nodes: 271
- Substantive components: 291
- Largest substantive component: 79
- Largest component using every typed edge: 286

### Substantive isolates by type

- publication: 93 of 94
- person: 55 of 142
- intervention_skill: 47 of 47
- law_or_principle: 31 of 33
- concept: 16 of 52
- method_or_methodology: 14 of 17
- tool: 11 of 11
- tradition: 2 of 5
- comparator_corpus: 1 of 1
- corpus: 1 of 1

### Highest substantive degree

- Recursion [concept]: 18 — articulation point
- Feedback [concept]: 18 — articulation point
- Viable System Model (VSM) [method_or_methodology]: 11 — articulation point
- Principia Cybernetica Project [organisation]: 6
- Self-organisation [concept]: 5
- J. P. Crutchfield [person]: 5
- P. Schuster [person]: 5
- Principia Cybernetica Web [publication]: 5
- Boundary [concept]: 5 — articulation point
- B. P. Stojkovic [person]: 4
- D. Pines [person]: 4
- J. Schmalian [person]: 4
- Metasystem transition [concept]: 4 — articulation point
- Observer [concept]: 4
- P. Wolynes [person]: 4
- R. B. Laughlin [person]: 4
- Law of Requisite Variety [law_or_principle]: 4 — articulation point
- Negative feedback [concept]: 4 — articulation point
- Valentin Turchin [person]: 4
- Emergence [concept]: 3

## Layers

- conceptual: 34 edges touching 40 nodes
- human_lineage: 111 edges touching 105 nodes
- practice: 18 edges touching 20 nodes
- contestation: 3 edges touching 6 nodes
- provenance: 357 edges touching 233 nodes
- legacy: 10 edges touching 12 nodes

## Source concentration

- Foundational Papers in Complexity Science — official tables of contents: 201 node uses; 417 edge uses
- SCiO CF Resources v9 draft: 61 node uses; 1 edge uses
- SCiO Professional Accreditation and Competency Framework: 47 node uses; 0 edge uses
- The Grammar of Systems - SCiO presentation: 41 node uses; 0 edge uses
- The Grammar of Systems II: From Order to Chaos and Back Again, 2nd edition: 41 node uses; 0 edge uses
- SCiO SysBoK - Recursion v1: 16 node uses; 19 edge uses
- SCiO SysBoK - Feedback v1: 16 node uses; 17 edge uses
- Benjamin Taylor VSM lecture: 9 node uses; 11 edge uses
- Introduction to Principia Cybernetica: 7 node uses; 11 edge uses
- Principia Cybernetica: Metasystem Transition Theory: 6 node uses; 10 edge uses
- The Cybernetic Manifesto: 4 node uses; 12 edge uses
- Core Thinking Integration: 8 node uses; 7 edge uses
- An Introduction to Cybernetics: 7 node uses; 7 edge uses
- An introductory systems thinking toolkit for civil servants: 11 node uses; 0 edge uses
- Cybersecurity Lessons from The Grammar of Systems, part 1: 11 node uses; 0 edge uses

## Emergent neighbourhoods

- Published neighbourhoods: 6
- Unique published neighbourhood members: 77
- Substantively connected nodes now: 136
- Connected nodes outside published neighbourhoods: 59

## Expansion and entity-resolution risk

- 0.8 expansion entries: 203
- People represented by initial-form labels: 108 of 142

## Interface checks

- Static view buttons: 7
- Static view anchors: 2
- Generated button-link markers: 3
- Generated anchor markers: 4
- CSS centre-alignment rules: 3

## Candidate observations for the public AI page

### The atlas has become broad much faster than it has become deep

Type: `measurement_and_inference`

```json
{
  "public_entries": 407,
  "developed_profiles": 28,
  "developed_share_pct": 6.9,
  "expansion_entries": 203
}
```

### There are now two materially different maps: a provenance graph and a substantive ideas-and-practice graph

Type: `measurement_and_inference`

```json
{
  "all_edges": 535,
  "substantive_edges": 168,
  "non_substantive_edges": 367,
  "substantive_share_pct": 31.4,
  "substantive_connected_nodes": 136,
  "all_edge_largest_component": 286
}
```

### The conceptual core is substantially more connected than methods, tools, practices and laws

Type: `measurement_and_inference`

```json
{
  "isolates_by_type": {
    "comparator_corpus": 1,
    "concept": 16,
    "corpus": 1,
    "intervention_skill": 47,
    "law_or_principle": 31,
    "method_or_methodology": 14,
    "person": 55,
    "publication": 93,
    "tool": 11,
    "tradition": 2
  },
  "entity_types": {
    "approach_family": 1,
    "comparator_corpus": 1,
    "concept": 52,
    "corpus": 1,
    "intervention_skill": 47,
    "law_or_principle": 33,
    "method_or_methodology": 17,
    "organisation": 1,
    "person": 142,
    "practice": 1,
    "publication": 94,
    "technology": 1,
    "tool": 11,
    "tradition": 5
  }
}
```

### The 0.8 breadth is auditable but heavily concentrated in a small number of discovery sources

Type: `measurement_and_inference`

```json
{
  "sources": 86,
  "top_sources": [
    {
      "id": "src_fpcs_official_toc",
      "title": "Foundational Papers in Complexity Science — official tables of contents",
      "node_uses": 201,
      "edge_uses": 417,
      "total_uses": 618,
      "url": "https://www.foundationalpapersincomplexityscience.org/tables-of-contents",
      "source_type": "publisher_table_of_contents"
    },
    {
      "id": "src_scio_cf_resources_2022",
      "title": "SCiO CF Resources v9 draft",
      "node_uses": 61,
      "edge_uses": 1,
      "total_uses": 62,
      "url": "",
      "source_type": "professional_framework_resource_guide"
    },
    {
      "id": "src_scio_accreditation_current",
      "title": "SCiO Professional Accreditation and Competency Framework",
      "node_uses": 47,
      "edge_uses": 0,
      "total_uses": 47,
      "url": "https://www.systemspractice.org/professional-accreditation",
      "source_type": "professional_body_page"
    },
    {
      "id": "src_grammar_presentation_2022",
      "title": "The Grammar of Systems - SCiO presentation",
      "node_uses": 41,
      "edge_uses": 0,
      "total_uses": 41,
      "url": "https://www.systemspractice.org/resources/grammar-systems",
      "source_type": "presentation"
    },
    {
      "id": "src_grammar_2ed_2025",
      "title": "The Grammar of Systems II: From Order to Chaos and Back Again, 2nd edition",
      "node_uses": 41,
      "edge_uses": 0,
      "total_uses": 41,
      "url": "https://www.systemspractice.org/resources/grammar-systems-ii-order-chaos-back-again-2nd-ed",
      "source_type": "book"
    },
    {
      "id": "src_sysbok_recursion_2013",
      "title": "SCiO SysBoK - Recursion v1",
      "node_uses": 16,
      "edge_uses": 19,
      "total_uses": 35,
      "url": "",
      "source_type": "legacy_map_presentation"
    },
    {
      "id": "src_sysbok_feedback_2013",
      "title": "SCiO SysBoK - Feedback v1",
      "node_uses": 16,
      "edge_uses": 17,
      "total_uses": 33,
      "url": "",
      "source_type": "legacy_map_presentation"
    },
    {
      "id": "src_taylor_vsm_lecture_2025",
      "title": "Benjamin Taylor VSM lecture",
      "node_uses": 9,
      "edge_uses": 11,
      "total_uses": 20,
      "url": "",
      "source_type": "private_teaching_material"
    }
  ],
  "expansion_source_distribution": {
    "1": 202,
    "2": 1
  }
}
```

### Initial-only author records create a predictable identity-resolution problem

Type: `measurement_and_risk`

```json
{
  "people_total": 142,
  "initial_form_people": 108,
  "share_pct": 76.1
}
```

### The published emergent neighbourhoods no longer cover the whole connected substantive graph

Type: `measurement_and_risk`

```json
{
  "connected_nodes": 136,
  "category_unique_members": 77,
  "connected_not_in_categories": 59
}
```

### A small set of bridge concepts carries a disproportionate amount of interpretive traffic

Type: `measurement_and_inference`

```json
{
  "articulation_points": [
    {
      "id": "concept_recursion",
      "label": "Recursion",
      "degree": 18
    },
    {
      "id": "concept_feedback",
      "label": "Feedback",
      "degree": 18
    },
    {
      "id": "method_or_methodology_viable_system_model_vsm",
      "label": "Viable System Model (VSM)",
      "degree": 11
    },
    {
      "id": "concept_boundary",
      "label": "Boundary",
      "degree": 5
    },
    {
      "id": "concept_metasystem_transition",
      "label": "Metasystem transition",
      "degree": 4
    },
    {
      "id": "law_or_principle_law_of_requisite_variety",
      "label": "Law of Requisite Variety",
      "degree": 4
    },
    {
      "id": "concept_negative_feedback",
      "label": "Negative feedback",
      "degree": 4
    },
    {
      "id": "person_norbert_wiener",
      "label": "Norbert Wiener",
      "degree": 3
    },
    {
      "id": "concept_information",
      "label": "Information",
      "degree": 3
    },
    {
      "id": "concept_viability",
      "label": "Viability",
      "degree": 3
    },
    {
      "id": "concept_information_theory",
      "label": "Information theory",
      "degree": 2
    },
    {
      "id": "concept_recursive_computation",
      "label": "Recursive computation",
      "degree": 2
    },
    {
      "id": "concept_recursive_definition",
      "label": "Recursive definition",
      "degree": 2
    },
    {
      "id": "method_or_methodology_systemic_intervention",
      "label": "Systemic Intervention",
      "degree": 2
    }
  ]
}
```

### The interface still treats many navigational affordances as actions rather than links

Type: `measurement_and_design_inference`

```json
{
  "button_view_links": 7,
  "anchor_view_links": 2,
  "generated_button_link_markers": 3,
  "generated_anchor_markers": 4,
  "text_align_center_rules": 3
}
```
