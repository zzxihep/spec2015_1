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

def gen_biaslst():
    fitname = os.listdir(os.getcwd() + os.sep + 'bias')
    fitname = [i for i in fitname if i[-5:] == '.fits']
    if len(fitname) > 0:
        path = os.getcwd()
        path = path + os.sep + 'bias' + os.sep
        f = open(path + 'spec_bias.lst', 'w')
        for i in fitname:
            print(i + ' === > spec_bias.lst')
            f.write(path + i + '\n')
        f.close()
    else:
        print('no bias found')

def gen_otherlst(path):
    fitname = os.listdir(path)
    fitname = [i for i in fitname if i[-5:] == '.fits' and i[0:2] == 'YF']
    f = open('all.lst','w')
    for i in fitname:
        f.write(i + '\n')
    f.close()
    halogen = []
    cor_halogen = []
    lamp = []
    cor_lamp = []
    obj = []
    std = []
    for i in fitname:
        fit = pyfits.open(i)
        name = fit[0].header['object'].lower()
        fit.close()
        if 'halogen' in name:
            halogen.append(i)
        else:
            cor_halogen.append(i)
            if 
    halogenf = open('halogen.lst','w')
    cor_halogenf = open('cor_halogen.lst','w')
    lampf = open('lamp.lst','w')
    cor_lampf = open('cor_lamp.lst','w')
    objf = open('obj.lst','w')
    stdf = open('std.lst','w')
    

def main():
    gen_biaslst()
    path = os.getcwd()
    dirname = os.listdir(path)
    dirname = [i for i in dirname if os.path.isdir(i) and 'bias' not in i \
            and 'other' not in i]
    for i in dirname:
        gen_otherlst(path + os.sep + i + os.sep)
