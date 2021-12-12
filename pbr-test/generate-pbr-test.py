import bpy

# More subdivisions = more polygons but more spherical meshes
SUBDIVISION_COUNT = 4

#
# Destroy all existing scenes, leaving just a new empty scene
#
empty_scene = bpy.data.scenes.new("Scene")
for scene in bpy.data.scenes:
    if scene != empty_scene:
        bpy.context.window.scene = scene
        bpy.ops.scene.delete()

empty_scene.name = "Scene"
        
#
# Garbage collect all blender objects not referenced by the (now empty) scene
#
bpy.ops.outliner.orphans_purge(do_recursive=True)

# Create a grid of spheres with different materials, varying metalness and roughness values on different axes
# Default configuration is a 6x6 grid with values [0, 0.2, 0.4, 0.6, 0.8, 1.0]
for metalness in range(0, 11, 2):
    for roughness in range(0, 11, 2):
        # Create a new material
        material = bpy.data.materials.new(name="m{}_r{}".format(metalness, roughness))
        material.use_nodes = True

        # Find the BSDF node
        bsdf = material.node_tree.nodes["Principled BSDF"]

        # Configure the BSDF node
        bsdf.inputs['Roughness'].default_value = roughness / 10
        bsdf.inputs['Metallic'].default_value = metalness / 10
        bsdf.inputs['Base Color'].default_value = (1.0, 0.0, 0.0, 1.0)
        
        # Add a sphere (alternate version using uv sphere instead below)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=SUBDIVISION_COUNT, radius=1, location=(metalness * 3, 0, roughness * 3))
        #bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, location=(metalness * 3, 0, roughness * 3))

        # Assign the material to the sphere
        bpy.context.active_object.data.materials.append(material)
        
# Alternative example of using a directional light
#bpy.ops.object.light_add(
#    type='SUN', 
#    radius=1,
#    align='WORLD',
#    location=(15, -25, 15),
#    rotation=(1.5708, 0, 0),
#    scale=(1, 1, 1)
#)

bpy.ops.object.light_add(
    type='POINT', 
    align='WORLD', 
    location=(15, -25, 15), 
    scale=(1, 1, 1)
)
bpy.context.active_object.data.energy=5000

# Alternate example of using a perspective projection
#bpy.ops.object.camera_add(
#    enter_editmode=False, 
#    align='VIEW', 
#    location=(15, -30, 15), 
#    rotation=(1.5707, 0, 0), 
#    scale=(1, 1, 1)
#)
#bpy.context.active_object.data.type = 'ORTHO'
#bpy.context.active_object.data.ortho_scale = 60

bpy.ops.object.camera_add(
    enter_editmode=False, 
    align='VIEW', 
    location=(15, -90, 15), 
    rotation=(1.5707, 0, 0), 
    scale=(1, 1, 1)
)
bpy.context.active_object.data.type = 'PERSP'
bpy.context.scene.camera = bpy.context.active_object

# Enable the eevee engine
bpy.context.scene.render.engine = 'BLENDER_EEVEE'

# Enable the cycles engine so that F12 render the scene raytraced with direct lighting only
#bpy.context.scene.render.engine = 'CYCLES'
#bpy.context.scene.cycles.max_bounces = 0

# If you want to render to disk, enable this
#bpy.context.scene.render.filepath='pbr-test-render.png'
#bpy.ops.render.render(write_still=1)

#
# Save file to disk. Enabling compression reduces the blend file size. We also want to
# save all paths as relative so that the .blend/textures folder can be relocated
# together and still work
#
bpy.ops.wm.save_as_mainfile(filepath='pbr-test.blend', compress=True, relative_remap=True)
