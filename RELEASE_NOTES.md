feat: Levanta Light — Lavender Light, written in Karla and IBM Plex Sans Arabic

Levanta Light is Lavender Light v2.7.0 with the writing area of Levanta
Dark. Colours, structure, hosting and pre-publish checks are Lavender
Light's: the 90 colour declarations still hash to Lavender Light's
digest. It has its own identifier, com.beshoysabri.levanta-light-theme,
so it installs alongside Levanta Dark, Lavender and Lavender Light, and
pairs with Levanta Dark under Use system color scheme.

The note body, Super and plain text alike, is set in Karla (v2.004, the
variable font, roman and italic) for English and IBM Plex Sans Arabic
(IBM's own woff2, Regular and Bold) for Arabic. Note titles, the
sidebar, the note list and menus stay in Inter. A new section 4 holds
it; the Daily view, selection and optional sections move down one.

Arabic needs no detection. The browser picks a font per character and
Karla has no Arabic, so Arabic falls through to Plex. Plex's faces carry
a unicode-range of the Arabic blocks, so Plex's Latin never replaces
Karla's and a note without Arabic never downloads Plex. Direction already
works: Super gives each paragraph dir="auto" (Lexical 0.49), and the
plain-text editor is a dir="auto" textarea, laid out line by line.

Plex rather than Noto Sans Arabic: its squarish, crisp shapes match
Karla's; its heh stands 0.41 em against Karla's 0.48 em x-height, where
Noto's stands 0.50 em and reads a size larger; and its Regular and Bold
sit at Karla's weight.

Typed arrows become real ones in English and Arabic: -> <- <-> => <=>
--> <-- <--> ==> <== <==> ---> <---. Karla has no arrow ligatures, and
Inter's never formed in Arabic, because a right-to-left run mirrors > to
< before ligatures are looked up. Levanta Arrows, built by the new
tools/build-arrows.py, holds Karla's - < = >, Inter's arrows redrawn at
Karla's stroke weight and centred on Karla's < >, and calt rules for
DFLT and latn plus the mirrored order for arab and hebr. It sits first
in the editor's stack with a unicode-range of just those characters. In
an Arabic paragraph -> draws ←, the way the text reads. <= and >= are
left alone, and code gets no arrows. The build is byte-for-byte
reproducible, and identical to Levanta Dark's.

The editor rule also honours Standard Notes' Monospace font option,
which Lavender Light's app-wide Inter overrides, keeps code monospace
inside the editor, and drops Inter's cv05 there. --levanta-text-font and
--levanta-text-ligatures are its knobs; the digest leaves them out, as
it does --sn-inter-*.

Section 7, the opt-ins: the arrows-off block also takes calt out of
--sn-inter-features, because font-feature-settings outranks
font-variant-ligatures (Lavender Light's block leaves Inter's arrows
fused); the tabular-figures block reaches the table cells' text; a new
block sets the note title in the writing fonts; and "confine Inter to
the editor" becomes "system font outside the editor".

Desktop and mobile need the fonts installed on the device, as Inter
always has; the README lists them, and LevantaArrows-*.ttf are served
from Pages.

Checked in app.standardnotes.com before release, in Super (the upgrade
dialog's live editor), with Chrome's per-node platform-font report:
Arabic from IBM Plex Sans Arabic, Latin from Karla, arrows from Levanta
Arrows in both directions, code in the monospace face, and the rest of
the app in Inter.

Released as 2.8.0.
