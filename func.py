# -*- coding: utf-8 -*-

# @Author: zhixiang zhang <zzx>
# @Date:   26-Jun-2017
# @Email:  zhangzx@ihep.ac.cn
# @Filename: func.py
# @Last modified by:   zzx
# @Last modified time: 02-Jul-2017

"""
basic function of project spec2015_1
"""

import os
import shutil
import webbrowser
import pyfits
from pyraf import iraf
try:
    from termcolor import colored
except ImportError:
    def colored(string, color):
        """ a instead of function colored"""
        return string

script_path = os.path.dirname(os.path.realpath(__file__))  # this script path
config_path = script_path + os.sep + 'config'  # the config file dir path
std_path = script_path+os.sep+'standarddir'  # standard star template dir path
extinction_file = config_path + os.sep + 'LJextinct.dat'


class obs(object):
    """
    the observatory information
    """
    name = 'Lijiang'
    longitude = 100.03
    latitude = 26.6951
    altitude = 3180.0

    def __init__(self):
        pass


def copy_lstfile(lstfile, dst):
    """
    copy lstfile to dst, and copy the files(name in lstfile) to dst
    lstfile : the lst file name(include abs path), like '/*/G4S5/abc.lst'
    type : string
    dst : derectory path, like 'G4S5', '/*/G4S5', 'G4S5/'
    type : string
    """
    print "copy %s to %s" % (lstfile, dst)
    shutil.copyfile(lstfile, dst=dst + os.sep + os.path.basename(lstfile))
    path = os.path.dirname(lstfile)
    namelst = open(lstfile).readlines()
    namelst = [i.strip() for i in namelst]
    for name in namelst:
        print "copy %s to %s" % (name, dst)
        shutil.copyfile(path + os.sep + name, dst=dst + os.sep + name)


def sname(fn):
    """
    get the standard name of a source
    fn : fits name
    type : string
    return : the source standard name
    type : string
    """
    namelst = open(config_path + os.sep + 'objcheck.lst').readlines()
    namedic = dict([i.split() for i in namelst])
    objname = pyfits.getval(fn, 'OBJECT')
    objname = objname.split('_')[0]
    if objname in namedic:
        return namedic[objname]
    print(colored(('can\'t match the object name %s.\nPlease check and '
                   'edit the match file.') % objname, 'yellow'))
    webbrowser.open(config_path + os.sep + 'objcheck.lst')
    raw_input('edit ok?(y)')
    return sname(fn)


def set_sname(fn):
    """
    set a new keyword 'SNAME' to fits fn,
    the value is standard name of the source.
    the SNAME value depend on the 'OBJECT' keyword.
    fn : fits name
    type : string
    """
    standname = sname(fn)
    size = len(pyfits.open(fn))
    if size == 1:
        iraf.hedit(images=fn, fields='SNAME', value=standname, add='Yes',
                   addonly='No', delete='No', verify='No', show='Yes',
                   update='Yes')
    else:
        for i in range(len(size)):
            iraf.hedit(images=fn + '[%d]' % i, fields='SNAME', value=standname,
                       add='Yes', addonly='No', delete='No', verify='No',
                       show='Yes', update='Yes')





def get_ra_dec(fn):
    """
    get the source coords
    fn : fits name
    type : string
    return : ra, dec (format like '12:34:56.78', '+23:45:67.89')
    type : string, string
    """
    standname = sname(fn)
    radeclst = open(config_path + os.sep + 'objradec.lst').readlines()
    radecdic = dict([i.split(None, 1) for i in radeclst])
    if standname in radecdic:
        ra, dec = radecdic[standname].split()
        return ra, dec
    print(colored('can\'t match %s, please check and edit objradec.lst'
                  % standname, 'yellow'))
    webbrowser.open(config_path + os.sep + 'objradec.lst')
    raw_input('edit ok?(y)')
    return get_ra_dec(fn)


