#!/usr/bin/env python3
"""Conceptual figures for the chapter 'Academic Identity and Professional Development' (stdlib only)."""
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import svgplot as sp  # noqa: E402

OUT = os.path.join(ROOT, "chapter", "figures")
os.makedirs(OUT, exist_ok=True)

DEFS = ("<defs><marker id='arr' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
        "<path d='M0,0 L10,5 L0,10 z' fill='#333'/></marker></defs>")


def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def mtext(x, y, text, width, size=11, anchor="middle", weight="normal", color="#111", lh=1.25, style=""):
    lines = wrap(text, width)
    out = [f"<text x='{x}' y='{y}' font-size='{size}' text-anchor='{anchor}' font-weight='{weight}' fill='{color}' {style}>"]
    for i, ln in enumerate(lines):
        out.append(f"<tspan x='{x}' dy='{0 if i == 0 else size * lh:.1f}'>{sp.esc(ln)}</tspan>")
    out.append("</text>")
    return "".join(out), len(lines)


def box(x, y, w, h, title, body, fill, tsize=12, bsize=10.2, width=None, rx=9, stroke="#333"):
    o = [f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='{fill}' stroke='{stroke}' stroke-width='1.2'/>"]
    t, n = mtext(x + w / 2, y + 19, title, int(w / (tsize * 0.58)), tsize, weight="bold")
    o.append(t)
    if body:
        b, _ = mtext(x + w / 2, y + 22 + n * tsize * 1.25, body, width or int(w / (bsize * 0.55)), bsize, color="#222")
        o.append(b)
    return "".join(o)


def arrow(x1, y1, x2, y2, col="#333", dash=None, width=1.6, both=False):
    d = f" stroke-dasharray='{dash}'" if dash else ""
    st = " marker-start='url(#arr)'" if both else ""
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{width}'{d} marker-end='url(#arr)'{st}/>"


def save(name, w, h, body):
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(sp.svg_doc(w, h, DEFS + body))


# ------------------------------------------------------------------ Figure 1
def fig1():
    W, H = 900, 720
    cx, cy = 450, 360
    o = []
    o.append(f"<circle cx='{cx}' cy='{cy}' r='265' fill='#f4f1ea' stroke='#8a7a55' stroke-width='1.2' stroke-dasharray='6,4'/>")
    drivers = [("Digitalisation", 450, 38), ("Interdisciplinarity", 130, 668), ("Globalisation and mobility", 770, 668)]
    for lab, x, y in drivers:
        o.append(f"<rect x='{x - 110}' y='{y - 16}' width='220' height='32' rx='16' fill='#8a7a55'/>"
                 f"<text x='{x}' y='{y + 5}' font-size='12.5' fill='white' text-anchor='middle' font-weight='bold'>{lab}</text>")
        dx, dy = cx - x, cy - y
        L = math.hypot(dx, dy)
        x1, y1 = x + dx / L * 22, y + dy / L * 22
        x2, y2 = cx - dx / L * 258, cy - dy / L * 258
        o.append(arrow(round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1), col="#8a7a55", dash="5,3"))
    roles = [("Teaching", "pedagogic expertise, student learning, curriculum", "#cfe0f3"),
             ("Research", "inquiry, publication, knowledge creation", "#f6d6c8"),
             ("Leadership", "academic citizenship, governance, mentoring", "#e3d9f0"),
             ("Community engagement", "outreach, extension, public scholarship", "#d6ecd2"),
             ("Lifelong learning", "continuous professional development, reflection", "#fbe7b5")]
    for i, (lab, sub, col) in enumerate(roles):
        a = math.radians(-90 + i * 72)
        x, y = cx + 128 * math.cos(a), cy + 128 * math.sin(a)
        o.append(f"<ellipse cx='{x:.1f}' cy='{y:.1f}' rx='112' ry='72' fill='{col}' fill-opacity='0.88' stroke='#555' stroke-width='1' "
                 f"transform='rotate({i * 72} {x:.1f} {y:.1f})'/>")
    for i, (lab, sub, col) in enumerate(roles):
        a = math.radians(-90 + i * 72)
        x, y = cx + 158 * math.cos(a), cy + 158 * math.sin(a)
        t, n = mtext(x, y - 10, lab, 22, 12.5, weight="bold")
        o.append(t)
        t, _ = mtext(x, y - 10 + n * 15.5 + 4, sub, 24, 9.6, color="#333")
        o.append(t)
    o.append(f"<circle cx='{cx}' cy='{cy}' r='62' fill='white' stroke='#1b4f9c' stroke-width='2'/>")
    t, _ = mtext(cx, cy - 12, "Academic identity", 12, 13, weight="bold", color="#1b4f9c")
    o.append(t)
    t, _ = mtext(cx, cy + 20, "negotiated, relational, in continuous becoming", 18, 9.2, color="#1b4f9c")
    o.append(t)
    for k in range(3):
        a0 = math.radians(k * 120 + 20)
        a1 = math.radians(k * 120 + 85)
        r = 76
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        o.append(f"<path d='M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}' fill='none' stroke='#1b4f9c' stroke-width='1.6' marker-end='url(#arr)'/>")
    o.append(f"<text x='{cx}' y='{H - 14}' font-size='10.5' text-anchor='middle' fill='#444'>Overlaps denote hybrid roles; dashed arrows denote "
             "macro-level transformations that continuously reshape the configuration.</text>")
    save("fig1_identity_model", W, H, "\n".join(o))


# ------------------------------------------------------------------ Figure 2
def fig2():
    W, H = 900, 600
    o = []
    layers = [("Global environment", "rankings and league tables · internationalisation · technology platforms · international research funding", "#efe7d6", 420, 270),
              ("National policy and regulation", "NEP 2020 · UGC regulations and career advancement criteria · accreditation and quality assurance", "#e6eef7", 330, 210),
              ("Institutional culture and governance", "mission and strategy · performance appraisal · workload allocation · digital infrastructure · reward systems", "#e9f3e5", 240, 152),
              ("Disciplinary and departmental communities", "epistemic norms · collegial networks · communities of practice · student expectations", "#f6e3e0", 150, 96)]
    cx, cy = 320, 310
    for i, (lab, sub, col, rx, ry) in enumerate(layers):
        o.append(f"<ellipse cx='{cx}' cy='{cy}' rx='{rx * 0.74}' ry='{ry}' fill='{col}' stroke='#666' stroke-width='1'/>")
    labpos = [58, 118, 176, 232]
    for (lab, sub, col, rx, ry), ly in zip(layers, labpos):
        t, n = mtext(cx, ly, lab, 60, 11.5, weight="bold")
        o.append(t)
        t2, _ = mtext(cx, ly + 14, sub, 70 if rx > 300 else (56 if rx > 200 else 40), 9.2, color="#333")
        o.append(t2)
    o.append(f"<ellipse cx='{cx}' cy='{cy + 18}' rx='78' ry='52' fill='white' stroke='#1b4f9c' stroke-width='2'/>")
    t, _ = mtext(cx, cy + 6, "Individual academic", 14, 11.5, weight="bold", color="#1b4f9c")
    o.append(t)
    t, _ = mtext(cx, cy + 34, "values · aspirations · self-efficacy · career stage", 22, 9, color="#1b4f9c")
    o.append(t)
    # negotiation panel on the right
    x0 = 690
    o.append(f"<rect x='{x0}' y='70' width='195' height='470' rx='10' fill='#fafafa' stroke='#333'/>")
    o.append(f"<text x='{x0 + 97}' y='94' font-size='12.5' font-weight='bold' text-anchor='middle'>Identity negotiation</text>")
    items = [("Systemic pressure", "metrics, accountability, efficiency demands", "#d1495b"),
             ("Personal agency", "values, scholarly commitments, professional autonomy", "#1b4f9c"),
             ("Possible outcomes", "alignment · strategic compliance · resistance · hybrid reinvention · exit", "#2e8b57")]
    y = 112
    for lab, sub, col in items:
        o.append(f"<rect x='{x0 + 12}' y='{y}' width='171' height='112' rx='8' fill='white' stroke='{col}' stroke-width='1.6'/>")
        t, n = mtext(x0 + 97, y + 22, lab, 22, 11.5, weight="bold", color=col)
        o.append(t)
        t, _ = mtext(x0 + 97, y + 44, sub, 26, 9.8, color="#222")
        o.append(t)
        y += 140
    o.append(arrow(x0 + 97, 224, x0 + 97, 250))
    o.append(arrow(x0 + 97, 364, x0 + 97, 390))
    o.append(arrow(cx + 316, cy, x0 - 4, cy, col="#555", dash="5,4", both=True))
    o.append(f"<text x='{x0 + 97}' y='565' font-size='9.8' fill='#555' text-anchor='middle'>top-down structuring ⇄ bottom-up agency</text>")
    save("fig2_forces_model", W, H, "\n".join(o))


# ------------------------------------------------------------------ Figure 3
def fig3():
    W, H = 900, 470
    o = []
    stages = [("1. Needs diagnosis", "self-assessment, appraisal dialogue, student feedback, career-stage analysis", "#e6eef7"),
              ("2. Learning pathways", "faculty development programmes · mentoring · faculty learning communities · online and AI-supported modules", "#e9f3e5"),
              ("3. Practice integration", "classroom enactment, research projects, leadership assignments, peer observation", "#fbe7b5"),
              ("4. Evidence and recognition", "teaching portfolios, outputs, competency assessment, stackable micro-credentials", "#f6e3e0"),
              ("5. Career progression", "promotion, leadership roles, mobility, renewed identity", "#e3d9f0")]
    bw, bh, gap = 158, 112, 20
    x = 22
    for i, (lab, sub, col) in enumerate(stages):
        o.append(box(x, 60, bw, bh, lab, sub, col, tsize=11.8, bsize=9.8))
        if i < len(stages) - 1:
            o.append(arrow(x + bw + 2, 60 + bh / 2, x + bw + gap - 2, 60 + bh / 2))
        x += bw + gap
    # feedback loop
    o.append(f"<path d='M{22 + 4 * (bw + gap) + bw / 2},{60 + bh} L{22 + 4 * (bw + gap) + bw / 2},{60 + bh + 40} L{22 + bw / 2},{60 + bh + 40} L{22 + bw / 2},{60 + bh + 4}' "
             "fill='none' stroke='#1b4f9c' stroke-width='1.8' stroke-dasharray='6,4' marker-end='url(#arr)'/>")
    o.append(f"<text x='450' y='{60 + bh + 34}' font-size='11' fill='#1b4f9c' text-anchor='middle'>Reflective practice and evaluation feed the next development cycle</text>")
    # pillars
    y0 = 250
    o.append(f"<text x='450' y='{y0}' font-size='13' font-weight='bold' text-anchor='middle'>Core pillars sustaining the cycle</text>")
    pillars = [("Digital pedagogy", "online and blended design, learning analytics, technology–pedagogy–content integration", "#cfe0f3"),
               ("Research capacity", "methods training, grant writing, research ethics, open science, collaboration networks", "#f6d6c8"),
               ("Leadership development", "academic leadership, inclusive management, change leadership, mentoring others", "#e3d9f0"),
               ("Collegial infrastructure", "protected time, recognition in appraisal, communities of practice, funding", "#d6ecd2")]
    pw = 200
    x = 22
    for lab, sub, col in pillars:
        o.append(box(x, y0 + 14, pw, 96, lab, sub, col, tsize=12, bsize=9.8))
        x += pw + 17
    o.append(f"<rect x='22' y='{y0 + 124}' width='{4 * pw + 3 * 17}' height='34' rx='6' fill='#5b5b5b'/>")
    o.append(f"<text x='{22 + (4 * pw + 51) / 2}' y='{y0 + 146}' font-size='11.5' fill='white' text-anchor='middle' font-weight='bold'>"
             "Institutional enabling conditions: policy alignment, resources, ethical and inclusive culture</text>")
    save("fig3_cpd_ecosystem", W, H, "\n".join(o))


# ------------------------------------------------------------------ Figure 4
def fig4():
    W, H = 900, 520
    o = []
    o.append(box(30, 50, 250, 150, "Job demands", "teaching and administrative workload · publication and grant metrics · digital adaptation and constant connectivity · role ambiguity · contractual insecurity", "#f6e3e0"))
    o.append(box(30, 300, 250, 150, "Job and personal resources", "autonomy and academic freedom · collegial and mentoring support · protected development time · fair appraisal · self-efficacy and reflective capacity", "#e9f3e5"))
    o.append(box(340, 50, 230, 100, "Health-impairment process", "chronic strain → exhaustion, disengagement, attrition", "#f2c7c1"))
    o.append(box(340, 350, 230, 100, "Motivational process", "engagement → professional growth, innovation, identity consolidation", "#cbe6c4"))
    o.append(arrow(282, 110, 338, 100, col="#b22"))
    o.append(arrow(282, 390, 338, 400, col="#2e8b57"))
    o.append(arrow(155, 298, 155, 202, col="#2e8b57", dash="4,3"))
    o.append("<text x='162' y='254' font-size='9.8' fill='#2e8b57'>resources buffer demands</text>")
    o.append("<circle cx='455' cy='250' r='60' fill='white' stroke='#1b4f9c' stroke-width='2'/>")
    t, _ = mtext(455, 242, "Academic resilience", 12, 12, weight="bold", color="#1b4f9c")
    o.append(t)
    t, _ = mtext(455, 272, "adaptive, relational, learnable", 16, 9.2, color="#1b4f9c")
    o.append(t)
    o.append(arrow(455, 190, 455, 153, col="#1b4f9c", dash="3,3"))
    o.append("<text x='462' y='176' font-size='9.4' fill='#1b4f9c'>attenuates</text>")
    o.append(arrow(455, 310, 455, 347, col="#1b4f9c"))
    o.append("<text x='462' y='334' font-size='9.4' fill='#1b4f9c'>amplifies</text>")
    o.append("<rect x='610' y='50' width='265' height='400' rx='10' fill='#fafafa' stroke='#333'/>")
    o.append("<text x='742' y='76' font-size='12.5' font-weight='bold' text-anchor='middle'>Strategic levers</text>")
    levers = [("Individual", "reflective practice · boundary setting · peer support · purposeful career planning", "#1b4f9c"),
              ("Leadership", "inclusive, distributed and compassionate leadership · transparent workload models", "#6a4c93"),
              ("Institutional", "well-being policy · sustainable metrics · recognition of teaching and service · secure contracts", "#2e8b57")]
    y = 90
    for lab, sub, col in levers:
        o.append(f"<rect x='622' y='{y}' width='241' height='104' rx='8' fill='white' stroke='{col}' stroke-width='1.6'/>")
        t, _ = mtext(742, y + 22, lab, 22, 11.8, weight="bold", color=col)
        o.append(t)
        t, _ = mtext(742, y + 44, sub, 34, 9.9)
        o.append(t)
        y += 118
    o.append(arrow(608, 250, 517, 250, col="#333"))
    o.append("<text x='563' y='242' font-size='9.6' text-anchor='middle'>strengthen</text>")
    o.append("<text x='450' y='495' font-size='10.5' text-anchor='middle' fill='#444'>Adapted from the job demands–resources model to the academic profession: "
             "resilience mediates whether demands lead to strain or to growth.</text>")
    save("fig4_resilience_model", W, H, "\n".join(o))


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4()
    print("figures written to", OUT)
