"""Bake the forest's tree cards (run once, headless).

  Blender -b --factory-startup -P prep_trees.py -- SOURCE_DIR OUT_DIR

Three boreal species, each a front and a side cut-out (512×1024, transparent) for crossed cards on the web:
  tree_*   black spruce: tall, narrow, from the fir sapling stacked into a cone
  fir_*    balsam fir: fuller and wider, from the second fir sapling
  pine_*   pine: from the pine sapling, sparser crown higher up
Each species is built from a scanned sapling by stacking rotated, scaled copies up a trunk.
This bakes textures; it is asset preparation, not a scene render.
"""
import bpy, os, sys, math

SRC, OUT = sys.argv[sys.argv.index('--') + 1:]

SPECIES = {
    # out prefix: (asset, which mesh, [(scale, height fraction, rotation deg)...])
    'tree': ('fir_sapling', 'fir_sapling_a', [(1.0, 0, 120), (0.9, 0.22, 60), (0.82, 0.42, 200), (0.7, 0.62, 300), (0.58, 0.84, 30), (0.45, 1.04, 150), (0.32, 1.22, 260)]),
    'fir':  ('fir_sapling', 'fir_sapling_b', [(1.25, 0, 0), (1.15, 0.18, 70), (1.05, 0.36, 160), (0.95, 0.54, 250), (0.82, 0.72, 330), (0.68, 0.9, 40), (0.52, 1.06, 130), (0.36, 1.2, 220)]),
    'pine': ('pine_sapling_small', None, [(0.55, 0.0, 0), (0.9, 0.35, 90), (1.0, 0.6, 200), (0.85, 0.85, 300), (0.6, 1.05, 30)]),
}

for prefix, (asset, pick, layers) in SPECIES.items():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=os.path.join(SRC, asset, asset + '.gltf'))
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    base = next((o for o in meshes if o.name == pick), None) if pick else max(meshes, key=lambda o: o.dimensions.z)
    for o in meshes:
        if o is not base: bpy.data.objects.remove(o)
    base.location = (0, 0, 0)
    h0 = base.dimensions.z
    for s, z, rz in layers[1:]:
        c = base.copy(); bpy.context.scene.collection.objects.link(c)
        c.scale = (s, s, s); c.location = (0, 0, z * h0); c.rotation_euler = (0, 0, math.radians(rz))
    s0, z0, r0 = layers[0]
    base.scale = (s0, s0, s0); base.location = (0, 0, z0 * h0); base.rotation_euler = (0, 0, math.radians(r0))
    bpy.context.view_layer.update()
    top = max((o.matrix_world @ o.data.vertices[i].co).z for o in bpy.context.scene.objects if o.type == 'MESH' for i in range(0, len(o.data.vertices), 50))
    scene = bpy.context.scene
    for eng in ('BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT'):
        try: scene.render.engine = eng; break
        except Exception: pass
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = 'PNG'; scene.render.image_settings.color_mode = 'RGBA'
    scene.render.resolution_x, scene.render.resolution_y = 512, 1024
    world = bpy.data.worlds.new('W'); scene.world = world; world.color = (0.72, 0.74, 0.76)
    sun = bpy.data.objects.new('Sun', bpy.data.lights.new('Sun', 'SUN')); scene.collection.objects.link(sun)
    sun.data.energy = 2.2; sun.rotation_euler = (math.radians(35), 0, math.radians(20))
    cam = bpy.data.objects.new('Cam', bpy.data.cameras.new('Cam')); scene.collection.objects.link(cam); scene.camera = cam
    h = top * 1.02
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = h
    for view, rot, loc in (('front', (math.radians(90), 0, 0), (0, -10, h / 2)), ('side', (math.radians(90), 0, math.radians(90)), (10, 0, h / 2))):
        cam.rotation_euler = rot; cam.location = loc
        scene.render.filepath = os.path.join(OUT, f'{prefix}_{view}.png')
        bpy.ops.render.render(write_still=True)
    print('CARD', prefix, 'height_m', round(h, 3))
print('TREES_OK')
