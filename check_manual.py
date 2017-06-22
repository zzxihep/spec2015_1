#! /usr/bin/env python

import os
import pyfits
#import numpy as np
from pyraf import iraf
#import matplotlib.pyplot as plt
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

#def check_out_val(path):
#    if os.path.isdir(path):
#        os.chdir(path)
#        if os.path.isfile('cor_lamp.lst'):
#            l = [i for i in file('cor_lamp.lst')]
#            num = len(l)
#            os.system('gedit cor_lamp.lst &')
#            for fitname in l:
#                fit = pyfits.open(fitname)
#                fitdata = fit[1].data
#                fitdata = fitdata * 2.0
#                fitdata[np.where(fitdata < 560000.0)] = 0.0
#                plt.imshow(fitdata)
#                plt.colorbar()
#                plt.title(fitname + ' ' + fit[0].header['object'])
#                plt.show()
#        os.chdir(os.path.split(os.getcwd())[0])


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
#        check_out_val(i)

if __name__ == '__main__':
    main()
    #check_other(os.getcwd())
