import bpy
import os

filename = "output"

# Clear existing scene objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Create a grid of cubes
grid_size = 10
cube_size = 1

for i in range(grid_size):
    for j in range(grid_size):
        print(i, ", ", j)
        bpy.ops.mesh.primitive_cube_add(
            size=cube_size, location=(i * cube_size, j * cube_size, 0))
print("all cubes initialized")

# Set up camera
camera = bpy.data.objects['Camera']
camera.location = ((grid_size - 1) * cube_size / 2,
                   (grid_size - 1) * cube_size / 2, grid_size * cube_size * 2.5)
camera.rotation_euler = (0, 0, 0)
print("camera initialized")


# Set up rendering settings
scene = bpy.context.scene
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = filename + '.png'

# Render the scene
print("start rendering")
bpy.ops.render.render(write_still=True)
print("rendering done")

# Save the scene to a Blender file
print("save to blenderfile")
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(filename + '.blend'))
