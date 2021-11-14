# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 18:31:58 2021

@author: Radu
"""

import os
import txt_db

rootdir = txt_db.rootdir

image_data = {}
images = []
metadata_col_names = txt_db.cols_list()
col_indexes = [str(i) for i in range(len(metadata_col_names)+1)]
df = txt_db.load_metadata()

def read_headings(src_path: str) -> dict:
    """ Reads the image metadata template file and returns the data as a dictionary.
    Adds the "Image file" heading, which is not included in the file.
    :param src_path: full path to the metadata file
    :return: dictionary containing the metadata as key-value pairs
    """
    metadata = {'0': txt_db.image_file_heading}
    with open(src_path, 'r') as src:
        line_id = 0
        for line in src:
            line_id += 1
            metadata[str(line_id)] = line
    return metadata


def metadata_headings(src_path: str) -> dict:
    """ Reads an image metadata file and returns the data as a dictionary.
    Adds the key "image_file" to point to the image file.
    :param src_path: full path to the metadata file
    :return: dictionary containing the metadata as key-value pairs
    """
    metadata = {'0': txt_db.image_file_heading}
    with open(src_path, 'r') as src:
        line_id = 0
        for line in src:
            line_id += 1
            words = line.split("\t")
            words = [w.strip() for w in words]
            metadata[str(line_id)] = words[0]
    return metadata


def metadata_indexed_values(src_path: str) -> dict:
    """ Reads an image metadata file and returns the data as a dictionary.
    Adds the key-value 0:"image_file" to point to the image file.
    :param src_path: full path to the metadata file
    :return: dictionary containing the metadata as index-value pairs
    """
    metadata = {}
    metadata_file = os.path.basename(src_path)
    metadata['0'] = txt_db.img_for(metadata_file)
    with open(src_path, 'r') as src:
        line_id = 0
        for line in src:
            line_id += 1
            words = line.split("\t")
            words = [w.strip() for w in words]
            metadata[str(line_id)] = words[1] if len(words) > 1 else "."
    return metadata


def all_meta():
    metas = []
    for root, subFolders, files in os.walk(rootdir):
        for file in files:
            if file.endswith(".txt"):
                src_path = os.path.join(root, file)
                metas.append(metadata_indexed_values(src_path))
    return metas


def selected_meta(filterby, sortby):
    """
    Filter, sort data frame then transform into list(dict), where
    each dict is a mapping of col_index:col_value.
    :param filterby: filter params
    :param sortby: sort params
    :return: list of dict of col_idx:col_val
    """
    df_flt = txt_db.select(df, filterby)
    df_srt = txt_db.order(df_flt, sortby)
    # Convert each row of the data frame to a list
    llist = [df_srt.loc[i].tolist() for i in df_srt.index]
    # Zip each list with the column indexes and convert to a dict
    metas = [dict(zip(col_indexes, lst)) for lst in llist]
    return metas


def save_meta(metadata: dict) -> None:
    """ Saves the image metadata to the metadata file.
    It is expected that the fields are loaded from the file in the correct order,
    and the entries in the 'metadata' dictionary are in the same order.
    ToDo: handle the situation where the "Image file" has been modified as a request to rename.
    20211107: Elaine says she will "never want to modify the name of the JPG file".
    :param metadata: content of the form
    :return: None
    """
    dst_path = rootdir + txt_db.meta_for(metadata[txt_db.image_file_heading])
    dst = open(dst_path, "w")
    for key in metadata:
        if key == txt_db.image_file_heading:
            # ToDo: load the metadata file from disk. Check whether the name is now different
            pass
        else:
            words = [key, metadata[key]]
            words = [w.strip() for w in words]
            line_out = "\t".join(words) + "\n"
            dst.write(line_out)
            # print(key, metadata[key])
    dst.close()
    global df
    # ToDo: refresh just this file, not the whole dataframe
    df = txt_db.load_metadata()


# for root, subFolders, files in os.walk(rootdir):
#     for file in files:
#         if file.endswith(".txt"):
#             src_path = os.path.join(root, file)
#             # ToDo: read metadata as a dict d, and store it: image_data[image_file] = d
#             metadata = metadata_dict(src_path)
