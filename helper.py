#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 18:34:36 2022

@author: mikionakata
"""

# def data_to_dict(df, vendor):
def data_to_dict(df, vendor=None):
    dict = {}
    
    for index, row in df.iterrows():
        
        if vendor != None and row["Vendor"] != vendor:
            continue
        
        obj = row_to_object(row)
        
        # If id exists
        if row["Handle"] in dict:
            dict[row["Handle"]]["variants"] += [obj]
        else:
            dict[row["Handle"]] = obj
    return dict

def row_to_object(row):
    color = None
    if row["Option1 Name"] == "Color":
        color = row["Option1 Value"]
    elif row["Option2 Name"] == "Color":
        color = row["Option2 Value"]
        
    size = None
    if row["Option1 Name"] == "Size":
        size = row["Option1 Value"]
    elif row["Option2 Name"] == "Size":
        size = row["Option2 Value"]
        
    url = row["Variant Image"]
    if url == "":
        url = None
    
    return {
        "name": row["Title"],
        "vendor": row["Vendor"],
        "price": row["Variant Price"],
        "variants": [{
            "name": row["Title"],
            "vendor": row["Vendor"],
            "price": row["Variant Price"],
            "size": size,
            "color": color,
            "url": url
        }]}