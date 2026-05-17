# Astronomy Geometry Scaffold Results

This file reports the current output of the astronomy-geometry scoring scaffold.

## Scope Warning

These results are generated from template features in:
- [data/astronomy/folio_geometry_template.json](data/astronomy/folio_geometry_template.json)
- [data/astronomy/eclipse_candidates_template.csv](data/astronomy/eclipse_candidates_template.csv)

They are demonstration outputs for pipeline behavior, not manuscript-grade inference.

## Generated Artifacts

- [artifacts/astronomy_candidate_scores.csv](artifacts/astronomy_candidate_scores.csv)
- [artifacts/astronomy_overlay_report.json](artifacts/astronomy_overlay_report.json)
- [artifacts/plots/astronomy_overlay_panels.png](artifacts/plots/astronomy_overlay_panels.png)

## Current Scaffold Output

From [artifacts/astronomy_overlay_report.json](artifacts/astronomy_overlay_report.json):

- Best candidate (within 1404-1438 window): `ecl_1433_06_17` (1433-06-17)
- Best score: 0.075884 (lower = better)
- Null calibration: `p_value_le = 0.00019996`, `z = -3.722`

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
