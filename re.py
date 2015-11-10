#! /usr/bin/env python

import os
from pyraf import iraf
import cor_ftbo
import wcal2d
import re_apall
import re_corflux

def main():
    dirname = os.listdir(os.getcwd())
    dirname = [tmp for tmp in dirname if os.path.isdir(tmp) and \
            'bias' not in tmp and 'other' not in tmp]
    path = os.getcwd()
    for i in dirname:
        os.chdir(path + os.sep + i)
	print('current dir : ' + os.getcwd())
        iraf.flpr()
	cor_ftbo.main()
	wcal2d.main()
	re_apall.main()
	re_corflux.main()
        os.chdir(path)

if __name__ == '__main__':
    main()
