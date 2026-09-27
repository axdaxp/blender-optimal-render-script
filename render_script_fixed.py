import bpy
import math
from mathutils import Vector

# =========================================================
# CLEAN SCENE
# =========================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

for block in bpy.data.meshes:
    if block.users == 0:
        bpy.data.meshes.remove(block)

for block in bpy.data.materials:
    if block.users == 0:
        bpy.data.materials.remove(block)

for block in bpy.data.images:
    if block.users == 0:
        bpy.data.images.remove(block)

# =========================================================
# SCENE SETTINGS - BLENDER 5.2 COMPATIBLE
# =========================================================
scene = bpy.context.scene
scene.render.engine = 'CYCLES'

# ===== CYCLES SETTINGS =====
scene.cycles.device = 'GPU'  # Change to 'CPU' if GPU not available
scene.cycles.samples = 256  # High quality
scene.cycles.preview_samples = 32

# Denoising
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'

# Bounces
scene.cycles.max_bounces = 12
scene.cycles.diffuse_bounces = 4
scene.cycles.glossy_bounces = 8
scene.cycles.transmission_bounces = 12
scene.cycles.transparent_max_bounces = 8

# Adaptive Sampling
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.01

# Clamp
scene.cycles.clamp_direct = 0.0
scene.cycles.clamp_indirect = 1.0

# Light Paths
scene.cycles.use_light_tree = True

# ===== RENDER SETTINGS =====
scene.render.resolution_x = 2400
scene.render.resolution_y = 1600
scene.render.resolution_percentage = 100
scene.render.film_transparent = False

# ===== COLOR MANAGEMENT =====
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Medium High Contrast'
scene.view_settings.exposure = 0.2
scene.view_settings.gamma = 1.0

# ===== OUTPUT =====
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '16'
scene.render.filepath = "//shoe_render_hq.png"

# =========================================================
# WORLD - HDRI / BACKGROUND
# =========================================================
world = bpy.data.worlds.new("World")
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.04, 0.05, 0.06, 1.0)  # Very Dark Gray
bg.inputs[1].default_value = 0.8
scene.world = world

# =========================================================
# LIGHTS - PROFESSIONAL 3-POINT LIGHTING
# =========================================================
# KEY LIGHT (Main/Top Light)
bpy.ops.object.light_add(type='AREA', location=(3, -8, 6))
key_light = bpy.context.object
key_light.name = "KeyLight"
key_light.data.energy = 3000
key_light.data.shape = 'RECTANGLE'
key_light.data.size = 5
key_light.data.size_y = 3
key_light.rotation_euler = (math.radians(65), 0, math.radians(25))

# FILL LIGHT (Left Side - Soft)
bpy.ops.object.light_add(type='AREA', location=(-5, -4, 4))
fill_light = bpy.context.object
fill_light.name = "FillLight"
fill_light.data.energy = 1200
fill_light.data.shape = 'RECTANGLE'
fill_light.data.size = 4
fill_light.data.size_y = 2.5
fill_light.rotation_euler = (math.radians(75), 0, math.radians(-45))

# RIM LIGHT (Back Light - Highlight Edge)
bpy.ops.object.light_add(type='AREA', location=(0, 6, 3.5))
rim_light = bpy.context.object
rim_light.name = "RimLight"
rim_light.data.energy = 800
rim_light.data.shape = 'RECTANGLE'
rim_light.data.size = 3.5
rim_light.data.size_y = 1.5
rim_light.rotation_euler = (math.radians(85), 0, math.radians(0))

# =========================================================
# CAMERA - PROFESSIONAL PRODUCT SHOT
# =========================================================
bpy.ops.object.camera_add(location=(0, -10, 3.5))
camera = bpy.context.object
camera.name = "RenderCamera"
camera.rotation_euler = (math.radians(75), 0, math.radians(0))
camera.data.lens = 60
camera.data.sensor_width = 36
camera.data.dof.use_dof = False
scene.camera = camera

# =========================================================
# BACKGROUND PLANE - GRADIENT CATCHER
# =========================================================
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 12, 2))
bg_plane = bpy.context.object
bg_plane.name = "BackgroundCatcher"
bg_plane.rotation_euler = (math.radians(90), 0, 0)
bg_plane.scale = (1, 1.5, 1)

