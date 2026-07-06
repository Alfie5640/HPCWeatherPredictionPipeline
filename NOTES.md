# Project Notes / Findings

## Labeling method comparison (Stage 4)

Two proxy-labeling approaches were implemented and compared on the January 2020 UK sample:

- **Threshold-based**: CAPE >= 500 J/kg AND shear >= 15 m/s (both required)
- **BRN-based**: Bulk Richardson Number (CAPE / 0.5*shear^2) within [10, 45]

Result on this sample: threshold method found 0 positive labels (expected — January UK
CAPE values are far below 500 J/kg). BRN method found 4 positive labels.

**Finding**: BRN's ratio-based nature means it can flag points as "favorable" purely
because both CAPE and shear are proportionally small, even when neither is meteorologically
significant in absolute terms. This is a known limitation of using BRN without a
minimum CAPE floor as a precondition — standard forecasting practice typically pairs
BRN with such a floor. Retained here deliberately (without the floor) to demonstrate
and document this exact failure mode, and to allow direct comparison against the
simpler threshold method.

**Implication for scaling (Stage 6)**: this discrepancy will need re-examining once
labels are computed on summer data with genuinely higher CAPE, since it's unclear
whether BRN's false-positive tendency persists at realistic CAPE magnitudes or is
specific to this near-zero-instability winter sample.
