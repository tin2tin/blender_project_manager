import bpy
import gpu
import blf
import bgl
from gpu_extras.batch import batch_for_shader


#from .functions.utils_functions import redrawAreas
from .global_variables import font_file



# compute dpi_fac on every blender startup
# dpi_fac = bpy.context.preferences.system.pixel_size * bpy.context.preferences.system.dpi / 72

# font id for makers
markers_font = {
    "font_id": 0,
}

# initialize fonts
def initializeFontId():
    print("loading font") #debug TODO add statement
    markers_font["font_id"] = blf.load(font_file)

# get link scene marker fram
def getMarkerFrameFromShotStrip(strip):
    marker_list = []
    frame_start = strip.frame_start
    scn = strip.scene
    for marker in scn.timeline_markers:
        marker_frame = (marker.frame - scn.frame_start) + frame_start
        if marker_frame >= strip.frame_final_start and marker_frame < strip.frame_final_end:
            marker_list.append((marker.name, marker_frame))
    return marker_list

# get marker coordinates
def getMarkerCoordinates(frame, channel, region, dpi_fac):
    m_width = 6
    m_height = 9
    m_pos_y = 0.035
    t_pos_x = 3
    t_pos_y = 7
    x, y =region.view2d.view_to_region(frame, channel + m_pos_y, clip=False)
    v1 = (x - m_width * dpi_fac, y)
    v2 = (x + m_width * dpi_fac, y)
    v3 = (x, y + m_height * dpi_fac)
    v4 = (x + t_pos_x, y + t_pos_y)
    return ((v1, v2, v3), v4)

# get strip rectangle
def getStripRectangle(strip):
    x_offset = 0.05
    y_offset = 0.05
    x1 = strip.frame_final_start
    x2 = strip.frame_final_end + x_offset
    y1 = strip.channel + y_offset
    y2 = strip.channel + 1 - y_offset
    return [x1, y1, x2, y2]

# get text bounding box
def getBoundingBoxCoordinates(pos, text, text_size, dpi_fac):
    step = text_size / 2 + 1
    width = len(text) * step * dpi_fac
    height = 9
    
    offs_x = 3
    offs_y = 3
    
    v1 = (pos[0] - offs_x, pos[1] - offs_y)
    v2 = (pos[0] + width + offs_x, pos[1] - offs_y)
    v3 = (pos[0] - offs_x, pos[1] + height + offs_y)
    v4 = (pos[0] + width + offs_x, pos[1] + height + offs_y)

    return (v1, v2, v3, v4)

# get warning zone of a strip
def getWarningZoneStrip(x, y):
    square_size = 10
    v1 = (x-square_size, y-square_size)
    v2 = (x, y-square_size)
    v3 = (x-square_size, y)
    v4 = (x, y)
    return (v1,v2,v3,v4)

# check if a strip has to be updated
def getStripNeedUpdate(strip):
    if strip.frame_start != strip.frame_final_start:
        return True
    elif (strip.frame_start + strip.frame_duration) != strip.frame_final_end:
        return True
    else:
        return False

# draw text
def drawText(location, text, f_id):
    blf.position(f_id, location[0], location[1], 0)   
    blf.draw(f_id, text)

# get dpi factor from context
def getDpiFactorFromContext(context):
    pixel_size = context.preferences.system.pixel_size
    dpi = context.preferences.system.dpi
    dpi_fac = pixel_size * dpi / 72
    return dpi_fac
   
