#!/usr/bin/env python3
"""Generate all manuscript figures as SVG from simulation output (stdlib only)."""
import csv
import json
import math
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import svgplot as sp  # noqa: E402

RUNS = os.path.join(ROOT, "runs")
FIG = os.path.join(ROOT, "manuscript", "figures")
os.makedirs(FIG, exist_ok=True)
T_S = 365
UG_PER_ML = 0.044e-9 * 149e3 * 1e3  # phi_v units -> ug/mL (VEGF 0.044 nM per unit; IgG 149 kDa)
SUM = json.load(open(os.path.join(ROOT, "results", "summary.json")))

REG_LABEL = {"R0": "No treatment", "R1": "Surgery alone", "R2": "Surgery + 1-yr anti-VEGF",
             "R3": "Surgery + continuous anti-VEGF", "R4": "Neoadjuvant + 1-yr adjuvant"}
REG_COL = {"R0": "#7f7f7f", "R1": "#3d3d3d", "R2": "#1b4f9c", "R3": "#2e8b57", "R4": "#d1495b"}
REG_DASH = {"R0": "2,3", "R1": None, "R2": None, "R3": "7,3", "R4": "3,2"}


def ts(exp, name):
    with open(os.path.join(RUNS, exp, name + "_ts.csv")) as f:
        return [{k: float(v) for k, v in r.items()} for r in csv.DictReader(f)]


def snap(exp, name, t):
    with open(os.path.join(RUNS, exp, f"{name}_snap_{t:04d}.bin"), "rb") as f:
        n = struct.unpack("i", f.read(4))[0]
        fields = []
        for _ in range(7):
            arr = struct.unpack(f"{n * n}f", f.read(4 * n * n))
            fields.append([list(arr[j * n:(j + 1) * n]) for j in range(n)])
    keys = ["c", "s", "m", "b", "v", "A", "sig"]
    return dict(zip(keys, fields)), n


def save(name, w, h, body):
    with open(os.path.join(FIG, name + ".svg"), "w") as f:
        f.write(sp.svg_doc(w, h, body))


