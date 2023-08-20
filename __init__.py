import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from .import_vtmb_x import xImport
from .export_vtmb_mdl import xExport
bl_info = {
    "name": "VTMB Blender tools",
    "blender": (2, 80, 0),
    "category": "Import-Export",
}

def import_vtmb_x(context, file_path):
    parsed_file =xImport(file_path)
    parsed_file.import_mesh()
    return {'FINISHED'}

def export_vtmb_mdl(context, file_path, options):
    exported_file = xExport(file_path)
    exported_file.export_mdl()
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
    

class ExportVTMBX(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export VTMB .mdl file"

    # ExportHelper mixin class uses this
    filename_ext = ".mdl"

    filter_glob: StringProperty(
        default="*.mdl",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Export options",
        description="Choose between two items",
        items=(
            ('OPT_A', "Export all", "Export all"),
            ('OPT_B', "Export UV", "Export UV"),
            ('OPT_C', "Export normals", "Export normals"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        return export_vtmb_mdl(context, self.filepath, self.use_setting)


# Only needed if you want to add into a dynamic menu.
def menu_func_import(self, context):
    self.layout.operator(ImportVTMBX.bl_idname, text="Import VTMB .x file")

def menu_func_export(self, context):
    self.layout.operator(ExportVTMBX.bl_idname, text="Export VTMB .mdl file")

# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access).
def register():
    bpy.utils.register_class(ImportVTMBX)
    bpy.utils.register_class(ExportVTMBX)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ImportVTMBX)
    bpy.utils.unregister_class(ExportVTMBX)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
