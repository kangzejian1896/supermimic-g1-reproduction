# Provenance and attribution

The implementation is derived from CuboiLeo/SuperMimic-Reproduced:
https://github.com/CuboiLeo/SuperMimic-Reproduced

Base revision: d9be385b3eeb13a638fb33fb200d3bfd9be9839f.
The upstream MIT copyright notice (2026 Yuxi Liu) is preserved verbatim in LICENSE.
This is an independent derivative implementation, not an official SuperMimic release.

Original research: SuperMimic: Scaling Humanoid Whole-Body Control with One Differentiable World Model, arXiv:2610.28480. https://supermimic.github.io/

Simulation framework: mjlab, pinned to 8bb2bc9e187797689ec82c78c35019afd2fd0376, and its MuJoCo Warp / MuJoCo dependencies. The G1 XML/meshes are provided by the separately installed mjlab dependency, not redistributed by this source package. Their respective licenses are not replaced by this repository's license.

Other implementations consulted during the research phase:
- https://github.com/JackMin7/supermimic_whole_body_tracking
- https://github.com/zita-ch/supermimic_vibed
- https://github.com/Motphys/Uni-SuperMimic

The source snapshot in this package is based on CuboiLeo, not a claim to have authored all referenced implementations. Upstream experiment reports are intentionally not bundled as this fork's results.

Training data includes [Motion Data by Bones Studio](https://bones.studio/). Use of the underlying dataset is subject to the BONES Motion Capture Dataset License Agreement.
