# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 10:58:50 2021

@author: Radu
"""

import datetime
import json
import os
import pandas as pd
import re

image_file_heading = "Image file"


def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


host_config = read_json(r"C:/sw/conf/host_conf.json")
rootdir = host_config["image_gallery"]["root_dir"]
images_dir = rootdir + "/static/images"


def meta_for(image_file: str) -> str:
    # ToDo: if the metadata file does not exist, create it from the template
    return image_file.replace(".JPG", ".txt")


def img_for(meta_file: str) -> str:
    # ToDo: if the image file does not exist, throw an error
    return meta_file.replace(".txt", ".JPG")


image_cols = {image_file_heading: 'str', 'Invent. Number': 'str',
              'Invent. IMG-': 'str', 'Hig Res Image': 'str', 'Date': 'str',
              'ID Title': 'str', 'Website Title': 'str',
              'Part of a Gallery': 'str', 'Medium': 'str', 'Substrate': 'str',
              'Dimensions HxWxD': 'str', 'Orientation': 'str',
              'Edition': 'str', 'Location': 'str',
              'in Inventory': 'str', 'Number Sold': 'int',
              'Sale Price': 'float', 'Cost of Goods': 'float',
              'Current Inventory': 'int', 'Goods Sold': 'float',
              'Currently Shown': 'str', 'Shown in Past': 'str',
              'Keywords': 'str'}

int_col_names = ["Invent. Number", "Invent. IMG-", "Number Sold",
                 "Current Inventory"]
float_col_names = ["Sale Price", "Cost of Goods", "Goods Sold"]
date_col_names = ["Date"]
all_filter_col_names = ["", "Part of a Gallery", "Medium", "Substrate",
                    "Dimensions HxWxD", "Orientation", "Edition", "Location"]
all_sort_col_names = ["", "Invent. Number", "Invent. IMG-", "Hig Res Image",
                  "Date", "ID Title", "Website Title", "Part of a Gallery",
                  "Medium", "Substrate", "Dimensions HxWxD", "Orientation",
                  "Edition", "Location", "in Inventory", "Number Sold",
                  "Sale Price", "Cost of Goods", "Current Inventory",
                  "Goods Sold", "Currently Shown", "Shown in Past"]


def metadata_dict(src_path: str) -> dict:
    """ Reads an image metadata file and returns the data as a dictionary.
    Adds the key "image_file" to point to the image file.
    :param src_path: full path to the metadata file
    :return: dictionary containing the metadata as key-value pairs
    """
    metadata = {}
    metadata_file = os.path.basename(src_path)
    metadata[image_file_heading] = img_for(metadata_file)
    with open(src_path, 'r') as src:
        line_id = 0
        for line in src:
            line_id += 1
            words = line.split("\t")
            words = [w.strip() for w in words]
            words = [re.sub(":$", "", w) for w in words]
            metadata[words[0]] = words[1] if len(words) > 1 else ""
    return metadata


def cols_as_str() -> dict:
    """
    Read the master list of metadata columns and create a dict where
    all columns are declared as type str.
    :return:
    """
    image_cols_str = {image_file_heading: 'str'}
    with open("MetadataTemplate.txt", 'r') as src:
        for line in src:
            col_name = line.replace("\n", "")
            image_cols_str[col_name] = 'str'
    return image_cols_str


def cols_list():
    """
    Read the master list of metadata columns and create a list
    Returns
    -------
    cols : list
        List of all metadata columns.
    """
    cols = []
    with open("MetadataTemplate.txt", 'r') as src:
        for line in src:
            cols.append(line.replace("\n", ""))
    return cols


def df_empty():
    """
    Create an empty dataframe with appropriate data column types.
    Returns
    -------
    df_empty : Pandas dataframe
        empty dataframe with appropriate data column types.
    """
    df_empty = pd.DataFrame({c: pd.Series(dtype=t) for c, t in image_cols.items()})
    return df_empty


def df_empty_str():
    """
    Create an empty dataframe with str data type for all columns.
    Returns
    -------
    df_empty : Pandas dataframe
        empty dataframe with str data type for all columns.
    """    
    image_cols_str = cols_as_str()
    df_empty = pd.DataFrame({c: pd.Series(dtype=t) for c, t in image_cols_str.items()})
    return df_empty


def apply_types(img_dict: dict) -> dict:
    """
    Apply data types to a dict containing image metadata

    Parameters
    ----------
    img_dict : dict
        dict containing image metadata.

    Returns
    -------
    dict
        dict containing image metadata, with appropriate data types.

    """
    for col_name in int_col_names:
        if img_dict[col_name]:
            img_dict[col_name] = int(img_dict[col_name])
    for col_name in float_col_names:
        if img_dict[col_name]:
            img_dict[col_name] = float(img_dict[col_name])
    for col_name in date_col_names:
        if img_dict[col_name]:
            img_dict[col_name] = parse_date(img_dict[col_name])
    return img_dict


def parse_date(s: str):
    """
    Parse a date according to a few supported formats

    Parameters
    ----------
    s : str
        Date in str format.

    Returns
    -------
    Datetime
        Parsed datetime object, or the original string.

    """
    if s:
        d = None
        formats = ['%m/%d/%Y', '%m/%d/%y']
        for format in formats:
            try:
                d = datetime.datetime.strptime(s, format)
                return d
            except ValueError:
                d = None
        return s
    else:
        return s


def load_metadata():
    """
    Load all metadata files into a dataframe.
    Returns
    -------
    df : Pandas Dataframe
        Dataframe containing all the image metadata.
    """
    df = df_empty()
    for root, subFolders, files in os.walk(images_dir):
        for file in files:
            if file.endswith(".txt"):
                src_path = os.path.join(root, file)
                meta_dict = metadata_dict(src_path)
                meta_dict = apply_types(meta_dict)
                meta_vals = [v for k, v in meta_dict.items()]
                df.loc[len(df)] = meta_vals
    return df


def select(df, filterby):
    """
    Filters a dataframe by a set of criteria
    :param df: data frame to be sorted
    :param filterby: dict of col_name:col_value to be used for filtering, eg
        ImmutableMultiDict([('filter1', 'Medium'), ('fv1', 'watercolor/liquid watercolor'), ('filter2', ''), ('sort1', ''), ('sort2', '')])
    :return: filtered data frame
    """
    if len(filterby) == 0:
        return df
    if 'filter1' in filterby.keys() and filterby['filter1']:
        if 'fv1' in filterby.keys() and filterby['fv1']:
            df = df[df[filterby['filter1']] == filterby['fv1']]
    if 'filter2' in filterby.keys() and filterby['filter2']:
        if 'fv2' in filterby.keys() and filterby['fv2']:
            df = df[df[filterby['filter2']] == filterby['fv2']]
    return df


def order(df, sortby):
    """
    Sorts a dataframe by a set of criteria
    :param df: data frame to be sorted
    :param sortby: list of col_name to be used for sorting
    :return: sorted data frame
    """
    if len(sortby) == 0:
        return df
    sort_cols = []
    # if 'sort1' in sortby.keys() and sortby['sort1']:
    #     sort_cols.append(sortby['sort1'])
    # if 'sort2' in sortby.keys() and sortby['sort2']:
    #     sort_cols.append(sortby['sort2'])
    return df.sort_values(by=sort_cols)


def ranges() -> dict:
    """
    Computes the ranges of a number of fields in the data, to facilitate sorting and filtering
    :return: dict of col_name:range_for_col
    """
    ranges_dict = {}
    df = load_metadata()
    # ToDo: convert the metadata dataframe into a canonical form
    for column in all_filter_col_names:
        if column:
            ranges_dict[column] = df[column].unique().tolist()
    return ranges_dict

