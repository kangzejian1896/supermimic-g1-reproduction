# 168k release checks · 2026-10-24

Both 168k exports passed restricted loading, finite-tensor checks and exact policy-output parity (maximum absolute difference 0). Six demo MP4s and the 24-example combined video decoded completely without errors. The combined video retains 5,122 frames at 25 fps (204.88 seconds). File hashes are in SHA256SUMS_168k; export manifests record source and output hashes. Source audit passed. This update changes model artifacts and documentation, not training code.

# Release validation

Checked on 2026-10-23 with the release source selected explicitly ahead of the original editable installation, using its existing validated dependencies. A clean `uv sync` from an empty machine has not been completed; do not treat runtime reuse as a fresh-install certification.

- Python source compilation and public-source content audit passed.
- Regression/numerical tests: see `validation_summary.json` for the final count. Dataset-dependent upstream tests are skipped because LAFAN1 motion files are not bundled.
- All three exported weights load with `torch.load(weights_only=True)` and produce exactly the same policy outputs as the corresponding original checkpoint on the exporter comparison batch (maximum absolute difference 0).
- The 36k models export was loaded into fresh world-model/policy/critic modules in 8 MuJoCo Warp environments. A generated robot-home-pose motion was used; no dataset is required for this check. All model state dictionaries matched, counters started at zero, and four optimizer updates changed all three networks with finite parameters. An atomic checkpoint was written successfully.
- The exported 36k policy was independently evaluated on all 128 existing validation references: 0 failures, mean full-reference normalized return **0.8814749**. The saved original-checkpoint benchmark was 0.8811195. The small difference between simulator runs is not an export-tensor mismatch; the tensor/policy-output parity check is exact. Private references and per-clip outputs are not redistributed.
- Source wheel build and archive audit results are recorded in `validation_summary.json` when packaging completes.

Re-run the data-independent checks:

```bash
uv run pytest tests -q
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl uv run python scripts/release/validate_runtime.py \
  --models weights/supermimic_g1_036000_models.pt
python scripts/release/check_source.py
```

The runtime smoke uses shorter horizons, smaller batches and 8 environments; it validates wiring and optimizer flow, not the full-scale training speed or quality. Upstream viewer and multi-GPU execution were not interactively revalidated in this preparation. No real robot was tested.
