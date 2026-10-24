# Model weights

Current version: [v0.2.0-168k](https://github.com/kangzejian1896/supermimic-g1-reproduction/releases/tag/v0.2.0-168k). Download `supermimic_g1_168000_policy.pt` for inference, or `supermimic_g1_168000_models.pt` for policy/world-model/critic initialization. Both match the 168k demo videos. Verify `SHA256SUMS_168k` before use.

Export manifests are in `docs/supermimic_g1_168000_policy.json` and `docs/supermimic_g1_168000_models.json`. Restricted loading and exact inference parity are verified. Use `--initialize-from` for the models export, not `--resume`.

Distribution authorization is confirmed by the publisher; specific downstream weight terms remain pending. See [WEIGHTS_NOTICE.md](../WEIGHTS_NOTICE.md). Source-code MIT does not automatically license weights. Older 32k/36k bundles remain in v0.1.0-rc1.
