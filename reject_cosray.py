#!/usr/binenv python
# -*- coding=utf-8 -*-

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
    iraf.crmedian(input=fn, output=oname, crmask='', median='', sigma='',
                  residual='', var0=0.0, var1=0.0, var2=0.0, lsigma=10.0,
                  hsigma=3.0, ncmed=5, nlmed=5, ncmed=5, nlmed=5, ncsig=25,
                  nlsig=25)


def main():
    """
    reject cosmic ray, after wavelength calibration here.
    out file name add a char 'c', like cwftbo*.fits
    """
    filename = 'cor_lamp.lst'
    crmedian('wftbo@'+filename, 'cwftbo@'+filename)


if __name__ == '__main__':
    main()
