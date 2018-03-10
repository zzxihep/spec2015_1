#!/usr/bin/env python

import os
from astropy.io import fits as pyfits
import numpy as np
from pyraf import iraf


def combine_lamp(lstfile):
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    iraf.imcombine(input='%ftbo%ftbo%@' + lstfile,
                   output=lstfile.replace('.lst', ''), combine='sum',
                   reject='none')


def wal(lstfile, lampname):
    iraf.noao()
    iraf.twodspec()
    iraf.longslit()
   # iraf.identify(images = 'Lamp.fits', section = 'middle column',
   #     database = 'database', coordlist = 'linelists$idhenear.dat',
   #     nsum = 10, match = -3.0, maxfeatures = 50, zwidth = 100.0,
   #     ftype = 'emission', fwidth = 20.0, cradius = 7.0, threshold = 0.0,
   #     minsep = 2.0, function = 'chebyshev', order = 6, sample = '*',
   #     niterate = 0, low_reject = 3.0, high_reject = 3.0, grow = 0.0,
   #     autowrite = 'no')

    #    iraf.reidentify(reference = 'Lamp', images = 'Lamp', interactive = 'no',
    #            section = 'column', newaps = 'yes', override = 'yes', refit = 'yes',
    #            trace = 'no', step = 10, nsum = 10, shift = 0.0, search = 0.0,
    #            nlost = 5, cradius = 7.0, threshold = 0.0, addfeatures = 'no',
    #            coordlist = 'linelists$idhenear.dat', match = -3.0,
    #            maxfeatures = 50, minsep = 2.0, database = 'database')

    iraf.identify(images=lampname, section='middle column',
                  database='database', coordlist='linelists$idhenear.dat',
                  units='', nsum=10, match=-3.0, maxfeatures=50, zwidth=100.0,
                  ftype='emission', fwidth=20.0, cradius=7.0, threshold=0.0,
                  minsep=2.0, function='chebyshev', order=6, sample='*',
                  niterate=0, low_reject=3.0, high_reject=3.0, grow=0.0,
                  autowrite=False, graphics='stdgraph', cursor='', crval='',
                  cdelt='')
    iraf.reidentify(reference=lampname, images=lampname, interactive='no',
                    section='column', newaps=True, override=True, refit=True,
                    trace=False, step=10, nsum=10, shift=0.0, search=0.0,
                    nlost=5, cradius=7.0, threshold=0.0, addfeatures=False,
                    coordlist='linelists$idhenear.dat', match=-3.0,
                    maxfeatures=50, minsep=2.0, database='database',
                    logfiles='logfile', plotfile='', verbose=False,
                    graphics='stdgraph', cursor='', answer='yes', crval='',
                    cdelt='', mode='al')
    iraf.fitcoords(images=lampname, fitname=lampname, interactive=True,
                   combine=False, database='database',
                   deletions='deletions.db', function='chebyshev', xorder=6,
                   yorder=6, logfiles='STDOUT,logfile', plotfile='plotfile',
                   graphics='stdgraph', cursor='', mode='al')
    iraf.longslit(dispaxis=2)
    iraf.transform(input='%ftbo%ftbo%@' + lstfile,
                   output='%wftbo%wftbo%@' + lstfile, minput='', moutput='',
                   fitnames=lampname + lampname, database='database',
                   interptype='spline3', flux=True)


def clear():
    filename = os.listdir(os.getcwd())
    filename = [tmp for tmp in filename if os.path.isfile(tmp) and
                ('lamp.fits' in tmp or (tmp[0:5] == 'wftbo' and tmp[-5:] == '.fits'))]
    for i in filename:
        print('remove ' + i)
        os.remove(i)


def classify_lamp():
    namelst = open('lamp.lst').readlines()
    namelst = [i.strip() for i in namelst]
    timelst = []
    altlst = []
    azmlst = []
    for fitname in namelst:
        fit = pyfits.open(fitname)
        sidminute = fit[0].header['LST'].split(':')
        sidminute = int(sidminute[0]) * 60.0 + \
            int(sidminute[1]) + float(sidminute[2]) / 60.0
        timelst.append(sidminute)  # local Sidereal time
        # Altitude Position of Telesocpe
        altlst.append(fit[0].header['ALTPOS'])
        azmlst.append(fit[0].header['AZMPOS'])  # Azimuth Position of Telesocpe
    namelst = np.array(namelst)
    timelst = np.array(timelst)
    arg = np.argsort(timelst)
    namelst = namelst[arg]
    timelst = timelst[arg]
    #diftime = timelst[1:]-timelst[:-1]
    #ind = np.where(diftime > 10)[0]+1
    subclass = []
    tmpclass = []
    for i in range(len(namelst)):
        if len(tmpclass) == 0:
            tmpclass.append([namelst[i], timelst[i]])
        elif timelst[i] - timelst[i - 1] < 10:
            tmpclass.append([namelst[i], timelst[i]])
        else:
            subclass.append(tmpclass)
            tmpclass = [[namelst[i], timelst[i]]]
    if len(tmpclass) > 0:
        subclass.append(tmpclass)
    corhalogen = open('cor_halogen.lst').readlines()
    corhalogen = [i.strip() for i in corhalogen]
    corlst = []
    for fitname in corhalogen:
        fit = pyfits.open(fitname)
        sidminute = fit[0].header['LST'].split(':')
        sidminute = int(sidminute[0]) * 60.0 + \
            int(sidminute[1]) + float(sidminute[2]) / 60.0 + 30
        corlst.append([fitname, sidminute])  # local Sidereal time
    ugly = []
    for i in range(len(subclass)):
        ugly.append([])
    for i in range(len(corlst)):
        ttime = 10000.0
        tind = 0
        for j in range(len(subclass)):
            if ttime > abs(corlst[i][1] - subclass[j][0][1]):
                ttime = abs(corlst[i][1] - subclass[j][0][1])
                tind = j
        ugly[tind].append(corlst[i])
    ret = []
    for i in range(len(subclass)):
        if len(ugly[i]) > 0:
            ret.append(subclass[i][0][0].replace('.fits', '') + 'lamp.lst')
            fil = open(subclass[i][0][0].replace(
                '.fits', '') + 'lamp.lst', 'w')
            for j in range(len(subclass[i])):
                fil.write(subclass[i][j][0] + '\n')
            fil.close()
            fil = open(subclass[i][0][0].replace(
                '.fits', '') + 'cor_halogen.lst', 'w')
            for j in range(len(ugly[i])):
                fil.write(ugly[i][j][0] + '\n')
            fil.close()
    return ret


def main():
    clear()
    lst = os.listdir('.')
    lst = classify_lamp()
    for name in lst:
        combine_lamp(name)
        wal(name.replace('lamp.lst', 'cor_halogen.lst'), name.replace('.lst', ''))
        # combine_lamp('lamp.lst')
        # wal('cor_halogen.lst')


if __name__ == '__main__':
    main()
