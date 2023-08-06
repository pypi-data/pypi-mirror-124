import sys
sys.path.append('../')
from shared_scripts.modules import filechecker, folderchecker, sizechecker

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def taskchecker():
    filechecker("/tmp/fruits")
    sizechecker("/tmp/services")
    linechecker("/tmp/top10")
    linechecker("/tmp/bottom10")
    sizechecker("/tmp/sorted_fruits")
    filechecker("/tmp/sorted_fruits")

    sizechecker("/tmp/counted_services")
    filechecker("/tmp/counted_services")
    linetotalchecker("/tmp/counted_services", '1300')
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 
