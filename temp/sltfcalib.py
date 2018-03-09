#!/Users/dupu/Software/ureka/Ureka/python/bin/python

import os
import sys
import pyfits
from pyraf import iraf

objlist = '/Users/dupu/work/mapping/2014_spec/code/objlist.txt'
standoutput = 'stand_spec.txt'
targetoutput = 'target_spec.txt'

def find_standard():
    stdout = os.popen("ls Y*otbfmsw.fits").readlines()
    namelst = [i.split('\n')[0] for i in stdout]
    print '#' * 50
    print 'please find standard star exposures...'
    f = open(standoutput, 'w')
    f2 = open(targetoutput, 'w')
    for i in xrange(len(namelst)):
        fits = pyfits.open(namelst[i])
        objname = fits[0].header['object']
        fits.close()
        print namelst[i], objname
        if raw_input('is this one a standard star? (yes:ENTER, no:"n")') == '':
            f.write(namelst[i] + '\n')
        else:
            f2.write(namelst[i] + '\n')
    f.close()
    f2.close()

    # ===== check standard list ====
    os.system("mvim " + standoutput)
    print 'please check standard list'
    a = raw_input('if ok press ENTER, if not input "e":')
    if a != '':
        print 'standard star error!'
        sys.exit()

    # ===== check target list ====
    os.system("mvim " + targetoutput)
    print 'please check target list'
    a = raw_input('if ok press ENTER, if not input "e":')
    if a != '':
        print 'target error!'
        sys.exit()

def correct_airmass():
    stdout = os.popen("ls Y*otbfmsw.fits").readlines()
    namelst = [i.split('\n')[0] for i in stdout]
    for i in xrange(len(namelst)):
        fits = pyfits.open(namelst[i])
        extnum = len(fits)
        objname = fits[0].header['object']
        fits.close()
        print '#' * 50
        print namelst[i], objname
        name = raw_input('please input the name of object:')
        ra, dec = findradec(name)
        print name, ra, dec
        for j in xrange(extnum):
            stdout = iraf.hselect(images = namelst[i] + '[%i]' % j, fields = 'airmass',
                    expr = 'yes', Stdout = 1)
            airold = float(stdout[0])
            print '+' * 5, namelst[i], 'ext:', j, 'airmass_old:', airold
            iraf.hedit(images = namelst[i] + '[%i]' % j, fields = 'airold',
                    value = airold, add = 'yes', addonly = 'yes', delete = 'no',
                    verify = 'no', show = 'yes', update = 'yes')
            iraf.hedit(images = namelst[i] + '[%i]' % j, fields = 'sname',
                    value = name, add = 'yes', addonly = 'yes', delete = 'no',
                    verify = 'no', show = 'yes', update = 'yes')
            iraf.hedit(images = namelst[i] + '[%i]' % j, fields = 'sname',
                    value = name, add = 'yes', addonly = 'yes', delete = 'no',
                    verify = 'no', show = 'yes', update = 'yes')
            iraf.hedit(images = namelst[i] + '[%i]' % j, fields = 'ra',
                    value = ra, add = 'yes', addonly = 'yes', delete = 'no',
                    verify = 'no', show = 'yes', update = 'yes')
            iraf.hedit(images = namelst[i] + '[%i]' % j, fields = 'dec',
                    value = dec, add = 'yes', addonly = 'yes', delete = 'no',
                    verify = 'no', show = 'yes', update = 'yes')
            iraf.twodspec()
            iraf.longslit(dispaxis = 2, nsum = 1, observatory = 'Lijiang',
                    extinction = 'onedstds$LJextinct.dat', caldir = 'onedstds$spec50cal/')
            iraf.setairmass(images = namelst[i] + '[%i]' % j,
                    observatory = 'Lijiang', intype = 'beginning',
                    outtype = 'effective', ra = 'ra', dec = 'dec',
                    equinox = 'epoch', st = 'lst', ut = 'date-obs',
                    date = 'date-obs', exposure = 'exptime', airmass = 'airmass',
                    utmiddle = 'utmiddle', scale = 750.0, show = 'yes',
                    override = 'yes', update = 'yes')
            print 'name                            airmass_new     airmass_old'
            iraf.hselect(images = namelst[i] + '[%i]' % j, fields = '$I,airmass,airold',
                    expr = 'yes')

