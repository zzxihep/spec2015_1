#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
separate fits file by whether type bias, and grism, slit.
"""

import os
import glob
import shutil
import func


def main():
    """
    Assume current dir = spec/
    separate fits file by type bias, grism, slit.
    """
    namelst = glob.glob('Y*.fits')
    if not os.path.isdir('bias'):
        os.mkdir('bias')
    for name in namelst:
        if func.is_bias(name):
            print 'mv %s bias/' % name
            shutil.move(name, 'bias'+os.sep+name)
        else:
            dirname = func.get_grism(name)+'_'+func.get_slit(name)
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            print 'mv %s %s' % (name, dirname)
            shutil.move(name, dirname+os.sep+name)


if __name__ == '__main__':
    main()
