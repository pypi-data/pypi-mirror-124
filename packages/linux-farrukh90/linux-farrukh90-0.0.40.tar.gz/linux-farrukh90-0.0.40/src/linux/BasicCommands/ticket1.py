

import sys
sys.path.append('../')
from linux.shared_scripts.modules import filechecker, folderchecker, sizechecker
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def taskchecker():
    folderchecker("/tmp/test")
    filechecker("/tmp/services")
    sizechecker("/tmp/services")
    filechecker("/tmp/passwd")
    sizechecker("/tmp/passwd")
    filechecker("/tmp/.secret")
    folderchecker("/tmp/Photos")
    folderchecker("/tmp/Photos/Hawaii")
    folderchecker("/tmp/Photos/Florida")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


