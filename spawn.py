import sys
import os
import shutil

folder_name = sys.argv[1]
try:
    os.makedirs(folder_name)
except:
    pass
for subfolder in ['main','model','data_access_objects','test','web-clients']:
    shutil.copytree(subfolder,os.path.join(folder_name,subfolder))