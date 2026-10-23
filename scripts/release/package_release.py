"""Package tracked source and explicitly selected model assets without experiment data."""
from pathlib import Path
import hashlib,json,shutil,subprocess,tarfile

root=Path(__file__).resolve().parents[2]
subprocess.run(['python3',str(root/'scripts/release/check_source.py')],check=True)
files=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0')
files=[Path(f) for f in files if f]
demo_videos = {Path(f'docs/media/val_{i:02d}.mp4') for i in [8,17,26,41,44,114]}
for f in files:
    if (root/f).is_symlink() or f.suffix in {'.pt','.npz','.npy','.log'} or (f.suffix == '.mp4' and f not in demo_videos):
        raise RuntimeError(f'Unexpected source artifact: {f}')
out=root/'release_assets';out.mkdir(exist_ok=True)
source=out/'supermimic-g1-source-rc1.tar.gz'
with tarfile.open(source,'w:gz') as tar:
    for f in sorted(files):tar.add(root/f,arcname=str(Path('supermimic-g1')/f),recursive=False)
weights=out/'supermimic-g1-weights-32k-36k-rc1.tar.gz'
with tarfile.open(weights,'w:gz',compresslevel=3) as tar:
    for f in sorted((root/'weights').iterdir()):
        if f.suffix in {'.pt','.json','.md'} or f.name=='SHA256SUMS':
            tar.add(f,arcname='supermimic-g1/weights/'+f.name,recursive=False)
    for name in ['WEIGHTS_NOTICE.md','NOTICE.md','docs/MODEL_CARD.md','docs/VALIDATION.md','docs/validation_summary.json','docs/benchmark_36k.json']:
        tar.add(root/name,arcname='supermimic-g1/'+name,recursive=False)
for f in (root/'checks/wheels').glob('*.whl'):shutil.copy2(f,out/f.name)
artifacts=[]
for f in sorted(out.iterdir()):
    if f.suffix=='.whl' or f.name.endswith('.tar.gz'):
        artifacts.append(dict(file=f.name,bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
(out/'manifest.json').write_text(json.dumps(dict(source_files=len(files),upstream_revision='d9be385b3eeb13a638fb33fb200d3bfd9be9839f',
    status='prepared locally; weight distribution authorization confirmed, specific license text pending',artifacts=artifacts),indent=2))
(out/'SHA256SUMS').write_text(''.join(f'{x["sha256"]}  {x["file"]}\n' for x in artifacts))
print(json.dumps(artifacts,indent=2))
