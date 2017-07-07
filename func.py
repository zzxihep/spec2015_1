# @Author: zhixiang zhang <zzx>
# @Date:   26-Jun-2017
# @Email:  zhangzx@ihep.ac.cn
# @Filename: func.py
# @Last modified by:   zzx
# @Last modified time: 02-Jul-2017


import os
import pyfits
import shutil
import webbrowser
from termcolor import colored
from pyraf import iraf

script_path = os.path.dirname(os.path.realpath(__file__))  # this script path
config_path = script_path+os.sep+'config'  # the config file dir path
std_path = script_path+os.sep+'standarddir'  # standard star template dir path
extinction_file = config_path+os.sep+'LJextinct.dat'


class obs:
    """
    the observatory information
    """
    name = 'Lijiang'
    longitude = 100.03
    latitude = 26.6951
    altitude = 3180.0


try:
    from termcolor import colored
except ImportError:
    def colored(string, color):
        return string


def sname(fn):
    """
    get the standard name of a source
    fn : fits name
    type : string
    return : the source standard name
    type : string
    """
    namelst = open(config_path+os.sep+'objcheck.lst').readlines()
    namedic = dict([i.split() for i in namelst])
    objname = pyfits.getval(fn, 'OBJECT')
    objname = objname.split('_')[0]
    if objname in namedic:
        return namedic[objname]
    else:
        print(colored(('can\'t match the object name %s.\nPlease check and '
                       'edit the match file.') % objname, 'yellow'))
        webbrowser.open(config_path+os.sep+'objcheck.lst')
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
            iraf.hedit(images=fn+'[%d]' % i, fields='SNAME', value=standname,
                       add='Yes', addonly='No', delete='No', verify='No',
                       show='Yes', update='Yes')


def copy_lstfile(lstfile, dst):
    """
    copy lstfile to dst, and copy the files(name in lstfile) to dst
    lstfile : the lst file name(include abs path), like '/*/G4S5/abc.lst'
    type : string
    dst : derectory path, like 'G4S5', '/*/G4S5', 'G4S5/'
    type : string
    """
    print("copy %s to %s" % (lstfile, dst))
    shutil.copyfile(lstfile, dst=dst+os.sep+os.path.basename(lstfile))
    path = os.path.dirname(lstfile)
    namelst = open(lstfile).readlines()
    namelst = [i.strip() for i in namelst]
    for name in namelst:
        print("copy %s to %s" % (name, dst))
        shutil.copyfile(path+os.sep+name, dst=dst+os.sep+name)


def get_ra_dec(fn):
    """
    get the source coords
    fn : fits name
    type : string
    return : ra, dec (format like '12:34:56.78', '+23:45:67.89')
    type : string, string
    """
    standname = sname(fn)
    radeclst = open(config_path+os.sep+'objradec.lst').readlines()
    radecdic = dict([i.split(None, 1) for i in radeclst])
    if standname in radecdic:
        ra, dec = radecdic[standname].split()
        return ra, dec
    else:
        print(colored('can\'t match %s, please check and edit objradec.lst'
                      % standname, 'yellow'))
        webbrowser.open(config_path+os.sep+'objradec.lst')
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
            iraf.hedit(images=fn+'[%d]' % i, fields='RA', value=ra, add='Yes',
                       addonly='No', delete='No', verify='No', show='Yes',
                       update='Yes')
            iraf.hedit(images=fn+'[%d]' % i, fields='DEC', value=dec,
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
    stdlstname = config_path+os.sep+'standard.lst'
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
    if int(val) == 0:
        return False
    else:
        return True


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
    val2 = pyfits.getval(fn, 'CLAMP2')
    val3 = pyfits.getval(fn, 'CLAMP3')
    val4 = pyfits.getval(fn, 'CLAMP4')
    if int(val2) == 1 or int(val3) == 1 or int(val4) == 1:
        return True
    else:
        return False


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
    if int(val2) == 1:
        return True
    else:
        return False


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
    else:
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
    if int(val4) == 1:
        return True
    else:
        return False


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
    if val.lower().strip() == 'bias':
        return True
    else:
        return False


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
                iraf.hedit(images=fn+'[%d]' % i, fields='AIROLD',
                           value=airmassold, add='Yes', addonly='Yes',
                           delete='No', verify='No', show='Yes', update='Yes')
    fit.close()
    ra, dec = get_ra_dec(fn)
    set_ra_dec(fn, ra, dec)
    iraf.twodspec()
    stdpath = std_path+os.sep
    extfile = config_path+os.sep+'LJextinct.dat'
    iraf.longslit(dispaxis=2, nsum=1, observatory='Lijiang',
                  extinction=extfile, caldir=stdpath)
    for i in range(size):
        iraf.setairmass(images=fn+'[%d]' % i, observatory=obs.name,
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
    stdlstname = config_path+os.sep+'standard.lst'
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
