# Current release: v0.2.0-168k

[Release assets](https://github.com/kangzejian1896/supermimic-g1-reproduction/releases/tag/v0.2.0-168k) contain 168k policy, policy/world-model/critic tensors, the 24-example comparison video, export manifests and SHA256SUMS_168k. Training: one A800 80GB, 84,287 clips, 170.11 motion hours, 25.86 logged hours. Both model exports match the current demos.

Exports omit optimizer, replay and motion/sampling state; restricted load and exact policy parity verified. The video preserves all 5,122 frames at 25 fps and was re-encoded to H.264 CRF 23 for distribution. Source code attribution and weight notice remain unchanged. Prior v0.1.0-rc1 assets are retained.
