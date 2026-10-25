# Boreä frames: review log

One entry per generated take. Each mistake is traced to the prompt line or reference that caused it, with the rule that prevents it.

## Frame 01 · take 1 (2026-10-25): rejected, regenerate with v2

File: `takes/frame01-take1.webp` (1672×941)

**Keep:**
- The composition: house upper right, Thermeä lower left.
- The cladding split, with cedar at both ends of the front and the sconces.
- The greenhouse with citrus, flush with the front.
- The barrel sauna with its door facing the fire pit; the hot tub to the right, the cold tub furthest right.
- 18 panels, the flue and vents, the unlit path lanterns, mist in the trees.

**Mistakes, causes and fixes:**

| # | Mistake | Cause | Fix |
|---|---|---|---|
| 1 | Roof rises toward the back; front wall reads as the low side | `ref1` (front elevation) draws the roof slope across the front façade, contradicting the section (14 ft front, 8 ft back) | New crop `ref1b` below the roof line; added `ref2` (profile) and `ref3` (low back); the prompt names the tall front wall and tapered side walls |
| 2 | Extra cedar volume with a door to the right of the greenhouse | The side door in `ref2` was placed literally beside the greenhouse | Prompt: "its glass end wall is the right edge of the building" |
| 3 | Deck high on a rocky slope, 5 steps; Thermeä down a hillside | Unstated terrain, so the model invented drama | "Nearly flat clearing, deck about 2 ft up, three steps, patio on the same level" |
| 4 | Valley, distant mountains and pink horizon behind the house | Unstated background | "Forest rises on every side and fills the background up to a thin band of sky" |
| 5 | 4 chairs around the fire pit, 8+ at the deck table | Counts not repeated strongly | "six lounge chairs", "six black chairs" |
| 6 | Reads as CGI: even tone-mapped light, cloned boulders and baby spruces, showroom-clean furniture, everything sharp | The style line literally asked for "photoreal architectural visualization" | Real-photograph framing (drone, RAW, settings), physical dawn light direction, exposure for the sky, 4 chosen imperfections (lichen and moss, forest-floor litter, dew, sensor noise) |

**Rule kept for every frame:** never write "architectural visualization" or "render" in a style line. Describe a real photograph and how it was shot.

## Round 2 · frames 01–16 (2026-10-25)

Takes are saved in `takes/` as `frameNN-takeN.webp`. Frame 15 was not delivered.

| Frame | Verdict | Notes |
|---|---|---|
| 01 · take 2 | **Approved** | Roof, low deck with three steps, flat clearing, six chairs, greenhouse as the right edge: all correct. Realism is much better. Minor: the pink glow sits behind the house instead of behind the camera. |
| 02 | Usable with an edit | The sun disc sits in the frame behind the house, yet the façade facing the camera is lit. The house faces east, so the sunrise is behind the camera. Too orange overall. |
| 03 | **Approved** | Fireplace with TV on the left wall, cream sectional, six chairs, double-sink island, three stools, blinds on the tall panes, transoms clear. |
| 04 | Approved; optional edit | Blinds up, continuity perfect, morning sun from the front (correct for an east façade). The view looks over treetops, so the site reads as raised; the sheet shows a level clearing. |
| 05 | **Approved** | Ceiling rises toward the glass; strong realism. |
| 06 | Usable with an edit | Neon-red tubes lie on top of the slab. They should be matte and set into the concrete with a faint warmth, like the film's subtle in-wall reveal. |
| 07 | **Approved** | Excellent. Optional: a drop already hangs at the emitter in the "before" frame. |
| 08 | **Approved** | Mist and droplets, identical framing. |
| 09 | Usable with an edit | Every sheet item is present (filtration, blue rainwater tank, 60 gal heater, heat-pump water heater, central vacuum, batteries, rack). An outdoor condenser unit with a fan grille stands in the lower left; it isn't on the sheet. |
| 10 | Usable with an edit | Door, cedar, sconce, smart lock, camera, greenhouse: correct. The background shows a lake and hills; the site is enclosed forest. |
| 11 | **Approved** | Glazing on the left, fireplace wall facing the camera, deck dining near and armchairs far: consistent with the plan. |
| 12 | **Approved** | Evening scene on, identical framing. |
| 13 | **Edit required** | The roof plane and solar panels are visible from eye level, so the roof rises toward the back. The front wall is the tallest and should hide the roof, leaving only the fascia and the top of the flue. |
| 14 | Redo from the fixed 13 | It inherits the roof problem. Night colours are oversaturated (orange cushions, saturated greens). |
| 15 | Missing | Generate it from the fixed 16 (camera closer). |
| 16 | Usable with an edit | A black volume with a window appears to the right of the greenhouse (it doesn't match 01); the paving turns into round wood slices instead of grey flagstones; oversaturated. |

**Lessons for the next frames:**
- In eye-level exteriors, write what hides the roof: "the front wall is the tallest; from here only the fascia and the top of the flue show".
- Always name the paving material and the building's right edge in every exterior, including night frames.
- For night exteriors, say "muted greens, off-white cushions": warm lights push the model into an orange cast.

## Drawings · round 1 (2026-10-25)

Saved in `drawings/`; trimmed, paper-matched versions are in `assets/projet/elev-*-v2.jpg`.

| Drawing | Verdict | Notes |
|---|---|---|
| E1 front | **Approved** | Tall front with a straight horizontal top, full-height glazing with transoms, cedar at both ends, deck with centre steps, greenhouse flush on the right. |
| E2 back | **Approved, one deviation** | 8 ft wall, windows and cedar panel match the sheet, the roof rises away with panels and flue. It shows 21 panels (7 × 3) instead of 18; invisible at page size. |
| E3 left | **Approved** | Slope rises toward the front, black and cedar split, covered deck with a post on the right. |
| E4 right | **Approved** | Roof rises toward the greenhouse (front) end; black siding, cedar with door, smart lock and sconce, then the greenhouse, in the sheet's order. |
| C1 section | **Approved** | One continuous slope from 14 ft to 8 ft, cathedral living area, flat 8 ft ceilings with the attic void, slab with insulation, gravel and red PEX tubes in cross-section. Labels are added in HTML on the page. |
