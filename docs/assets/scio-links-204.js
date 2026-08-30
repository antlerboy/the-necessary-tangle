(() => {
  'use strict';

  const CF_DROPBOX = 'https://www.dropbox.com/scl/fi/v5vl9o1e9gtwxbqiyb2no/SCiO-CF-Resources.pdf?dl=0&rlkey=a9d5ckhbsdjld7ab3sp60jaj9';
  const CF_SCIO_PDF = 'https://www.systemspractice.org/system/files/2024-05/CF%20resources%20colour.pdf';
  const RESOURCES = 'https://www.systemspractice.org/resources';
  const SYSBOK_SCIO = 'https://www.systemspractice.org/sysbok-from-scio';
  const SYSBOK_KUMU = 'https://kumu.io/koryckaa/scio-sysbok-v1';
  const BOOKS_ARTICLES = 'https://www.systemspractice.org/resources/books-articles-newsletters?author=All&category=All&field_author_is_a_member_value=All&field_has_attachments_value=All&field_organiser__target_id=All&language=All&resource_type%5B0%5D=10&resource_type%5B1%5D=1&resource_type%5B2%5D=11&sort_by=field_publication_date_value&sort_order=DESC&title=';
  const MEDIA = 'https://www.systemspractice.org/resources/speakers-videos-slidedecks-podcasts?field_has_attachments_value=1&resource_type%5B0%5D=14&sort_by=field_publication_date_value&sort_order=DESC';

  function parseList(value) {
    if (Array.isArray(value)) return value.slice();
    if (!value) return [];
    try {
      const parsed = JSON.parse(value);
      return Array.isArray(parsed) ? parsed : [];
    } catch (_) {
      return [];
    }
  }

  function writeList(record, key, values) {
    record[key] = JSON.stringify([...new Set(values.filter(Boolean))]);
  }

  function upsertSource(data, source) {
    const sources = data.sources || (data.sources = []);
    const existing = sources.find((item) => item.id === source.id);
    if (existing) Object.assign(existing, source);
    else sources.push(source);
  }

  function upsertMiningRecord(data, record) {
    const records = data.source_mining_register || (data.source_mining_register = []);
    const existing = records.find((item) => item.id === record.id);
    if (existing) Object.assign(existing, record);
    else records.push(record);
  }

  function patch(data) {
    if (!data || typeof data !== 'object') return data;
    const sources = data.sources || (data.sources = []);

    const legacySysbokIds = new Set(
      sources
        .filter((source) => /^SCiO SysBoK\b/i.test(source.title || ''))
        .map((source) => source.id)
        .filter(Boolean)
    );

    sources.forEach((source) => {
      if (source.id === 'src_scio_cf_resources_2022' || /^SCiO CF Resources\b/i.test(source.title || '')) {
        Object.assign(source, {
          title: 'SCiO Competency Framework resources — current public guide',
          url: CF_DROPBOX,
          archived_url: CF_SCIO_PDF,
          date: 'current public link; checked 2026-08-30',
          access: 'public',
          publisher: 'SCiO — Systems and Complexity in Organisation',
          public_link_status: 'public_link',
          review_status: 'checked',
          last_checked: '2026-08-30',
          notes: 'SCiO’s current Professional Accreditation page links directly to this Dropbox CF Resources guide. The older official SCiO-hosted PDF is retained as a second public route. Use the guide as evidence of SCiO’s competency/resource framing, not as independent proof of the referenced methods or claims.'
        });
      }
      if (legacySysbokIds.has(source.id)) {
        Object.assign(source, {
          url: SYSBOK_KUMU,
          publisher: 'SCiO — Systems and Complexity in Organisation',
          access: 'public',
          public_link_status: 'public_link',
          review_status: 'checked',
          last_checked: '2026-08-30',
          notes: 'SCiO SysBoK source record. The current SCiO page credits a group of SCiO members, describes SysBoK as incomplete and work in progress, and links to this live Kumu project. Keep the original SysBoK relationship semantics and attribution when using this material.'
        });
      }
    });

    upsertSource(data, {
      id: 'src_scio_cf_resources_current_2026',
      title: 'SCiO Competency Framework resources — current SCiO-linked copy',
      source_type: 'official_professional_body_competency_resource_guide',
      quality_tier: 'A',
      access: 'public',
      url: CF_DROPBOX,
      archived_url: CF_SCIO_PDF,
      date: 'current public link; checked 2026-08-30',
      notes: 'The SCiO Professional Accreditation page currently links this Dropbox copy as “CF Resources”. The SCiO-hosted May 2024 PDF remains a working public fallback.',
      creators: '["SCiO — Systems and Complexity in Organisation"]',
      publisher: 'SCiO — Systems and Complexity in Organisation',
      licence: 'source_terms',
      review_status: 'checked',
      last_checked: '2026-08-30',
      public_link_status: 'public_link'
    });

    upsertSource(data, {
      id: 'src_scio_resource_library_live_2026',
      title: 'SCiO resource library — all resources',
      source_type: 'official_professional_body_resource_corpus',
      quality_tier: 'A',
      access: 'public_catalogue_mixed_item_rights',
      url: RESOURCES,
      date: 'current; checked 2026-08-30',
      notes: 'SCiO’s live resource catalogue. The site exposes title, resource type, language, category, author, organiser, membership, attachment and ordering filters. Preserve those categories and each item’s reuse label rather than flattening the catalogue.',
      creators: '["SCiO — Systems and Complexity in Organisation"]',
      publisher: 'SCiO — Systems and Complexity in Organisation',
      licence: 'mixed_item_level_rights',
      review_status: 'checked',
      last_checked: '2026-08-30',
      public_link_status: 'public_link'
    });

    upsertSource(data, {
      id: 'src_scio_resource_library_books_current',
      title: 'SCiO resources — books, articles and newsletters',
      source_type: 'official_professional_body_resource_category',
      quality_tier: 'A',
      access: 'public_catalogue_mixed_item_rights',
      url: BOOKS_ARTICLES,
      date: 'current; checked 2026-08-30',
      notes: 'SCiO’s own current resource-navigation route for books, articles and newsletters.',
      creators: '["SCiO — Systems and Complexity in Organisation"]',
      publisher: 'SCiO — Systems and Complexity in Organisation',
      licence: 'mixed_item_level_rights',
      review_status: 'checked',
      last_checked: '2026-08-30',
      public_link_status: 'public_link'
    });

    upsertSource(data, {
      id: 'src_scio_resource_library_media_current',
      title: 'SCiO resources — speakers, videos, slide decks and podcasts',
      source_type: 'official_professional_body_resource_category',
      quality_tier: 'A',
      access: 'public_catalogue_mixed_item_rights',
      url: MEDIA,
      date: 'current; checked 2026-08-30',
      notes: 'SCiO’s own current resource-navigation route for speaker material, video, slide decks and podcasts.',
      creators: '["SCiO — Systems and Complexity in Organisation"]',
      publisher: 'SCiO — Systems and Complexity in Organisation',
      licence: 'mixed_item_level_rights',
      review_status: 'checked',
      last_checked: '2026-08-30',
      public_link_status: 'public_link'
    });

    upsertSource(data, {
      id: 'src_scio_sysbok_landing_2026',
      title: 'SysBoK, from SCiO — project page',
      source_type: 'official_professional_body_project_page',
      quality_tier: 'A',
      access: 'public',
      url: SYSBOK_SCIO,
      date: 'current; checked 2026-08-30',
      notes: 'SCiO’s project page credits a group of SCiO members, states that SysBoK is incomplete and work in progress, and explains its emphasis on Precedents and Dependent Derivatives.',
      creators: '["SCiO members"]',
      publisher: 'SCiO — Systems and Complexity in Organisation',
      licence: 'site_terms',
      review_status: 'checked',
      last_checked: '2026-08-30',
      public_link_status: 'public_link'
    });

    upsertSource(data, {
      id: 'src_scio_sysbok_live_2026',
      title: 'SCiO SysBoK — live Kumu project',
      source_type: 'official_professional_body_connected_concept_model',
      quality_tier: 'A',
      access: 'public',
      url: SYSBOK_KUMU,
      date: 'current; checked 2026-08-30',
      notes: 'The live Kumu project linked by SCiO. Treat its nodes and relations as an explicitly attributed SCiO comparator/source graph. Preserve its Precedent and Dependent Derivative semantics until independently reconciled.',
      creators: '["SCiO members"]',
      publisher: 'SCiO — Systems and Complexity in Organisation',
      licence: 'source_terms',
      review_status: 'checked',
      last_checked: '2026-08-30',
      public_link_status: 'public_link'
    });

    const sysbokLinkIds = ['src_scio_sysbok_landing_2026', 'src_scio_sysbok_live_2026'];
    const attachLiveSysbokLinks = (record) => {
      const ids = parseList(record.source_ids);
      if (!ids.some((id) => legacySysbokIds.has(id))) return;
      writeList(record, 'source_ids', [...ids, ...sysbokLinkIds]);
    };
    (data.nodes || []).forEach(attachLiveSysbokLinks);
    (data.edges || []).forEach(attachLiveSysbokLinks);
    (data.profiles || []).forEach(attachLiveSysbokLinks);

    upsertMiningRecord(data, {
      id: 'mine_scio_live_resources_2026',
      label: 'SCiO live resources, preserving catalogue categories',
      url: RESOURCES,
      status: 'active bounded corpus',
      role: 'Use SCiO’s complete live resource catalogue as a professional-practice corpus, preserving title, resource type, language, category, author, organiser, attachment metadata and item-level reuse conditions.',
      caveat: 'Catalogue presence establishes that SCiO hosts or points to a resource. It does not establish truth, priority, influence or effectiveness. “Use with Accreditation”, “Contact the Author” and “Confidential – Members Only” must remain distinct.',
      next_step: 'Continue item-level reconciliation against existing people, works, methods and sources; do not manufacture duplicates or republish protected attachments.'
    });

    upsertMiningRecord(data, {
      id: 'mine_scio_sysbok_live_2026',
      label: 'SCiO SysBoK live Kumu graph',
      url: SYSBOK_KUMU,
      status: 'active attributed comparator corpus',
      role: 'Use the live Kumu nodes, examples, references, Precedent relations and Dependent Derivative relations as an attributed SCiO source-discovery and comparison graph.',
      caveat: 'SCiO explicitly describes SysBoK as incomplete and work in progress. Preserve attribution, relationship wording and provenance; do not silently turn its graph into canonical atlas truth.',
      next_step: 'Reconcile Kumu nodes and links against canonical IDs and retain direct SCiO/Kumu source links on every carried-over statement.'
    });

    data.meta = data.meta || {};
    data.meta.scio_public_links = {
      checked: '2026-08-30',
      competency_resources: CF_DROPBOX,
      competency_resources_scio_pdf: CF_SCIO_PDF,
      resource_library: RESOURCES,
      resource_books_articles_newsletters: BOOKS_ARTICLES,
      resource_speakers_video_slides_podcasts: MEDIA,
      sysbok_scio: SYSBOK_SCIO,
      sysbok_kumu: SYSBOK_KUMU
    };

    return data;
  }

  const previous = Object.getOwnPropertyDescriptor(window, 'TANGLE_DATA');
  try {
    Object.defineProperty(window, 'TANGLE_DATA', {
      configurable: true,
      enumerable: true,
      get() {
        return previous?.get ? previous.get.call(window) : undefined;
      },
      set(value) {
        if (previous?.set) {
          previous.set.call(window, value);
          patch(window.TANGLE_DATA);
          return;
        }
        Object.defineProperty(window, 'TANGLE_DATA', {
          configurable: true,
          enumerable: true,
          writable: true,
          value: patch(value)
        });
      }
    });
  } catch (_) {
    if (window.TANGLE_DATA) patch(window.TANGLE_DATA);
  }
})();
