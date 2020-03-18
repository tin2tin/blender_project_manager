import bpy, os


from ..global_variables import creating_shot_statement, creating_shot_folder_statement, python_temp, shot_setup_file
from ..functions.file_functions import getNextShot, createDirectory, replaceContentInPythonScript, suppressExistingFile
from ..functions.project_data_functions import getShotPattern, getShotReplacementList


class BPMCreateShot(bpy.types.Operator):
    """Create Shot from Timeline"""
    bl_idname = "bpm.create_shot"
    bl_label = "Create Shot"
    #bl_options = {}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_isproject and context.window_manager.bpm_isedit

    def execute(self, context):
        winman = context.window_manager
        
        if winman.bpm_debug: print(creating_shot_statement) #debug
        
        project_datas = winman.bpm_datas[0]
        next_shot_folder, next_shot_file, next_shot_number = getNextShot(project_datas.project_folder, getShotPattern(project_datas), project_datas.shot_digits)

        createDirectory(next_shot_folder)

        if winman.bpm_debug: print(creating_shot_folder_statement + next_shot_folder) #debug

        # modify and copy python script
        replacement_list = getShotReplacementList(project_datas, next_shot_folder, next_shot_file, next_shot_number)
        
        temp_python_script = os.path.join(next_shot_folder, python_temp)

        replaceContentInPythonScript(shot_setup_file, temp_python_script, replacement_list)

        # launch the blend command

        # delete the python temp
        #suppressExistingFile(temp_python_script)

        return {'FINISHED'}