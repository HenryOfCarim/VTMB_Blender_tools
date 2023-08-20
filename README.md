# VTMB_Blender_tools
I was interested in Vampire: The Masquerade – Bloodlines character modding tools and the first thing I noticed was how old they are
I simply can't work with 2.4 Blender so this project is intended to update them to modern 2.80+ API

As I understood, because of the unknown strip algorithm adding new skinned meshes is impossible
The current workflow is based on converting .mdl to directX .x files and then patching the existing .mdl with your edited file

For converting VTMB .mdl files you need Vamped 0.92 or  PackFile Explorer 3.09 they convert .mdl files to .x
The addon allows importing these .x files and exporting them as .mdl(creates a new patched file with _x.mdl)

![import_export](https://github.com/HenryOfCarim/VTMB_Blender_tools/assets/18252816/5a4a55cb-c8af-4e4c-97d4-7197150a69a8)

I don't  know who was the original creator of these blender scripts but in files were mentioned

- DDLullu (author of scripts)
- Arben OMARI (author of directX mesh file converter)






