#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 22:08:34 2015

@author: zzx
"""

import os
import pyfits
from pyraf import iraf

stdlstname = 'std.lst'

def get_std_group(lstfile):
    f = open(lstfile)
    l = f.readlines()
    f.close()
    l = [tmp.split('\n')[0] for tmp in l]
    group = {}
    for i in l:
        fit = pyfits.open(i)
        name = fit[0].header['object']
        if name in group:
            group[name].append(i)
        else:
            group[name] = [i]
    return group
    
def get_std_mjd(groupset):
    mjdlst = {}
    for i in groupset:
        fit = pyfits.open(groupset[i][0])
        mjdlst[i] = fit[0].header['MJD']
    return mjdlst
    
stdgroup = get_std_group(stdlstname)
stdmjdlst = get_std_mjd(stdgroup)

def select_std(filename):
    fit = pyfits.open(filename)
    fitmjd = fit[0].header['MJD']
    timedif = 10000000.
    name = ''
    for i in stdmjdlst:
        tmp = abs(stdmjdlst[i] - fitmjd)
        if tmp < timedif:
            timedif = tmp
            name = i
    return name
    
def main():
    get
    pass

if __name__ == '__main__':
    main()