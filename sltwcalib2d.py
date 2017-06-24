#!/usr/bin/env python

import re
import os
from pyraf import iraf

def identify():
    iraf.twodspec()
    iraf.longslit()
    iraf.identify(images = 'Lamp.fits', section = 'middle column', 
            database = 'database', coordlist = 'linelists$idhenear.dat', 
            nsum = 10, match = -3.0, maxfeatures = 50, zwidth = 100.0, 
            ftype = 'emission', fwidth = 20.0, cradius = 7.0, threshold = 0.0, 
            minsep = 2.0, function = 'chebyshev', order = 6, sample = '*', 
            niterate = 0, low_reject = 3.0, high_reject = 3.0, grow = 0.0, 
            autowrite = 'no')

def reidentify():
    iraf.twodspec()
    iraf.longslit()
    iraf.reidentify(reference = 'Lamp', images = 'Lamp', interactive = 'no', 
            section = 'column', newaps = 'yes', override = 'yes', refit = 'yes', 
            trace = 'no', step = 10, nsum = 10, shift = 0.0, search = 0.0, 
            nlost = 5, cradius = 7.0, threshold = 0.0, addfeatures = 'no', 
            coordlist = 'linelists$idhenear.dat', match = -3.0, 
            maxfeatures = 50, minsep = 2.0, database = 'database')

def fitcoords():
    iraf.twodspec()
    iraf.longslit()
    iraf.fitcoords(images = 'Lamp', fitname = 'Lamp', interactive = 'yes', 
            combine = 'no', database = 'database', deletions = 'deletions.db', 
            function = 'chebyshev', xorder = 6, yorder = 6)

def transform(lst):
    f = open(lst)
    l = f.readlines()
    f.close()
    namelst = ['ftbo' + i for i in l]
    outputlst = ['wftbo' + i for i in l]
#    namelst = [i.split('.')[0] + 'otbf.fits' for i in l]
#    outputlst = [i.split('.')[0] + 'otbfw.fits' for i in l]
    f = open("temp1.txt", 'w')
    for i in namelst:
        f.write(i + '\n')
    f.close()
    f = open("temp2.txt", 'w')
    for i in outputlst:
        f.write(i + '\n')
    f.close()
    iraf.twodspec()
    iraf.longslit(dispaxis = 2)
    #for i in namelst:
    #    print '#' * 30, i, '===>', i.split('.')[0] + 'w.fits'
    #    iraf.transform(input = i, output = i.split('.')[0] + 'w.fits', 
    #            minput = '', moutput = '', fitnames = 'LampLamp', 
    #            database = 'database', interptype = 'spline3', 
    #            flux = 'yes')
    iraf.transform(input = '@temp1.txt', output = '@temp2.txt', 
            minput = '', moutput = '', fitnames = 'LampLamp', 
            database = 'database', interptype = 'spline3', 
            flux = 'yes')

def clear():
    print('remove wftbo*.fits')
    filelst = os.listdir('.')
    filelst = [i for i in filelst if re.match('^wftboYF.+\.fits', i) != None]
    for name in filelst:
        print('remove ' + name)
        os.remove(name)
    

def main():
    clear()
    corhalogenlst = 'cor_halogen.lst'

    identify()
    reidentify()
    fitcoords()
    transform(corhalogenlst)

if __name__ == "__main__":
    main()
