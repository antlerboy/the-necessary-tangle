(() => {
  'use strict';

  function installStyles() {
    if (document.getElementById('iteration-20-styles')) return;
    const style = document.createElement('style');
    style.id = 'iteration-20-styles';
    style.textContent = `
      .site-header {
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto;
        grid-template-rows: auto auto;
        gap: .28rem 1.7rem;
        align-items: start;
        padding-top: .85rem;
        padding-bottom: .7rem;
      }
      .site-header .brand-stack {
        grid-column: 1;
        grid-row: 1 / span 2;
        display: grid;
        gap: .18rem;
        min-width: 0;
      }
      .site-header .brand-stack > .brand {
        justify-self: start;
        align-items: flex-start;
        gap: .85rem;
      }
      .site-header .brand-mark:not(:fullscreen) {
        width: 64px !important;
        height: 64px !important;
        flex-basis: 64px !important;
        overflow: hidden;
        border-radius: 12px;
      }
      .site-header .brand-mark:not(:fullscreen) > img,
      .site-header .brand-mark:not(:fullscreen) > video,
      .site-header .brand-mark:not(:fullscreen) > svg {
        display: block;
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
      .site-header .brand strong {
        font-size: clamp(2rem, 3.2vw, 3.15rem);
        line-height: .94;
      }
      .site-header .brand small {
        margin-top: .28rem;
        font-size: .78rem;
        line-height: 1.25;
      }
      .site-header .brand-stack > .little-rq-rule {
        grid-column: auto;
        margin: .18rem 0 0 calc(64px + .85rem) !important;
        width: min(82ch, calc(100% - 64px - .85rem)) !important;
        gap: .45rem;
        font-size: .72rem;
        line-height: 1.3;
        opacity: .88;
      }
      .site-header .brand-stack > .little-rq-rule .rule-all {
        font-size: .69rem;
        opacity: .72;
      }
      .site-header > .header-meta {
        grid-column: 2;
        grid-row: 1;
        display: grid;
        justify-items: end;
        gap: .18rem;
        margin-top: .12rem;
        font-size: .71rem;
        line-height: 1.2;
        white-space: nowrap;
      }
      .site-header > .header-meta span:first-child {
        border: 0;
        border-radius: 0;
        padding: 0;
        background: transparent;
        color: var(--accent);
        font-weight: 700;
      }
      .site-header > .theme-toggle {
        grid-column: 2;
        grid-row: 2;
        justify-self: end;
        align-self: start;
        margin-top: .2rem;
      }
      .main-nav {
        padding-top: .26rem;
        padding-bottom: .26rem;
      }
      .main-nav a {
        padding: .48rem .68rem;
        font-size: .92rem;
      }
      @media (max-width: 820px) {
        .site-header {
          gap: .5rem 1rem;
        }
        .site-header .brand-stack {
          grid-column: 1 / -1;
          grid-row: 1;
        }
        .site-header > .header-meta {
          grid-column: 1;
          grid-row: 2;
          justify-items: start;
          grid-auto-flow: column;
          justify-content: start;
          gap: .65rem;
          white-space: normal;
        }
        .site-header > .theme-toggle {
          grid-column: 2;
          grid-row: 2;
          margin-top: 0;
        }
      }
      @media (max-width: 520px) {
        .site-header .brand-mark:not(:fullscreen) {
          width: 52px !important;
          height: 52px !important;
          flex-basis: 52px !important;
          border-radius: 9px;
        }
        .site-header .brand strong {
          font-size: clamp(1.75rem, 10vw, 2.35rem);
        }
        .site-header .brand-stack > .little-rq-rule {
          margin-left: 0 !important;
          width: 100% !important;
        }
        .site-header > .header-meta {
          grid-auto-flow: row;
          gap: .12rem;
        }
        .main-nav a {
          padding: .44rem .58rem;
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
