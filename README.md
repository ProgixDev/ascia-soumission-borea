# Soumission · Chalet Boreä · ASCIA

Interactive web soumission (hardware quote) from ASCIA for the smart-home equipment of the **Boreä** chalet by New Way Living. One static page:

- a 15-second hero film
- the design sheet as a scrolling story
- a realistic 3D model of the chalet with all 224 devices placed where they are installed, plus an architectural 2D plan
- the full price list, AI, greenhouse, a day in the chalet, the 64 automations, options with a live total, terms, and signature with PDF export

All prices and quantities come from the ASCIA draft in `_source/soumission-borea-ascia.html` (hardware only, before taxes; installation is quoted separately).

## Run it

It is a static site with no build step. Serve the folder and open it:

```bash
python3 -m http.server 4810
```

Then go to <http://localhost:4810>. Opening `index.html` straight from disk won't load the 3D model, because browsers block local file requests.

## What's where

| Path | What it is |
|---|---|
| `index.html` | The whole page: HTML, CSS and JS. The data (systems, prices, rooms, automations, options) is in the first `<script>`, and the 3D viewer is in the `<script type="module">` at the end. |
| `assets/` | Everything the page loads: the film (`borea-hero.mp4` / `.webm` + poster), logos, the design-story images (`assets/projet/`), the 3D model `borea.glb` (Draco-compressed) and the sky `misty_pines_1k.hdr`. |
| `build_single.py` | Bundles the page and all its assets into one file, `dist/Soumission-Borea-ASCIA.html`, to send to the client. |
| `3d/` | The Blender pipeline that builds `assets/borea.glb` (see below). |
| `v2-video/` | Hero film production: image prompts, video prompts (Kling 4.0), drawing prompts, reference crops, generated frames (`takes/`), the 9 Kling clips (`clips/`), the cut film (`final/`) and a review log. |
| `_source/` | The original ASCIA soumission draft, the source of truth for prices and terms. |

## Editing the page

- **Prices, devices, quantities:** the `SYS` array in `index.html`. Totals, bars, tables and the recap all compute from it.
- **Devices in the 3D and the plan:** `ZONES` (what is in each room). The 3D mounting point of each device comes from its label, via `kind()` and the `mountRoom` / `mountTerrasse` / `mountThermea` / `mountSerre` functions.
- **Automations, timeline, options:** the `A`, `DAY` and `OPTIONS` arrays.
- **Design-story section:** the `PROJET` array (text, specs, images).
- After changing the 3D model, bump `MODEL_VERSION` in `index.html` so browsers fetch the new `borea.glb` instead of a cached one.

## Rebuilding the 3D model

Blender 5.1, run headless with no add-on needed. Blender is only the workshop; nothing is rendered there. Realism is done on the web: forest HDRI lighting, AgX tone mapping, ambient occlusion and soft shadows.

```bash
cd 3d
B=/Applications/Blender.app/Contents/MacOS/Blender
# 1. Poly Haven scans -> light pieces in prepped/ (rocks, ferns, fire pit, armchair, potted plant)
$B -b --factory-startup -P prep_assets.py  -- "$PWD/source" "$PWD/textures" "$PWD/prepped"
# 2. Tree cards for the forest (black spruce, balsam fir, pine)
$B -b --factory-startup -P prep_trees.py   -- "$PWD/source" "$PWD/prepped"
# 3. BlendKit furniture and plants -> light pieces (needs the BlendKit downloads, see below)
$B -b --factory-startup -P prep_blendkit.py -- "$HOME/blenderkit_data/models" "$PWD/prepped"
# 4. Build the chalet and export assets/borea.glb (+ borea.blend)
$B -b --factory-startup -P build_borea.py  -- "$PWD/../assets/borea.glb" "$PWD/borea.blend" "$PWD/unused.png"
```

`prepped/` already holds the outputs of steps 1–3, so normally only step 4 is needed.

Notes on `build_borea.py`:
- Units are feet: x = width (0–24), z = depth (0 = back wall, 25 = front), y = up.
- `terr(x, z)` gives the ground height; anything placed outside the clearing must use it.
- The page relies on the node named `Roof` (lifted by "Toit ouvert") and on materials named `Glow_*` (lit by the night toggle).

To build only some BlendKit pieces: `ONLY=lemon,basil $B -b ... -P prep_blendkit.py -- ...`

## The single file for the client

```bash
python3 build_single.py
```

This writes `dist/Soumission-Borea-ASCIA.html` (about 31 MB) with every asset embedded. The fonts and the 3D libraries still load from Google Fonts and jsDelivr, so the file needs an internet connection.

## Asset credits

- **Poly Haven** (CC0): fir sapling, pine sapling, mossy rocks, fern, stone fire pit, modern armchair, potted plant, all textures, and the `misty_pines` HDRI.
- **BlendKit** (free models, royalty-free license), by asset base ID:

| Piece | BlendKit asset ID |
|---|---|
| Sectional sofa | `6613c079-7f59-4373-b74a-86f1c43d4d3c` |
| Platform bed | `0d29b2f7-dea9-46ea-aad5-af2a38ee561e` |
| Nightstand | `a4e5c2d2-5545-4839-afd3-16f044b1e4fd` |
| Counter stool | `7ee47229-e3f4-4189-9ec5-e84529547593` |
| Dining chairs (from set) | `aacf8c17-ebb3-479f-ba28-0ebb48212d46` |
| Lemon tree | `9836ddfb-b4f6-4bc5-9f27-e686e7a14f2f` |
| Cucumber / tomato vine | `4447d8e3-e98b-48c4-ada5-30fdfad8313a` |
| Chives | `cdda838b-9e93-4013-a5ec-4a66fff37e29` |
| Basil | `b4e92724-844a-477c-b821-668c3aa1043a` |
| Grass clump | `6fb05a3f-f141-4b94-8e39-18d19337cc49` |

To re-download them, use the BlendKit add-on in Blender (logged in, resolution set to 1024), or run `bpy.ops.scene.blenderkit_download(asset_base_id=...)`.

- The hero film frames and the elevation and section drawings were generated with AI image tools from the prompts in `v2-video/`. The clips were generated with Kling 4.0.
