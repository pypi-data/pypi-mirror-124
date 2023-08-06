

import sys
sys.path.append('../')
from linux.shared_scripts.modules import filechecker, folderchecker, sizechecker
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def taskchecker():
    filechecker("/tmp/services")
    filechecker("/tmp/passwd")
    filechecker("/tmp/.secret")
    folderchecker("/tmp/Photos")
    folderchecker("/tmp/Photos/Hawaii")
    folderchecker("/tmp/Photos/Florida")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


