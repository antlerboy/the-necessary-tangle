/* Focused behaviour checks for filters, random rules, and offline fallbacks. */
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = file => fs.readFileSync('docs/assets/' + file, 'utf8');

function filtering() {
  const handlers = {};
  const fields = {
    bibliographyFilters: { hidden: true, addEventListener: (event, fn) => { handlers[event] = fn; } },
    bibliographySearch: { value: '' }, bibliographySection: { value: '' },
    bibliographyReview: { value: '' }, bibliographyCount: { textContent: '' },
  };
  const rows = [
    { textContent: 'Ashby, Design for a Brain', dataset: { section: 'short', review: 'passages' } },
    { textContent: 'Fano, Transmission of Information', dataset: { section: 'selected', review: 'passages' } },
    { textContent: 'La pensée', dataset: { section: 'short', review: 'catalogue' } },
  ];
  vm.runInNewContext(source('early-cybernetics.js'), {
    document: { getElementById: id => fields[id], querySelectorAll: () => rows },
    setTimeout: fn => fn(),
  });
  assert.equal(fields.bibliographyFilters.hidden, false);
  assert.equal(rows.filter(r => !r.hidden).length, 3);
  fields.bibliographySearch.value = 'PENSEE'; handlers.input();
  assert.equal(rows.filter(r => !r.hidden)[0], rows[2]);
  fields.bibliographySearch.value = ''; fields.bibliographyReview.value = 'passages'; handlers.change();
  assert.equal(rows.filter(r => !r.hidden).length, 2);
  fields.bibliographySection.value = 'short'; handlers.change();
  assert.equal(rows.filter(r => !r.hidden)[0], rows[0]);
  fields.bibliographySearch.value = 'missing'; handlers.input();
  assert.ok(fields.bibliographyCount.textContent.includes('Clear a filter'));
  Object.values(fields).filter(f => 'value' in f).forEach(f => { f.value = ''; }); handlers.reset();
  assert.equal(rows.filter(r => !r.hidden).length, 3);
  let prevented = false; handlers.submit({ preventDefault: () => { prevented = true; } });
  assert.ok(prevented);
}

async function rules() {
  const rows = JSON.parse(source('redquadrant-rules.json')).rules;
  async function fixture(local, fetcher) {
    let click;
    const output = { textContent: 'Static fallback' };
    const button = { hidden: true, addEventListener: (_, fn) => { click = fn; } };
    const permalink = {};
    const host = {
      dataset: { rulesPage: 'https://transduction.systems/little-redquadrant-rules/' },
      querySelector: selector => ({ '[data-rule-text]': output, '[data-rule-next]': button, '[data-rule-link]': permalink })[selector],
      querySelectorAll: () => local ? rows.map(r => ({ dataset: { ruleNumber: r.number }, textContent: r.text })) : [],
    };
    vm.runInNewContext(source('redquadrant-rules.js'), {
      document: { readyState: 'complete', querySelectorAll: () => [host] },
      window: { crypto: { getRandomValues: array => { array[0] = 0; } } }, fetch: fetcher,
    });
    await new Promise(resolve => setImmediate(resolve));
    return { output, button, permalink, next: () => click() };
  }
  const local = await fixture(true, () => { throw new Error('Should not fetch'); });
  assert.equal(local.button.hidden, false);
  assert.ok(local.output.textContent.includes(rows[0].text));
  const previous = local.output.textContent; local.next();
  assert.notEqual(local.output.textContent, previous);
  assert.ok(local.permalink.href.endsWith('#rule-2'));
  const remote = await fixture(false, async () => ({ ok: true, json: async () => ({ rules: rows }) }));
  assert.equal(remote.button.hidden, false);
  const offline = await fixture(false, async () => { throw new Error('Offline'); });
  assert.equal(offline.button.hidden, true);
  assert.equal(offline.output.textContent, 'Static fallback');
  const malformed = await fixture(false, async () => ({ ok: true, json: async () => ({ rules: [] }) }));
  assert.equal(malformed.button.hidden, true);
}

(async () => { filtering(); await rules(); console.log('Release 0.22 interaction checks passed: combined filtering/reset, random rule/non-repeat, and failed-data fallback.'); })().catch(error => { console.error(error); process.exitCode = 1; });
