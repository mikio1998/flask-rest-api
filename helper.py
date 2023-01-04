#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 18:34:36 2022

@author: mikionakata
"""
from collections import defaultdict

def decode_sold_products_data(df):
    dict = defaultdict(lambda: [])
    for index, row in df.iterrows():
        obj = sold_prod_row_to_object(row)
        if row["Handle"] in dict:
            found = False
            for i in range(len(dict[row["Handle"]])): #for each variant
                item = dict[row["Handle"]][i]
                if item['size'] == obj["size"] and item['color'] == obj["color"]:
                    new = dict[row["Handle"]]
                    new[i]["quantity"] = dict[row["Handle"]][i]["quantity"] + obj["quantity"]
                    dict.update({row["Handle"]: new})
                    found = True
                    break
            if found == False:
                dict[row["Handle"]] += [obj]
        else:
            dict[row["Handle"]] += [obj]
    return dict

def sold_prod_row_to_object(row):
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
        "size": size,
        "color": color,
        "url": url,
        "quantity": row["Quantity"]
    }


    
# def data_to_dict(df, vendor):
def decode_products_data(df, vendor=None):
    dict = {}
    
    for index, row in df.iterrows():
        
        if vendor != None and row["Vendor"] != vendor:
            continue
        
        obj = row_to_object(row)
        
        # If id exists
        if row["Handle"] in dict:
            obj["name"] = dict[row["Handle"]][0]["name"]
            obj["vendor"] = dict[row["Handle"]][0]["vendor"]
            dict[row["Handle"]] += [obj]
        else:
            dict[row["Handle"]] = [obj]
    return dict

def row_to_object(row):
    color = None
    if row["Option1 Name"] == "color":
        color = row["Option1 Value"]
    elif row["Option2 Name"] == "color":
        color = row["Option2 Value"]
        
    size = None
    if row["Option1 Name"] == "size":
        size = row["Option1 Value"]
    elif row["Option2 Name"] == "size":
        size = row["Option2 Value"]
        
    url = row["Variant Image"]
    if url == "":
        url = None
        
    return {
        "name": row["Title"],
        "vendor": row["Vendor"],
        "price": row["Variant Price"],
        "size": size,
        "color": color,
        "url": url,
        "sku": row["Variant SKU"]
    }

def get_variants(df, handle):
    dict = {handle: []}
    for index, row in df.iterrows():
        if row["Handle"] == handle:
            obj = row_to_object(row)
            if len(dict[handle]) != 0:
                obj["name"] = dict[handle][0]["name"]
            dict[handle] += [obj]
    return dict
    
    
    
    
    
    
    
    