

import sys
sys.path.append('../')
from linux.shared_scripts import filechecker, folderchecker, sizechecker
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def taskchecker():
    filechecker("/tmp/services")
    filechecker("/tmp/passwd")
    filechecker("/tmp/.secret")
    folderchecker("/tmp/Photos")
    folderchecker("/tmp/Photos/Hawaii")
    folderchecker("/tmp/Photos/Florida")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


