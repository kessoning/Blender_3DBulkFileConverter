bl_info = {
    "name": "3D Batch File Converter",
    "description": "Bulk converts 3D files between different formats.",
    "author": "Giovanni Muzio",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D > Tools",
    "category": "Import-Export",
}

import bpy
import os

# Panel class defines the UI elements in the Blender interface
class ConvertFilesPanel(bpy.types.Panel):
    """Panel for converting 3D files in Blender's UI."""
    bl_label = "Convert 3D Files"
    bl_idname = "OBJECT_PT_convert_3d_files"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    # Draw method defines how to draw the panel
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Layout to choose source and target folders, and conversion format
        layout.prop(scene, "source_folder")
        layout.prop(scene, "target_folder")
        layout.prop(scene, "target_format")

        # Show compression option for GLTF and GLB formats
        if scene.target_format in {'GLTF', 'GLB'}:
            layout.prop(scene, "use_compression")

        # Show separate texture export option for GLTF format
        if scene.target_format == 'GLTF':
            layout.prop(scene, "export_separate_textures")

        # General options for merging, overwriting, and subfolder inclusion
        layout.prop(scene, "merge_objects")
        layout.prop(scene, "overwrite_files")
        layout.prop(scene, "include_subfolders")
        layout.prop(scene, "export_to_subfolders")

        # Button to execute the conversion
        layout.operator("object.convert_3d_files")

# Operator class to handle the conversion operation
class ConvertFilesOperator(bpy.types.Operator):
    bl_idname = "object.convert_3d_files"
    bl_label = "Convert 3D Files"

    # Execute method is called when the operator is run
    def execute(self, context):
        sc = context.scene
        convert_files(sc.source_folder, sc.target_folder, sc.target_format, sc.merge_objects, sc.overwrite_files, sc.use_compression, sc.export_separate_textures, sc.include_subfolders, sc.export_to_subfolders)
        return {'FINISHED'}

# Main function to convert files
def convert_files(source_folder, target_folder, target_format, merge_objects, overwrite_files, use_compression, export_separate_textures, include_subfolders, export_to_subfolders):
    # Supported import formats and corresponding Blender operators
    supported_formats = {
        ".gltf": "import_scene.gltf",
        ".glb": "import_scene.gltf",
        ".obj": "import_scene.obj",
        ".stl": "import_mesh.stl",
        ".fbx": "import_scene.fbx",
    }

    # Determine the target file extension based on selected format
    target_ext = ".fbx" if target_format == "FBX" else ".obj"
    if target_format in {'GLTF', 'GLB'}:
        target_ext = ".gltf" if target_format == "GLTF" else ".glb"

    # Walk through the source folder (including subfolders if selected)
    for root, dirs, files in os.walk(source_folder):
        if not include_subfolders:
            dirs[:] = []  # Skip subdirectories if not selected
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in supported_formats:
                source_file = os.path.join(root, file)
                file_name = os.path.splitext(file)[0]

                # Create a subfolder for the file if the option is enabled
                if export_to_subfolders:
                    file_target_folder = os.path.join(target_folder, file_name)
                    os.makedirs(file_target_folder, exist_ok=True)
                else:
                    file_target_folder = target_folder

                target_file = os.path.join(file_target_folder, file_name + target_ext)

                # Skip existing files if overwrite is not enabled
                if not overwrite_files and os.path.exists(target_file):
                    continue  # Skip existing files if overwrite is not enabled

                bpy.ops.wm.read_homefile(use_empty=True)

                # Import the file based on its extension
                if file_ext in ['.gltf', '.glb']:
                    bpy.ops.import_scene.gltf(filepath=source_file)
                elif file_ext == '.obj':
                    bpy.ops.import_scene.obj(filepath=source_file)
                elif file_ext == '.stl':
                    bpy.ops.import_mesh.stl(filepath=source_file)
                elif file_ext == '.fbx':
                    bpy.ops.import_scene.fbx(filepath=source_file)

                # Export logic based on the selected target format
                if target_format == "FBX":
                    bpy.ops.export_scene.fbx(filepath=target_file, use_selection=False)
                elif target_format == "OBJ":
                    bpy.ops.export_scene.obj(filepath=target_file, use_selection=False)
                elif target_format in ["GLTF", "GLB"]:
                    # Ensure the context is correct for GLTF/GLB export
                    for window in bpy.context.window_manager.windows:
                        screen = window.screen
                        for area in screen.areas:
                            if area.type == 'VIEW_3D':
                                override = {'window': window, 'screen': screen, 'area': area}
                                if target_format == "GLTF":
                                    bpy.ops.export_scene.gltf(override, filepath=target_file, export_format='GLTF_SEPARATE' if export_separate_textures else 'GLTF_EMBEDDED', use_selection=False)
                                elif target_format == "GLB":
                                    bpy.ops.export_scene.gltf(override, filepath=target_file, export_format='GLB', use_selection=False)
                                break

# Register function to add the add-on to Blender
def register():
    bpy.types.Scene.source_folder = bpy.props.StringProperty(name="Source Folder", description="Select Source Folder", default="", subtype='DIR_PATH')
    bpy.types.Scene.target_folder = bpy.props.StringProperty(name="Target Folder", description="Select Target Folder", default="", subtype='DIR_PATH')
    bpy.types.Scene.target_format = bpy.props.EnumProperty(name="Target Format", description="Choose a target format", items=[ ('FBX', "FBX", ""), ('OBJ', "OBJ", ""), ('GLTF', "GLTF", ""), ('GLB', "GLB", "")])
    bpy.types.Scene.merge_objects = bpy.props.BoolProperty(name="Merge Objects", description="Merge all objects into a single mesh", default=True)
    bpy.types.Scene.overwrite_files = bpy.props.BoolProperty(name="Overwrite Existing Files", description="Overwrite files in the target folder if they exist", default=False)
    bpy.types.Scene.use_compression = bpy.props.BoolProperty(name="Use Compression", description="Compress the output file (only for GLTF/GLB)", default=False)
    bpy.types.Scene.export_separate_textures = bpy.props.BoolProperty(name="Export Separate Textures", description="Export textures separately (only for GLTF)", default=False)
    bpy.types.Scene.include_subfolders = bpy.props.BoolProperty(name="Include Subfolders", description="Process files in subfolders of the source folder", default=False)
    bpy.types.Scene.export_to_subfolders = bpy.props.BoolProperty(name="Export to Individual Subfolders", description="Export each file to its own subfolder", default=False)
    
    bpy.utils.register_class(ConvertFilesPanel)
    bpy.utils.register_class(ConvertFilesOperator)

# Unregister function to remove the add-on from Blender
def unregister():
    del bpy.types.Scene.source_folder
    del bpy.types.Scene.target_folder
    del bpy.types.Scene.target_format
    del bpy.types.Scene.merge_objects
    del bpy.types.Scene.overwrite_files
    del bpy.types.Scene.use_compression
    del bpy.types.Scene.export_separate_textures
    del bpy.types.Scene.include_subfolders
    del bpy.types.Scene.export_to_subfolders
    
    bpy.utils.unregister_class(ConvertFilesPanel)
    bpy.utils.unregister_class(ConvertFilesOperator)

# Standard boilerplate to allow running this script directly
if __name__ == "__main__":
    register()
