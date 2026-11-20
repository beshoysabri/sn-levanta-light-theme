#!/usr/bin/env python3
"""
Build Levanta Arrows — the small font that turns typed arrows (->, <-, =>,
<->, -->, …) into real arrows in the note editor, in left-to-right AND
right-to-left (Arabic, Hebrew) paragraphs.

Why it exists
-------------
Karla, the editor's Latin face, has no arrow ligatures, so on its own `->`
stays two characters. Inter has them, but only for left-to-right text: in a
right-to-left run the shaper mirrors `>` into `<` before ligatures are looked
up, so Inter sees `hyphen less` and never matches its `hyphen greater` rule.

Levanta Arrows carries:
  - Karla's own `-  <  =  >`, so ordinary hyphens and comparisons look exactly
    like the rest of the Karla text;
  - Inter's arrow glyphs, redrawn at Karla's stroke weight and centred on
    Karla's `<` and `>`;
  - a `calt` feature with Inter's left-to-right arrow rules (DFLT, latn) and
    the mirrored rules for right-to-left scripts (arab, hebr).

The theme puts it first in the editor's font stack with a unicode-range that
covers only those characters, so it never touches letters.

Usage:  python3 tools/build-arrows.py
Needs:  pip install fonttools brotli
Reads:  dist/fonts/Karla.woff2, dist/fonts/InterVariable.woff2
Writes: dist/fonts/LevantaArrows-{Regular,Bold}.{woff2,ttf}

Both sources are SIL OFL 1.1 with no Reserved Font Name, and so is the result.
"""

import argparse
import copy
import os
from pathlib import Path

from fontTools import subset
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.misc.timeTools import timestampSinceEpoch
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / 'dist' / 'fonts'

VERSION = '1.000'
# A fixed build date keeps rebuilds byte-identical (override with SOURCE_DATE_EPOCH).
BUILD_DATE = int(os.environ.get('SOURCE_DATE_EPOCH', 1795132800))  # 2026-11-20

# Inter glyph name -> the code point it is mapped to in Inter.
ARROWS = {
    'arrowleft': 0x2190, 'arrowright': 0x2192, 'arrowboth': 0x2194,
    'arrowdblleft': 0x21D0, 'arrowdblright': 0x21D2, 'arrowdblboth': 0x21D4,
    'uni27F5': 0x27F5, 'uni27F6': 0x27F6, 'uni27F7': 0x27F7,
    'uni27F8': 0x27F8, 'uni27F9': 0x27F9, 'uni27FA': 0x27FA,
    'leftLongArrow2': 0x1F850, 'rightLongArrow2': 0x1F852,
}
KARLA = {0x2D: 'hyphen', 0x3C: 'less', 0x3D: 'equal', 0x3E: 'greater'}

# Inter's arrows are ~20% heavier than Karla at the same nominal weight, so
# each style takes them from the Inter instance whose shaft, after scaling,
# is as thick as Karla's hyphen at that style's weight (0.068 em at 400,
# 0.103 em at 700). At 0.9 the arrows are about 8% taller than Karla's < >,
# the same proportion Inter keeps between its own arrows and < >.
SCALE = 0.9
STYLES = {
    'Regular': {'karla_wght': 400, 'inter_wght': 372},
    'Bold': {'karla_wght': 700, 'inter_wght': 681},
}

# Left-to-right rules: Inter's own set. `<=` and `>=` are left alone on
# purpose — they mean "less/greater than or equal", not an arrow.
LTR_RULES = '''
  sub less equal equal greater by uni27FA;
  sub less hyphen hyphen greater by uni27F7;
  sub hyphen hyphen hyphen greater by rightLongArrow2;
  sub less hyphen hyphen hyphen by leftLongArrow2;
  sub less equal greater by arrowdblboth;
  sub less hyphen greater by arrowboth;
  sub equal equal greater by uni27F9;
  sub less equal equal by uni27F8;
  sub hyphen hyphen greater by uni27F6;
  sub less hyphen hyphen by uni27F5;
  sub hyphen greater by arrowright;
  sub less hyphen by arrowleft;
  sub equal greater by arrowdblright;
'''

# Right-to-left rules. In an Arabic or Hebrew run HarfBuzz mirrors < and >
# before it looks up ligatures, so a typed `->` arrives as `hyphen less` and
# is already shown as "<-". Each rule turns what is on screen into the arrow
# it looks like, so `->` points the way the paragraph reads (←), the same way
# brackets flip. A typed `<=` arrives as `greater equal` and stays "less than
# or equal".
RTL_RULES = '''
  sub greater equal equal less by uni27FA;
  sub greater hyphen hyphen less by uni27F7;
  sub hyphen hyphen hyphen less by leftLongArrow2;
  sub greater hyphen hyphen hyphen by rightLongArrow2;
  sub greater equal less by arrowdblboth;
  sub greater hyphen less by arrowboth;
  sub equal equal less by uni27F8;
  sub greater equal equal by uni27F9;
  sub hyphen hyphen less by uni27F5;
  sub greater hyphen hyphen by uni27F6;
  sub hyphen less by arrowleft;
  sub greater hyphen by arrowright;
  sub equal less by arrowdblleft;
'''

FEATURES = f'''
languagesystem DFLT dflt;
languagesystem latn dflt;
languagesystem arab dflt;
languagesystem hebr dflt;

lookup ARROWS_LTR {{{LTR_RULES}}} ARROWS_LTR;
lookup ARROWS_RTL {{{RTL_RULES}}} ARROWS_RTL;

feature calt {{
  script DFLT; language dflt; lookup ARROWS_LTR;
  script latn; language dflt; lookup ARROWS_LTR;
  script arab; language dflt; lookup ARROWS_RTL;
  script hebr; language dflt; lookup ARROWS_RTL;
}} calt;
'''

