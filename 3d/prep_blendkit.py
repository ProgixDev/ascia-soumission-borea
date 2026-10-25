"""Turn the free BlendKit downloads into light web pieces (run once, headless).

  Blender -b --factory-startup -P prep_blendkit.py -- BLENDERKIT_MODELS_DIR OUT_DIR

Each piece: append from the downloaded .blend (1K version), join, simplify, turn to face the way the
chalet needs, put its base centre at the origin, cap textures, export a GLB with WebP textures.
Rotations come from reading each model's geometry (where the backs and the headboard are).
"""
import bpy, os, sys, math, glob
from mathutils import Matrix, Vector

SRC, OUT = sys.argv[sys.argv.index('--') + 1:]
os.makedirs(OUT, exist_ok=True)

# name: (folder prefix, object filter, decimate ratio, rotation about Z in degrees, max texture px)
PIECES = {
    'sofa':       ('new-standard-sec', None, 0.04, 180, 1024),
    'bed':        ('modern-bed', None, 0.05, 0, 1024),
    'nightstand': ('night-stand-mode', None, 1.0, 0, 512),
    'stool':      ('ikea-anssi-bar-s', None, 0.12, 90, 512),
    'chair':      ('modern-minimal-t', 'chair', 1.0, -90, 512),   # one chair from the set, facing +x
    'lemon':      ('lemon-bush-tree', None, 1.0, 0, 512),         # potted lemon tree (greenhouse citrus)
    'cucumber':   ('cucumber-plant', None, 1.0, 0, 512),           # A-frame trellis vine (cucumbers, and tomatoes with red fruit)
    'chive':      ('chive-herbs-pott', None, 0.08, 0, 512),
    'basil':      ('potted-plant-bas', None, 0.15, 0, 512),
    'grass':      ('realistic-grass', None, 0.5, 0, 512),           # groundcover clumps scattered over the clearing
}
ONLY = set(os.environ.get('ONLY', '').split(',')) - {''}

def blend_for(prefix):
    hits = glob.glob(os.path.join(SRC, prefix + '*', '*_1K_*.blend')) or glob.glob(os.path.join(SRC, prefix + '*', '*.blend'))
    return hits[0]

for name, (prefix, filt, ratio, rot, px) in PIECES.items():
    if ONLY and name not in ONLY: continue
    bpy.ops.wm.read_factory_settings(use_empty=True)
    path = blend_for(prefix)
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = list(src.objects)
    for o in dst.objects:
        if o: bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.update()
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    if filt == 'chair':
        # the set is a walnut table plus four chairs of three parts each; keep the chair nearest +x/-y
        table = max(meshes, key=lambda o: o.dimensions.x * o.dimensions.y)
        tc = table.matrix_world.translation.copy()
        meshes = [o for o in meshes if o is not table]
        key = min({tuple(round(v, 2) for v in o.matrix_world.translation) for o in meshes}, key=lambda t: (-(t[0] - tc.x), t[1] - tc.y))
        keep = [o for o in meshes if tuple(round(v, 2) for v in o.matrix_world.translation) == key]
        # chairs on the -y side of the table face +y; make the kept chair face +y explicitly
        facing = math.atan2(tc.y - key[1], tc.x - key[0]) - math.pi / 2
        for o in [o for o in meshes if o not in keep] + [table]:
            bpy.data.objects.remove(o)
        meshes = keep
        extra = Matrix.Rotation(-facing, 4, 'Z')
    else:
        extra = Matrix.Identity(4)
    # particles (leaves, fruit) become real geometry; their source objects are dropped
    sources = set()
    for o in list(meshes):
        if not o.particle_systems: continue
        for ps in o.particle_systems:
            ps.settings.display_percentage = 100
            src = ps.settings.instance_object
            if src: sources.add(src)
            if src and len(src.data.polygons) < 100 and ps.settings.count > 1500:   # leaf cards: keep 40%, enough for a full canopy
                ps.settings.count = int(ps.settings.count * 0.4)
        if len(o.data.polygons) > 20000:   # the branches themselves tolerate simplification well
            md = o.modifiers.new('dec_branches', 'DECIMATE'); md.ratio = 0.25
            with bpy.context.temp_override(object=o, active_object=o):
                bpy.ops.object.modifier_move_to_index(modifier='dec_branches', index=0)
                bpy.ops.object.modifier_apply(modifier='dec_branches')
        bpy.context.view_layer.update()
        before = set(bpy.context.scene.objects)
        bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
        bpy.ops.object.duplicates_make_real(use_base_parent=False, use_hierarchy=False)
        new = [n for n in bpy.context.scene.objects if n not in before and n.type == 'MESH']
        print('PARTICLES', o.name, 'made real:', len(new))
        meshes += new
        for md in [m for m in o.modifiers if m.type == 'PARTICLE_SYSTEM']: o.modifiers.remove(md)
    meshes = [o for o in meshes if o not in sources]
    # bake world transforms into the meshes (single users), drop empties
    for o in meshes:
        if o.data.users > 1: o.data = o.data.copy()
        o.data.transform(o.matrix_world); o.parent = None; o.matrix_world = Matrix.Identity(4)
    for o in [o for o in bpy.context.scene.objects if o.type != 'MESH']:
        bpy.data.objects.remove(o)
    for o in [o for o in bpy.context.scene.objects if o.type == 'MESH' and o not in meshes]:
        bpy.data.objects.remove(o)
    # one mesh per piece
    bpy.ops.object.select_all(action='DESELECT')
    for o in meshes: o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1: bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    for md in list(ob.modifiers):   # bake the model's own modifiers (subdivision, bevel...) before simplifying
        try: bpy.ops.object.modifier_apply(modifier=md.name)
        except RuntimeError: ob.modifiers.remove(md)
    if ratio < 1:
        md = ob.modifiers.new('dec', 'DECIMATE'); md.ratio = ratio
        bpy.ops.object.modifier_apply(modifier='dec')
    # orientation, then base centre at the origin
    ob.data.transform(Matrix.Rotation(math.radians(rot), 4, 'Z') @ extra)
    vs = [v.co for v in ob.data.vertices]
    c = Vector(((min(v.x for v in vs) + max(v.x for v in vs)) / 2, (min(v.y for v in vs) + max(v.y for v in vs)) / 2, min(v.z for v in vs)))
    ob.data.transform(Matrix.Translation(-c))
    ob.name = name
    for img in bpy.data.images:
        if img.size[0] > px:
            img.scale(px, max(1, px * img.size[1] // img.size[0]))
            img.pack()   # keep the shrunk pixels; the source file is not next to this .blend
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, name + '.glb'), export_format='GLB', export_apply=True,
                              export_yup=True, export_image_format='WEBP', use_selection=False)
    tris = sum(len(p.vertices) - 2 for p in ob.data.polygons)
    print(f'PIECE {name} tris={tris} dims={tuple(round(d, 2) for d in ob.dimensions)} mats={[m.name for m in ob.data.materials]}')
print('BK_OK')
