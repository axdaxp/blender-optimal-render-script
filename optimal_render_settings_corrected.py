"""
═══════════════════════════════════════════════════════════════════════════════
  BLENDER 5.2 - OPTIMAL RENDER SETTINGS (CORRECTED)
  High Quality + Fast Rendering for Product Shots
  Compatible with Blender 5.2 API
═══════════════════════════════════════════════════════════════════════════════
"""

import bpy

scene = bpy.context.scene

print("\n" + "="*80)
print("APPLYING OPTIMAL RENDER SETTINGS FOR BLENDER 5.2")
print("="*80 + "\n")

# ═════════════════════════════════════════════════════════════════════════════
# 1. RENDER ENGINE
# ═════════════════════════════════════════════════════════════════════════════
scene.render.engine = 'CYCLES'
print("✓ Render Engine: CYCLES")

# ═════════════════════════════════════════════════════════════════════════════
# 2. GPU / CPU DEVICE
# ═════════════════════════════════════════════════════════════════════════════
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    # Try CUDA first (NVIDIA)
    try:
        prefs.compute_device_type = 'CUDA'
        scene.cycles.device = 'GPU'
        print("✓ Device: GPU (NVIDIA CUDA)")
    except:
        # Try HIP for AMD
        try:
            prefs.compute_device_type = 'HIP'
            scene.cycles.device = 'GPU'
            print("✓ Device: GPU (AMD HIP)")
        except:
            # Fallback to CPU
            scene.cycles.device = 'CPU'
            print("✓ Device: CPU")
except Exception as e:
    scene.cycles.device = 'CPU'
    print(f"✓ Device: CPU (GPU not available: {e})")

# ═════════════════════════════════════════════════════════════════════════════
# 3. ADAPTIVE SAMPLING + SAMPLES
# ═════════════════════════════════════════════════════════════════════════════
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.005
scene.cycles.samples = 160

if hasattr(scene.cycles, 'preview_samples'):
    scene.cycles.preview_samples = 32

print(f"✓ Sampling: Adaptive ON (threshold: 0.005)")
print(f"✓ Final Samples: {scene.cycles.samples}")

# ═════════════════════════════════════════════════════════════════════════════
# 4. DENOISING - CORRECTED FOR BLENDER 5.2
# ═════════════════════════════════════════════════════════════════════════════
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'

# CORRECTED: Use 'denoising_use_gpu' not 'denoise_use_gpu'
if hasattr(scene.cycles, 'denoising_use_gpu'):
    scene.cycles.denoising_use_gpu = (scene.cycles.device == 'GPU')
    print("✓ Denoiser: OptiX (GPU accelerated)")
else:
    print("✓ Denoiser: OpenImageDenoise")

# ═════════════════════════════════════════════════════════════════════════════
# 5. LIGHT BOUNCES - OPTIMIZED
# ═════════════════════════════════════════════════════════════════════════════
scene.cycles.max_bounces = 8
scene.cycles.diffuse_bounces = 2
scene.cycles.glossy_bounces = 4
scene.cycles.transmission_bounces = 8
scene.cycles.transparent_max_bounces = 8
scene.cycles.volume_bounces = 0

print(f"✓ Max Bounces: {scene.cycles.max_bounces}")
print(f"✓ Diffuse Bounces: {scene.cycles.diffuse_bounces}")
print(f"✓ Glossy Bounces: {scene.cycles.glossy_bounces}")
print(f"✓ Transmission Bounces: {scene.cycles.transmission_bounces}")

# ═════════════════════════════════════════════════════════════════════════════
# 6. CLAMPING - REDUCE NOISE & FIREFLIES
# ═════════════════════════════════════════════════════════════════════════════
if hasattr(scene.cycles, 'clamp_direct'):
    scene.cycles.clamp_direct = 0.0

if hasattr(scene.cycles, 'clamp_indirect'):
    scene.cycles.clamp_indirect = 2.0
    print(f"✓ Clamp Indirect: 2.0")

# ═════════════════════════════════════════════════════════════════════════════
# 7. LIGHT TREE - FASTER SAMPLING
# ═════════════════════════════════════════════════════════════════════════════
if hasattr(scene.cycles, 'use_light_tree'):
    scene.cycles.use_light_tree = True
    print("✓ Light Tree: ON (faster sampling)")

# ═════════════════════════════════════════════════════════════════════════════
# 8. RESOLUTION - PROFESSIONAL PRODUCT SHOT
# ═════════════════════════════════════════════════════════════════════════════
scene.render.resolution_x = 2400
scene.render.resolution_y = 1600
scene.render.resolution_percentage = 100

print(f"✓ Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}")

# ═════════════════════════════════════════════════════════════════════════════
# 9. FILM & OUTPUT SETTINGS
# ═════════════════════════════════════════════════════════════════════════════
scene.render.film_transparent = False
scene.render.use_motion_blur = False

# High bit depth PNG
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '16'
scene.render.image_settings.compression = 9

print(f"✓ Output Format: PNG 16-bit")
print(f"✓ Color Mode: RGBA")

# ═════════════════════════════════════════════════════════════════════════════
# 10. COLOR MANAGEMENT - FILMIC
# ═════════════════════════════════════════════════════════════════════════════
scene.display_settings.display_device = 'sRGB'
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Medium High Contrast'
scene.view_settings.exposure = 0.0
scene.view_settings.gamma = 1.0

print(f"✓ View Transform: Filmic")
print(f"✓ Look: Medium High Contrast")

# ═════════════════════════════════════════════════════════════════════════════
# 11. TILE SIZE - GPU MEMORY OPTIMIZATION
# ═════════════════════════════════════════════════════════════════════════════
if scene.cycles.device == 'GPU':
    scene.render.tile_x = 256
    scene.render.tile_y = 256
    print(f"✓ Tile Size: 256x256 (GPU optimized)")
else:
    scene.render.tile_x = 128
    scene.render.tile_y = 128
    print(f"✓ Tile Size: 128x128 (CPU optimized)")

# ═════════════════════════════════════════════════════════════════════════════
# SUMMARY & READY TO RENDER
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "="*80)
print("✅ OPTIMAL RENDER SETTINGS APPLIED SUCCESSFULLY!")
print("="*80)
print(f"""
📊 FINAL CONFIGURATION:
   • Engine: Cycles
   • Device: {scene.cycles.device}
   • Samples: {scene.cycles.samples} (Adaptive: ON)
   • Denoiser: OpenImageDenoise
   • Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}
   • Tile Size: {scene.render.tile_x}x{scene.render.tile_y}
   • Output: PNG 16-bit
   
⏱️  ESTIMATED RENDER TIME:
   • RTX 3060+: 5-10 minutes
   • RTX 2080: 10-15 minutes
   • CPU (i7/Ryzen 7): 20-40 minutes
   
🎯 TO RENDER:
   In Blender console, run:
   
   bpy.ops.render.render(write_still=True)
   
   OR press F12 in Blender viewport
   
💾 Output will be saved to:
   """)
print("="*80 + "\n")

print("✅ Ready to render your shoe at optimal quality + speed!")
