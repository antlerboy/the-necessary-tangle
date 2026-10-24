(() => {
  'use strict';
  const form = document.getElementById('quickContributionForm');
  if (!form) return;
  const status = document.getElementById('quickContributionStatus');
  const button = form.querySelector('button[type="submit"]');
  let sending = false;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (sending || !form.reportValidity()) return;
    sending = true; button.disabled = true; status.textContent = 'Sending…';
    const input = new FormData(form);
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    try {
      const response = await fetch('https://events.transduction.systems/api/contributions', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text: input.get('text'), email: input.get('email'), website: input.get('website')}),
        signal: controller.signal, credentials: 'omit',
      });
      const receipt = await response.json();
      if (!response.ok || !receipt.received || !receipt.id) throw Error(receipt.error || 'Your contribution could not be saved. Please try again.');
      form.reset();
      status.textContent = (receipt.duplicate ? 'This contribution is already in the inbox.' : 'Contribution received for Benjamin to review. Thank you.') + ' Receipt: ' + receipt.id;
    } catch (error) {
      status.textContent = error.name === 'AbortError' ? 'The request timed out. Your text is still here. Try again; a duplicate won’t be added.' : (error.message || 'The request failed. Your text is still here. Please try again.');
    } finally {
      clearTimeout(timeout); sending = false; button.disabled = false;
    }
  });
})();
