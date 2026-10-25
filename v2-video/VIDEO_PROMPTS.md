# Boreä hero film: video prompts (Kling 4.0)

Uses the frames exactly as delivered, from `takes/`.

**Settings for every clip:** Kling 4.0, **3 s** (the shortest it allows), 16:9, 1080p (or 4K if your plan includes it), **sound off**.
- **Pairs:** the first image is the start frame and the second is the end frame (keyframe at 3.0 s).
- **Single images:** start frame only.

Each prompt says when the action starts and finishes, so the useful part of each clip lands in a known window and the edit is a simple trim.

Why not one 15-second generation with 10 keyframes: our 9 shots are in different places (aerial, living room, greenhouse…). Keyframes in one clip get interpolated, so Kling would morph one room into the next instead of cutting. One clip per shot, then hard cuts in the edit.

---

## Shot 1 · Sunrise over the chalet · 3 s
**Start:** `frame01-take2.webp` · **End (3.0 s):** `frame02-take1.webp`

```
Very slow drone push-in toward the chalet as the sun rises, the camera gliding forward a few metres at constant height and angle. From 0.0 s to 2.4 s the light warms from cool blue dawn to golden sunrise, the mist between the spruce trees thins and glows, and soft light spreads across the façade, the deck and the solar panels; from 2.4 s to 3.0 s the image settles and holds on the end frame. The cabin, the greenhouse, the Thermeä and every object stay exactly in place and keep their shape. 24 mm, wide. Smooth ease-in and ease-out. Real-time. No people, no animals, no new objects, no camera shake.
```

## Shot 2 · Blinds rise · 3 s
**Start:** `frame03-take1.webp` · **End (3.0 s):** `frame04-take1.webp`

```
Locked-off static camera at eye level, facing the full-height windows. At 0.3 s all the roller blinds start rising together, smoothly and evenly, rolling up into their slim black cassettes; by 2.4 s they are fully up, revealing the deck and the forest, and morning sunlight has spread across the oak floor; hold still until 3.0 s. The furniture, the plants and the room stay perfectly still and unchanged. 24 mm. Real-time. No people, no camera movement.
```

## Shot 3 · The radiant floor revealed · 3 s
**Start:** `frame05-take1.webp` · **End (3.0 s):** `frame06-take1.webp`

```
Very slow dolly-in at floor level, a few centimetres forward over the whole clip. From 0.4 s to 2.2 s a precise rectangle of oak planks in the foreground fades away cleanly, as if turning transparent, revealing the concrete slab beneath with the red heating tubes, which warm up gently; hold on the revealed floor until 3.0 s. The cut edges stay straight and rigid. The rest of the room, the furniture and the sunlight stay unchanged. 28 mm, low angle. Real-time. No people, no objects moving, no floor breaking apart.
```

## Shot 4 · Greenhouse watering · 3 s
**Start:** `frame07-take1.webp` · **End (3.0 s):** `frame08-take1.webp`

```
Locked-off static camera, low in the greenhouse. At 0.3 s the misting nozzles along the roof start spraying a fine mist that drifts down through the backlit sunbeams; from 0.6 s drops fall from the drip emitter and darken the soil; by 2.2 s the leaves glisten with droplets and sway very slightly; the mist keeps drifting until 3.0 s. The plants keep their shape and position. 35 mm, shallow depth of field, focus stays on the drip line. Real-time. No people, no camera movement.
```

## Shot 5 · The brain · 3 s
**Start:** `frame09-take1.webp`

```
Slow dolly-in down the length of the mechanical room, about one metre forward across the full 3 s, perfectly smooth, at eye level. Throughout, the small green and amber lights on the network switch and the status lights on the battery cabinet blink softly; nothing else moves. Every appliance, pipe and the rack keep their exact shape and position. 18 mm, deep focus. Ease-in, ease-out. Real-time. No people, no doors opening, no camera shake.
```

## Shot 6 · Secure arrival · 3 s
**Start:** `frame10-take1.webp`

```
Slow push-in toward the black door and its smart lock, about half a metre across the full 3 s, smooth and steady. At 1.2 s the lock's blue ring pulses once brightly, then stays lit. The warm wall sconce stays steady, the string lights inside the greenhouse shimmer faintly, and the young spruce needles move very slightly in a light breeze. The door stays closed. 35 mm. Ease-in, ease-out. Real-time. No people, no door opening, no new objects.
```

## Shot 7 · Evening scene · 3 s
**Start:** `frame11-take1.webp` · **End (3.0 s):** `frame12-take1.webp`

```
Locked-off static camera. At 0.3 s the evening lighting scene turns on: the warm recessed lights and the LED line along the ceiling fade up softly until 1.6 s, the light under the kitchen counter glows, and at 1.0 s the linear gas fireplace ignites with low orange flames that flicker gently until 3.0 s. Outside the windows the sky stays deep blue. The furniture and the room stay perfectly still. 24 mm. Real-time. No people, no camera movement; the TV stays black.
```

## Shot 8 · Thermeä session · 3 s
**Start:** `frame13-take1.webp` · **End (3.0 s):** `frame14-take1.webp`

```
Locked-off static camera at eye level on the stone path. At 0.3 s the fire pit ignites and the flames rise and flicker; at 0.8 s the hot tub's lights glow aqua and steam starts drifting from its surface; at 1.2 s the barrel sauna's door glows amber; from 1.4 s to 2.2 s the path lanterns and deck lights switch on one after another, nearest first; everything glows steadily until 3.0 s. The chairs, tubs, rocks and cabin stay exactly in place. 24 mm. Real-time. No people, no camera movement.
```

## Shot 9 · The whole home at night · 3 s
**Start:** `frame16-take1.webp`

```
Slow drone crane up and pull back across the full 3 s, rising and drifting away from the chalet to reveal more of the dark spruce forest around the lit clearing, then easing to a stop on a locked wide frame. Throughout, the fire flickers, steam drifts from the hot tub and the windows glow steadily. The cabin, the greenhouse and the Thermeä keep their exact shape and layout. 24 mm, wide. Ease-in, ease-out. Real-time. No people, no new buildings, no camera shake.
```

---

## Cut list (15.0 s)

| Shot | Keep from the clip | Timeline |
|---|---|---|
| 1 | 0.6–2.4 | 0.0–1.8 |
| 2 | 0.4–2.4 | 1.8–3.8 |
| 3 | 0.6–2.2 | 3.8–5.4 |
| 4 | 0.4–2.2 | 5.4–7.2 |
| 5 | 0.8–2.2 | 7.2–8.6 |
| 6 | 0.6–2.0 | 8.6–10.0 |
| 7 | 0.2–2.0 | 10.0–11.8 |
| 8 | 0.2–2.0 | 11.8–13.6 |
| 9 | 1.4–2.8 | 13.6–15.0 |

The windows are built from the timecodes in each prompt. If a clip runs early or late, shift its window by the same amount; the lengths stay the same.

Hard cuts, as in the ASCIA film. One colour grade across all clips: slightly cool, deep blacks, saturation pulled down a little on shots 1, 8 and 9 so the exteriors match the interiors. Export 1920×1080, H.264 plus WebM, muted, for the hero loop.
