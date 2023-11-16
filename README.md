# 3D Batch File Converter

## Description
This tool stands out in its ability to effortlessly convert large batches of 3D files between popular formats such as GLTF, GLB, OBJ, and FBX. Equipped with features like compression, separate texture exports, and subfolder processing, this add-on streamlines the workflow, making file conversion a breeze in complex projects.

## Reason for Creation
As a 3D artist constantly juggling various file formats, I often found myself needing to convert numerous files – a task that was both time-consuming and cumbersome with existing tools. This add-on is the result of a personal necessity to simplify and speed up the file conversion process in Blender, making it a valuable tool for anyone in the 3D creation sphere.

## Installation
To install the add-on in Blender:

1. Download the `3d_batch_file_converter.py` script from this repository.
2. Open Blender and go to `Edit > Preferences`.
3. In the Preferences window, navigate to the Add-ons tab.
4. Click on the "Install..." button and select the downloaded `.py` file.
5. Find the add-on in the list and enable it by ticking the checkbox next to its name.

## Usage
After installation, the add-on can be accessed in Blender's 3D Viewport under the Tools panel.

- **Source Folder**: Select the folder containing the 3D files to convert.
- **Target Folder**: Choose the destination folder for the converted files.
- **Target Format**: Select the desired output format (GLTF, GLB, OBJ, or FBX).
- **Use Compression**: Enable this option to compress the output files (applies to GLTF and GLB formats).
- **Export Separate Textures**: Enable this to export textures separately (applicable for GLTF format).
- **Merge Objects**: Merge all objects into a single mesh.
- **Overwrite Existing Files**: If enabled, existing files in the target folder will be overwritten.
- **Include Subfolders**: Process files located in subfolders of the source folder.
- **Export to Individual Subfolders**: Create individual subfolders for each exported file.

To convert files, set the desired options and click the "Convert 3D Files" button.

## Features
- Supports multiple 3D file formats for conversion.
- Options for compression and separate texture export.
- Ability to include subfolders in the conversion process.
- Option to export each file into its own subfolder, useful for organizing files and textures.

## Requirements
- Tested on Blender 3.4.

## Author
Giovanni Muzio

## License
[MIT License](LICENSE.md)
