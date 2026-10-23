"""Check distributable source for accidental local paths and large binary files."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
ignored = {'.git','.venv','__pycache__','.pytest_cache','.ruff_cache','checks','release_assets','data','logs','dist','build','weights'}
violations = []
demo_names = {f'val_{i:02d}.{ext}' for i in [8,17,26,41,44,114] for ext in ['mp4','jpg']}
patterns = [r'/mnt/' + r'nas/', r'/home/' + r'(?:xmov|kangzejian)/',
            r'192[.]168[.]' + r'\d+[.]\d+', r'-----BEGIN ' + r'(?:RSA |OPENSSH )?PRIVATE KEY-----']
for p in root.rglob('*'):
    if any(part in ignored for part in p.relative_to(root).parts) or not p.is_file():
        continue
    rel = p.relative_to(root)
    if rel.parent == Path('docs/media') and rel.name in demo_names and not p.is_symlink():
        header = p.read_bytes()[:12]
        valid = (p.suffix == '.mp4' and header[4:8] == b'ftyp') or (p.suffix == '.jpg' and header[:3] == b'\xff\xd8\xff')
        if not valid or p.stat().st_size > 10*1024*1024:
            violations.append(str(rel))
        continue
    if p.is_symlink() or p.stat().st_size > 2*1024*1024:
        violations.append(str(p.relative_to(root)))
        continue
    try:
        text = p.read_text()
    except UnicodeDecodeError:
        violations.append(str(p.relative_to(root)))
        continue
    if any(re.search(pattern,text) for pattern in patterns):
        violations.append(str(p.relative_to(root)))
if violations:
    raise SystemExit('Review unexpected release content: '+', '.join(violations))
print('Source audit passed (no checked patterns/oversized binary files). This is not an exhaustive secret scan.')
