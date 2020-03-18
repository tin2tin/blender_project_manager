import bpy, os


from ..global_variables import file_project, loading_statement, currently_loading_statement, folders_loading_statement, custom_folders_file, bpm_statement
from .json_functions import read_json
from .dataset_functions import setPropertiesFromJsonDataset


# get project data file
def getProjectDataFile(winman):
    if bpy.data.is_saved:
        # edit file
        parent_folder = os.path.dirname(bpy.data.filepath)
        subparent_folder = os.path.dirname(parent_folder)
        edit_project_data_file = os.path.join(parent_folder, file_project)
        shot_project_data_file = os.path.join(subparent_folder, file_project)
        if os.path.isfile(edit_project_data_file):
            winman.bpm_isproject = True
            winman.bpm_isedit = True
            return edit_project_data_file
        elif os.path.isfile(shot_project_data_file):
            winman.bpm_isproject = True
            winman.bpm_isedit = False
            return shot_project_data_file

# load datas
def createProjectDatas(winman, project_data_file):
    if winman.bpm_debug: print(loading_statement + project_data_file) #debug

    datas = winman.bpm_datas.add()
    dataset = read_json(project_data_file)

    # set datas
    setPropertiesFromJsonDataset(dataset, datas, winman)

# get custom folders file
def getCustomFoldersFile(winman):
    if winman.bpm_isedit:
        parent_folder = os.path.dirname(bpy.data.filepath)
    else:
        parent_folder = os.path.dirname(os.path.dirname(bpy.data.filepath))
    folders_file = os.path.join(parent_folder, custom_folders_file)
    if os.path.isfile(folders_file):
        return folders_file

# load custom folders
def loadCustomFolders(winman, folders_file):
    folders_coll = winman.bpm_folders
    dataset = read_json(folders_file)
    for f in dataset["folders"]:
        folder = folders_coll.add()
        setPropertiesFromJsonDataset(f, folder, winman)

# get shot pattern
def getShotPattern(project_datas):
    prefix = project_datas.project_prefix
    if not project_datas.project_prefix.endswith("_"):
        prefix += "_"
    prefix += project_datas.shot_prefix
    return prefix

# get shot replacement list for python script
def getShotReplacementList(project_datas, next_shot_folder, next_shot_file, next_shot_number):
    replacement_list = []
    replacement_list.append(['|bpm_statement', bpm_statement])
    replacement_list.append(['|filepath', next_shot_file])
    replacement_list.append(['|scene_name', project_datas.shot_prefix + next_shot_number])
    replacement_list.append(['|frame_start', project_datas.shot_start_frame])
    replacement_list.append(['|frame_end', project_datas.shot_start_frame + project_datas.default_shot_length])
    replacement_list.append(['|framerate', project_datas.framerate])
    replacement_list.append(['|resolution_x', project_datas.resolution_x])
    replacement_list.append(['|resolution_y', project_datas.resolution_y])

    return replacement_list