# Living-mark repair, 7 September 2026

The user's report of non-playing marks reopens the playback check. The previous tests demonstrated one native video playing in Chrome, not reliable playback of every mark in the reader's browser.

The replacement derives animated WebP images from the existing videos, without changing the originals. This removes dependence on H.264 decoding and video autoplay permission. A still image remains the reduced-motion default, but the compact play control is never hidden merely because that preference is active. Explicit motion choice is kept for the browser session; ?motion=on is a direct opt-in route.

The publication test compares successive screenshots of each of the 44 marks, with HTMLMediaElement.play deliberately rejected. It also checks pause, resume, reduced-motion default, explicit override and reload. The same test runs before publication and against the deployed site. The results, not this note, determine whether publication has been verified.
