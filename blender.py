import bpy
import os
import csv
import math

input_filename = "input_data_10.csv"
output_filename = "output"

input_data = []
grid_size_i = 0
grid_size_j = 0
grid_size_max = 0
cube_size = 1
cube_spacing = cube_size/10
materials = [
    {
        "name": "redMaterial",
        "color_value": (1, 0, 0, 1),
        "blender_material": None
    },
    {
        "name": "blackMaterial",
        "color_value": (.1, .1, .1, 1),
        "blender_material": None
    },
]

# Clear existing scene objects


def clearExistingBlenderScene():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()


def readInCSVFile():
    global grid_size_i
    global grid_size_j
    global grid_size_max
    with open(input_filename, 'r') as file:
        reader = csv.reader(file)
        # next(reader, None)
        for item in reader:
            input_data.append(item)
            print(item)

    print(input_data)
    grid_size_i = len(input_data)
    grid_size_j = len(input_data[0])
    if grid_size_i > grid_size_j:
        grid_size_max = grid_size_i
    else:
        grid_size_max = grid_size_j


def createMaterials():
    for mat in materials:
        print(mat["name"])
        material = bpy.data.materials.new(name=mat["name"])
        material.use_nodes = True

        # Set Principled BSDF node color to red
        nodes = material.node_tree.nodes
        principled_bsdf = nodes.get("Principled BSDF")
        if principled_bsdf:
            principled_bsdf.inputs["Base Color"].default_value = mat["color_value"]
        mat["blender_material"] = material

    print("all materials created", materials)


def createGrid():
    global grid_size_i
    global grid_size_j
    for i, row in enumerate(input_data):
        print(row)
        for j, element in enumerate(row):
            print(i, j)
            bpy.ops.mesh.primitive_cube_add(
                size=cube_size, location=(i * (cube_size + cube_spacing), j * (cube_size + cube_spacing), 0))
            match element:
                case "r":
                    bpy.context.object.data.materials.append(
                        materials[0]["blender_material"])
                case _:
                    bpy.context.object.data.materials.append(
                        materials[1]["blender_material"])

    print("all cubes initialized")


def setupCamera():
    global grid_size_i
    global grid_size_j
    global grid_size_max
    # Set up camera
    camera = bpy.data.objects['Camera']
    camera.location = ((grid_size_i - 1) * (cube_size + cube_spacing) / 2,
                       (grid_size_j - 1) * (cube_size + cube_spacing) / 2, grid_size_max * (cube_size + cube_spacing) * 2.7)
    camera.rotation_euler = (0, 0, math.radians(90))
    print("camera initialized")


def renderScene():
    # Set up rendering settings
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = output_filename + '.png'

    # Render the scene
    print("start rendering")
    bpy.ops.render.render(write_still=True)
    print("rendering done")


def saveBlenderFile():
    # Save the scene to a Blender file
    print("save to blenderfile")
    bpy.ops.wm.save_as_mainfile(
        filepath=os.path.abspath(output_filename + '.blend'))


def main():
    clearExistingBlenderScene()
    readInCSVFile()
    createMaterials()
    createGrid()
    setupCamera()
    renderScene()
    saveBlenderFile()


if __name__ == "__main__":
    main()
