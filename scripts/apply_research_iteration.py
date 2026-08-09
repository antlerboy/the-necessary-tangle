#!/usr/bin/env python3
"""Apply the 0.7 research, source and emergent-neighbourhood iteration.

This pass is deliberately bibliographic and structural. It itemises the 89
papers in the named Santa Fe Institute collection, gives Principia Cybernetica
an inspectable first-pass representation, registers further official public
sources, and derives provisional neighbourhoods from the current substantive
public graph. It does not pretend that an inventory is a full scholarly review.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
DOCS_ASSETS = ROOT / "docs" / "assets"

RELEASE = "0.7-constellations-alpha"
GENERATED = "2026-08-09"
REPOSITORY = "https://github.com/antlerboy/the-necessary-tangle"

FPCS_TOC_URL = "https://www.foundationalpapersincomplexityscience.org/tables-of-contents"
FPCS_CITATION_URL = "https://www.foundationalpapersincomplexityscience.org/how-to-cite"

# The original papers listed in the official table of contents. Commentary
# authors and essay titles are held separately by the publisher and are not
# silently treated as authors of the historical papers.
FPCS_PAPERS: list[dict[str, Any]] = [
    {"number": 1, "volume": 1, "authors": "A. J. Lotka", "title": "Contribution to the Energetics of Evolution", "year": "1922"},
    {"number": 2, "volume": 1, "authors": "L. Szilárd", "title": "On the Decrease of Entropy in a Thermodynamic System by the Intervention of Intelligent Beings", "year": "1929"},
    {"number": 3, "volume": 1, "authors": "S. Wright", "title": "The Roles of Mutation, Inbreeding, Crossbreeding, and Selection in Evolution", "year": "1932"},
    {"number": 4, "volume": 1, "authors": "C. H. Waddington", "title": "Canalization of Development and the Inheritance of Acquired Characters", "year": "1942"},
    {"number": 5, "volume": 1, "authors": "W. S. McCulloch and W. Pitts", "title": "A Logical Calculus of the Ideas Immanent in Nervous Activity", "year": "1943"},
    {"number": 6, "volume": 1, "authors": "A. Rosenblueth, N. Wiener, and J. Bigelow", "title": "Behavior, Purpose, and Teleology", "year": "1943"},
    {"number": 7, "volume": 1, "authors": "F. A. Hayek", "title": "The Use of Knowledge in Society", "year": "1945"},
    {"number": 8, "volume": 1, "authors": "A. Rosenblueth and N. Wiener", "title": "The Role of Models in Science", "year": "1945"},
    {"number": 9, "volume": 1, "authors": "C. E. Shannon", "title": "A Mathematical Theory of Communication", "year": "1948"},
    {"number": 10, "volume": 1, "authors": "W. Weaver", "title": "Science and Complexity", "year": "1948"},
    {"number": 11, "volume": 1, "authors": "A. M. Turing", "title": "Computing Machinery and Intelligence", "year": "1950"},
    {"number": 12, "volume": 1, "authors": "J. Nash", "title": "Non-Cooperative Games", "year": "1951"},
    {"number": 13, "volume": 1, "authors": "A. M. Turing", "title": "The Chemical Basis of Morphogenesis", "year": "1952"},
    {"number": 14, "volume": 1, "authors": "E. T. Jaynes", "title": "Information Theory and Statistical Mechanics", "year": "1957"},
    {"number": 15, "volume": 1, "authors": "R. E. Kálmán", "title": "Contributions to the Theory of Optimal Control", "year": "1960"},
    {"number": 16, "volume": 1, "authors": "R. Landauer", "title": "Irreversibility and Heat Generation in the Computing Process", "year": "1961"},
    {"number": 17, "volume": 1, "authors": "M. Minsky", "title": "Steps Toward Artificial Intelligence", "year": "1961"},
    {"number": 18, "volume": 1, "authors": "K. J. Arrow", "title": "The Economic Implications of Learning by Doing", "year": "1962"},
    {"number": 19, "volume": 1, "authors": "M. Bunge", "title": "The Complexity of Simplicity", "year": "1962"},
    {"number": 20, "volume": 1, "authors": "J. H. Holland", "title": "Outline for a Logical Theory of Adaptive Systems", "year": "1962"},
    {"number": 21, "volume": 2, "authors": "H. A. Simon", "title": "The Architecture of Complexity", "year": "1962"},
    {"number": 22, "volume": 2, "authors": "S. Ulam", "title": "On Some Mathematical Problems Connected with Patterns of Growth in Figures", "year": "1962"},
    {"number": 23, "volume": 2, "authors": "E. N. Lorenz", "title": "Deterministic Nonperiodic Flow", "year": "1963"},
    {"number": 24, "volume": 2, "authors": "A. Cobham", "title": "The Intrinsic Computational Difficulty of Functions", "year": "1964"},
    {"number": 25, "volume": 2, "authors": "R. J. Solomonoff", "title": "A Formal Theory of Inductive Inference, Part 1", "year": "1964"},
    {"number": 26, "volume": 2, "authors": "G. J. Chaitin", "title": "On the Length of Programs for Computing Finite Binary Sequences", "year": "1966"},
    {"number": 27, "volume": 2, "authors": "D. M. Raup", "title": "Geometric Analysis of Shell Coiling; General Problems", "year": "1966"},
    {"number": 28, "volume": 2, "authors": "J. von Neumann", "title": "Theory of Self-Reproducing Automata", "year": "1966"},
    {"number": 29, "volume": 2, "authors": "B. B. Mandelbrot", "title": "How Long is the Coast of Britain? Statistical Self-Similarity and Fractional Dimension", "year": "1967"},
    {"number": 30, "volume": 2, "authors": "M. Kimura", "title": "Evolutionary Rate at the Molecular Level", "year": "1968"},
    {"number": 31, "volume": 2, "authors": "A. N. Kolmogorov", "title": "Three Approaches to the Quantitative Definition of Information", "year": "1968"},
    {"number": 32, "volume": 2, "authors": "M. I. Budyko", "title": "The Effect of Solar Radiation Variations on the Climate of the Earth", "year": "1969"},
    {"number": 33, "volume": 2, "authors": "S. Kauffman", "title": "Metabolic Stability and Epigenesis in Randomly Constructed Genetic Nets", "year": "1969"},
    {"number": 34, "volume": 2, "authors": "R. C. Conant and W. R. Ashby", "title": "Every Good Regulator of a System Must Be a Model of That System", "year": "1970"},
    {"number": 35, "volume": 2, "authors": "G. R. Price", "title": "Selection and Covariance", "year": ""},
    {"number": 36, "volume": 2, "authors": "O. E. Rössler", "title": "A System–Theoretic Model of Biogenesis (Ein systemtheoretisches Modell zur Biogenese)", "year": "1971"},
    {"number": 37, "volume": 2, "authors": "T. C. Schelling", "title": "Dynamic Models of Segregation", "year": "1971"},
    {"number": 38, "volume": 2, "authors": "E. B. W. Zubrow", "title": "Carrying Capacity and Dynamic Equilibrium in the Prehistoric Southwest", "year": "1971"},
    {"number": 39, "volume": 2, "authors": "P. W. Anderson", "title": "More Is Different", "year": "1972"},
    {"number": 40, "volume": 2, "authors": "R. M. Karp", "title": "Reducibility Among Combinatorial Problems", "year": "1972"},
    {"number": 41, "volume": 2, "authors": "R. M. May", "title": "Will a Large Complex System Be Stable?", "year": "1972"},
    {"number": 42, "volume": 2, "authors": "H. von Foerster", "title": "Notes on an Epistemology for Living Things", "year": "1972"},
    {"number": 43, "volume": 2, "authors": "C. H. Bennett", "title": "Logical Reversibility of Computation", "year": "1973"},
    {"number": 44, "volume": 2, "authors": "M. S. Granovetter", "title": "The Strength of Weak Ties", "year": "1973"},
    {"number": 45, "volume": 3, "authors": "C. S. Holling", "title": "Resilience and Stability of Ecological Systems", "year": "1973"},
    {"number": 46, "volume": 3, "authors": "H. A. Simon", "title": "The Organization of Complex Systems", "year": "1973"},
    {"number": 47, "volume": 3, "authors": "J. Maynard Smith", "title": "The Theory of Games and the Evolution of Animal Conflicts", "year": "1974"},
    {"number": 48, "volume": 3, "authors": "F. G. Varela, H. R. Maturana, and R. Uribe", "title": "Autopoiesis: The Organization of Living Systems, Its Characterization, and a Model", "year": "1974"},
    {"number": 49, "volume": 3, "authors": "D. Sherrington and S. Kirkpatrick", "title": "Solvable Model of a Spin-Glass", "year": "1975"},
    {"number": 50, "volume": 3, "authors": "H. Haken", "title": "Synergetics", "year": "1976"},
    {"number": 51, "volume": 3, "authors": "K. Hasselmann", "title": "Stochastic Climate Models Part I. Theory", "year": "1976"},
    {"number": 52, "volume": 3, "authors": "S. J. Gould and N. Eldredge", "title": "Punctuated Equilibria: The Tempo and Mode of Evolution Reconsidered", "year": "1977"},
    {"number": 53, "volume": 3, "authors": "G. Parisi", "title": "Infinite Number of Order Parameters for Spin-Glasses", "year": "1979"},
    {"number": 54, "volume": 3, "authors": "N. H. Packard, J. P. Crutchfield, J. D. Farmer, and R. S. Shaw", "title": "Geometry from a Time Series", "year": "1980"},
    {"number": 55, "volume": 3, "authors": "R. Axelrod and W. D. Hamilton", "title": "The Evolution of Cooperation", "year": "1981"},
    {"number": 56, "volume": 3, "authors": "F. J. Dyson", "title": "A Model for the Origin of Life", "year": "1982"},
    {"number": 57, "volume": 3, "authors": "J. J. Hopfield", "title": "Neural Networks and Physical Systems with Emergent Collective Computational Abilities", "year": "1982"},
    {"number": 58, "volume": 3, "authors": "M. J. Feigenbaum", "title": "Universal Behavior in Nonlinear Systems", "year": "1983"},
    {"number": 59, "volume": 3, "authors": "S. Wolfram", "title": "Universality and Complexity in Cellular Automata", "year": "1984"},
    {"number": 60, "volume": 3, "authors": "I. Prigogine and G. Nicolis", "title": "Self-Organisation in Nonequilibrium Systems: Towards a Dynamics of Complexity", "year": "1985"},
    {"number": 61, "volume": 3, "authors": "C. G. Langton", "title": "Studying Artificial Life with Cellular Automata", "year": "1986"},
    {"number": 62, "volume": 3, "authors": "J. Pearl", "title": "Fusion, Propagation, and Structuring in Belief Networks", "year": "1986"},
    {"number": 63, "volume": 3, "authors": "P. Bak, C. Tang, and K. Wiesenfeld", "title": "Self-Organized Criticality: An Explanation of the 1/f Noise", "year": "1987"},
    {"number": 64, "volume": 3, "authors": "S. Kauffman and S. Levin", "title": "Towards a General Theory of Adaptive Walks on Rugged Landscapes", "year": "1987"},
    {"number": 65, "volume": 3, "authors": "C. Reynolds", "title": "Flocks, Herds, and Schools: A Distributed Behavioral Model", "year": "1987"},
    {"number": 66, "volume": 3, "authors": "M. Eigen, J. McCaskill, and P. Schuster", "title": "Molecular Quasi-Species", "year": "1988"},
    {"number": 67, "volume": 4, "authors": "W. B. Arthur", "title": "Competing Technologies, Increasing Returns, and Lock-In by Historical Events", "year": "1989"},
    {"number": 68, "volume": 4, "authors": "A. S. Perelson", "title": "Immune Network Theory", "year": "1989"},
    {"number": 69, "volume": 4, "authors": "J. D. Farmer", "title": "A Rosetta Stone for Connectionism", "year": "1990"},
    {"number": 70, "volume": 4, "authors": "J. A. Wheeler", "title": "Information, Physics, Quantum: The Search for Links", "year": "1990"},
    {"number": 71, "volume": 4, "authors": "W. Bialek, F. Rieke, R. R. de Ruyter van Steveninck, and D. Warland", "title": "Reading a Neural Code", "year": "1991"},
    {"number": 72, "volume": 4, "authors": "J. H. Holland and J. H. Miller", "title": "Artificial Adaptive Agents in Economic Theory", "year": "1991"},
    {"number": 73, "volume": 4, "authors": "K. Lindgren", "title": "Evolutionary Phenomena in Simple Dynamics", "year": "1991"},
    {"number": 74, "volume": 4, "authors": "H. A. Simon", "title": "Organizations and Markets", "year": "1991"},
    {"number": 75, "volume": 4, "authors": "J. S. Lansing and J. M. Kremer", "title": "Emergent Properties of Balinese Water Temple Networks: Coadaptation on a Rugged Fitness Landscape", "year": "1993"},
    {"number": 76, "volume": 4, "authors": "M. Mitchell, P. T. Hraber, and J. P. Crutchfield", "title": "Revisiting the Edge of Chaos: Evolving Cellular Automata to Perform Computations", "year": "1993"},
    {"number": 77, "volume": 4, "authors": "W. B. Arthur", "title": "Inductive Reasoning and Bounded Rationality", "year": "1994"},
    {"number": 78, "volume": 4, "authors": "J. P. Crutchfield", "title": "The Calculi of Emergence: Computation, Dynamics, and Induction", "year": "1994"},
    {"number": 79, "volume": 4, "authors": "S. Forrest, A. S. Perelson, L. Allen, and R. Cherukuri", "title": "Self–Nonself Discrimination in a Computer", "year": "1994"},
    {"number": 80, "volume": 4, "authors": "P. Schuster, W. Fontana, P. F. Stadler, and I. L. Hofacker", "title": "From Sequences to Shapes and Back: A Case Study in RNA Secondary Structures", "year": "1994"},
    {"number": 81, "volume": 4, "authors": "M. Gell-Mann and S. Lloyd", "title": "Information Measures, Effective Complexity, and Total Information", "year": "1996"},
    {"number": 82, "volume": 4, "authors": "F. J. Odling-Smee, K. N. Laland, and M. W. Feldman", "title": "Niche Construction", "year": "1996"},
    {"number": 83, "volume": 4, "authors": "G. B. West, J. H. Brown, and B. J. Enquist", "title": "A General Model for the Origin of Allometric Scaling Laws in Biology", "year": "1997"},
    {"number": 84, "volume": 4, "authors": "D. H. Wolpert and W. G. Macready", "title": "No Free Lunch Theorems for Optimization", "year": "1997"},
    {"number": 85, "volume": 4, "authors": "S. Amari", "title": "Natural Gradient Works Efficiently in Learning", "year": "1998"},
    {"number": 86, "volume": 4, "authors": "S. Bowles", "title": "Endogenous Preferences: The Cultural Consequences of Markets and Other Economic Institutions", "year": "1998"},
    {"number": 87, "volume": 4, "authors": "D. Watts and S. Strogatz", "title": "Collective Dynamics of ‘Small-World’ Networks", "year": "1998"},
    {"number": 88, "volume": 4, "authors": "R. B. Laughlin, D. Pines, J. Schmalian, B. P. Stojkovic, and P. Wolynes", "title": "The Middle Way", "year": "1999"},
    {"number": 89, "volume": 4, "authors": "E. Ostrom", "title": "Collective Action and the Evolution of Social Norms", "year": "2000"},
]

CANONICAL_SOURCES: list[dict[str, Any]] = [
    {
        "id": "src_fpcs_official_toc",
        "title": "Foundational Papers in Complexity Science — official tables of contents",
        "source_type": "publisher_table_of_contents",
        "quality_tier": "A",
        "access": "public",
        "url": FPCS_TOC_URL,
        "date": "2024",
        "notes": "Official item-level contents for the four-volume Santa Fe Institute Press collection. It supports the bibliographic inventory, not the substantive claims of all 89 original papers.",
        "creators": json.dumps(["Santa Fe Institute Press", "David C. Krakauer (editor)"], ensure_ascii=False),
        "publisher": "Santa Fe Institute Press",
        "licence": "source_terms",
        "review_status": "checked_primary_register",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_fpcs_official_citation",
        "title": "Foundational Papers in Complexity Science — official citation",
        "source_type": "publisher_citation_record",
        "quality_tier": "A",
        "access": "public",
        "url": FPCS_CITATION_URL,
        "date": "2024",
        "notes": "Official citation record for the four-volume 2024 collection edited by David C. Krakauer.",
        "creators": json.dumps(["Santa Fe Institute Press"], ensure_ascii=False),
        "publisher": "Santa Fe Institute Press",
        "licence": "source_terms",
        "review_status": "checked_primary_register",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_principia_home",
        "title": "Principia Cybernetica Web",
        "source_type": "official_project_site",
        "quality_tier": "B",
        "access": "public",
        "url": "https://pespmc1.vub.ac.be/",
        "date": "1993–2003",
        "notes": "Official project website. Use it for the project's stated programme, organisation and terminology; do not treat those self-descriptions as independent validation.",
        "creators": json.dumps(["Principia Cybernetica Project editors"], ensure_ascii=False),
        "publisher": "Principia Cybernetica Project",
        "licence": "source_terms",
        "review_status": "checked_primary_register",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_principia_introduction",
        "title": "Introduction to Principia Cybernetica",
        "source_type": "official_project_statement",
        "quality_tier": "B",
        "access": "public",
        "url": "https://pespmc1.vub.ac.be/INTRO.html",
        "date": "1993–2003",
        "notes": "Official account of the project, its evolutionary-cybernetics programme, metasystem-transition language, semantic-network ambitions and dates.",
        "creators": json.dumps(["Francis Heylighen", "Cliff Joslyn", "Valentin Turchin"], ensure_ascii=False),
        "publisher": "Principia Cybernetica Project",
        "licence": "source_terms",
        "review_status": "checked_primary_register",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_principia_systems_concepts",
        "title": "Principia Cybernetica: Systems Concepts",
        "source_type": "official_semantic_network",
        "quality_tier": "B",
        "access": "public",
        "url": "https://pespmc1.vub.ac.be/SYSCONC.html",
        "date": "1992–",
        "notes": "Official semantic-network vocabulary developed by the project editors. It is valuable as a historical corpus and comparator, not as an unquestionable dictionary of the field.",
        "creators": json.dumps(["Principia Cybernetica Project editors", "Cliff Joslyn", "Johan Bollen"], ensure_ascii=False),
        "publisher": "Principia Cybernetica Project",
        "licence": "source_terms",
        "review_status": "checked_primary_register",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_principia_mstt",
        "title": "Principia Cybernetica: Metasystem Transition Theory",
        "source_type": "official_project_theory_page",
        "quality_tier": "B",
        "access": "public",
        "url": "https://pespmc1.vub.ac.be/MSTT.html",
        "date": "",
        "notes": "Official project account of metasystem transition theory and its attribution to work by Valentin Turchin, Cliff Joslyn and Francis Heylighen.",
        "creators": json.dumps(["Principia Cybernetica Project editors"], ensure_ascii=False),
        "publisher": "Principia Cybernetica Project",
        "licence": "source_terms",
        "review_status": "checked_primary_register",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_principia_global_brain",
        "title": "The Global Brain Group",
        "source_type": "official_project_group_page",
        "quality_tier": "B",
        "access": "public",
        "url": "https://pespmc1.vub.ac.be/GBRAIN-L.html",
        "date": "",
        "notes": "Official page for the group associated with Principia Cybernetica. It supports membership and project-history statements, not all wider global-brain claims.",
        "creators": json.dumps(["Principia Cybernetica Project"], ensure_ascii=False),
        "publisher": "Principia Cybernetica Project",
        "licence": "source_terms",
        "review_status": "checked_primary_register",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_ashby_digital_archive",
        "title": "The W. Ross Ashby Digital Archive",
        "source_type": "primary_archive",
        "quality_tier": "A",
        "access": "public",
        "url": "https://www.ashby.info/archive.html",
        "date": "",
        "notes": "Primary digital archive of Ashby's journals and index cards. Strong for chronology, wording and research development; interpretation still requires context.",
        "creators": json.dumps(["W. Ross Ashby Digital Archive", "International Society for the Systems Sciences"], ensure_ascii=False),
        "publisher": "International Society for the Systems Sciences",
        "licence": "source_terms",
        "review_status": "checked_canonical_source",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cybernetics_thought_collective",
        "title": "Cybernetics Thought Collective digital collection",
        "source_type": "multi_institutional_archive",
        "quality_tier": "A",
        "access": "public",
        "url": "https://digital.library.illinois.edu/collections/38ec6eb0-18c3-0135-242c-0050569601ca-1",
        "date": "",
        "notes": "University of Illinois digital collection linking archival records around Ashby, McCulloch, von Foerster, Wiener and the cybernetics network.",
        "creators": json.dumps(["University of Illinois Library"], ensure_ascii=False),
        "publisher": "University of Illinois Library",
        "licence": "collection_terms",
        "review_status": "checked_canonical_source",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_cybernetics_society_archive",
        "title": "The Cybernetics Society archive",
        "source_type": "professional_body_archive",
        "quality_tier": "B",
        "access": "public",
        "url": "https://archive.cybsoc.org/",
        "date": "",
        "notes": "Public archive of a professional society. Useful for events, publications and field history; institutional inclusion is not evidence of intellectual agreement.",
        "creators": json.dumps(["The Cybernetics Society"], ensure_ascii=False),
        "publisher": "The Cybernetics Society",
        "licence": "source_terms",
        "review_status": "checked_canonical_source",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_ifsr_conversations",
        "title": "IFSR Conversations and Dialogues",
        "source_type": "federation_conversation_archive",
        "quality_tier": "B",
        "access": "public",
        "url": "https://ifsr.org/conversations-dialogues/",
        "date": "",
        "notes": "Official archive of IFSR conversations and dialogues. Useful for practitioner discourse and collaborative development, with claims checked against the individual records.",
        "creators": json.dumps(["International Federation for Systems Research"], ensure_ascii=False),
        "publisher": "International Federation for Systems Research",
        "licence": "source_terms",
        "review_status": "checked_canonical_source",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_system_dynamics_bibliography",
        "title": "System Dynamics Society bibliography",
        "source_type": "maintained_field_bibliography",
        "quality_tier": "B",
        "access": "public",
        "url": "https://systemdynamics.org/bibliography/",
        "date": "",
        "notes": "Maintained field bibliography. Strong for discovery and bibliographic coverage; individual sources must still support individual statements.",
        "creators": json.dumps(["System Dynamics Society"], ensure_ascii=False),
        "publisher": "System Dynamics Society",
        "licence": "source_terms",
        "review_status": "checked_canonical_source",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_sfi_research_overview",
        "title": "Santa Fe Institute research overview",
        "source_type": "research_institute_overview",
        "quality_tier": "B",
        "access": "public",
        "url": "https://www.santafe.edu/research/overview",
        "date": "",
        "notes": "Official overview of the institute's current research framing. Useful for institutional scope and terminology, not a neutral definition of complexity science.",
        "creators": json.dumps(["Santa Fe Institute"], ensure_ascii=False),
        "publisher": "Santa Fe Institute",
        "licence": "source_terms",
        "review_status": "checked_canonical_source",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
    {
        "id": "src_necsi_online_resources",
        "title": "New England Complex Systems Institute online resources",
        "source_type": "research_institute_resource_collection",
        "quality_tier": "B",
        "access": "public",
        "url": "https://necsi.edu/online-resources",
        "date": "",
        "notes": "Official resource collection. Use for discovery and teaching material while checking substantive claims against the underlying sources.",
        "creators": json.dumps(["New England Complex Systems Institute"], ensure_ascii=False),
        "publisher": "New England Complex Systems Institute",
        "licence": "source_terms",
        "review_status": "checked_canonical_source",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    },
]

CANONICAL_REGISTER: list[dict[str, Any]] = [
    {"source_id": "src_fpcs_official_toc", "category": "curated historical collection", "scope": "The official 89-paper contents of a four-volume complexity-science collection.", "good_for": "Bibliographic inventory, chronology and identifying a declared canon.", "not_enough_for": "Treating the collection as exhaustive or its selection as neutral."},
    {"source_id": "src_principia_home", "category": "project corpus", "scope": "Principia Cybernetica's official project, reference and research pages.", "good_for": "The project's own organisation, programme, terminology and publication history.", "not_enough_for": "Independent validation of the project's philosophical or scientific claims."},
    {"source_id": "src_principia_dictionary", "category": "curated dictionary", "scope": "Combined ASC, Krippendorff and Hornung glossary material in hypertext form.", "good_for": "Historical terminology, definitions and discovery of source traditions.", "not_enough_for": "A single canonical definition of contested concepts."},
    {"source_id": "src_ashby_digital_archive", "category": "primary archive", "scope": "Ashby's journals and index cards.", "good_for": "Primary chronology, wording, development of ideas and archival locators.", "not_enough_for": "Uncontextualised inference about influence or settled meaning."},
    {"source_id": "src_cybernetics_thought_collective", "category": "multi-institutional archive", "scope": "Digital records connecting major cybernetics figures and institutions.", "good_for": "Correspondence, events, institutional relations and documented human lineage.", "not_enough_for": "Assuming contact means intellectual influence."},
    {"source_id": "src_asc_library", "category": "professional-body library", "scope": "A large searchable cybernetics library maintained by the ASC.", "good_for": "Discovery, bibliography and access to field material.", "not_enough_for": "Endorsement or correctness of every included work."},
    {"source_id": "src_cybernetics_society_archive", "category": "professional-body archive", "scope": "Cybernetics Society events, publications and historical records.", "good_for": "Institutional history, participation and public field records.", "not_enough_for": "Equating society participation with shared doctrine."},
    {"source_id": "src_isss_world_systems", "category": "comparator registry", "scope": "Maps, reference corpora and public systems resources gathered by ISSS.", "good_for": "Finding comparator maps and bodies of knowledge.", "not_enough_for": "Recovering relation semantics where the source map lost them."},
    {"source_id": "src_ifsr_conversations", "category": "conversation archive", "scope": "IFSR conversations and dialogues among systems researchers and practitioners.", "good_for": "Collaborative discourse, practice history and explicit participant accounts.", "not_enough_for": "Turning discussion into consensus or documented influence without further evidence."},
    {"source_id": "src_system_dynamics_bibliography", "category": "maintained bibliography", "scope": "A large field bibliography maintained by the System Dynamics Society.", "good_for": "Systematic discovery and bibliographic checking in system dynamics.", "not_enough_for": "Substantive support without reading the listed work."},
    {"source_id": "src_sfi_research_overview", "category": "research-institute corpus", "scope": "Santa Fe Institute research framing and public materials.", "good_for": "Institutional scope, current terminology and discovery of complexity research.", "not_enough_for": "A neutral boundary around complexity science."},
    {"source_id": "src_necsi_online_resources", "category": "research and teaching collection", "scope": "NECSI public complexity resources.", "good_for": "Discovery, teaching and institutional comparison.", "not_enough_for": "Replacing original papers or independent scholarly review."},
]

PRINCIPIA_NODES: list[dict[str, Any]] = [
    {
        "id": "organisation_principia_cybernetica_project",
        "label": "Principia Cybernetica Project",
        "entity_type": "organisation",
        "description": "An international project begun in 1989 to develop a collaborative philosophical world-view grounded in the project's account of evolutionary cybernetics.",
        "aliases": ["PCP"],
        "source_ids": ["src_principia_home", "src_principia_introduction"],
        "set_tags": ["cybernetics", "complexity", "principia"],
        "x": 0.70,
        "y": -0.32,
    },
    {
        "id": "publication_principia_cybernetica_web",
        "label": "Principia Cybernetica Web",
        "entity_type": "publication",
        "description": "The public hypertext and semantic-network website of the Principia Cybernetica Project, first implemented on the web in 1993.",
        "aliases": ["PCP Web"],
        "source_ids": ["src_principia_home", "src_principia_introduction"],
        "set_tags": ["cybernetics", "complexity", "principia", "semantic_network"],
        "x": 0.76,
        "y": -0.22,
    },
    {
        "id": "concept_evolutionary_cybernetics",
        "label": "Evolutionary cybernetics",
        "entity_type": "concept",
        "description": "Principia Cybernetica's programme for interpreting evolution as continuing self-organisation and the emergence of higher levels of control.",
        "aliases": [],
        "source_ids": ["src_principia_introduction"],
        "set_tags": ["cybernetics", "complexity", "principia", "evolution"],
        "x": 0.62,
        "y": -0.20,
    },
    {
        "id": "concept_metasystem_transition",
        "label": "Metasystem transition",
        "entity_type": "concept",
        "description": "In Principia Cybernetica, the emergence of a new level of control that coordinates previously separate systems into a higher-order system.",
        "aliases": ["MST"],
        "source_ids": ["src_principia_introduction", "src_principia_mstt"],
        "set_tags": ["cybernetics", "complexity", "principia", "evolution"],
        "x": 0.58,
        "y": -0.10,
    },
    {
        "id": "approach_family_metasystem_transition_theory",
        "label": "Metasystem Transition Theory",
        "entity_type": "approach_family",
        "description": "A theoretical programme developed within Principia Cybernetica around the repeated emergence of higher levels of control and organisation.",
        "aliases": ["MSTT"],
        "source_ids": ["src_principia_mstt"],
        "set_tags": ["cybernetics", "complexity", "principia", "evolution"],
        "x": 0.66,
        "y": -0.08,
    },
    {
        "id": "concept_global_brain",
        "label": "Global brain",
        "entity_type": "concept",
        "description": "A metaphor and research programme treating worldwide communication networks as a potentially self-organising system with distributed collective intelligence.",
        "aliases": ["Global Brain"],
        "source_ids": ["src_principia_home", "src_principia_global_brain"],
        "set_tags": ["cybernetics", "complexity", "principia", "networks"],
        "x": 0.82,
        "y": -0.10,
    },
    {
        "id": "person_francis_heylighen",
        "label": "Francis Heylighen",
        "entity_type": "person",
        "description": "A cybernetics researcher and Principia Cybernetica editor associated with its evolutionary-cybernetics, semantic-network and global-brain programmes.",
        "aliases": [],
        "source_ids": ["src_principia_introduction", "src_principia_dictionary", "src_principia_global_brain"],
        "set_tags": ["cybernetics", "complexity", "principia", "person"],
        "x": 0.76,
        "y": -0.42,
    },
    {
        "id": "person_valentin_turchin",
        "label": "Valentin Turchin",
        "entity_type": "person",
        "description": "A cybernetician and Principia Cybernetica editor whose work introduced and developed the project's metasystem-transition framework.",
        "aliases": [],
        "source_ids": ["src_principia_introduction", "src_principia_mstt"],
        "set_tags": ["cybernetics", "complexity", "principia", "person"],
        "x": 0.68,
        "y": -0.44,
    },
    {
        "id": "person_cliff_joslyn",
        "label": "Cliff Joslyn",
        "entity_type": "person",
        "description": "A cybernetics researcher and Principia Cybernetica editor associated with metasystem-transition theory and the project's semantic-network implementation.",
        "aliases": [],
        "source_ids": ["src_principia_introduction", "src_principia_systems_concepts", "src_principia_mstt"],
        "set_tags": ["cybernetics", "complexity", "principia", "person"],
        "x": 0.84,
        "y": -0.40,
    },
]

# source, target, relation_type, family, sources, phrase, note
PRINCIPIA_EDGES = [
    ("publication_principia_cybernetica_web", "organisation_principia_cybernetica_project", "part_of", "classification", ["src_principia_home"], "is the public web of", "The project site identifies the web as the website of PCP."),
    ("comparator_corpus_principia_cybernetica_web_dictionary", "publication_principia_cybernetica_web", "part_of", "classification", ["src_principia_dictionary"], "is part of", "The dictionary identifies itself as part of Principia Cybernetica Web."),
    ("concept_evolutionary_cybernetics", "organisation_principia_cybernetica_project", "espouses_epistemology", "identity", ["src_principia_introduction"], "is espoused by", "The project calls its specific approach evolutionary cybernetics."),
    ("concept_metasystem_transition", "approach_family_metasystem_transition_theory", "part_of", "classification", ["src_principia_mstt"], "is a central concept in", "The project presents metasystem transition as the central unit of the theory."),
    ("approach_family_metasystem_transition_theory", "organisation_principia_cybernetica_project", "part_of", "classification", ["src_principia_mstt"], "was developed within", "The official project page presents MSTT as a Principia Cybernetica programme."),
    ("concept_global_brain", "organisation_principia_cybernetica_project", "part_of", "classification", ["src_principia_home", "src_principia_global_brain"], "is a research programme associated with", "The project describes intelligent-web research inspired by the global-brain metaphor."),
    ("person_francis_heylighen", "organisation_principia_cybernetica_project", "member_of", "classification", ["src_principia_introduction"], "was an editor of", "The official introduction names Heylighen as an author and editor."),
    ("person_valentin_turchin", "organisation_principia_cybernetica_project", "member_of", "classification", ["src_principia_introduction"], "was an editor of", "The official introduction names Turchin as an author and editor."),
    ("person_cliff_joslyn", "organisation_principia_cybernetica_project", "member_of", "classification", ["src_principia_introduction"], "was an editor of", "The official introduction names Joslyn as an author and editor."),
    ("approach_family_metasystem_transition_theory", "person_valentin_turchin", "formulated_by", "historical", ["src_principia_mstt"], "was formulated in part by", "The official MSTT page attributes the basic tenets to Turchin and Joslyn."),
    ("approach_family_metasystem_transition_theory", "person_cliff_joslyn", "formulated_by", "historical", ["src_principia_mstt"], "was formulated in part by", "The official MSTT page attributes the basic tenets to Turchin and Joslyn."),
    ("comparator_corpus_principia_cybernetica_web_dictionary", "person_francis_heylighen", "authored_by", "documentary", ["src_principia_dictionary"], "was compiled and converted to hypertext by", "The dictionary page credits Francis Heylighen, helped by An Vranckx."),
    ("concept_evolutionary_cybernetics", "tradition_cybernetics", "extends", "influence", ["src_principia_introduction"], "extends", "The project explicitly presents the programme as a further development of cybernetic principles."),
    ("concept_metasystem_transition", "concept_self_organisation", "explanatory_prerequisite", "conceptual", ["src_principia_introduction"], "uses an account of", "The project frames evolution and metasystem transitions through continuing self-organisation."),
]

FPCS_AUTHOR_LINKS: dict[int, list[str]] = {
    5: ["person_warren_mcculloch"],
    6: ["person_arturo_rosenblueth", "person_norbert_wiener", "person_julian_bigelow"],
    8: ["person_arturo_rosenblueth", "person_norbert_wiener"],
    9: ["person_claude_e_shannon"],
    11: ["person_alan_turing"],
    13: ["person_alan_turing"],
    21: ["person_herbert_simon"],
    34: ["person_roger_c_conant", "person_w_ross_ashby"],
    42: ["person_heinz_von_foerster"],
    46: ["person_herbert_simon"],
    48: ["person_francisco_varela", "person_humberto_maturana"],
    74: ["person_herbert_simon"],
}

FPCS_CONCEPT_LINKS: dict[int, list[str]] = {
    6: ["tradition_cybernetics"],
    9: ["concept_information_theory"],
    10: ["concept_complexity"],
    11: ["concept_recursion"],
    21: ["concept_complexity"],
    23: ["concept_complexity"],
    29: ["concept_emergence"],
    31: ["concept_information"],
    34: ["concept_regulation", "concept_requisite_variety"],
    39: ["concept_emergence"],
    42: ["concept_observer"],
    48: ["concept_self_organisation"],
    59: ["concept_complexity"],
    60: ["concept_self_organisation", "concept_complexity"],
    63: ["concept_self_organisation"],
    78: ["concept_emergence"],
}


def parse(value: Any, fallback: Any = None) -> Any:
    if fallback is None:
        fallback = []
    if isinstance(value, (list, dict)):
        return value
    if value in (None, ""):
        return fallback
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return fallback


def j(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def normalise_url(value: str) -> str:
    return value.rstrip("/")


def upsert_sources(existing: list[dict[str, Any]], additions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {source["id"]: dict(source) for source in existing}
    id_by_url = {
        normalise_url(str(source.get("url") or "")): source["id"]
        for source in existing if source.get("url")
    }
    for source in additions:
        url_key = normalise_url(str(source.get("url") or ""))
        target_id = id_by_url.get(url_key, source["id"])
        merged = {**by_id.get(target_id, {}), **source, "id": target_id}
        for key in ("doi", "isbn", "archived_url", "content_hash"):
            merged.setdefault(key, "")
        by_id[target_id] = merged
        if url_key:
            id_by_url[url_key] = target_id
    return list(by_id.values())


def public_node(record: dict[str, Any]) -> dict[str, Any]:
    node = {
        "id": record["id"],
        "label": record["label"],
        "entity_type": record["entity_type"],
        "description": record["description"],
        "aliases": j(record.get("aliases", [])),
        "boundary_ring": str(record.get("boundary_ring", 1)),
        "inclusion_reason": record.get("inclusion_reason", "named_public_corpus"),
        "status": "accepted",
        "source_ids": j(record.get("source_ids", [])),
        "set_tags": j(record.get("set_tags", [])),
        "espoused_labels": j(record.get("espoused_labels", [])),
        "observed_clusters": j(record.get("observed_clusters", [])),
        "canonical_definition": record["description"],
        "valid_from": record.get("valid_from", ""),
        "valid_to": record.get("valid_to", ""),
        "external_ids": j(record.get("external_ids", {})),
        "geographies": j(record.get("geographies", [])),
        "licence": record.get("licence", "source_terms"),
        "review_status": record.get("review_status", "bibliographic_first_pass"),
        "reviewed_by": "curator_release_pass",
        "reviewed_at": GENERATED,
        "x": record.get("x", 0),
        "y": record.get("y", 0),
        "canonical_id": record["id"],
        "public_visibility": "public",
        "publication_level": record.get("publication_level", "described"),
        "public_stub_text": "",
        "public_source_count": len(record.get("source_ids", [])),
        "no_public_link_count": 0,
    }
    return node


def upsert_nodes(existing: list[dict[str, Any]], additions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {node["id"]: dict(node) for node in existing}
    for node in additions:
        by_id[node["id"]] = {**by_id.get(node["id"], {}), **node}
    return list(by_id.values())


def edge_record(
    edge_id: str,
    source: str,
    target: str,
    relation_type: str,
    family: str,
    source_ids: list[str],
    phrase: str,
    note: str,
    *,
    status: str = "accepted",
    confidence: str = "0.9",
) -> dict[str, Any]:
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relation_type": relation_type,
        "relation_family": family,
        "directed": "true",
        "dependency_kind": "",
        "confidence": confidence,
        "claim_status": status,
        "source_ids": j(source_ids),
        "evidence_ids": "[]",
        "source_locator": "",
        "valid_from": "",
        "valid_to": "",
        "scope_conditions": note,
        "assertion_mode": "asserted",
        "inference_method": "",
        "claim_id": "",
        "reviewed_by": "curator_release_pass",
        "reviewed_at": GENERATED,
        "notes": note,
        "plain_phrase": phrase,
        "public_review_label": "accepted in bibliographic first pass" if status == "accepted" else status,
    }


def upsert_edges(existing: list[dict[str, Any]], additions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {edge["id"]: dict(edge) for edge in existing}
    for edge in additions:
        by_id[edge["id"]] = {**by_id.get(edge["id"], {}), **edge}
    return list(by_id.values())


def make_foundational_nodes_and_edges() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    corpus = public_node({
        "id": "corpus_foundational_papers_2024",
        "label": "Foundational Papers in Complexity Science",
        "entity_type": "corpus",
        "description": "A four-volume 2024 Santa Fe Institute Press collection of 89 historical papers selected to represent important foundations of complexity science.",
        "aliases": ["Foundational Papers in Complexity Science collection"],
        "source_ids": ["src_fpcs_official_toc", "src_fpcs_official_citation"],
        "set_tags": ["complexity", "foundational_papers", "corpus"],
        "x": 0.08,
        "y": 0.68,
        "publication_level": "described",
        "review_status": "official_collection_registered",
    })
    nodes = [corpus]
    edges: list[dict[str, Any]] = []
    inventory: list[dict[str, Any]] = []
    ranges = {1: (1, 20), 2: (21, 44), 3: (45, 66), 4: (67, 89)}
    for paper in FPCS_PAPERS:
        number = paper["number"]
        volume = paper["volume"]
        year_text = f" ({paper['year']})" if paper["year"] else ""
        node_id = f"publication_fpcs_{number:03d}"
        start, end = ranges[volume]
        position = (number - start) / max(1, end - start)
        angle = math.pi * (0.12 + 0.76 * position) + (volume - 2.5) * 0.07
        radius = 0.64 + 0.055 * volume
        x = round(math.cos(angle) * radius, 6)
        y = round(0.38 + math.sin(angle) * 0.42 + (volume - 2.5) * 0.07, 6)
        description = (
            f"{paper['authors']}, ‘{paper['title']}’{year_text}; item {number} in volume {volume} "
            "of the 2024 Foundational Papers in Complexity Science collection. This is a bibliographic first-pass entry, not yet a substantive summary."
        )
        nodes.append(public_node({
            "id": node_id,
            "label": paper["title"],
            "entity_type": "publication",
            "description": description,
            "aliases": [],
            "source_ids": ["src_fpcs_official_toc"],
            "set_tags": ["complexity", "foundational_papers", f"volume_{volume}"],
            "x": x,
            "y": y,
            "external_ids": {"fpcs_number": number, "fpcs_volume": volume},
            "review_status": "official_toc_bibliographic_inventory",
        }))
        inventory.append({**paper, "node_id": node_id})
        edges.append(edge_record(
            f"e_fpcs_part_{number:03d}", node_id, "corpus_foundational_papers_2024", "part_of", "classification",
            ["src_fpcs_official_toc"], "is item in", f"Official table of contents, volume {volume}, item {number}."
        ))
        for person_id in FPCS_AUTHOR_LINKS.get(number, []):
            edges.append(edge_record(
                f"e_fpcs_author_{number:03d}_{person_id.removeprefix('person_')}", node_id, person_id,
                "authored_by", "documentary", ["src_fpcs_official_toc"], "was authored in part by",
                "Bibliographic authorship recorded in the official table of contents."
            ))
        for concept_id in FPCS_CONCEPT_LINKS.get(number, []):
            edges.append(edge_record(
                f"e_fpcs_topic_{number:03d}_{concept_id}", concept_id, node_id,
                "described_by", "evidence", ["src_fpcs_official_toc"], "has a foundational treatment in",
                "A cautious first-pass topic link based on the paper title and collection placement; substantive review remains pending.",
                status="provisional", confidence="0.65"
            ))
    return nodes, edges, inventory


def update_principia_dictionary_node(nodes: list[dict[str, Any]]) -> None:
    for node in nodes:
        if node.get("id") != "comparator_corpus_principia_cybernetica_web_dictionary":
            continue
        description = (
            "A hypertext dictionary combining the ASC Glossary, Klaus Krippendorff's dictionary and Bernd Hornung's glossary, compiled and converted by Francis Heylighen with help from An Vranckx."
        )
        node.update(public_node({
            "id": node["id"],
            "label": "Web Dictionary of Cybernetics and Systems",
            "entity_type": "comparator_corpus",
            "description": description,
            "aliases": ["Principia Cybernetica Web Dictionary"],
            "source_ids": ["src_principia_dictionary"],
            "set_tags": ["cybernetics", "systems", "principia", "dictionary", "comparator"],
            "x": 0.84,
            "y": -0.26,
            "review_status": "official_source_first_pass",
        }))
        break


def substantive(edge: dict[str, Any]) -> bool:
    return edge.get("relation_family") in {
        "conceptual", "historical", "influence", "practice", "contestation", "human", "identity"
    } and edge.get("relation_type") != "legacy_association_unspecified" and edge.get("claim_status") != "legacy_unresolved"


def derive_neighbourhoods(data: dict[str, Any]) -> dict[str, Any]:
    redirects = data.get("canonical_redirects", {})
    canonical = lambda node_id: redirects.get(node_id, node_id)
    excluded_types = {"publication", "corpus", "comparator_corpus", "source", "event"}
    public_nodes = {
        node["id"]: node for node in data.get("nodes", [])
        if node.get("public_visibility") == "public"
        and canonical(node["id"]) == node["id"]
        and node.get("entity_type") not in excluded_types
    }
    adjacency: dict[str, dict[str, int]] = {node_id: {} for node_id in public_nodes}
    edge_weights: Counter[tuple[str, str]] = Counter()
    for edge in data.get("edges", []):
        if not substantive(edge):
            continue
        source = canonical(edge.get("source", ""))
        target = canonical(edge.get("target", ""))
        if source not in public_nodes or target not in public_nodes or source == target:
            continue
        pair = tuple(sorted((source, target)))
        edge_weights[pair] += 1
        adjacency[source][target] = adjacency[source].get(target, 0) + 1
        adjacency[target][source] = adjacency[target].get(source, 0) + 1

    # Connected components report fragmentation. Communities within the
    # connected material are then found by deterministic greedy modularity.
    seen: set[str] = set()
    components: list[list[str]] = []
    for start in sorted(adjacency):
        if start in seen:
            continue
        queue = deque([start])
        seen.add(start)
        component: list[str] = []
        while queue:
            current = queue.popleft()
            component.append(current)
            for neighbour in sorted(adjacency[current]):
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        components.append(component)

    active = {node_id for node_id, neighbours in adjacency.items() if neighbours}
    degree = {node_id: sum(adjacency[node_id].values()) for node_id in active}
    communities: dict[str, set[str]] = {node_id: {node_id} for node_id in active}
    node_community = {node_id: node_id for node_id in active}
    total_degree = dict(degree)
    total_edge_weight = sum(edge_weights.values())

    # Clauset-Newman-Moore style greedy merging. Each accepted merge increases
    # weighted modularity. It is deterministic because ties are resolved by id.
    if total_edge_weight:
        while True:
            cross_weights: Counter[tuple[str, str]] = Counter()
            for (source, target), weight in edge_weights.items():
                source_community = node_community[source]
                target_community = node_community[target]
                if source_community != target_community:
                    cross_weights[tuple(sorted((source_community, target_community)))] += weight
            best_pair: tuple[str, str] | None = None
            best_gain = 1e-12
            for (left, right), cross_weight in cross_weights.items():
                gain = (
                    cross_weight / total_edge_weight
                    - (total_degree[left] * total_degree[right]) / (2 * total_edge_weight * total_edge_weight)
                )
                if gain > best_gain + 1e-12 or (
                    abs(gain - best_gain) <= 1e-12
                    and best_pair is not None
                    and (left, right) < best_pair
                ):
                    best_gain = gain
                    best_pair = (left, right)
            if best_pair is None:
                break
            left, right = best_pair
            keep, drop = (left, right) if left < right else (right, left)
            communities[keep] |= communities.pop(drop)
            total_degree[keep] += total_degree.pop(drop)
            for node_id in communities[keep]:
                node_community[node_id] = keep

    # Tiny communities are retained only where they are disconnected from the
    # larger graph. Connected fragments below five nodes join the neighbouring
    # community with which they share the most typed connection weight.
    for _ in range(20):
        small = [community_id for community_id, members in communities.items() if len(members) < 5]
        changed = False
        for community_id in sorted(small, key=lambda item: (len(communities.get(item, set())), item)):
            if community_id not in communities:
                continue
            neighbour_weight: Counter[str] = Counter()
            for (source, target), weight in edge_weights.items():
                source_community = node_community[source]
                target_community = node_community[target]
                if source_community == community_id and target_community != community_id:
                    neighbour_weight[target_community] += weight
                elif target_community == community_id and source_community != community_id:
                    neighbour_weight[source_community] += weight
            if not neighbour_weight:
                continue
            target_community = max(
                neighbour_weight,
                key=lambda item: (neighbour_weight[item], len(communities[item]), item),
            )
            communities[target_community] |= communities.pop(community_id)
            total_degree[target_community] += total_degree.pop(community_id)
            for node_id in communities[target_community]:
                node_community[node_id] = target_community
            changed = True
        if not changed:
            break

    anchors = [
        ({"concept_feedback", "concept_negative_feedback", "tradition_control_theory", "tradition_cybernetics"}, "Feedback, control and learning"),
        ({"concept_boundary", "concept_information", "method_or_methodology_systemic_intervention"}, "Boundaries, information and systemic intervention"),
        ({"concept_observer", "concept_emergence", "concept_self_organisation"}, "Observation, emergence and self-organisation"),
        ({"concept_recursion", "person_alan_turing", "person_kurt_gödel"}, "Recursion, computation and self-reference"),
        ({"concept_viability", "concept_requisite_variety", "method_or_methodology_viable_system_model_vsm"}, "Viability, variety and organisation"),
        ({"approach_family_metasystem_transition_theory", "person_valentin_turchin", "person_cliff_joslyn"}, "Metasystem-transition theory and its formulators"),
    ]
    candidate_communities = [members for members in communities.values() if len(members) >= 3]
    candidate_communities.sort(
        key=lambda members: (-len(members), sorted(public_nodes[node_id]["label"] for node_id in members)[0])
    )
    clusters: list[dict[str, Any]] = []
    membership: dict[str, list[str]] = {node_id: [] for node_id in public_nodes}
    for index, members in enumerate(candidate_communities[:12], start=1):
        label = ""
        for anchor_ids, anchor_label in anchors:
            if members & anchor_ids:
                label = anchor_label
                break
        degree_rank = sorted(
            members,
            key=lambda node_id: (-degree.get(node_id, 0), public_nodes[node_id]["label"]),
        )
        central = degree_rank[:5]
        if not label:
            names = [public_nodes[node_id]["label"] for node_id in central[:3]]
            label = ", ".join(names[:-1]) + (f" and {names[-1]}" if len(names) > 1 else names[0])
        cluster_id = f"observed_neighbourhood_{index:02d}"
        internal_edges = sum(
            weight for pair, weight in edge_weights.items()
            if pair[0] in members and pair[1] in members
        )
        clusters.append({
            "id": cluster_id,
            "label": label,
            "size": len(members),
            "edge_count": internal_edges,
            "central_node_ids": central,
            "node_ids": sorted(members),
            "method": "Deterministic greedy modularity on the undirected graph of current public conceptual, historical, influence, practice, human, identity and contestation connections.",
            "status": "provisional_observed_neighbourhood",
            "caveat": "This reflects current coverage and curatorial boundary choices. It is a diagnostic neighbourhood, not a discovered natural kind or settled school.",
        })
        for node_id in members:
            membership[node_id].append(cluster_id)

    for node in data.get("nodes", []):
        if node.get("id") in membership:
            node["observed_clusters"] = j(membership[node["id"]])

    isolates = [node_id for node_id, neighbours in adjacency.items() if not neighbours]
    return {
        "release": RELEASE,
        "method": "Current public non-publication entries were linked through substantive typed relations. Fragmentation is reported by connected component; provisional neighbourhoods within connected material are produced by deterministic greedy modularity.",
        "analytic_population_count": len(public_nodes),
        "substantive_edge_weight": total_edge_weight,
        "component_count": len(components),
        "named_neighbourhood_count": len(clusters),
        "isolated_entry_count": len(isolates),
        "isolated_node_ids": sorted(isolates),
        "neighbourhoods": clusters,
        "interpretation": "The graph presently has several coherent conceptual-practice neighbourhoods and a large weakly connected periphery. The periphery is chiefly a connection and evidence backlog, not evidence for hundreds of independent schools.",
    }

def update_collection_register(data: dict[str, Any]) -> None:
    collections = {item["id"]: item for item in data.get("public_collections", [])}
    additions = [
        {"id": "foundational_papers", "label": "Foundational papers", "description": "The complete 89-item bibliographic first pass through the named Santa Fe Institute Press collection."},
        {"id": "principia", "label": "Principia Cybernetica", "description": "Project, web corpus, people and concepts represented from official Principia sources."},
        {"id": "canonical_sources", "label": "Canonical source register", "description": "High-value public archives, bibliographies, institutional corpora and comparator collections, with limits stated."},
        {"id": "observed_neighbourhoods", "label": "Observed neighbourhoods", "description": "Provisional groupings generated from current substantive graph connections rather than imposed schools."},
    ]
    for item in additions:
        collections[item["id"]] = item
    data["public_collections"] = list(collections.values())

    corpus = {item["id"]: item for item in data.get("corpus_register", [])}
    corpus["corpus_foundational_complexity_papers"] = {
        "id": "corpus_foundational_complexity_papers",
        "label": "Foundational Papers in Complexity Science",
        "status": "first_pass_itemised_89_publication_entries",
        "issue_url": f"{REPOSITORY}/issues/3",
        "source_ids": ["src_fpcs_official_toc", "src_fpcs_official_citation"],
        "completion_test": "All 89 historical papers are inventoried and browsable. Substantive summaries, original-publication locators and connection review remain explicit next work.",
    }
    corpus["corpus_principia_cybernetica"] = {
        "id": "corpus_principia_cybernetica",
        "label": "Principia Cybernetica",
        "status": "first_pass_project_people_concepts_and_corpora_mapped",
        "issue_url": f"{REPOSITORY}/issues/12",
        "source_ids": ["src_principia_home", "src_principia_introduction", "src_principia_dictionary", "src_principia_systems_concepts", "src_principia_mstt", "src_principia_global_brain"],
        "completion_test": "The first project structure is public; systematic page-level corpus review and independent contextualisation remain pending.",
    }
    corpus["corpus_canonical_public_sources"] = {
        "id": "corpus_canonical_public_sources",
        "label": "Canonical public source register",
        "status": "first_register_published_and_open_for_extension",
        "issue_url": f"{REPOSITORY}/issues/12",
        "source_ids": [item["source_id"] for item in CANONICAL_REGISTER],
        "completion_test": "Each registered source states its type, scope, use and limit; additional traditions and non-English corpora remain to be added.",
    }
    data["corpus_register"] = list(corpus.values())


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    # Remove the obsolete pre-2024 FPCS registration. The official 2024
    # project explicitly provides a print collection and public contents site,
    # not the unrelated PDF previously registered under this id.
    data["sources"] = [
        source for source in data.get("sources", [])
        if source.get("id") != "src_foundational_papers_complexity_science"
    ]

    data["sources"] = upsert_sources(data.get("sources", []), CANONICAL_SOURCES)
    # Ensure the existing dictionary record carries the official source detail.
    data["sources"] = upsert_sources(data["sources"], [{
        "id": "src_principia_dictionary",
        "title": "Web Dictionary of Cybernetics and Systems",
        "source_type": "curated_dictionary",
        "quality_tier": "B",
        "access": "public",
        "url": "https://pespmc1.vub.ac.be/ASC/INDEXASC.html",
        "date": "",
        "notes": "Official Principia page describing the combination of the ASC, Krippendorff and Hornung glossaries, compiled and converted to hypertext by Francis Heylighen with help from An Vranckx.",
        "creators": j(["Francis Heylighen", "An Vranckx", "ASC glossary contributors", "Klaus Krippendorff", "Bernd Hornung"]),
        "publisher": "Principia Cybernetica Project",
        "licence": "source_terms",
        "review_status": "checked_primary_register",
        "last_checked": GENERATED,
        "public_link_status": "public_link",
    }])

    fpcs_nodes, fpcs_edges, inventory = make_foundational_nodes_and_edges()
    principia_nodes = [public_node(record) for record in PRINCIPIA_NODES]
    data["nodes"] = upsert_nodes(data.get("nodes", []), fpcs_nodes + principia_nodes)
    update_principia_dictionary_node(data["nodes"])

    principia_edges = [
        edge_record(f"e_principia_{index:02d}", source, target, relation_type, family, source_ids, phrase, note)
        for index, (source, target, relation_type, family, source_ids, phrase, note) in enumerate(PRINCIPIA_EDGES, start=1)
    ]
    data["edges"] = upsert_edges(data.get("edges", []), fpcs_edges + principia_edges)
    data["foundational_papers"] = inventory
    data["canonical_source_register"] = CANONICAL_REGISTER
    update_collection_register(data)
    data["emergent_neighbourhoods"] = derive_neighbourhoods(data)

    meta = data.setdefault("meta", {})
    meta.update({
        "release": RELEASE,
        "generated": GENERATED,
        "status": "public alpha with corpus inventory, source register and observed graph neighbourhoods",
        "author_role": "curator",
        "coverage_status": "The 89-paper Foundational Papers collection is itemised; Principia Cybernetica has a first connected representation; source and neighbourhood registers are public. Evidence depth remains uneven.",
        "membership_model": "curator-approved roles; no automatic permissions; agent-assisted work requires a named human sponsor",
        "map_model": "reader, provenance and full-graph layers with provisional observed neighbourhoods",
    })
    redirects = data.get("canonical_redirects", {})
    canonical = lambda node_id: redirects.get(node_id, node_id)
    public_nodes = [node for node in data.get("nodes", []) if node.get("public_visibility") == "public" and canonical(node["id"]) == node["id"]]
    meta.update({
        "node_count": len(data.get("nodes", [])),
        "edge_count": len(data.get("edges", [])),
        "source_count": len(data.get("sources", [])),
        "claim_count": len(data.get("claims", [])),
        "evidence_count": len(data.get("evidence", [])),
        "profile_count": len(data.get("profiles", [])),
        "journey_count": len(data.get("journeys", [])),
        "public_entry_count": len(public_nodes),
        "described_entry_count": sum(node.get("publication_level") != "research_stub" for node in public_nodes),
        "stub_entry_count": sum(node.get("publication_level") == "research_stub" for node in public_nodes),
        "public_link_source_count": sum(bool(source.get("url")) for source in data.get("sources", [])),
        "no_public_link_source_count": sum(not bool(source.get("url")) for source in data.get("sources", [])),
        "corpus_register_count": len(data.get("corpus_register", [])),
        "foundational_paper_count": len(inventory),
        "canonical_source_register_count": len(CANONICAL_REGISTER),
        "observed_neighbourhood_count": len(data["emergent_neighbourhoods"]["neighbourhoods"]),
    })

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    print(
        f"Applied {RELEASE}: {meta['public_entry_count']} public entries, {meta['edge_count']} edges, "
        f"{meta['source_count']} sources, {meta['foundational_paper_count']} foundational papers and "
        f"{meta['observed_neighbourhood_count']} named observed neighbourhoods."
    )


if __name__ == "__main__":
    main()
