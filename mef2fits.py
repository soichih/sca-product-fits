#!/usr/bin/env python

import os, sys, subprocess


if __name__ == "__main__":

    outfile = sys.argv[1]
    infile = sys.argv[2:]

    valid_infiles  = []
    del_files = []
    for idx, fn in enumerate(infile):
        if (fn.endswith(".fz")):
            tmpfile = "%s.unpack" % (fn)
            cmd = "funpack -O %s %s" % (tmpfile,fn)
            os.system(cmd)
            del_files.append(tmpfile)
            valid_infiles.append(tmpfile)
        else:
            valid_infiles.append(fn)

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
    """ % (outfile, " ".join(valid_infiles))

    try:
        ret = subprocess.Popen(cmd.split(), 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        (_stdout, _stderr) = ret.communicate()
        if (ret.returncode != 0):
            print "There was a problem:\n%s" % (_stderr)
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e
    
    for fn in del_files:
        if (os.path.isfile(fn)):
            os.remove(fn)
