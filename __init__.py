import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from .import_vtmb_x import xImport

bl_info = {
    "name": "VTMB Blender tools",
    "blender": (2, 80, 0),
    "category": "Import-Export",
}

def import_vtmb_x(context, file_path):
    parsed_file =xImport(file_path)
    parsed_file.import_mesh()
    return {'FINISHED'}

class ImportVTMBX(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import VTMB .x file"

    # ImportHelper mixin class uses this
    filename_ext = ".x"

    filter_glob: StringProperty(
        default="*.x",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    def execute(self, context):
        return import_vtmb_x(context, self.filepath)


# Only needed if you want to add into a dynamic menu.
def menu_func_import(self, context):
    self.layout.operator(ImportVTMBX.bl_idname, text="Import VTMB .x file")


# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access).
def register():
    bpy.utils.register_class(ImportVTMBX)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportVTMBX)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.import_test.some_data('INVOKE_DEFAULT')
