#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: zhixiang zhang <zzx>
# @Date:   27-Jun-2017
# @Email:  zhangzx@ihep.ac.cn
# @Filename: check_lessing.py
# @Last modified by:   zzx
# @Last modified time: 02-Jul-2017

"""
check the missing files.
if some file missing, we can\'t complete the whole process.
this routine check if there are missing files, and copy missing
data from other dir.
"""

import os
from termcolor import colored
import gen_lst
import func


def find_lst(lfname):
    """
    Find lst file in other date. lfname(lst file name) should be like
    'Grism_3_Slit_5.05/halogen.lst', 'bias/spec_bias.lst' etc.
    Assume curent dir = spec.
    This function assume date dir like '20170312'.
    lfname : lst file name
    type : string
    return : near date same name lst file(abs file path),
        if can\'t find, return None
    type : string or None
    """
    curdir = os.getcwd()  # current dir, shpuld **/20xxxxxx/spec
    specdir = os.path.basename(curdir)  # should spec
    abstoday_dir = os.path.dirname(curdir)  # should **/20xxxxxx
    today_dir = os.path.basename(abstoday_dir)  # should 20xxxxxx
    root_dir = os.path.dirname(abstoday_dir)  # should **/
    print root_dir
    oday_dirlst = os.listdir(root_dir)
    oday_dirlst = [i for i in oday_dirlst if os.path.isdir(root_dir+os.sep+i)]
    oday_dirlst.sort(key=lambda x: abs(int(today_dir)-int(x)))
    # sort date dir, key is abs diff to current date dir
    for dirname in oday_dirlst:
        filepath = root_dir+os.sep+dirname+os.sep+specdir+os.sep+lfname
        if os.path.isfile(filepath):
            return filepath
    return None


def main():
    """
    Assume current dir = spec
    check lst file list:
        bias.lst
        halogen.lst
        lamp.lst
        std.lst
    """
    print '-'*10+'check lessing'+'-'*10
    lflst = ['halogen.lst', 'lamp.lst', 'std.lst']
    curdir = os.getcwd()
    print colored('current dir = ' + curdir, 'green')

    if not os.path.isdir('bias'):
        print 'mkdir bias'
        os.mkdir('bias')
    bias_name = 'bias/spec_bias.lst'
    if not os.path.isfile(bias_name):
        pathname = find_lst(bias_name)
        func.copy_lstfile(pathname, 'bias')

    dirlst = os.listdir('.')
    dirlst = [i for i in dirlst if os.path.isdir(i) and
              i != 'bias' and i != 'other']
    for dirname in dirlst:
        for lstname in lflst:
            dirlstname = dirname+os.sep+lstname
            if not os.path.isfile(dirlstname):
                print colored('not found file '+dirlstname, 'red')
                pathname = find_lst(dirlstname)
                func.copy_lstfile(pathname, dirname)
    gen_lst.main()


if __name__ == '__main__':
    main()
