# PBR Test Scene

This creates a scene with a grid of spheres with materials that change metalness/roughness on X/Y axis of the final render.

To produce the .blend file, run `blender -b -P generate.py`

On macOS, the binary is embedded in the .app file. So run something like `/Applications/Blender.app/Contents/MacOS/Blender -b -P generate.py`

This script has some commented out sections that can be adjusted/moved around to tweak things