# Rendering Demo Scenes

## How to use this Repo

This repo contains scripts to generate blender files that can be used for testing renderers.

Most of it will use content provided elsewhere. Much of the time it can be imported into blender,
and it may look ok, but often it has problems. The goal of the scripts here is to import the
upstream data and fix it so that the resulting file is similar quality to if it had been
authored in blender in the first place.

For most scripts, they can be passed to blender to produce a scene and save it to a .blend file.
To do this, run `blender -b -P generate.py`. (assuming blender is on your PATH)

On macOS, the binary is embedded in the .app file. So run something like
`/Applications/Blender.app/Contents/MacOS/Blender -b -P generate.py`

There may be instructions in subdirectories that describe specific steps for building that
particular scene.

## Scenes

### pbr-test

This test scene does not use upstream assets. It programmatically generates spheres with varying
metalness and roughness. It is intended to be used to verify basic correctness of simple PBR rendering.

[![PBR Test eevee render](screenshots/pbr-test-eevee-small.png)](screenshots/pbr-test-eevee.png)

## License

### Source Art Assets

Art assets from outside sources are under various licenses indicated above.

### Original material in this rep

All materials original to this repo not covered under other licenses (such as scripts that generate blender files)
are licensed under either of:

* Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
* MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.

### The Data You Generate

The data you generate with these scripts is 100% yours and we make no license claims against it,
but we do appreciate a mention if you feel it appropriate to do so!

## Contribution

Unless you explicitly state otherwise, any contribution intentionally
submitted for inclusion in the work by you, as defined in the Apache-2.0
license, shall be dual licensed as above, without any additional terms or
conditions.

See [LICENSE-APACHE](LICENSE-APACHE) and [LICENSE-MIT](LICENSE-MIT).
