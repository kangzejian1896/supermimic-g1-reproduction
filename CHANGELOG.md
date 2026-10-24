# Changelog

## 2026-10-24 · 168k model and video release

- Publish matching policy and policy/world-model/critic exports with exact inference parity.
- Refresh six validation demos and add the full 24-example Ref/control video.
- Record training resources, validation selection, aggregate metrics and artifact checksums.

# Release candidate changes

Base: CuboiLeo/SuperMimic-Reproduced d9be385b3eeb13a638fb33fb200d3bfd9be9839f.

Experiment changes carried into this release:
- Opt-in paper protocol across training/environment configuration.
- Per-episode COM randomization and documented pelvis-anchor interpretation.
- Full-reference-horizon normalized benchmark return, with executed-step diagnostic retained.
- Correct parallel environment count for packed multi-clip .pt libraries.

Release preparation changes:
- Propagate the stored protocol into benchmark and viewer entry points.
- Add packed-library support to the benchmark CLI.
- Restricted checkpoint deserialization with explicit pathlib compatibility.
- Export only learned tensors and portable configuration; verify exact policy-output parity.
- Add model-only initialization for fresh optimizer/sampling state.
- Write training checkpoints atomically.
- Add synthetic data generation, a real-simulator training smoke check and protocol regression tests.
- Replace upstream results prose with English documentation and explicit provenance, dataset/weight license notices, and reproduction limitations.

`docs/upstream.patch` records the four-file experiment patch before these release-engineering changes. It is not the complete release diff.
