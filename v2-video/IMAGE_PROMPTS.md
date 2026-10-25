# Boreä hero film: image prompts (V2, frames only)

15-second hero video for the soumission. No text, no people. Built from **16 still frames** that later become start and end frames for the video model. Every element comes from the Boreä sheet (`assets/borea-fiche.jpg`). The smart-home actions come from the soumission itself (blinds, radiant floor, greenhouse irrigation, server rack, smart lock, lighting scenes, Thermeä session).

Target model: GPT Image 2 or NanoBanana Pro. Use **the same model for all 16**, landscape **16:9**, the highest resolution available.

---

## 1. What the film reference teaches (ASCIA landing film, 11.5 s)

| Observed | Applied here |
|---|---|
| Photoreal architectural visualization, no people, no clutter | Same calm framing, but written as a **real photograph** (after take 1 read as CGI) |
| One smart action per shot (blinds rise, sprinklers pop, towel rail, shower thermostat) | One action per shot, frame A = before, frame B = after |
| Locked or very slow camera, frontal one-point compositions, eye level | Frontal interiors, slow aerials, no tricks |
| In-wall X-ray reveal of the plumbing behind the shower | Floor cutaway revealing the radiant slab (shot 3) |
| Soft overcast daylight, charcoal and grey palette, small LED accents | Same grade; warm light only where a real lamp exists |
| Shots last about 2 s | 9 shots, 1.4 to 2 s each |

## 2. Facts locked from the Boreä sheet (do not deviate)

- **Volume:** one storey, 24 ft wide × 25 ft deep. Single-slope (shed) roof in **black standing-seam metal**, **14 ft at the front, sloping down to 8 ft at the back**, thin black fascia.
- **Cladding:** matte **black vertical metal siding** plus tall panels of **natural honey cedar boards**.
  - Front: narrow cedar panel at the left end, wide full-height cedar panel at the right end, one black cylinder sconce on each.
  - Back: cedar panel on the right third with one window, two windows in the black part.
  - Left side: cedar on the right half (bedroom window), small window in the black half.
  - Right side: cedar panel with a **black exterior door with a tall glass panel** and a sconce, then the greenhouse.
- **Front façade:** almost all **full-height black-framed glazing**: a central sliding door, tall panes, and upper panes following the roof slope.
- **Deck:** covered cedar deck, 24 × 8 ft. Two wooden armchairs with cream cushions and a small round table on the left; a wood dining table with black chairs on the right; potted plants; small warm puck lights along the edge; a bollard light at the left corner; steps down near the centre.
- **Greenhouse:** 10 × 12 ft, **black-framed glass with a pitched glass roof**, attached to the right end and flush with the front. Lush plants, small citrus trees with yellow fruit, warm string lights inside.
- **Roof:** **18 solar panels** (dark blue, thin silver frames), one black plumbing vent pipe, one squat roof ventilator. A black flue pipe is visible on the back.
- **Site:** dense **spruce and fir forest**, granite boulders, ferns, wild grass, grey river stones along the wall base. Summer, everything green.
- **Thermeä:**
  - Steps lead to a **flagstone path**, then a **circular stone patio** with a **round stone fire pit** ringed by **six lounge chairs with cream cushions**.
  - **Barrel sauna** (horizontal, wood, dark steel bands) on a wooden platform to the **left**.
  - **Square hot tub** with a silver-grey cabinet to the **right**, and a **round dark-wood cold-plunge tub** further right.
  - Warm ground lanterns everywhere; a second path continues downhill.
- **Interior:**
  - White **cathedral ceiling rising toward the front glass**, recessed downlights, **wide oak plank floor**, white walls.
  - Left wall: **black linear gas fireplace with a TV above**.
  - **Cream L-shaped sectional** on a beige rug, round wood coffee table.
  - **Wood dining table with six black chairs**.
  - **White kitchen island with a double sink and three black stools**; white counter with a black cooktop on the right wall.
  - **White wall-mounted heat pump** high on the back wall.
