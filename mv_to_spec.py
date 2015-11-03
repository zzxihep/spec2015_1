#!/usr/bin/env python

import os,shutil
import pyfits

def main():
        os.mkdir('spec')
	#os.system("mkdir spec")
	#ifitsname = os.popen("ls *.fits").readlines()
        ifitsname = os.listdir(os.getcwd())
        fitsnames = [ i for i in ifitsname if os.path.isfile(i) and i[-5:] == '.fits' ]
	for i in fitsnames:
		fits = pyfits.open(i)
		hdr  = fits[1].header
		if 'NAXIS1' in hdr and 'NAXIS2' in hdr:
			xnum = fits[1].header["NAXIS1"]
			ynum = fits[1].header["NAXIS2"]
			if xnum == 2148 and ynum == 4612:
				print "mv " + i + " to spec"
                                shutil.move(i, os.getcwd() + os.sep + 'spec' + os.sep + i)
				#os.system("mv " + i + " spec/")

if __name__ == "__main__":
	main()
