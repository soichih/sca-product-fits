#!/usr/bin/env python
import os
import json

pngs=[]
dzis=[]

for file in os.listdir("output"):
    if file.endswith(".png"):
        pngs.append({"filename": "output/"+file}) #what about size?
    if file.endswith(".dzi"):
        dzis.append({"filename": "output/"+file}) #what about size?

products = []
products.append({"type": "png", "files": pngs})
products.append({"type": "dzi", "files": dzis})

with open("products.json", "w") as outfile:
    json.dump(products, outfile)
