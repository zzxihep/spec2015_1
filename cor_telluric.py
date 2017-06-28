#!/usr/bin/env python
# coding=utf8

# @Author: zhixiang zhang <zzx>
# @Date:   26-Jun-2017
# @Email:  zhangzx@ihep.ac.cn
# @Filename: cor_telluric.py
# @Last modified by:   zzx
# @Last modified time: 28-Jun-2017


import os
import sys
import glob
import shutil
import pyfits
from pyraf import iraf
import func
import re_corflux


def to_str(lst, sep=','):
    """
    convert string list to a sum string,
    like lst = ['abc.fits', 'def.fits', 'ghi.fits'],
    return 'abc.fits,def.fits,ghi.fits'
    lst : string list
    type : list
    sep : separator, default ','
    type : string
    return : sum string
    type : string
    """
    ret = ''
    for string in lst:
        ret += string + sep
    size = len(sep)
    ret = ret[:-size]
    return ret


def scopy_cmp(fn, w1='INDEF', w2='INDEF'):
    """
    copy part of a spectrum, and generate a new spectrum fits file.
    if a same name file already exist, this function will delete the old.
    if the fits fn have more than one apertures,
    this function will just extract the last aperture.
    fn : fits name
    type : string
    w1 : start wavelength, default='INDEF'
    type : float or a string='INDEF'
    w2 : end wavelength, default='INDEF'
    type : float or a string='INDEF'
    return : out put file name
    type : string
    """
    nax2 = pyfits.getval(fn, keyword='NAXIS2')
    outname = str(w1) + '_' + str(w2) + '_' + fn
    if os.path.isfile(outname):
        print('remove file ' + outname)
        os.remove(outname)
    iraf.scopy(input=fn, output=outname, w1=w1, w2=w2, apertures=nax2,
               bands=1, beams='', apmodulus=0, format='multispec',
               renumber='Yes', offset=0, clobber='No', merge='No',
               rebin='No', verbose='Yes')
    return outname


def icontinuum(fn):
    """
    call iraf command continuum.
    If out put file already exist, this function will delete the old one.
    fn : fits name
    type : string
    return : out put file name
    type : string
    """
    outname = 'c' + fn
    if os.path.isfile(outname):
        print('remove file ' + outname)
        os.remove(outname)
    iraf.continuum(input=fn, output=outname, lines='*', bands=1, type='ratio',
                   replace='no', wavescale='Yes', logscale='No', override='No',
                   listonly='No', logfiles='logfile', interactive='Yes',
                   sample='*', naverage=1, function='spline3', order=1,
                   low_reject=1.5, high_reject=0.0, niterate=20, grow=2.0,
                   markrej='Yes', graphics='stdgraph', cursor='', ask='yes')
    return outname  # return out fit name


def scombine(fstr, oname, combine='sum'):
    """
    Call iraf command scombine, generate a combined spectrum file.
    If the file already exist, this function will delete the old one.
    fstr : input string, like fstr=abc.fits,abd.fits,abe.fits
    type : string
    oname : output file name
    type : string
    combine : the spectrum combine method, the method include
    'average', 'median', 'sum', default='sum'.
    type : string
    """
    if os.path.isfile(oname):
        print('remove file ' + oname)
        os.remove(oname)
    iraf.scombine(input=fstr, output=oname, noutput='', logfile='STDOUT',
                  apertures='', group='apertures', combine=combine,
                  reject='none', first='No', w1='INDEF', w2='INDEF',
                  dw='INDEF', nw='INDEF', log='No', scale='none', zero='none',
                  weight='none', sample='', lthreshold='INDEF',
                  hthreshold='INDEF', nlow=1, nhigh=1, nkeep=1, mclip='Yes',
                  lsigma=3.0, hsigma=3.0, rdnoise='RDNOISE', gain='GAIN',
                  snoise=0.0, sigscale=0.1, pclip=-0.5, grow=0, blank=1.0)


def gen_cal(fn):
    """
    generate the calibration file of iraf command telluric.
    If the file already exist, this function will delete the old one.
    fn : fits name
    type : name
    return : out put file name
    type : string
    """
    windows = [[6800.0, 7108.0],
               [7111.0, 7470.0],
               [7500.0, 7800.0],
               [8000.0, 8480.0]]
    oname = 'cont_' + fn
    if os.path.isfile(oname):
        print('remove file ' + oname)
        os.remove(oname)
    namelst = []
    for window in windows:
        name = scopy_cmp(fn, w1=window[0], w2=window[1])
        namelst.append(name)
    namestr = ''
    for name in namelst:
        tmpname = icontinuum(name)
        namestr += tmpname + ','
    namestr = namestr[:-1]
    scombine(fstr=namestr, oname=oname)
    return oname


def telluric(iname, oname, cal, dscale=0.0):
    """
    call iraf command telluric.
    if output file already exist, this function will delete the old one.
    iname : input file name
    type : string
    oname : output file name
    type : string
    cal : calibration file name
    type : string
    """
    if os.path.isfile(oname):
        print('remove file ' + oname)
        os.remove(oname)
    iraf.telluric(input=iname, output=oname, cal=cal, ignoreaps='Yes',
                  xcorr='Yes', tweakrms='Yes', interactive='Yes', sample='*',
                  threshold=0.0, lag=10, shift=0.0, scale=1.0, dshift=1.0,
                  dscale=dscale, offset=1.0, smooth=1, cursor='', airmass='',
                  answer='yes')


def main():
    """
    Assume current dir = Grism_x_Slit_x
    main function
    """
    teldir = 'telluric'
    if not os.path.isdir(teldir):
        print 'mkdir ' + teldir
        os.mkdir(teldir)
    fitlst = glob.glob('awftbo*.fits')
    for name in fitlst:
        print 'copy %s %s%s' % (name, teldir, os.sep)
        shutil.copyfile(name, teldir+os.sep+name)
    os.chdir(teldir)
    namelst = glob.glob('awftbo*.fits')
    stdlst = [i for i in namelst if func.is_std(i)]
    objlst = list(set(namelst) - set(stdlst))
    for name in objlst:
        print name
    calstdlst = []
    for name in stdlst:
        calname = gen_cal(name)
        calstdlst.append(calname)
    calobjlst = []
    for name in objlst:
        calname = gen_cal(name)
        calobjlst.append(calname)
    for i, name in enumerate(calstdlst):
        telluric(stdlst[i], 'telself_' + stdlst[i], name)
    for i, name in enumerate(calobjlst):
        telluric(objlst[i], 'telself_' + objlst[i], name)
    stdcalname = 'stdcalaver.fits'
    namestr = to_str(calstdlst)
    scombine(namestr, stdcalname, combine='average')
    for i, name in enumerate(objlst):
        telluric(name, 'telstd_' + name, stdcalname)
    namelst = glob.glob('tel*.fits')
    stdlst = [i for i in namelst if func.is_std(i)]
    objlst = list(set(namelst) - set(stdlst))
    re_corflux.standard(stdlst)
    re_corflux.calibrate(objlst)
    os.chdir('..')


if __name__ == '__main__':
    main()
