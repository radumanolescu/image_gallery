# -*- coding: utf-8 -*-
"""
Created on Tue Nov 09 06:12:28 2021
In the metadata files, the "Invent. Number" should be a number in range(300),
while the "Invent. IMG-" should be the numeric part of the image file name.
In some metadata files, the "Invent. Number" is swapped with the "Invent. IMG-".
Un-swap those fields.

@author: Radu
"""

import os
import shutil

rootdir = r'C:\Users\Radu\-\projects\Python\image_gallery\static\images'
INV_NUM_KEY = "Invent. Number:"
INV_IMG_KEY = "Invent. IMG-:"


def is_int(s: str) -> bool:
    try:
        some_int = int(s)
        return True
    except ValueError:
        return False


def is_inv_num(s: str) -> bool:
    if is_int(s):
        inv_num = int(s)
        if inv_num < 1000:
            return True
        else:
            return False
    else:
        return False


for root, subFolders, files in os.walk(rootdir):
    for file in files:
        if file.endswith(".txt"):
            src_path = os.path.join(root, file)
            metadata = {}
            inv_img_int = int(file.replace("IMG_", "").replace(".txt", ""))
            with open(src_path, 'r') as src:
                for line in src:
                    words = line.split("\t")
                    words = [w.strip() for w in words]
                    metadata[words[0]] = words[1] if len(words) > 1 else ""
            inv_num = metadata[INV_NUM_KEY]
            correct_inv_num = ""
            if is_inv_num(metadata[INV_NUM_KEY]):
                correct_inv_num = metadata[INV_NUM_KEY]
            if is_inv_num(metadata[INV_IMG_KEY]):
                correct_inv_num = metadata[INV_IMG_KEY]
            correct_inv_img = str(inv_img_int)
            metadata[INV_NUM_KEY] = correct_inv_num
            metadata[INV_IMG_KEY] = correct_inv_img
            print("correct_inv_num:", correct_inv_num, "\tcorrect_inv_img:", correct_inv_img)
            # Write the correct data back out
            dst = open(src_path, "w")
            for key in metadata:
                line = key + "\t" + metadata[key] + "\n"
                dst.write(line)
            dst.close()
