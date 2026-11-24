#!/usr/bin/env python3
"""Experimental-procedure figures for the PLA-ZnO chapter (stdlib only).

All drawings are dimensioned schematics of the experimental set-up. None of them
plots measured data. Figure 2 is a placeholder for the laboratory photographs.
"""
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import svgplot as sp  # noqa: E402
from render import svg_to_png  # noqa: E402

OUT = os.path.join(ROOT, "pla_zno_chapter", "figures")
os.makedirs(OUT, exist_ok=True)

DEFS = ("<defs>"
        "<marker id='arr' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
        "<path d='M0,0 L10,5 L0,10 z' fill='#333'/></marker>"
        "<marker id='load' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='8' markerHeight='8' orient='auto-start-reverse'>"
        "<path d='M0,0 L10,5 L0,10 z' fill='#c0392b'/></marker>"
        "<marker id='dim' viewBox='0 0 10 10' refX='10' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'>"
        "<path d='M0,1 L10,5 L0,9 z' fill='#1b4f9c'/></marker>"
        "<pattern id='hatch' width='6' height='6' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'>"
        "<line x1='0' y1='0' x2='0' y2='6' stroke='#999' stroke-width='1'/></pattern>"
        "</defs>")

BLUE = "#1b4f9c"
RED = "#c0392b"


def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def mtext(x, y, text, width, size=11, anchor="middle", weight="normal", color="#111", lh=1.25):
    lines = wrap(text, width)
    o = [f"<text x='{x}' y='{y}' font-size='{size}' text-anchor='{anchor}' font-weight='{weight}' fill='{color}'>"]
    for i, ln in enumerate(lines):
        o.append(f"<tspan x='{x}' dy='{0 if i == 0 else size * lh:.1f}'>{sp.esc(ln)}</tspan>")
    o.append("</text>")
    return "".join(o)


def text(x, y, s, size=11, anchor="middle", weight="normal", color="#111", rotate=None):
    tr = f" transform='rotate({rotate} {x} {y})'" if rotate is not None else ""
    return (f"<text x='{x}' y='{y}' font-size='{size}' text-anchor='{anchor}' font-weight='{weight}' "
            f"fill='{color}'{tr}>{sp.esc(s)}</text>")


def line(x1, y1, x2, y2, col="#333", w=1.2, dash=None, marker=None, both=False):
    d = f" stroke-dasharray='{dash}'" if dash else ""
    m = f" marker-end='url(#{marker})'" if marker else ""
    if marker and both:
        m += f" marker-start='url(#{marker})'"
    return f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{col}' stroke-width='{w}'{d}{m}/>"


def rect(x, y, w, h, fill="none", stroke="#333", sw=1.2, rx=0, extra=""):
    return (f"<rect x='{x:.1f}' y='{y:.1f}' width='{w:.1f}' height='{h:.1f}' rx='{rx}' fill='{fill}' "
            f"stroke='{stroke}' stroke-width='{sw}' {extra}/>")


def hdim(x1, x2, y, label, ext_from=None, size=10.5, above=True):
    """Horizontal dimension line with arrowheads and a centred label."""
    o = []
    if ext_from is not None:
        o.append(line(x1, ext_from, x1, y + (-4 if y < ext_from else 4), "#1b4f9c", 0.7))
        o.append(line(x2, ext_from, x2, y + (-4 if y < ext_from else 4), "#1b4f9c", 0.7))
    o.append(line(x1, y, x2, y, BLUE, 0.9, marker="dim", both=True))
    o.append(text((x1 + x2) / 2, y - 4 if above else y + 13, label, size, color=BLUE))
    return "".join(o)


def vdim(x, y1, y2, label, ext_from=None, size=10.5, side="left"):
    o = []
    if ext_from is not None:
        s = -1 if x < ext_from else 1
        o.append(line(ext_from, y1, x + 4 * s, y1, BLUE, 0.7))
        o.append(line(ext_from, y2, x + 4 * s, y2, BLUE, 0.7))
    o.append(line(x, y1, x, y2, BLUE, 0.9, marker="dim", both=True))
    if side == "left":
        o.append(text(x - 5, (y1 + y2) / 2 + 4, label, size, anchor="end", color=BLUE))
    else:
        o.append(text(x + 5, (y1 + y2) / 2 + 4, label, size, anchor="start", color=BLUE))
    return "".join(o)


