#!/usr/bin/env python

import os
from astropy.io import fits
from pyraf import iraf
import func


def combinelamp(lst):
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    iraf.imcombine(input='%ftbo%ftbo%@' + lst, output='Lamp', combine='sum',
                   reject='none')


def get_edge(filename):
    fit = fits.open(filename)
    keyword = fit[0].header['YGRNM']
    print(keyword)
    if keyword.strip().lower() == 'grism 14':
        return 1300
    elif keyword.strip().lower() == 'grism 3':
        return 700
    elif keyword.strip().lower() == 'grism 8':
        return 1500
    else:
        print("can't find the edge of Helium and Neon fits in lamp")


def combine_fit(namelst):
    fit = fits.open(namelst[0])
    for name in namelst[1:]:
        tf = fits.open(name)
        fit[0].data = fit[0].data + tf[0].data
    fit[0].data = fit[0].data / float(len(namelst))
    return fit


def combinelamp2(lstfn):
    print('run combinelamp')
    namelst = ['ftbo'+i.strip() for i in open(lstfn).readlines()]
    if func.get_grism(namelst[0]).lower() == 'grism_8':
        combinelamp(lstfn)
        return
    Helst, Nelst, HeNelst = [], [], []
    for name in namelst:
        if func.is_Helium(name):
            if func.is_Neon(name):
                print 'HeNelst <--- '+name
                HeNelst.append(name)
            else:
                print 'Helst <--- '+name
                Helst.append(name)
        elif func.is_Neon(name):
            print 'Nelst <--- '+name
            Nelst.append(name)
    if len(Helst) == 0 or len(Nelst) == 0:
        combinelamp(lstfn)
    else:
        edge = get_edge(namelst[0])
        print('edge = %d' % edge)
        Hefit = combine_fit(Helst+HeNelst)
        Nefit = combine_fit(Nelst+HeNelst)
        Hefit[0].data[edge:, :] = Nefit[0].data[edge:, :]
        Hefit.writeto('Lamp.fits')


def clear():
    if os.path.isfile('Lamp.fits'):
        print('remove Lamp.fits')
        os.remove('Lamp.fits')


def main():
    lamplst = 'lamp.lst'
    clear()
    combinelamp2(lamplst)
    # combinelamp(lamplst)


if __name__ == '__main__':
    main()
