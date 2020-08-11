import os, sys
from src.lib.request_lib import query_google_imgs

###############################
# Export Root Directory
###############################
thisdir = os.path.dirname(os.path.abspath(__file__))
rootdir = os.path.dirname(thisdir)
sys.path.append(rootdir)

###############################
# Test images
###############################

imgsQuery = query_google_imgs(rootdir, {"q":"flower", "searchType":"image", "imgSize":"large"})
print(imgsQuery)