# ---------------------------------------------------------------- Figure 1
def fig1():
    W, H = 900, 500
    o = []
    BW, BH = 175, 64
    X = [30, 270, 510]
    Y = [45, 185, 345]

    def box(ci, ri, title, sub, fill):
        x, y = X[ci], Y[ri]
        o.append(f"<rect x='{x}' y='{y}' width='{BW}' height='{BH}' rx='9' fill='{fill}' stroke='#333' stroke-width='1.2'/>")
        o.append(f"<text x='{x + BW / 2}' y='{y + 20}' text-anchor='middle' font-size='12.5' font-weight='bold'>{title}</text>")
        for i, s_ in enumerate(sub):
            o.append(f"<text x='{x + BW / 2}' y='{y + 37 + 14 * i}' text-anchor='middle' font-size='10.5'>{s_}</text>")

    def path(pts, col="#333", dash=None, inhib=False, label="", lpos=None, lcol=None, anchor="middle"):
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        da = f" stroke-dasharray='{dash}'" if dash else ""
        mk = "url(#bar)" if inhib else "url(#arr)"
        o.append(f"<path d='{d}' fill='none' stroke='{col}' stroke-width='1.6'{da} marker-end='{mk}'/>")
        if label:
            lx, ly = lpos
            o.append(f"<text x='{lx}' y='{ly}' font-size='10.5' fill='{lcol or col}' text-anchor='{anchor}'>{label}</text>")

    o.append("<defs><marker id='arr' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
             "<path d='M0,0 L10,5 L0,10 z' fill='#333'/></marker>"
             "<marker id='bar' viewBox='0 0 10 10' refX='5' refY='5' markerWidth='9' markerHeight='9' orient='auto'>"
             "<path d='M5,0 L5,10' stroke='#b22' stroke-width='3'/></marker></defs>")
    o.append("<text x='10' y='24' font-size='15' font-weight='bold'>A</text>")
    box(0, 0, "Primary tumour c", ["proliferation, hypoxic death", "removed at excision"], "#dbe7f6")
    box(0, 1, "Satellites s", ["Poisson seeding before", "surgery; same kinetics"], "#dbe7f6")
    box(1, 0, "VEGF (free v, total V)", ["tumour: constitutive + hypoxic", "activated immune cells"], "#f8e1c4")
    box(1, 1, "Microvessels b", ["sprouting S(v) / regression", "O₂ supply σ, co-option κn"], "#f6d5d5")
    box(2, 0, "Anti-VEGF antibody A", ["plasma Cp(t), extravasation", "∝ b; binding constant KD"], "#e3f1df")
    box(2, 1, "Immune cells m", ["recruited through vessels", "kill tumour, secrete VEGF"], "#ece3f5")
    box(0, 2, "Chemokine a", ["secreted by tumour and", "activated immune cells"], "#ece3f5")
    box(2, 2, "Systemic priming P(t)", ["driven by tumour burden", "decays after excision"], "#ece3f5")
    cx = lambda ci: X[ci] + BW / 2
    # tumour -> VEGF
    path([(X[0] + BW, Y[0] + 32), (X[1] - 2, Y[0] + 32)], label="secretion", lpos=(237, Y[0] + 26))
    path([(X[0] + BW, Y[1] + 20), (X[1] - 2, Y[0] + BH - 8)], label="", lpos=(0, 0))
    # antibody -| VEGF
    path([(X[2], Y[0] + 32), (X[1] + BW + 3, Y[0] + 32)], col="#b22", inhib=True, label="neutralises", lpos=(477, Y[0] + 26))
    # VEGF -> b
    path([(cx(1), Y[0] + BH), (cx(1), Y[1] - 2)], label="sprouting", lpos=(cx(1) + 6, Y[0] + BH + 40), anchor="start")
    # b -> tumour O2
    path([(X[1], Y[1] + 44), (X[0] + BW + 2, Y[1] + 44)], label="O₂ → growth", lpos=(237, Y[1] + 60))
    # b -> m
    path([(X[1] + BW, Y[1] + 44), (X[2] - 2, Y[1] + 44)], label="entry ∝ b", lpos=(477, Y[1] + 60))
    # m -> VEGF and VEGF -| m
    path([(X[2] + 30, Y[1]), (X[1] + BW - 20, Y[0] + BH + 2)], label="VEGF", lpos=(X[2] + 8, Y[0] + BH + 30), anchor="start")
    path([(X[1] + BW, Y[0] + BH - 14), (X[2] + 70, Y[1] - 3)], col="#b22", dash="4,3", inhib=True,
         label="anergy ψ(v)", lpos=(X[2] + 72, Y[0] + BH + 52), anchor="start")
    # killing m -| tumour (routed below row 2)
    yk = Y[1] + BH + 26
    path([(cx(2), Y[1] + BH), (cx(2), yk), (X[0] + 130, yk), (X[0] + 130, Y[1] + BH + 3)], col="#b22", inhib=True,
         label="cytotoxic killing (τ0 + τAΓ); inactivation βK", lpos=(cx(1), yk - 6))
    # satellites -> chemokine
    path([(X[0] + 45, Y[1] + BH), (X[0] + 45, Y[2] - 2)], label="", lpos=(0, 0))
    # chemokine -> m (chemotaxis)
    yc = Y[2] + 32
    path([(X[0] + BW, yc), (X[1] + BW + 40, yc), (X[1] + BW + 40, Y[1] + BH + 2 + 40), (X[2] + 20, Y[1] + BH + 2)],
         col="#555", label="chemotaxis, recruitment", lpos=(cx(1), yc - 6))
    # priming -> m
    path([(cx(2) + 40, Y[2]), (cx(2) + 40, Y[1] + BH + 2)], col="#555", label="primed influx", lpos=(cx(2) + 34, Y[2] - 20), lcol="#555", anchor="end")
    o.append(f"<text x='30' y='{Y[2] + BH + 22}' font-size='10.5' fill='#444'>Red bars: inhibition. Surgery resets all fields inside "
             "radius rp + w; checkpoint blockade multiplies kill capacity by (1 + g).</text>")
    # panel B geometry
    o.append("<text x='712' y='24' font-size='15' font-weight='bold'>B</text>")
    gx, gy, R = 800, 200, 85
    o.append(f"<rect x='{gx - 88}' y='{gy - 150}' width='176' height='300' fill='#fff8f2' stroke='#333'/>")
    o.append(f"<circle cx='{gx}' cy='{gy}' r='{R * 0.38}' fill='#1b4f9c' opacity='0.85'/>")
    o.append(f"<circle cx='{gx}' cy='{gy}' r='{R * 0.62}' fill='none' stroke='#d1495b' stroke-width='1.8' stroke-dasharray='6,4'/>")
    import random
    rnd = random.Random(4)
    for _ in range(16):
        ang = rnd.uniform(0, 2 * math.pi)
        r = R * 0.38 + rnd.expovariate(1 / 22.0)
        x, y = gx + r * math.cos(ang), gy + r * math.sin(ang)
        if abs(x - gx) < 82 and abs(y - gy) < 120:
            o.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='3.2' fill='#00a6a6' stroke='#035' stroke-width='0.6'/>")
    o.append(f"<text x='{gx}' y='{gy + 4}' text-anchor='middle' font-size='10' fill='white'>primary</text>")
    o.append(f"<text x='{gx}' y='{gy + 128}' text-anchor='middle' font-size='10' fill='#d1495b'>- - excision radius rp + w</text>")
    o.append(f"<text x='{gx}' y='{gy + 143}' text-anchor='middle' font-size='10'>40 × 40 mm dermal sheet</text>")
    o.append(f"<circle cx='{gx - 70}' cy='{gy - 135}' r='3.2' fill='#00a6a6' stroke='#035' stroke-width='0.6'/>"
             f"<text x='{gx - 62}' y='{gy - 131}' font-size='10'>satellite seed</text>")
    # timeline
    y0 = 468
    x0, x1, tmax = 40, 860, 1825
    tx = lambda t: x0 + (x1 - x0) * t / tmax
    o.append(f"<text x='{x0}' y='{y0 - 24}' font-size='10.5' font-weight='bold'>Treatment timeline (days)</text>")
    o.append(f"<line x1='{x0}' x2='{x1 + 10}' y1='{y0}' y2='{y0}' stroke='#333' stroke-width='1.4' marker-end='url(#arr)'/>")
    o.append(f"<rect x='{tx(393)}' y='{y0 - 6}' width='{tx(758) - tx(393)}' height='12' fill='#f2c14e' opacity='0.4'/>")
    marks = [(0, "0", 1, "middle"), (302, "302 neoadjuvant ", -1, "end"), (365, "365 surgery", 1, "middle"),
             (393, " 393 adjuvant", -1, "start"), (758, "758 end of 1-yr course", 1, "middle"), (1825, "1825", 1, "middle")]
    for t, lab, side, anc in marks:
        x = tx(t)
        ly = y0 + 18 if side > 0 else y0 - 9
        o.append(f"<line x1='{x}' x2='{x}' y1='{y0 - 5}' y2='{y0 + 5}' stroke='#333'/>"
                 f"<text x='{x}' y='{ly}' font-size='9.5' text-anchor='{anc}'>{lab}</text>")
    save("fig1_schematic", W, H + 22, "\n".join(o))


