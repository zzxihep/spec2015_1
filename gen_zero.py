#! /usr/bin/env python

import os
import shutil
from pyraf import iraf

"""
generate spec Zero file individually.
then cp Zero.fits to every Grism_xx_Slit_xx dir.
"""


def coroverscan(lstfn):
    """
    call iraf command ccdproc, overscan correct.
    lstfn : lst file name
    type : string
    output file : oYF*.fits
    """
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    iraf.ccdproc(images='@'+lstfn+'//[1]', output='%o%o%@'+lstfn, ccdtype='',
                 max_cache=0, noproc=False, fixpix=False, overscan=True,
                 trim=False, zerocor=False, darkcor=False, flatcor=False,
                 illumcor=False, fringecor=False, readcor=False, scancor=False,
                 readaxis='line', fixfile='', biassec='[5:45,1:4612]',
                 trimsec='', zero='', dark='', flat='', illum='', fringe='',
                 minreplace=1.0, scantype='shortscan', nscan=1,
                 interactive=False, function='chebyshev', order=1, sample='*',
                 naverage=1, niterate=1, low_reject=3.0, high_reject=3.0,
                 grow=1.0)
    iraf.flpr()


def combinebias(lstfn):
    """
    call iraf command zerocombine, combine bias fits.
    lstfn : lst file name
    type : string
    output file : Zero.fits
    """
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    iraf.zerocombine(input='o//@'+lstfn, output='Zero', combine='average',
                     reject='minmax', ccdtype='', process=False, delete=False,
                     clobber=False, scale='none', statsec='', nlow=0, nhigh=1,
                     nkeep=1, mclip=True, lsigma=3.0, hsigma=3.0,
                     rdnoise='rdnoise', gain='gain', snoise=0.0, pclip=-0.5,
                     blank=0.0)


def clear():
    path = os.getcwd()
    filename = os.listdir(path)
    filename = [tmp for tmp in filename if os.path.isfile(tmp) and
                tmp[0:3] == 'oYF' and tmp[-5:] == '.fits']
    for i in filename:
        print('remove ' + i)
        os.remove(path + os.sep + i)
    if os.path.isfile('Zero.fits'):
        print('remove Zero.fits')
        os.remove(path + os.sep + 'Zero.fits')


def main():
    if os.path.isdir('bias'):
        if os.path.isfile(os.getcwd()+os.sep+'bias'+os.sep+'spec_bias.lst'):
            os.chdir('bias')
            clear()
            coroverscan('spec_bias.lst')
            combinebias('spec_bias.lst')
            dirname, filename = os.path.split(os.getcwd())
            os.chdir(dirname)
            iraf.flpr()
            path = os.getcwd()
            dirname = os.listdir(path)
            dirname = [tmp for tmp in dirname if os.path.isdir(tmp)
                       and 'bias' not in tmp and 'other' not in tmp]
            for dirg in dirname:
                print('copy Zero to ' + path + os.sep + dirg)
                shutil.copyfile(path + os.sep + 'bias' + os.sep + 'Zero.fits',
                                path + os.sep + dirg + os.sep + 'Zero.fits')
        else:
            print('no spec_bias.lst in ' + os.getcwd())
    else:
        print('no bias dir in ' + os.getcwd())


if __name__ == '__main__':
    main()
