'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou (tonton)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {  
 "name": "Project Manager",  
 "author": "Samy Tichadou (tonton)",  
 "version": (0, 1),  
 "blender": (2, 83, 0),  
 "location": "Timeline",  
 "description": "Manage small animation project from Blender",  
  "wiki_url": "https://github.com/samytichadou/blender_project_manager",  
 "tracker_url": "https://github.com/samytichadou/blender_project_manager/issues/new",  
 "category": "Animation"}


import bpy


# IMPORT SPECIFICS
##################################

from .startup_handler import bpmStartupHandler
from .functions.filebrowser_update_function import updateFilebrowserPath

from .operators.open_shot import *
from .operators.back_to_edit import *
from .operators.create_shot import *
from .operators.create_project import *
from .operators.update_shot_duration import *

from .operators.display_modify_project_settings import *
from .operators.save_project_settings_to_json import *

from .properties import *
from .gui import *

from .operators.dummy_markers import * #debug

# register
##################################

classes = (BPMOpenShot,
            BPMBackToEdit,
            BPMCreateShot,
            BpmCreateProject,
            BPMUpdateShotDuration,
            BpmDisplayModifyProjectSettings,
            BpmSaveProjectSettingsToJson,
            BpmDummy, #debug

            ProjectSettings,
            CustomFolders,

            BPM_MT_sequencer_menu,
            BPM_MT_topbar_menu,
            BPM_UL_Folders_Uilist,
            BPM_PT_FileBrowser_Panel,
            )

def register():

    ### OPERATORS ###
    from bpy.utils import register_class
    for cls in classes :
        register_class(cls)

    ### PROPERTIES ###
    bpy.types.WindowManager.bpm_isproject = \
        bpy.props.BoolProperty(default=False)
    bpy.types.WindowManager.bpm_isedit = \
        bpy.props.BoolProperty(default=False)
    bpy.types.WindowManager.bpm_debug = \
        bpy.props.BoolProperty(default=True)
    bpy.types.WindowManager.bpm_foldersindex = \
        bpy.props.IntProperty(update = updateFilebrowserPath)
    bpy.types.WindowManager.bpm_datas = \
        bpy.props.CollectionProperty(type = ProjectSettings)
    bpy.types.WindowManager.bpm_folders = \
        bpy.props.CollectionProperty(type = CustomFolders)

    bpy.types.SceneSequence.bpm_isshot = \
        bpy.props.BoolProperty(default=False)

    bpy.types.Scene.bpm_displaymarkers = \
        bpy.props.BoolProperty(name = "Display shot markers", default = False)

    ### HANDLER ###
    bpy.app.handlers.load_post.append(bpmStartupHandler)

    ### SPECIAL GUI ###
    bpy.types.TOPBAR_HT_upper_bar.prepend(bpmTopbarFunction)
    bpy.types.SEQUENCER_MT_editor_menus.append(bpmSequencerMenuFunction)
    bpy.types.TOPBAR_MT_app.append(createProjectAppMenuFunction)

def unregister():
    
    ### OPERATORS ###
    from bpy.utils import unregister_class
    for cls in reversed(classes) :
        unregister_class(cls)

    ### PROPERTIES ###
    del bpy.types.WindowManager.bpm_isproject
    del bpy.types.WindowManager.bpm_isedit
    del bpy.types.WindowManager.bpm_debug
    del bpy.types.WindowManager.bpm_foldersindex
    del bpy.types.WindowManager.bpm_datas
    del bpy.types.WindowManager.bpm_folders

    del bpy.types.SceneSequence.bpm_isshot

    del bpy.types.Scene.bpm_displaymarkers

    ### HANDLER ###
    bpy.app.handlers.load_post.remove(bpmStartupHandler)

    ### SPECIAL GUI ###
    bpy.types.SEQUENCER_MT_editor_menus.remove(bpmSequencerMenuFunction)
    bpy.types.SEQUENCER_MT_editor_menus.remove(bpmSequencerMenuFunction)
    bpy.types.TOPBAR_MT_app.remove(createProjectAppMenuFunction)