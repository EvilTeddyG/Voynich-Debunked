# Astronomy Geometry Preregistration Template

## Study ID
- Prereg ID:
- Date:
- Analyst(s):
- Freeze commit SHA:

## Objective
Primary question:
- Do measured folio geometries rank a candidate event distinctly within the C14-constrained window under pre-specified scoring?

## Inputs (Frozen Before Scoring)
- Folio source images and extraction protocol:
- Measurement sheet path:
- Candidate event table path:
- Date window:

## Feature Set (Frozen)
- spoke_count
- ring_count
- zodiac_divisions
- ring_spacing_cv
- occlusion_phase
- calibration_density

## Scoring Configuration (Frozen)
- Scale constants:
- Weight constants:
- Visibility modifier formulation:
- Final score definition:

## Blind Procedure
- Run mode: `--blind`
- Blind key custodian (separate from scoring analyst):
- Unblinding condition (must be met before opening key):
  - ranking reviewed
  - null metrics recorded
  - manuscript notes frozen

## Null Calibration Plan
- Null sample size:
- Null generator definition:
- Primary rarity metric: `p_value_le`
- Secondary metric: z-score

## Acceptance Criteria
- Predefine what constitutes:
  - strong support
  - weak support
  - non-support
- Predefine interpretation limits:
  - allowed claim level: constrained dependence inference
  - disallowed claim level: authorship attribution, definitive production-date proof
- Predefine ranking-surface checks:
  - near-tie count threshold window
  - minimum acceptable best-vs-runner-up gap
  - expected behavior under candidate-table expansion

## Sensitivity Plan
- Weight perturbation plan:
- Feature ablation plan:
- Candidate table perturbation plan:

## Reporting Commitments
- Publish full ranking, not only top hit.
- Publish false-match diagnostics.
- Publish failures and near-misses.
- Publish final unblinding key after freeze criteria met.
- Freeze interpretation notes before unblinding and publish the frozen note with the final report.