# ---------------------------------------------------------------- Figure 2
def fig2():
    times = [364, 450, 520, 600, 750]
    rows = [("A_R1", "T", "Surgery alone: tumour density"), ("A_R1", "b", "Surgery alone: microvessel density"),
            ("A_R2", "T", "1-yr anti-VEGF: tumour density"), ("A_R2", "b", "1-yr anti-VEGF: microvessel density")]
    cw, gap, top, left = 150, 10, 40, 70
    W = left + len(times) * (cw + gap) + 90
    H = top + len(rows) * (cw + 34) + 10
    o = []
    for ri, (name, fld, lab) in enumerate(rows):
        y = top + ri * (cw + 34)
        o.append(f"<text x='{left}' y='{y - 8}' font-size='11.5' font-weight='bold'>{'ABCD'[ri]}  {lab}</text>")
        for ci, t in enumerate(times):
            d, n = snap("representative", name, t)
            # crop central 30 mm
            lo, hi = int(n * 0.125), int(n * 0.875)
            if fld == "T":
                g = [[d["c"][j][i] + d["s"][j][i] for i in range(lo, hi)] for j in range(lo, hi)]
                img = sp.heatmap_image(g, 0, 0.6, left + ci * (cw + gap), y, cw, cw, "viridis")
            else:
                g = [[d["b"][j][i] for i in range(lo, hi)] for j in range(lo, hi)]
                img = sp.heatmap_image(g, 1.0, 4.0, left + ci * (cw + gap), y, cw, cw, "magma")
            o.append(img)
            if ri == 0:
                o.append(f"<text x='{left + ci * (cw + gap) + cw / 2}' y='{top - 24}' text-anchor='middle' font-size='11'>day {t}</text>")
        if fld == "T":
            o.append(sp.colorbar(left + len(times) * (cw + gap) + 4, y, 12, cw, 0, 0.6, "T = c + s", "viridis", ticks=[0, 0.2, 0.4, 0.6]))
        else:
            o.append(sp.colorbar(left + len(times) * (cw + gap) + 4, y, 12, cw, 1, 4, "b", "magma", ticks=[1, 2, 3, 4]))
    o.append(f"<text x='{left}' y='{H - 4}' font-size='10' fill='#444'>Each panel shows the central 30 × 30 mm of the domain; surgery on day 365.</text>")
    save("fig2_snapshots", W, H + 6, "\n".join(o))


