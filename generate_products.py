#!/usr/bin/env python
import os
import json

images=[]
dzis=[]

for file in os.listdir("output"):
    if file.endswith(".png"):
        images.append({"filename": "output/"+file}) #what about size?
    if file.endswith(".dzi"):
        dzis.append({"filename": "output/"+file}) #what about size?

products = []
products.append({"type": "soichih/image", "files": images})
products.append({"type": "soichih/dzi", "files": dzis})

with open("products.json", "w") as outfile:
    json.dump(products, outfile)
