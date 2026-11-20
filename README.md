# Levanta Light Theme for Standard Notes

[![License: MIT](https://img.shields.io/badge/License-MIT-6d61d1.svg)](LICENSE)
[![Standard Notes](https://img.shields.io/badge/Standard%20Notes-Theme-6366f1.svg)](https://standardnotes.com)

A light theme for [Standard Notes](https://standardnotes.com) with a lavender accent, where **the note you write is set in [Karla](https://fonts.google.com/specimen/Karla) for English and [IBM Plex Sans Arabic](https://fonts.google.com/specimen/IBM+Plex+Sans+Arabic) for Arabic**, and typed arrows like `->` and `=>` become real arrows in both languages. The rest of the app — note titles, sidebar, note list, menus — stays in [Inter](https://rsms.me/inter/).

Levanta Light is a fork of [Lavender Light](https://github.com/beshoysabri/sn-lavender-light-theme): the same mirrored white palette, stylesheet structure, GitHub Pages hosting and pre-publish checks, with a new [writing area](#the-writing-area) and [arrows](#arrows). Its night-time twin is [Levanta Dark](https://github.com/beshoysabri/sn-levanta-dark-theme). It keeps the family's version line, so the history is shared — v2.8.0 is the first Levanta release.

## Installation

1. Open the Standard Notes **desktop** app
2. Go to **Preferences** > **Plugins** > **Install Custom Plugin** (at the bottom of the page — older versions had it under **General** > **Advanced Settings**)
3. Paste the following URL:

```
https://beshoysabri.github.io/sn-levanta-light-theme/ext.json
```

4. Click **Install**
5. Select **Levanta Light** from the Appearance menu

There's a preview and a copy button at **[beshoysabri.github.io/sn-levanta-light-theme](https://beshoysabri.github.io/sn-levanta-light-theme)**.

Levanta Light has its own identifier, so it installs alongside Levanta Dark, Lavender and Lavender Light rather than replacing any of them.

**Install from the desktop app, not the web app.** The web app's Content-Security-Policy only lets it fetch plugin links from Standard Notes' own servers and `raw.githubusercontent.com`, and even that one fails, because the request is sent with credentials and GitHub answers `Access-Control-Allow-Origin: *`. Pasting the link there gives *"Error downloading package details"* — for every self-hosted theme. Installed themes sync with your account, though, and the web app loads the stylesheet and fonts from Pages without complaint, so once it's installed on the desktop it shows up on the web too.

### Pair it with Levanta Dark

Install [Levanta Dark](https://beshoysabri.github.io/sn-levanta-dark-theme) as well, then go to **Preferences** > **Appearance**, turn on **Use system color scheme**, and choose:

- **Automatic Light Theme:** Levanta Light
- **Automatic Dark Theme:** Levanta Dark

Standard Notes then switches between the two with your OS. The choice is stored per device, so set it once on each.

| Client | Colours | Inter (the app) | Karla, Plex Arabic, arrows (the editor) |
|---|---|---|---|
| Web | yes | downloaded automatically | downloaded automatically |
| iPhone, Android | yes | downloaded automatically | downloaded automatically |
| Desktop (Windows, macOS, Linux) | yes | install on the computer — see below | install on the computer — see below |

### The desktop app needs the fonts installed

The desktop app sends `Content-Security-Policy: default-src 'self' blob:` with no `font-src`, so it refuses to download **any** webfont — from this repo, from a CDN, or inlined as a `data:` URI. Its own page is a local file, so `'self'` only covers files on disk, and a theme has no path to its fonts there that works on every computer. No theme can ship a font file into it. The phone apps have no such policy and download the fonts as the web app does (checked on iPhone and Android).

What does work is a font installed on the computer. There's no download, so CSP has nothing to block — it's a name lookup, and the stacks are written so installed copies are found automatically. Without them the desktop app shows the colours on the system font, and `->` stays as typed.

**Install the font pack**, one zip with all eight files and their licenses: [`levanta-fonts.zip`](https://beshoysabri.github.io/sn-levanta-light-theme/dist/fonts/levanta-fonts.zip) (1.3 MB) — Inter, Karla, IBM Plex Sans Arabic and Levanta Arrows.

- **Windows** — extract the zip, select all the `.ttf` files, right-click → **Install for all users**. Plain **Install** puts the fonts in your user profile only, and it isn't certain the desktop app looks there; "for all users" always works. Then quit Standard Notes completely, including from the icon in the system tray, and open it again: fonts are read at launch.
- **macOS** — double-click each `.ttf` → **Install** (or drag them into Font Book), then quit Standard Notes with Cmd+Q and reopen it.
- **Linux** — copy the `.ttf` files to `~/.local/share/fonts`, run `fc-cache -f`, and restart Standard Notes.

Install the bold faces too: the theme turns off synthetic bold, so a family with only a Regular shows bold text unbolded. Each font is optional — without Karla the editor falls back to Inter, without Plex Arabic it uses the system's Arabic face, and without Levanta Arrows `->` stays as typed.

<details>
<summary>Alternative: jsDelivr</summary>

The theme is also reachable over jsDelivr:

```
https://cdn.jsdelivr.net/gh/beshoysabri/sn-levanta-light-theme@master/ext.json
```

Both origins serve the same files. GitHub Pages is the default because branch-pinned jsDelivr URLs are cached for roughly 12 hours, so a push doesn't show up until the cache expires or you purge it. Pages republishes on every push to `master`.

</details>

## The writing area

What you type in a note — the body of a Super note or a plain-text note — is set in Karla for English and IBM Plex Sans Arabic for Arabic. Note titles, the sidebar, the note list and menus stay in Inter. Section 4 of `dist/dist.css` does it.

**Arabic finds its font on its own.** Nothing has to detect it. A browser picks a font per character, walking the family stack until one has the glyph: Karla has no Arabic, so Arabic letters fall through to Plex, and a sentence that mixes the two languages gets each script in its own face. The Plex faces are also limited to the Arabic Unicode blocks with `unicode-range`, so Plex's own Latin letters never stand in for Karla's, and a note without Arabic never downloads Plex. Checked in app.standardnotes.com with Chrome's per-element font report: in a mixed Super paragraph the Arabic glyphs came from IBM Plex Sans Arabic, the Latin ones from Karla and the arrows from Levanta Arrows.

**Direction is the editor's job, and it already does it.** Super gives every paragraph `dir="auto"`, and the plain-text editor is a `dir="auto"` textarea, which browsers lay out line by line. A paragraph that starts in Arabic runs right to left and aligns right, and the next one, in English, runs left to right. No theme rule is involved.

**Why IBM Plex Sans Arabic rather than Noto Sans Arabic.** Both were set beside Karla at the editor's size, and Plex was the better match:

- Karla's curves are squarish and its terminals crisp. Plex Arabic was drawn to sit beside IBM Plex's similarly engineered Latin, and it reads as the same kind of letter. Noto Sans Arabic is rounder and softer, closer to a humanist sans.
- Size: Plex's `ه` stands 0.41 em, just under Karla's x-height of 0.48 em, so in a mixed line the two scripts look the same size. Noto's stands 0.50 em, about 20% taller, and its teeth (`س`) a third taller than Plex's, so it reads a size larger.
- Plex's Regular and Bold sit at Karla's weight, in two files of about 72 KB — all that Super uses.

**Weights and styles.** Karla is the variable font, roman and italic, 200 to 800. Plex ships Regular (400) and Bold (700), Super's body and its bold text and headings. Arabic has no italic; italic Arabic is slanted by the browser.

**Code and the Monospace option.** Code blocks and inline code keep a monospace face, with no arrows. Standard Notes' **Monospace font** option switches the editor to monospace as well — under Lavender Light's app-wide Inter it had no effect.

## Arrows

Type an arrow the way you would in plain text and it's drawn as a real one, in English and in Arabic:

| Type | Get |
|---|---|
| `->` `<-` `<->` | → ← ↔ |
| `=>` `<=>` | ⇒ ⇔ |
| `-->` `<--` `<-->` | ⟶ ⟵ ⟷ |
| `==>` `<==` `<==>` | ⟹ ⟸ ⟺ |

`<=` and `>=` are left alone; they mean "less/greater than or equal". Code never gets arrows. Only the drawing changes: the note still holds the characters you typed, so search, copy and export all see `->`.

**In an Arabic paragraph, `->` points the way the text reads: ←.** It's the same mirroring that flips `(` into `)` in right-to-left text — without the theme you'd see `<-` there, two separate characters. English inside an Arabic paragraph keeps its own direction, so `start -> end` still gives →.

**Why it needs a font of its own.** Karla has no arrow ligatures, so on its own `->` would stay two characters. Inter has them, but only for left-to-right text: in a right-to-left run the browser mirrors `>` into `<` *before* it looks up ligatures, so Inter sees `-<` and its `->` rule never matches. That's why arrows never formed in Arabic under Lavender Light. **Levanta Arrows** is a 2 KB font that holds Karla's own `-` `<` `=` `>`, Inter's arrows redrawn at Karla's stroke weight and centred on Karla's `<` and `>`, and rules for both directions. It comes first in the editor's stack with a `unicode-range` of just those characters, so it touches nothing else, and a hyphen in an ordinary word is still Karla's. `tools/build-arrows.py` rebuilds it (`pip install fonttools brotli`), byte for byte.

To keep `->` as typed in the editor, set `--levanta-text-ligatures` in section 4 to `common-ligatures no-contextual`; section 7 has a block that turns arrows off everywhere.

One rare mix gets it wrong. In an *English* paragraph, `<=` right after an Arabic word is drawn ⇐, and `=>` there stays as typed. The font can't tell that spot from `=>` typed in an Arabic paragraph, which is the commoner case, so the Arabic reading wins.

## Hosting

Pushing to `master` triggers `.github/workflows/pages.yml`, which verifies the theme before publishing — that `ext.json` and `package.json` agree on a version, that every font file exists, that every `@font-face` source is an absolute Pages URL, that all **90** colour declarations still hash to the Lavender Light palette's digest, that some rule applies `--sn-inter-font` to Standard Notes' own page and no rule reaches into editor plugins' frames, and another applies `--levanta-text-font` to the editor, that code inside the editor stays monospace, that the section 7 opt-ins are still commented out, and that braces balance in the comment-stripped `dist.css`. A failed check blocks the deploy rather than shipping a broken stylesheet.

The digest covers every custom property except the three `--sn-inter-*` and two `--levanta-*` typography knobs, so Levanta Light's colours are proven identical to Lavender Light's.

Enable it once under **Settings → Pages → Source → GitHub Actions**.

## Color Palette

| Role | Hex | Preview |
|------|-----|---------|
| Background | `#ffffff` | ![ffffff](https://img.shields.io/badge/-ffffff-ffffff?style=flat-square) |
| Sidebar & surfaces | `#f5f5f5` | ![f5f5f5](https://img.shields.io/badge/-f5f5f5-f5f5f5?style=flat-square) |
| Border | `#eeeeee` | ![eeeeee](https://img.shields.io/badge/-eeeeee-eeeeee?style=flat-square) |
| Separator | `#e0e0e0` | ![e0e0e0](https://img.shields.io/badge/-e0e0e0-e0e0e0?style=flat-square) |
| Foreground | `#2a2a2a` | ![2a2a2a](https://img.shields.io/badge/-2a2a2a-2a2a2a?style=flat-square) |
| Secondary text | `#707070` | ![707070](https://img.shields.io/badge/-707070-707070?style=flat-square) |
| Accent (Lavender) | `#6d61d1` | ![6d61d1](https://img.shields.io/badge/-6d61d1-6d61d1?style=flat-square) |
| Accent, darkened | `#5446c9` | ![5446c9](https://img.shields.io/badge/-5446c9-5446c9?style=flat-square) |
| Selection wash | `#6d61d1` at 18% | ![e5e3f7](https://img.shields.io/badge/-e5e3f7-e5e3f7?style=flat-square) |
| Text selection | `#6d61d1` at 25% | ![dad8f4](https://img.shields.io/badge/-dad8f4-dad8f4?style=flat-square) |
| Text on accent | `#ffffff` | ![ffffff](https://img.shields.io/badge/-ffffff-ffffff?style=flat-square) |
| Success | `#007662` | ![007662](https://img.shields.io/badge/-007662-007662?style=flat-square) |
| Warning | `#ebad00` | ![ebad00](https://img.shields.io/badge/-ebad00-ebad00?style=flat-square) |
| Danger | `#cc2128` | ![cc2128](https://img.shields.io/badge/-cc2128-cc2128?style=flat-square) |

The two translucent rows are previewed as they render on the background.

## Typography

Inter v4.1 sets the app: sidebar, note list, menus and note titles. The note body is Karla and IBM Plex Sans Arabic — see [The writing area](#the-writing-area). All the fonts are bundled in `dist/fonts/` under the SIL Open Font License.

Two details make the webfonts work at all:

- **The `@font-face` sources are absolute, not relative.** Standard Notes inlines theme CSS instead of linking it, so a relative `url('fonts/…')` resolves against the app's own origin and 404s. v2.2.0 shipped that bug; the fonts never loaded in any client.
- **The family is set on elements, not through a variable.** Standard Notes doesn't read `--sn-stylekit-sans-serif-font` for its own chrome, so setting that variable changes nothing. A rule on every element is what reaches the UI, and the editor rule in section 4 is more specific, so it wins inside the editor only. Since v2.8.1 both are scoped to Standard Notes' own page, `:where(body:has(> #app-group-root))`: SN also loads the theme into every editor plugin's frame, and an unscoped `body *` rule replaced the plugins' own fonts with Inter.

Code keeps a monospace face everywhere, and contextual alternates are off there so `->` stays two characters where that matters.

Five variables in `dist/dist.css` control it:

| Variable | Purpose |
|---|---|
| `--sn-inter-font` | The app's family stack. Inter has no Arabic or CJK glyphs, so those scripts fall through to the next family rather than rendering as boxes. |
| `--sn-inter-mono` | Code face. Defaults to whatever Standard Notes already uses. |
| `--sn-inter-features` | Inter's OpenType features. `cv05` gives lowercase `l` a tail so it stops looking like a capital `I`. |
| `--levanta-text-font` | The editor's stack: Levanta Arrows, Karla, Plex Arabic, then installed copies and system fallbacks. |
| `--levanta-text-ligatures` | Arrows in the editor: `common-ligatures contextual` (on) or `common-ligatures no-contextual` (off). |

Section 7 has opt-ins: tighter heading tracking, roomier leading in Super, tabular figures in Super tables, arrows off everywhere, the note title in the writing fonts, and the system font outside the editor.

## Daily View

Standard Notes' Daily notebook borrows the app's `danger` token for today's date, the days that have an entry, the entry tiles and both create-note buttons — so on a lavender theme they came out red. Section 5 of the stylesheet repaints those specific elements with the accent instead.

It's scoped deliberately rather than recolouring `--sn-stylekit-danger-color` wholesale, for two reasons: destructive controls should stay red, and the rules only *reference* the accent variables rather than declaring new ones — so the colour digest is unaffected.

One difference from Lavender: a day that has an entry sets its date in the darkened shade, because on the lavender wash `#6d61d1` is 3.9:1 and `#5446c9` is 5.4:1.

## Selection

Standard Notes uses one colour for both hover and selection, in the two places that matter: `--navigation-item-selected-background-color` in the sidebar, and `--item-cell-selected-background-color` in the note list, which the app defines as the contrast background. Under native Light those are a white bar on the grey sidebar (`#fdfdfd`) and a grey bar in the list (`#f4f5f7`).

Section 6 keeps hover a neutral grey and gives the selected sidebar item and the selected note an 18% lavender wash — the same strength as Lavender's. The selected sidebar label is in the darkened `#5446c9` (5.0:1 on the wash) rather than the accent (3.6:1). That rule sets `-webkit-text-fill-color` as well as `color`: Standard Notes paints tag titles with `-webkit-text-fill-color: var(--navigation-item-text-color)`, which wins over `color`, so a `color` alone never reaches the screen — which is why Lavender v2.6.0's lavender label still renders in its text colour. Like the Daily view rules, they only *reference* variables, so the colour digest is unaffected — and they match Standard Notes' own class names, so they may need revisiting if the app restyles its sidebar or note list.

## Colours: What Changed vs Lavender

The base, the accent's depth, and two rules — the same as in Lavender Light, which this palette is.

- **A mirrored base.** Each grey sits at the same contrast from the base as its twin, on the other side of it: background `#1e1e1e` → `#ffffff`; sidebar and surfaces `#252525` → `#f5f5f5`; borders `#2a2a2a` → `#eeeeee`; separators `#333333` → `#e0e0e0`; text `#eeeeee` → `#2a2a2a`, 14.4:1 on its base in both themes.
- **Hover a step lighter than the mirror.** Sidebar hover `#ebebeb` and note-list hover `#f2f2f2`, not the exact twins `#e8e8e8` and `#ebebeb`. A pastel wash carries less contrast than the grey it would be mirrored from, so mirrored hovers were as loud as the selection.
- **A deeper accent.** `#a79ef4` is 2.4:1 on white — fine on charcoal, too faint for links, icons and buttons on white. The accent keeps its 246° hue and deepens to `#6d61d1`, 4.9:1, level with native Light's blue (5.0:1). The darkened shade, `#5446c9`, drops HSL lightness by the same 6.9 points as in Lavender and Dark Blue.
- **White text on the accent again.** Lavender needed dark text on its pastel; `#6d61d1` takes `#ffffff` at 4.9:1 — primary buttons, the new-note button, badges, the Daily view's date tiles.
- **The same washes, from the deeper accent.** An 18% backdrop for selected rows, a 25% text-selection wash under the body text (10.3:1), a 35% scrollbar thumb.
- **Accent text on a wash uses the darkened shade** — the selected sidebar label and a Daily view day with an entry. On dark, the pastel is light enough to read on its own wash; on light, the accent isn't.
- **The selected sidebar label really is tinted.** The rule sets `-webkit-text-fill-color` too; Lavender's sets only `color`, which Standard Notes' own fill colour overrides — see [Selection](#selection).
- **Status colours are native Light's** — success `#007662`, warning `#ebad00`, danger `#cc2128` — instead of native Dark's.

As in Lavender, accessory tint 1 — the colour of the Super, plain-text and rich-text note icons, natively `#086dd6` — follows the accent, so no blue is left over. The other five tints stay native.

## Customization

Want a different lavender? Replace `6d61d1` in `dist/dist.css` with your preferred shade — without the `#`, so the translucent variants (`#6d61d12e`, `#6d61d140`, `#6d61d159`) follow it — and move `--sn-stylekit-info-color-darkened` with it.

On a light theme the accent carries text, so pick something that stays at 4.5:1 or better on white:

| Name | Hex | On white |
|------|-----|---------|
| **Lavender Light** | `#6d61d1` (default) | 4.9:1 |
| Catppuccin Latte Lavender | `#7287fd` | 3.2:1 — too light for text |
| Tailwind Violet 600 | `#7c3aed` | 5.7:1 |
| Tailwind Indigo 600 | `#4f46e5` | 6.3:1 |
| Material Deep Purple 400 | `#7e57c2` | 5.2:1 |

If you publish your own copy, the Pages workflow refuses any colour change until `EXPECTED` in `.github/workflows/pages.yml` is updated to match; the failed run prints the new digest.

## License

Theme: MIT — see `LICENSE`.
Fonts: Inter, Karla, IBM Plex Sans Arabic and Levanta Arrows are all under the SIL Open Font License 1.1 — see `LICENSE-3RD-PARTY`. The Plex files are IBM's own, unmodified; Levanta Arrows is built from Karla and Inter.
