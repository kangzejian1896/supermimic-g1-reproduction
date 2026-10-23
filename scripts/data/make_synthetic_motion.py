"""Generate a small G1 standing reference from the robot asset, not motion data."""
import argparse
from pathlib import Path
import tempfile
import numpy as np
import mujoco
from supermimic.data.motion_convert import load_g1_model, convert_csv_to_npz


def generate(output: Path, seconds: float = 2.0):
    model = load_g1_model()
    q = model.qpos0.copy()
    if model.nkey:
        q = model.key_qpos[0].copy()
    assert seconds > 0
    raw = np.repeat(q[None, :], max(3, round(seconds * 50) + 1), axis=0)
    raw[:, 3:7] = raw[:, [4, 5, 6, 3]]  # converter input is xyzw
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        csv = Path(temporary) / "synthetic_stand.csv"
        np.savetxt(csv, raw, delimiter=",")
        convert_csv_to_npz(csv, output, 50, 50, model=model)
    with np.load(output) as data:
        payload = {k:data[k] for k in data.files}
    payload['source'] = np.asarray('synthetic robot home pose; no motion dataset')
    np.savez_compressed(output, **payload)
    print(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('data/npz/synthetic/stand.npz'))
    parser.add_argument('--seconds', type=float, default=2.0)
    args = parser.parse_args()
    generate(args.output, args.seconds)
