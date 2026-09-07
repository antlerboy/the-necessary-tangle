# Automatic living-mark repair, 7 September 2026

The user's report of non-playing marks reopens the playback check. Their subsequent instruction is explicit: automatic animation without playback controls. The previous tests demonstrated one native video playing in Chrome, not reliable playback of every mark in the reader's browser.

The replacement derives animated WebP images from the existing videos, without changing the originals. This removes dependence on H.264 decoding and video autoplay permission. No play, pause or resume controls are created. Old player-button pause state is ignored. A still image remains the operating-system reduced-motion default; ?motion=on provides an explicit URL-level opt-in.

The publication test compares successive screenshots of each of the 44 marks with HTMLMediaElement.play deliberately rejected. It checks cold load, reload, mobile layout, absence of player controls and the reduced-motion preference. The same tests run before publication and against the deployed site. The results, not this note, determine whether publication has been verified.
