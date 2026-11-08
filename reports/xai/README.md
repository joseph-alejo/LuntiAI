# LuntiAI XAI evidence

Generated on October 30, 2026 by the executed notebook in
`notebooks/LuntiAI_ML_and_XAI.ipynb`.

- `evaluation.json`: dataset and model hashes, package versions, model scores,
  explanation reconstruction errors, sampling rule, sensitivity measurements,
  and the explicitly failed experimental comparison.
- `model-comparison.csv`, `classification-report.csv`: prediction evaluation.
- `tree-shap-sample.npz`: signed attributions for 120 cases × 8 features × 12
  outputs, with row identifiers, baselines, and model probabilities.
- `global-shap-by-class.csv`: mean absolute attributions for the balanced sample.
- `reference-comparison.csv`, `local-sensitivity.csv`: bounded sensitivity checks.
- `demonstration-cases.csv`: correct, incorrect, and smallest-margin examples.
- PNG files: notebook figures and browser screenshots.
- `browser-checks.json`: browser validation evidence for the revised interface.

The 15 regression tests passed in the pinned environment. Browser checks passed
on desktop and at a 390-pixel mobile width. The notebook contains 12 executed code
cells, five embedded plots, and no unhandled cell errors.

The deployed path-dependent TreeSHAP mode passed all-class reconstruction on the
120-case sample with a maximum error of approximately 5.67e-14. The experimental
interventional mode failed the 1e-5 tolerance on its one-case comparison and is
not used by the API. Its failure remains visible in the results; it is not treated
as successful validation. Additivity alone does not establish causal validity.

These results describe synthetic data and a known holdout. No independent field
validation, probability-calibration study, or farmer comprehension study was done.
All application changes remain local; no remote deployment was performed.
