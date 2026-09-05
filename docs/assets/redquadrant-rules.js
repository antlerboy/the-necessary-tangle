/* Reusable rules reader. Supply a local copy of the maintained JSON; no third-party requests or storage. */
(() => {
  'use strict';
  async function mount(host) {
    const output = host.querySelector('[data-rule-text]');
    const button = host.querySelector('[data-rule-next]');
    if (!output || !button) return;
    let rows = Array.from(host.querySelectorAll('[data-rule-number]'), (li) => ({ number: Number(li.dataset.ruleNumber), text: li.textContent }));
    if (!rows.length) {
      try {
        const response = await fetch(host.dataset.rulesSource || '/assets/redquadrant-rules.json');
        if (!response.ok) throw new Error('Rules unavailable');
        rows = (await response.json()).rules;
      } catch (_) { button.hidden = true; return; }
    }
    if (!Array.isArray(rows) || rows.length !== 256 || rows.some(r => !Number.isInteger(r.number) || typeof r.text !== 'string')) { button.hidden = true; return; }
    let current = null;
    function show() {
      const pool = rows.filter(r => r.number !== current);
      const random = new Uint32Array(1);
      const index = window.crypto?.getRandomValues ? (window.crypto.getRandomValues(random), random[0] % pool.length) : Math.floor(Math.random() * pool.length);
      const rule = pool[index];
      current = rule.number;
      output.textContent = `Little RedQuadrant rule #${rule.number}: ${rule.text}`;
      const permalink = host.querySelector('[data-rule-link]');
      if (permalink) permalink.href = (host.dataset.rulesPage || '/little-redquadrant-rules/') + '#rule-' + rule.number;
    }
    button.hidden = false;
    button.addEventListener('click', show);
    show();
  }
  function init() { document.querySelectorAll('[data-rq-rules]').forEach(mount); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once:true }); else init();
})();
