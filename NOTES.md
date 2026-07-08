# Project Notes

## Labeling
- First tried labeling severe weather using CAPE/shear thresholds and BRN
- This was leaky as BRN and the thresholds were built from the same features (CAPE, shear) used as model inputs, so a model could just reconstruct the labeling rule instead of learning real patterns
- Turned to predicting heavy precipitation instead

## Scaling to autumn 2020
- Moved from a 3 day January sample to Sept -> Dec 2020
- ~40x the original sample
- CAPE computation crashed WSL repeatedly here, as each parallel task was holding a reference to the full dataset rather than just its own timestep, causing memory blowup
- Sliced the dataset down to a single timestep before creating each delayed task. This kept memory stable and let the full run finish

## Model comparison
~1.17M rows, ~4.3% positive (heavy rain) rate.

| Model | ROC-AUC | PR-AUC |
|---|---|---|
| Logistic Regression | 0.738 | 0.125 |
| Random Forest | 0.849 | 0.356 |
| XGBoost | 0.798 | 0.217 |

Random Forest was the best performer, and tuned its decision threshold (0.35) for a better precision/recall balance (0.39 / 0.38, F1 0.388) instead of using the default 0.5

## Feature importance (Random Forest)
Shear features dominated (bulk_shear_10m_850 highest at ~0.21) and CAPE, BRN were low
Autumn/winter UK rain is mostly frontal, which shear captures well, rather than convective instability, which is what CAPE is measuring

## Limitations
- The labels are based on a rainfall threshold, not real reports of severe weather. I didn't find a freely available UK or Europe storm report database
- CAPE and wind shear are better at identifying summer thunderstorms than the autumn and winter rainfall used in this dataset
