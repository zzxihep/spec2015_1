#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 22:08:34 2015

@author: zzx
"""

import os
import pyfits
from pyraf import iraf
from termcolor import colored
from func import script_path
import func

stdpath = func.std_path+os.sep
extpath = func.lijiang_extinction_file


def standard(namelst):
    iraf.noao()
    iraf.twodspec()
    iraf.longslit(dispaxis=2, nsum=1, observatory='Lijiang',
                  extinction=extpath, caldir=stdpath)
    stdnamelst = []
    for std_fitsname in namelst:
        stdname, stdmag, stdmagband = func.standard_star_info(std_fitsname)
        print(colored('the standard star is ' + stdname, 'green'))
        stdnamelst.append(std_fitsname)
    stdnamestr = func.to_str(stdnamelst)
    if os.path.isfile('Std'):
        print('remove file Std')
        os.remove('Std')
    iraf.standard(input=stdnamestr, output='Std', samestar=True,
                  beam_switch=False, apertures='', bandwidth='INDEF',
                  bandsep='INDEF',  # 30.0  20.0
                  fnuzero=3.6800000000000E-20, extinction=extpath,
                  caldir=stdpath, observatory='Lijiang', interact=True,
                  graphics='stdgraph', cursor='', star_name=stdname,
                  airmass='', exptime='', mag=stdmag, magband=stdmagband,
                  teff='', answer='yes')
    if os.path.isfile('Sens.fits'):
        print('remove file Sens.fits')
        os.remove('Sens.fits')
    iraf.sensfunc(standards='Std', sensitivity='Sens',
                  extinction=extpath, function='spline3', order=9)
    iraf.splot('Sens')


def calibrate(namelst):
    iraf.noao()
    iraf.twodspec()
    iraf.longslit(dispaxis=2, nsum=1, observatory='Lijiang',
                  extinction=extpath, caldir=stdpath)
    for fitname in namelst:
        outname = 'mark_' + fitname
        if os.path.isfile(outname):
            print('remove file ' + outname)
            os.remove(outname)
        stdfitname = 'Sens'
        iraf.calibrate(input=fitname, output=outname, extinct='yes',
                       flux='yes', extinction=extpath, ignoreaps='yes',
                       sensitivity=stdfitname, fnu='no')
        iraf.splot(images=outname)


def main():
    for name in file('cor_lamp.lst'):
        func.set_airmass('awftbo'+name.strip())
    stdlst = open('std.lst').readlines()
    stdlst = ['awftbo'+i.strip() for i in stdlst]
    standard(stdlst)
    objlst = open('cor_std.lst').readlines()
    objlst = ['awftbo'+i.strip() for i in objlst]
    calibrate(objlst)


if __name__ == '__main__':
    main()
