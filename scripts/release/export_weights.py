"""Export portable model weights, excluding optimizer and dataset sampling state."""
import argparse
import hashlib
import json
from pathlib import Path

import torch
from supermimic.checkpoints import load_checkpoint
from supermimic.eval.benchmark import load_policy_from_checkpoint


def portable_config(config):
    config = json.loads(json.dumps(config, default=str))
    config.update(run_name="supermimic_g1_release", log_root="logs", resume=None)
    config["data"] = dict(npz_dir="data/npz/motions", library=None,
                          manifest=None, clips=None, limit=None)
    return config


def export(source, output, include_models=False):
    if output.exists():
        raise FileExistsError(output)
    raw = load_checkpoint(source)
    names = ["policy", "wm", "critic"] if include_models else ["policy"]
    payload = {"format_version": 1, "iteration": int(raw["iteration"]),
               "num_updates": int(raw["num_updates"]),
               "config": portable_config(raw["config"])}
    for name in names:
        payload[name] = {}
        for key, value in raw[name].items():
            if not isinstance(value, torch.Tensor) or not torch.isfinite(value).all():
                raise ValueError(f"Invalid model tensor: {name}.{key}")
            payload[name][key] = value.detach().cpu().clone()
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(payload, output)
    # Verify both restricted deserialization and identical inference after export.
    exported = torch.load(output, weights_only=True, map_location="cpu")
    assert set(exported) == set(payload)
    original, _ = load_policy_from_checkpoint(source, "cpu")
    released, _ = load_policy_from_checkpoint(output, "cpu")
    torch.manual_seed(0)
    obs = torch.randn(8, 93 * payload["config"]["policy"]["history"])
    goal = torch.randn(8, payload["config"]["policy"]["goal_dim"])
    with torch.inference_mode():
        error = float((original(obs, goal) - released(obs, goal)).abs().max())
    assert error == 0.0, error
    result = dict(file=output.name, sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                  bytes=output.stat().st_size, iteration=payload["iteration"],
                  contents=names, restricted_load_verified=True,
                  policy_output_max_abs_diff=error,
                  source_checkpoint_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  tensors={name:sum(v.numel() for v in payload[name].values()) for name in names},
                  excluded=["optimizer states", "replay", "per-motion sampling statistics",
                            "motion data", "internal filesystem paths"],
                  weight_license="See WEIGHTS_NOTICE.md; not covered by the code MIT license")
    output.with_suffix(".json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--include-models", action="store_true")
    a = p.parse_args()
    torch.set_num_threads(4)
    export(a.checkpoint, a.output, a.include_models)
