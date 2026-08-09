(() => {
  "use strict";

  const interactiveSelector = "a, button, input, select, textarea, summary, [role='button']";
  const actionSelector = ".open-card, .open-journey, [data-view-link], a[href]";

  function markClickableCards(root = document) {
    root.querySelectorAll?.(".card").forEach((card) => {
      if (card.querySelector(actionSelector)) card.classList.add("is-clickable");
    });
  }

  document.addEventListener("click", (event) => {
    if (event.target.closest(interactiveSelector)) return;
    const card = event.target.closest(".card.is-clickable");
    if (!card) return;
    const action = card.querySelector(actionSelector);
    if (action) action.click();
  });

  const observer = new MutationObserver((records) => {
    for (const record of records) {
      for (const node of record.addedNodes) {
        if (!(node instanceof Element)) continue;
        if (node.matches(".card")) markClickableCards(node.parentElement || document);
        else markClickableCards(node);
      }
    }
  });

  function init() {
    markClickableCards();
    observer.observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
