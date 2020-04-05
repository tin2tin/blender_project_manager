import bpy
import os


from ..global_variables import (
                            saving_to_json_statement,
                            saved_to_json_statement,
                            shot_file,
                            bypass_shot_settings_update_statement,
                        )
from .json_functions import create_json_file, createJsonDatasetFromProperties


#update function for filebrowser custom path
def updateShotSettingsProperties(self, context):
    winman = context.window_manager
    debug = winman.bpm_generalsettings.debug

    if winman.bpm_generalsettings.bypass_update_tag:
        if debug: print(bypass_shot_settings_update_statement) #debug
        return

    # create the json file
    if debug: print(saving_to_json_statement) #debug
    shot_json = os.path.join(self.shot_folder, shot_file)

    # format the json dataset
    json_dataset = createJsonDatasetFromProperties(self)
    # create json file
    create_json_file(json_dataset, shot_json)

    if debug: print(saved_to_json_statement) #debug