def set_ra_dec(fn, ra, dec):
    """
    set the fits fn keyword 'RA' and 'DEC'
    fn : fits name
    type : string
    ra : format like '12:34:56.78'
    type : string
    dec : format like '+23:45:67.89'
    type : string
    """
    size = len(pyfits.open(fn))
    if size == 1:
        iraf.hedit(images=fn, fields='RA', value=ra, add='Yes', addonly='No',
                   delete='No', verify='No', show='Yes', update='Yes')
        iraf.hedit(images=fn, fields='DEC', value=dec, add='Yes', addonly='No',
                   delete='No', verify='No', show='Yes', update='Yes')
    else:
        for i in range(len(size)):
            iraf.hedit(images=fn + '[%d]' % i, fields='RA', value=ra,
                       add='Yes', addonly='No', delete='No', verify='No',
                       show='Yes', update='Yes')
            iraf.hedit(images=fn + '[%d]' % i, fields='DEC', value=dec,
                       add='Yes', addonly='No', delete='No', verify='No',
                       show='Yes', update='Yes')


def is_std(fn):
    """
    whether the star of fn is a standard star
    fn : fits name
    type : string
    return : whether the source is standard star
    type : boolean
    """
    stdlstname = config_path + os.sep + 'standard.lst'
    stdlst = open(stdlstname).readlines()
    stdset = set([i.split()[0].lower() for i in stdlst])
    objname = pyfits.getval(fn, 'OBJECT').split('_')[0].lower()
    if objname in stdset:
        return True
    for name in stdset:
        if name in objname:
            return True
    return False


def is_halogen(fn):
    """
    whether the fits fn is halogen flat, determined by keyword 'CLAMP1'
    fn : fits name
    type : string
    return :
    type : boolean
    """
    val = pyfits.getval(fn, 'CLAMP1')
    return bool(int(val) != 0)


def is_lamp(fn):
    """
    whether the fits fn is a wavelength calibrate file, determined by keyword
    'CLAMP2', 'CLAMP3', 'CLAMP4'
    'CLAMP2' : FeAr
    'CLAMP3' : Neon
    'CLAMP4' : Helium
    fn : fits name
    type : string
    return :
    type : boolean
    """
    val2 = int(pyfits.getval(fn, 'CLAMP2'))
    val3 = int(pyfits.getval(fn, 'CLAMP3'))
    val4 = int(pyfits.getval(fn, 'CLAMP4'))
    return True if val2 == 1 or val3 == 1 or val4 == 1 else False


def is_FeAr(fn):
    """
    whether the FeAr lamp light
    'CLAMP2' : FeAr
    'CLAMP3' : Neon
    'CLAMP4' : Helium
    fn : fits name
    type : string
    return :
    type : boolean
    """
    val2 = pyfits.getval(fn, 'CLAMP2')
    return bool(int(val2) == 1)


def is_Neon(fn):
    """
    whether the Neon lamp light
    'CLAMP2' : FeAr
    'CLAMP3' : Neon
    'CLAMP4' : Helium
    fn : fits name
    type : string
    return :
    type : boolean
    """
    val3 = pyfits.getval(fn, 'CLAMP3')
    if int(val3) == 1:
        return True
    return False


def is_Helium(fn):
    """
    whether the Helium lamp light
    'CLAMP2' : FeAr
    'CLAMP3' : Neon
    'CLAMP4' : Helium
    fn : fits name
    type : string
    return :
    type : boolean
    """
    val4 = pyfits.getval(fn, 'CLAMP4')
    return bool(int(val4) == 1)


def is_bias(fn):
    """
    whether the fits type is bias
    determined by keyword 'IMAGETYP'
    fn : fits name
    type : string
    return :
    type : boolean
    """
    val = pyfits.getval(fn, 'IMAGETYP')
    return bool(val.lower().strip() == 'bias')


def is_spec(fn):
    """
    whether the fits type is spec.
    determined by file size.
    fn : fits name
    type : string
    return :
    type : boolean
    """
    if fn[-5:] == '.fits':
        size = os.path.getsize(fn)
        if size == 39646080:
            return True
    return False