# ---------------------------------------------------------------- Figure 3
def fig3():
    W, H = 900, 360
    o = []
    for pi, p in enumerate(("A", "B")):
        ax = sp.Axes(80 + pi * 440, 40, 350, 250, (0, 1825), (1e3, 1e9), ylog=True, xlabel="Time (days)",
                     ylabel="Total tumour burden (cells)" if pi == 0 else "",
                     title=f"Phenotype {p}: {'weak' if p == 'A' else 'strong'} VEGF immunosuppression", letter="AB"[pi])
        ax.span(393, 758, label="1-yr course")
        ax.vline(T_S, label="surgery")
        for r in ("R0", "R1", "R2", "R3", "R4"):
            d = ts("representative", f"{p}_{r}")
            ax.line([x["t"] for x in d], [x["M_c"] + x["M_s"] for x in d], color=REG_COL[r], dash=REG_DASH[r], label=REG_LABEL[r])
        ax.hline(1e7, color="#999", dash="2,2", label="major recurrence")
        ax.hline(1e6, color="#bbb", dash="2,2", label="detection")
        if pi == 1:
            ax.legend(x=ax.x + 140, y=ax.y + 150, size=9.5)
        o.append(ax.render())
    save("fig3_burden", W, H, "\n".join(o))


# ---------------------------------------------------------------- Figure 4
def fig4():
    W, H = 900, 640
    o = []
    p = "B"
    runs = {r: ts("representative", f"{p}_{r}") for r in ("R1", "R2", "R3")}
    axs = []
    ax = sp.Axes(90, 40, 330, 210, (300, 1300), (0, 400), xlabel="Time (days)", ylabel="Plasma antibody (µg/mL)",
                 title="Plasma pharmacokinetics", letter="A")
    for r in ("R2", "R3"):
        d = runs[r]
        ax.line([x["t"] for x in d], [x["Cp"] * UG_PER_ML for x in d], color=REG_COL[r], dash=REG_DASH[r], label=REG_LABEL[r], width=1.2)
    ax.vline(T_S)
    ax.legend(x=ax.x + 110, y=ax.y + 10, size=9.5)
    axs.append(ax)
    ax = sp.Axes(540, 40, 330, 210, (300, 1300), (1e-4, 1), ylog=True, xlabel="Time (days)", ylabel="Free VEGF in tumour (v / φv)",
                 title="Tumour free VEGF", letter="B")
    for r in ("R1", "R2", "R3"):
        d = runs[r]
        ax.line([x["t"] for x in d], [x["vfree_tumor"] if x["vfree_tumor"] > 0 else None for x in d], color=REG_COL[r], dash=REG_DASH[r], label=REG_LABEL[r])
    ax.vline(T_S)
    axs.append(ax)
    nmax = max(x["neovasc"] for r in runs for x in runs[r] if 300 <= x["t"] <= 1300)
    ax = sp.Axes(90, 360, 330, 210, (300, 1300), (0, sp.nice_ticks(0, nmax * 1.05)[-1] + (sp.nice_ticks(0, nmax)[1] if nmax > 0 else 1)), xlabel="Time (days)", ylabel="Neovascular area ∫(b−1) dx (mm²)",
                 title="Tumour neovasculature", letter="C")
    for r in ("R1", "R2", "R3"):
        d = runs[r]
        ax.line([x["t"] for x in d], [x["neovasc"] for x in d], color=REG_COL[r], dash=REG_DASH[r], label=REG_LABEL[r])
    ax.vline(T_S)
    ax.legend(x=ax.x + 8, y=ax.y + 8, size=9.5)
    axs.append(ax)
    rmax = max(x["recruit"] for r in runs for x in runs[r] if 300 <= x["t"] <= 1300)
    ax = sp.Axes(540, 360, 330, 210, (300, 1300), (0, round(rmax * 1.1, 1) + 0.1), xlabel="Time (days)", ylabel="Immune recruitment (mm² day⁻¹)",
                 title="Vessel-dependent immune recruitment", letter="D")
    for r in ("R1", "R2", "R3"):
        d = runs[r]
        ax.line([x["t"] for x in d], [x["recruit"] for x in d], color=REG_COL[r], dash=REG_DASH[r], label=REG_LABEL[r])
    ax.vline(T_S)
    axs.append(ax)
    o = [a.render() for a in axs]
    save("fig4_pkpd", W, H, "\n".join(o))


