# coding=utf8
#!/usr/bin/env python

import os
import sys
import func
from pyraf import iraf

def to_str(lst, sep=','):
    """
    convert string list to a sum string, like lst = ['abc.fits', 'def.fits', 'ghi.fits'], return 'abc.fits,def.fits,ghi.fits'
    lst : string list
    type : list
    sep : separator, default is ','
    type : char
    return : sum string
    type : string
    """
    ret = ''
    for string in lst:
        ret += string + sep
    size = len(sep)
    ret = ret[:-size]
    return ret

def scopy_cmp(fn, w1 = 'INDEF', w2 = 'INDEF'):
    """
    copy part of a spectrum, and generate a new spectrum fits file. if a same name file already exist, this function will delete the old one. if the fits fn have more than one apertures, this function will just extract the last aperture.
    fn : fits name
    type : string
    w1 : start wavelength, default='INDEF'
    type : float or a string='INDEF'
    w2 : end wavelength, default='INDEF'
    type : float or a string='INDEF'
    return : out put file name
    type : string
    """
    nax2 = pyfits.getval(fn, keyword = 'NAXIS2')
    outname = str(w1)+'_'+str(w2)+'_'+fn
    if os.path.isfile(outname):
        print('remove file '+outname)
        os.remove(outname)
    iraf.scopy(input = fn, output = outname, w1 = w1, w2 = w2, \
        apertures = nax2, bands = 1, beams = '', apmodulus = 0, \
        format = 'multispec', renumber = 'Yes', offset = 0, \
        clobber = 'No', merge = 'No', rebin = 'No', verbose = 'Yes')
    return outname

def icontinuum(fn):
    """
    call iraf command continuum, if out put file already exist, this function will delete the old one.
    fn : fits name
    type : string
    return : out put file name
    type : string
    """
    outname = 'c'+fn
    if os.path.isfile(outname):
        print('remove file '+outname)
        os.remove(outname)
    iraf.continuum(input = fn, output = 'c'+fn, lines = '*', bands = 1, \
        type = 'ratio', replace = 'Yes', wavescale = 'Yes', logscale = 'No', \
        override = 'No', listonly = 'No', logfiles = 'logfile', \
        interactive = 'Yes', sample = '*', naverage = 1, function = 'spline3', \
        order = 1, low_reject = 2.0, high_reject = 0.0, niterate = 10, \
        grow = 1.0, markrej = 'Yes', graphics = 'stdgraph', cursor = '', \
        ask = 'Yes')
    return 'c'+fn # return out fit name

def scombine(fstr, oname, combine = 'sum'):
    """
    call iraf command scombine, generate a combined spectrum file, if the file already exist, this function will delete the old one.
    fstr : input string, like fstr=abc.fits,abd.fits,abe.fits
    type : string
    oname : output file name
    type : string
    combine : the spectrum combine method, the method include 'average', 'median', 'sum', default='sum'
    type : string
    """
    if os.path.isfile(oname):
        print('remove file '+oname)
        os.remove(oname)
    iraf.scombine(input=fstr, output=oname, noutput = '', logfile='STDOUT', \
        apertures = '', group = 'apertures', combine=combine, reject = 'none',\
        first = 'No', w1 = 'INDEF', w2 = 'INDEF', dw = 'INDEF', nw = 'INDEF', \
        log = 'No', scale = 'none', zero = 'none', weight = 'none', \
        sample = '', lthreshold = 'INDEF', lthreshold = 'INDEF', nlow = 1, \
        nhigh = 1, nkeep = 1, mclip = 'Yes', lsigma = 3.0, hsigma = 3.0, \
        rdnoise = 'RDNOISE', gain = 'GAIN', snoise = 0.0, sigscale = 0.1, \
        pclip = -0.5, grow = 0, blank = 1.0)

def gen_cal(fn):
    """
    generate the calibration file of iraf command telluric, if the file already exist, this function will delete the old one.
    fn : fits name
    type : name
    return : out put file name
    type : string
    """
    windows = [[6800.0, 7110.0], [7110.0, 7470.0], [7500.0, 7800], [8000.0, 8480.0]]
    oname = 'cont_' + fn
    if os.path.isfile(oname):
        print('remove file '+oname)
        os.remove(oname)
    namelst = []
    for window in windows:
        name = scopy_cmp(fn, w1 = window[0], w2 = window[1])
        namelst.append(name)
    namestr = ''
    for name in namelst:
        oname = icontinuum(name)
        namestr += oname + ','
    namestr = namestr[:-1]
    scombine(fstr = namestr, oname=oname)
    return oname

def telluric(iname, oname, cal):
    """
    call iraf command telluric, if output file already exist, this function will delete the old one.
    iname : input file name
    type : string
    oname : output file name
    type : string
    cal : calibration file name
    type : string
    """
    iraf.telluric(input=iname, output=oname, cal=cal, ignoreaps='Yes', \
        xcorr = 'Yes', tweakrms='Yes', interactive='Yes', sample='*', \
        threshold=0.0, lag=10, shift=0.0, scale=1.0, dshift=1.0, dscale=0.2, \
        offset=1.0, smooth=1, cursor='', airmass='AIRMASS', answer='yes')

def main():
    stdlst = open('std.lst').readlines()
    stdlst = ['waftbo'+i.strip() for i in stdlst]
    objlst = open('cor_std.lst').readlines()
    objlst = ['waftbo'+i.strip() for i in objlst]
    calstdlst = []
    for name in stdlst:
        calname = gen_cal(name)
        calstdlst.append(calname)
    calobjlst = []
    for name in objlst:
        calname = gen_cal(name)
        calobjlst.append(calname)
    for i, name in enumerate(calstdlst):
        telluric(stdlst[i], 'telself_'+stdlst[i], name)
    for i, name in enumerate(calobjlst):
        telluric(objlst[i], 'telself_'+objlst[i], name)
    stdcalname = 'stdcalaver.fits'
    namestr = to_str(calstdlst)
    scombine(namestr, stdcalname, combine='average')
    for i, name in enumerate(objlst):
        telluric(name, 'telstd_'+name, stdcalname)

if __name__ == '__main__':
    main()
