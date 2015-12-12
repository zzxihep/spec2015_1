#!/usr/bin/env python

import os
import pyfits
from pyraf import iraf
from filedict import filedict

def findmarkfit(dirpath):
    print('current dir ' + dirpath)
    dirlst = os.listdir(dirpath)
    ret = []
    for i in dirlst:
        name = dirpath + os.sep + i
        if os.path.isdir(name):
            ret = ret + findmarkfit(name)
        else:
            if i[0:5] == 'mark_' and i[-5:] == '.fits':
                ret.append(name)
    return ret

def main():
    print('FLAG 1================')
    checkfilepath = os.path.split(os.path.abspath(__file__))[0] + os.sep + 'objcheck.lst'
    dct = filedict(checkfilepath)
    fitlst = findmarkfit(os.getcwd())
    for fitname in fitlst:
        print(fitname)
    for fitname in fitlst:
        fit = pyfits.open(fitname)
        oldsname = fit[0].header['sname']
        newsname = dct[str(oldsname)]
        iraf.hedit(images = fitname, fields = 'sname',
                value = newsname, add = 'yes', delete = 'no',
                verify = 'no', show = 'yes', update = 'yes')

if __name__ == '__main__':
    main()
