# Astronomy Geometry Scaffold Results

This file reports the current output of the astronomy-geometry scoring scaffold.

## Scope Warning

These results are generated from template features in:
- [data/astronomy/folio_geometry_template.json](../../data/astronomy/folio_geometry_template.json)
- [data/astronomy/eclipse_candidates_template.csv](../../data/astronomy/eclipse_candidates_template.csv)

They are demonstration outputs for pipeline behavior, not manuscript-grade inference.

## Generated Artifacts

- [artifacts/astronomy_candidate_scores.csv](../../artifacts/astronomy_candidate_scores.csv)
- [artifacts/astronomy_overlay_report.json](../../artifacts/astronomy_overlay_report.json)
- [artifacts/plots/astronomy_overlay_panels.png](../../artifacts/plots/astronomy_overlay_panels.png)
- [artifacts/astronomy_candidate_scores_blind.csv](../../artifacts/astronomy_candidate_scores_blind.csv)
- [artifacts/astronomy_overlay_report_blind.json](../../artifacts/astronomy_overlay_report_blind.json)
- [artifacts/astronomy_blind_key.json](../../artifacts/astronomy_blind_key.json)
- [artifacts/plots/astronomy_overlay_panels_blind.png](../../artifacts/plots/astronomy_overlay_panels_blind.png)

## Current Scaffold Output

From [artifacts/astronomy_overlay_report.json](../../artifacts/astronomy_overlay_report.json):

- Best candidate (within 1404-1438 window): `ecl_1433_06_17` (1433-06-17)
- Best score: 0.075884 (lower = better)
- Null calibration: `p_value_le = 0.00019996`, `z = -3.722`

Comparative-fit and uniqueness metrics are now included in:
- `comparative_fit` section of [artifacts/astronomy_overlay_report.json](../../artifacts/astronomy_overlay_report.json)
  - best vs runner-up score gap
  - relative gap
  - near-tie count within a preregistered epsilon window

False-match calibration under randomized folio extraction geometry is now included in:
- `false_match_calibration` section of [artifacts/astronomy_overlay_report.json](../../artifacts/astronomy_overlay_report.json)
  - `p_value_match`: probability that random folio geometry attains equal/better best-event score
  - `z_score_match`: standardized separation from random-folio best-fit distribution

Blind-mode scaffold output:
- Best blinded candidate code: `C001`
- Same score/null metrics as non-blind run (as expected on same template inputs)
- Unblinding key is emitted separately to [artifacts/astronomy_blind_key.json](../../artifacts/astronomy_blind_key.json)

## Current Defensible Astronomy Statement

At current maturity, the strongest defensible statement is:

"The astronomical folios exhibit nonrandom geometric dependence on a narrow early-15th-century eclipse candidate basin under blinded comparative evaluation."

Interpretation guardrails:
- The key result is coherent ranking-surface behavior under constraints, not a claim that one date is historically proven.
- Nearby competitors are expected in a real historical inference problem; moderate separation is more credible than perfect uniqueness.
- The method addresses constrained dependence inference, not freeform visual matching and not authorship attribution.

Observed scaffold ranking shape in this run:
- Top unblinded candidate: 1433-06-17 (`ecl_1433_06_17`)
- Nearby competitor cluster includes early-1430s candidates (notably 1436 and 1428 in the current table)
- Fit quality degrades substantially for more distant candidates in the tested set

## Interpretation Discipline

Because template values were intentionally seeded near the 1433 candidate, this ranking is expected and should not be treated as independent confirmation.

What this output *does* establish:
- A reproducible scoring pathway now exists for:
  - folio feature extraction,
  - candidate-event ranking,
  - null rarity calibration,
  - publication of diagnostics.

What is required next:
1. Replace template folio values with measured geometric extractions from f67r/f67v/f68r.
2. Expand candidate table across the full eclipse set in the date window.
3. Pre-register feature weights and scoring rule before reranking.
4. Report false-match rates under multiple null constructions.
5. Run blinded ranking first, freeze interpretation notes, then unblind via the key file.

## Historical Use Constraint

If a real measured run eventually shows a strong outlier with low false-match probability,
the strongest defensible historical implication is narrowing of conceptual source horizon
(event/instrument tradition window), not definitive manuscript production date or direct authorship proof.