- **Mechanical room** (5 × 12 ft): filtration unit, blue rainwater tank, 60-gallon water heater, heat-pump water heater, central vacuum, solar batteries. The wall-mounted 9U network rack comes from the soumission.
- **Slab:** insulated monolithic slab with **red PEX hydronic radiant tubing** (from the section drawing).

> **One inconsistency in the sheet:** the front elevation leaves out the greenhouse. The plan, the right-side elevation and the Thermeä view all place it at the right end, flush with the front. These prompts follow those three.

## 3. Shot list (15.0 s)

| Shot | Time | Frames | What happens | ASCIA system |
|---|---|---|---|---|
| 1 | 0.0–1.8 | 01 → 02 | Dawn aerial; the sun rises across the façade and the solar roof | Solar energy |
| 2 | 1.8–3.8 | 03 → 04 | Living room; roller blinds rise and reveal deck and forest | Motorized blinds |
| 3 | 3.8–5.4 | 05 → 06 | Floor-level view; the oak floor turns into a cutaway of the radiant slab | Climate, radiant floor |
| 4 | 5.4–7.2 | 07 → 08 | Greenhouse; drip lines and misting switch on | Rainwater irrigation |
| 5 | 7.2–8.6 | 09 | Mechanical room; rack, batteries and water equipment, LEDs alive | The brain (local server) |
| 6 | 8.6–10.0 | 10 | Side door at dusk; smart lock glowing, camera under the eave | Security and access |
| 7 | 10.0–11.8 | 11 → 12 | Living room at blue hour; the evening scene turns on, fireplace lit | Lighting scenes |
| 8 | 11.8–13.6 | 13 → 14 | Thermeä; fire, hot tub lights and lanterns come on | Thermeä session |
| 9 | 13.6–15.0 | 15 → 16 | Night aerial pulls back to the framing of frame 01 | The whole home |

Frame 16 matches the framing of frame 01, so the film can loop cleanly from night back to dawn.

## 4. Reference crops (attach these, not the whole sheet)

The whole sheet carries titles, labels and leader lines. Attached as-is, the model draws them and copies the illustration style. Use these clean crops in `soumission/v2-video/refs/`:

| File | Use it only for |
|---|---|
| `ref1-facade-avant.jpg` | Not used for exteriors anymore: its roof line runs the wrong way |
| `ref1b-facade-avant-sans-toit.jpg` | Front glazing, cedar panels, sconces and deck, without the misleading roof line |
| `ref2-cote-droit-serre.jpg` | Right side: cedar panel, side door, sconce, greenhouse structure and planting |
| `ref3-facade-arriere.jpg` | Back façade: windows, cedar panel, flue pipe |
| `ref4-cote-gauche.jpg` | Left side: windows and cladding split |
| `ref5-plan.jpg` | Room layout and furniture or equipment placement |
| `ref6-thermea.jpg` | Thermeä layout: positions of path, fire pit, chairs, sauna, hot tub, cold tub |
| `ref7-toit-solaire.jpg` | Solar panel arrangement and roof vents |
| `ref8-coupe.jpg` | Ceiling heights and slab/radiant-floor construction |

## 5. Generation order (continuity chain)

1. Generate **01** and approve it. It becomes the master exterior.
2. **02** = edit of approved 01.
3. **03**, then **04** = edit of 03. The approved 04 is the master interior.
4. **05** (attaching 04), then **06** = edit of 05.
5. **07** (attaching 02), then **08** = edit of 07.
6. **09**.
7. **10** (attaching 02).
8. **11** (attaching 04), then **12** = edit of 11.
9. **13** (attaching 02), then **14** = edit of 13.
10. **15** (attaching 01 and 14), then **16** = edit of 15.

Every "B" frame is made **in edit mode on its approved "A" frame**, so only the named change happens.

---

## 6. The prompts

### Frame 01 · Shot 1A · Dawn aerial (master exterior) · v2

**Attach, in this order:** `ref1b-facade-avant-sans-toit.jpg`, `ref2-cote-droit-serre.jpg`, `ref3-facade-arriere.jpg`, `ref6-thermea.jpg`, `ref7-toit-solaire.jpg`

