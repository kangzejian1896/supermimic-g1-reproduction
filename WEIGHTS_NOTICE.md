# Weight release terms — authorization confirmed; license text pending

The source-code MIT license does not grant a license to the prepared model weights.
These local artifacts are release candidates; no public weight upload has been performed.
The publisher confirmed on 2026-10-23 that authorization covering public model-weight distribution is already in place and will supply the applicable terms. The exact license text/identifier remains to be inserted. No unconditional MIT/Apache/CC weight license is inferred by this preparation.

Training data includes [Motion Data by Bones Studio](https://bones.studio/). Use of the underlying dataset is subject to the BONES Motion Capture Dataset License Agreement.

Relevant source: https://huggingface.co/datasets/bones-studio/seed/blob/main/LICENSE.md (reviewed 2026-10-23). The dataset uses a custom agreement. Its sections 5.2, 6 and 8 address model/results ownership, restrictions, and attribution; a separate agreement may apply to the publisher. This file records the licensing dependency rather than replacing or interpreting that agreement as a blanket downstream license.

Prepared weights contain learned model tensors and generic configuration only. They omit motion files, annotations, replay, per-motion sampling statistics, and optimizer states. Removing those items does not itself establish permission to distribute a trained model.

When the publisher supplies the applicable terms, record that weight license here and in the model card/Hugging Face metadata, preserving the required data attribution. The code package can retain its existing MIT license independently.
