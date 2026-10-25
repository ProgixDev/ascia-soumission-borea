"""Build the Boreä chalet in Blender and export it for the soumission page.

Run headless:
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_borea.py -- OUT.glb OUT.blend PREVIEW.png

Units and axes match the page's 3D viewer: 1 unit = 1 ft, page X = width (0 → 24, left → right
seen from the front), page Z = depth (0 = back wall, 25 = front wall), page Y = up, finished floor = 0.
Blender is Z-up, so a page point (x, y, z) is placed at Blender (x, -z, y); the glTF exporter turns
that back into page coordinates.

Geometry follows the drawings fixed for the soumission: single-slope roof 14 ft at the front and 8 ft
at the back, greenhouse flush with the front on the right, deck 8 ft deep, Thermeä below the steps.
Named hooks used by the page: node "Roof" (lifted by the "Toit ouvert" button) and materials whose
name starts with "Glow_" (driven by the night toggle).
"""
import bpy, bmesh, math, random, sys, os
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:]
GLB, BLEND, PREVIEW = argv

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
random.seed(7)

H = lambda z: 8 + 6 * max(0.0, min(1.0, z / 25))   # top of wall at depth z
GROUND = -1.6                                        # ground level around the cabin
TC = (12.0, 47.0, 8.0)                               # Thermeä patio centre x, z and radius

def P(x, y, z):
    return Vector((x, -z, y))

# ---------- collections ----------
def coll(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or scene.collection).children.link(c)
    return c
C = {n: coll(n) for n in ['House', 'Interior', 'Greenhouse', 'Deck', 'Thermea', 'Site']}

# ---------- materials ----------
def lin(h):
    h = h.lstrip('#')
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return out

MATS = {}
def mat(name, color, rough=0.6, metal=0.0, alpha=1.0, emit=None, strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*lin(color), 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if alpha < 1:
        b.inputs['Alpha'].default_value = alpha
        for attr, val in (('surface_render_method', 'BLENDED'), ('blend_method', 'BLEND')):
            try: setattr(m, attr, val)
            except Exception: pass
    if emit:
        b.inputs['Emission Color'].default_value = (*lin(emit), 1)
        b.inputs['Emission Strength'].default_value = strength
    MATS[name] = m
    return m

HERE = os.path.dirname(os.path.abspath(__file__))
TEXD, PREP = os.path.join(HERE, 'textures'), os.path.join(HERE, 'prepped')
TEX_TILE = {}   # material name -> texture repeat in feet, used by the UV pass

def tex_mat(name, folder, tile, diffuse=True, rough=True, normal=True, base='#ffffff', rough_val=0.6, metal=0.0, nstr=1.0):
    """PBR material from a Poly Haven 1K set (Diffuse / Rough / nor_gl)."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    def img(fn, noncolor):
        n = nt.nodes.new('ShaderNodeTexImage')
        n.image = bpy.data.images.load(os.path.join(TEXD, folder, fn), check_existing=True)
        if noncolor: n.image.colorspace_settings.name = 'Non-Color'
        return n
    if diffuse: nt.links.new(img('Diffuse.jpg', False).outputs['Color'], b.inputs['Base Color'])
    else: b.inputs['Base Color'].default_value = (*lin(base), 1)
    if rough: nt.links.new(img('Rough.jpg', True).outputs['Color'], b.inputs['Roughness'])
    else: b.inputs['Roughness'].default_value = rough_val
    if normal:
        nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = nstr
        nt.links.new(img('nor_gl.jpg', True).outputs['Color'], nm.inputs['Color'])
        nt.links.new(nm.outputs['Normal'], b.inputs['Normal'])
    b.inputs['Metallic'].default_value = metal
    MATS[name] = m; TEX_TILE[name] = tile
    return m

BLACK   = tex_mat('BlackMetal', 'box_profile_metal_sheet', 5.5, diffuse=False, base='#1b1a1f', metal=0.6, nstr=1.2)
TRIM    = mat('BlackTrim', '#111015', 0.4, 0.6)
CEDAR   = tex_mat('Cedar', 'wood_floor', 3.5)
DECKW   = tex_mat('DeckCedar', 'wood_floor_deck', 6.0)
OAK     = tex_mat('Oak', 'laminate_floor_02', 2.8)
WHITE   = mat('InteriorWhite', '#ecebe6', 0.85)
TILE    = mat('Tile', '#9a9893', 0.5)
CONC    = tex_mat('Concrete', 'concrete_floor_worn_001', 8.0)
GLASS   = mat('Glass', '#cfe3ff', 0.05, 0.0, alpha=0.14)
FABRIC  = tex_mat('Fabric', 'rough_linen', 2.0, rough=False, rough_val=0.95, nstr=0.6)
FABDARK = mat('FabricDark', '#3d3a40', 0.9)
WOODF   = tex_mat('WoodFurniture', 'wood_floor', 3.0)
STEEL   = mat('Steel', '#a8acb2', 0.35, 0.9)
PANEL   = mat('SolarCell', '#1c2a5c', 0.22, 0.35)
ALU     = mat('SolarFrame', '#c9ccd1', 0.35, 0.9)
PLANT   = mat('Leaf', '#3f6e43', 0.8)
CITRUS  = mat('Citrus', '#e9c33a', 0.5)
POT     = mat('Pot', '#4a4848', 0.8)
STONE   = tex_mat('Flagstone', 'rock_01', 3.0, rough=False, rough_val=0.9)
ROCK    = mat('Granite', '#6e6a65', 0.95)
SPRUCE  = mat('Spruce', '#22402f', 0.9)
TRUNK   = mat('Bark', '#3b2a20', 1.0)
GROUNDM = tex_mat('ForestFloor', 'forest_leaves_02', 9.0, rough=False, rough_val=1.0)
GRAVEL  = tex_mat('Gravel', 'gravel_floor_02', 4.0, rough=False, rough_val=1.0)
SPAGREY = tex_mat('SpaCabinet', 'wood_floor', 2.5)      # grey composite slats (tinted on the web)
ACRYL   = mat('Acrylic', '#e9ebec', 0.22)
CAB     = mat('Cabinet', '#efeee9', 0.55)
QUARTZ  = mat('Quartz', '#f4f2ee', 0.16)
HEADR   = mat('Headrest', '#3a3a3f', 0.65)
SOIL    = tex_mat('Soil', 'concrete_floor_worn_001', 3.0, rough=False, rough_val=1.0)   # tinted dark brown on the web
TOMATO  = mat('Tomato', '#c8261a', 0.35)
PIPE    = mat('Pipe', '#f2f2f0', 0.4)
GROWL   = mat('Glow_Grow', '#fff4e6', 0.4, emit='#fff1dc', strength=0.0)
APPL    = mat('Appliance', '#f2f2f0', 0.4)
BLUE    = mat('RainTank', '#2f6fb0', 0.5)
SCREEN  = mat('Screen', '#0b0b0e', 0.2, 0.3)
# night-driven materials (the page raises their emission when "Nuit" is on)
FIRE    = mat('Glow_Fire', '#ff8a3d', 0.6, emit='#ff8a3d', strength=4.0)
WATER   = mat('Glow_Water', '#2d7f9a', 0.08, emit='#5ec8e5', strength=0.3)
LANTERN = mat('Glow_Lantern', '#ffd9a0', 0.4, emit='#ffc98a', strength=0.0)
STRING  = mat('Glow_String', '#ffe2b0', 0.4, emit='#ffc98a', strength=0.0)
SCONCE  = mat('Glow_Sconce', '#ffd9a0', 0.4, emit='#ffc98a', strength=0.0)
FIREPL  = mat('Glow_Fireplace', '#ff9a4a', 0.6, emit='#ff8a3d', strength=0.0)

# ---------- mesh helpers ----------
def obj(name, bm, m, c, mats=None):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    for mm in (mats or [m]):
        me.materials.append(mm)
    ob = bpy.data.objects.new(name, me)
    c.objects.link(ob)
    return ob

def box(name, x0, y0, z0, w, h, d, m, c):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1)
    bmesh.ops.scale(bm, vec=(w, d, h), verts=bm.verts)
    bmesh.ops.translate(bm, vec=P(x0 + w / 2, y0 + h / 2, z0 + d / 2), verts=bm.verts)
    ob = obj(name, bm, m, c)
    mn = min(w, h, d)
    if mn >= 0.12 and not (m.name == 'Glass' or m.name.startswith('Glow')):
        ob['bev'] = min(0.05, mn * 0.2)   # rounded edges, applied by the bevel pass before export
    return ob

def cyl(name, x, y, z, r, h, m, c, seg=24, axis='Y', r2=None):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=h)
    if axis == 'X':
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=__import__('mathutils').Matrix.Rotation(math.pi / 2, 3, 'Y'))
    elif axis == 'Z':
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=__import__('mathutils').Matrix.Rotation(math.pi / 2, 3, 'X'))
    bmesh.ops.translate(bm, vec=P(x, y, z), verts=bm.verts)
    return obj(name, bm, m, c)

def round_cyls():
    for ob in bpy.data.objects:
        if ob.type == 'MESH' and 'bev' not in ob and ob.data.materials and ob.name.split('.')[0] in ROUND_CYL:
            ob['bev'] = 0.04
ROUND_CYL = {'CoffeeTable', 'CoffeeTableBase', 'ColdTubFloor', 'BedLamp', 'BedLampBase', 'SaunaPipeCap', 'RainTank', 'WaterHeater60', 'HeatPumpHeater', 'CentralVacuum'}

def tube(name, x, y, z, r, h, m, c, seg=48, axis='Y'):
    """Open band (no caps), e.g. a steel hoop around a barrel."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=False, segments=seg, radius1=r, radius2=r, depth=h)
    M = __import__('mathutils').Matrix
    if axis == 'X': bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=M.Rotation(math.pi / 2, 3, 'Y'))
    elif axis == 'Y': pass
    bmesh.ops.translate(bm, vec=P(x, y, z) if axis != 'Y' else P(x, y, z), verts=bm.verts)
    return obj(name, bm, m, c)

