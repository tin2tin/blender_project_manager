import bpy
import os


class BPMImportAsset(bpy.types.Operator):
    """Import asset in shot"""
    bl_idname = "bpm.import_asset"
    bl_label = "Import asset"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'SHOT'

    def execute(self, context):
        from ..functions.file_functions import linkAssetLibrary
        from ..global_variables import (
                                    importing_asset_statement,
                                    asset_not_existing_message,
                                    asset_not_existing_statement,
                                    asset_file_not_found_message,
                                    asset_file_not_found_statement,
                                    asset_imported_statement,
                                    asset_folder,
                                )

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        debug = general_settings.debug
        asset_name = general_settings.asset_choose
        asset_list = winman.bpm_assets
        asset = None

        asset_folder = os.path.join(general_settings.project_folder, asset_folder)

        if debug: print(importing_asset_statement + asset_name) #debug

        try:
            asset = asset_list[asset_name]
        except KeyError:
            self.report({'INFO'}, asset_not_existing_message + asset_name)
            if debug: print(asset_not_existing_statement + asset_name) #debug
            return {'FINISHED'}

        chosen_asset_folder = os.path.join(asset_folder, asset.name)
        chosen_asset_file = os.path.join(chosen_asset_folder, asset.name + ".blend")

        if not os.path.isfile(chosen_asset_file):
            self.report({'INFO'}, asset_file_not_found_message + chosen_asset_file)
            if debug: print(asset_file_not_found_statement + chosen_asset_file) #debug
            return {'FINISHED'}           
        
        # link asset
        linkAssetLibrary(chosen_asset_file, asset.asset_type)

        if debug: print(asset_imported_statement) #debug
        
        return {'FINISHED'}