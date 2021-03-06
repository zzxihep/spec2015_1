#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 16:54:57 2015

@author: zzx
"""
import os
from pyraf import iraf
import sspecplot
import func


def apall(ilst, olst):
    iraf.noao()
    iraf.twodspec()
    iraf.apextract(dispaxis=2, database='database')
    for i, infile in enumerate(ilst):
        outfile = olst[i]
        laper, raper, back_samp = func.get_aper(infile)
        while True:
            if os.path.isfile(outfile):
                print('remove ' + outfile)
                os.remove(outfile)
            delfile = os.getcwd()+os.sep+'database/ap'+infile[0:-5]
            if os.path.isfile(delfile):
                print('remove ' + delfile)
                os.remove(delfile)
            iraf.apall(input=infile, output=outfile, apertures=2,
                       format='multispec', references='', profiles='',
                       interactive=True, find=True, recenter=True,
                       resize=False, edit=True, trace=True, fittrace=True,
                       extract=True, extras=True, review=True, line='INDEF',
                       nsum=10, lower=laper, upper=raper, apidtable='',
                       b_function='chebyshev', b_order=2, b_sample=back_samp,
                       b_naverage=-25, b_niterate=1, b_low_reject=3.0,
                       b_high_reject=3.0, b_grow=0.0, width=5.0, radius=10.0,
                       threshold=0.0, nfind=2, minsep=5.0, maxsep=100000.0,
                       order='increasing', aprecenter='', npeaks='INDEF',
                       shift=True, llimit='INDEF', ulimit='INDEF', ylevel=0.1,
                       peak=True, bkg=True, r_grow=0.0, avglimits=False,
                       t_nsum=20, t_step=10, t_nlost=3, t_function='legendre',
                       t_order=7, t_sample='*', t_naverage=1, t_niterate=1,
                       t_low_reject=3.0, t_high_reject=3.0, t_grow=0.0,
                       background='median', skybox=1, weights='none',
                       pfit='fit1d', clean=True, saturation='INDEF',
                       readnoise=9.4, gain=0.35, lsigma=4.0, usigma=4.0,
                       nsubaps=1)
            iraf.flpr()
            sspecplot.sspecplot(outfile)
            getval = raw_input(('Are you need repeat apall,'
                                'may be clean should be close(r/n)'))
            if getval != 'r':
                break


def main():
    print('='*20 + ' extract ' + '='*20)
    lst = [i.strip() for i in file('cor_lamp.lst')]
    ilst = ['wftbo'+i for i in lst]
    olst = ['awftbo'+i for i in lst]
    apall(ilst, olst)


if __name__ == '__main__':
    main()
