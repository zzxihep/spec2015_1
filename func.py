import os
import pyfits
import shutil
import webbrowser
from termcolor import colored
from pyraf import iraf

script_path = os.path.dirname(os.path.realpath(__file__))

def sname(fn):
    """
    get the standard name of a source
    fn : fits name
    type : string
    return : the source standard name
    type : string
    """
    namelst = open(script_path+os.sep+'objcheck.lst').readlines()
    namedic = dict([i.split() for i in namelst])
    objname = pyfits.getval(fn, 'OBJECT')
    if objname in namedic:
        return namedic[objname]
    else:
        print(colored('can\'t match the object name %s\nPlease check and edit the match file.', 'yellow'))
        webbrowser.open(script_path+os.sep+'objcheck.lst')
        raw_input('edit ok?(y)')
        sname(fn)

def set_sname(fn):
    """
    set a new keyword 'SNAME' to fits fn, the value is standard name of the source. the SNAME value depend on the 'OBJECT' keyword.
    fn : fits name
    type : string
    """
    standname = sname(fn)
    size = len(pyfits.open(fn))
    if size == 1:
        iraf.hedit(images=fn, fields='SNAME', value=standname, add = 'Yes', \
            addonly='No', delete='No', verify='No', show='Yes', update='Yes')
    else:
        for i in range(len(size)):
            iraf.hedit(images=fn+'[%d]'%i, fields='SNAME', value=standname, \
                add = 'Yes', addonly='No', delete='No', verify='No', \
                show='Yes', update='Yes')

def copy_lstfile(lstfile, dst):
    """
    copy lstfile to dst, and copy the files(name in lstfile) to dst
    lstfile : the lst file name(include abs path)
    type : string
    dst : derectory path
    type : string
    """
    print("copy %s to %s" % (lstfile, dst))
    shutil.copyfile(lstfile, dst=dst+os.sep)
    path = os.path.dirname(lstfile)
    namelst = open(lstfile).readlines()
    namelst = [i.strip() for i in namelst]
    for name in namelst:
        print("copy %s to %s" % (name, dst))
        shutil.copyfile(path+os.sep+name, dst=dst+os.sep)

def get_ra_dec(fn):
    """
    get the source coords
    fn : fits name
    type : string
    return : ra, dec (format like '12:34:56.78', '+23:45:67.89')
    type : string, string
    """
    standname = sname(fn)
    radeclst = open(script_path+os.sep+'objradec.lst').readlines()
    radecdic = dict([i.split(None, 1) for i in radeclst])
    if standname in radecdic:
        ra, dec = radecdic[standname].split()
        return ra, dec
    else:
        print(colored('can\'t match %s, please check and edit objradec.lst', 'yellow'))
        webbrowser.open(script_path+os.sep+'objradec.lst')
        raw_input('edit ok?(y)')
        get_ra_dec(fn)

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
        iraf.hedit(images=fn, fields='RA', value=ra, add = 'Yes', \
            addonly='No', delete='No', verify='No', show='Yes', update='Yes')
        iraf.hedit(images=fn, fields='DEC', value=dec, add = 'Yes', \
            addonly='No', delete='No', verify='No', show='Yes', update='Yes')
    else:
        for i in range(len(size)):
            iraf.hedit(images=fn+'[%d]'%i, fields='RA', value=ra, \
                add = 'Yes', addonly='No', delete='No', verify='No', \
                show='Yes', update='Yes')
            iraf.hedit(images=fn+'[%d]'%i, fields='DEC', value=dec, \
                add = 'Yes', addonly='No', delete='No', verify='No', \
                show='Yes', update='Yes')

def is_std(fn):
    """
    whether the star of fn is a standard star
    fn : fits name
    type : string
    return : whether the source is standard star
    type : boolean
    """
    stdlstname = script_path + os.sep + 'standard.lst'
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
    whether the fits fn is a wavelength calibrate file, determined by keyword 'CLAMP2', 'CLAMP3', 'CLAMP4'
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