COPYRIGHT = (
    'Copyright 2019 The Karla Project Authors (https://github.com/googlefonts/karla). '
    'Copyright (c) 2016 The Inter Project Authors (https://github.com/rsms/inter). '
    'Levanta Arrows: arrow ligatures for left-to-right and right-to-left text, '
    'by Beshoy Sabri, 2026.'
)
LICENSE = ('This Font Software is licensed under the SIL Open Font License, Version 1.1. '
           'This license is available with a FAQ at: https://openfontlicense.org')


def bounds(glyphset, name):
    pen = BoundsPen(glyphset)
    glyphset[name].draw(pen)
    return pen.bounds


def build(style, karla_src, inter_src, scale):
    params = STYLES[style]
    font = instancer.instantiateVariableFont(copy.deepcopy(karla_src), {'wght': params['karla_wght']})
    inter = instancer.instantiateVariableFont(copy.deepcopy(inter_src), {'wght': params['inter_wght'], 'opsz': 14})

    # Keep only Karla's four symbols; the layout tables are rebuilt below.
    options = subset.Options()
    options.layout_features = []
    options.glyph_names = True
    options.notdef_outline = True
    options.name_IDs = []
    options.drop_tables += ['STAT', 'GDEF', 'GPOS', 'GSUB']
    subsetter = subset.Subsetter(options)
    subsetter.populate(unicodes=KARLA.keys())
    subsetter.subset(font)

    k_upm, i_upm = font['head'].unitsPerEm, inter['head'].unitsPerEm
    k_gs, i_gs = font.getGlyphSet(), inter.getGlyphSet()

    # Centre the arrows on Karla's < and > rather than on Inter's taller axis.
    gt = bounds(k_gs, 'greater')
    target_centre = (gt[1] + gt[3]) / 2
    ar = bounds(i_gs, 'arrowright')
    s = scale * k_upm / i_upm
    dy = target_centre - (ar[1] + ar[3]) / 2 * s

    # glyf appends each new name to its glyph order as it is set, so work
    # from a copy and hand the final order to both afterwards.
    order = list(font.getGlyphOrder()) + list(ARROWS)
    glyf, hmtx = font['glyf'], font['hmtx']
    for name in ARROWS:
        rec = DecomposingRecordingPen(i_gs)
        i_gs[name].draw(rec)
        pen = TTGlyphPen(None)
        rec.replay(TransformPen(pen, (s, 0, 0, s, 0, dy)))
        glyph = pen.glyph()
        glyph.recalcBounds(glyf)
        glyf[name] = glyph
        hmtx[name] = (round(i_gs[name].width * s), glyph.xMin)
    font.setGlyphOrder(order)
    glyf.glyphOrder = order

    cmap = newTable('cmap')
    cmap.tableVersion = 0
    cmap.tables = []
    mapping = {**KARLA, **{cp: name for name, cp in ARROWS.items()}}
    for platform, encoding, fmt in ((0, 3, 4), (3, 1, 4), (0, 4, 12), (3, 10, 12)):
        table = CmapSubtable.newSubtable(fmt)
        table.platformID, table.platEncID, table.language = platform, encoding, 0
        table.cmap = {cp: g for cp, g in mapping.items() if fmt == 12 or cp <= 0xFFFF}
        cmap.tables.append(table)
    font['cmap'] = cmap

    addOpenTypeFeaturesFromString(font, FEATURES)

    bold = style == 'Bold'
    name = font['name']
    name.names = []
    ps = f'LevantaArrows-{style}'
    for name_id, value in {
        0: COPYRIGHT,
        1: 'Levanta Arrows',
        2: style,
        3: f'{VERSION};LVNT;{ps}',
        4: f'Levanta Arrows {style}',
        5: f'Version {VERSION}',
        6: ps,
        13: LICENSE,
        14: 'https://openfontlicense.org',
    }.items():
        name.setName(value, name_id, 3, 1, 0x409)

    os2 = font['OS/2']
    os2.usWeightClass = 700 if bold else 400
    os2.achVendID = 'LVNT'
    # Keep USE_TYPO_METRICS from Karla; set REGULAR or BOLD, clear ITALIC.
    os2.fsSelection = (os2.fsSelection & (1 << 7)) | ((1 << 5) if bold else (1 << 6))
    os2.updateFirstAndLastCharIndex(font)
    os2.recalcUnicodeRanges(font)
    head = font['head']
    head.macStyle = 1 if bold else 0
    head.fontRevision = float(VERSION)
    head.created = head.modified = timestampSinceEpoch(BUILD_DATE)
    font.recalcTimestamp = False
    font['post'].formatType = 2.0
    return font


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    parser.add_argument('--karla', default=FONTS / 'Karla.woff2', type=Path)
    parser.add_argument('--inter', default=FONTS / 'InterVariable.woff2', type=Path)
    parser.add_argument('--out', default=FONTS, type=Path)
    parser.add_argument('--scale', default=SCALE, type=float)
    args = parser.parse_args()

    karla, inter = TTFont(args.karla), TTFont(args.inter)
    args.out.mkdir(parents=True, exist_ok=True)
    for style in STYLES:
        font = build(style, karla, inter, args.scale)
        font.flavor = None
        font.save(args.out / f'LevantaArrows-{style}.ttf')
        font.flavor = 'woff2'
        font.save(args.out / f'LevantaArrows-{style}.woff2')
        print(f'LevantaArrows-{style}: {len(font.getGlyphOrder())} glyphs')


if __name__ == '__main__':
    main()
