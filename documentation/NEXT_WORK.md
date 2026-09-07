# Next work

## Automatic living-mark repair, 7 September 2026

Authorised by Benjamin's report that the marks do not play and his explicit instruction that no playback controls are needed when play is automatic. Repair playback only. Do not add a play, pause or resume button. Preserve the alpha practice pack, graph content, original marks, source-owner-reviewed assets, feedback dot and events service.

The old implementation depended on H.264 media support and video autoplay permission. It also hid the video in reduced-motion mode. Passing one randomly selected video in Chrome did not establish reliable playback for every mark or the reader's browser.

Use animated-image derivatives of the existing 44 moving marks so animation no longer depends on video playback. Preserve originals and remove obsolete control markup and state. Respect the operating-system reduced-motion preference by default. An explicit ?motion=on URL can enable animation without any player controls. Cache-version the changed scripts.

Acceptance: make validate; all existing practice browser checks; visible pixel changes for all 44 animated marks while video playback is deliberately rejected; no playback controls; default automatic motion on cold load, reload and mobile; reduced-motion preference; deployed commit and live checks. Stop after acceptance or report the exact failed check.

Previous unrelated feedback, research and Greebling publication dependencies remain open. This repair does not close them.
