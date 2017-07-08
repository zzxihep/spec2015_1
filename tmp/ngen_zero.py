#! /usr/bin/env python

import os,shutil
import pyfits
from pyraf import iraf

def coroverscan(filename):
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    iraf.ccdproc(images = '@' + filename + '//[1]'
    	, output = '%o%o%@' + filename
	, ccdtype = '', max_cache = 0, noproc = False
	, fixpix = False, overscan = True, trim = False
	, zerocor = False, darkcor = False, flatcor = False
	, illumcor = False, fringecor = False, readcor = False
	, scancor = False, readaxis = 'line', fixfile = ''
	, biassec = '[5:45,1:4612]', trimsec = '', zero = ''
	, dark = '', flat = '', illum = '', fringe = ''
	, minreplace = 1.0, scantype = 'shortscan', nscan = 1
	, interactive = False, function = 'chebyshev', order = 1
	, sample = '*', naverage = 1, niterate = 1
	, low_reject = 3.0, high_reject = 3.0, grow = 1.0)
    iraf.flpr()

def combinebias(filename):
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    iraf.zerocombine(input = 'o//@' + filename
	, output = 'Zero', combine = 'average', reject = 'minmax'
	, ccdtype = '', process = False, delete = False
	, clobber = False, scale = 'none', statsec = ''
	, nlow = 0, nhigh = 1, nkeep = 1, mclip = True
	, lsigma = 3.0, hsigma = 3.0, rdnoise = 'rdnoise'
	, gain = 'gain', snoise = 0.0, pclip = -0.5, blank = 0.0)

def clear():
    path = os.getcwd()
    filename = os.listdir(path)
    filename = [tmp for tmp in filename if os.path.isfile(tmp) and \
            tmp[0:3] == 'oYF' and tmp[-5:] =='.fits']
    for i in filename:
        print('remove ' + i)
        os.remove(path + os.sep + i)
    if os.path.isfile('Zero.fits'):
        print('remove Zero.fits')
        os.remove(path + os.sep + 'Zero.fits')

def gen_biaslst():
    biaspath = os.getcwd()
    fitname = []
    fitname = os.listdir(biaspath)
    fitname = [i for i in fitname if i[0:2] == 'YF' and i[-5:] == '.fits']
    nfitname = []
    for name in fitname:
        fit = pyfits.open(name)
        if 'bia' in fit[0].header['OBJECT'].lower():
            nfitname.append(name)
    if len(nfitname) > 0:
        nfitname.sort()
        f = open('spec_bias.lst', 'w')
        for i in nfitname:
            print(i + ' ---> spec_bias.lst')
            f.write( i + '\n')
        f.close()


def main():
    clear()
    gen_biaslst()
    coroverscan('spec_bias.lst')
    combinebias('spec_bias.lst')

if __name__ == '__main__':
    main()