def staves(name, m, c, centre, axis, radius, length, n, thick, tile, seed=1):
    """A ring of n planks around an axis ('X' horizontal barrel, 'Y' upright tub), each with its own
    UVs running along the grain, so the wood reads as separate staves."""
    rr = random.Random(seed)
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap')
    cxp, cyp, czp = centre
    chord = 2 * radius * math.sin(math.pi / n) * 0.985
    for k in range(n):
        a = k / n * 2 * math.pi
        if axis == 'X':
            g = Vector((1, 0, 0)); rad = Vector((0, math.sin(a), math.cos(a))); tan = Vector((0, math.cos(a), -math.sin(a)))
        else:
            g = Vector((0, 1, 0)); rad = Vector((math.cos(a), 0, math.sin(a))); tan = Vector((-math.sin(a), 0, math.cos(a)))
        ctr = Vector((cxp, cyp, czp)) + rad * (radius - thick / 2)
        toB = lambda v: Vector((v.x, -v.z, v.y))       # page direction -> Blender
        hx, hy, hz = length / 2, chord / 2, thick / 2
        corners = {}
        for sx in (-1, 1):
            for sy in (-1, 1):
                for sz in (-1, 1):
                    pp = ctr + g * (sx * hx) + tan * (sy * hy) + rad * (sz * hz)
                    corners[(sx, sy, sz)] = bm.verts.new(P(pp.x, pp.y, pp.z))
        uo, vo = rr.random() * 4, rr.random() * 4
        faces = [((1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1)), ((-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1)),
                 ((-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1)), ((-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1)),
                 ((-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)), ((-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1))]
        for fk in faces:
            f = bm.faces.new([corners[q] for q in fk])
            for l, q in zip(f.loops, fk):
                l[uvl].uv = (vo + (q[1] * hy + q[2] * hz) / tile, uo + q[0] * hx / tile)   # v runs along the grain
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = obj(name, bm, m, c); ob['bev'] = min(0.035, thick * 0.25)
    return ob