def save(name, w, h, body):
    svg = os.path.join(OUT, name + ".svg")
    with open(svg, "w") as f:
        f.write(sp.svg_doc(w, h, DEFS + body))
    svg_to_png(svg, os.path.join(OUT, name + ".png"))
    print("figure:", name)


# ------------------------------------------------------------------ Figure 1: workflow
def fig_workflow():
    W, H = 960, 380
    steps = [
        ("1. Drying", "PLA pellets 60 °C, 6 h; ZnO powder 110 °C, 2 h", "#e6eef7"),
        ("2. Weighing", "PLA and ZnO weighed to ±0.01 g for 0, 1, 3 and 5 wt% ZnO (Table 1)", "#e6eef7"),
        ("3. ZnO dispersion", "ZnO in anhydrous ethanol, magnetic stirring at 420 rpm for 30 min", "#e9f3e5"),
        ("4. Pellet coating", "PLA pellets added, tumbled until ethanol evaporates; dried 60 °C, 12 h", "#e9f3e5"),
        ("5. Melt compounding", "Extruded, cooled and pelletised to homogenise the ZnO", "#fbe7b5"),
        ("6. Filament extrusion", "Second extrusion pass to Ø1.75 ± 0.05 mm; diameter and MFI checked", "#fbe7b5"),
        ("7. 3D printing", "Flat (XY) build, 100 % infill, ±45° raster, same layout for every composition", "#f6e3e0"),
        ("8. Conditioning", "23 ± 2 °C and 50 ± 10 % RH for at least 40 h; dimensions and mass recorded", "#f6e3e0"),
        ("9. Mechanical tests", "Tensile, three-point flexure, Shore D hardness, fracture inspection", "#e3d9f0"),
    ]
    bw, bh, gap = 164, 100, 24
    o = [text(W / 2, 28, "Experimental sequence for PLA–ZnO feedstock, specimens and tests", 15, weight="bold")]
    pos = []
    x0 = (W - (5 * bw + 4 * gap)) / 2
    for i in range(5):
        pos.append((x0 + i * (bw + gap), 52))
    x1 = (W - (4 * bw + 3 * gap)) / 2
    for i in range(4):
        pos.append((x1 + i * (bw + gap), 216))
    for (lab, sub, col), (x, y) in zip(steps, pos):
        o.append(rect(x, y, bw, bh, col, "#333", 1.2, 9))
        o.append(text(x + bw / 2, y + 22, lab, 12.5, weight="bold"))
        o.append(mtext(x + bw / 2, y + 44, sub, 25, 10.2, color="#222"))
    for i in range(4):
        (xa, ya), (xb, _) = pos[i], pos[i + 1]
        o.append(line(xa + bw + 2, ya + bh / 2, xb - 3, ya + bh / 2, marker="arr", w=1.6))
    # elbow from step 5 to step 6
    xa, ya = pos[4]
    xb, yb = pos[5]
    ymid = (ya + bh + yb) / 2
    o.append(f"<path d='M{xa + bw / 2},{ya + bh + 2} L{xa + bw / 2},{ymid} L{xb + bw / 2},{ymid} L{xb + bw / 2},{yb - 3}' "
             "fill='none' stroke='#333' stroke-width='1.6' marker-end='url(#arr)'/>")
    for i in range(5, 8):
        (xa, ya), (xb, _) = pos[i], pos[i + 1]
        o.append(line(xa + bw + 2, ya + bh / 2, xb - 3, ya + bh / 2, marker="arr", w=1.6))
    legend = [("#e6eef7", "Raw materials"), ("#e9f3e5", "Mixture preparation"), ("#fbe7b5", "Feedstock"),
              ("#f6e3e0", "Specimens"), ("#e3d9f0", "Testing")]
    lx = 150
    for col, lab in legend:
        o.append(rect(lx, 345, 16, 12, col, "#555", 0.8, 2))
        o.append(text(lx + 22, 355, lab, 10.5, anchor="start"))
        lx += 22 + len(lab) * 6.6 + 34
    save("fig1_workflow", W, H, "\n".join(o))


