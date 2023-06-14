import bpy
import os
import csv
import math


dir = "input_data/"
dimension = "3D/"
project = "House/"
output_filename = "output"

input_data = []
grid_size_y = 0
grid_size_x = 0
grid_size_max = 0
cube_size = 1
cube_spacing = 0  # cube_size/10
materials = {
    "blackMaterial": {
        "name": "blackMaterial",
        "color_value": (.1, .1, .1, 1),
        "blender_material": None
    },
    "redMaterial": {
        "name": "redMaterial",
        "color_value": (1, 0, 0, 1),
        "blender_material": None
    },
    "whiteMaterial": {
        "name": "whiteMaterial",
        "color_value": (.9, .9, .9, 1),
        "blender_material": None
    },
    "brownMaterial": {
        "name": "brownMaterial",
        "color_value": (.65, .21, .042, 1),
        "blender_material": None
    }}


def clearExistingBlenderScene():
    # Clear existing scene objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()


def readInCSVFiles():
    folder_path = dir+dimension+project
    file_list = os.listdir(folder_path)
    sorted_files = sorted(file_list)

    for file_name in sorted_files:
        csv_data = []
        with open(os.path.join(folder_path, file_name), 'r') as file:
            reader = csv.reader(file)
            # next(reader, None)
            for item in reader:
                csv_data.append(item)
        input_data.append(csv_data)

    checkFileDimensions()


def checkFileDimensions():
    global grid_size_y
    global grid_size_x
    global grid_size_max
    grid_size_y = len(input_data[0])
    grid_size_x = len(input_data[0][0])
    if grid_size_y > grid_size_x:
        grid_size_max = grid_size_y
    else:
        grid_size_max = grid_size_x

    # check for consistency
    for z_index, z in enumerate(input_data):
        if not len(z) == grid_size_y:
            print("invalid dimensions (z)")
        for y_index, y in enumerate(z):
            if not len(y) == grid_size_x:
                print("invalid dimensions (y)")


def createMaterials():
    for key in materials:
        print(key)
        material = bpy.data.materials.new(name=materials[key]["name"])
        material.use_nodes = True

        # Set Principled BSDF node color to red
        nodes = material.node_tree.nodes
        principled_bsdf = nodes.get("Principled BSDF")
        if principled_bsdf:
            principled_bsdf.inputs["Base Color"].default_value = materials[key]["color_value"]
        materials[key]["blender_material"] = material

    print("all materials created", materials)


def createGrid():
    global grid_size_y
    global grid_size_x
    for z_index, z in enumerate(input_data):
        print("create z-grid", z_index)
        for y_index, y in enumerate(z):
            for x_index, x in enumerate(y):
                if not x == "0":
                    # print(y_index, x_index)
                    bpy.ops.mesh.primitive_cube_add(
                        size=cube_size, location=(y_index * (cube_size + cube_spacing), x_index * (cube_size + cube_spacing), z_index * (cube_size + cube_spacing)))
                    match x:
                        case "r":
                            bpy.context.object.data.materials.append(
                                materials["redMaterial"]["blender_material"])
                        case "w":
                            bpy.context.object.data.materials.append(
                                materials["whiteMaterial"]["blender_material"])
                        case "b":
                            bpy.context.object.data.materials.append(
                                materials["brownMaterial"]["blender_material"])
                        case _:
                            bpy.context.object.data.materials.append(
                                materials["blackMaterial"]["blender_material"])

    print("all cubes initialized")


def setupCamera():
    global grid_size_y
    global grid_size_x
    global grid_size_max
    # Set up camera
    camera = bpy.data.objects['Camera']
    # camera.location = ((grid_size_y - 1) * (cube_size + cube_spacing) / 2,
    #                    (grid_size_x - 1) * (cube_size + cube_spacing) / 2, grid_size_max * (cube_size + cube_spacing) * 2.7)
    # camera.rotation_euler = (0, 0, math.radians(90))
    camera.location = (45, 27, 24)
    camera.rotation_euler = (math.radians(67), 0, math.radians(122))
    print("camera initialized")


def setupLight():
    # Disable world color
    world = bpy.context.scene.world
    world.use_nodes = True
    bg_node = world.node_tree.nodes["Background"]
    bg_node.inputs["Strength"].default_value = 0  # Set strength to 0

    # Add a sun light
    bpy.ops.object.light_add(
        type='SUN', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    bpy.context.object.data.angle = 1.6

    # Add light inside
    bpy.ops.object.light_add(type='POINT', radius=1,
                             align='WORLD', location=(5, 5, 3), scale=(1, 1, 1))
    bpy.context.object.data.energy = 1000

    # Add spotlight
    bpy.ops.object.light_add(type='SPOT', align='WORLD',
                             location=(30, 15, 10), scale=(1, 1, 1))
    bpy.context.object.rotation_euler = [0, math.radians(80), math.radians(20)]
    bpy.context.object.data.energy = 5000


def renderScene():
    # Set up rendering settings
    # bpy.data.scenes['Scene'].render.engine = 'CYCLES'
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
    readInCSVFiles()
    createMaterials()
    createGrid()
    setupCamera()
    setupLight()
    renderScene()
    saveBlenderFile()


if __name__ == "__main__":
    main()
