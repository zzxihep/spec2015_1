#! /usr/bin/env python
# -*- coding = utf-8 -*-

import sys
# from astropy import time
import pyfits
import ephem
from pyraf import iraf
import func

"""
Some day Lijiang data airmass and other keywords are absolutely wrong.
We can not get the right airmass just through command setairmass.
This routine is to repair the wrong keyword airmass and other keyword.
The default repaired fits are awftbo*.fits
"""


# def get_sidereal_time(datestr): # some time can not work
#     """
#     return the sidereal time at the obs time and at the func obs observatory.
#     observatory longitude information come from func.obs.longitude.
#     datestr : obs time, formate like '2015-12-22T22:22:22.029'
#     type : string
#     return : sidereal time, format like u'9:42:43.484'
#     type : string
#     """
#     print datestr
#     utime = time.Time(datestr, format='isot', scale='utc')
#     sidtime = utime.sidereal_time(kind='apparent',
#                                   longitude=str(func.obs.longitude)+'d')
#     sidstr = sidtime.to_string(sep=':')
#     return sidstr


def get_sidereal_time2(datestr):
    """
    return the local sidereal time at the obs time and at the func observatory.
    observatory coord information come from func.obs.
    datestr : obs time, format '2015-12-22T22:22:22.029'
    type : string
    return : local sidereal time, format '09:42:43.32'
    type : string
    """
    ndate = datestr.replace('-', '/').replace('T', ' ')
    # convert date format to '2015/12/22 22:22:22.029'
    print ndate
    ob = ephem.Observer()
    ob.lon = str(func.obs.longitude)
    ob.lat = str(func.obs.latitude)
    ob.elevation = func.obs.altitude
    ob.date = ndate
    sidtime = str(ob.sidereal_time())
    return sidtime


def cor_keyword(fn):
    """
    Correct bad keyword of setairmass command needed.
    then set airmass.
    fn : fits name
    type : string
    """
    ra, dec = func.get_ra_dec(fn)
    func.set_ra_dec(fn, ra, dec)  # set ra dec
    iraf.hedit(images=fn, fields='EPOCH', value='2000.000', add='Yes',
               addonly='No', delete='No', verify='No', show='Yes',
               update='Yes')  # set epoch
    dateobs = pyfits.getval(fn, 'DATE-OBS')
    sidtime = get_sidereal_time2(dateobs)
    iraf.hedit(images=fn, fields='LST', value=sidtime, add='Yes', addonly='No',
               delete='No', verify='No', show='Yes', update='Yes')
    func.set_airmass(fn)


def main():
    """
    If the day airmass and other keyword was wrong, this routine just try to
    repair the airmass keyword and other keyword.
    """
    namelst = open('cor_lamp.lst').readlines()
    namelst = ['awftbo'+i.strip() for i in namelst]
    for name in namelst:
        cor_keyword(name)
        func.set_airmass(name)


if __name__ == '__main__':
    main()