> v2 after the take 1 review. Changes: the roof direction is locked, the site is flat, the forest closes the background, counts are fixed, and the style now asks for a real photograph instead of a render. `ref1` is replaced by `ref1b`, cropped below the sheet's misleading roof line.

```
First attached image: the lower part of the front façade — use it only for the glazing, the cedar panels, the sconces and the deck. Second attached image: the right side — use it only for the roof profile (tall at the front, low at the back) and the attached greenhouse. Third attached image: the back façade — use it only to see that the back is the low side, with the black flue pipe. Fourth attached image: a top view of the site — use it only for the positions of the deck, steps, paths, fire pit, chairs, sauna, hot tub and cold tub. Fifth attached image: the roof — use it only for the solar panel arrangement and the vents. The attachments are drawings; the result is a real photograph of a real place.

A real aerial photograph of the Boreä chalet at dawn, taken by an architectural photographer with a drone on the morning of the handover. A single-storey Nordic modern cabin, 24 ft wide and 25 ft deep. Its single-slope black standing-seam metal roof is highest along the front, above the deck, at 14 ft, and falls toward the back to 8 ft; the front façade is the tallest wall and the two side walls taper from tall at the front to low at the back. From this raised viewpoint we look down onto the roof plane as it falls away from the camera, carrying 18 dark-blue solar panels with thin silver frames in three rows of six, with one black flue pipe, one plumbing vent and one squat roof ventilator near the low back edge. The walls are matte black vertical metal siding with tall panels of honey-toned vertical cedar boards. The front façade is full-height black-framed glazing from the deck to the 14 ft fascia — a lower row of tall panes with a central sliding door and an upper row of transom panes — between a narrow cedar panel at the left end and a wide full-height cedar panel at the right end, each with one black cylindrical sconce. A 10 × 12 ft greenhouse of black-framed glass with a pitched glass roof is attached to the right end, flush with the front façade, full of leafy plants and small citrus trees with yellow fruit; its glass end wall is the right edge of the building.

The covered cedar deck runs the full width, about 2 ft above the ground, with three wide wooden steps down at the centre; on it, two wooden armchairs with cream cushions and a small round table on the left, and a wooden dining table with six black chairs on the right. The clearing is nearly flat. About 10 m in front of the steps, on the same level, a flagstone path reaches a circular stone patio: a round stone fire pit, unlit, ringed by six lounge chairs with cream cushions; on the left a horizontal wooden barrel sauna with dark steel bands on a low wooden platform, its glass door facing the fire pit; on the right a square hot tub with a silver-grey cabinet, set level on a gravel pad; further right a round dark-wood cold-plunge tub. Small black path lanterns, unlit, along the flagstones. Around the clearing, a dense forest of tall spruce and fir of uneven heights rises on every side and fills the background up to a thin band of sky.

Composition: the cabin and greenhouse in the upper-right third, the Thermeä patio in the lower-left third, the flagstone path linking them as a leading line; spruce tops crowd the frame edges.

Camera: drone about 18 m high and 35 m in front of the cabin, offset to the right, looking down about 35°, 24 mm full-frame equivalent, f/2.8, 1/15 s, ISO 800, shot in RAW, verticals corrected.

Lighting: twenty minutes before sunrise. The brightest part of the sky is behind the camera, in the east, so the front glazing reflects a pale pink-grey dawn glow, while the sky beyond the house is still deep blue. Soft, almost shadowless light; the cabin interior is dark; low mist lies between the spruce trunks and thins out over the clearing. Exposed for the sky glow, so the forest floor and the space under the deck fall into deep shadow.

Mood: still, awakening.

Realism: granite boulders of varied size and shape, half sunk into the ground, with grey-green lichen, moss and rust stains; a real forest floor of lowbush blueberry, bracken, dry spruce needles and fallen twigs between uneven young conifers; flagstones irregular and slightly uneven, set in gravel and moss; dew on the deck boards, the cushions and the hot tub cabinet; a few spruce needles on the deck; fine sensor noise in the shadows and gentle lens vignetting.

Style: a real photograph, not a render — natural irregularity, true optical behaviour, honest exposure.

Colour grade: neutral and slightly cool dawn tones, low contrast, deep but detailed shadows, muted natural greens, the pale pink glow only where the glass reflects the eastern sky.

16:9 landscape. No people, no animals, no text, no labels, no logos, no watermark; no CGI look, no HDR, no oversaturation, no fisheye.
```

