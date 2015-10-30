#!/usr/bin/env python

import os
import pyfits

def main():
	os.system("mkdir spec")
	ifitsname = os.popen("ls *.fits").readlines()
	fitsnames = [ i.split('\n')[0] for i in ifitsname ]
	for i in fitsnames:
		fits = pyfits.open(i)
		hdr  = fits[1].header
		if 'NAXIS1' in hdr and 'NAXIS2' in hdr:
			xnum = fits[1].header["NAXIS1"]
			ynum = fits[1].header["NAXIS2"]
			if xnum == 2148 and ynum == 4612:
				print "mv " + i + " to spec"
				os.system("mv " + i + " spec/")

if __name__ == "__main__":
	main()
