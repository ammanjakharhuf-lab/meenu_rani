#!/usr/bin/env python3
"""Summarise simulation time series into outcome metrics (stdlib only)."""
import csv
import sys

T_SURG = 365.0
M_DET = 1e6


def load(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    return [{k: float(v) for k, v in r.items()} for r in rows]


def metrics(path, t_surg=T_SURG, m_det=M_DET):
    ts = load(path)
    pre = [r for r in ts if r["t"] < t_surg]
    post = [r for r in ts if r["t"] > t_surg]
    at_s = pre[-1] if pre else ts[0]
    t_rec = None
    for r in post:
        if r["M_c"] + r["M_s"] >= m_det:
            t_rec = r["t"] - t_surg
            break
    peak = max((r["M_c"] + r["M_s"] for r in post), default=0.0)
    final = ts[-1]["M_c"] + ts[-1]["M_s"]
    auc = sum((r["M_c"] + r["M_s"]) for r in post) * 1.0  # cell-days (dt_out = 1 day)
    return {
        "Mc_at_surgery": at_s["M_c"],
        "Ms_at_surgery": at_s["M_s"],
        "n_sat": int(ts[-1]["n_sat"]),
        "t_rec": t_rec,
        "peak_post": peak,
        "final": final,
        "auc_post": auc,
    }


if __name__ == "__main__":
    for p in sys.argv[1:]:
        m = metrics(p)
        tr = "none" if m["t_rec"] is None else f"{m['t_rec']:.0f}"
        print(f"{p}: Mc(ts)={m['Mc_at_surgery']:.2e} Ms(ts)={m['Ms_at_surgery']:.2e} nsat={m['n_sat']} "
              f"t_rec={tr} peak={m['peak_post']:.2e} final={m['final']:.2e} auc={m['auc_post']:.2e}")
