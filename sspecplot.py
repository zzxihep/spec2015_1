#!/usr/bin/env python

import os
from astropy.io import fits as pyfits
import numpy as np
import matplotlib.pyplot as plt

ssglobfilename = []

def sspecplot(filename):
    fit = pyfits.open(filename)
    ape = 0
    ape2= -1
    if 'APNUM1' in fit[0].header:
        ape = int(fit[0].header['APNUM1'].split()[0]) - 1
        if 'APNUM2' in fit[0].header:
            ape2= int(fit[0].header['APNUM2'].split()[0]) - 1
    num = fit[0].data.shape[1]
    y = fit[0].data[0][ape]# + 2500
    y2= fit[0].data[1][ape]
    z = []
    z2= []
    if ape2 >= 0:
        z = fit[0].data[0][ape2]
        z2= fit[0].data[1][ape2]
    length = len(y)
    begin = fit[0].header['CRVAL1']
    step  = fit[0].header['CD1_1']
    print('begin from ' + str(begin))
    print('step is ' + str(step))
    x = np.linspace(begin, begin+length*step,
    		length, endpoint = False)
    print('end ' + str(x[-1]))
    plt.ion()
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1,1,1)
    ax1.plot(x,y,color='red')
    ax1.plot(x,y2)
    if ape2 >= 0:
        fig2 = plt.figure()
        ax2  = fig2.add_subplot(1,1,1)
        ax2.plot(x,z,color='red')
        ax2.plot(x,z2)
    objname = fit[0].header['OBJECT'].split()[0]
    objname = objname.split('_')[0].lower()
    if len(ssglobfilename) > 0:
        for tfilename in ssglobfilename:
            if tfilename != filename:
                nfit = pyfits.open(tfilename)
                if objname in nfit[0].header['OBJECT'].lower():
                    y = nfit[0].data[0][ape]
                    y2= nfit[0].data[1][ape]
                    z = []
                    z2= []
                    if ape2 >= 0:
                        z = nfit[0].data[0][ape2]
                        z2= nfit[0].data[1][ape2]
                    length = len(y)
                    begin = nfit[0].header['CRVAL1']
                    step  = nfit[0].header['CD1_1']
                    print('begin from ' + str(begin))
                    print('step is ' + str(step))
                    x = np.linspace(begin, begin+length*step, length, endpoint = False)
                    print('end ' + str(x[-1]))
                    ax1.plot(x,y,color='red')
                    ax1.plot(x,y2)
                    if ape2 >= 0:
                        ax2.plot(x,z,color='red')
                        ax2.plot(x,z2)
    if filename not in ssglobfilename:
        ssglobfilename.append(os.getcwd()+os.sep+filename)
#    plt.plot(x,y, color = 'red')
#    plt.plot(x,y2, color = 'green')
    plt.show()
