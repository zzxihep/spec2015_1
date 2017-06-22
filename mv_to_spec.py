#!/usr/bin/env python

import re
import os
import shutil
import pyfits

def main():
    os.mkdir('spec')
    ifitsname = os.listdir(os.getcwd())
    fitsnames = [i for i in ifitsname if os.path.isfile(i) and re.match("^Y[A-Z].+[a-l][\d]{6}\\.fits$", i) != None]
    for i in fitsnames:
        fits = pyfits.open(i)
        hdr = fits[1].header
        if 'NAXIS1' in hdr and 'NAXIS2' in hdr:
            xnum = fits[1].header["NAXIS1"]
            ynum = fits[1].header["NAXIS2"]
            if xnum == 2148 and ynum == 4612 and os.path.getsize(i) == 39646080:
                print("mv " + i + " to spec")
                shutil.move(i, os.getcwd() + os.sep + 'spec' + os.sep + i)

if __name__ == "__main__":
    main()
