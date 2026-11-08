# Restoration checks — November 8, 2026

The hosted app initially served predictions but lacked complete class-specific
SHAP output. The Space was initially reported as sleeping and woke on access.
The saved model and generated training dataset were retained.

Changes include complete TreeSHAP output shared with the executed notebook,
free-account explanation access, a same-origin frontend, corrected model-loader
dependency, explicit weather/rainfall source labels, removal of unsupported
soil-accuracy claims, a local Windows launcher, and a dataset/inference guide.

Validation before publication:

- 19 automated tests passed; seven dependency deprecation warnings.
- After the final weather-log sanitization, all four weather tests passed again.
- JavaScript syntax and Windows launcher parsing passed.
- Local API smoke test passed, including login, invalid-input rejection, daily
  quota, complete XAI reconstruction, demo premium redemption, and history.
- Browser: signed in with a disposable test account, selected Madaum, submitted
  a recommendation, and saw Cacao at 88.11% for the November offline presets.
  All eight contributions were visible. The expanded runner-up view compared
  Cacao with Rice and showed a gap of approximately 80.68 percentage points.
- Tagalog explanation labels rendered. At a 390-pixel viewport, the page's
  measured document width did not exceed the viewport; explanation text and
  signed bars remained readable. The temporary viewport override was reset.

Publication and hosted checks:

- Code revision `87f9dbcfc887e055641310e607570f2b18998a24` was pushed to
  GitHub and Hugging Face; the Space returned to `RUNNING` after its rebuild.
- The earlier local checkout was fast-forwarded to the same revision.
- Hosted API smoke checks passed with complete XAI, including quota-limited
  responses. The reference Banana case remained 99.21%, with maximum
  reconstruction error approximately `4.26e-14`.
- The deployed weather endpoint returned live OpenWeatherMap temperature and
  humidity and explicitly labeled monthly rainfall as a preset.
- The hosted browser completed sign-in and a Madaum prediction using live
  weather (30.8 °C, 78% humidity, 170 mm/month preset rainfall). It displayed
  Cacao at 83.43%, all eight signed contributions, and the synthetic-data
  limitation. Rainfall attribution was labeled mm/month. No browser console
  errors were captured during this check. Weather-dependent results can change.

`local-api.json` records the local request checks. `hosted-api.json`
records the post-publication checks on Hugging Face. The smoke script
does not write account credentials and removes its own disposable account.

The XAI study's earlier, executed results remain in `reports/xai/`; they were
not re-estimated merely for this website restoration. Synthetic test accuracy
does not establish field performance. The failed experimental interventional
TreeSHAP mode remains excluded from the application.
