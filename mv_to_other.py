#!/usr/bin/env python

"""
mv useless dir to other/ dir
"""
import os
import glob
import shutil
import func


def has_obj(namelst):
    """
    To find if there are obj fits in namelst.
    If any obj fits, return True, else return False.
    namelst : fits name list, ['1.fits', '2.fits', '3.fits']
    type : string list
    return : True or False
    type : boolean
    """
    for name in namelst:
        if func.is_bias(name) or func.is_halogen(name) or \
           func.is_lamp(name) or func.is_std(name):
            pass
        else:
            return True
    return False


def main():
    """
    Assume current dir = spec/
    mv useless dir(no obj fits) to other/
    """
    odirname = 'other'
    dirlst = os.listdir('.')
    dirlst = [i for i in dirlst if os.path.isdir(i) and
              i != 'bias' and i != odirname]
    if not os.path.isdir(odirname):
        os.mkdir('other')
    for dirname in dirlst:
        os.chdir(dirname)
        namelst = glob.glob('Y*.fits')
        hasobj = has_obj(namelst)
        os.chdir('..')
        if not hasobj:
            print 'mv %s %s%s' % (dirname, odirname, os.sep)
            shutil.move(dirname, 'other'+os.sep+dirname)


if __name__ == '__main__':
    main()
