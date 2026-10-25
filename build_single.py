"""Bundle the soumission into one self-contained HTML file to send to the client.

  python3 build_single.py            -> dist/Soumission-Borea-ASCIA.html

Every local asset (film, poster, logos, project images, 3D model, sky) is embedded as a data URI.
The fonts and the 3D libraries still load from their CDNs, so the file needs an internet connection.
"""
import base64, mimetypes, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(HERE, 'index.html'), os.path.join(HERE, 'dist', 'Soumission-Borea-ASCIA.html')
MIME = {'.glb': 'model/gltf-binary', '.hdr': 'application/octet-stream', '.mp4': 'video/mp4', '.jpg': 'image/jpeg', '.png': 'image/png'}

def data_uri(rel):
    path = os.path.join(HERE, rel)
    ext = os.path.splitext(path)[1].lower()
    with open(path, 'rb') as f:
        return f'data:{MIME.get(ext) or mimetypes.guess_type(path)[0]};base64,' + base64.b64encode(f.read()).decode()

s = open(SRC, encoding='utf-8').read()

# the WebM copy is a duplicate of the MP4: keep the MP4, which every browser plays
s = re.sub(r'\s*<source src="assets/borea-hero\.webm" type="video/webm">', '', s)

# static references in attributes
s = re.sub(r'(src|href|poster)="(assets/[^"$]+)"', lambda m: f'{m.group(1)}="{data_uri(m.group(2))}"', s)

# references built in JavaScript: a lookup table, filled once
projet = sorted(set(re.findall(r'`([a-z-]+(?:-v2)?\.jpg)`', s)))
table = {f'projet/{f}': data_uri(f'assets/projet/{f}') for f in projet}
table['borea.glb'] = data_uri('assets/borea.glb')
table['misty_pines_1k.hdr'] = data_uri('assets/misty_pines_1k.hdr')
assets_js = '<script>window.__ASSETS=' + '{' + ','.join(f'"{k}":"{v}"' for k, v in table.items()) + '};</script>\n'
s = s.replace('src="assets/projet/${f}"', 'src="${window.__ASSETS[\'projet/\' + f]}"', 1)
s = s.replace("'assets/borea.glb?v=' + MODEL_VERSION", "window.__ASSETS['borea.glb']", 1)
s = s.replace("'assets/misty_pines_1k.hdr'", "window.__ASSETS['misty_pines_1k.hdr']", 1)
s = s.replace('</head>', assets_js + '</head>', 1)

code = re.sub(r'/\*.*?\*/', '', re.sub(r'data:[^"\']+', '', s), flags=re.S)   # ignore comments and embedded data
left = re.findall(r'assets/[A-Za-z0-9_./-]+', code)
assert not left, f'unbundled references: {left}'
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(s)
print(f'{OUT}  {os.path.getsize(OUT) / 1e6:.1f} MB')
