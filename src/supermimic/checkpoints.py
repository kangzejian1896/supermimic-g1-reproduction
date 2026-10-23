"""Portable checkpoint loading and model-only initialization."""
from pathlib import Path, PosixPath, WindowsPath

import torch


def load_checkpoint(path, device="cpu"):
    # Legacy training configs contain pathlib values. Permit only these specific
    # value types, while retaining PyTorch's restricted tensor/dict unpickler.
    with torch.serialization.safe_globals([Path, PosixPath, WindowsPath]):
        return torch.load(path, map_location=device, weights_only=True)


def initialize_models(trainer, path):
    """Load model tensors only; retain fresh optimizer, replay and schedule state."""
    checkpoint = load_checkpoint(path, trainer.device)
    required = ("policy", "wm", "critic")
    missing = [name for name in required if name not in checkpoint]
    if missing:
        raise ValueError(f"Model initialization needs {required}; missing {missing}")
    for name in required:
        getattr(trainer, name).load_state_dict(checkpoint[name], strict=True)

