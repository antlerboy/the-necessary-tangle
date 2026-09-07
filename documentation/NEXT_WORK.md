# Next work

## Living-mark playback repair, 7 September 2026

Authorised by Benjamin's report that none of the marks play and his request to make them work again. Repair playback only. Preserve the alpha practice pack, graph content, source-owner-reviewed assets, feedback dot and events service.

Confirmed defects in the previous implementation: playback depended on H.264 media support, and reduced-motion mode removed the video and hid the only play control. A passing test of one randomly chosen video in Chrome did not cover all marks or the reader's experience.

Use animated-image derivatives of the existing 44 moving marks so playback no longer depends on video codecs or video autoplay permission. Preserve all originals. Keep a compact, accessible pause/resume control, a still default for reduced-motion preferences, and an explicit working play override. Cache-version the changed scripts.

Acceptance: make validate; all original practice browser checks; visible pixel changes for all 44 animated marks with video playback deliberately rejected; stable pause and working resume; reduced-motion default and explicit opt-in; cold load, reload, desktop/mobile; deployed commit and live checks. Stop after acceptance or report the exact failed check.

Previous unrelated feedback, research, and Greebling publication dependencies remain open. This repair does not close them.
