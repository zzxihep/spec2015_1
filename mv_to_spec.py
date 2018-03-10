#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: zhixiang zhang <zzx>
# @Date:   08-Jan-2017
# @Email:  zhangzx@ihep.ac.cn
# @Filename: mv_to_spec.py
# @Last modified by:   zzx
# @Last modified time: 27-Jun-2017

import re
import os
import glob
import shutil
from astropy.io import fits as pyfits
from func import is_spec


def main():
    """
    mv spec file from current dir to spec/
    if dir spec not exist, mkdir spec.
    """
    if not os.path.isdir('spec'):
        print('mkdir spec')
        os.mkdir('spec')
    ifitsname = os.listdir(os.getcwd())
    ifitsname = glob.glob('Y*.fits')
    fitsnames = [i for i in ifitsname if os.path.isfile(i) and
                 re.match("^Y[A-Z].+[a-l][\d]{6}\\.fits$", i) is not None]
    for i in fitsnames:
        if is_spec(i):
            fits = pyfits.open(i)
            hdr = fits[1].header
            naxis1 = pyfits.getval(i, 'NAXIS1', 1)
            naxis2 = pyfits.getval(i, 'NAXIS2', 1)
            if naxis1 == 2148 and naxis2 == 4612:
                print('mv %s to spec/' % i)
                shutil.move(i, '.'+os.sep+'spec'+os.sep+i)


if __name__ == "__main__":
    main()
