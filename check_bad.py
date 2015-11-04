#! /usr/bin/env python

import os
import pyfits
import numpy as np

def check_bias():
    if not os.path.isdir(os.getcwd()):
        print('no bias dir in ' + os.getcwd())
        return False
    if not os.path.isfile(os.getcwd() + os.sep + 'bias' + os.sep + 'spec_bias.lst'):
        print('no spec_bias.lst in ' + os.getcwd() + os.sep + 'bias')
        return False
    os.chdir('bias')
    f = open('spec_bias.lst')
    fitlst = f.readlines()
    f.close()
    fitlst = [tmp.split('\n')[0] for tmp in fitlst]
    goodlst= []
    print('filename mean std linemax linemin colmax colmin')
    for i in fitlst:
        fit  = pyfits.open(i)
        mean = fit[1].data.mean()
        std  = fit[1].data.std()
        linedata = fit[1].data.mean(axis=0)
        coldata  = fit[1].data.mean(axis=1)
        linemax  = linedata.max()
        linemin   = linedata.min()
        colmax   = coldata.max()
        colmin   = coldata.min()
        flag = True
        if mean < 20120-30 or mean > 20120+30:
            print('mean of %s = %.2f out of range(20090 - 20150)' % (i, mean))
            flag = False
        if std > 50:
            print('std of %s = %.2f out of range(50)' % (i, std))
            flag = False
        if linemax > mean + 200:
            print('linemax of %s = %.2f out of range %.2f + 200. may be it is a bad line' \
                    % (i, linemax, mean))
            flag = False
        if linemin < mean - 200:
            print('linemin of %s = %.2f out of range %.2f - 200. may be it is a bad line' \
                    % (i, linemin, mean))
            flag = False
        if colmax > mean + 200:
            print('colmax of %s = %.2f out of range %.2f + 200. may be it is a bad col' \
                    % (i, colmax, mean))
            flag = False
        if colmin < mean - 200:
            print('colmin of %s = %.2f out of range %.2f - 200. may be it is a bad col' \
                    % (i, colmin, mean))
            flag = False
        print('%s  %.2f  %.2f  %.2f  %.2f  %.2f  %.2f' \
                % (i, mean, std, linemax, linemin, colmax, colmin))
        if flag == True:
            goodlst.append(i)
    if len(goodlst) == 0:
        print('no bias file up to standard, abort')
        dirname, filename = os.path.split(os.getcwd())
        os.chdir(dirname)
        os._exit(1)
    if len(goodlst) < len(fitlst):
        f = open('spec_bias.lst','w')
        for name in goodlst:
            f.write(name + '\n')
        f.close()
    dirname, filename = os.path.split(os.getcwd())
    os.chdir(dirname)
    return True

def check_halogen(abspathfile):
    """Detect whether beyond the linear region"""
    path, filename = os.path.split(abspathfile)
    f = open(abspathfile)
    fitlst = f.readlines()
    f.close()
    fitlst = [tmp.split('\n')[0] for tmp in fitlst]
    goodlst = []
    for i in fitlst:
        flag = True
        fit = pyfits.open(path + os.sep + i)
        xx,yy = fit[1].data.shape
        yy = yy / 2
        center= fit[1].data[1500:xx,yy-50:yy+50].mean(axis=1)
        maxindex = center.argmax()
        print('%s(maxindex, val) %d %.2f' % (i, maxindex+1500, center[maxindex]))
        if center[maxindex] > 280000. or center[maxindex] < 150000.:
            frome = (0 if maxindex - 30 < 0 else maxindex - 30)
            toe   = (xx-1 if maxindex+30 > xx-1 else maxindex+30)
            maxpart = center[frome:toe]
            if len(np.where(maxpart > 250000.)) > len(maxpart)/2:
                print('the max val in %s > 280000 %.3f' % (i, center[maxindex]))
                flag = False
            if len(np.where(maxpart < 100000.)) > len(maxpart)/2:
                print('the max val in %s < 150000 %.3f' % (i, center[maxindex]))
                flag = False
        if flag == True:
            goodlst.append(i)
    if len(goodlst) == 0:
        getval = raw_input('no halogen file up to standard, are you want delete the halogen \
                fits(d), only delete halogen.lst(h), do nothing(n or Enter)')
        if getval == d:
            for i in fitlst:
                print('remove ' + path + os.sep + i)
                os.remove(path + os.sep + i)
            print('remove ' + abspathfile)
            os.remove(abspathfile)
        elif getval == h:
            print('remove ' + abspathfile)
            os.remove(abspathfile)
        else:
            pass
    if len(goodlst) < len(fitlst):
        f = open(abspathfile, 'w')
        for i in goodlst:
            f.write(i + '\n')

def check_other(path):
    """Only check halogen"""
    abshalogenpath = os.getcwd() + os.sep + path + os.sep + 'halogen.lst'
    if os.path.isfile(abshalogenpath):
        print('check halogen ' + path)
        check_halogen(abshalogenpath)
    else:
        print('no halogen.lst in %s abort' % path)
        os._exit()

def main():
    print('check bias')
    check_bias()
    dirname = os.listdir(os.getcwd())
    dirname = [i for i in dirname if os.path.isdir(i) and 'bias' not in i and 'other' not in i]
    for i in dirname:
        check_other(i)

if __name__ == '__main__':
    main()
