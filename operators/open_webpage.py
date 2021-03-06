import bpy
import webbrowser


class BPMOpenWikiPage(bpy.types.Operator):
    """Find help on the wiki page"""
    bl_idname = "bpm.open_wiki_page"
    bl_label = "Help"
    bl_options = {'REGISTER'}

    wiki_page : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # import statements and functions
        from ..global_variables import opening_web_page_statement, wiki_url
        
        url = wiki_url + self.wiki_page

        if context.window_manager.bpm_generalsettings.debug: print(opening_web_page_statement + url) #debug
        
        webbrowser.open(url)

        return {'FINISHED'}