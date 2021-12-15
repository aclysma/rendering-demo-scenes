# bistro

Please download the zip fron https://developer.nvidia.com/orca/amazon-lumberyard-bistro
and extract in this directory.

You should have a directory structure like this:

```
rendering-demo-scenes
 - bistro
   - bistro.md (this file)
   - Bistro_v5_2
     - Textures
       - Antenna_Metal_BaseColor.dds
       - ...
     - BistroExterior.fbx
     - BistroExterior.pyscene
     - ...
```

Now move the *.fbx files and the Textures folder up a level.

```
rendering-demo-scenes
 - bistro
   - bistro.md (this file)
   - Textures
     - Antenna_Metal_BaseColor.dds
     - ...
   - BistroExterior.fbx
   - BistroInterior.fbx
```

This ensures that the resulting .blend file will references ./Textures/*.dds

To produce the .blend file, run `blender -b -P generate-bistro.py`

On macOS, the binary is embedded in the .app file. So run something like `/Applications/Blender.app/Contents/MacOS/Blender -b -P generate-bistro.py`

The script can be adjusted to only import the interior or exterior FBX file

## Source Art License

The original assets were released as Creative Commons CC-BY 4.0.

```
 @misc{ORCAAmazonBistro,
   title = {Amazon Lumberyard Bistro, Open Research Content Archive (ORCA)},
   author = {Amazon Lumberyard},
   year = {2017},
   month = {July},
   note = {\small \texttt{http://developer.nvidia.com/orca/amazon-lumberyard-bistro}},
   url = {http://developer.nvidia.com/orca/amazon-lumberyard-bistro}
}
```
