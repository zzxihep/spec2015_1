#! /usr/bin/env python

import os
import glob
from astropy.io import fits as pyfits
from pyraf import iraf
import func


def get_trim_sec():
    path = func.config_path
    print('the script path is ' + path)
    f = open(path + os.sep + 'trim.lst')
    lst = f.readlines()
    f.close()
    lst = [i.split() for i in lst]
    dirlst = os.listdir(os.getcwd())
    fitname = ''
    for name in dirlst:
        if name[0:2] == 'YF' and name[-5:] == '.fits':
            fit = pyfits.open(name)
            if 'bias' not in fit[0].header['OBJECT'].lower():
                fitname = name
    fit = pyfits.open(fitname)
    hdr = fit[0].header
    curdirname = (hdr['YGRNM'] + '_' + hdr['YAPRTNM']).replace(' ', '_')
    # curdirname = os.path.split(os.getcwd())[1]
    for i in lst:
        if i[0] == curdirname:
            return (i[1], i[2], i[3], i[4])
    print('cann\'t find trim sec')


def coroverbiastrim(lstfile):
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    x1, x2, y1, y2 = get_trim_sec()
    iraf.ccdproc(images='@'+lstfile+'//[1]', output='%bo%bo%@'+lstfile,
                 ccdtype='', max_cache=0, noproc=False, fixpix=False,
                 overscan=True, trim=False, zerocor=True, darkcor=False,
                 flatcor=False, illumcor=False, fringecor=False, readcor=False,
                 scancor=False, readaxis='line', fixfile='',
                 biassec='[5:45,%s:%s]' % (y1, y2),
                 trimsec='[%s:%s,%s:%s]' % (x1, x2, y1, y2), zero='Zero',
                 dark='', flat='', illum='', fringe='', minreplace=1.0,
                 scantype='shortscan', nscan=1, interactive=False,
                 function='chebyshev', order=1, sample='*', naverage=1,
                 niterate=1, low_reject=3.0, high_reject=3.0, grow=1.0)
    iraf.ccdproc(images='%bo%bo%@'+lstfile, output='%tbo%tbo%@'+lstfile,
                 ccdtype='', max_cache=0, noproc=False, fixpix=False,
                 overscan=False, trim=True, zerocor=False, darkcor=False,
                 flatcor=False, illumcor=False, fringecor=False, readcor=False,
                 scancor=False, readaxis='line', fixfile='',
                 biassec='[5:45,%s:%s]' % (y1, y2),
                 trimsec='[%s:%s,%s:%s]' % (x1, x2, y1, y2), zero='Zero',
                 dark='', flat='', illum='', fringe='', minreplace=1.0,
                 scantype='shortscan', nscan=1, interactive=False,
                 function='chebyshev', order=1, sample='*', naverage=1,
                 niterate=1, low_reject=3.0, high_reject=3.0, grow=1.0)
    iraf.flpr()


def combine_flat(lstfile):
    if os.path.isfile('Halogen.fits'):
        print 'remove Halogen.fits'
        os.remove('Halogen.fits')
    if os.path.isfile('Resp.fits'):
        print 'remove Resp.fits'
        os.remove('Resp.fits')
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    iraf.flatcombine(input='tbo//@'+lstfile, output='Halogen',
                     combine='average', reject='crreject', ccdtype='',
                     process=False, subsets=False, delete=False, clobber=False,
                     scale='mode', statsec='', nlow=1, nhigh=1, nkeep=1,
                     mclip=True, lsigma=3.0, hsigma=3.0, rdnoise='rdnoise',
                     gain='gain', snoise=0.0, pclip=-0.5, blank=1.0)
    iraf.twodspec()
    iraf.longslit(dispaxis=2, nsum=1, observatory='Lijiang',
                  extinction=func.config_path +os.sep+ 'LJextinct.dat',
                  caldir=func.std_path+os.sep,
                  interp='poly5')
    iraf.response(calibration='Halogen', normalization='Halogen',
                  response='Resp', interactive=True, threshold='INDEF',
                  sample='*', naverage=1, function='spline3', order=25,
                  low_reject=10.0, high_reject=10.0, niterate=1, grow=0.0,
                  graphics='stdgraph', cursor='')


def corhalogen(lstfile):
    namelst = glob.glob('ftbo*.fits')
    for name in namelst:
        print 'remove ', name
        os.remove(name)
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    iraf.ccdproc(images='tbo@'+lstfile, output='%ftbo%ftbo%@'+lstfile,
                 ccdtype='', max_cache=0, noproc=False, fixpix=False,
                 overscan=False, trim=False, zerocor=False, darkcor=False,
                 flatcor=True, illumcor=False, fringecor=False, readcor=False,
                 scancor=False, readaxis='line', fixfile='', biassec='',
                 trimsec='', zero='Zero', dark='', flat='Resp', illum='',
                 fringe='', minreplace=1.0, scantype='shortscan', nscan=1,
                 interactive=False, function='chebyshev', order=1, sample='*',
                 naverage=1, niterate=1, low_reject=3.0, high_reject=3.0,
                 grow=1.0)
    iraf.flpr()


def clear():
    filename = os.listdir(os.getcwd())
    filename = [tmp for tmp in filename if os.path.isfile(tmp) and
                (tmp[0:5] == 'tboYF' or tmp[0:6] == 'ftboYF' or
                 tmp == 'Halogen.fits' or tmp == 'Resp.fits' or
                 tmp[0:4] == 'boYF')]
    for i in filename:
        print('remove ' + i)
        os.remove(i)


def add_DISPAXIS(filelst):
    iraf.hedit(images='@' + filelst + '[0]', fields='DISPAXIS',
               value='2', addonly='Yes', delete='No', verify='No', show='Yes', update='Yes')


def main():
    clear()
    print('=' * 20 + ' correct trim bias overscan ' + '=' * 20)
    add_DISPAXIS('all.lst')
    coroverbiastrim('all.lst')
    print('=' * 20 + ' correct flat ' + '=' * 20)
    combine_flat('halogen.lst')
    corhalogen('cor_halogen.lst')


if __name__ == '__main__':
    main()
