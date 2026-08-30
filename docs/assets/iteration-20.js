(() => {
  'use strict';

  function installStyles() {
    if (document.getElementById('iteration-20-styles')) return;
    const style = document.createElement('style');
    style.id = 'iteration-20-styles';
    style.textContent = `
      .site-header .brand-stack {
        display: grid;
        gap: .18rem;
        min-width: 0;
        flex: 1 1 auto;
      }
      .site-header .brand-stack > .brand {
        justify-self: start;
      }
      .site-header .brand-stack > .little-rq-rule {
        grid-column: auto;
        margin: .08rem 0 0 calc(48px + .9rem);
        width: min(72ch, calc(100% - 48px - .9rem));
      }
      @media (max-width: 820px) {
        .site-header {
          flex-wrap: wrap;
          gap: .7rem 1rem;
        }
        .site-header .brand-stack {
          flex-basis: 100%;
          order: -2;
        }
        .site-header .brand-stack > .little-rq-rule {
          margin-left: calc(48px + .9rem);
          width: calc(100% - 48px - .9rem);
        }
      }
      @media (max-width: 520px) {
        .site-header .brand-stack > .little-rq-rule {
          margin-left: 0;
          width: 100%;
        }
      }
    `;
    document.head.appendChild(style);
  }

  function placeRule() {
    const header = document.querySelector('.site-header');
    const brand = header?.querySelector(':scope > .brand, :scope > .brand-stack > .brand');
    const rule = document.getElementById('littleRqRule');
    if (!header || !brand || !rule) return false;

    let stack = header.querySelector(':scope > .brand-stack');
    if (!stack) {
      stack = document.createElement('div');
      stack.className = 'brand-stack';
      header.insertBefore(stack, brand);
      stack.appendChild(brand);
    }
    if (rule.parentElement !== stack) stack.appendChild(rule);
    return true;
  }

  function init() {
    installStyles();
    if (placeRule()) return;
    const header = document.querySelector('.site-header');
    if (!header) return;
    const observer = new MutationObserver(() => {
      if (placeRule()) observer.disconnect();
    });
    observer.observe(header, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
