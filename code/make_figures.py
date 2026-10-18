# -*- coding: utf-8 -*-
"""Regenerates the two English figures of the disulfide-trigger analysis.

Self-contained: all measured constants are embedded. Run from anywhere:

    python code/make_figures.py

Writes figures/d1_potential_axis.png and figures/d1_nernst_backcalculation.png
relative to the repository root. Dependencies: numpy, matplotlib.
Data provenance: data/foldx_ev_raw_1oro_constructs.tsv (the five-model FoldX
results; the ev/ec arrays below are its E(V) / E_combined columns in mV).
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

FIG = Path(__file__).resolve().parents[1] / "figures"

# FoldX five-model consensus (mV), from data/foldx_ev_raw_1oro_constructs.tsv
ev = np.array([-0.28242, -0.281006, -0.277349, -0.28128, -0.287471]) * 1000
ec = np.array([-0.346943, -0.345789, -0.342333, -0.346299, -0.350688]) * 1000

# ── Figure 1: compartment potentials vs threshold ──────────────────────────
fig, ax = plt.subplots(figsize=(9.2, 4.6), dpi=300)
comps = [
    ("Plasma / extracellular", -130, -40, "#c9d8e8"),
    ("Endoplasmic reticulum", -230, -170, "#f2d3b3"),
    ("Cytosol", -320, -260, "#b7d8b7"),
    ("Nucleus", -320, -260, "#a8cfa8"),
    ("Mitochondrial matrix", -360, -300, "#d8b8c8"),
]
ys = np.arange(len(comps))[::-1]
for (name, lo, hi, c), y in zip(comps, ys):
    ax.barh(y, hi - lo, left=lo, height=0.52, color=c, edgecolor="#555", linewidth=0.6)
    ax.text(lo - 8, y, f"{lo}", ha="right", va="center", fontsize=8.5, color="#333")
    ax.text(hi + 8, y, f"{hi}", ha="left", va="center", fontsize=8.5, color="#333")
    ax.text(30, y, name, ha="left", va="center", fontsize=10)

ax.axvline(ev.mean(), color="#b96d55", linestyle="--", linewidth=1.4)
ax.text(ev.mean() + 8, len(comps) - 0.55,
        f"This design's threshold E(V) ≈ {ev.mean():.0f} mV\n(FoldX, Cys→Ser, 5-model consensus)",
        ha="left", va="bottom", fontsize=8.6, color="#b96d55")
ax.axvline(ec.mean(), color="#123d43", linestyle="--", linewidth=1.4)
ax.text(ec.mean() - 8, len(comps) - 0.55 - 0.62,
        f"Combined estimate E_c ≈ {ec.mean():.0f} mV\n(entropic + solvation corrections)",
        ha="right", va="bottom", fontsize=8.6, color="#123d43")

ax.set_xlim(-420, 130)
ax.set_yticks([])
ax.set_xlabel("Compartment redox potential $E_h$ (mV vs NHE) — more negative = more reducing", fontsize=10)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.set_title("Compartment potentials vs. the disulfide breaking threshold:\n"
             "the compartment-selectivity case for a GSH-responsive switch", fontsize=11, pad=20)
fig.text(0.13, 0.015,
         "Compartment ranges are literature-derived summary values (Schafer & Buettner 2001; Hwang 1992; "
         "Montero 2013), shown schematically.",
         fontsize=7.2, color="#666")
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig(FIG / "d1_potential_axis.png")
plt.close(fig)

# ── Figure 2: Nernst back-calculation ──────────────────────────────────────
E0, COEF, GSH_CYT = -240.0, 29.58, 7e-3  # mV, mV/decade, M (HeLa-like cytosol)


def ratio_needed(e_target_mv, gsh=GSH_CYT):
    gsh2_gssg = 10 ** ((E0 - e_target_mv) / COEF)
    gssg = gsh ** 2 / gsh2_gssg
    return gsh / gssg


r1, r2 = ratio_needed(ev.mean()), ratio_needed(ec.mean())
fig, ax = plt.subplots(figsize=(8.6, 4.2), dpi=300)
bars = [
    ("Physiological cytosol/nucleus\n(30:1 – 100:1)", 30, 100, "#1c7770"),
    ("Needed to reach E(V)\n(−282 mV)", r1, r1, "#b96d55"),
    ("Needed to reach E_combined\n(−346 mV)", r2, r2, "#123d43"),
]
for i, (lab, lo, hi, c) in enumerate(bars):
    if lo == hi:
        ax.bar(i, hi, width=0.52, color=c, edgecolor="#555", linewidth=0.6)
        ax.text(i, hi * 1.3, f"≈ {hi:.1e} : 1", ha="center", fontsize=9.5)
    else:
        ax.bar(i, hi, width=0.52, color=c, edgecolor="#555", linewidth=0.6, alpha=0.45)
        ax.bar(i, lo, width=0.52, color=c, edgecolor="#555", linewidth=0.6)
        ax.text(i, hi * 1.3, f"{lo:.0f}–{hi:.0f} : 1", ha="center", fontsize=9.5)
ax.set_yscale("log")
ax.set_ylim(10, 3e6)
ax.set_xticks(range(3), [b[0] for b in bars], fontsize=9.5)
ax.set_ylabel("Required GSH : GSSG ratio (log axis)", fontsize=10)
ax.set_title("What it takes to force the switch open in HeLa-like cytosol ([GSH] ≈ 7 mM):\n"
             "Nernst back-calculation, E_h = −240 mV − 29.58·lg([GSH]²/[GSSG]), 25 °C, pH 7",
             fontsize=10.5)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(FIG / "d1_nernst_backcalculation.png")
plt.close(fig)

print(f"E(V) mean = {ev.mean():.1f} mV (range {ev.min():.0f}..{ev.max():.0f})")
print(f"E_combined mean = {ec.mean():.1f} mV")
print(f"ratio needed: E(V) {r1:.3e} : 1 | E_combined {r2:.3e} : 1")
print(f"figures written to {FIG}")
