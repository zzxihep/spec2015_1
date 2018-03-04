#!/usr/bin/env python

"""
copy flux spec and counts spec to a specdir named 'ljspec'
the spec files are classified by their keyword 'SNAME'
"""

import os
import sys
import shutil
import func


def main():
    snameset = set()
    curdir = os.getcwd()
    updir = os.path.dirname(curdir)
    if not os.path.isdir(updir+os.sep+'ljspec'):
        print 'mkdir ', updir+os.sep+'ljspec'
        os.mkdir(updir+os.sep+'ljspec')
    specdir = updir+os.sep+'ljspec'
    if len(sys.argv) <= 1:
        dirlst = os.listdir('.')
        dirlst = [i for i in dirlst if os.path.isdir(i)]
    else:
        dirlst = sys.argv[1:]
    for dirname in dirlst:
        for path, dlst, flst in os.walk(curdir+os.sep+dirname):
            for fname in flst:
                if 'mark' in fname and '.fits' in fname:
                    sname = func.sname(path+os.sep+fname)
                    if not os.path.isdir(specdir+os.sep+sname):
                        print 'mkdir ', specdir+os.sep+sname
                        os.mkdir(specdir+os.sep+sname)
                        print 'mkdir ', specdir+os.sep+sname+os.sep+'fits_in'
                        os.mkdir(specdir+os.sep+sname+os.sep+'fits_in')
                    todir = specdir+os.sep+sname+os.sep+'fits_in'
                    if not os.path.isfile(todir+os.sep+fname):
                        snameset.add(sname)
                        print 'cp '+path+os.sep+fname+'  ' + todir+os.sep+fname
                        shutil.copyfile(path+os.sep+fname, todir+os.sep+fname)
                        fname2 = fname.replace('mark_', '')
                        print 'cp', path+os.sep+fname2, todir+os.sep+fname2
                        shutil.copyfile(path+os.sep+fname2,
                                        todir+os.sep+fname2)
    print 'List updated objects below:'
    for sname in snameset:
        print ' '*12, sname


if __name__ == '__main__':
    main()
