#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil
import gen_lst
import glob

def find_lst(dirname,filename):
    path = os.getcwd()
    upper, spec = os.path.split(path)
    upper, curdate = os.path.split(upper)
    other_dir = os.listdir(upper)
    other_dir = [i for i in other_dir if os.path.isdir(upper + os.sep + i) and i < curdate]
    other_dir.sort(reverse = True)
    for i in other_dir:
        if os.path.isfile(upper + os.sep + i + os.sep + spec + os.sep \
                + dirname + os.sep + filename):
            return upper + os.sep + i + os.sep + spec + os.sep + dirname + os.sep + filename
        hope = upper + os.sep + i + os.sep + spec + os.sep + 'other' + os.sep + dirname + os.sep
        gen_lst.gen_otherlst(hope)
        if os.path.isfile(hope + filename):
            print('find ' + filename + ' in ' + hope)
            return hope + filename
    return ''

def copy_lst_and_fit(lst_path, topath):
    l = open(lst_path).readlines()
    l = [i.split('\n')[0] for i in l]
    frompath, lstname = os.path.split(lst_path)
    print('copy ' + lstname + ' from ' + frompath + ' to ' + topath)
    shutil.copyfile(frompath + os.sep + lstname, topath + os.sep + lstname)
    for name in l:
        print('copy ' + i + ' from ' + frompath + ' to ' + topath)
        shutil.copyfile(frompath + os.sep + name, topath + os.sep + name)

def check_bias():
    if not os.path.isdir('bias'):
        os.mkdir('bias')
    if not os.path.isfile(os.getcwd() + os.sep + 'bias' + os.sep + 'spec_bias.lst'):
        print('lack bias in ' + os.getcwd())
        lstpath = find_lst('bias','spec_bias.lst')
        if lstpath == '':
            print('cann\'t find spec_bias.lst')
            os._exit(1)
        else:
            copy_lst_and_fit(lstpath, os.getcwd() + os.sep + 'bias' + os.sep)

def check_other(dirname):
    lstname = glob.glob(os.getcwd() + os.sep + dirname + os.sep + '*.lst')
    stdlstname = ['halogen.lst', 'lamp.lst', 'std.lst']
    ret = False
    for i in stdlstname:
        if i not in lstname:
            lstpath = find_lst(dirname, i)
            if lstpath == '':
                print('cann\'t find ' + dirname + os.sep + i + ' in other place \n abort')
                os._exit(1)
            else:
                copy_lst_and_fit(lstpath, os.getcwd() + os.sep + dirname + os.sep)
                ret = True
    return ret

def main():
    check_bias()
    dirname = os.listdir(os.getcwd())
    dirname = [i for i in dirname if os.path.isdir(i) and 'bias' not in i and 'other' not in i]
    for i in dirname:
        flag = check_other(i)
        if flag:
            gen_lst.main()

if __name__ == '__main__':
    main()
