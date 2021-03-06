import bpy, os


# display project settings
class BpmSaveProjectSettingsToJson(bpy.types.Operator):
    """Save Project Settings to json"""
    bl_idname = "bpm.save_project_settings_json"
    bl_label = "Save Project Settings"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT'
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.label(text="Save Project Settings to json file ?")
        
    def execute(self, context):
        # import statements and functions
        from ..functions.json_functions import createJsonDatasetFromProperties, create_json_file
        from ..global_variables import file_project, saving_to_json_statement, saved_to_json_statement

        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings
        datas = winman.bpm_projectdatas

        if general_settings.debug: print(saving_to_json_statement)

        project_file = os.path.join(general_settings.project_folder, file_project)

        # format the json dataset
        json_dataset = createJsonDatasetFromProperties(datas, ())

        # create json file
        create_json_file(json_dataset, project_file)

        if general_settings.debug: print(saved_to_json_statement)

        return {'FINISHED'}