def findradec(name):
    f = open(objlist)
    f.readline()
    l = f.readlines()
    f.close()
    namelst = [i.split()[0] for i in l]
    ralst = [i.split()[1] for i in l]
    declst = [i.split()[2] for i in l]

    if name not in namelst:
        print 'object ', name, ' not in objlist!'
        ra = raw_input('please input ra:')
        dec = raw_input('please input dec:')
        f = open(objlist, 'a')
        text = '%-12s %-11s   %-11s\n' % (name, ra, dec)
        f.write(text)
        f.close()
        print 'add object ', name, ' into objlist...ok!'

        f = open(objlist)
        f.readline()
        l = f.readlines()
        f.close()
        namelst = [i.split()[0] for i in l]
        ralst = [i.split()[1] for i in l]
        declst = [i.split()[2] for i in l]

    for i in xrange(len(namelst)):
        if namelst[i] == name:
            ra = ralst[i]
            dec = declst[i]

    return ra, dec

def standard():
    f = open(standoutput)
    l = f.readlines()
    f.close()
    namelst = [i.split('\n')[0] for i in l]
    temp = ''
    for i in namelst:
        temp = temp + i + ','
    temp = temp[0: -1]

#    for i in xrange(len(namelst)):
#        iraf.hselect(images = namelst[i], fields = '$I,object', expr = 'yes')
#    standname = raw_input('please input standard star name:')
#    print 'standard star name:', standname
    iraf.twodspec()
    iraf.longslit(dispaxis = 2, nsum = 1, observatory = 'Lijiang',
            extinction = 'onedstds$LJextinct.dat', caldir = 'onedstds$ctiocal/')
    for i in xrange(len(namelst)):
        print '+' * 10, namelst[i]
        iraf.hselect(images = namelst[i], fields = '$I,object', expr = 'yes')
        standname = raw_input('please input standard star name:')
        print 'standard star name:', standname
        #iraf.standard(input = namelst[i], output = namelst[i].split('.')[0] + '.std',
        #        samestar = 'yes', interact = 'yes', star_name = standname, airmass = '',
        #        exptime = '', extinction = 'onedstds$LJextinct.dat',
        #        caldir = 'onedstds$ctiocal/')
        iraf.standard(input = namelst[i], output = 'std',
                samestar = 'yes', interact = 'yes', star_name = standname, airmass = '',
                exptime = '', extinction = 'onedstds$LJextinct.dat',
                caldir = 'onedstds$ctiocal/')

#    iraf.standard(input = temp, output = 'std',
#            samestar = 'yes', interact = 'yes', star_name = standname, airmass = '',
#            exptime = '', extinction = 'onedstds$LJextinct.dat',
#            caldir = 'onedstds$ctiocal/')

def sensfunc():
    iraf.twodspec()
    iraf.longslit(dispaxis = 2, nsum = 1, observatory = 'Lijiang',
            extinction = 'onedstds$LJextinct.dat', caldir = 'onedstds$ctiocal/')
    iraf.sensfunc(standards = 'std', sensitivity = 'sens',
            extinction = 'onedstds$LJextinct.dat', function = 'spline3', order = 9)

def calibrate():
    namelst = [i.split('\n')[0] for i in file(targetoutput)]
    for i in namelst:
        iraf.twodspec()
        iraf.longslit(dispaxis = 2, nsum = 1, observatory = 'Lijiang',
                extinction = 'onedstds$LJextinct.dat', caldir = 'onedstds$ctiocal/')
        iraf.calibrate(input = i, output = i.split('.')[0] + 'f.fits',
                extinct = 'yes', flux = 'yes', extinction = 'onedstds$LJextinct.dat',
                ignoreaps = 'yes', sensitivity = 'sens', fnu = 'no')

def main():
    correct_airmass()
    find_standard()
    standard()
    sensfunc()
    calibrate()

if __name__ == "__main__":
    main()