**Approve when:**
- the front wall is the tallest wall and the roof falls away toward the back;
- the side walls taper;
- the glazing reaches the fascia;
- the greenhouse's glass end is the right edge of the building;
- the deck is low, with three steps;
- the Thermeä is on flat ground;
- there are six chairs around the fire pit and six at the deck table;
- forest fills the background;
- rocks and shrubs look varied, not cloned.

---

### Frame 02 · Shot 1B · Sunrise (edit of 01)

**Attach:** approved frame 01 (edit mode)

```
The exact same image: same camera, same composition, same cabin, same site. Only the light changes. The sun has just risen at the left of frame: low warm golden sunlight rakes across the front glazing, the cedar panels and the deck boards; long soft shadows from the spruce trees stretch across the clearing; the mist is lifting and glows where the sunlight crosses it; the solar panels on the roof pick up a soft sheen of light. The cabin interior stays dark and every exterior light stays off. Everything else unchanged. Colour grade: neutral with warm sunlight, deep charcoal blacks, natural greens. 16:9. No people, no text.
```

---

### Frame 03 · Shot 2A · Living room, blinds down

**Attach, in this order:** `ref5-plan.jpg`, `ref8-coupe.jpg`, `ref1b-facade-avant-sans-toit.jpg`

```
First attached image: the floor plan — use it only for the room layout and the furniture placement in the open living space. Second attached image: the section — use it only for the ceiling shape and heights. Third attached image: the front façade — use it only for the pattern of the full-height glazing, seen here from inside. The attachments are drawings; render a real, photographed interior.

Inside the Boreä open living space (24 × 13 ft), early morning, seen from the back of the room looking straight toward the full-height front glazing. A white cathedral ceiling rises from the back toward the glass, with small recessed downlights (off); a wide natural oak plank floor; white walls. On the left wall, a long black linear gas fireplace with a wall-mounted TV above it, and facing it a light cream L-shaped sectional sofa on a beige rug with a round wooden coffee table holding a plant. In the centre, a solid wood dining table with six black chairs and a plant centrepiece. On the right, a white kitchen island with a double sink and three black stools, and a white counter with a black cooktop along the right wall. Potted plants in the corners.

Every tall window pane is covered by a lowered motorized roller blind: light-grey translucent screen fabric hanging from a slim black cassette at the top of each pane, the bottom bar just above the floor. Daylight glows softly through the fabric; the upper panes that follow the roof slope have no blinds and let in a band of cool sky light.

Composition: one-point frontal symmetry, the vanishing point centred on the glazing, the ceiling slope leading the eye to the windows, the dining table in the midground, the floor occupying the bottom third.

Camera: standing at the back of the living space near the bedroom wall, eye level at 1.5 m, 24 mm, f/8, everything sharp, verticals corrected.

Lighting: soft, low, diffuse morning light filtered through the blind fabric, cool white balance, gentle falloff toward the back of the room, no lamps on.

Mood: calm, still.

Realism: a fine visible weave in the blind fabric, oak grain and fine seams, a faint reflection of the room in the glass above the blinds.

Style: a real architectural photograph, not a render — natural irregularity, true optical behaviour, honest exposure.

Colour grade: neutral and slightly cool, deep charcoal blacks, soft highlight roll-off.

16:9 landscape. No people, no text, no labels, no logos, no watermark; not an illustration; no fisheye, no HDR halos.
```

---

### Frame 04 · Shot 2B · Blinds up (edit of 03, master interior)

**Attach:** approved frame 03 (edit mode)

```
The exact same image: same camera, same room, same furniture. Only the blinds change: every roller blind is fully raised and rolled up into its slim black cassette at the top of the pane. Through the full-height glazing we now see the covered cedar deck — two wooden armchairs with cream cushions and a small round table on the left, a wooden dining table with black chairs on the right, potted plants — and beyond it the dense spruce and fir forest in soft morning light. Daylight now floods the room and lays long window-shaped light patches across the oak floor. Everything else unchanged. 16:9. No people, no text.
```

