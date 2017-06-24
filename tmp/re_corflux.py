#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 22:08:34 2015

@author: zzx
"""

import os
import pyfits
from pyraf import iraf

stdlstname = 'std.lst'
objradeclst = 'objradec.lst'

def get_std_group(lstfile):
    f = open(lstfile)
    l = f.readlines()
    f.close()
    l = [tmp.split('\n')[0] for tmp in l]
    group = {}
    for i in l:
        fit = pyfits.open('awftbo'+i)
        name = fit[0].header['object']
        if name in group:
            group[name].append(i)
        else:
            group[name] = [i]
    return group
    
def get_std_mjd(groupset):
    mjdlst = {}
    for i in groupset:
        fit = pyfits.open('awftbo'+groupset[i][0])
        mjdlst[i] = fit[0].header['MJD']
    return mjdlst
    
stdgroup = {}
stdmjdlst = {}

def select_std(filename):
    fit = pyfits.open(filename)
    fitmjd = fit[0].header['MJD']
    timedif = 10000000.
    name = ''
    for i in stdmjdlst:
        tmp = abs(stdmjdlst[i] - fitmjd)
        if tmp < timedif:
            timedif = tmp
            name = i
    return name
    
def get_radec_dict():
    path = os.path.split(os.path.realpath(__file__))[0]
    f = open(path + os.sep + objradeclst)
    l = f.readlines()
    f.close()
    l = [tmp.split() for tmp in l]
    return dict([[tmp[0],[tmp[1],tmp[2]]] for tmp in l])

objradecdict = get_radec_dict()

def findradec(name):
    global objradecdict
    while name not in objradecdict:
        print('cann\'t find radec, please add objname ra dec to objradec.lst. The routine will try again.')
        filepath = os.path.split(os.path.realpath(__file__))[0] + os.sep + objradeclst
        os.system('gedit ' + filepath)
        objradecdict = get_radec_dict()
    return objradecdict[name]
        
def get_fit_normal_lst():
    filepath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'objcheck.lst'
    f = open(filepath)
    l = f.readlines()
    f.close()
    l = [tmp.split() for tmp in l]
    return dict(l)
        
obj_fit_normal_lst = get_fit_normal_lst()
        
def find_normal_objname(fitobjname):
    global obj_fit_normal_lst
    while fitobjname not in obj_fit_normal_lst:
        print('=' * 20 + 'cann\'t find the real objname, please add objname a note to objcheck.lst. The routine will try again.')
        filepath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'objcheck.lst'
        os.system('gedit ' + filepath)
        obj_fit_normal_lst = get_fit_normal_lst()
    return obj_fit_normal_lst[fitobjname]

def cor_airmass(lstfile):
    f = open(lstfile)
    l = f.readlines()
    f.close()
    l = [tmp.split('\n')[0] for tmp in l]
    fitlst = ['awftbo' + tmp for tmp in l]
    for fitname in fitlst:
        if os.path.isfile(fitname):
            fit = pyfits.open(fitname)
            objname = fit[0].header['object'].replace('_', ' ').split()[0]
            print(fitname + ' ' + objname)
            objname_new = find_normal_objname(objname)
            if len(objname_new) == 0:
                objname_new = raw_input('please input object name:')
            radec = findradec(objname_new)
            if len(radec) == 0:
                radec = raw_input('please input ra dec of objname:')
                radec = radec.split()
            fitextnum = len(fit)
            fit.close()
            for lay in range(fitextnum):
                airold = iraf.hselect(images = fitname + '[%i]' % lay, fields = 'airmass', expr = 'yes', Stdout = 1)
                airold = float(airold[0])
                print(fitname + ' ' + objname + ' ' + str(lay) + ' airmass old: ' + str(airold))
                fitnamelay = fitname + '[%i]' % lay
                iraf.hedit(images = fitnamelay, fields = 'airold', 
                    value = airold, add = 'yes', addonly = 'yes', delete = 'no', 
                    verify = 'no', show = 'yes', update = 'yes')
                iraf.hedit(images = fitnamelay, fields = 'sname', 
                    value = objname_new, add = 'yes', addonly = 'yes', delete = 'no', 
                    verify = 'no', show = 'yes', update = 'yes')
                iraf.hedit(images = fitnamelay, fields = 'RA', 
                    value = radec[0], add = 'yes', addonly = 'yes', delete = 'no', 
                    verify = 'no', show = 'yes', update = 'yes')
                iraf.hedit(images = fitnamelay, fields = 'DEC', 
                    value = radec[1], add = 'yes', addonly = 'yes', delete = 'no', 
                    verify = 'no', show = 'yes', update = 'yes')
                iraf.twodspec()
                stdpath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'standarddir' + os.sep
                iraf.longslit(dispaxis = 2, nsum = 1, observatory = 'Lijiang', 
                    extinction = 'onedstds$LJextinct.dat', caldir = stdpath)
                iraf.setairmass(images = fitnamelay,
                    observatory = 'Lijiang', intype = 'beginning', 
                    outtype = 'effective', ra = 'ra', dec = 'dec', 
                    equinox = 'epoch', st = 'lst', ut = 'date-obs', 
                    date = 'date-obs', exposure = 'exptime', airmass = 'airmass', 
                    utmiddle = 'utmiddle', scale = 750.0, show = 'yes', 
                    override = 'yes', update = 'yes')
                #iraf.hedit(images = fitnamelay, fields = 'AIRMASS',
                #     value = '1', add = 'yes', addonly = 'yes', delete = 'no',
                #     verify = 'no', show = 'yes', update = 'yes')

                print('name airmass_new airmass_old')
                iraf.hselect(fitnamelay, fields = '$I,airmass,airold', 
                             expr = 'yes')
    
def get_std_name(objname):
    scripath = os.path.split(os.path.realpath(__file__))[0]
    f = open(scripath + os.sep + 'standard.lst')
    name = f.readlines()
    f.close()
    stdnames = []
    for i in name:
        stdnames.append(i.split())
    fitsname = objname.lower()
    for i in stdnames:
        if i[0] in fitsname:
            return i[1], i[2], i[3]
    print('can\'t find standard name %s' % fitsname)
    os.system('gedit ' + scripath + os.sep + 'standard.lst' + ' &')
    valget = raw_input('Please input the standard star name:')
    valget = valget.lower()
    for i in stdnames:
        if i[0] in valget:
            return i[1]
    return []

#def standard():
#    f = open('std.lst')
#    l = f.readlines()
#    f.close()
#    namelst = [i.split('\n')[0] for i in l]
#    temp = ''
#    for i in namelst:
#        temp = temp + 'awftbo'+ i + ','
#    temp = temp[0: -1]
#    stdpath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'standarddir' + os.sep
#    extpath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'LJextinct.dat'
#
##    for i in xrange(len(namelst)):
##        iraf.hselect(images = namelst[i], fields = '$I,object', expr = 'yes')
##    standname = raw_input('please input standard star name:')
##    print 'standard star name:', standname
#    iraf.twodspec()
#    iraf.longslit(dispaxis = 2, nsum = 1, observatory = 'Lijiang', 
#            extinction = extpath, caldir = stdpath)
#    for i in xrange(len(namelst)):
#        print '+' * 10, namelst[i]
#        iraf.hselect(images = 'awftbo'+namelst[i], fields = '$I,object', expr = 'yes')
#        standname = raw_input('please input standard star name:')
#        print 'standard star name:', standname
#        #iraf.standard(input = namelst[i], output = namelst[i].split('.')[0] + '.std', 
#        #        samestar = 'yes', interact = 'yes', star_name = standname, airmass = '', 
#        #        exptime = '', extinction = 'onedstds$LJextinct.dat', 
#        #        caldir = 'onedstds$ctiocal/')
#        iraf.standard(input = 'awftbo'+namelst[i], output = 'Std', 
#                samestar = 'yes', interact = 'yes', star_name = standname, airmass = '', 
#                exptime = '', extinction = extpath, 
#                caldir = stdpath)
#
#    iraf.twodspec()
#    iraf.longslit(dispaxis = 2, nsum = 1, observatory = 'Lijiang', 
#        extinction = extpath, caldir = stdpath)
#    iraf.sensfunc(standards = 'Std', sensitivity = 'Sens', 
#        extinction = extpath, function = 'spline3', order = 9)
#    iraf.splot('Sens')
#
##    iraf.standard(input = temp, output = 'std', 
##            samestar = 'yes', interact = 'yes', star_name = standname, airmass = '', 
##            exptime = '', extinction = 'onedstds$LJextinct.dat', 
##            caldir = 'onedstds$ctiocal/')


def standard():
    stdpath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'standarddir' + os.sep
    print('standard dir is ' + stdpath)
    extpath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'LJextinct.dat'
    iraf.noao()
    iraf.twodspec()
    iraf.longslit(dispaxis = 2, nsum = 1, observatory = 'Lijiang', 
            extinction = extpath, caldir = stdpath)
    for objname in stdgroup:
        stdname, stdmag, stdmagband = get_std_name(objname)
        print('the standard star is ' + stdname)
        stdmag = float(stdmag)
        outname1 = 'stdawftbo' + stdgroup[objname][0]
        inname   = ''
        for tmpname in stdgroup[objname]:
            inname = inname + 'awftbo' + tmpname + ','
        inname = inname[0:-1]
        for tmpname in stdgroup[objname]:
            #            iraf.standard(input = 'awftbo'+tmpname
            iraf.standard(input = inname
                , output = 'Std', samestar = True, beam_switch = False
                , apertures = '', bandwidth = 'INDEF', bandsep = 'INDEF' # 30.0  20.0
                , fnuzero = 3.6800000000000E-20, extinction = extpath
                , caldir = stdpath, observatory = 'Lijiang'
                , interact = True, graphics = 'stdgraph', cursor = ''
                , star_name = stdname, airmass = '', exptime = ''
                , mag = stdmag, magband = stdmagband, teff = '', answer = 'yes')
             #    for name in stdgroup:
        #inpar = 'stdawftbo' + stdgroup[name][0]
    iraf.sensfunc(standards = 'Std', sensitivity = 'Sens', 
        extinction = extpath, function = 'spline3', order = 9)
    iraf.splot('Sens')
            
def calibrate(lstfile):
    stdpath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'standarddir' + os.sep
    extpath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'LJextinct.dat'
    iraf.noao()
    iraf.twodspec()
    iraf.longslit(dispaxis = 2, nsum = 1, observatory = 'Lijiang', 
        extinction = extpath, caldir = stdpath)
    f = open(lstfile)
    l = f.readlines()
    f.close()
    l = [tmp.split('\n')[0] for tmp in l]
    for fitname in l:
        stdobjname = select_std(fitname)
   #     stdfitname = 'sensawftbo' + stdgroup[stdobjname][0]
        stdfitname = 'Sens'
        iraf.calibrate(input = 'awftbo'+ fitname, output = 'mark_awftbo' + fitname, 
            extinct = 'yes', flux = 'yes', extinction = extpath, 
            ignoreaps = 'yes', sensitivity = stdfitname, fnu = 'no')
        iraf.splot(images = 'mark_awftbo' + fitname)
            
def clear():
    filename = os.listdir(os.getcwd())
    filename = [tmp for tmp in filename if os.path.isfile(tmp) and \
        ( tmp[0:10] == 'sensawftbo' or tmp[0:9] == 'stdawftbo' or tmp[0:11] \
        == 'mark_awftbo')]
    for i in filename:
        print('remove ' + i)
        os.remove(i)
    if os.path.isfile('Sens.fits'):
        os.remove('Sens.fits')
    if os.path.isfile('Std'):
        os.remove('Std')
        
def main():
    global stdgroup
    global stdmjdlst
    clear()
    stdgroup = get_std_group(stdlstname)
    stdmjdlst = get_std_mjd(stdgroup)
    cor_airmass('cor_lamp.lst')
    standard()
    calibrate('cor_std.lst')

if __name__ == '__main__':
    main()
