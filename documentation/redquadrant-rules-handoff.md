# RedQuadrant rules: receiving-site handoff

Requested by Benjamin P Taylor on 5 September 2026. This is part of the
Necessary Tangle 0.22 candidate. Integrate after that candidate is reviewed.

## Maintained material

- Canonical page: https://transduction.systems/little-redquadrant-rules/
- Exact 256-rule source: `sources/redquadrant-rules.json`.
- Deployable local copy: `docs/assets/redquadrant-rules.json`.
- Portable progressive enhancement: `docs/assets/redquadrant-rules.js`.
- Stable individual destinations: `/little-redquadrant-rules/#rule-1` through
  `#rule-256` on transduction.systems.

The full list is present in the HTML without JavaScript. Its text is checked
against the supplied list from the Tangle changes thread. The earlier header
implementation remains in `site-enhancements.js` for traceability, with its
initialisation removed. The maintained component reads local data, selects a
rule on load and on button activation, avoids immediate repetition, and
retains its static fallback if data cannot be read. It uses no storage.

## RedQuadrant

Queue: https://github.com/antlerboy/redquadrant/issues/1

Add a compact practice strip immediately above the footer returned by
`app/_components/SiteChrome.tsx`. Connect it to the existing `FooterShed` in
`app/_components/EasterEggsLive.tsx`, using the site's current Tool Shed route.
Retain modest visual weight: one short rule, a small 'Another rule' button,
and 'All 256 rules' and 'Tool Shed' links. Match the existing site typography
and spacing. Do not turn the strip into a large promotional card.

For the React implementation, import a local copy of the JSON and use local
component state. Choose the random item after mounting to avoid hydration
mismatch; the initial server-rendered rule remains readable. Preserve the
button's focus and announce only the changed rule with `aria-live="polite"`.
No iframe or client request to a GitHub issue is needed.

This supplies the implementation material for the existing 5 September request
in the queue. Its separate 'our story' and welcome-pack work remains with the
RedQuadrant update packet.

## antlerboy.com

Queue: https://github.com/antlerboy/aboutme/issues/1

Place a small 'A question for practice' aside after 'Thinking and writing' and
the library callout, before 'Groups'. This connects the rules with Benjamin's
public practice and writing without crowding the introductory biography.
Use one rule plus 'Another rule', 'All 256 rules', and 'RedQuadrant Tool Shed'.
The existing Tangle work card can use the canonical transduction.systems link
and offer the new `/systems-thinking/` entrance to first-time readers.

Copy the JSON and script into the static site's own asset directory. The
following markup works with the portable component; supply the actual local
asset path through `data-rules-source`. Style it with the receiving site's own
CSS, keeping the text readable and the button easy to focus and activate.

```html
<aside class="rq-rule" aria-label="A question for practice"
  data-rq-rules data-rules-source="/assets/redquadrant-rules.json"
  data-rules-page="https://transduction.systems/little-redquadrant-rules/">
  <p data-rule-text aria-live="polite">Little RedQuadrant rule #1:
    Start with purpose. A project plan without purpose is decorative administration.</p>
  <button type="button" data-rule-next hidden>Another rule</button>
  <a data-rule-link href="https://transduction.systems/little-redquadrant-rules/#rule-1">This rule</a>
  <a href="https://transduction.systems/little-redquadrant-rules/">All 256 rules</a>
  <a href="https://chosen-path.org/2020/08/28/an-invitation-to-the-redquadrant-tool-shed/">RedQuadrant Tool Shed</a>
</aside>
<script src="/assets/redquadrant-rules.js" defer></script>
```

## Gateway and domain handoff

The accessible educational entrance envisaged in the 3 September publications
and web-system plan is built at `/systems-thinking/` on transduction.systems.
Use this as the destination for systemsthinking.info. Redirect the root over
HTTPS, preserve query strings, and decide deliberately what to do with any
existing paths; do not silently break established links. The canonical tag
on the destination already points to transduction.systems. The redirect has
not been configured in this packet. Check the destination after publication
before changing domain routing.

## Receiving-site acceptance

- The selected placement has the site's own visual treatment.
- The static rule and all-rules link work when JavaScript or data loading fails.
- Keyboard activation changes the rule without moving focus.
- No immediate repeat; all 256 source texts remain available.
- Narrow screens do not overflow; focus and text have sufficient contrast.
- Tool Shed and canonical individual-rule links resolve after publication.