---

### Frame 05 · Shot 3A · Floor level, radiant floor (before)

**Attach, in this order:** approved frame 04, `ref8-coupe.jpg`

```
First attached image: the approved interior — use it for the room's identity: same materials, furniture, colours and light. Second attached image: the section drawing — use it only for the floor and slab construction. Render a real, photographed interior.

The same Boreä open living space, seen from floor level in the morning: a wide natural oak plank floor in the foreground, the light cream L-shaped sectional, the round wooden coffee table and the black linear gas fireplace with the TV above it on the left wall in the background, the dining table with black chairs in the midground, the white cathedral ceiling rising toward the full-height glazing on the right, where the blinds are raised and the forest is visible.

Composition: the floor fills the lower half of the frame, its plank lines leading diagonally toward the sofa and the fireplace; furniture in the upper half; the glazing at the right edge.

Camera: lens 30 cm above the floor, placed near the kitchen island and looking diagonally left across the room, 28 mm, f/8, deep focus, verticals corrected.

Lighting: morning sunlight through the front glazing casting soft, long light patches across the oak floor from the right; cool ambient fill from the sky; no lamps on.

Mood: warm, quiet.

Realism: fine oak grain, subtle plank seams, a soft sheen where the sun hits the floor.

Style: a real architectural photograph, not a render — natural irregularity, true optical behaviour, honest exposure.

Colour grade: neutral and slightly cool, warm sunlight, deep charcoal blacks.

16:9 landscape. No people, no text, no labels, no logos, no watermark; no fisheye, no HDR halos.
```

---

### Frame 06 · Shot 3B · Radiant floor revealed (edit of 05)

**Attach:** approved frame 05 (edit mode)

```
The exact same image: same camera, same room, same light. Only the foreground floor changes: a precise rectangular section of the oak floor, about 3 by 2 metres with perfectly straight edges, becomes an architectural cutaway, as if the planks were made invisible. Beneath it we see the insulated monolithic concrete slab, with a layer of rigid grey insulation board below, and red PEX hydronic radiant-heating tubes laid in a tight, even serpentine loop pattern embedded in the concrete, giving off a faint warm glow. The cut edges show the thickness of the oak planks and the slab layers cleanly, rendered photoreal in the same light as the rest of the image. Everything else unchanged. 16:9. No people, no text, no labels.
```

---

### Frame 07 · Shot 4A · Greenhouse, before watering

**Attach, in this order:** `ref2-cote-droit-serre.jpg`, approved frame 02

```
First attached image: the right side of the cabin — use it only for the greenhouse structure (black frame, glass walls, pitched glass roof) and its planting. Second attached image: the approved exterior — use it only for materials and morning light. Render a real, photographed place.

Inside the Boreä greenhouse (10 × 12 ft) in the morning: thin black aluminium glazing bars, clear glass walls and a pitched glass roof overhead. Cedar raised planting beds full of lush growth — cherry tomato vines on stakes, broad cucumber leaves, a row of basil — and small potted citrus trees with yellow fruit. Black drip-irrigation lines run along the soil with small emitters at each plant; a slim black misting line with fine nozzles runs along the roof ridge; a strand of small bulb string lights hangs along the roof bars, switched off. Through the glass, the dense spruce forest.

Composition: foreground the soil and a drip emitter in sharp focus at the lower left, midground the tomato and basil leaves, background the glass wall, black mullions and the forest softly out of focus; the roof bars form leading lines toward the light.

Camera: low, 60 cm above the bed, 35 mm, f/2.8, shallow depth of field, focus on the drip line in the foreground.

Lighting: low morning sun backlighting the leaves through the glass roof, translucent glowing leaf edges, soft fill from the white sky.

Mood: fresh, alive.

Realism: dry surface on the soil, fine hairs on the tomato stems, dust and faint water marks on the glass.

Style: a real architectural photograph, not a render — natural irregularity, true optical behaviour, honest exposure.

Colour grade: natural vivid greens, neutral whites, deep charcoal blacks on the frame.

16:9 landscape. No people, no text, no labels, no logos, no watermark; no HDR halos, no oversaturation.
```

