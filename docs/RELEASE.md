# Publishing the prepared candidate

Source repository: https://github.com/kangzejian1896/supermimic-g1-reproduction . Code and six 44k demo videos are included in Git; weight binaries are distributed separately.

Prepared deliverables:

- Source archive, preserving upstream MIT attribution and this fork's provenance.
- Separate weights archive containing two policies, one policy/world-model/critic bundle, export manifests and SHA256SUMS.
- Installation, data-format, training, evaluation, model-card and validation documentation.

The publisher has confirmed authorization covering weight distribution and will supply its terms. Insert those terms into WEIGHTS_NOTICE.md and the model card for publication. The source MIT notice must not silently extend to weights or data. The remaining item is the exact license wording, not a request to re-confirm the already confirmed authorization.

Suggested distribution: GitHub for source; a GitHub Release or Hugging Face model repository for model files. Do not add private training checkpoints, references, dataset manifests, caches, environment directories, experiment logs, tokens or internal host configuration. Local release_assets/, checks/ and model binaries are excluded from Git.

Never advertise an unavailable download URL or fabricate a citation/DOI. Preserve version distinctions: current repository demos are 44k (val 08, 17, 26, 41, 44, 114); prepared weight bundles remain 32k/36k. The earlier standalone public site remains 32k. Include docs/media and docs/demo_manifest.json when publishing the source.

Published candidate: [v0.1.0-rc1](https://github.com/kangzejian1896/supermimic-g1-reproduction/releases/tag/v0.1.0-rc1), with the 32k/36k weight archive and archive SHA256. The source tree contains the six 44k demonstration videos.
