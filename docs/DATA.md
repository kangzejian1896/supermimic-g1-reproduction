# Motion data contract

No BONES-SEED motions, derived reference tensors, clip IDs, text annotations or private split manifests are redistributed in the release.

The public converter (`scripts/data/csv_to_npz_batch.py`) expects **headerless** CSV:

- Columns 0–2: root position in meters.
- Columns 3–6: root quaternion in xyzw order.
- Columns 7–35: 29 joint angles in radians, ordered exactly as `G1_JOINT_NAMES` in `supermimic.data.motion_convert`.
- Set `--input-fps` to the actual rate; output defaults to 50 Hz.

Raw BONES-SEED files may use centimeters/degrees and a different orientation representation. Convert those conventions explicitly before this generic CSV path. Do not infer units from file extension. The internal datav5 conversion/split pipeline is not included; users must supply their own authorized, converted data.

NPZ arrays: `fps`, `joint_pos (T,29)`, `joint_vel (T,29)`, `body_pos_w (T,30,3)`, `body_quat_w (T,30,4)` in wxyz, `body_lin_vel_w (T,30,3)`, `body_ang_vel_w (T,30,3)`, plus `body_names` and `joint_names`. Body order is tied to the pinned G1 XML. Quaternion order differs between CSV input and the NPZ/simulator output.

`build_library.py` packs pelvis pose, joint positions and velocities into fp16 71-dimensional reference states with clip offsets. Do not distribute such a cache if the source license prohibits data redistribution.

Keep train/validation/test splits disjoint, including mirrored variants. The prepared models were trained on 84,287 datav5 train clips and evaluated on 128 held-out validation clips. Test data was not used in this release preparation. An equivalent public split cannot be reconstructed from aggregate counts alone.

For data-independent installation checks, `make_synthetic_motion.py` generates a short standing reference from the separately installed G1 asset's home pose. It contains no motion-capture source data.
