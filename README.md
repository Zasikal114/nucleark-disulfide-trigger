# The disulfide release trigger, priced in millivolts

**NucleArk — Tsinghua iGEM 2026.** The design-level analysis behind one line of
our [project wiki](https://2026.igem.wiki/tsinghua): the first release design
for our condensate-based nuclear-delivery system was a chemical trigger —
inter-chain disulfide bonds that snap open in a reducing environment and let go
of the cargo. This repository keeps the full quantitative case for why the
project pivoted from that trigger to light control, so the wiki can stay short.

Scope note: this is the **design-level analysis only**. The safety conclusion
itself is carried by the wet lab's BSO toxicity experiment (mainline T1), which
is referenced below but not interpreted here.

---

## 1 · The bond — from "does it break" to "how many millivolts"

We generated five AlphaFold-Multimer conformation models of the 1ORO-scaffold
double-strand construct, mutated each inter-chain cysteine pair to serine, and
used FoldX to compute the folding free-energy change of removing the disulfide.
Converted through

**E(V) = −ΔΔG / (23.06 × n_cys)**  (n_cys = 2)

the breaking potential of the designed bond is:

| Quantity | Value | Five-model spread |
|---|---|---|
| **E(V)** (strict threshold) | **≈ −282 mV** | −277 to −287 mV |
| **E_combined** (entropic + solvation corrections) | **≈ −346 mV** | −342 to −351 mV |

The more negative the number, the more reducing an environment must be to open
the switch. This pair of values is the quantitative anchor around which the
tunable-threshold molecular library was designed (nine-construct LLPS
predictions in [`data/llps_predictions_9_constructs.csv`](data/llps_predictions_9_constructs.csv)).

Raw FoldX output (all energy terms per model):
[`data/foldx_ev_raw_1oro_constructs.tsv`](data/foldx_ev_raw_1oro_constructs.tsv).

## 2 · The environment — the cell already ships a potential gradient

Compartments are not electrically interchangeable. Plasma/extracellular fluid
sits around −40 to −130 mV; the endoplasmic reticulum (oxidative folding) around
−170 to −230 mV; the cytosol and nucleus are the most reducing compartments,
around −260 to −320 mV, sustained by a millimolar glutathione (GSH) pool that is
essentially absent from blood.

The designed threshold of −282 mV lands inside that intracellular window:
closed in the bloodstream, closed through the secretory pathway, opened by the
endogenous GSH gradient on arrival in the cytosol or nucleus — with no external
manipulation at all. That is the design argument for a GSH-responsive switch,
and it is why the response threshold was made tunable rather than fixed: the
margin between threshold and environment is a design variable.

![Compartment potentials vs. the breaking threshold](figures/d1_potential_axis.png)

## 3 · The counterfactual — forcing the switch open is expensive, and blind

The alternative to riding the endogenous gradient is to push the environment
past the threshold yourself. The Nernst relation for the GSH/GSSG couple,

**E_h = −240 mV − 29.58·lg([GSH]²/[GSSG])**  (25 °C, pH 7),

states exactly what that costs in HeLa-like cytosol ([GSH] ≈ 7 mM):

| Target potential | Required GSH : GSSG ratio | vs. physiological (30–100 : 1) |
|---|---|---|
| −282 mV (E(V), strict threshold) | ≈ 3.7 × 10³ : 1 (GSSG ≤ 1.9 µM) | 37–120 × higher |
| −346 mV (E_combined) | ≈ 5.7 × 10⁵ : 1 (GSSG ≤ 12 nM) | ~4 orders of magnitude higher |

Two conclusions follow.

1. **The threshold sits at or beyond the edge of what physiology reaches**:
   any systemic redox reprogramming — perfusion with strong reductants, GSH
   esters, genetic depletion of the glutathione pool — has to buy a shift two
   to four orders of magnitude larger than normal biological fluctuation.
2. **The manipulation is blind to compartments**: a cytosol dragged to
   −346 mV has crossed the mitochondrial matrix potential and will scramble the
   ER's oxidative folding chemistry at the same time. The wet lab's mild
   pharmacological probe of the same axis (BSO, which depletes GSH) produces a
   clear toxicity phenotype — an empirical echo of how narrow this control
   window is.

![Nernst back-calculation](figures/d1_nernst_backcalculation.png)

## 4 · Design decision — why the trigger became light

The disulfide analysis did what a good negative result should do: it moved the
design. A redox trigger can be made selective on paper, but the only entity
allowed to pull the trigger is the cell's own gradient — which means the release
time and place cannot be chosen, only received. Light needs no such compromise:
it deposits no chemistry, shifts no potentials, and is switched by the
experimenter. That reasoning, together with the robustness of the CORdensate
photo-switchable condensation module (Li Pilong's lab, Tsinghua) across fusion
partners, is why NucleArk's final design couples condensation to illumination
rather than to glutathione.

---

## Repository layout

```
figures/    d1_potential_axis.png / d1_nernst_backcalculation.png  (English, main)
            *_zh.png                                              (Chinese originals)
code/       make_figures.py — regenerates both English figures
data/       foldx_ev_raw_1oro_constructs.tsv — raw FoldX output, 5 models, all terms
            llps_predictions_9_constructs.csv — LLPS predictor panel for the library
docs/       D1_wiki_copy_zh.md — the original Chinese write-up (wiki文案)
```

## Reproduce

```bash
python code/make_figures.py   # needs numpy + matplotlib; writes into figures/
```

## Provenance & caveats

- FoldX values: 1ORO-scaffold construct, Cys→Ser mutation, five
  AlphaFold-Multimer models (`data/foldx_ev_raw_1oro_constructs.tsv`).
- Compartment redox ranges are **literature-derived summary values**
  (Schafer & Buettner 2001; Hwang 1992; Montero 2013), shown schematically in
  the figures — re-verify against the original papers before citing the ranges
  in a publication.
- Nernst coefficient 29.58 mV/decade valid at 25 °C, pH 7, two-electron transfer.
- The Chinese write-up in `docs/` is the source this analysis was first
  drafted in; numbers are identical.

## License

MIT — see [LICENSE](LICENSE).
