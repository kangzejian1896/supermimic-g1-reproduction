# SuperMimic G1 model card

## Identity and status

- Architecture: reference-conditioned G1 policy with a differentiable learned world model and critic.
- Base implementation: CuboiLeo/SuperMimic-Reproduced, d9be385b3eeb13a638fb33fb200d3bfd9be9839f, with the changes in CHANGELOG.md.
- Primary candidate: iteration 36,000; seed 42; 5.60 logged training hours on one A800 80GB. Evaluation uses additional GPU time and is excluded from that training figure.
- Companion export: iteration 32,000, matching the earlier public demonstration, 4.98 logged training hours.
- Current README demos: iteration 44,000; 6.82 logged training hours (about 6 h 49 min) on one NVIDIA A800-SXM4-80GB. Six owner-selected validation examples: 08, 17, 26, 41, 44, 114. These demos are newer than the prepared 32k/36k weight exports; see [demo_manifest.json](demo_manifest.json).
- Prepared locally on 2026-10-23. This is an intermediate checkpoint, not a completed 320k schedule or an official paper release.
- Weight distribution authorization: **confirmed by the publisher on 2026-10-23**. The specific weight license text remains to be supplied, separately from the MIT source-code license. See WEIGHTS_NOTICE.md. Source and release assets are maintained at [kangzejian1896/supermimic-g1-reproduction](https://github.com/kangzejian1896/supermimic-g1-reproduction).

## Inputs and outputs

The policy expects scaled/ordered features assembled by this repository's environment: proprioception history `(B,930)` and future reference goal `(B,680)`. Output is `(B,29)` joint-position control actions, consumed by the configured G1 PD/action pipeline at 50 Hz. Raw joint trajectories, motor torques and text embeddings are not interchangeable with these arrays. Use the pinned environment to assemble observations.

Policy: 8,892,807 tensors' scalar elements; world model: 8,815,113; critic: 235,689, as counted in the exported state dictionaries. These counts include any serialized buffers and should not be assumed to be trainable-parameter-only counts.

The policy is deterministic given its inputs. Simulation exploration uses Gaussian action noise during training. This release does not implement a probabilistic text-to-motion model.

## Training data

The internal processed datav5 split contains 84,287 training clips (~170.11 hours) derived from BONES-SEED and 128 held-out validation clips. No final test-set measurement is claimed. Private preprocessing/split manifests and raw/derived motion data are not included. This limits exact independent reproduction of the training data distribution.

**Training data includes [Motion Data by Bones Studio](https://bones.studio/). Use of the underlying dataset is subject to the BONES Motion Capture Dataset License Agreement.**

Source data: https://huggingface.co/datasets/bones-studio/seed . Dataset license: https://huggingface.co/datasets/bones-studio/seed/blob/main/LICENSE.md . Model exports do not grant access to or redistribution rights for that dataset.

## Evaluation

Native deterministic benchmark, with noise/domain randomization disabled and full-reference return normalization:

| 36k checkpoint | Clips | Failures | Mean normalized return |
|---|---:|---:|---:|
| datav5 training coverage | 84,287 | 58 | 0.909059 |
| datav5 validation | 128 | 0 | 0.881120 |

These are the saved original-checkpoint benchmark aggregates; [VALIDATION.md](VALIDATION.md) records the separate release-export checks. Full-clip completion is measured against the configured pelvis-height/gravity thresholds, not a general physical safety criterion. Training coverage is not a held-out generalization metric.

The earlier public 32k videos and current 44k README demos use a separate processed-reference protocol with GT first-frame pose and zero initial velocity, and continue after threshold crossings for error measurement. Do not mix those RMSE values with this benchmark's returns. Text labels shown in the demo describe references; they are not model inputs.

## Intended use and limitations

Intended use is simulation research on reference-motion tracking and differentiable world-model control. No real-robot validation, physical deployment readiness, text-semantic accuracy, unseen-environment robustness, or original-paper benchmark equivalence is established.

Inference requires valid G1 reference motion and matching observation/action conventions. The checkpoint can drift, terminate early, or track some poses poorly despite aggregate completion numbers. Robot contacts and PD settings differ from other simulator backends. No prop dynamics or hand/finger manipulation is modeled.

## Contents and export

Policy-only exports contain model state tensors, training iteration/update counters and generic configuration. The model export additionally contains world model and critic tensors. No optimizer, replay, sampling-bin scores/memory, motion files or internal paths are included. The exported model does not support exact optimizer-state resumption.

SHA256 and source-checkpoint hashes are in each artifact's JSON sidecar. Restricted deserialization and exact policy-output equality after export are verified. Those checks establish faithful serialization, not resistance to memorization or a legal redistribution entitlement.
