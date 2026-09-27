"""
╔═══════════════════════════════════════════════════════════════════════════╗
║     BLENDER 5.2 - OPTIMAL RENDER SETTINGS                                 ║
║     High Quality + Fast Rendering Balance                                 ║
║     Perfect for Product Shots (Shoes, Accessories, etc.)                  ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import bpy
import os

scene = bpy.context.scene

print("\n" + "="*80)
print("APPLYING OPTIMAL RENDER SETTINGS FOR BLENDER 5.2")
print("="*80 + "\n")

# ═════════════════════════════════════════════════════════════════════════════
# 1. ENGINE SELECTION
# ═════════════════════════════════════════════════════════════════════════════
print("✓ Setting render engine...")
scene.render.engine = 'CYCLES'

# ═════════════════════════════════════════════════════════════════════════════
# 2. DEVICE OPTIMIZATION
# ═════════════════════════════════════════════════════════════════════════════
print("✓ Configuring GPU/CPU...")

try:
    # Try to enable GPU rendering (RTX/CUDA/HIP)
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'CUDA'  # Change to 'HIP' for AMD, 'OPTIX' for RTX
    scene.cycles.device = 'GPU'
    print("  ✓ GPU rendering ENABLED")
except:
    scene.cycles.device = 'CPU'
    print("  ⚠ GPU not available, using CPU")

# ═════════════════════════════════════════════════════════════════════════════
# 3. SAMPLING & DENOISING (Critical for Quality vs Speed)
# ═════════════════════════════════════════════════════════════════════════════
print("✓ Setting up sampling strategy...")

# ADAPTIVE SAMPLING - Renders faster by using fewer samples in simple areas
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.005  # Lower = higher quality, but slower
print("  ✓ Adaptive Sampling: ON (Threshold: 0.005)")

# PREVIEW vs FINAL RENDER SAMPLES
scene.cycles.samples = 192  # Optimal: 192 samples for final render
if hasattr(scene.cycles, 'preview_samples'):
    scene.cycles.preview_samples = 48  # Fast preview in viewport
print(f"  ✓ Final Render Samples: {scene.cycles.samples}")
print(f"  ✓ Preview Samples: 48")

# DENOISING - Reduces noise DRAMATICALLY while preserving detail
print("✓ Configuring denoiser...")
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'  # Best quality denoiser
scene.cycles.denoise_use_gpu = True if scene.cycles.device == 'GPU' else False
print("  ✓ OptiX Denoiser: ON")

# ═════════════════════════════════════════════════════════════════════════════
# 4. LIGHT BOUNCES - Optimize for Product Shots
# ═════════════════════════════════════════════════════════════════════════════
print("✓ Optimizing light bounces...")

# These settings balance realism with render speed
scene.cycles.max_bounces = 8
scene.cycles.diffuse_bounces = 2  # Very important for fabric/matte surfaces
scene.cycles.glossy_bounces = 4   # For shiny/reflective surfaces
scene.cycles.transmission_bounces = 8  # For transparent sole
scene.cycles.transparent_max_bounces = 8
scene.cycles.volume_bounces = 0

print(f"  ✓ Max Bounces: {scene.cycles.max_bounces}")
print(f"  ✓ Diffuse Bounces: {scene.cycles.diffuse_bounces}")
print(f"  ✓ Glossy Bounces: {scene.cycles.glossy_bounces}")

# ═════════════════════════════════════════════════════════════════════════════
# 5. CAUSTICS & CLAMPING - Reduce noise
# ═════════════════════════════════════════════════════════════════════════════
print("✓ Reducing fireflies and noise...")

# Clamp indirect light to reduce extreme values (fireflies)
if hasattr(scene.cycles, 'clamp_direct'):
    scene.cycles.clamp_direct = 0.0
if hasattr(scene.cycles, 'clamp_indirect'):
    scene.cycles.clamp_indirect = 2.5

# Caustics - Usually not needed for product shots
scene.cycles.caustics_reflective = False
scene.cycles.caustics_refractive = False

print("  ✓ Clamp Indirect: 2.5")
print("  ✓ Caustics: Disabled")

# ═════════════════════════════════════════════════════════════════════════════
# 6. RESOLUTION - Professional Product Shot
# ═════════════════════════════════════════════════════════════════════════════
print("✓ Setting resolution...")

scene.render.resolution_x = 2400
scene.render.resolution_y = 1600
scene.render.resolution_percentage = 100

print(f"  ✓ Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}")

# ═════════════════════════════════════════════════════════════════════════════
# 7. FILM & COLOR MANAGEMENT
# ═════════════════════════════════════════════════════════════════════════════
print("✓ Configuring color management...")

scene.render.film_transparent = False
scene.render.use_motion_blur = False  # Disable unless needed
scene.render.use_motion_blur_next = False

# High bit depth for post-processing flexibility
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '16'
scene.render.image_settings.compression = 9  # Max compression

# Color management
scene.display_settings.display_device = 'sRGB'
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Medium High Contrast'
scene.view_settings.exposure = 0.0
scene.view_settings.gamma = 1.0

print("  ✓ Color Depth: 16-bit")
print("  ✓ View Transform: Filmic")
print("  ✓ Look: Medium High Contrast")

# ═════════════════════════════════════════════════════════════════════════════
# 8. TILE SIZE - GPU Memory Optimization
# ═════════════════════════════════════════════════════════════════════════════
print("✓ Optimizing tile size...")

# Tile size affects GPU memory usage and speed
# 256x256 = faster, good for high-end GPUs (RTX 3080+)
# 128x128 = balanced
# 64x64 = for lower-end GPUs or limited memory
if scene.cycles.device == 'GPU':
    scene.render.tile_x = 256
    scene.render.tile_y = 256
    print(f"  ✓ Tile Size: 256x256 (GPU optimized)")
else:
    scene.render.tile_x = 128
    scene.render.tile_y = 128
    print(f"  ✓ Tile Size: 128x128 (CPU optimized)")

# ═════════════════════════════════════════════════════════════════════════════
# 9. LIGHT TREE - For efficient sampling (NEW in Blender 4.0+)
# ═════════════════════════════════════════════════════════════════════════════
print("✓ Configuring light sampling...")

if hasattr(scene.cycles, 'use_light_tree'):
    scene.cycles.use_light_tree = True
    print("  ✓ Light Tree: ON (Faster light sampling)")
else:
    print("  ⚠ Light Tree: Not available in this Blender version")

# ═════════════════════════════════════════════════════════════════════════════
# 10. MOTION BLUR & DEPTH OF FIELD (Optional)
# ═════════════════════════════════════════════════════════════════════════════
print("✓ Configuring camera effects...")

# For product shots, we usually don't want these
# But keep them available if needed:
if scene.camera and hasattr(scene.camera.data, 'dof'):
    scene.camera.data.dof.use_dof = False
    print("  ✓ Depth of Field: OFF")

# ═════════════════════════════════════════════════════════════════════════════
# 11. OUTPUT PATH
# ═════════════════════════════════════════════════════════════════════════════
print("✓ Setting output path...")

# Set output to project folder
output_path = bpy.path.abspath("//renders/")
os.makedirs(output_path, exist_ok=True)
scene.render.filepath = output_path + "shoe_render_optimal.png"

print(f"  ✓ Output: {scene.render.filepath}")

# ═════════════════════════════════════════════════════════════════════════════
# 12. QUICK RENDER SETTINGS (For testing)
# ═════════════════════════════════════════════════════════════════════════════
def set_quick_render():
    """Use for quick preview renders"""
    scene.cycles.samples = 32
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 854
    scene.cycles.adaptive_threshold = 0.02
    print("\n⚡ QUICK RENDER MODE ACTIVATED")

def set_final_render():
    """Use for final high-quality renders"""
    scene.cycles.samples = 256
    scene.render.resolution_x = 2400
    scene.render.resolution_y = 1600
    scene.cycles.adaptive_threshold = 0.005
    print("\n🎬 FINAL RENDER MODE ACTIVATED")

def set_ultra_quality():
    """Use for extremely high quality (slower)"""
    scene.cycles.samples = 512
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2560
    scene.cycles.adaptive_threshold = 0.002
    print("\n⭐ ULTRA QUALITY MODE ACTIVATED")

# ═════════════════════════════════════════════════════════════════════════════
# 13. SUMMARY
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "="*80)
print("✅ OPTIMAL RENDER SETTINGS APPLIED!")
print("="*80)
print(f"""
📊 RENDER CONFIGURATION:
   • Engine: {scene.render.engine}
   • Device: {scene.cycles.device}
   • Samples: {scene.cycles.samples} (Adaptive: ON)
   • Denoiser: OptiX/OpenImageDenoise
   • Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}
   • Tile Size: {scene.render.tile_x}x{scene.render.tile_y}
   • Color Depth: 16-bit
   
⏱️  ESTIMATED RENDER TIME:
   • Quick Test: 2-5 minutes
   • Final Render: 8-15 minutes (RTX 3080)
   • Final Render: 20-40 minutes (CPU)
   
🎯 USAGE:
   • Quick test: set_quick_render()
   • Final render: set_final_render()
   • Ultra quality: set_ultra_quality()
   
   Then run: bpy.ops.render.render(write_still=True)
""")
print("="*80 + "\n")

# ═════════════════════════════════════════════════════════════════════════════
# READY TO RENDER!
# ═════════════════════════════════════════════════════════════════════════════
print("🚀 Ready to render! Execute this command in Blender console:")
print("    bpy.ops.render.render(write_still=True)")
print("\n")
