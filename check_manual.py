#! /usr/bin/env python

import os
from pyraf import iraf

def check_bias():
    biaspath = os.getcwd() + os.sep + 'bias'
    if os.path.isfile(biaspath + os.sep + 'spec_bias.lst'):
        os.chdir('bias')
        os.system('gedit spec_bias.lst &')
        iraf.imexamine(input = '@spec_bias.lst[1]', frame = 1)
        dirname, filename = os.path.split(os.getcwd())
        os.chdir(dirname)
        iraf.flpr()
    else:
        print('no bias dir in ' + os.getcwd())

def check_other(path):
    if os.path.isdir(path):
        os.chdir(path)
        lstlst = ['halogen.lst', 'lamp.lst', 'cor_lamp.lst','std.lst','cor_std.lst']
        for i in lstlst:
            if os.path.isfile(i):
                os.system('gedit %s &' % i)
                iraf.imexamine(input = '@%s[1]'%i, frame = 1)
        dirname, filename = os.path.split(os.getcwd())
        os.chdir(dirname)
        iraf.flpr()
    else:
        print('no dir ' + path + ' in ' + os.getcwd())

def main():
    path = os.getcwd()
    print('check bias')
    check_bias()
    dirname = os.listdir(os.getcwd())
    dirname = [i for i in dirname if os.path.isdir(i) and 'bias' not in i and 'other' not in i]
    print('check other')
    for i in dirname:
        print(i)
        check_other(i)

if __name__ == '__main__':
    main()
