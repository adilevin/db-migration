import sys
import os
import shutil

folder_name = sys.argv[1]
try:
    os.makedirs(folder_name)
    os.makedirs(os.path.join(folder_name,'sqlite_files'))
except:
    pass
for subfolder in ['main','model','data_access_objects','test','web-clients']:
    shutil.copytree(subfolder,os.path.join(folder_name,subfolder))