# ui draw callback
def drawBpmSequencerCallbackPx():
    context = bpy.context

    scn = context.scene
    m_display = scn.bpm_displaymarkers
    mn_display = scn.bpm_displaymarkernames
    
    if not scn.bpm_extraui: return

    sequencer = scn.sequence_editor
    region = context.region

    # compute dpi_fac on every draw dynamically
    dpi = context.preferences.system.dpi
    dpi_fac = getDpiFactorFromContext(context)

    # setup markers
    vertices_m = ()
    indices_m = ()
    color_m = (1, 1, 1, 1)

    # setup markers text
    #text_size = int(12 * dpi_fac)
    id_m = markers_font["font_id"]
    text_size = 12
    blf.color(id_m, *color_m)
    blf.size(id_m, text_size, dpi)
    marker_texts = []

    # setup markers bounding box
    vertices_m_bb = ()
    indices_m_bb = ()
    color_m_bb = (0, 0, 0, 0.5)

    # setup extras
    # bpm shots
    vertices_e = ()
    indices_e = ()
    color_e = (0, 1, 0, 0.25)
    # warning bpm shots
    vertices_e_w = ()
    indices_e_w = ()
    color_e_w = (1, 0, 0, 1)

    # iterate through strips
    bgl.glEnable(bgl.GL_BLEND) # enable transparency

    n_e = 0
    n_e_w = 0
    n_m = 0
    n_m_bb = 0

    ### COMPUTE TIMELINE ###
    for strip in sequencer.sequences_all:

        if strip.type in {'SCENE'}:

            if strip.bpm_isshot:

                # bpm shot
                x1, y1, x2, y2 = getStripRectangle(strip)
                y1 += 0.5

                v1 = region.view2d.view_to_region(x1, y1, clip=False)
                v2 = region.view2d.view_to_region(x2, y1, clip=False)
                v3 = region.view2d.view_to_region(x1, y2, clip=False)
                v4 = region.view2d.view_to_region(x2, y2, clip=False)

                vertices_e += (v1, v2, v3, v4)
                indices_e += ((n_e, n_e + 1, n_e + 2), (n_e + 2, n_e + 1, n_e + 3))
                n_e += 4

                # bpm need to update
                if getStripNeedUpdate(strip):
                    vertices_e_w += getWarningZoneStrip(*v4)
                    indices_e_w += ((n_e_w, n_e_w + 1, n_e_w + 2), (n_e_w + 2, n_e_w + 1, n_e_w + 3))
                    n_e_w += 4

                if strip.scene:

                    # markers
                    if m_display != 'NONE' :
                        if (m_display == 'SELECTED' and strip.select) \
                        or (m_display == 'PERSTRIP' and strip.bpm_displaymarkers) \
                        or (m_display == 'ALL'):
                            for m in getMarkerFrameFromShotStrip(strip):
                                coord = getMarkerCoordinates(m[1], strip.channel, region, dpi_fac)
                                vertices_m += coord[0]
                                indices_m += ((n_m, n_m + 1, n_m + 2),)
                                n_m += 3   

                                # markers text
                                if (mn_display == "ALL") \
                                or (mn_display == "CURRENT" and scn.frame_current == m[1]):
                                    text = m[0]
                                    if len(text) > scn.bpm_displaymarkerlimit:
                                        text = text[0:scn.bpm_displaymarkerlimit - 3] + "..."
                                    marker_texts.append((coord[1], text))

                                    # marker box
                                    if scn.bpm_displaymarkerboxes:
                                        vertices_m_bb += getBoundingBoxCoordinates(coord[1], text, text_size, dpi_fac)
                                        indices_m_bb += ((n_m_bb, n_m_bb + 1, n_m_bb + 2), (n_m_bb + 2, n_m_bb + 1, n_m_bb + 3))
                                        n_m_bb += 4
    
    ### DRAW SHADERS ###

    bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE)
    
    #extras
    BPM_extra_shaders = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    BMP_extra_batch = batch_for_shader(BPM_extra_shaders, 'TRIS', {"pos": vertices_e}, indices=indices_e)
    BPM_extra_shaders.bind()
    BPM_extra_shaders.uniform_float("color", color_e)
    BMP_extra_batch.draw(BPM_extra_shaders,)

    bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)

    #warning zones
    BPM_extra__warning_shaders = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    BMP_extra_warning_batch = batch_for_shader(BPM_extra__warning_shaders, 'TRIS', {"pos": vertices_e_w}, indices=indices_e_w)
    BPM_extra__warning_shaders.bind()
    BPM_extra__warning_shaders.uniform_float("color", color_e_w)
    BMP_extra_warning_batch.draw(BPM_extra__warning_shaders,)

    # markers bounding boxes
    BPM_marker_bb_shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    BMP_marker_bb_batch = batch_for_shader(BPM_marker_bb_shader, 'TRIS', {"pos": vertices_m_bb}, indices=indices_m_bb)
    BPM_marker_bb_shader.bind()
    BPM_marker_bb_shader.uniform_float("color", color_m_bb)
    BMP_marker_bb_batch.draw(BPM_marker_bb_shader,)

    # markers
    BPM_marker_shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    BMP_marker_batch = batch_for_shader(BPM_marker_shader, 'TRIS', {"pos": vertices_m}, indices=indices_m)
    BPM_marker_shader.bind()
    BPM_marker_shader.uniform_float("color", color_m)
    BMP_marker_batch.draw(BPM_marker_shader,)

    # draw marker texts
    for t in marker_texts:
        drawText(t[0], t[1], id_m)

    bgl.glDisable(bgl.GL_BLEND)

#enable callback
cb_handle = []
def enableSequencerCallback():
    if cb_handle:
        return
    
    initializeFontId()

    cb_handle.append(bpy.types.SpaceSequenceEditor.draw_handler_add(
        drawBpmSequencerCallbackPx, (), 'WINDOW', 'POST_PIXEL'))

    print('add') #debug TODO statement system

#disable callback
def disableSequencerCallback():
    if not cb_handle:
        return
    bpy.types.SpaceSequenceEditor.draw_handler_remove(cb_handle[0], 'WINDOW')
    cb_handle.clear()

    print('remove') #debug TODO statement system