# ------------------------------------------------------------------ Figure 2: photographs (placeholder)
def fig_equipment_placeholder():
    W, H = 900, 640
    panels = [("(a) 3D printer and filament feeder", "Bambu Lab printer with multi-spool feeder"),
              ("(b) Magnetic-stirring apparatus", "REMI 2MLH magnetic stirrer with flask"),
              ("(c) Melt-flow-index tester", "PACORR melt-flow-index tester"),
              ("(d) Stirrer controller detail", "Controller display at 420 rpm")]
    o = []
    for i, (cap, sub) in enumerate(panels):
        x = 20 + (i % 2) * 440
        y = 20 + (i // 2) * 310
        o.append(rect(x, y, 420, 290, "#f2f2f2", "#999", 1))
        o.append(rect(x, y + 262, 420, 28, "#fafafa", "#999", 1))
        o.append(text(x + 210, y + 281, cap, 11.5))
        o.append(text(x + 210, y + 120, "Insert original photograph", 14, weight="bold", color="#888"))
        o.append(text(x + 210, y + 144, sub, 11.5, color="#888"))
    save("fig2_equipment", W, H, "\n".join(o))


# ------------------------------------------------------------------ Figure 3: specimen geometry
def dogbone_path(x0, yc, s):
    """ASTM D638 Type I outline: L0 165, W0 19, W 13, narrow length 57, fillet R 76 (mm)."""
    xt = math.sqrt(76 ** 2 - 73 ** 2)  # fillet length along x (21.1 mm)
    a = 54 - xt
    pts_top = [(0, -9.5), (a, -9.5)]
    r = 76 * s

    def P(x, y):
        return f"{x0 + x * s:.1f},{yc + y * s:.1f}"
    d = (f"M{P(0, -9.5)} L{P(a, -9.5)} A{r:.1f},{r:.1f} 0 0 0 {P(54, -6.5)} L{P(111, -6.5)} "
         f"A{r:.1f},{r:.1f} 0 0 0 {P(165 - a, -9.5)} L{P(165, -9.5)} L{P(165, 9.5)} L{P(165 - a, 9.5)} "
         f"A{r:.1f},{r:.1f} 0 0 0 {P(111, 6.5)} L{P(54, 6.5)} A{r:.1f},{r:.1f} 0 0 0 {P(a, 9.5)} L{P(0, 9.5)} Z")
    del pts_top
    return d


def fig_specimens():
    W, H = 940, 640
    s = 4.0
    o = []
    # (a) tensile
    o.append(text(20, 28, "(a) Tensile specimen, ASTM D638 Type I (thickness 3.2 mm)", 13, anchor="start", weight="bold"))
    x0, yc = 140, 120
    o.append(f"<path d='{dogbone_path(x0, yc, s)}' fill='#dfe6ee' stroke='#333' stroke-width='1.3'/>")
    g1, g2 = x0 + 57.5 * s, x0 + 107.5 * s
    o.append(line(g1, yc - 26, g1, yc + 26, RED, 1.2, dash="4,3"))
    o.append(line(g2, yc - 26, g2, yc + 26, RED, 1.2, dash="4,3"))
    o.append(line(g1, yc + 26, g1, yc + 50, RED, 0.7))
    o.append(line(g2, yc + 26, g2, yc + 50, RED, 0.7))
    o.append(line(g1, yc + 50, g2, yc + 50, RED, 0.9))
    o.append(text((g1 + g2) / 2, yc + 64, "gauge length 50", 10.5, color=RED))
    o.append(hdim(x0, x0 + 165 * s, yc + 90, "overall length 165", ext_from=yc + 40, above=False))
    o.append(hdim(x0 + 54 * s, x0 + 111 * s, yc - 52, "narrow section 57", ext_from=yc - 28))
    o.append(vdim(x0 - 18, yc - 9.5 * s, yc + 9.5 * s, "W0 = 19", ext_from=x0))
    o.append(vdim(x0 + 80 * s, yc - 6.5 * s, yc + 6.5 * s, "W = 13", None, side="right"))
    o.append(text(x0 + 140 * s, yc - 52, "fillet R 76", 10.5, color=BLUE))
    o.append(line(x0 + 140 * s, yc - 47, x0 + 128 * s, yc - 7.9 * s, BLUE, 0.8))
    o.append(text(x0 + 165 * s + 14, yc - 2, "grip", 10.5, anchor="start", color="#444"))
    o.append(text(x0 + 165 * s + 14, yc + 12, "region", 10.5, anchor="start", color="#444"))
    # (b) flexural bar
    yb = 268
    o.append(text(20, yb, "(b) Flexural bar, ASTM D790 Procedure A", 13, anchor="start", weight="bold"))
    xb, ytop = 60, yb + 30
    o.append(rect(xb, ytop, 127 * s, 12.7 * s, "#e9f3e5", "#333", 1.3))
    o.append(text(xb + 63.5 * s, ytop + 30, "top view", 10.5, color="#444"))
    o.append(hdim(xb, xb + 127 * s, ytop + 12.7 * s + 24, "length 127", ext_from=ytop + 12.7 * s, above=False))
    o.append(vdim(xb + 127 * s + 18, ytop, ytop + 12.7 * s, "b = 12.7", ext_from=xb + 127 * s, side="right"))
    ys = ytop + 175
    o.append(text(xb, ys - 62, "side view on supports (span-to-depth ratio 16:1)", 10.5, anchor="start", color="#444"))
    o.append(rect(xb, ys, 127 * s, 3.2 * s, "#e9f3e5", "#333", 1.3))
    sl, sr = xb + (63.5 - 25.6) * s, xb + (63.5 + 25.6) * s
    for xs_ in (sl, sr):
        o.append(f"<path d='M{xs_ - 12},{ys + 3.2 * s + 22} L{xs_ + 12},{ys + 3.2 * s + 22} L{xs_},{ys + 3.2 * s} Z' fill='#bbb' stroke='#333'/>")
    xm = xb + 63.5 * s
    o.append(f"<path d='M{xm - 10},{ys - 22} L{xm + 10},{ys - 22} L{xm},{ys} Z' fill='#bbb' stroke='#333'/>")
    o.append(line(xm, ys - 48, xm, ys - 24, RED, 1.8, marker="load"))
    o.append(text(xm + 8, ys - 38, "P", 12, anchor="start", color=RED, weight="bold"))
    o.append(hdim(sl, sr, ys + 3.2 * s + 46, "support span L = 51.2", ext_from=ys + 3.2 * s + 24, above=False))
    o.append(vdim(xb + 127 * s + 18, ys, ys + 3.2 * s, "d = 3.2", ext_from=xb + 127 * s, side="right"))
    # (c) hardness block
    xh, yh = 680, yb + 30
    o.append(text(xh - 30, yb, "(c) Hardness block, Shore D", 13, anchor="start", weight="bold"))
    hs = 5.0
    o.append(rect(xh, yh, 40 * hs, 40 * hs, "url(#hatch)", "#333", 1.3))
    o.append(rect(xh + 12 * hs, yh + 12 * hs, 16 * hs, 16 * hs, "#fbe7b5", "#c08a1e", 1.0, extra="stroke-dasharray='4,3'"))
    for i, (px, py) in enumerate([(14, 14), (26, 14), (20, 20), (14, 26), (26, 26)]):
        o.append(f"<circle cx='{xh + px * hs}' cy='{yh + py * hs}' r='4.5' fill='{RED}'/>")
        o.append(text(xh + px * hs - 13, yh + py * hs - 6, str(i + 1), 10, anchor="start", color=RED))
    o.append(hdim(xh, xh + 40 * hs, yh + 40 * hs + 24, "40", ext_from=yh + 40 * hs, above=False))
    o.append(vdim(xh - 16, yh, yh + 40 * hs, "40", ext_from=xh))
    o.append(hdim(xh, xh + 12 * hs, yh - 10, "12", size=9.5))
    o.append(mtext(xh + 100, yh + 40 * hs + 56, "Thickness 6 mm. Hatched band: 12 mm edge margin with no indentations. "
                   "Sites 1–5 are at least 6 mm apart.", 40, 10, color="#333"))
    o.append(text(W / 2, H - 12, "All dimensions in millimetres. Drawings are to scale within each panel.", 10.5, color="#444"))
    save("fig3_specimens", W, H, "\n".join(o))


# ------------------------------------------------------------------ Figure 4: build layout and orientation
def fig_build():
    W, H = 960, 640
    s = 2.0
    px, py = 40, 60
    o = [text(px, 36, "(a) Build-plate layout for one composition (256 × 256 mm plate)", 13, anchor="start", weight="bold")]
    o.append(rect(px, py, 256 * s, 256 * s, "#f7f7f7", "#333", 1.4, 6))
    # tensile coupons
    for i in range(5):
        yc = 12 + 9.5 + i * 27
        d = dogbone_path(px + 12 * s, py + yc * s, s)
        o.append(f"<path d='{d}' fill='#dfe6ee' stroke='#333' stroke-width='1'/>")
        o.append(text(px + 12 * s + 165 * s + 6, py + yc * s + 4, f"T{i + 1}", 9.5, anchor="start"))
    for i in range(5):
        y = 150 + i * 17.7
        o.append(rect(px + 12 * s, py + y * s, 127 * s, 12.7 * s, "#e9f3e5", "#333", 1))
        o.append(text(px + 12 * s + 127 * s + 6, py + (y + 9) * s, f"F{i + 1}", 9.5, anchor="start"))
    for i, (bx, by) in enumerate([(160, 150), (208, 150), (160, 198)]):
        o.append(rect(px + bx * s, py + by * s, 40 * s, 40 * s, "#fbe7b5", "#333", 1))
        o.append(text(px + (bx + 20) * s, py + (by + 23) * s, f"H{i + 1}", 10))
    # axes
    ax, ay = px + 256 * s - 70, py + 256 * s - 18
    o.append(line(ax, ay, ax + 40, ay, marker="arr", w=1.3))
    o.append(line(ax, ay, ax, ay - 40, marker="arr", w=1.3))
    o.append(text(ax + 48, ay + 4, "X", 11, weight="bold"))
    o.append(text(ax, ay - 46, "Y", 11, weight="bold"))
    o.append(mtext(px + 128 * s, py + 256 * s + 24, "T = tensile, F = flexural, H = hardness. Specimen IDs record composition, "
                   "plate position and build number.", 80, 10.5, color="#333"))
    # (b) raster
    rx, ry = 610, 60
    o.append(text(rx, 36, "(b) Alternating ±45° raster", 13, anchor="start", weight="bold"))
    for k, (ang, lab) in enumerate([(45, "odd layers +45°"), (-45, "even layers −45°")]):
        bx = rx + k * 160
        o.append(f"<clipPath id='c{k}'><rect x='{bx}' y='{ry}' width='130' height='130'/></clipPath>")
        o.append(rect(bx, ry, 130, 130, "#fff", "#333", 1.2))
        g = [f"<g clip-path='url(#c{k})'>"]
        for t in range(-260, 260, 10):
            if ang > 0:
                g.append(line(bx + t, ry + 130, bx + t + 130, ry, "#1b4f9c", 0.9))
            else:
                g.append(line(bx + t, ry, bx + t + 130, ry + 130, "#d1495b", 0.9))
        g.append("</g>")
        o.append("".join(g))
        o.append(text(bx + 65, ry + 148, lab, 10.5))
    o.append(mtext(rx + 145, ry + 178, "Two perimeters surround the raster. Line width 0.42 mm; layer height 0.20 mm.", 44, 10.5, color="#333"))
    # (c) side view, load direction
    sy = 330
    o.append(text(rx, sy, "(c) Loading relative to layers (XY build)", 13, anchor="start", weight="bold"))
    lx, ly, lw = rx + 50, sy + 50, 220
    for i in range(8):
        o.append(rect(lx, ly + i * 9, lw, 9, "#dfe6ee" if i % 2 else "#c9d6e4", "#7a8a9a", 0.6))
    o.append(line(lx - 4, ly + 36, lx - 44, ly + 36, RED, 2, marker="load"))
    o.append(line(lx + lw + 4, ly + 36, lx + lw + 44, ly + 36, RED, 2, marker="load"))
    o.append(text(lx + lw / 2, ly + 92, "tension acts along the layers (in-plane)", 10.5, color=RED))
    o.append(line(lx + lw + 62, ly, lx + lw + 62, ly + 72, BLUE, 0.9, marker="dim", both=True))
    o.append(text(lx + lw + 68, ly - 10, "Z (build direction)", 10, anchor="end", color=BLUE))
    o.append(mtext(rx + 145, ly + 130, "Every composition uses this orientation. Layer interfaces lie parallel to the load, "
                   "so interlayer bonding is not loaded directly in tension.", 46, 10.5, color="#333"))
    save("fig4_build_layout", W, H, "\n".join(o))


# ------------------------------------------------------------------ Figure 5: test set-ups
def fig_setups():
    W, H = 960, 500
    o = []
    # (a) tensile
    cx = 150
    o.append(text(cx, 30, "(a) Uniaxial tension", 13, weight="bold"))
    o.append(rect(cx - 50, 50, 100, 26, "#999", "#333", 1, 3))
    o.append(text(cx, 68, "load cell 5 kN", 10, color="white"))
    o.append(rect(cx - 34, 84, 68, 52, "#bbb", "#333", 1, 2))
    o.append(rect(cx - 34, 334, 68, 52, "#bbb", "#333", 1, 2))
    o.append(text(cx + 42, 112, "wedge grip", 10, anchor="start", color="#444"))
    o.append(text(cx + 42, 362, "wedge grip", 10, anchor="start", color="#444"))
    o.append(f"<path d='M{cx - 10},96 L{cx + 10},96 L{cx + 10},160 Q{cx + 10},176 {cx + 6.5},186 L{cx + 6.5},284 "
             f"Q{cx + 10},294 {cx + 10},310 L{cx + 10},374 L{cx - 10},374 L{cx - 10},310 Q{cx - 10},294 {cx - 6.5},284 "
             f"L{cx - 6.5},186 Q{cx - 10},176 {cx - 10},160 Z' fill='#dfe6ee' stroke='#333' stroke-width='1.2'/>")
    o.append(rect(cx - 22, 196, 44, 7, BLUE, BLUE, 0.5, 1))
    o.append(rect(cx - 22, 266, 44, 7, BLUE, BLUE, 0.5, 1))
    o.append(line(cx + 22, 199.5, cx + 46, 199.5, BLUE, 0.8))
    o.append(line(cx + 22, 269.5, cx + 46, 269.5, BLUE, 0.8))
    o.append(vdim(cx + 46, 199.5, 269.5, "extensometer, 50 mm", side="right", size=10))
    o.append(line(cx, 390, cx, 432, RED, 2, marker="load"))
    o.append(text(cx, 452, "crosshead 5 mm/min", 10.5, color=RED))
    # (b) flexure
    bx = 480
    o.append(text(bx, 30, "(b) Three-point flexure", 13, weight="bold"))
    o.append(line(bx, 80, bx, 160, RED, 2, marker="load"))
    o.append(text(bx + 8, 110, "1.37 mm/min", 10.5, anchor="start", color=RED))
    o.append(f"<path d='M{bx - 16},160 L{bx + 16},160 L{bx + 16},176 A16,16 0 0 1 {bx - 16},176 Z' fill='#bbb' stroke='#333'/>")
    o.append(text(bx - 22, 176, "nose R 5", 10, anchor="end", color="#444"))
    o.append(rect(bx - 150, 192, 300, 14, "#e9f3e5", "#333", 1.2))
    for xs_ in (bx - 110, bx + 110):
        o.append(f"<path d='M{xs_ - 16},222 A16,16 0 0 1 {xs_ + 16},222 L{xs_ + 16},250 L{xs_ - 16},250 Z' fill='#bbb' stroke='#333'/>")
    o.append(text(bx + 130, 244, "support R 5", 10, anchor="start", color="#444"))
    o.append(rect(bx - 140, 250, 280, 12, "#888", "#333", 1))
    o.append(hdim(bx - 110, bx + 110, 290, "L = 51.2 mm", ext_from=262, above=False))
    o.append(f"<path d='M{bx - 150},199 Q{bx},226 {bx + 150},199' fill='none' stroke='{RED}' stroke-width='1' stroke-dasharray='4,3'/>")
    o.append(text(bx, 340, "deflection D measured at mid-span", 10.5, color="#333"))
    o.append(text(bx, 358, "test ends at break or 5 % outer-fibre strain", 10.5, color="#333"))
    # (c) Shore D
    hx = 800
    o.append(text(hx, 30, "(c) Shore D hardness", 13, weight="bold"))
    o.append(rect(hx - 90, 400, 180, 14, "#888", "#333", 1))
    o.append(rect(hx + 66, 90, 16, 310, "#aaa", "#333", 1))
    o.append(rect(hx - 40, 96, 122, 18, "#aaa", "#333", 1))
    o.append(rect(hx - 34, 114, 8, 68, "#777", "#333", 1))
    o.append(rect(hx - 52, 132, 44, 30, "#666", "#333", 1, 3))
    o.append(text(hx - 30, 152, "5 kg", 10, color="white"))
    o.append(text(hx + 60, 160, "stand", 10, anchor="end", color="#444"))
    o.append(f"<circle cx='{hx - 30}' cy='222' r='50' fill='#f3f3f3' stroke='#333' stroke-width='1.3'/>")
    o.append(line(hx - 30, 222, hx - 2, 196, "#333", 1.4))
    o.append(text(hx - 30, 252, "Shore D", 10, color="#444"))
    o.append(rect(hx - 44, 272, 28, 12, "#ccc", "#333", 1))
    o.append(f"<path d='M{hx - 34},284 L{hx - 26},284 L{hx - 30},302 Z' fill='#333'/>")
    o.append(rect(hx - 70, 302, 120, 30, "#fbe7b5", "#333", 1.2))
    o.append(text(hx - 10, 322, "6 mm block", 10))
    o.append(rect(hx - 80, 332, 140, 68, "#ddd", "#333", 1))
    o.append(text(hx - 10, 372, "rigid flat support", 10, color="#444"))
    o.append(text(hx, 440, "reading taken 1 s after contact", 10.5, color="#333"))
    o.append(text(hx, 458, "5 sites per block (Figure 3c)", 10.5, color="#333"))
    o.append(text(W / 2, H - 10, "Schematic, not to scale.", 10.5, color="#444"))
    save("fig5_test_setups", W, H, "\n".join(o))


# ------------------------------------------------------------------ Figure 6: data reduction
def fig_reduction():
    W, H = 960, 440
    o = []

    def axes(x0, y0, w, h, xl, yl):
        a = [line(x0, y0, x0 + w, y0, "#333", 1.3, marker="arr"), line(x0, y0, x0, y0 - h, "#333", 1.3, marker="arr")]
        a.append(text(x0 + w / 2, y0 + 30, xl, 11.5))
        a.append(text(x0 - 22, y0 - h / 2, yl, 11.5, rotate=-90))
        return "".join(a)

    # (a) tensile
    x0, y0, w, h = 80, 360, 360, 290
    o.append(text(x0 - 40, 34, "(a) Tensile record", 13, anchor="start", weight="bold"))
    o.append(axes(x0, y0, w, h, "engineering strain ε", "engineering stress σ"))
    pts = []
    for i in range(121):
        e = i / 120 * 1.0
        sig = 1.0 - (1 - e / 0.62) ** 2 if e <= 0.62 else 1.0 - 0.6 * (e - 0.62) ** 2
        pts.append((x0 + e * 300, y0 - sig * 230))
    o.append("<polyline points='" + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + "' fill='none' stroke='#111' stroke-width='2'/>")
    xb, yb = pts[-1]
    o.append(line(xb, yb, xb, yb + 26, "#111", 2))
    # chord modulus region
    e1, e2 = 0.04, 0.16
    xa1, xa2 = x0 + e1 * 300, x0 + e2 * 300
    o.append(rect(xa1, y0 - 250, xa2 - xa1, 250, BLUE, "none", 0, extra="fill-opacity='0.10'"))
    sl = 2 / 0.62 * 230 / 300
    o.append(line(x0, y0, x0 + 80, y0 - 80 * sl, BLUE, 1.4, dash="5,3"))
    o.append(mtext(xa2 + 5, y0 - 80, "E: least-squares slope between 0.05 % and 0.25 % strain (shaded band, width exaggerated)", 23, 10, anchor="start", color=BLUE))
    pk = pts[int(0.62 * 120)]
    o.append(f"<circle cx='{pk[0]:.1f}' cy='{pk[1]:.1f}' r='5' fill='{RED}'/>")
    o.append(text(pk[0], pk[1] - 12, "σmax = Fmax / A0", 11, color=RED))
    o.append(line(pk[0], pk[1] + 6, pk[0], y0, RED, 0.8, dash="3,3"))
    o.append(text(pk[0], y0 + 14, "ε at σmax", 10, color=RED))
    o.append(f"<circle cx='{xb:.1f}' cy='{yb:.1f}' r='5' fill='#2e8b57'/>")
    o.append(line(xb, yb + 26, xb, y0, "#2e8b57", 0.8, dash="3,3"))
    o.append(text(xb, y0 + 14, "εb (break)", 10, color="#2e8b57"))
    # (b) flexural
    x0, y0 = 560, 360
    o.append(text(x0 - 40, 34, "(b) Flexural record", 13, anchor="start", weight="bold"))
    o.append(axes(x0, y0, w, h, "mid-span deflection D", "load P"))
    pts = []
    for i in range(101):
        dd = i / 100 * 0.78
        p = 1.0 - (1 - dd / 0.7) ** 2 if dd <= 0.7 else 1.0 - 0.8 * (dd - 0.7) ** 2
        pts.append((x0 + dd * 300, y0 - p * 230))
    o.append("<polyline points='" + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + "' fill='none' stroke='#111' stroke-width='2'/>")
    sl = 2 / 0.7 * 230 / 300
    o.append(line(x0, y0, x0 + 120, y0 - 120 * sl, BLUE, 1.4, dash="5,3"))
    o.append(text(x0 + 126, y0 - 120 * sl - 4, "initial slope m", 10.5, anchor="start", color=BLUE))
    pk = pts[int(0.7 / 0.78 * 100)]
    o.append(f"<circle cx='{pk[0]:.1f}' cy='{pk[1]:.1f}' r='5' fill='{RED}'/>")
    o.append(text(pk[0] - 10, pk[1] - 12, "Pmax → σf", 11, color=RED))
    x5 = x0 + 0.78 * 300
    o.append(line(x5, y0, x5, y0 - 260, "#777", 1, dash="6,4"))
    o.append(text(x5 + 4, y0 - 264, "D at 5 % strain limit", 10, anchor="start", color="#555"))
    o.append(text(W / 2, H - 10, "Illustrative curve shapes showing where each property is read. These are not measured data.", 10.5, color="#444"))
    save("fig6_data_reduction", W, H, "\n".join(o))


if __name__ == "__main__":
    fig_workflow()
    fig_equipment_placeholder()
    fig_specimens()
    fig_build()
    fig_setups()
    fig_reduction()
