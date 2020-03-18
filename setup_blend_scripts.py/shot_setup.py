import bpy

# variables
filepath = #filepath
scene_name = #scene_name
frame_start = #frame_start
frame_end = #frame_end
framerate = #framerate
resolution_x = #resolution_x
resolution_y = #resolution_y

# set scene
scn = bpy.context.scene
scn.name = scene_name
scn.frame_start = frame_start
scn.frame_end = frame_end
scn.render.fps = framerate
scn.render.resolution_x = resolution_x
scn.render.resolution_y = resolution_y

# save file
bpy.ops.wm.save_as_mainfile(filepath=filepath)

# quit
#bpy.ops.wm.quit_blender()