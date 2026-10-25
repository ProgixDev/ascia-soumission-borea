"""Prepare the Poly Haven scans for the web model (run once, headless).

  Blender -b --factory-startup -P prep_assets.py -- SOURCE_DIR TEXTURE_DIR OUT_DIR

- fir_sapling  -> two cut-out images (front and side) for crossed tree cards: a few hundred KB instead
                  of millions of triangles. This bakes a texture; it is asset preparation, not a scene render.
- rocks        -> six mossy boulders, simplified to about a quarter of their triangles.
- fern, fire pit, armchair (re-covered in cream linen), potted plant (soil simplified) -> light GLBs.
Small objects get 512 px textures; the rocks keep 1K.
"""
import bpy, os, sys, math

SRC, TEX, OUT = sys.argv[sys.argv.index('--') + 1:]
os.makedirs(OUT, exist_ok=True)

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def load(aid):
    bpy.ops.import_scene.gltf(filepath=os.path.join(SRC, aid, aid + '.gltf'))
    return [o for o in bpy.data.objects if o.type == 'MESH']

def shrink_images(px):
    for img in bpy.data.images:
        if img.size[0] > px:
            img.scale(px, px * img.size[1] // img.size[0])
            img.pack()

def decimate(ob, ratio):
    md = ob.modifiers.new('dec', 'DECIMATE'); md.ratio = ratio
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    ob.modifiers.clear(); ob.data = me

def export(name):
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, name + '.glb'), export_format='GLB',
                              export_apply=True, export_yup=True, export_image_format='WEBP')

# ---------- tree cards from the fir sapling ----------
reset()
meshes = load('fir_sapling')
tree = next(o for o in meshes if o.name == 'fir_sapling_a')
for o in meshes:
    if o is not tree: bpy.data.objects.remove(o)
tree.location = (0, 0, 0)
# one sapling is too sparse for a mature black spruce: stack rotated copies into a tall, full cone
h0 = tree.dimensions.z
for i, (s, z, rz) in enumerate([(1.0, 0, 120), (0.9, 0.22, 60), (0.82, 0.42, 200), (0.7, 0.62, 300), (0.58, 0.84, 30), (0.45, 1.04, 150), (0.32, 1.22, 260)]):
    c = tree.copy(); bpy.context.scene.collection.objects.link(c)
    c.scale = (s, s, s); c.location = (0, 0, z * h0); c.rotation_euler = (0, 0, math.radians(rz))
bpy.context.view_layer.update()
scene = bpy.context.scene
for eng in ('BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT'):
    try: scene.render.engine = eng; break
    except Exception: pass
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
h = (1.22 + 0.32) * h0          # top of the highest copy
scene.render.resolution_x, scene.render.resolution_y = 512, 1024
world = bpy.data.worlds.new('W'); scene.world = world
world.color = (0.72, 0.74, 0.76)
sun = bpy.data.objects.new('Sun', bpy.data.lights.new('Sun', 'SUN')); scene.collection.objects.link(sun)
sun.data.energy = 2.2; sun.rotation_euler = (math.radians(35), 0, math.radians(20))
cam = bpy.data.objects.new('Cam', bpy.data.cameras.new('Cam')); scene.collection.objects.link(cam); scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = h * 1.04
for view, rot, loc in (('front', (math.radians(90), 0, 0), (0, -10, h / 2)), ('side', (math.radians(90), 0, math.radians(90)), (10, 0, h / 2))):
    cam.rotation_euler = rot; cam.location = loc
    scene.render.filepath = os.path.join(OUT, f'tree_{view}.png')
    bpy.ops.render.render(write_still=True)
print('TREE_CARD_ASPECT', round(scene.render.resolution_x / scene.render.resolution_y * h * 1.04, 4), 'height_m', round(h * 1.04, 4))

# ---------- mossy rocks ----------
reset()
for o in load('rock_moss_set_01'):
    decimate(o, 0.25)
    o.location = (0, 0, 0)
for m in bpy.data.materials:   # nudge the tan scan toward the sheet's grey granite
    b = m.node_tree.nodes.get('Principled BSDF')
    if b and not b.inputs['Base Color'].is_linked:
        b.inputs['Base Color'].default_value = (0.8, 0.82, 0.84, 1)
shrink_images(1024)
export('rocks')

# ---------- ferns, fire pit ----------
for aid in ('fern_02', 'stone_fire_pit'):
    reset()
    for o in load(aid): o.location = (0, 0, 0)
    shrink_images(512)
    export(aid)

# ---------- armchair re-covered in cream linen ----------
reset()
load('modern_arm_chair_01')
pillow = bpy.data.materials['modern_arm_chair_01_pillow']
nt = pillow.node_tree; b = nt.nodes['Principled BSDF']
for link in list(b.inputs['Base Color'].links): nt.links.remove(link)
diff = nt.nodes.new('ShaderNodeTexImage'); diff.image = bpy.data.images.load(os.path.join(TEX, 'rough_linen', 'Diffuse.jpg'))
nt.links.new(diff.outputs['Color'], b.inputs['Base Color'])
b.inputs['Roughness'].default_value = 0.92
for link in list(b.inputs['Roughness'].links): nt.links.remove(link)
shrink_images(512)
export('armchair')

# ---------- potted plant, soil simplified ----------
reset()
for o in load('potted_plant_02'):
    if o.name.endswith('_dirt'): decimate(o, 0.04)
shrink_images(512)
export('potted_plant')
print('PREP_OK')
