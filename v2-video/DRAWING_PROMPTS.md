# Boreä drawings for the "Le projet" section: image prompts

These replace the blurry crops from the sheet: the four elevations, the architectural section, and optionally the plan and the roof view.

**Rules for all of them:**
- **No text in the images.** Room names, dimensions and callouts are added afterwards as sharp HTML labels on the page. AI can't spell, and baked labels go blurry.
- **Same house as the film.** Each prompt attaches the approved film frames, so the drawings match what people just watched.
- **Background:** plain warm off-white (#F3F0E9), the colour of the page's drawing panels, so the images sit in the page without a visible box.
- Use the same image model as the frames, at the highest resolution available.

## Geometry fixed once, used everywhere

The sheet contradicts itself, so this is the version every prompt uses. It follows the section drawing and the film.

- **Roof:** single slope in black standing-seam metal, **14 ft at the front** (deck side) and **8 ft at the back**.
- **Front façade:** the tallest wall, with a straight horizontal top.
- **Side walls:** tapered, tall at the front end and low at the back end.
- **Back façade:** 8 ft high with a straight top. From behind you see the roof rising away, carrying the solar panels, as in the sheet's back elevation.
- **Greenhouse:** at the right end of the front, flush with the front façade.
- **Each side keeps the cladding and window layout of its panel on the sheet**, so the images still read as the sheet.

Files to attach are in `soumission/v2-video/refs/` and `soumission/v2-video/takes/`.

---

## E1 · Front elevation

**Attach, in this order:** `takes/frame01-take2.webp`, `refs/ref1b-facade-avant-sans-toit.jpg` · **Ratio:** 16:9

```
First attached image: the approved photo of the cabin — use it for the exact materials, colours, glazing and greenhouse. Second attached image: the lower front façade from the design sheet — use it only for the layout of the glazing, cedar panels, sconces and deck.

A photoreal architectural front elevation of the Boreä chalet, seen perfectly straight-on in orthographic projection — no perspective, no vanishing points, all vertical and horizontal lines parallel to the frame. The front façade is 24 ft wide and 14 ft tall with a straight horizontal top edge: a thick black metal fascia of the single-slope roof. Almost the whole façade is full-height black-framed glazing: a lower row of tall panes with a central sliding glass door and an upper row of transom panes. A narrow panel of honey-toned vertical cedar boards at the left end and a wide full-height cedar panel at the right end, each with one black cylindrical wall sconce. Inside, glimpsed through the glass: warm interior with the cream sofa, the wood dining table and plants. In front, the covered cedar deck about 2 ft above the ground with three wide steps at the centre, two wooden armchairs with cream cushions on the left and a wooden dining table with black chairs on the right, potted plants. Attached to the right end, flush with the front, the 10 ft wide glass greenhouse with thin black frames and a pitched glass roof, full of leafy plants and small citrus trees with yellow fruit. Along the base, a strip of grey river stones and a few young spruce.

Composition: the full building centred with generous even margins, ground line in the lower quarter, a thin soft contact shadow on the ground. Behind the building, a few dark spruce trees cut out cleanly. Background: plain warm off-white (#F3F0E9), seamless.

Lighting: soft, even overcast daylight from the front so every material reads clearly; the interior lights on, warm 2700 K, glowing through the glass.

Realism: real cedar grain, fine ribs on the black metal, true glass reflections, slight weathering on the deck boards.

Style: a clean, photoreal architectural presentation elevation, as in a premium builder's catalogue.

Colour grade: neutral, true-to-material colours, deep charcoal blacks, honey cedar.

16:9 landscape. No text, no labels, no dimensions, no arrows, no logos, no watermark, no perspective distortion.
```

## E2 · Back elevation

**Attach, in this order:** `takes/frame01-take2.webp`, `refs/ref3-facade-arriere.jpg` · **Ratio:** 16:9

```
First attached image: the approved photo of the cabin — use it for the exact materials, colours, roof and solar panels. Second attached image: the back façade from the design sheet — use it only for the window positions, the cedar panel and the flue pipe.

A photoreal architectural back elevation of the Boreä chalet, perfectly straight-on in orthographic projection — no perspective, all lines parallel to the frame. The back wall is 24 ft wide and 8 ft tall with a straight horizontal top and black fascia. It is clad in matte black vertical metal siding, with a panel of honey-toned vertical cedar boards over the right third. In the black part, one small single window on the left and one wider double window in the middle; in the cedar panel, one window. All windows have black frames, with warm light behind them. Above the back wall, the black standing-seam roof rises away from the viewer toward the 14 ft front edge, seen as a sloping band carrying the 18 dark-blue solar panels with thin silver frames, foreshortened; one black flue pipe and one squat roof vent stand near the back edge. A strip of grey river stones, a few granite stones and young spruce at the base, with small warm ground lights.

Composition: the building centred with generous even margins, ground line in the lower quarter, soft contact shadow. A few dark spruce trees behind, cut out cleanly. Background: plain warm off-white (#F3F0E9), seamless.

Lighting: soft, even overcast daylight; warm 2700 K light inside the windows.

Realism: fine ribs on the metal siding and roof, real cedar grain, subtle reflections on the panels.

Style: a clean, photoreal architectural presentation elevation, as in a premium builder's catalogue.

Colour grade: neutral, true-to-material colours, deep charcoal blacks, honey cedar.

16:9 landscape. No text, no labels, no dimensions, no arrows, no logos, no watermark, no perspective distortion.
```

## E3 · Left side (bedroom)

**Attach, in this order:** `takes/frame01-take2.webp`, `refs/ref4-cote-gauche.jpg` · **Ratio:** 16:9

```
First attached image: the approved photo of the cabin — use it for the exact materials and colours. Second attached image: the left side from the design sheet — use it only for the split between black siding and cedar and the two window positions.

A photoreal architectural side elevation of the Boreä chalet, left side, perfectly straight-on in orthographic projection — no perspective, all lines parallel to the frame. The side wall is 25 ft long and tapers: its top edge rises in one straight slope from 8 ft at the left end (the back of the cabin) to 14 ft at the right end (the front), following the black single-slope roof, whose thin black edge is visible along the top. The left half of the wall is matte black vertical metal siding with one small black-framed window; the right half is honey-toned vertical cedar boards with one black-framed bedroom window; warm light behind both. At the right, the covered cedar deck projects 8 ft beyond the front corner, about 2 ft above the ground, with the edge of an armchair with cream cushions visible on it. Grey river stones and young spruce along the base.

Composition: the building centred with generous even margins, ground line in the lower quarter, soft contact shadow. A few dark spruce trees behind, cut out cleanly. Background: plain warm off-white (#F3F0E9), seamless.

Lighting: soft, even overcast daylight; warm 2700 K light inside the windows.

Realism: fine metal ribs, real cedar grain, slight weathering on the deck edge.

Style: a clean, photoreal architectural presentation elevation, as in a premium builder's catalogue.

Colour grade: neutral, true-to-material colours, deep charcoal blacks, honey cedar.

16:9 landscape. No text, no labels, no dimensions, no arrows, no logos, no watermark, no perspective distortion.
```

## E4 · Right side (greenhouse)

**Attach, in this order:** `takes/frame10-take1.webp`, `takes/frame01-take2.webp`, `refs/ref2-cote-droit-serre.jpg` · **Ratio:** 16:9

```
First attached image: the approved photo of the side door — use it for the exact door, cedar, sconce, siding and greenhouse frame. Second attached image: the approved photo of the whole cabin — use it for the overall look. Third attached image: the right side from the design sheet — use it only for the order of the elements from left to right.

A photoreal architectural side elevation of the Boreä chalet, right side, perfectly straight-on in orthographic projection — no perspective, all lines parallel to the frame. From left to right: a section of matte black vertical metal siding; a panel of honey-toned vertical cedar boards holding a black exterior door with a tall glass panel, a black cylindrical sconce glowing warm to its left and a small black smart lock on the door; then the 10 × 12 ft glass greenhouse with thin black aluminium frames and a pitched glass roof, full of leafy plants and small citrus trees with yellow fruit, warm string lights inside. The cabin's top edge slopes in one straight line, rising toward the greenhouse end (the front of the cabin, 14 ft) from the low back end (8 ft), with the black roof edge visible. Grey river stones, a flagstone path to the door, and young spruce at the base.

Composition: the building centred with generous even margins, ground line in the lower quarter, soft contact shadow. A few dark spruce trees behind, cut out cleanly. Background: plain warm off-white (#F3F0E9), seamless.

Lighting: soft, even overcast daylight; the sconce and the greenhouse lights glowing warm 2700 K.

Realism: real cedar grain, fine metal ribs, true reflections in the greenhouse glass and the door glass.

Style: a clean, photoreal architectural presentation elevation, as in a premium builder's catalogue.

Colour grade: neutral, true-to-material colours, deep charcoal blacks, honey cedar, natural greens.

16:9 landscape. No text, no labels, no dimensions, no arrows, no logos, no watermark, no perspective distortion.
```

## C1 · Architectural section

**Attach, in this order:** `refs/ref8-coupe.jpg`, `takes/frame04-take1.webp`, `takes/frame06-take1.webp` · **Ratio:** 16:9

```
First attached image: the section drawing from the design sheet — use it only for the order of the rooms from left to right and their ceiling types. Second attached image: the approved interior photo — use it for the furniture, materials and light inside. Third attached image: the approved radiant-floor photo — use it for the slab and the red heating tubes. The first attachment is a labelled diagram; the result carries no text.

A photoreal architectural section of the Boreä chalet: the building cut cleanly in half from front to back and seen straight-on in orthographic projection, like a dollhouse with the near wall removed. The cut faces of the walls, the roof and the slab are crisp solid charcoal. One single-slope black roof runs in a straight line from 14 ft on the left (the front) down to 8 ft on the right (the back). From left to right: the open living space under a white sloped cathedral ceiling following the roof, with small warm recessed lights, the cream sofa, the wood dining table with black chairs, a tall plant and the black linear fireplace with the TV above on the far wall; then the bedroom with a flat white 8 ft ceiling, the bed with white bedding and a grey throw and two bedside lamps; then the small bathroom with a flat 8 ft ceiling, a white vanity and a mirror; and the mechanical room with a flat 8 ft ceiling, a white water heater and a dark battery cabinet. Above the flat ceilings, the empty triangular attic space under the slope. All rooms stand on wide natural oak plank floors. Under the whole building, the insulated monolithic concrete slab with thickened edges: a layer of grey rigid insulation underneath, and a single row of small red PEX heating tubes cut in cross-section, evenly spaced as red dots in the concrete across the full width. Below, a band of compacted gravel and soil. A few dark spruce trees behind the low back end.

Composition: the whole section centred with generous even margins, the ground line a little below the middle so the slab layers read clearly. Background: plain warm off-white (#F3F0E9), seamless.

Lighting: warm 2700 K interior light in every room, soft and even; the cut faces evenly lit.

Realism: real oak grain, fabric texture on the sofa and bedding, aggregate visible in the cut concrete.

Style: a clean, photoreal architectural presentation section, as in a premium builder's catalogue.

Colour grade: neutral, warm interiors, deep charcoal cut faces, true red tubes.

16:9 landscape. No text, no labels, no dimensions, no arrows, no logos, no watermark, no perspective distortion.
```

---

## Optional

### P1 · Floor plan (top-down)

Only if you want the plan to match the new drawings. The current plan crop already reads well.

**Attach, in this order:** `refs/ref5-plan.jpg`, `takes/frame04-take1.webp` · **Ratio:** 1:1

```
First attached image: the floor plan from the design sheet — use it for the exact layout of every wall, room, piece of furniture, fixture, the greenhouse and the deck. Second attached image: the approved interior photo — use it for the materials and colours. The first attachment is labelled; the result carries no text.

A photoreal top-down floor plan of the Boreä chalet, seen from directly above in orthographic projection with the roof removed, walls cut at waist height as solid charcoal. Exactly the layout of the first attachment: the bedroom top left with the bed, rug, nightstands and plants; the bathroom top centre with shower, toilet and vanity; the mechanical room top right with its equipment (filtration unit, blue rainwater tank, water heater, central vacuum, battery cabinet); the open living space across the middle with the fireplace on the left wall, the cream L-shaped sofa on a rug with the round coffee table, the dining table with six black chairs, the white island with double sink and three stools, the counter with cooktop on the right wall, the white heat-pump unit on the wall; the greenhouse attached on the right, full of plants; the cedar deck along the bottom with two armchairs, a small round table, a dining table with chairs and steps at the centre. Wide natural oak floors, grey floor in the bathroom and mechanical room, black window frames in the outer walls.

Composition: the full plan centred with even margins, a soft drop shadow under the walls. Background: plain warm off-white (#F3F0E9), seamless.

Lighting: soft, even light from above, gentle ambient occlusion in the corners.

Style: a clean, photoreal architectural presentation plan, as in a premium builder's catalogue.

1:1. No text, no labels, no dimensions, no arrows, no logos, no watermark.
```

### T1 · Roof view (for the solar step)

**Attach, in this order:** `takes/frame01-take2.webp`, `refs/ref7-toit-solaire.jpg` · **Ratio:** 16:9

```
First attached image: the approved photo of the cabin — use it for the exact roof, panels, vents, greenhouse and deck. Second attached image: the roof view from the design sheet — use it only for the panel arrangement and the vent positions.

A photoreal view of the Boreä chalet's roof from a drone directly above and slightly in front, looking down: the black standing-seam single-slope roof carrying 18 dark-blue solar panels with thin silver frames in three neat rows of six, one black plumbing vent pipe, one squat roof ventilator and the black flue pipe near the back edge. The glass roof of the greenhouse at the right end, the cedar deck and its furniture along the front edge, and the tops of the spruce forest all around.

Composition: the roof fills the centre of the frame with the panel grid square to the frame.

Lighting: soft late-morning daylight, a gentle sheen on the panels.

Realism: fine ribs on the metal, slight dust on the panels, spruce needles in the roof gutter.

Style: a real aerial photograph.

Colour grade: neutral, deep charcoal blacks, natural greens.

16:9 landscape. No people, no text, no logos, no watermark.
```

---

## After you generate

Send them to me. I'll put them in the "Le projet" section and add sharp HTML labels on top: room names and heights on the section, side names on the elevations, and room names and dimensions on the plan.
