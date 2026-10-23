# SuperMimic G1

**Independent reproduction · Differentiable world-model control · MuJoCo Warp**

A reference-motion-conditioned whole-body controller for Unitree G1, using a learned differentiable world model and short-horizon BPTT actor–critic training in **MuJoCo Warp / mjlab**.

This is an independent reproduction **derived from [CuboiLeo/SuperMimic-Reproduced](https://github.com/CuboiLeo/SuperMimic-Reproduced), commit `d9be385b3eeb13a638fb33fb200d3bfd9be9839f`**. It is not the authors' official implementation. The original work is [SuperMimic: Scaling Humanoid Whole-Body Control with One Differentiable World Model](https://arxiv.org/abs/2610.28480) ([project](https://supermimic.github.io/)).

**Release state:** source code and six 44k validation demos are provided in this repository. Sanitized 32k/36k weights are packaged separately. Code is MIT; weight distribution authorization is confirmed by the publisher; the separate weight license text is pending. See [WEIGHTS_NOTICE.md](WEIGHTS_NOTICE.md).

[44k validation demos](#validation-demos--44k) · [Model card](docs/MODEL_CARD.md) · [Paper alignment](docs/PAPER_ALIGNMENT.md) · [Data format](docs/DATA.md) · [Validation](docs/VALIDATION.md)

## Training at a glance

| Demo checkpoint | Training GPU | Training data | Time to checkpoint |
|:--|:--|:--|:--|
| **44,000 iterations** · seed 42 | **1 × NVIDIA A800-SXM4-80GB** | **84,287 clips · 170.11 motion hours** | **6.82 hours ≈ 6 h 49 min** |

The full processed **BONES-SEED datav5 training split** contains 30,619,722 frames at 50 Hz. Training uses 4,096 parallel environments; **128 held-out validation clips** are used for evaluation. The GPU has 80GB capacity; observed training allocation was about 24GB. Time is the training loop's logged elapsed time at iteration 44,000, excluding additional evaluation and rendering GPU time. This is an intermediate checkpoint of a 320k schedule, not the completed schedule.

## Validation demos · 44k

**Left: kinematic reference. Right: actual SuperMimic MuJoCo Warp rollout.** All six videos below use the **44k** checkpoint, with a shared camera and timeline, full motion duration and on-screen errors. These are reference-conditioned control results; the text describes the motion and is not a policy input.

Click a thumbnail to open its MP4. The repository also includes a [six-video gallery](docs/index.html) with playback and speed controls; serve the repository locally with `python3 -m http.server 8000`, then open `http://localhost:8000/docs/`.

| val 08 · Side stretch | val 17 · Lateral dance |
|:--:|:--:|
| [![Side stretch](docs/media/val_08.jpg)](docs/media/val_08.mp4) | [![Lateral dance](docs/media/val_17.jpg)](docs/media/val_17.mp4) |

| val 26 · Backward jump | val 41 · Balletic turn |
|:--:|:--:|
| [![Backward jump](docs/media/val_26.jpg)](docs/media/val_26.mp4) | [![Balletic turn](docs/media/val_41.jpg)](docs/media/val_41.mp4) |

| val 44 · Retro dance | val 114 · Pickaxe strikes |
|:--:|:--:|
| [![Retro dance](docs/media/val_44.jpg)](docs/media/val_44.mp4) | [![Pickaxe strikes](docs/media/val_114.jpg)](docs/media/val_114.mp4) |

Across **all 128 validation clips**, this visualization protocol gives **0.1128 rad** mean per-clip joint RMSE and **0.2046 m** mean per-clip root-position RMSE, with **128/128** clips not crossing the height/tilt failure thresholds. Completion does not imply perfect tracking. The six displayed examples were selected by the project owner for presentation and do not replace the full-split evaluation. The zero-initial-velocity visualization protocol differs from the native reward benchmark below.

[Demo protocol and checkpoint hash](docs/demo_manifest.json) · Motion Data by [Bones Studio](https://bones.studio/).

**Version note:** these demos are 44k; the currently prepared weight bundles below remain 32k/36k. They do not reproduce the 44k videos.

## What is included

- World model, differentiable kinematics, analytic rewards, policy and critic, replay, training and evaluation.
- Opt-in `paper_protocol`: per-episode COM randomization, pelvis reference anchor, full-reference return normalization, and packed-library evaluation that retains parallel environments.
- Portable policy-only and policy/world-model/critic exports, with checksums and identical policy outputs after export.
- Model-only initialization for new training data, atomic checkpoint writes, and a synthetic smoke example that needs no motion dataset.

**Inputs:** 10 frames of proprioception (930 values) and 10 future reference frames (680 values). **Output:** 29 joint-position control actions at 50 Hz. No text embeddings, TRACE conditioning, or text-to-motion generation are included. Physical simulation uses 4 substeps of 5 ms each.

## Install

Linux, Python 3.12 and a CUDA-capable NVIDIA GPU are required for physics training/evaluation. The tested training device was one A800 80GB; observed training allocation was about 24GB. That is an observed configuration, not a guaranteed minimum. See [tested runtime](docs/tested-runtime.txt).

From the repository root, with [uv](https://docs.astral.sh/uv/) installed:

```bash
uv sync --frozen --group dev
# Avoid accidentally importing Python packages from ROS/other environments.
env -u PYTHONPATH uv run pytest tests -q
```

The upstream lockfile and mjlab revision are retained. `pyproject.toml` configures the PyTorch CUDA 13.0 and NVIDIA package indexes. mjlab supplies its G1 robot asset; third-party dependency/asset licenses remain applicable. No robot meshes are vendored here.

## Try without a motion dataset

Generate a short, constant reference from the robot's home pose:

```bash
uv run python scripts/data/make_synthetic_motion.py
# Place the prepared release weights in weights/ first.
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl uv run python scripts/eval_benchmark.py \
  --ckpt weights/supermimic_g1_036000_policy.pt \
  --npz-dir data/npz/synthetic --num-envs 1 --out logs/synthetic_eval.json
```

This verifies the interface, not realistic tracking quality. To view motions you have prepared:

```bash
CUDA_VISIBLE_DEVICES=0 uv run python scripts/play.py \
  --ckpt weights/supermimic_g1_036000_policy.pt \
  --npz-dir data/npz/motions --num-envs 1 --viewer viser
```

The viewer shows a reference ghost and the simulated robot. Its environment protocol is read from the checkpoint, including the pelvis anchor. The policy acts on reference motion, not on the dataset's text labels.

## Prepare data and train

Acquire motion data under its applicable license; none is shipped in this repository. Supply headerless G1 CSVs in meters/radians, root quaternion **xyzw**, and the documented joint order. For raw BONES-SEED CSV conventions, see [DATA.md](docs/DATA.md); do not feed centimeter/Euler files directly into this converter.

```bash
uv run python scripts/data/csv_to_npz_batch.py \
  --input-dir data/csv/train --output-dir data/npz/train --input-fps 50
uv run python scripts/data/build_library.py \
  --npz-dir data/npz/train --out data/library/train.pt
CUDA_VISIBLE_DEVICES=0 bash scripts/train_paper.sh \
  --run-name g1_paper_seed42 --data.library data/library/train.pt
```

Defaults: 4096 environments, world-model horizon 8, imagination horizon 32, policy batch 4096, world-model batch 2048, seed 42, and a 320,000-iteration schedule. The paper's 3-hour result is a performance milestone on H100, not this full schedule's duration. `configs/paper_protocol.json` records the experiment configuration; CLI flags configure the trainer. Use a fresh run name to avoid overwriting earlier logs.

To initialize a new training run from the released model tensors:

```bash
CUDA_VISIBLE_DEVICES=0 bash scripts/train_paper.sh \
  --run-name g1_finetune --data.library data/library/train.pt \
  --initialize-from weights/supermimic_g1_036000_models.pt
```

`--initialize-from` resets optimizer, replay/sampling state and iteration counters. It is different from `--resume`, which requires a complete private training checkpoint and a compatible dataset. Public exports deliberately omit optimizer state and per-motion sampling statistics.

## Evaluate

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl uv run python scripts/eval_benchmark.py \
  --ckpt weights/supermimic_g1_036000_policy.pt \
  --npz-dir data/npz/val --num-envs 128 --out logs/val.json
# Packed libraries are also supported; one .pt can contain many motions.
CUDA_VISIBLE_DEVICES=1 MUJOCO_GL=egl uv run python scripts/eval_benchmark.py \
  --ckpt weights/supermimic_g1_036000_policy.pt \
  --library data/library/train.pt --num-envs 1024 --out logs/train_eval.json
```

Evaluate immutable numbered checkpoints on a separate GPU if training is running. `sm-train` saves checkpoints but does not automatically launch benchmark jobs. The benchmark uses the full reference horizon as the denominator in `paper_protocol`; early failure earns zero reward for the remaining duration. Legacy executed-step normalization is retained separately for diagnostics.

## Prepared checkpoints

| Artifact | Contents | Purpose |
|---|---|---|
| `supermimic_g1_036000_policy.pt` | Policy + portable config | Inference, 36k candidate |
| `supermimic_g1_036000_models.pt` | Policy, world model, critic + config | Model-only training initialization |
| `supermimic_g1_032000_policy.pt` | Policy + portable config | Matches the public 32k video demo |

Weights are packaged separately from the Git source; see [weights/README.md](weights/README.md). No raw data, replay, text annotations, optimizer states, per-motion scores, or internal filesystem paths are included in these exports. SHA256 files accompany the prepared artifacts. PyTorch restricted loading (`weights_only=True`) is verified.

The 36k checkpoint's existing native benchmark: **0 failures / 128 validation clips, mean normalized return 0.8811**; **58 failures / 84,287 training clips, return 0.9091**. Training-set coverage is not generalization. This uses our processed datav5 split, not the original paper's full dataset/filtering. The public 32k demo uses a different zero-initial-velocity visualization protocol; its RMSE must not be equated to native benchmark return. See the model card for limitations.

## Attribution and licenses

Code: [MIT](LICENSE), preserving the original copyright notice. Changes and provenance: [NOTICE.md](NOTICE.md), [CHANGELOG.md](CHANGELOG.md). Model weights: [WEIGHTS_NOTICE.md](WEIGHTS_NOTICE.md), **not automatically MIT**.

**Training data includes [Motion Data by Bones Studio](https://bones.studio/). Use of the underlying dataset is subject to the BONES Motion Capture Dataset License Agreement.** Obtain data from [bones-studio/seed](https://huggingface.co/datasets/bones-studio/seed) under its license. Dataset access or redistribution rights are not granted by this repository.

Please cite the original SuperMimic paper and acknowledge CuboiLeo's reproduction when using this implementation. This fork's measured results must not be attributed to the original authors. No real-robot deployment or full-paper performance reproduction is claimed.