# ---------------------------------------------------------------- Figure 5
def fig5():
    W, H = 900, 640
    rep = SUM["replicates"]
    o = []
    for pi, p in enumerate(("A", "B")):
        for ei, (ep, lab) in enumerate((("km_det", "detectable recurrence (≥10⁶ cells)"), ("km_major", "major recurrence (≥10⁷ cells)"))):
            ax = sp.Axes(90 + ei * 450, 40 + pi * 310, 340, 220, (0, 1460), (0, 1.02), xlabel="Days after surgery",
                         ylabel="Fraction free of event", title=f"Phenotype {p}: {lab}", letter="ABCD"[pi * 2 + ei],
                         yticks=[0, 0.25, 0.5, 0.75, 1.0])
            for r in ("R1", "R2", "R3", "R4"):
                xs, ys = rep[f"{p}_{r}"][ep]
                ax.line(xs, ys, color=REG_COL[r], dash=REG_DASH[r], label=REG_LABEL[r], step=True, width=1.8)
            if pi == 0 and ei == 1:
                ax.legend(x=ax.x + 120, y=ax.y + 10, size=9.5)
            o.append(ax.render())
    save("fig5_km", W, H, "\n".join(o))


# ---------------------------------------------------------------- Figure 6
def fig6():
    W, H = 900, 350
    o = []
    dose = SUM["dose"]
    fr = [1.0, 0.1, 0.01, 0.003, 0.001, 0.0003, 0.0001, 0.00003]
    ax = sp.Axes(90, 40, 330, 230, (2e-5, 1.5), (1e6, 1e9), xlog=True, ylog=True, xlabel="Dose fraction of 7.5 mg/kg q3w",
                 ylabel="Tumour burden at day 1825 (cells)", title="Continuous adjuvant: dose response", letter="A")
    for p, col in (("A", "#1b4f9c"), ("B", "#d1495b")):
        ys = [dose[f"{p}_d{f:g}"]["final"] for f in fr]
        ax.line(fr, ys, color=col, label=f"Phenotype {p}", marker=True)
        ax.hline(SUM["representative"][f"{p}_R1"]["final"], color=col, dash="3,3")
    ax.legend(x=ax.x + 10, y=ax.y + 10, size=9.5)
    o.append(ax.render())
    dur = SUM["duration"]
    months = [0, 3, 6, 12, 24, 36, 48]
    ax = sp.Axes(540, 40, 330, 230, (0, 48), (1e6, 1e9), ylog=True, xlabel="Adjuvant duration (months)",
                 ylabel="Tumour burden at day 1825 (cells)", title="Treatment duration", letter="B", xticks=[0, 6, 12, 24, 36, 48])
    for p, col in (("A", "#1b4f9c"), ("B", "#d1495b")):
        ax.line(months, [dur[f"{p}_m{m}"]["final"] for m in months], color=col, label=f"Phenotype {p}: final", marker=True)
        ax.line(months, [dur[f"{p}_m{m}"]["peak"] for m in months], color=col, dash="4,3", label=f"Phenotype {p}: post-op peak")
    ax.legend(x=ax.x + 10, y=ax.y + 140, size=9.5)
    o.append(ax.render())
    save("fig6_dose_duration", W, H, "\n".join(o))


# ---------------------------------------------------------------- Figure 7
SENS_LABEL = {"alpha_c": "αc (proliferation)", "lambda_sigma": "λσ (O₂ demand)", "kappa_n": "κn (co-option)",
              "gamma_v": "γv (constitutive VEGF)", "alpha_v": "αv (hypoxic VEGF)", "gamma_vm": "γvm (immune VEGF)",
              "alpha_b": "αb (sprouting)", "q_m": "qm (recruitment)", "beta_K": "βK (inactivation)",
              "tau_A": "τA (kill capacity)", "beta_P": "βP (priming decay)", "K_D": "KD (affinity)"}


