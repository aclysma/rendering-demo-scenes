import bpy
import os

blend_path = bpy.data.filepath
working_dir = os.path.dirname(blend_path)
fbx_interior_file_path = os.path.join(working_dir, "BistroInterior.fbx")
fbx_exterior_file_path = os.path.join(working_dir, "BistroExterior.fbx")

#TODO: The interior/exterior objects don't perfectly line up
#TODO: The exterior FBX has opaque windows that need to be removed
#TODO: Exclude the animation data (on the lights that cross the streets)
#TODO: Ambient occlusion not set up properly
#TODO: Remove the empty on the exterior FBX
#TODO: Make sure it saves texture paths relative instead of absolute?
#TODO: Automatically handle copying data out of the Bistro_v5_2 folder to this folder?

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

#
# Import the interior FBX file and bake the scale transform into the meshes
#
bpy.ops.import_scene.fbx(filepath=fbx_interior_file_path)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

#
# Delete all objects named "exterior" that came from the interior FBX
#
for object in bpy.data.objects:
    object.select_set("Bistro_Research_Exterior" in object.name)

bpy.ops.object.delete()

#
# Import the exterior FBX file and bake the scale transform into the meshes
#
bpy.ops.import_scene.fbx(filepath=fbx_exterior_file_path)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

#
# Fix the materials (the nodes aren't properly hooked up to the BSDF node)
#
for material in bpy.data.materials:
    print("Process material", material.name)
    
    # Ignore this blender built-in material
    if material.name == "Dots Stroke":
        print("  Skip built-in blender material")
        continue
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # We will search for these nodes in the shader graph
    output_node = None
    bsdf_node = None
    normal_map_node = None
    base_color_image_node = None
    normal_image_node = None
    pbr_image_node = None
    emissive_image_node = None
    
    # Look at each node and see if it's something we're looking for
    for node in nodes:
        if isinstance(node, bpy.types.ShaderNodeBsdfPrincipled):
            print("    BSDF:", node.name)
            bsdf_node = node
        elif isinstance(node, bpy.types.ShaderNodeOutputMaterial):
            print("    OUTPUT:", node.name)
            output_node = node
        elif isinstance(node, bpy.types.ShaderNodeNormalMap):
            print("    NORMAL MAP:", node.name)
            normal_map_node = node
        elif isinstance(node, bpy.types.ShaderNodeTexImage):    
            fp = node.image.filepath
            if "_BaseColor.dds" in fp:
                print("    IMAGE (BASE COLOR):", node.name, node.image.filepath)
                base_color_image_node = node
            elif "_Normal.dds" in fp:
                print("    IMAGE (NORMAL):", node.name, node.image.filepath)
                normal_image_node = node
            elif "_Specular.dds" in fp:
                print("    IMAGE (PBR):", node.name, node.image.filepath)
                pbr_image_node = node
            elif "_Emissive.dds" in fp:
                print("    IMAGE (EMISSIVE):", node.name, node.image.filepath)
                emissive_image_node = node
            else:
                print("*********** UNKNOWN IMAGE NODE ***********", node, node.image.filepath)
        else:
            print("*********** UNKNOWN NODE ***********", node)
        
    # The normal maps seem ok and don't need fixing
    # The base color seems ok. Alpha only seems to be hooked up if the material can actually be transparent.
    #   In which case, there is a second image node that connects to the BRDF alpha input
    # The specular image input is wrong.. instead of hooking it to the specular input
    #   of the BRDF we want R=ao, G=Roughness, B=Metalness. AO uses a really hacky node specific to GLTF
    #   (see 23:40 here: https://www.youtube.com/watch?v=cJ66-WWY37I)
    # Emissive seems ok as well
    if pbr_image_node:
        separate_rgb_image_node = nodes.new('ShaderNodeSeparateRGB')
        links.new(pbr_image_node.outputs['Color'], separate_rgb_image_node.inputs['Image'])
        links.new(separate_rgb_image_node.outputs['G'], bsdf_node.inputs['Roughness'])
        links.new(separate_rgb_image_node.outputs['B'], bsdf_node.inputs['Metallic'])
        
        