def prism_x(name, x0, x1, pts, m, c):
    """Prism along X from a polygon of (z, y) points."""
    bm = bmesh.new()
    a = [bm.verts.new(P(x0, y, z)) for z, y in pts]
    b = [bm.verts.new(P(x1, y, z)) for z, y in pts]
    bm.faces.new(a); bm.faces.new(list(reversed(b)))
    n = len(pts)
    for i in range(n):
        bm.faces.new([a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return obj(name, bm, m, c)

def cut(target, cutters):
    """Boolean-subtract cutter boxes from target, bake the result, delete the cutters."""
    for i, cu in enumerate(cutters):
        md = target.modifiers.new(f'cut{i}', 'BOOLEAN')
        md.operation = 'DIFFERENCE'; md.object = cu; md.solver = 'EXACT'
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(target.evaluated_get(dg))
    old = target.data; target.modifiers.clear(); target.data = me
    bpy.data.meshes.remove(old)
    for cu in cutters:
        bpy.data.objects.remove(cu)

def window_x(name, x_face, z0, z1, y0, y1, c, depth=0.5):
    """Black frame + glass in a wall that runs along Z (side walls)."""
    t = 0.22
    xs = x_face
    box(name + '_fT', xs, y1 - t, z0, depth, t, z1 - z0, TRIM, c)
    box(name + '_fB', xs, y0, z0, depth, t, z1 - z0, TRIM, c)
    box(name + '_fL', xs, y0, z0, depth, y1 - y0, t, TRIM, c)
    box(name + '_fR', xs, y0, z1 - t, depth, y1 - y0, t, TRIM, c)
    box(name + '_g', xs + depth / 2 - 0.03, y0 + t, z0 + t, 0.06, y1 - y0 - 2 * t, z1 - z0 - 2 * t, GLASS, c)

def window_z(name, z_face, x0, x1, y0, y1, c, depth=0.5, split=False):
    """Black frame + glass in a wall that runs along X (back wall)."""
    t = 0.22
    box(name + '_fT', x0, y1 - t, z_face, x1 - x0, t, depth, TRIM, c)
    box(name + '_fB', x0, y0, z_face, x1 - x0, t, depth, TRIM, c)
    box(name + '_fL', x0, y0, z_face, t, y1 - y0, depth, TRIM, c)
    box(name + '_fR', x1 - t, y0, z_face, t, y1 - y0, depth, TRIM, c)
    if split:
        xm = (x0 + x1) / 2
        box(name + '_fM', xm - t / 2, y0, z_face, t, y1 - y0, depth, TRIM, c)
    box(name + '_g', x0 + t, y0 + t, z_face + depth / 2 - 0.03, x1 - x0 - 2 * t, y1 - y0 - 2 * t, 0.06, GLASS, c)

def sconce(name, x, y, z, c, facing='z'):
    if facing == 'z':
        box(name, x - 0.18, y, z, 0.36, 0.8, 0.3, TRIM, c)
        box(name + '_lamp', x - 0.12, y - 0.04, z + 0.05, 0.24, 0.06, 0.2, SCONCE, c)
    else:
        box(name, x, y, z - 0.18, 0.3, 0.8, 0.36, TRIM, c)
        box(name + '_lamp', x + 0.05, y - 0.04, z - 0.12, 0.2, 0.06, 0.24, SCONCE, c)

FT = 3.28084   # the scans are in metres, the model in feet

def import_glb(name):
    """Import a prepared scan, bake its transforms, put its base at the origin, keep it out of the scene."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(PREP, name + '.glb'))
    new = [o for o in bpy.data.objects if o not in before]
    meshes = []
    for o in new:
        if o.type == 'MESH':
            o.data.transform(o.matrix_world)
            vs = [v.co for v in o.data.vertices]
            cx = (min(v.x for v in vs) + max(v.x for v in vs)) / 2; cy = (min(v.y for v in vs) + max(v.y for v in vs)) / 2; mz = min(v.z for v in vs)
            o.data.transform(__import__('mathutils').Matrix.Translation((-cx, -cy, -mz)))
            meshes.append(o.data)
    for o in new:
        bpy.data.objects.remove(o)
    return meshes

def inst(me, name, x, y, z, s, rot, c):
    ob = bpy.data.objects.new(name, me); c.objects.link(ob)
    ob.location = P(x, y, z); ob.scale = (s, s, s); ob.rotation_euler = (0, 0, rot)
    return ob

ROCKS = import_glb('rocks')
FERNS = import_glb('fern_02')
FIREPIT = import_glb('stone_fire_pit')
ARMCHAIR = import_glb('armchair')
PLANTS = import_glb('potted_plant')
SOFA, BED, NIGHT, CHAIR, STOOL = (import_glb(n) for n in ('sofa', 'bed', 'nightstand', 'chair', 'stool'))
LEMON, CUKE, CHIVE, BASIL = (import_glb(n) for n in ('lemon', 'cucumber', 'chive', 'basil'))
def without_material(meshes, matname):
    """Copy of a scan with the faces of one material removed (the tomato vine is the cucumber vine without its cucumbers)."""
    out = []
    for me in meshes:
        me2 = me.copy(); idx = [i for i, m in enumerate(me2.materials) if m and m.name.startswith(matname)]
        if idx:
            bm = bmesh.new(); bm.from_mesh(me2)
            bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index in idx], context='FACES')
            bm.to_mesh(me2); bm.free()
        out.append(me2)
    return out
TOMVINE = without_material(CUKE, 'Cucumbers')

# ---------- site ----------
bm = bmesh.new()
def terr(x, z):
    """Ground height: flat in the clearing (house, deck, Thermeä), rolling gently up into the forest."""
    dx, dz = (x - 14) / 34, (z - 36) / 42
    k = min(1.0, max(0.0, (math.hypot(dx, dz) - 1.0) / 1.5)); k = k * k * (3 - 2 * k)
    roll = (math.sin(x * .045 + 1.3) * math.cos(z * .052 - .7) * 2.4 + math.sin(x * .11 + z * .07) * .9
            + math.cos(z * .13 - x * .05) * .6 + 2.2)
    return GROUND + k * roll * 1.5
bm = bmesh.new()
N, X0, Z0, SPAN = 200, -136.0, -116.0, 300.0
cell = SPAN / N
grid = [[bm.verts.new(P(X0 + i * cell, terr(X0 + i * cell, Z0 + j * cell), Z0 + j * cell)) for i in range(N + 1)] for j in range(N + 1)]
for j in range(N):
    for i in range(N):
        bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
gnd = obj('Ground', bm, GROUNDM, C['Site'])
for poly in gnd.data.polygons: poly.use_smooth = True
box('Foundation', -0.5, GROUND, -0.5, 25, -GROUND, 26, CONC, C['House'])
box('GravelStrip', -1.6, GROUND, -1.6, 27.2, 0.05, 27.2, GRAVEL, C['Site'])

# ---------- exterior shell ----------
# back wall (z 0..0.5), 8 ft, windows: méca small, bathroom double, bedroom in the cedar panel
back = box('BackWall', 0, 0, 0, 24, 8.15, 0.5, BLACK, C['House'])
wins_back = [(20.4, 22.6, 3.2, 6.4, False), (12.6, 17.0, 3.4, 6.6, True), (2.8, 5.4, 3.2, 6.6, False)]
cut(back, [box('c', a - 0.01, b0, -0.2, a2 - a + 0.02, b1 - b0, 0.9, BLACK, C['House']) for a, a2, b0, b1, _ in wins_back])
box('BackCedar', 0, 0, -0.12, 8.2, 8, 0.12, CEDAR, C['House'])
cut(bpy.data.objects['BackCedar'], [box('c', 2.79, 3.19, -0.4, 2.62, 3.42, 0.8, CEDAR, C['House'])])
for i, (a, a2, b0, b1, sp) in enumerate(wins_back):
    window_z(f'BackWin{i}', 0, a, a2, b0, b1, C['House'], split=sp)
box('BackLining', 0.5, 0, 0.5, 23, 8, 0.02, WHITE, C['Interior'])

# side walls: tapered prisms, 8 ft at the back, 14 ft at the front
side_pts = [(0, 0), (25, 0), (25, 14), (0, 8)]
left = prism_x('LeftWall', 0, 0.5, side_pts, BLACK, C['House'])
cut(left, [box('c', -0.2, 3.4, 4.0, 0.9, 3.2, 2.4, BLACK, C['House']), box('c', -0.2, 3.4, 16.4, 0.9, 3.6, 3.0, BLACK, C['House'])])
cedar_left = prism_x('LeftCedar', -0.12, 0, [(12.5, 0), (25, 0), (25, 14), (12.5, H(12.5))], CEDAR, C['House'])
cut(cedar_left, [box('c', -0.4, 3.4, 16.4, 0.8, 3.6, 3.0, CEDAR, C['House'])])
window_x('LeftWin0', 0, 4.0, 6.4, 3.4, 6.6, C['House'])
window_x('LeftWin1', 0, 16.4, 19.4, 3.4, 7.0, C['House'])
prism_x('LeftLining', 0.5, 0.52, [(0.5, 0), (24.5, 0), (24.5, H(24.5)), (0.5, H(0.5))], WHITE, C['Interior'])
cut(bpy.data.objects['LeftLining'], [box('c', 0.3, 3.4, 4.0, 0.4, 3.2, 2.4, WHITE, C['House']), box('c', 0.3, 3.4, 16.4, 0.4, 3.6, 3.0, WHITE, C['House'])])

prism_x('RightWall', 23.5, 24, side_pts, BLACK, C['House'])
prism_x('RightCedar', 24, 24.12, [(2.6, 0), (10.4, 0), (10.4, H(10.4)), (2.6, H(2.6))], CEDAR, C['House'])
box('SideDoor', 24.1, 0.05, 5.0, 0.12, 7.0, 3.0, TRIM, C['House'])
box('SideDoorGlass', 24.2, 1.2, 5.6, 0.04, 5.0, 1.0, GLASS, C['House'])
box('SideDoorLock', 24.22, 3.4, 7.25, 0.08, 0.7, 0.22, TRIM, C['House'])
sconce('SideSconce', 24.12, 6.4, 4.2, C['House'], facing='x')
prism_x('RightLining', 23.48, 23.5, [(0.5, 0), (24.5, 0), (24.5, H(24.5)), (0.5, H(0.5))], WHITE, C['Interior'])

# front façade: full-height glazing between a narrow cedar panel (left) and a wide one (right)
FZ = 24.5
box('FrontCedarL', 0, 0, FZ, 2.6, 14, 0.5, CEDAR, C['House'])
box('FrontCedarR', 20.4, 0, FZ, 3.6, 14, 0.5, CEDAR, C['House'])
box('FrontHeader', 2.6, 13.4, FZ, 17.8, 0.6, 0.5, BLACK, C['House'])
box('FrontSill', 2.6, 0, FZ, 17.8, 0.25, 0.5, TRIM, C['House'])
box('FrontTransom', 2.6, 9.2, FZ, 17.8, 0.3, 0.5, TRIM, C['House'])
bay = 17.8 / 6
for i in range(7):
    box(f'FrontMullion{i}', 2.6 + i * bay - 0.12, 0, FZ, 0.24, 13.4, 0.5, TRIM, C['House'])
for i in range(6):
    x0 = 2.6 + i * bay + 0.12
    box(f'FrontGlassLow{i}', x0, 0.25, FZ + 0.22, bay - 0.24, 8.95, 0.06, GLASS, C['House'])
    box(f'FrontGlassHigh{i}', x0, 9.5, FZ + 0.22, bay - 0.24, 3.9, 0.06, GLASS, C['House'])
box('DoorHandleL', 2.6 + 3 * bay - 0.5, 3.6, FZ + 0.5, 0.1, 1.6, 0.12, STEEL, C['House'])
box('DoorHandleR', 2.6 + 3 * bay + 0.4, 3.6, FZ + 0.5, 0.1, 1.6, 0.12, STEEL, C['House'])
sconce('FrontSconceL', 1.3, 6.6, 25.0, C['House'])
sconce('FrontSconceR', 22.2, 6.6, 25.0, C['House'])

# floors
box('FloorOak', 0.5, 0, 0.5, 23, 0.06, 24, OAK, C['Interior'])
box('FloorTileSdb', 13.1, 0.061, 0.5, 5.8, 0.01, 7.4, TILE, C['Interior'])
box('FloorTileMeca', 19.1, 0.061, 0.5, 4.4, 0.01, 11.4, TILE, C['Interior'])

# interior partitions, 8 ft (bedroom / bathroom / mechanical room at the back)
for i, (x, z, w, d) in enumerate([(0.5, 11.875, 10, .25), (12, 11.875, 1, .25), (12.875, .5, .25, 11.5), (13, 7.875, 1, .25),
                                  (16, 7.875, 3, .25), (18.875, .5, .25, 11.5), (19, 11.875, 1, .25), (22, 11.875, 1.5, .25)]):
    box(f'Partition{i}', x, 0, z, w, 8, d, WHITE, C['Interior'])

# ---------- roof (one node so the page can lift it) ----------
roof = bpy.data.objects.new('Roof', None)
C['House'].objects.link(roof)
k = 6 / 25; ang = math.atan(k)
z0r, z1r = -1.0, 27.5
L = (z1r - z0r) * math.sqrt(1 + k * k)
zc = (z0r + z1r) / 2
roof_parts = []
slab = box('RoofSlab', -1, 0, 0, 26, 1.0, L, BLACK, C['House'])
roof_parts.append(slab)
for i in range(18):   # standing seams along the slope
    roof_parts.append(box(f'Seam{i}', -0.6 + i * 1.5, 1.0, 0, 0.06, 0.12, L - 0.2, TRIM, C['House']))
# 18 solar panels, three rows of six, on the upper surface
for r in range(3):
    for cI in range(6):
        x0 = 1.6 + cI * 3.55; zz = 6.0 + r * 5.6
        roof_parts.append(box(f'SolarFrame_{r}{cI}', x0, 1.12, zz, 3.4, 0.12, 5.4, ALU, C['House']))
        roof_parts.append(box(f'SolarCell_{r}{cI}', x0 + 0.08, 1.2, zz + 0.08, 3.24, 0.06, 5.24, PANEL, C['House']))
# underside: white cathedral ceiling inside, cedar soffit over the front overhang
s_front = (24.5 - z0r) / math.cos(ang)
roof_parts.append(box('CeilingSlope', 0.5, -0.06, 1.5, 23, 0.05, s_front - 1.5, WHITE, C['Interior']))
roof_parts.append(box('Soffit', -1, -0.1, s_front + 0.5, 26, 0.1, L - s_front - 0.5, CEDAR, C['House']))
# parts above are built flat in slope space (page z = distance s along the slope from the back eave,
# page y = height above the roof underside); bend them onto the underside line y = 8 + k·z
for ob in roof_parts:
    for v in ob.data.vertices:
        x, s, yl = v.co.x, -v.co.y, v.co.z
        zp = z0r + s * math.cos(ang) - yl * math.sin(ang)
        yp = (8 + k * z0r) + s * math.sin(ang) + yl * math.cos(ang)
        v.co = P(x, yp, zp)
    ob.parent = roof
# chimney flue, plumbing vent, roof ventilator near the low back edge
for nm, x, z, r, h in [('Flue', 19.0, 1.6, 0.35, 4.0), ('PlumbingVent', 20.6, 1.4, 0.22, 2.0), ('Ventilator', 22.0, 1.8, 0.55, 1.4)]:
    ob = cyl(nm, x, H(z) + 1.0 + h / 2, z, r, h, TRIM, C['House'], seg=20)
    ob.parent = roof
    if nm == 'Ventilator':
        cap = cyl(nm + 'Cap', x, H(z) + 1.0 + h + 0.15, z, r * 1.25, 0.3, TRIM, C['House'], seg=20)
        cap.parent = roof
# flat 8 ft ceilings over bedroom, bathroom and mechanical room (lift with the roof)
box('CeilingFlat', 0.5, 8.0, 0.5, 23, 0.08, 11.6, WHITE, C['Interior']).parent = roof

# ---------- interior ----------
I = C['Interior']
# bedroom
for me in BED: inst(me, 'Bed', 5.6, 0.06, 3.85, FT * 0.8, 0.0, I)          # BlendKit low platform bed
for x in (1.6, 9.6):
    for me in NIGHT: inst(me, 'Nightstand', x, 0.06, 1.3, FT, 0.0, I)      # BlendKit oak nightstands
    cyl('BedLampBase', x, 1.95, 1.2, 0.18, 0.12, TRIM, I, seg=20)
    cyl('BedLamp', x, 2.45, 1.2, 0.36, 0.75, FABRIC, I, seg=24, r2=0.28)
box('BedRug', 1.2, 0.07, 2.4, 7.6, 0.02, 8.4, FABRIC, I)
# bathroom
box('Vanity', 13.4, 0, 0.6, 2.6, 2.8, 1.6, WOODF, I); box('Basin', 13.7, 2.8, 0.8, 2.0, 0.15, 1.2, APPL, I)
box('Mirror', 13.7, 4.0, 0.52, 2.0, 2.4, 0.06, GLASS, I)
box('ShowerGlass', 16.2, 0.06, 0.6, 0.06, 7.0, 2.8, GLASS, I); box('ShowerTray', 16.3, 0.06, 0.6, 2.5, 0.12, 2.8, APPL, I)
box('Toilet', 13.7, 0, 5.2, 1.3, 1.4, 2.0, APPL, I)
# mechanical room (from the sheet): filtration, rainwater tank, 60 gal heater, heat-pump heater, central vacuum, batteries, rack
box('Filtration', 19.4, 0, 0.7, 1.6, 2.6, 1.4, APPL, I)
cyl('RainTank', 22.6, 2.4, 2.0, 0.9, 4.8, BLUE, I)
cyl('WaterHeater60', 20.2, 2.6, 4.8, 0.95, 5.2, APPL, I)
cyl('HeatPumpHeater', 22.7, 3.0, 6.0, 0.8, 6.0, APPL, I)
cyl('CentralVacuum', 19.8, 3.4, 8.0, 0.5, 2.0, APPL, I)
box('Batteries', 21.6, 0, 8.6, 1.6, 4.2, 2.4, FABDARK, I)
box('Rack', 22.6, 3.0, 11.0, 0.9, 3.0, 0.6, TRIM, I)
box('RackLeds', 22.58, 4.6, 11.05, 0.04, 0.08, 0.5, mat('Glow_Leds', '#5de08a', 0.4, emit='#5de08a', strength=2.0), I)
# living: fireplace + TV on the left wall, sectional, coffee table, dining, kitchen
box('Fireplace', 0.52, 1.4, 14.4, 0.7, 1.6, 6.0, TRIM, I); box('FireplaceFlame', 1.2, 1.7, 14.9, 0.05, 0.8, 5.0, FIREPL, I)
box('TV', 0.55, 4.4, 15.2, 0.15, 2.4, 4.4, SCREEN, I)
for me in SOFA: inst(me, 'Sofa', 5.43, 0.06, 19.73, FT * 0.82, 0.0, I)       # BlendKit L-sectional, backs to the glass
box('LivingRug', 1.6, 0.07, 15.2, 8.0, 0.03, 8.4, FABRIC, I)
cyl('CoffeeTable', 4.6, 0.7, 18.6, 1.15, 0.12, WOODF, I, seg=40)
cyl('CoffeeTableBase', 4.6, 0.32, 18.6, 0.95, 0.64, WOODF, I, seg=40)
# dining: solid oak table, six BlendKit chairs
box('DiningTop', 10.8, 2.35, 15.9, 2.5, 0.16, 5.6, WOODF, I)
for x, z in [(11.0, 16.1), (13.0, 16.1), (11.0, 21.2), (13.0, 21.2)]:
    box('TableLeg', x, 0, z, 0.3, 2.35, 0.3, WOODF, I)
for zz in (16.9, 18.7, 20.5):
    for me in CHAIR: inst(me, 'DiningChair', 10.25, 0.06, zz, FT, 0.0, I)
    for me in CHAIR: inst(me, 'DiningChair', 13.85, 0.06, zz, FT, math.pi, I)
# kitchen island: white cabinets with door reveals, quartz top overhanging toward the stools, double sink, faucet
box('IslandBase', 16.7, 0.06, 15.8, 2.3, 2.85, 6.2, CAB, I)
box('IslandTop', 16.3, 2.9, 15.6, 2.8, 0.14, 6.6, QUARTZ, I)
for k in range(1, 4):
    box('IslandReveal', 18.99, 0.3, 15.8 + k * 1.55, 0.03, 2.5, 0.03, TRIM, I)
for z0 in (17.5, 19.0):
    box('IslandSinkBowl', 17.3, 2.62, z0, 1.2, 0.42, 1.3, STEEL, I)
cyl('FaucetBase', 18.35, 3.25, 18.85, 0.07, 0.6, STEEL, I, seg=16)
cyl('FaucetSpout', 18.05, 3.52, 18.85, 0.05, 0.6, STEEL, I, seg=16, axis='X')
for zz in (16.6, 18.6, 20.6):
    for me in STOOL: inst(me, 'Stool', 15.45, 0.06, zz, FT * 0.75, 0.0, I)     # BlendKit counter stools
# wall counter with cooktop
box('CounterBase', 21.8, 0.06, 13.1, 1.7, 2.85, 9.4, CAB, I)
box('CounterTop', 21.6, 2.9, 13.0, 1.9, 0.14, 9.6, QUARTZ, I)
box('Cooktop', 21.9, 3.04, 15.9, 1.4, 0.03, 2.2, SCREEN, I)
for k in range(1, 6):
    box('CounterReveal', 21.79, 0.3, 13.1 + k * 1.57, 0.03, 2.5, 0.03, TRIM, I)
box('HeatPumpUnit', 9.0, 6.4, 12.2, 3.2, 1.0, 0.8, APPL, I)
for x, z, rr in [(1.4, 13.3, 0.4), (1.4, 23.5, 2.0), (20.8, 13.4, 3.5)]:
    for me in PLANTS: inst(me, 'Plant', x, 0.06, z, FT * 1.45, rr, I)

# ---------- greenhouse (10 × 12 ft, right end, flush with the front) ----------
G = C['Greenhouse']
GX0, GX1, GZ0, GZ1, GE, GR = 24.0, 34.0, 13.0, 25.0, 8.5, 11.2
box('GH_Curb', GX0, GROUND, GZ0, GX1 - GX0, 0.6 - GROUND, GZ1 - GZ0, CONC, G)
box('GH_Floor', GX0 + 0.2, 0.6, GZ0 + 0.2, 9.6, 0.05, 11.6, GRAVEL, G)
box('GH_GlassFront', GX0, 0.6, GZ1 - 0.06, GX1 - GX0, GE - 0.6, 0.06, GLASS, G)
box('GH_GlassSide', GX1 - 0.06, 0.6, GZ0, 0.06, GE - 0.6, GZ1 - GZ0, GLASS, G)
box('GH_GlassBack', GX0, 0.6, GZ0, GX1 - GX0, GE - 0.6, 0.06, GLASS, G)
# pitched glass roof, ridge front-to-back at the middle
for side in (0, 1):
    bm = bmesh.new()
    xa, xb = (GX0, (GX0 + GX1) / 2) if side == 0 else ((GX0 + GX1) / 2, GX1)
    ya, yb = (GE, GR) if side == 0 else (GR, GE)
    vs = [bm.verts.new(P(xa, ya, GZ0)), bm.verts.new(P(xb, yb, GZ0)), bm.verts.new(P(xb, yb, GZ1)), bm.verts.new(P(xa, ya, GZ1))]
    bm.faces.new(vs); obj(f'GH_Roof{side}', bm, GLASS, G)
for z in (GZ0, GZ1):   # gable triangles
    bm = bmesh.new()
    vs = [bm.verts.new(P(GX0, GE, z)), bm.verts.new(P(GX1, GE, z)), bm.verts.new(P((GX0 + GX1) / 2, GR, z))]
    bm.faces.new(vs); obj('GH_Gable', bm, GLASS, G)
# black aluminium frame
for x in [GX0 + i * 2.5 for i in range(5)]:
    box('GH_PostF', x - 0.08, 0.6, GZ1 - 0.16, 0.16, GE - 0.6, 0.16, TRIM, G)
for z in [GZ0 + i * 2.4 for i in range(6)]:
    box('GH_PostS', GX1 - 0.16, 0.6, z - 0.08, 0.16, GE - 0.6, 0.16, TRIM, G)
box('GH_EaveF', GX0, GE - 0.16, GZ1 - 0.16, 10, 0.16, 0.16, TRIM, G)
box('GH_EaveS', GX1 - 0.16, GE - 0.16, GZ0, 0.16, 0.16, 12, TRIM, G)
box('GH_EaveH', GX0, GE - 0.16, GZ0, 0.16, 0.16, 12, TRIM, G)
box('GH_Ridge', (GX0 + GX1) / 2 - 0.08, GR - 0.1, GZ0, 0.16, 0.16, 12, TRIM, G)
for z in [GZ0 + i * 2.4 for i in range(6)]:
    for xa, ya, xb, yb in [(GX0, GE, (GX0 + GX1) / 2, GR), ((GX0 + GX1) / 2, GR, GX1, GE)]:
        bm = bmesh.new()
        dx, dy = xb - xa, yb - ya; ln = math.hypot(dx, dy)
        bmesh.ops.create_cube(bm, size=1); bmesh.ops.scale(bm, vec=(ln, 0.12, 0.12), verts=bm.verts)
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=__import__('mathutils').Matrix.Rotation(math.atan2(dy, dx), 3, 'Y').inverted())
        bmesh.ops.translate(bm, vec=P((xa + xb) / 2, (ya + yb) / 2, z), verts=bm.verts)
        obj('GH_Rafter', bm, TRIM, G)
# raised cedar beds (tomatoes west, cucumbers east), soil, drip lines
FL = 0.65                                           # greenhouse floor level
for bx0, bx1, crop in ((24.35, 26.65, 'tomato'), (31.35, 33.65, 'cucumber')):
    box('GH_Bed', bx0, FL, 13.4, bx1 - bx0, 1.35, 11.2, DECKW, G)
    box('GH_Soil', bx0 + 0.15, FL + 1.36, 13.55, bx1 - bx0 - 0.3, 0.05, 10.9, SOIL, G)
    for dx in (0.6, bx1 - bx0 - 0.6):
        cyl('GH_DripLine', bx0 + dx, FL + 1.44, 19.0, 0.035, 10.6, TRIM, G, seg=8, axis='Z')
    vine = TOMVINE if crop == 'tomato' else CUKE
    for zc in (16.2, 21.8):
        for me in vine: inst(me, 'GH_Vine', (bx0 + bx1) / 2, FL + 1.4, zc, FT * 1.05, math.pi / 2, G)
        if crop == 'tomato':   # cherry-tomato trusses hanging in the vine
            rt = random.Random(int(zc * 10))
            bm = bmesh.new()
            for k in range(46):
                tx = (bx0 + bx1) / 2 + (rt.random() - .5) * 2.4; tz = zc + (rt.random() - .5) * 4.6
                ty = FL + 1.7 + rt.random() * 2.6 * (1 - abs(tx - (bx0 + bx1) / 2) / 1.6)
                ret = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.085 + rt.random() * 0.03)
                bmesh.ops.translate(bm, vec=P(tx, ty, tz), verts=ret['verts'])
            obj('GH_Tomatoes', bm, TOMATO, G)
# two potted lemon trees down the aisle
for x, z, rr in ((29.0, 18.4, 0.3), (29.2, 22.9, 2.1)):
    for me in LEMON: inst(me, 'GH_Lemon', x, FL, z, FT * 0.62, rr, G)
# potting bench along the open end, basil and chives
box('GH_BenchTop', 26.9, FL + 2.6, 13.3, 4.2, 0.12, 1.3, WOODF, G)
for x in (27.0, 30.9):
    for z in (13.4, 14.45):
        box('GH_BenchLeg', x, FL, z, 0.12, 2.6, 0.12, TRIM, G)
box('GH_BenchShelf', 26.95, FL + 0.8, 13.35, 4.1, 0.08, 1.2, WOODF, G)
for i, x in enumerate((27.4, 28.2, 29.0, 29.8, 30.6)):
    herb = BASIL if i % 2 == 0 else CHIVE
    for me in herb: inst(me, 'GH_Herb', x, FL + 2.72, 13.95, FT * (1.0 if herb is BASIL else 1.9), i * 1.3, G)
# grow-light bars on wires, misting line along the ridge, circulation fans
for bx in (25.5, 32.5):
    box('GH_GrowBar', bx - 0.18, 7.0, 15.0, 0.36, 0.12, 8.0, TRIM, G)
    box('GH_GrowLED', bx - 0.14, 6.98, 15.2, 0.28, 0.02, 7.6, GROWL, G)
    for z in (15.4, 22.6):
        cyl('GH_GrowWire', bx, 7.7, z, 0.012, 1.3, TRIM, G, seg=6)
cyl('GH_MistLine', (GX0 + GX1) / 2, GR - 0.45, 19.0, 0.04, 11.6, PIPE, G, seg=8, axis='Z')
for k in range(8):
    cyl('GH_MistNozzle', (GX0 + GX1) / 2, GR - 0.55, 13.6 + k * 1.55, 0.05, 0.16, PIPE, G, seg=8)
for z in (13.5, 24.5):
    cyl('GH_Fan', GX1 - 1.0, 7.2, z, 0.45, 0.5, TRIM, G, seg=24, axis='Z')
for i in range(12):
    z = GZ0 + 0.5 + i * 1.0
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.1)
    bmesh.ops.translate(bm, vec=P((GX0 + GX1) / 2, GR - 0.6 - 0.25 * math.sin(i), z), verts=bm.verts); obj('GH_Bulb', bm, STRING, G)

# ---------- deck (24 × 8 ft, covered by the roof overhang near the glass) ----------
D = C['Deck']
box('DeckFrame', 0, GROUND + 0.3, 25, 24, -GROUND - 0.4, 8, TRIM, D)
for i in range(16):
    box(f'DeckBoard{i}', 0, -0.12, 25.05 + i * 0.5, 24, 0.12, 0.45, DECKW, D)
box('Step0', 10, GROUND, 33.0, 4, -0.55 - GROUND, 1.1, DECKW, D)
box('Step1', 10, GROUND, 34.1, 4, -1.08 - GROUND, 1.1, DECKW, D)
for x in (3.7, 7.3):   # two armchairs with cream cushions, facing the forest
    for me in ARMCHAIR: inst(me, 'Armchair', x, 0, 27.9, FT, math.pi, D)
cyl('SideTable', 5.3, 0.9, 28.6, 0.6, 1.8, WOODF, D)
box('DeckTable', 15.5, 2.3, 27.4, 5.5, 0.2, 2.6, WOODF, D)
for x in (15.7, 20.6):
    for z in (27.6, 29.7):
        box('DeckTableLeg', x, 0, z, 0.2, 2.3, 0.2, WOODF, D)
for x in (15.9, 17.7, 19.5):
    for z, back in ((26.1, 26.1), (30.3, 31.38)):
        box('DeckChair', x, 1.5, z, 1.3, 0.12, 1.2, FABDARK, D); box('DeckChairBack', x, 1.5, back, 1.3, 1.5, 0.12, FABDARK, D)
        box('DeckChairLeg', x + 0.6, 0, z + 0.5, 0.15, 1.5, 0.15, FABDARK, D)
for x, z, rr in [(1.0, 31.8, 0.3), (23.0, 31.8, 1.7), (9.0, 32.2, 4.1), (15.0, 32.2, 2.6)]:
    for me in PLANTS: inst(me, 'DeckPlant', x, 0, z, FT * 1.2, rr, D)
for i in range(9):   # puck lights along the deck edge
    box(f'DeckLight{i}', 1.5 + i * 2.6, -0.5, 32.96, 0.3, 0.2, 0.05, LANTERN, D)

# ---------- Thermeä ----------
T = C['Thermea']
cx, cz, R = TC
TY = GROUND + 0.25
cyl('PatioBase', cx, GROUND + 0.1, cz, R, 0.2, GROUNDM, T, seg=64)   # moss between the stones
rng = random.Random(3)
def flagstone(name, x, z, s):
    bm = bmesh.new()
    n = rng.randint(9, 13); rot = rng.random() * 6.3; sx, sz = s * (0.8 + 0.4 * rng.random()), s * (0.8 + 0.4 * rng.random())
    pts = [(x + sx * (0.72 + 0.32 * rng.random()) * math.cos(rot + (i + rng.random() * .4) / n * 2 * math.pi), z + sz * (0.72 + 0.32 * rng.random()) * math.sin(rot + (i + rng.random() * .4) / n * 2 * math.pi)) for i in range(n)]
    tilt = (rng.random() - .5) * .03
    top = [bm.verts.new(P(px, TY + tilt * (px - x), pz)) for px, pz in pts]
    bot = [bm.verts.new(P(px, TY - 0.15, pz)) for px, pz in pts]
    bm.faces.new(top); bm.faces.new(list(reversed(bot)))
    for i in range(n):
        bm.faces.new([top[i], bot[i], bot[(i + 1) % n], top[(i + 1) % n]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return obj(name, bm, STONE, T)
stones = []   # Poisson-disk layout: random, evenly spaced stones of varied size, never in rings
for _ in range(4000):
    a = rng.random() * 2 * math.pi; d = math.sqrt(rng.random()) * (R - 0.55)
    x, z = cx + math.cos(a) * d, cz + math.sin(a) * d
    if math.hypot(x - cx, z - cz) < 1.75: continue        # the fire-pit ring sits on its own
    if all(math.hypot(x - u, z - v) > 1.32 for u, v in stones): stones.append((x, z))
for x, z in stones:
    near = min(math.hypot(x - u, z - v) for u, v in stones if (u, v) != (x, z))
    flagstone('Flagstone', x, z, min(0.62, near * 0.47))
for i, z in enumerate([35.9, 37.4]):   # path from the steps
    flagstone('PathStone', 12.0 + (0.4 if i % 2 else -0.3), z, 0.8)
for i, z in enumerate([55.0, 56.6, 58.2, 59.8]):   # path continuing downhill
    flagstone('PathStone', 12.5 + (0.5 if i % 2 else -0.2), z, 0.8)
# barrel sauna on a small platform, glass door facing the fire pit
SX0, SX1, SR, SZ = -3.8, 2.6, 2.55, 46.0
SY = TY + 0.3 + 0.75 + SR                       # deck + cradles + radius
box('SaunaDeck', -4.8, TY, 42.4, 8.8, 0.3, 7.2, DECKW, T)
for x in (SX0 + 0.9, SX1 - 0.9):               # cradles under the barrel
    box('SaunaCradle', x - 0.3, TY + 0.3, SZ - 2.0, 0.6, 1.0, 4.0, WOODF, T)
staves('SaunaStaves', CEDAR, T, ((SX0 + SX1) / 2, SY, SZ), 'X', SR, SX1 - SX0, 36, 0.18, 3.5, seed=5)
for x in (SX0 + 0.8, SX1 - 0.8):
    tube('SaunaBand', x, SY, SZ, SR + 0.025, 0.22, TRIM, T, axis='X')
# plank end walls; the front one frames a full glass door facing the fire pit
DOOR = (SZ - 0.8, SZ + 0.8, SY - SR + 0.35, SY + 1.2)
for xw, front in ((SX0 + 0.06, False), (SX1 - 0.24, True)):
    zb = SZ - (SR - 0.22)
    while zb < SZ + SR - 0.22 - 0.05:
        zc = zb + 0.21; half = math.sqrt(max(0.0, (SR - 0.2) ** 2 - (zc - SZ) ** 2))
        y0, y1 = SY - half, SY + half
        spans = [(y0, y1)]
        if front and DOOR[0] - 0.05 < zc < DOOR[1] + 0.05:
            spans = [(y0, DOOR[2]), (DOOR[3], y1)]
        for a0, a1 in spans:
            if a1 - a0 > 0.1: box('SaunaEndBoard', xw, a0, zb, 0.18, a1 - a0, 0.42, CEDAR, T)
        zb += 0.43
fx = SX1 - 0.2
box('SaunaDoorFrameL', fx, DOOR[2], DOOR[0] - 0.12, 0.2, DOOR[3] - DOOR[2], 0.12, TRIM, T)
box('SaunaDoorFrameR', fx, DOOR[2], DOOR[1], 0.2, DOOR[3] - DOOR[2], 0.12, TRIM, T)
box('SaunaDoorFrameT', fx, DOOR[3], DOOR[0] - 0.12, 0.2, 0.12, DOOR[1] - DOOR[0] + 0.24, TRIM, T)
box('SaunaDoor', fx + 0.08, DOOR[2], DOOR[0], 0.05, DOOR[3] - DOOR[2], DOOR[1] - DOOR[0], GLASS, T)
box('SaunaDoorHandle', fx + 0.22, SY - 0.6, DOOR[1] - 0.3, 0.12, 1.2, 0.08, WOODF, T)
cyl('SaunaStovePipe', SX0 + 1.1, SY + SR + 0.9, SZ, 0.2, 2.0, STEEL, T, seg=20)
cyl('SaunaPipeCap', SX0 + 1.1, SY + SR + 2.0, SZ, 0.34, 0.12, STEEL, T, seg=20)
# fire pit with logs and flame, ringed by six lounge chairs
for me in FIREPIT: inst(me, 'FirePit', 12.0, TY, 47.0, FT, 0.0, T)
for i in range(4):
    a = i * math.pi / 4
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.12, radius2=0.12, depth=1.8)
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=__import__('mathutils').Matrix.Rotation(a, 3, 'Z') @ __import__('mathutils').Matrix.Rotation(math.pi / 2, 3, 'X'))
    bmesh.ops.translate(bm, vec=P(12.0, TY + 0.5, 47.0), verts=bm.verts); obj('Log', bm, TRUNK, T)
cyl('Flame', 12.0, TY + 1.4, 47.0, 0.55, 1.4, FIRE, T, seg=10, r2=0.04)
for i in range(6):   # six cream armchairs facing the fire
    a = i / 6 * 2 * math.pi + math.pi / 6
    x, z = 12.0 + 4.3 * math.cos(a), 47.0 + 4.3 * math.sin(a)
    for me in ARMCHAIR: inst(me, 'LoungeChair', x, TY, z, FT, math.atan2(math.cos(a), math.sin(a)) + math.pi, T)
# square hot tub and round cold-plunge tub
HX, HZ, HW, HH = 20.2, 44.4, 6.4, 2.9
box('HotTubPlinth', HX + 0.1, TY, HZ + 0.1, HW - 0.2, 0.2, HW - 0.2, TRIM, T)
box('HotTubBase', HX + 0.12, TY, HZ + 0.12, HW - 0.24, 0.42, HW - 0.24, TRIM, T)
for x0, z0, w, d in ((HX + 0.09, HZ + 0.09, HW - 0.18, 0.08), (HX + 0.09, HZ + HW - 0.17, HW - 0.18, 0.08), (HX + 0.09, HZ + 0.09, 0.08, HW - 0.18), (HX + HW - 0.17, HZ + 0.09, 0.08, HW - 0.18)):
    box('HotTubBacking', x0, TY + 0.2, z0, w, HH - 0.5, d, TRIM, T)   # dark backing seen between the slats
ns = int(HW / 0.33)
for k in range(ns):                              # vertical grey composite slats on all four sides
    t = 0.18 + k * (HW - 0.36) / (ns - 1)
    box('SpaSlat', HX + t - 0.12, TY + 0.2, HZ, 0.24, HH - 0.5, 0.09, SPAGREY, T)
    box('SpaSlat', HX + t - 0.12, TY + 0.2, HZ + HW - 0.09, 0.24, HH - 0.5, 0.09, SPAGREY, T)
    box('SpaSlat', HX, TY + 0.2, HZ + t - 0.12, 0.09, HH - 0.5, 0.24, SPAGREY, T)
    box('SpaSlat', HX + HW - 0.09, TY + 0.2, HZ + t - 0.12, 0.09, HH - 0.5, 0.24, SPAGREY, T)
TOP = TY + HH - 0.32
for x0, z0, w, d in ((HX, HZ, HW, 0.75), (HX, HZ + HW - 0.75, HW, 0.75), (HX, HZ + 0.75, 0.75, HW - 1.5), (HX + HW - 0.75, HZ + 0.75, 0.75, HW - 1.5)):
    box('SpaDeck', x0, TOP, z0, w, 0.32, d, ACRYL, T)       # white acrylic top frame
IN0, IN1 = 0.75, HW - 0.75
box('SpaShellFloor', HX + IN0, TY + 0.4, HZ + IN0, IN1 - IN0, 0.12, IN1 - IN0, ACRYL, T)
for x0, z0, w, d in ((HX + IN0, HZ + IN0, IN1 - IN0, 0.08), (HX + IN0, HZ + IN1 - 0.08, IN1 - IN0, 0.08), (HX + IN0, HZ + IN0, 0.08, IN1 - IN0), (HX + IN1 - 0.08, HZ + IN0, 0.08, IN1 - IN0)):
    box('SpaShellWall', x0, TY + 0.4, z0, w, TOP - TY - 0.4, d, ACRYL, T)
box('SpaSeatN', HX + IN0, TY + 0.4, HZ + IN0, IN1 - IN0, 1.3, 1.3, ACRYL, T)
box('SpaSeatE', HX + IN1 - 1.3, TY + 0.4, HZ + IN0 + 1.3, 1.3, 1.3, IN1 - IN0 - 1.3, ACRYL, T)
for x, z in ((HX + IN0 + 0.15, HZ + IN0 + 0.15), (HX + IN1 - 0.85, HZ + IN0 + 0.15), (HX + IN1 - 0.85, HZ + IN1 - 0.85)):
    box('SpaHeadrest', x, TOP + 0.05, z, 0.7, 0.28, 0.7, HEADR, T)
box('HotTubWater', HX + IN0 + 0.05, TOP - 0.18, HZ + IN0 + 0.05, IN1 - IN0 - 0.1, 0.04, IN1 - IN0 - 0.1, WATER, T)
box('SpaStep1', HX - 1.5, TY, HZ + 2.2, 1.5, 1.0, 2.0, SPAGREY, T)
box('SpaStep2', HX - 0.8, TY + 1.0, HZ + 2.2, 0.8, 0.9, 2.0, SPAGREY, T)
# cold plunge: upright cedar staves in two steel hoops, water inside
CTX, CTZ, CTR, CTH = 30.0, 43.6, 1.6, 2.6
cyl('ColdTubFloor', CTX, TY + 0.2, CTZ, CTR - 0.1, 0.2, WOODF, T, seg=32)
staves('ColdTubStaves', CEDAR, T, (CTX, TY + CTH / 2, CTZ), 'Y', CTR, CTH, 24, 0.16, 3.0, seed=9)
for yy in (TY + 0.45, TY + CTH - 0.45):
    tube('ColdTubBand', CTX, yy, CTZ, CTR + 0.02, 0.2, TRIM, T, axis='Y')
cyl('ColdTubWater', CTX, TY + CTH - 0.35, CTZ, CTR - 0.18, 0.04, WATER, T, seg=40)
box('ColdTubStep', CTX - 2.6, TY, CTZ - 0.9, 0.9, 1.1, 1.8, CEDAR, T)
box('TubGravel', HX - 1.2, GROUND + 0.02, HZ - 3.6, 14.0, 0.06, 10.6, GRAVEL, T)
# path lanterns
for i, (x, z) in enumerate([(10.4, 36.0), (13.8, 37.4), (5.0, 42.6), (4.4, 51.4), (8.6, 54.6), (15.6, 54.6), (19.4, 51.8), (19.0, 41.6), (11.0, 57.6), (14.0, 60.6)]):
    cyl('Lantern', x, TY + 0.8, z, 0.14, 1.6, TRIM, T, seg=10)
    cyl('LanternGlow', x, TY + 1.5, z, 0.16, 0.25, LANTERN, T, seg=10)

# ---------- rocks, ferns and the spruce forest (scans + baked tree cards) ----------
def card_mat(name, fn):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; bsdf = nt.nodes['Principled BSDF']
    n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(os.path.join(PREP, fn))
    nt.links.new(n.outputs['Color'], bsdf.inputs['Base Color']); nt.links.new(n.outputs['Alpha'], bsdf.inputs['Alpha'])
    bsdf.inputs['Roughness'].default_value = 0.9
    try: m.surface_render_method = 'DITHERED'
    except Exception: pass
    return m
def card_mesh(prefix, label):
    """Three crossed vertical quads, 1 unit tall, 0.5 wide (each baked tree is twice as tall as wide)."""
    CARD_F, CARD_S = card_mat(f'TreeCard{label}Front', f'{prefix}_front.png'), card_mat(f'TreeCard{label}Side', f'{prefix}_side.png')
    me = bpy.data.meshes.new(f'{label}Card'); bm = bmesh.new(); uv = bm.loops.layers.uv.new('UVMap')
    for k, deg in enumerate((0, 60, 120)):
        dx, dy = 0.25 * math.cos(math.radians(deg)), 0.25 * math.sin(math.radians(deg))
        vs = [bm.verts.new((-dx, -dy, 0)), bm.verts.new((dx, dy, 0)), bm.verts.new((dx, dy, 1)), bm.verts.new((-dx, -dy, 1))]
        f = bm.faces.new(vs); f.material_index = 1 if k == 1 else 0
        for l, (u, v) in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))): l[uv].uv = (u, v)
    bm.to_mesh(me); bm.free(); me.materials.append(CARD_F); me.materials.append(CARD_S)
    return me
SPRUCE_C, FIR_C, PINE_C = card_mesh('tree', 'Spruce'), card_mesh('fir', 'Fir'), card_mesh('pine', 'Pine')
GRASS = import_glb('grass')

S = C['Site']
r = random.Random(11)
def free_spot(dmin, dmax, cxz=(13, 32)):
    while True:
        a = r.random() * 2 * math.pi; d = dmin + r.random() * (dmax - dmin)
        x, z = cxz[0] + math.cos(a) * d, cxz[1] + math.sin(a) * d
        inside_house = -2 < x < 36 and -2 < z < 35
        on_patio = math.hypot(x - cx, z - cz) < R + 1.0 or (10 < x < 15 and 33 < z < 62) or (-6 < x < 33 and 40 < z < 52)
        if not inside_house and not on_patio: return x, z
for i in range(40):   # mossy granite boulders around the cabin
    x, z = free_spot(9, 38)
    inst(ROCKS[i % len(ROCKS)], 'Boulder', x, terr(x, z) - 0.3, z, FT * (0.32 + r.random() * 0.4), r.random() * 6.3, S)
for i in range(16):   # and ringing the Thermeä patio, as on the sheet
    a = i / 16 * 2 * math.pi + r.random() * 0.2; d = R + 1.6 + r.random() * 1.4
    x, z = cx + math.cos(a) * d, cz + math.sin(a) * d
    if (10 < x < 15 and z < cz) or (-6 < x < 33 and 40 < z < 52 and abs(z - cz) < 7 and (x < 3 or x > 18)): continue
    inst(ROCKS[i % len(ROCKS)], 'Boulder', x, GROUND - 0.25, z, FT * (0.25 + r.random() * 0.3), r.random() * 6.3, S)
for i in range(220):  # ferns along walls, paths, the clearing edge and into the woods
    x, z = free_spot(4, 46)
    inst(FERNS[i % len(FERNS)], 'Fern', x, terr(x, z), z, FT * (1.0 + r.random() * 0.7), r.random() * 6.3, S)
for i in range(420):  # grass clumps: the groundcover that breaks up the forest floor
    x, z = free_spot(3, 52)
    inst(GRASS[0], 'Grass', x, terr(x, z) - 0.05, z, FT * (0.8 + r.random() * 0.9), r.random() * 6.3, S)
for i in range(70):   # young spruces and firs close in
    x, z = free_spot(7, 30)
    inst(SPRUCE_C if i % 3 else FIR_C, 'YoungSpruce', x, terr(x, z), z, 3 + r.random() * 5, r.random() * 6.3, S)
for i in range(360):  # the forest: black spruce, balsam fir and pine at varied heights
    while True:
        a = r.random() * 2 * math.pi; d = 32 + (r.random() ** 0.6) * 100
        x, z = 14 + math.cos(a) * d, 28 + math.sin(a) * d
        if not (-14 < x < 48 and -14 < z < 64): break
    q = r.random()
    me, hgt = (SPRUCE_C, 32 + r.random() * 26) if q < .5 else (FIR_C, 22 + r.random() * 18) if q < .8 else (PINE_C, 40 + r.random() * 24)
    inst(me, 'Spruce', x, terr(x, z), z, hgt, r.random() * 6.3, S)

# ---------- rounded edges: a light 3-segment bevel with hardened normals on every tagged block ----------
round_cyls()
for ob in bpy.data.objects:
    b = ob.get('bev') if ob.type == 'MESH' else None
    if not b: continue
    md = ob.modifiers.new('bev', 'BEVEL')
    md.width = b; md.segments = 3; md.limit_method = 'ANGLE'; md.angle_limit = math.radians(40)
    md.use_clamp_overlap = True; md.harden_normals = True
    for poly in ob.data.polygons: poly.use_smooth = True

# ---------- UVs: planar projection in feet for every generated mesh with a textured material ----------
for ob in bpy.data.objects:
    if ob.type != 'MESH' or ob.data.uv_layers: continue
    me = ob.data
    tiles = {i: TEX_TILE.get(m.name) for i, m in enumerate(me.materials) if m}
    if not any(tiles.values()): continue
    uvl = me.uv_layers.new(name='UVMap')
    for poly in me.polygons:
        t = tiles.get(poly.material_index)
        if not t: continue
        n = poly.normal; ax = max(range(3), key=lambda i: abs(n[i]))
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            u, v = (co.x, co.y) if ax == 2 else (co.y, co.z) if ax == 0 else (co.x, co.z)
            uvl.data[li].uv = (u / t, v / t)

# ---------- export ----------
opts = dict(filepath=GLB, export_format='GLB', export_yup=True, export_apply=True, export_lights=False,
            export_cameras=False, export_extras=False, export_image_format='WEBP', export_image_quality=80,
            export_gpu_instances=True,
            export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6,
            export_draco_position_quantization=14, export_draco_normal_quantization=10,
            export_draco_texcoord_quantization=12)
try:
    bpy.ops.export_scene.gltf(**opts)
except TypeError:
    for k in ('export_image_quality', 'export_gpu_instances'): opts.pop(k, None)
    print('NOTE: exporter rejected an option, exported without it')
    bpy.ops.export_scene.gltf(**opts)
bpy.ops.wm.save_as_mainfile(filepath=BLEND)

# no Blender render: the web viewer is the only place this model is judged
print('BUILD_OK', len(bpy.data.objects), 'objects')
