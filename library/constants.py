import os

"""
THIS FILE CONTAINS THE SETUP VARIABLES FOR THE LIBRARIES MODULE
for constants to the study-case go to the repo root folder file named "study-case-constants.py" 
"""

# as a workaround to avoid circular import, we redefined the functions, sadly...

def joinToHome(input_path):
    """
    join a relative path to the home path
    """
    return os.path.join(os.environ['HOME'],input_path.strip('/'))

def create_dir_ifnot_exists(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def createDirs(dirList):
    for dirPath in dirList:
        create_dir_ifnot_exists(dirPath)


# the output folder, mostly for temporary files
default_output_folder = joinToHome('data/sanit3d_out')
temp_files_outdir = os.path.join(default_output_folder,'temporary')


createDirs([default_output_folder,temp_files_outdir])

