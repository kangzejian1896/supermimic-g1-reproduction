# Model weights

The release candidate contains:

- `supermimic_g1_036000_policy.pt`: policy-only inference weights.
- `supermimic_g1_036000_models.pt`: policy + world model + critic, for model-only initialization.
- `supermimic_g1_032000_policy.pt`: matches the 32k public video demo.

Each `.pt` has a `.json` sidecar with SHA256, byte size, source-checkpoint hash, tensor counts and export verification. `SHA256SUMS` can be verified with `sha256sum -c SHA256SUMS` from this directory.

These files are deliberately ignored by Git and packaged as separate release assets. Download the archive and its checksum from [v0.1.0-rc1](https://github.com/kangzejian1896/supermimic-g1-reproduction/releases/tag/v0.1.0-rc1). The publisher confirmed distribution authorization; the exact weight terms remain to be supplied: see `../WEIGHTS_NOTICE.md` and `../docs/MODEL_CARD.md`. Do not infer MIT terms for weights from the source-code license.

Loading uses PyTorch's `weights_only=True`. Policy-only exports are suitable for `eval_benchmark.py` and `play.py`; they are not resumable optimizer checkpoints. Use the `models` export with `--initialize-from`, not `--resume`.
