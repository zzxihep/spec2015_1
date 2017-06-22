# coding=utf8
#!/usr/bin/env python

import os
import sys
from pyraf import iraf
from PyAstronomy.pyasl import read1dFitsSpec

# def read_spec(filename):
    # w, s = read1dFitsSpec

def icontinuum(fn):
    iraf.continuum(input = fn, output = 'c'+fn, lines = '*', bands = 1, \
        type = 'ratio', replace = 'Yes', wavescale = 'Yes', logscale = 'No', \
        override = 'No', listonly = 'No', logfiles = 'logfile', \
        interactive = 'Yes', sample = '*', naverage = 1, function = 'spline3', \
        order = 1, low_reject = 2.0, high_reject = 0.0, niterate = 10, \
        grow = 1.0, markrej = 'Yes', graphics = 'stdgraph', cursor = '', \
        ask = 'Yes')
    return 'c'+fn # return out fit name

def scombine(fstr, oname):
    iraf.scombine(input=fstr, output=oname, noutput = '', logfile='STDOUT', \
        apertures = '', group = 'apertures', combine = 'sum', reject = 'none',\
        first = 'No', w1 = 'INDEF', w2 = 'INDEF', dw = 'INDEF', nw = 'INDEF', \
        log = 'No', scale = 'none', zero = 'none', weight = 'none', \
        sample = '', lthreshold = 'INDEF', lthreshold = 'INDEF', nlow = 1, \
        nhigh = 1, nkeep = 1, mclip = 'Yes', lsigma = 3.0, hsigma = 3.0, \
        rdnoise = 'RDNOISE', gain = 'GAIN', snoise = 0.0, sigscale = 0.1, \
        pclip = -0.5, grow = 0, blank = 1.0)

def continuum(fn):
    windows = [[6800.0, 7110.0], [7110.0, 7470.0], [7500.0, 7800], [8000.0, 8480.0]]
    namelst = []
    for window in windows:
        name = scopy_cmp(fn, w1 = window[0], w2 = window[1])
        namelst.append(name)
    cnamelst = []
    for name in namelst:
        oname = icontinuum(name)
        cnamelst.append(oname)
    namestr = ''
    for name in cnamelst:
        namestr += name+','
    namestr = namestr[:]

def scopy_cmp(fn, w1 = 'INDEF', w2 = 'INDEF'):
    nax2 = pyfits.getval(fn, keyword = 'NAXIS2')
    outname = str(w1)+'_'+str(w2)+'_'+fn
    iraf.scopy(input = fn, output = outname, w1 = w1, w2 = w2, \
        apertures = nax2, bands = 1, beams = '', apmodulus = 0, \
        format = 'multispec', renumber = 'Yes', offset = 0, \
        clobber = 'No', merge = 'No', rebin = 'No', verbose = 'Yes')
    return outname