mat_bg = bpy.data.materials.new(name="BackgroundMat")
mat_bg.use_nodes = True
nodes = mat_bg.node_tree.nodes
links = mat_bg.node_tree.links

for node in list(nodes):
    nodes.remove(node)

out = nodes.new(type='ShaderNodeOutputMaterial')
out.location = (400, 0)

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)
bsdf.inputs['Base Color'].default_value = (0.08, 0.10, 0.12, 1.0)
bsdf.inputs['Roughness'].default_value = 0.95

links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
bg_plane.data.materials.append(mat_bg)

# =========================================================
# FLOOR / GROUND PLANE
# =========================================================
bpy.ops.mesh.primitive_plane_add(size=25, location=(0, 0, -0.05))
floor = bpy.context.object
floor.name = "GroundPlane"

mat_floor = bpy.data.materials.new(name="FloorMat")
mat_floor.use_nodes = True
nodes = mat_floor.node_tree.nodes
links = mat_floor.node_tree.links

for node in list(nodes):
    nodes.remove(node)

out = nodes.new(type='ShaderNodeOutputMaterial')
out.location = (300, 0)

# Shadow catcher + reflective
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)
bsdf.inputs['Base Color'].default_value = (0.11, 0.13, 0.15, 1.0)
bsdf.inputs['Roughness'].default_value = 0.55
bsdf.inputs['Metallic'].default_value = 0.02

links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
floor.data.materials.append(mat_floor)

# =========================================================
# PLACEHOLDER SHOE MODEL (Will use your imported model)
# =========================================================
# Create a simple base form - REPLACE with your actual shoe model
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=64, 
    ring_count=48, 
    radius=1.0, 
    location=(0, 0, 1.2)
)
shoe = bpy.context.object
shoe.name = "ShoeUpper"
shoe.scale = (2.2, 1.3, 0.8)

# Subdivisions for smoothness
bpy.ops.object.modifier_add(type='SUBSURF')
shoe.modifiers["Subdivision"].levels = 3
shoe.modifiers["Subdivision"].render_levels = 3

# Smooth shading
bpy.ops.object.shade_smooth()

# =========================================================
# MATERIAL: UPPER FABRIC (Woven Textile)
# =========================================================
mat_upper = bpy.data.materials.new(name="FabricUpper")
mat_upper.use_nodes = True
nodes = mat_upper.node_tree.nodes
links = mat_upper.node_tree.links

for node in list(nodes):
    nodes.remove(node)

# Output
out = nodes.new(type='ShaderNodeOutputMaterial')
out.location = (600, 0)

# Main BSDF
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (350, 0)

# Textures for fabric weave
noise = nodes.new(type='ShaderNodeTexNoise')
noise.location = (-300, 250)
noise.inputs['Scale'].default_value = 220.0
noise.inputs['Detail'].default_value = 8.0
noise.inputs['Roughness'].default_value = 0.65

# Bump node for fabric texture
bump = nodes.new(type='ShaderNodeBump')
bump.location = (50, 250)
bump.inputs['Strength'].default_value = 0.12

# Wave for subtle line pattern
wave = nodes.new(type='ShaderNodeTexWave')
wave.location = (-300, -50)
wave.inputs['Scale'].default_value = 200.0
wave.inputs['Distortion'].default_value = 0.5

# Mix RGB for blending textures
mix_color = nodes.new(type='ShaderNodeMix')
mix_color.location = (100, -100)
mix_color.data_type = 'RGBA'
mix_color.inputs['A'].default_value = (0.72, 0.72, 0.72, 1.0)
mix_color.inputs['B'].default_value = (0.85, 0.85, 0.85, 1.0)

# Setup connections
links.new(noise.outputs['Fac'], bump.inputs['Height'])
links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
links.new(wave.outputs['Fac'], mix_color.inputs['Factor'])
links.new(mix_color.outputs['Result'], bsdf.inputs['Base Color'])

