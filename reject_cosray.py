#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
from pyraf import iraf

iraf.imred()
iraf.crutil()


def crmedian(fn, oname):
    """
    Reject cosmic ray with iraf command crmedian
    fn : fits name or fits name list, like abc.fits or abc.fits,abd.fits or
        @name.lst, should required with iraf syntax.
    type : string
    oname : out put file name or file name list, like cabc.fits or
        cabc.fits,cabd.fits or @cname.lst, should required with iraf syntax.
    """
    if os.path.isfile(oname):
        print 'remove file ' + oname
        os.remove(oname)
    iraf.crmedian(input=fn, output=oname, crmask='', median='', sigma='',
                  residual='', var0=0.0, var1=0.0, var2=0.0, lsigma=10.0,
                  hsigma=3.0, ncmed=5, nlmed=5, ncsig=25, nlsig=25)


def main():
    """
    reject cosmic ray, after wavelength calibration here.
    out file name add a char 'c', like cwftbo*.fits.
    But in order compatible with old naming notations,
    we rename the file name.
    """
    filename = 'cor_lamp.lst'
    namelst = open(filename).readlines()
    namelst = [i.strip() for i in namelst]
    for name in namelst:
        crmedian('wftbo'+name, 'cwftbo'+name)
    print "rename 's/wftbo/pcwftbo/' wftbo*.fits"
    os.system("rename 's/wftbo/pcwftbo/' wftbo*.fits")
    print "rename 's/cwftbo/wftbo/' cwftbo*.fits"
    os.system("rename 's/cwftbo/wftbo/' cwftbo*.fits")


if __name__ == '__main__':
    main()
