#!/usr/bin/env python

import sys
import os
import numpy
import pyfits
import scipy, scipy.stats
import math
from optparse import OptionParser
import PIL
from PIL import Image


if __name__ == "__main__":

    # Read the command line options
    parser = OptionParser()
    parser.add_option("", "--scale", dest="scaling",
                      help="Type of scaling (lin / asinh)",
                      default="lin")
    parser.add_option("-s", "--tilesize", dest="tilesize",
                      help="size of an individual size",
                      default=512, type=int)
    parser.add_option("-o", "--out", dest="outfile",
                      help="output filename",
                      default="fits2png",
                      )
    parser.add_option("-t", "--type", dest="filetype",
                      help="file type (e.g. png, jpg)",
                      default="png",
                      )
    parser.add_option("--min", dest="mingood",
                      help="minimum good flux value",
                      default=-1e10, type=float)
    parser.add_option("--max", dest="maxgood",
                      help="maximum good flux value",
                      default=+1e10, type=float)
    parser.add_option("--mask", dest="mask",
                      help="mask all pixels without valid data",
                      action="store_true")
    parser.add_option("-n", "--nsamples", dest="nsamples",
                      help="number of samples for scaling determination",
                      default=1000, type=int)
    (options, cmdline_args) = parser.parse_args()


    #
    # Open FITS file
    #
    infile = cmdline_args[0]
    hdulist = pyfits.open(infile)

    # Extract the wcs information produced by swarp and save it to the exposure dir
   # try:
   #      primary = hdulist[0].header
   #      wcs_keywords = ['CRPIX1','CRPIX2','CRVAL1','CRVAL2','CD1_1','CD1_2','CD2_1','CD2_2']
   #      wcs = {}
   #      for wk in wcs_keywords:
   #          try:
   #              wcs[wk] = primary[wk]
   #          except:
   #              wcs[wk] = "0"
   #      wcs_file = exposure_dir + "/wcs.json"
   #      f = open(wcs_file,'w')
   #      f.write(json.dumps(wcs))
   #      f.close()
   #  except Exception, e:
   #      print e



    #
    # Find best scaling
    #
    data = hdulist[0].data
    if (data == None):
        print ("No image data found in PrimaryHDU - need to run mef2fits first?")
        sys.exit(0)

    print("Image-size: %d x %d" % (data.shape[1], data.shape[0]))
    print("Masking out pixels with intensities outside valid range")
    data[(data<options.mingood)|(data>options.maxgood)] = numpy.NaN

    if (options.mask):
        print("Masking out pixels without valid data")
        data[data == 0.0] = numpy.NaN
    #print data
    #print data.shape

    n_samples = options.nsamples
    boxwidth=10

    box_center_x = numpy.random.randint(boxwidth, data.shape[1]-boxwidth, n_samples)
    box_center_y = numpy.random.randint(boxwidth, data.shape[0]-boxwidth, n_samples)
    samples = numpy.zeros(n_samples)

    for i in range(n_samples):
        
        x1, x2 = int(box_center_x[i]-boxwidth), int(box_center_x[i]+boxwidth)
        y1, y2 = int(box_center_y[i]-boxwidth), int(box_center_y[i]+boxwidth)

        samples[i] = numpy.mean(data[y1:y2, x1:x2])

    #
    # Now do some filtering of the median values
    #
    valid = numpy.isfinite(samples)
    #_old_sigma, _old_med = numpy.max(samples) - numpy.min(samples)
    for iter in range(3):
    
        _med = numpy.median(samples[valid])
        _vars = numpy.percentile(samples[valid], [16,84])
        #_vars = scipy.stats.scoreatpercentile(samples[valid], [16,84])
        _sigma = 0.5*(_vars[1] - _vars[0])

        print iter, numpy.sum(valid), _med, _vars, _sigma

        valid = numpy.isfinite(samples) & (samples > _med-3*_sigma) & (samples < _med+3*_sigma)
        if (numpy.sum(valid) <= 0):
            break

    if (options.scaling == "lin"):
        min_intensity = _med - _sigma
        max_intensity = _med + 10*_sigma
        print "linear Intensity scaling: %f -- %f" % (min_intensity, max_intensity)

        norm_flux = (data - min_intensity) / (max_intensity - min_intensity)
        norm_flux[norm_flux < 0] = 0.0
        norm_flux[norm_flux > 1] = 1.0
    elif (options.scaling == "asinh"):
        min_intensity = _med - 3*_sigma
        max_intensity = _med + 30*_sigma
        print "arcsinh Intensity scaling: %f -- %f" % (min_intensity, max_intensity)

        norm_flux = (data - min_intensity) / (max_intensity - min_intensity)
        norm_flux[norm_flux < 0] = 0.0
        norm_flux[norm_flux > 1] = 1.0
        norm_flux = numpy.arcsinh(norm_flux)

    #
    # Create PNG file:
    # remap data from intensity range to 0...255
    #
    greyscale = (norm_flux * 255.).astype(numpy.uint8)

    img = Image.fromarray(greyscale)
    img.transpose(Image.FLIP_TOP_BOTTOM).save("%s.%s" % (
        options.outfile,options.filetype))