# Material properties
bsdf.inputs['Roughness'].default_value = 0.72
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Sheen Weight'].default_value = 0.15
bsdf.inputs['Sheen Tint'].default_value = 0.35
bsdf.inputs['Coat Weight'].default_value = 0.08
bsdf.inputs['Coat Roughness'].default_value = 0.35

links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

shoe.data.materials.append(mat_upper)

# =========================================================
# MATERIAL: SOLE / TRANSPARENT BASE
# =========================================================
mat_sole = bpy.data.materials.new(name="TransparentSole")
mat_sole.use_nodes = True
nodes = mat_sole.node_tree.nodes
links = mat_sole.node_tree.links

for node in list(nodes):
    nodes.remove(node)

out = nodes.new(type='ShaderNodeOutputMaterial')
out.location = (400, 0)

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)

bsdf.inputs['Base Color'].default_value = (0.42, 0.45, 0.48, 1.0)
bsdf.inputs['Roughness'].default_value = 0.25
bsdf.inputs['Transmission'].default_value = 0.70
bsdf.inputs['IOR'].default_value = 1.50
bsdf.inputs['Coat Weight'].default_value = 0.30
bsdf.inputs['Coat Roughness'].default_value = 0.25

links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

# Create sole object
bpy.ops.mesh.primitive_cylinder_add(
    vertices=96, 
    radius=1.2, 
    depth=0.25, 
    location=(0, 0, 0.05)
)
sole = bpy.context.object
sole.name = "ShoeSOLE"
sole.scale = (2.5, 1.6, 0.3)

bpy.ops.object.shade_smooth()
sole.data.materials.append(mat_sole)

# =========================================================
# MATERIAL: DARK ACCENTS / HEEL
# =========================================================
mat_dark = bpy.data.materials.new(name="DarkHeelAccent")
mat_dark.use_nodes = True
nodes = mat_dark.node_tree.nodes
links = mat_dark.node_tree.links

for node in list(nodes):
    nodes.remove(node)

out = nodes.new(type='ShaderNodeOutputMaterial')
out.location = (300, 0)

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)
bsdf.inputs['Base Color'].default_value = (0.12, 0.14, 0.17, 1.0)
bsdf.inputs['Roughness'].default_value = 0.60
bsdf.inputs['Metallic'].default_value = 0.05

links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

# =========================================================
# APPLY SMOOTH SHADING
# =========================================================
for obj in bpy.context.view_layer.objects:
    if obj.type == 'MESH' and obj.name not in ['BackgroundCatcher', 'GroundPlane']:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.shade_smooth()
        obj.select_set(False)

# =========================================================
# COMPOSITOR - POST PROCESSING
# =========================================================
scene.use_nodes = True
comp_nodes = scene.node_tree.nodes
comp_links = scene.node_tree.links

# Clear default nodes
comp_nodes.clear()

# Render Layers
render_node = comp_nodes.new(type='CompositorNodeRLayers')
render_node.location = (0, 0)

# Composite Output
composite_node = comp_nodes.new(type='CompositorNodeComposite')
composite_node.location = (400, 0)

# Viewer (optional)
viewer_node = comp_nodes.new(type='CompositorNodeViewer')
viewer_node.location = (400, -100)

# Connect
comp_links.new(render_node.outputs['Image'], composite_node.inputs['Image'])
comp_links.new(render_node.outputs['Image'], viewer_node.inputs['Image'])

# =========================================================
# FINAL SETTINGS & RENDER
# =========================================================
print("=" * 60)
print("BLENDER 5.2 - HIGH QUALITY SHOE RENDER")
print("=" * 60)
print(f"Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}")
print(f"Samples: {scene.cycles.samples}")
print(f"Engine: {scene.render.engine}")
print(f"Device: {scene.cycles.device}")
print(f"Denoiser: {scene.cycles.denoiser}")
print(f"Output: {scene.render.filepath}")
print("=" * 60)
print("⚠️  IMPORTANT: Replace 'ShoeUpper' and 'ShoeSOLE' objects")
print("    with your actual shoe model from DBJ_Custom_Performance_Shoe")
print("=" * 60)
print("\nStarting render...")

# RENDER
bpy.ops.render.render(write_still=True)

print("✅ Render complete!")
print(f"Saved to: {bpy.path.abspath(scene.render.filepath)}")
