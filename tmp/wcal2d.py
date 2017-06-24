#!/usr/bin/env python

import os
from pyraf import iraf

def combine_lamp(lstfile):
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    iraf.imcombine(input = '%ftbo%ftbo%@'+lstfile
        , output = 'Lamp', combine = 'sum', reject = 'none')

def wal(lstfile):
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

















    iraf.identify(images = 'Lamp'
        , section = 'middle column', database = 'database'
        , coordlist = 'linelists$idhenear.dat', units = '', nsum = 10
        , match = -3.0, maxfeatures = 50, zwidth = 100.0
        , ftype = 'emission', fwidth = 20.0, cradius = 7.0
        , threshold = 0.0, minsep = 2.0, function = 'chebyshev'
        , order = 6, sample = '*', niterate = 0
        , low_reject = 3.0, high_reject = 3.0, grow = 0.0
        , autowrite = False, graphics = 'stdgraph', cursor = ''
        , crval = '', cdelt = '')
    iraf.reidentify(reference = 'Lamp'
        , images = 'Lamp', interactive = 'no', section = 'column'
        , newaps = True, override = True, refit = True, trace = False
        , step = 10, nsum = 10, shift = 0.0, search = 0.0, nlost = 5
        , cradius = 7.0, threshold = 0.0, addfeatures = False
        , coordlist = 'linelists$idhenear.dat', match = -3.0, maxfeatures = 50
        , minsep = 2.0, database = 'database', logfiles = 'logfile'
        , plotfile = '', verbose = False, graphics = 'stdgraph', cursor = ''
        , answer = 'yes', crval = '', cdelt = '', mode = 'al')
    iraf.fitcoords(images = 'Lamp'
        , fitname = 'Lamp', interactive = True, combine = False, database = 'database'
        , deletions = 'deletions.db', function = 'chebyshev', xorder = 6
        , yorder = 6, logfiles = 'STDOUT,logfile', plotfile = 'plotfile'
        , graphics = 'stdgraph', cursor = '', mode = 'al')
    iraf.longslit(dispaxis = 2)
    iraf.transform(input = '%ftbo%ftbo%@' + lstfile
        , output = '%wftbo%wftbo%@' + lstfile, minput = '', moutput = ''
        , fitnames = 'LampLamp', database = 'database', interptype = 'spline3'
        , flux = True)

def clear():
    filename = os.listdir(os.getcwd())
    filename = [tmp for tmp in filename if os.path.isfile(tmp) and \
            (tmp == 'Lamp.fits' or (tmp[0:5] == 'wftbo' and tmp[-5:] == '.fits'))]
    for i in filename:
        print('remove ' + i)
        os.remove(i)

def main():
    clear()
    combine_lamp('lamp.lst')
    wal('cor_halogen.lst')

if __name__ == '__main__':
    main()
