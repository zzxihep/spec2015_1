#!/usr/bin/env python
# -*- encoding=utf-8 -*-

# @Author: zhixiang zhang <zzx>
# @Date:   26-Jun-2017
# @Email:  zhangzx@ihep.ac.cn
# @Filename: gen_lst.py
# @Last modified by:   zzx
# @Last modified time: 01-Jul-2017

"""
Generate lst file for different fits type.
the lst file include :
    spec_bias.lst
    all.lst
    halogen.lst
    cor_halogen.lst
    lamp.lst
    cor_lamp.lst
    std.lst
    cor_std.lst
"""

import os
import glob
import pyfits
from termcolor import colored
import func


def gen_lst(namelst, ynfun, outname):
    """
    generate a lst file in current dir, the file name = outname.
    If outname already exist, this function will delete the old.
    namelst : fits name list, ['1.fits', '2.fits', '3.fits']
    type : string list
    ynfun : function to check filename in namelst, receive a string parameter,
        return a boolean value. If value yes, the filename will be accepted.
    type : function
    return : accepted filename list
    type : string list
    """
    if os.path.isfile(outname):
        os.remove(outname)
    newnamelst = []
    for name in namelst:
        if ynfun(name):
            newnamelst.append(name)
    if newnamelst == []:
        print colored('no file name write to '+outname, 'red')
    else:
        fil = open(outname, 'w')
        for name in newnamelst:
            objvalue = pyfits.getval(name, 'OBJECT')
            print '%s  --->  %-16s  %s' % (name, outname, objvalue)
            fil.write(name+'\n')
        fil.close()
    return newnamelst


def main():
    """
    Assume current dir = spec/
    """
    if os.path.isdir('bias'):
        print 'cd bias/'
        os.chdir('bias')
        namelst = glob.glob('YF*.fits')
        namelst.sort()
        gen_lst(namelst=namelst, ynfun=func.is_bias, outname='spec_bias.lst')
        print 'cd ..'
        os.chdir('..')
    else:
        print colored('no bias dir found', 'red')

    dirlst = os.listdir('.')
    dirlst = [i for i in dirlst if os.path.isdir(i) and
              i != 'bias' and i != 'other']
    for mdir in dirlst:
        print 'cd '+mdir
        os.chdir(mdir)
        namelst = glob.glob('YF*.fits')
        namelst.sort()
        gen_lst(namelst, lambda x: True, outname='all.lst')
        halogen_lst = gen_lst(namelst, func.is_halogen, 'halogen.lst')
        namelst = sorted(list(set(namelst)-set(halogen_lst)))
        gen_lst(namelst, lambda x: not func.is_halogen(x), 'cor_halogen.lst')
        lamplst = gen_lst(namelst, func.is_lamp, 'lamp.lst')
        namelst = sorted(list(set(namelst)-set(lamplst)))
        gen_lst(namelst, lambda x: not func.is_lamp(x), 'cor_lamp.lst')
        standlst = gen_lst(namelst, func.is_std, 'std.lst')
        namelst = sorted(list(set(namelst)-set(standlst)))
        gen_lst(namelst, lambda x: not func.is_std(x), 'cor_std.lst')
        print 'cd ..'
        os.chdir('..')


if __name__ == '__main__':
    main()
