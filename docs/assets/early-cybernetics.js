(() => {
  'use strict';
  const form = document.getElementById('bibliographyFilters');
  if (!form) return;
  const query = document.getElementById('bibliographySearch');
  const section = document.getElementById('bibliographySection');
  const review = document.getElementById('bibliographyReview');
  const count = document.getElementById('bibliographyCount');
  const rows = Array.from(document.querySelectorAll('[data-bibliography-entry]'));
  const normalise = s => s.normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  function apply() {
    const words = normalise(query.value.trim()).split(/\s+/).filter(Boolean);
    let shown = 0;
    rows.forEach(row => {
      const haystack = normalise(row.textContent);
      const match = words.every(word => haystack.includes(word)) && (!section.value || row.dataset.section === section.value) && (!review.value || row.dataset.review === review.value);
      row.hidden = !match;
      if (match) shown++;
    });
    count.textContent = `${shown} of ${rows.length} source entries shown${shown === 0 ? '. Clear a filter or try another word.' : '.'}`;
  }
  form.addEventListener('submit', e => { e.preventDefault(); apply(); });
  form.addEventListener('input', apply);
  form.addEventListener('change', apply);
  form.addEventListener('reset', () => setTimeout(apply,0));
  form.hidden = false;
  apply();
})();
