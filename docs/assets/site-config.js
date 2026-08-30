window.TANGLE_CONFIG = {
  projectTitle: "The Necessary Tangle",
  repositoryUrl: "https://github.com/antlerboy/the-necessary-tangle",
  issuesUrl: "https://github.com/antlerboy/the-necessary-tangle/issues",
  discussionsUrl: "https://github.com/antlerboy/the-necessary-tangle/discussions",
  authorName: "Benjamin P Taylor",
  authorRole: "curator",
  authorUrl: "https://www.antlerboy.com/",
  contentLicence: "CC BY-SA 4.0",
  contentLicenceUrl: "https://creativecommons.org/licenses/by-sa/4.0/",
  publishedUrl: "https://transduction.systems/"
};

/*
 * 0.20.3 reader/source corrections.
 *
 * This file runs before public-data.js. Intercepting that one assignment lets
 * the live reader correct a small number of source and relation records before
 * app.js indexes the graph, without republishing the source-owner-gated prior-map
 * derivative or rewriting the multi-megabyte checked-in data artefact by hand.
 */
(() => {
  'use strict';

  let resolvedData;

  function parseList(value) {
    if (Array.isArray(value)) return value;
    if (!value) return [];
    try {
      const parsed = JSON.parse(value);
      return Array.isArray(parsed) ? parsed : [];
    } catch (_) {
      return [];
    }
  }

  function addSource(data, source) {
    const sources = data.sources || (data.sources = []);
    if (!sources.some((item) => item.id === source.id)) sources.push(source);
  }

  function addEdge(data, edge) {
    const edges = data.edges || (data.edges = []);
    if (!edges.some((item) => item.id === edge.id)) edges.push(edge);
  }

  function addMiningRecord(data, record) {
    const records = data.source_mining_register || (data.source_mining_register = []);
    if (!records.some((item) => item.id === record.id)) records.push(record);
  }

  function patchScioSources(data) {
    const currentGuideUrl = 'https://www.systemspractice.org/sites/default/files/2025-01/SCiO%20CF%20Resources%20-%20colour%20Jan2025.pdf';
    const sysbokUrl = 'https://www.systemspractice.org/sysbok-from-scio';

    (data.sources || []).forEach((source) => {
      if (source.id === 'src_scio_cf_resources_2022' || /SCiO CF Resources v9 draft/i.test(source.title || '')) {
        source.title = 'SCiO CF Resources v10 Jan2025';
        source.url = currentGuideUrl;
        source.date = '2025-01';
        source.access = 'public';
        source.public_link_status = 'public_link';
        source.review_status = 'checked';
        source.last_checked = '2026-08-30';
        source.notes = 'Current public SCiO Competency Framework resource guide. It records sources and examples used around the competency framework; inclusion documents SCiO practice and does not establish independent authority or effectiveness.';
      }
      if (/^SCiO SysBoK\b/i.test(source.title || '')) {
        source.url = sysbokUrl;
        source.access = 'public';
        source.public_link_status = 'public_link';
        source.review_status = 'checked';
        source.last_checked = '2026-08-30';
        source.notes = 'Public SCiO SysBoK source. The maintained SCiO page describes SysBoK as an incomplete work in progress and links to the live Kumu model; item-level statements in the atlas may still derive from an earlier named SysBoK snapshot.';
      }
    });

    addSource(data, {
      id: 'src_scio_resource_library_live_2026',
      title: 'SCiO resource library',
      source_type: 'official_professional_body_resource_corpus',
      quality_tier: 'A',
      access: 'public_catalogue_mixed_item_rights',
      url: 'https://www.systemspractice.org/resources',
      date: 'current; checked 2026-08-30',
      notes: 'Live SCiO resource catalogue. On 30 August 2026 the public index reported 572 resources and exposed filters for resource type, language, category, author, organiser and attachment type. Reuse rights vary by item and must be respected.',
      creators: '["SCiO — Systems and Complexity in Organisation"]',
      publisher: 'SCiO — Systems and Complexity in Organisation',
      licence: 'mixed_item_level_rights',
      review_status: 'checked',
      last_checked: '2026-08-30',
      public_link_status: 'public_link'
    });

    addSource(data, {
      id: 'src_scio_sysbok_live_2026',
      title: 'SysBoK, from SCiO — live public model',
      source_type: 'official_professional_body_connected_concept_model',
      quality_tier: 'A',
      access: 'public',
      url: sysbokUrl,
      date: 'current; checked 2026-08-30',
      notes: 'SCiO describes SysBoK as an incomplete work-in-progress connected Systems Thinking concepts model created by SCiO members. The public page links to the Kumu model and says it focuses especially on precedents and dependent derivatives.',
      creators: '["SCiO members"]',
      publisher: 'SCiO — Systems and Complexity in Organisation',
      licence: 'site_and_item_terms',
      review_status: 'checked',
      last_checked: '2026-08-30',
      public_link_status: 'public_link'
    });

    addMiningRecord(data, {
      id: 'mine_scio_live_resources_2026',
      label: 'SCiO live resource library',
      url: 'https://www.systemspractice.org/resources',
      status: 'active bounded corpus',
      role: 'Treat the complete live SCiO resource library as a professional-practice source corpus, preserving its own resource types, categories, authorship and item-level reuse conditions.',
      caveat: 'Catalogue inclusion establishes that SCiO hosts or points to a resource. It does not establish truth, priority, influence or effectiveness, and some items require author permission or membership.',
      next_step: 'Ingest item-level metadata reproducibly, preserve SCiO categories, then promote only source-supported statements and relations into the canonical graph.'
    });

    addMiningRecord(data, {
      id: 'mine_scio_sysbok_live_2026',
      label: 'SCiO SysBoK live Kumu model',
      url: 'https://kumu.io/koryckaa/scio-sysbok-v1#map',
      status: 'active comparator corpus',
      role: 'Use the live SysBoK nodes, examples, references, Precedent relations and Dependent Derivative relations as an attributed comparator and source-discovery graph.',
      caveat: 'SCiO explicitly describes SysBoK as incomplete and work in progress. Preserve its relation wording and provenance; do not silently promote its graph into the canonical atlas.',
      next_step: 'Create a reproducible node-and-link import with explicit SCiO/Kumu credit, reconciliation against canonical IDs and a source-role label on every imported statement.'
    });
  }

  function patchMeadowsConnectivity(data) {
    const nodes = new Set((data.nodes || []).map((node) => node.id));
    if (!nodes.has('person_donella_meadows') || !nodes.has('concept_leverage_points')) return;
    addEdge(data, {
      id: 'e_203_meadows_leverage_points',
      source: 'person_donella_meadows',
      target: 'concept_leverage_points',
      relation_type: 'developed',
      relation_family: 'historical',
      directed: 'true',
      dependency_kind: '',
      confidence: '0.98',
      claim_status: 'accepted',
      source_ids: '["src_meadows_leverage_points"]',
      evidence_ids: '[]',
      source_locator: 'Donella Meadows Project, Leverage Points: Places to Intervene in a System',
      valid_from: '',
      valid_to: '',
      scope_conditions: 'This states authorship and development of the named leverage-points account; it does not claim Meadows originated every idea or intervention level that the essay synthesises.',
      assertion_mode: 'asserted',
      inference_method: 'primary author archive',
      claim_id: '',
      reviewed_by: 'Benjamin P Taylor',
      reviewed_at: '2026-08-30',
      notes: 'Adds a reader-visible substantive route from Meadows to the concept developed in her named essay. Her existing authorship links remain documentary provenance.',
      plain_phrase: 'developed',
      public_review_label: 'source-established'
    });
  }

  function patch(data) {
    if (!data || typeof data !== 'object') return data;
    patchScioSources(data);
    patchMeadowsConnectivity(data);
    return data;
  }

  try {
    Object.defineProperty(window, 'TANGLE_DATA', {
      configurable: true,
      enumerable: true,
      get() { return resolvedData; },
      set(value) {
        resolvedData = patch(value);
        Object.defineProperty(window, 'TANGLE_DATA', {
          configurable: true,
          enumerable: true,
          writable: false,
          value: resolvedData
        });
      }
    });
  } catch (_) {
    /* The ordinary public-data.js assignment remains the safe fallback. */
  }
})();
