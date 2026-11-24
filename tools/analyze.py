#!/usr/bin/env python3
"""Compute outcome metrics for every experiment and write results/summary.json."""
import csv
import json
import os
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "model"))
T_S = 365.0
M_DET, M_MAJOR = 1e6, 1e7
HORIZON = 1825.0


def load(path):
    with open(path) as f:
        return [{k: float(v) for k, v in r.items()} for r in csv.DictReader(f)]


def first_cross(ts, thr):
    for r in ts:
        if r["t"] > T_S and r["M_c"] + r["M_s"] >= thr:
            return r["t"] - T_S
    return None


def metrics(prefix):
    ts = load(prefix + "_ts.csv")
    pre = [r for r in ts if r["t"] < T_S]
    post = [r for r in ts if r["t"] > T_S]
    at_s = pre[-1]
    tot = [r["M_c"] + r["M_s"] for r in post]
    seeds_removed = 0
    seeds_total = 0
    re = None
    with open(prefix + "_events.csv") as f:
        ev = list(csv.DictReader(f))
    for e in ev:
        if e["type"] == "surgery":
            re = float(e["dist_from_edge"])
    for e in ev:
        if e["type"] == "seed" and float(e["t"]) < T_S:
            seeds_total += 1
            r = ((float(e["x"]) - 20) ** 2 + (float(e["y"]) - 20) ** 2) ** 0.5
            if re is not None and r <= re:
                seeds_removed += 1
    return {
        "Mc_surg": at_s["M_c"], "Ms_surg": at_s["M_s"], "rp_surg": at_s["r_p"],
        "t_det": first_cross(ts, M_DET), "t_major": first_cross(ts, M_MAJOR),
        "peak": max(tot) if tot else 0.0, "final": ts[-1]["M_c"] + ts[-1]["M_s"],
        "final_c": ts[-1]["M_c"], "final_s": ts[-1]["M_s"],
        "auc": sum(tot), "seeds": seeds_total, "seeds_removed": seeds_removed,
        "resection_radius": re,
    }


def manifest(exp):
    with open(os.path.join(ROOT, "runs", exp, "manifest.csv")) as f:
        return [r["name"] for r in csv.DictReader(f)]


def km(times, horizon):
    """Kaplan-Meier with administrative censoring at horizon (no other censoring)."""
    n = len(times)
    ev = sorted(t for t in times if t is not None and t <= horizon)
    xs, ys = [0.0], [1.0]
    at_risk = n
    s = 1.0
    i = 0
    while i < len(ev):
        t = ev[i]
        d = 0
        while i < len(ev) and ev[i] == t:
            d += 1
            i += 1
        s *= (at_risk - d) / at_risk
        at_risk -= d
        xs.append(t)
        ys.append(s)
    xs.append(horizon)
    ys.append(s)
    return xs, ys


def median_time(times):
    vals = sorted(t for t in times if t is not None)
    n = len(times)
    if len(vals) < (n + 1) / 2:
        return None
    return vals[(n + 1) // 2 - 1] if n % 2 else vals[n // 2 - 1]


def main():
    out = {}
    for exp in ("representative", "dose", "duration", "sensitivity", "margin", "combination"):
        d = os.path.join(ROOT, "runs", exp)
        out[exp] = {n: metrics(os.path.join(d, n)) for n in manifest(exp)}
    # replicates
    d = os.path.join(ROOT, "runs", "replicates")
    names = sorted(set(manifest("replicates")))
    rep = {n: metrics(os.path.join(d, n)) for n in names}
    out["replicates_raw"] = rep
    agg = {}
    hz = HORIZON - T_S
    for p in ("A", "B"):
        for r in ("R1", "R2", "R3", "R4"):
            runs = [v for k, v in rep.items() if k.startswith(f"{p}_{r}_s")]
            if not runs:
                continue
            tdet = [v["t_det"] for v in runs]
            tmaj = [v["t_major"] for v in runs]
            agg[f"{p}_{r}"] = {
                "n": len(runs),
                "median_t_det": median_time(tdet),
                "median_t_major": median_time(tmaj),
                "frac_free_det": sum(1 for t in tdet if t is None) / len(runs),
                "frac_free_major": sum(1 for t in tmaj if t is None) / len(runs),
                "peak_mean": st.mean(v["peak"] for v in runs),
                "peak_sd": st.pstdev(v["peak"] for v in runs),
                "final_mean": st.mean(v["final"] for v in runs),
                "final_sd": st.pstdev(v["final"] for v in runs),
                "auc_mean": st.mean(v["auc"] for v in runs),
                "auc_sd": st.pstdev(v["auc"] for v in runs),
                "Mc_surg_mean": st.mean(v["Mc_surg"] for v in runs),
                "Ms_surg_mean": st.mean(v["Ms_surg"] for v in runs),
                "seeds_mean": st.mean(v["seeds"] for v in runs),
                "seeds_removed_mean": st.mean(v["seeds_removed"] for v in runs),
                "km_det": km(tdet, hz), "km_major": km(tmaj, hz),
            }
    out["replicates"] = agg
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "summary.json"), "w") as f:
        json.dump(out, f, indent=1)

    def f(v):
        return "none" if v is None else (f"{v:.3g}" if isinstance(v, float) else str(v))
    for exp in ("representative", "dose", "duration", "margin", "combination", "sensitivity"):
        print(f"## {exp}")
        for n, m in out[exp].items():
            print(f"  {n:22s} Mc_s={f(m['Mc_surg'])} Ms_s={f(m['Ms_surg'])} tdet={f(m['t_det'])} tmaj={f(m['t_major'])} "
                  f"peak={f(m['peak'])} final={f(m['final'])} (c={f(m['final_c'])}) auc={f(m['auc'])} seeds={m['seeds']}/{m['seeds_removed']} re={f(m['resection_radius'])}")
    print("## replicates")
    for k, a in agg.items():
        print(f"  {k}: n={a['n']} med_det={f(a['median_t_det'])} med_major={f(a['median_t_major'])} free_det={a['frac_free_det']:.2f} "
              f"free_major={a['frac_free_major']:.2f} peak={a['peak_mean']:.3g}±{a['peak_sd']:.2g} final={a['final_mean']:.3g}±{a['final_sd']:.2g} "
              f"auc={a['auc_mean']:.3g}±{a['auc_sd']:.2g} Mc_s={a['Mc_surg_mean']:.3g} Ms_s={a['Ms_surg_mean']:.3g} seeds={a['seeds_mean']:.1f} removed={a['seeds_removed_mean']:.1f}")


if __name__ == "__main__":
    main()
