# Reader update 0.20.4

Date: 30 August 2026

## Little RedQuadrant rule

The random Little RedQuadrant rule now belongs to the title stack. It sits directly under `The Necessary Tangle` and its subtitle, above the main navigation, rather than occupying a separate position at the end of the header row.

The existing behaviour remains: a rule is selected on load, selecting it chooses another, and `all 256` opens the complete list.

## SCiO links

The Competency Framework resource source has been rechecked against SCiO's current Professional Accreditation page. That page currently links `CF Resources` to the public Dropbox document. The older SCiO-hosted May 2024 PDF is retained as a second public route. The guessed January 2025 direct-site URL used in 0.20.3 is no longer treated as the canonical current link.

The public reader also exposes SCiO-native routes to:

- all SCiO resources;
- books, articles and newsletters;
- speakers, videos, slide decks and podcasts;
- the Competency Framework resources;
- the SCiO SysBoK project page;
- the live SysBoK Kumu project.

## SysBoK attribution and linking

The SCiO SysBoK project page and the live Kumu graph now have separate source records and separate public links.

Every existing public node, profile or connection which already cites a SCiO SysBoK source is augmented with both current links in the reader. This makes attribution and inspection local to the item rather than merely recording SysBoK as a corpus elsewhere in the atlas.

SCiO's own framing is retained: SysBoK was created by a group of SCiO members during Development Events, is incomplete and work in progress, and particularly models `Precedents` and `Dependent Derivatives`. Those semantics remain attributed source material until independently reconciled.

## Remaining data work

This pass improves current links, attribution and source reach. It does not claim a complete automated import of every live SCiO resource or every Kumu node and edge. Those remain reconciliation tasks because catalogue content changes and the Kumu project does not provide a public machine API suitable for silently treating its live graph as canonical atlas data.
