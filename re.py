#! /usr/bin/env python

import os
from pyraf import iraf

def main():
    dirname = os.listdir(os.getcwd())
    dirname = [tmp for tmp in dirname if os.path.isdir(tmp) and \
            'bias' not in tmp and 'other' not in tmp]
    path = os.getcwd()
    for i in dirname:
        os.chdir(i)
        iraf.flpr()
        realwork()
        os.chdir(path)

if __name__ == '__main__':
    main()
