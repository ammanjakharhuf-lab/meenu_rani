#!/usr/bin/env python3
"""Run every simulation experiment reported in the manuscript (stdlib only).

Usage: python3 model/experiments.py [experiment ...]   (default: all)
Outputs go to runs/<experiment>/ ; a manifest.csv lists run name and arguments.
"""
import concurrent.futures as cf
import csv
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(ROOT, "build", "melanoma_vegf")
PARAMS = os.path.join(ROOT, "model", "base_params.txt")

T_S = 365
START = T_S + 28                      # adjuvant start 4 weeks after surgery (wound healing)
NEO = T_S - 63                        # three q3w doses before surgery
PHENO = {"A": "v_I=1.0", "B": "v_I=0.1"}  # A: weak, B: strong VEGF-mediated immunosuppression


def drug(start, stop, frac=1.0):
    return f"dose_frac={frac} drug_start={start} drug_stop={stop}"


REGIMENS = {
    "R0": "t_surgery=1e9",                                  # no treatment
    "R1": "",                                               # surgery alone
    "R2": drug(START, START + 365),                         # 1-year adjuvant (AVAST-M-like)
    "R3": drug(START, 1e9),                                 # continuous adjuvant
    "R4": drug(NEO, START + 365),                           # neoadjuvant + 1-year adjuvant
}


def run(job):
    name, args, outdir = job
    cmd = [BIN, PARAMS, f"out={os.path.join(outdir, name)}"] + args.split()
    env = dict(os.environ, OMP_NUM_THREADS="1")
    subprocess.run(cmd, check=True, env=env, stdout=subprocess.DEVNULL)
    return name


def execute(exp, jobs):
    outdir = os.path.join(ROOT, "runs", exp)
    os.makedirs(outdir, exist_ok=True)
    mpath = os.path.join(outdir, "manifest.csv")
    new = not os.path.exists(mpath)
    with open(mpath, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["name", "args"])
        for n, a in jobs:
            w.writerow([n, a])
    with cf.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
        list(ex.map(run, [(n, a, outdir) for n, a in jobs]))
    print(f"{exp}: {len(jobs)} runs done")


def exp_representative():
    snaps = "snapshots=300,364,450,520,600,750,1000"
    jobs = []
    for p, pa in PHENO.items():
        for r, ra in REGIMENS.items():
            jobs.append((f"{p}_{r}", f"{pa} {ra} {snaps}"))
    return jobs


def exp_replicates():
    lo = int(os.environ.get("REP_FROM", 1))
    hi = int(os.environ.get("REP_TO", 20))
    jobs = []
    for p, pa in PHENO.items():
        for r in ("R1", "R2", "R3", "R4"):
            for sd in range(lo, hi + 1):
                jobs.append((f"{p}_{r}_s{sd}", f"{pa} {REGIMENS[r]} seed={sd}"))
    return jobs


def exp_dose():
    jobs = []
    for p, pa in PHENO.items():
        for fr in (1.0, 0.1, 0.01, 0.003, 0.001, 0.0003, 0.0001, 0.00003):
            jobs.append((f"{p}_d{fr:g}", f"{pa} {drug(START, 1e9, fr)}"))
    return jobs


def exp_duration():
    jobs = []
    for p, pa in PHENO.items():
        for months in (0, 3, 6, 12, 24, 36, 48):
            a = pa if months == 0 else f"{pa} {drug(START, START + months * 30.4)}"
            jobs.append((f"{p}_m{months}", a))
    return jobs


SENS = ["alpha_c", "lambda_sigma", "kappa_n", "gamma_v", "alpha_v", "gamma_vm", "alpha_b",
        "q_m", "beta_K", "tau_A", "beta_P", "K_D"]


def base_value(key):
    with open(PARAMS) as f:
        for line in f:
            line = line.split("#")[0]
            if "=" in line:
                k, v = (x.strip() for x in line.split("=", 1))
                if k == key:
                    return float(v)
    raise KeyError(key)


def exp_sensitivity():
    jobs = [("base_R1", PHENO["A"]), ("base_R3", f"{PHENO['A']} {REGIMENS['R3']}")]
    for k in SENS:
        b = base_value(k)
        for tag, f in (("lo", 0.5), ("hi", 1.5)):
            val = b * f
            if k == "kappa_n":
                val = min(val, 1.0) if f < 1 else 1.0  # kappa_n is a fraction; only lower it
                if f > 1:
                    continue
            jobs.append((f"{k}_{tag}_R1", f"{PHENO['A']} {k}={val:g}"))
            jobs.append((f"{k}_{tag}_R3", f"{PHENO['A']} {k}={val:g} {REGIMENS['R3']}"))
    return jobs


def exp_margin():
    jobs = []
    for mg in (0.5, 1.0, 2.0, 3.0, 4.0):
        for r in ("R1", "R4"):
            jobs.append((f"w{mg:g}_{r}", f"{PHENO['A']} margin={mg} {REGIMENS[r]}"))
    return jobs


def exp_combination():
    jobs = []
    for g in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0):
        io = f"io_start={START} io_stop={START + 365} io_gain={g}"
        for p, pa in PHENO.items():
            jobs.append((f"{p}_g{g:g}_R1", f"{pa} {io}"))
            jobs.append((f"{p}_g{g:g}_R2", f"{pa} {io} {REGIMENS['R2']}"))
    return jobs


def exp_late_io():
    jobs = []
    for st in (480, 540, 600):
        io = f"io_start={st} io_stop={st + 365} io_gain=1"
        jobs.append((f"A_io{st}_R1", f"{PHENO['A']} {io}"))
        jobs.append((f"A_io{st}_R2", f"{PHENO['A']} {io} {REGIMENS['R2']}"))
    return jobs


EXPERIMENTS = {
    "representative": exp_representative,
    "replicates": exp_replicates,
    "dose": exp_dose,
    "duration": exp_duration,
    "sensitivity": exp_sensitivity,
    "margin": exp_margin,
    "combination": exp_combination,
    "late_io": exp_late_io,
}

if __name__ == "__main__":
    wanted = sys.argv[1:] or list(EXPERIMENTS)
    for e in wanted:
        execute(e, EXPERIMENTS[e]())
