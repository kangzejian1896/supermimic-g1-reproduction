# Paper alignment and implementation choices

This is a documented reproduction attempt, not a claim of exact implementation or benchmark parity. See the original paper: https://arxiv.org/abs/2610.28480 .

| Item | Release configuration |
|---|---|
| Simulator | MuJoCo Warp, through pinned mjlab; 50 Hz control, 4 × 5 ms substeps |
| Policy input | 93-dimensional proprioception × 10 history frames; 10 future reference frames |
| Policy | Encoder/decoder hidden widths 2048/1024/512/256, latent 32 + tanh |
| World model | 2048 × 3 hidden layers, k=8 training windows |
| Critic | Hidden widths 256/128 |
| Imagination | H=32, batch 4096, deterministic policy actions |
| Exploration | Simulation action noise standard deviation 0.1 |
| Training | 4096 environments, UTD 0.4, 320k vector-environment iterations |
| Randomization | Per-episode friction, joint bias, COM; no pushes |
| Failure | Pelvis height error > 0.25m or projected gravity-z error > 0.8 |
| Evaluation | Full clip, deterministic, no sensor/action noise or DR; failed tails count as zero return |

`--env.paper-protocol` changes COM resampling from startup to reset, selects the pelvis as the relative reference anchor and root reward basis, and uses full-reference return normalization in benchmark evaluation. These choices are passed through both training and exported-policy evaluation/viewing.

Known differences and assumptions:

- Our training corpus is 84,287 processed datav5 motions (~170.11 hours), not the paper's 129,514 motions / 264.56 hours. The exact private split manifests are not redistributed. Training from another public split does not reproduce our checkpoint's training distribution exactly.
- A800 80GB differs from the paper's H100. Reported training time is not directly comparable. Periodic evaluation used a separate GPU and is not included in model-training time.
- The paper gives K=10 but not the exact 68-value-per-frame representation used by this reproduction. Feature ordering/scales, some activations, termination-head widths and internal encodings follow the upstream implementation.
- We interpret one iteration as one vectorized environment step; UTD=0.4 means approximately one joint WM/policy update per 2.5 such steps. This counting convention must accompany timing claims.
- Warmup=40, the 10-second training episode limit, reset noise, PD/action scale, tracked-body selection and sampling EMA are retained implementation choices.
- The pelvis anchor is our documented interpretation of the paper's root convention; it is not a verified match to unpublished author code.
- Reference caches use fp16 storage; computation is float32 with TF32 enabled. Synthetic smoke tests are only functional checks.
- No speed-interface distillation, original-paper full benchmark, real-robot test, or text/TRACE conditioning has been reproduced here.
