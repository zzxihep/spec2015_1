#!/usr/bin/env python

import os,sys
import pyfits

def get_standard_lst():
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    filename = dirname + os.sep + 'standard.lst'
    f = open(filename)
    l = f.readlines()
    f.close()
    l = [i.split('\n')[0] for i in l]
    l = [i.split() for i in l]
    return l

standardlst = get_standard_lst()
standardlst = [tmp[0] for tmp in standardlst]

def is_std(object_val):
    name = object_val.lower()
    for i in standardlst:
        if i in name:
            return True
    return False

def gen_biaslst():
    biaspath = os.getcwd() + os.sep + 'bias'
    fitname = []
    if os.path.isdir(biaspath):
        fitname = os.listdir(biaspath)
    fitname = [i for i in fitname if os.path.isfile(os.getcwd() + os.sep + \
            'bias' + os.sep + i) and i[0:2] == 'YF' and i[-5:] == '.fits']
    if len(fitname) > 0:
        fitname.sort()
        path = os.getcwd()
        path = path + os.sep + 'bias' + os.sep
        f = open(path + 'spec_bias.lst', 'w')
        for i in fitname:
            print(i + ' ---> spec_bias.lst')
            f.write( i + '\n')
        f.close()
    else:
        print('no bias found')

def gen_otherlst(path):
    fitname = []
    if os.path.isdir(path):
        fitname = os.listdir(path)
    fitname = [i for i in fitname if i[-5:] == '.fits' and i[0:2] == 'YF']
    if len(fitname) > 0:
        f = open(path + 'all.lst','w')
        for i in fitname:
            f.write(i + '\n')
        f.close()
    halogen = []
    cor_halogen = []
    lamp = []
    cor_lamp = []
    std = []
    cor_std = []
    for i in fitname:
        fit = pyfits.open(path + i)
        name = fit[0].header['object'].lower()
        if 'halogen' in name:
            print(i + ' : ' + name + ' ---> halogen.lst')
            halogen.append(i)
        else:
            print(i + ' : ' + name + ' ---> cor_halogen.lst')
            cor_halogen.append(i)
            if fit[0].header['CLAMP2'] == 1 or fit[0].header['CLAMP3'] == 1 \
                    or fit[0].header['CLAMP4'] == 1:
                print(i + ' : ' + name + ' ---> lamp.lst')
                lamp.append(i)
            else:
                print(i + ' : ' + name + ' ---> cor_lamp.lst')
                cor_lamp.append(i)
                if is_std(name):
                    print(i + ' : ' + name + ' ---> std.lst')
                    std.append(i)
                else:
                    print(i + ' : ' + name + ' ---> cor_std.lst')
                    cor_std.append(i)
        fit.close()
    if len(halogen) > 0:
        halogen.sort()
        f = open(path + 'halogen.lst','w')
        for name in halogen:
            f.write(name + '\n')
        f.close()
    if len(cor_halogen) > 0:
        cor_halogen.sort()
        f = open(path + 'cor_halogen.lst','w')
        for name in cor_halogen:
            f.write(name + '\n')
        f.close()
    if len(lamp) > 0:
        lamp.sort()
        f = open(path + 'lamp.lst','w')
        for name in lamp:
            f.write(name + '\n')
        f.close()
    if len(cor_lamp) > 0:
        cor_lamp.sort()
        f = open(path + 'cor_lamp.lst','w')
        for name in cor_lamp:
            f.write(name + '\n')
        f.close()
    if len(std) > 0:
        std.sort()
        f = open(path + 'std.lst','w')
        for name in std:
            f.write(name + '\n')
        f.close()
    if len(cor_std) > 0:
        cor_std.sort()
        f = open(path + 'cor_std.lst','w')
        for name in cor_std:
            f.write(name + '\n')
        f.close()
    

def main():
    gen_biaslst()
    path = os.getcwd()
    dirname = os.listdir(path)
    dirname = [i for i in dirname if os.path.isdir(i) and 'bias' not in i \
            and 'other' not in i]
    for i in dirname:
        gen_otherlst(path + os.sep + i + os.sep)

if __name__ == '__main__':
    main()
