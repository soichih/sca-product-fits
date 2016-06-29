#!/usr/bin/env python

import os, sys, subprocess
import deepzoom

if __name__ == "__main__":

    source = sys.argv[1]
    dest = sys.argv[2]

    creator = deepzoom.ImageCreator(tile_size=512, tile_overlap=2, tile_format="jpg", image_quality=0.9, resize_filter="bicubic")
    creator.create(source, dest)


    