---

### Frame 08 · Shot 4B · Irrigation on (edit of 07)

**Attach:** approved frame 07 (edit mode)

```
The exact same image: same camera, same focus, same light. Only the watering changes: each drip emitter releases beads of water that darken the soil in a circle around it, a fine mist sprays from the nozzles along the roof ridge and drifts down through the backlit sun rays, catching the light, and small droplets sit on the leaves. Everything else unchanged. 16:9. No people, no text.
```

---

### Frame 09 · Shot 5 · Mechanical room, the brain

**Attach, in this order:** `ref5-plan.jpg`, `ref8-coupe.jpg`

```
First attached image: the floor plan — use it only for the equipment in the mechanical room (top right of the plan) and its placement. Second attached image: the section — use it only for the room's 8 ft flat ceiling. Render a real, photographed room.

The Boreä mechanical room, a narrow 5 × 12 ft utility room with an 8 ft flat white ceiling, matte white walls and a smooth grey sealed-concrete floor, seen from the doorway looking along its length. Along the walls, neatly installed: a white filtration unit with cartridge housings, a blue cylindrical rainwater storage tank, a white 60-gallon water heater, a compact heat-pump water heater, a white central vacuum unit, and a dark-grey solar battery cabinet with a small glowing status light. On the right wall at chest height, a compact wall-mounted black 9U network cabinet with a glass door: a small server, a 16-port network switch with tiny green and amber port lights, a network gateway and neatly dressed cables; beside it a slim energy gateway with a small status light. Copper and PEX pipes run in clean parallel lines.

Composition: one-point perspective down the length of the room, the network cabinet in the right third as the hero, equipment receding on both sides, the floor's soft reflection leading the eye.

Camera: standing in the doorway, eye level at 1.5 m, 18 mm, f/8, deep focus, verticals corrected.

Lighting: cool white light from a linear LED fixture along the ceiling, even and clean, soft shadows under the equipment, the small status lights glowing.

Mood: precise, quiet.

Realism: faint scuffs on the concrete, slight sheen on the white appliances, cable ties and labels without readable text.

Style: a real architectural photograph, not a render — natural irregularity, true optical behaviour, honest exposure.

Colour grade: neutral and slightly cool, deep charcoal blacks, small green and amber accents.

16:9 landscape. No people, no readable text, no logos, no watermark; no fisheye, no HDR halos.
```

---

### Frame 10 · Shot 6 · Side door at dusk, smart lock

**Attach, in this order:** `ref2-cote-droit-serre.jpg`, approved frame 02

```
First attached image: the right side of the cabin — use it only for the cedar panel, the black exterior door with its tall glass panel, the wall sconce and the corner of the greenhouse. Second attached image: the approved exterior — use it only for materials and site. Render a real, photographed place.

The side entrance of the Boreä chalet at dusk: a black exterior door with a tall vertical glass panel set into a wall of natural honey-toned vertical cedar boards, a black cylindrical wall sconce to the left of the door glowing warm, matte black vertical metal siding beyond. On the door, a sleek black smart lock with a fingerprint reader, its small ring indicator glowing soft white. Under the black roof eave above the door, a small black security camera. At the right edge of the frame, the corner of the glass greenhouse glows warmly from inside; a strip of grey river stones and young spruce at the base of the wall.

Composition: the door in the left-centre third, the lit sconce and the lock as the brightest points, the greenhouse glow at the right edge, the stone strip as a leading line.

Camera: eye level at 1.6 m, 3 m from the door, slightly off-axis from the left, 35 mm, f/4, focus on the lock.

Lighting: blue-hour sky as cool ambient light, warm 2700 K pool from the sconce on the cedar boards, warm glow spilling from the greenhouse.

Mood: welcoming, secure.

Realism: fine cedar grain and slight weathering, a soft reflection of the sky in the door glass, a soft pool of sconce light on the stones below.

Style: a real architectural photograph, not a render — natural irregularity, true optical behaviour, honest exposure.

Colour grade: cool blue ambient with warm accents only from real lamps, deep charcoal blacks.

16:9 landscape. No people, no text, no logos, no watermark; no HDR halos.
```