def benefit(sens, k):
    r1, r3 = sens[k + "_R1"], sens[k + "_R3"]
    if r1["auc"] <= 0:
        return None
    return 100 * (1 - r3["auc"] / r1["auc"])


def fig7():
    sens = SUM["sensitivity"]
    base = benefit(sens, "base")
    keys = ["alpha_c", "lambda_sigma", "kappa_n", "gamma_v", "alpha_v", "gamma_vm", "alpha_b", "q_m", "beta_K", "tau_A", "beta_P", "K_D"]
    rows = []
    for k in keys:
        lo = benefit(sens, f"{k}_lo") if f"{k}_lo_R1" in sens else None
        hi = benefit(sens, f"{k}_hi") if f"{k}_hi_R1" in sens else None
        spread = max(abs((lo if lo is not None else base) - base), abs((hi if hi is not None else base) - base))
        rows.append((spread, k, lo, hi))
    rows.sort(reverse=True)
    W, H = 760, 440
    ax = sp.Axes(220, 40, 480, 340, (-20, 100), (0, 1), xlabel="Reduction in post-operative tumour burden AUC (%)",
                 title="One-at-a-time sensitivity of continuous adjuvant benefit (phenotype A)")
    ax.bars_h([SENS_LABEL[k] for _, k, _, _ in rows], [lo for _, _, lo, _ in rows], [hi for _, _, _, hi in rows], base)
    o = [ax.render(frame=True, ticks=False)]
    for v in (-20, 0, 20, 40, 60, 80, 100):
        px = ax._tx(v)
        o.append(f"<line x1='{px}' x2='{px}' y1='{ax.y + ax.h}' y2='{ax.y + ax.h + 4}' stroke='#222'/>"
                 f"<text x='{px}' y='{ax.y + ax.h + 15}' font-size='10' text-anchor='middle'>{v}</text>")
    o.append(f"<rect x='{ax.x + 300}' y='{ax.y + ax.h - 50}' width='12' height='10' fill='#1b4f9c'/><text x='{ax.x + 318}' y='{ax.y + ax.h - 41}' font-size='10'>parameter × 0.5</text>")
    o.append(f"<rect x='{ax.x + 300}' y='{ax.y + ax.h - 34}' width='12' height='10' fill='#d1495b'/><text x='{ax.x + 318}' y='{ax.y + ax.h - 25}' font-size='10'>parameter × 1.5</text>")
    o.append(f"<text x='{ax._tx(base) + 4}' y='{ax.y + 12}' font-size='10'>baseline {base:.0f}%</text>")
    save("fig7_sensitivity", W, H, "\n".join(o))
    return base, rows


# ---------------------------------------------------------------- Figure 8
def fig8():
    comb = SUM["combination"]
    gains = [0.0, 0.25, 0.5, 0.6, 0.75, 1.0]
    W, H = 900, 340
    o = []
    for pi, p in enumerate(("A", "B")):
        ax = sp.Axes(90 + pi * 450, 40, 330, 220, (0, 1.0), (1e3, 3e11), ylog=True, xlabel="Checkpoint-blockade kill gain g",
                     ylabel="Post-operative burden AUC (cell·days)", title=f"Phenotype {p}", letter="AB"[pi],
                     xticks=[0, 0.25, 0.5, 0.75, 1.0])
        ax.line(gains, [max(comb[f"{p}_g{g:g}_R1"]["auc"], 1e3) for g in gains], color="#3d3d3d", marker=True, label="Checkpoint blockade alone")
        ax.line(gains, [max(comb[f"{p}_g{g:g}_R2"]["auc"], 1e3) for g in gains], color="#1b4f9c", dash="5,3", marker=True, label="+ 1-yr anti-VEGF")
        ax.legend(x=ax.x + 130, y=ax.y + 10, size=9.5)
        o.append(ax.render())
    save("fig8_combination", W, H, "\n".join(o))


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); base, rows = fig7(); fig8()
    print("sensitivity baseline benefit %.1f%%" % base)
    for spread, k, lo, hi in rows:
        print(f"  {k:14s} lo={lo if lo is None else round(lo, 1)} hi={hi if hi is None else round(hi, 1)} spread={spread:.1f}")
    print("figures written to", FIG)
