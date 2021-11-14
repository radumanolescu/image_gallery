# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 21:48:54 2021

Create a thumbnail for each image

Install PIL (actually: pillow) in Anaconda
https://stackoverflow.com/questions/46717354/how-to-install-pil-on-spyderanaconda-3

@author: Radu
"""

import os
#import shutil
from PIL import Image 

rootdir = r'C:\SharedByRadu\Art\thumbnails'
MAX_SIZE = (100, 100) 

for root, subFolders, files in os.walk(rootdir):
    for file in files:
        if file.endswith(".JPG"):
            src_path = os.path.join(root,file)
            print(src_path)
            image = Image.open(src_path)
            image.thumbnail(MAX_SIZE) 
            image.save(src_path)