def set_airmass(fn):
    """
    Set airmass of fits fn. If keyword 'AIRMASS' already exist, the old airmass
    value will saved by keyword 'AIROLD'. If keyword 'AIROLD' also exist, the
    old airmass value will just overwritten. If the fits fn have more than one
    hdu or more than one star, this function assume they have same ra, dec and
    observed in same time.
    fn : fits name
    type : string
    """
    fit = pyfits.open(fn)
    size = len(fit)
    for i, hdu in enumerate(fit):
        if 'AIRMASS' in hdu.header:
            airmassold = hdu.header['AIRMASS']
            print(colored('%s[%d] airmassold = %f' % (fn, i, airmassold),
                          'blue'))
            if 'AIROLD' in hdu.header:
                airold = hdu.header['AIROLD']
                print(colored('%s[%d] AIROLD = %f' % (fn, i, airold),
                              'yellow'))
                print(colored(('\'AIROLD\' keyword alreay exist, the airmass '
                               'old will not saved'), 'yellow'))
            else:
                iraf.hedit(images=fn + '[%d]' % i, fields='AIROLD',
                           value=airmassold, add='Yes', addonly='Yes',
                           delete='No', verify='No', show='Yes', update='Yes')
    fit.close()
    ra, dec = get_ra_dec(fn)
    set_ra_dec(fn, ra, dec)
    iraf.twodspec()
    stdpath = std_path + os.sep
    extfile = config_path + os.sep + 'LJextinct.dat'
    iraf.longslit(dispaxis=2, nsum=1, observatory='Lijiang',
                  extinction=extfile, caldir=stdpath)
    for i in range(size):
        iraf.setairmass(images=fn + '[%d]' % i, observatory=obs.name,
                        intype='beginning', outtype='effective', ra='ra',
                        dec='dec', equinox='epoch', st='lst', ut='date-obs',
                        date='date-obs', exposure='exptime', airmass='airmass',
                        utmiddle='utmiddle', scale=750.0, show='yes',
                        override='yes', update='yes')


def standard_star_info(fn):
    """
    get standard star information.
    fn : fits name
    type : string
    return : standard star name, magnitude, mag band
    type : string, float, string
    """
    stdname = sname(fn)
    stdlstname = config_path + os.sep + 'standard.lst'
    lst = open(stdlstname).readlines()
    lst = dict([i.split(None, 2)[1:] for i in lst])
    mag, band = lst[stdname].split()
    return stdname, float(mag), band


def to_str(lst, sep=','):
    """
    convert string list to a sum string,
    like lst = ['abc.fits', 'def.fits', 'ghi.fits'],
    return 'abc.fits,def.fits,ghi.fits'
    lst : string list
    type : list
    sep : separator, default ','
    type : string
    return : sum string
    type : string
    """
    ret = ''
    for string in lst:
        ret += string + sep
    size = len(sep)
    ret = ret[:-size]
    return ret


def get_grism(fn):
    """
    get grism value, the grism keyword = 'YGRNM'.
    blank char will be replaced by '_'.
    fn : fits name
    type : string
    return : grism name
    type : string
    """
    name = pyfits.getval(fn, 'YGRNM')
    name = name.replace(' ', '_')
    return name


def get_slit(fn):
    """
    get slit value, the slit keyword = 'YAPRTNM'.
    blank char will replaced by '_'.
    fn : fits name
    type : string
    return : slit name
    type : string
    """
    name = pyfits.getval(fn, 'YAPRTNM')
    name = name.replace(' ', '_')
    return name


def get_aper(fn):
    """
    get aperture parameter for iraf command apall.
    the parameter include lower, upper, background window.
    the parameter come from data file aperture.lst
    if fn sname not in aperture.lst, will show a warn info and
        return default value : -15.0, 15.0, '-50:-26,26:50'
    fn : fits name
    type : string
    return : lower, upper, back_window
             like -15.0, 15.0, '-50:-26,26:50'
    type : float, float, string
    """
    lst = [i.split() for i in file(config_path + os.sep + 'aperture.lst')]
    dic = dict([[i[0], [float(i[1]), float(i[2]), i[3]]] for i in lst])
    name = sname(fn)
    if name in dic:
        tmp = dic[name]
        return float(tmp[0]), float(tmp[1]), tmp[2]
    print colored('%s %s not in aperture.lst' % (fn, name), 'yellow')
    return -15.0, 15.0, '-50:-26,26:50'


def get_trimsec(fn):
    """
    get trim section of fits fn. determined by Grism and Slit.
    trim section info come from data file trim.lst
    if grism_slit of fn not in trim.lst, will print a wran info and return None
    fn : fits name
    type : string
    return (x1, x2, y1, y2)
    type : (string, string, string, string)
    """
    grism = get_grism(fn)
    slit = get_slit(fn)
    name = grism + '_' + slit
    lst = [i.split() for i in file(config_path + os.sep + 'trim.lst')]
    dic = dict([[i[0], [i[1], i[2], i[3], i[4]]] for i in lst])
    if name in dic:
        return tuple(dic[name])
    print colored('%s trim section not found in trim.lst', 'yellow!!!')
    return None