---

### Frame 11 · Shot 7A · Living room at blue hour, lights off

**Attach, in this order:** approved frame 04, `ref5-plan.jpg`

```
First attached image: the approved interior — use it for the room's identity: same architecture, materials, furniture and colours. Second attached image: the floor plan — use it only for the furniture placement. Render a real, photographed interior.

The same Boreä open living space at blue hour, seen from the opposite corner: on the left wall the long black linear gas fireplace (off) with the wall-mounted TV (black) above it, the light cream L-shaped sectional on the beige rug with the round wooden coffee table, the solid wood dining table with six black chairs in the midground, the white cathedral ceiling sloping down toward the back wall with small recessed downlights, the full-height front glazing along the left side of the frame with the blinds raised, the deck and the dark spruce forest outside under a deep blue sky.

Composition: diagonal view across the room toward the fireplace wall, the dining table in the midground, the ceiling slope as a strong line, the blue windows on the left balancing the room.

Camera: standing in the front-right corner near the kitchen counter, eye level at 1.5 m, 24 mm, f/8, deep focus, verticals corrected.

Lighting: no lamps on — the room is lit only by cool blue dusk light through the glazing, soft and low, the oak floor catching a faint blue sheen.

Mood: hushed.

Realism: faint reflections of the room in the glass, oak grain, fabric texture on the sofa.

Style: a real architectural photograph, not a render — natural irregularity, true optical behaviour, honest exposure.

Colour grade: cool blue-grey, deep charcoal blacks, low saturation.

16:9 landscape. No people, no text, no logos, no watermark; no fisheye, no HDR halos.
```

---

### Frame 12 · Shot 7B · Evening scene on (edit of 11)

**Attach:** approved frame 11 (edit mode)

```
The exact same image: same camera, same room, same furniture. Only the lighting changes: the evening scene has switched on. The recessed downlights glow at a low warm 2700 K level, a warm LED line glows along the ceiling edge and under the kitchen counter, the black linear gas fireplace is lit with low orange flames, and the plant centrepiece on the dining table catches warm light. The TV stays black, the blinds stay raised, and the windows keep their deep blue dusk sky, so warm light inside contrasts with the blue outside. Everything else unchanged. 16:9. No people, no text.
```

---

### Frame 13 · Shot 8A · Thermeä at blue hour, off

**Attach, in this order:** `ref6-thermea.jpg`, approved frame 02

```
First attached image: a top view of the site — use it only for the layout and positions of the path, fire pit, chairs, barrel sauna, hot tub, cold-plunge tub, boulders and lanterns. Second attached image: the approved exterior — use it for the cabin's identity, materials and site. The first attachment is a drawing; render a real, photographed place.

The Thermeä zone of the Boreä chalet at blue hour, seen from the lower flagstone path looking back up toward the cabin. Foreground: flagstones and granite boulders. Midground: the circular stone patio with the round stone fire pit in the centre, holding neatly stacked unlit wood, ringed by six lounge chairs with cream cushions; on the left the horizontal wooden barrel sauna with dark steel bands on its small wooden platform, its glass door dark; on the right the square hot tub with its silver-grey cabinet, its water dark and still; further right the round dark-wood cold-plunge tub. Background: the flagstone path and wide wooden steps leading up to the covered cedar deck and the cabin's full-height black-framed glazing, warmly lit from inside, the black and cedar façade and the greenhouse glowing at the right, the spruce forest dark against a deep blue sky. The small ground lanterns along the paths are off.

Composition: the path as a leading line from the bottom centre to the fire pit and up to the cabin; sauna left third, hot tub and cold tub right third; the glowing cabin at the top centre.

Camera: standing on the lower path about 6 m beyond the fire pit, eye level at 1.4 m, 24 mm, f/8, deep focus.

Lighting: cool blue-hour ambient from the sky; the only warm light comes from the cabin windows in the background.

Mood: anticipation.

Realism: moss in the flagstone joints, dew on the cushions, a faint reflection of the sky on the hot tub water.

Style: a real architectural photograph, not a render — natural irregularity, true optical behaviour, honest exposure.

Colour grade: cool blue-grey ambient, warm only from the cabin windows, deep charcoal blacks.

16:9 landscape. No people, no text, no labels, no logos, no watermark; not an illustration; no HDR halos.
```

