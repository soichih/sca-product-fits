#!/usr/bin/env python

import os, sys, subprocess


if __name__ == "__main__":

    infile = sys.argv[1]
    outfile = sys.argv[2]

    #
    # Run swarp
    #
    cmd = """\
    swarp 
    -IMAGEOUT_NAME %s
    -WEIGHTOUT_NAME /dev/null
    -SUBTRACT_BACK N
    -FSCALE_KEYWORD XXXXXXX
    -VERBOSE_TYPE QUIET
    %s
    """ % (outfile, infile)

    try:
        ret = subprocess.Popen(cmd.split(), 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        (_stdout, _stderr) = ret.communicate()
        if (ret.returncode != 0):
            print "There was a problem:\n%s" % (_stderr)
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e
    