---

### Frame 14 · Shot 8B · Thermeä session on (edit of 13)

**Attach:** approved frame 13 (edit mode)

```
The exact same image: same camera, same composition, same objects. Only the Thermeä comes alive: the fire pit is lit with real flames rising from the stacked wood and throwing flickering warm light on the chairs and stones; the hot tub's underwater lights glow soft aqua and steam rises from its surface; the barrel sauna's glass door glows amber from inside; the cold-plunge tub stays dark and still; every small ground lantern along the paths and the puck lights along the deck edge are on, laying warm pools of light on the flagstones and boulders. The sky stays deep blue. Everything else unchanged. 16:9. No people, no text.
```

---

### Frame 15 · Shot 9A · Night aerial, close

**Attach, in this order:** approved frame 01, approved frame 14

```
First attached image: the approved dawn aerial — use it for the cabin's identity, the site layout and the camera direction. Second attached image: the approved Thermeä at night — use it only for the night lighting state (lit interior, fire, hot tub lights, lanterns). Render a real, photographed place.

The Boreä chalet and its Thermeä at night, seen from the air from the same direction as the first attachment but closer and lower. The cabin glows from inside through the full-height front glazing, the two black cylindrical sconces light the cedar panels, the deck's puck lights trace its edge, the greenhouse glows warm with its string lights, and the 18 solar panels on the black roof catch faint sky light. Below the deck, the Thermeä is fully lit: the fire pit burning, the hot tub glowing aqua with rising steam, the barrel sauna's door glowing amber, ground lanterns along every path. The dense spruce forest is dark around the clearing; a thin band of deep blue night sky above the treeline.

Composition: the cabin in the upper-right third and the Thermeä in the lower-left third, as in the first attachment, but filling more of the frame.

Camera: aerial drone about 8 m high, 22 m from the cabin, offset to the right, looking down about 20°, 24 mm full-frame equivalent, f/4, everything sharp.

Lighting: deep blue night ambient, warm 2700 K light from the windows, sconces, deck lights and lanterns, flickering firelight, aqua glow from the hot tub.

Mood: serene.

Realism: steam catching the light above the hot tub, soft light spill on the tree trunks nearest the clearing, true reflections in the glazing.

Style: a real architectural photograph, not a render — natural irregularity, true optical behaviour, honest exposure.

Colour grade: deep blue night with warm and aqua accents from real sources, deep charcoal blacks.

16:9 landscape. No people, no animals, no text, no labels, no logos, no watermark; no HDR halos, no oversaturation.
```

---

### Frame 16 · Shot 9B · Night aerial, pull-back (edit of 15)

**Attach:** approved frame 15 (edit mode). Keep approved frame 01 at hand to compare the framing.

```
The exact same scene, same night lighting, same cabin and Thermeä. Only the camera changes: it has risen and pulled back to about 15 m high and 40 m from the cabin, looking down about 25°, the framing of the dawn aerial — the cabin and greenhouse in the upper-right third, the Thermeä in the lower-left third, more of the dark spruce forest around the clearing, and a thin band of deep blue night sky with a few faint stars above the treeline. Everything else unchanged. 16:9. No people, no text.
```

---

## 7. Checks on every frame before approving

- Is everything in it on the Boreä sheet or in the soumission? Remove anything else: no extra buildings, no second storey, no snow, no different furniture.
- Exterior: a single-slope roof that is high at the front, black siding with cedar panels where the sheet shows them, the greenhouse on the right.
- Interior: the ceiling rises toward the glass, the fireplace with the TV is on the left wall, and the island has a double sink.
- Continuity: B frames differ from their A frames only in the named change.
- No text anywhere. Displays and labels stay unreadable; mask them in the edit if needed.
