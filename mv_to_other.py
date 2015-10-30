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

def main():
    dirnames = os.popen("ls").readlines()
    dirnames = [ i.split('\n')[0] for i in dirnames ]
    dirnames = [ i for i in dirnames if os.path.isdir(i) and 'bias' not in i and 'other' not in i]
    standard = get_standard_lst()
    standard = [i[0] for i in standard]
    print('mkdir other')
    os.system('mkdir other')
    for i in dirnames:
        ifitsname = os.popen('ls ' + i).readlines()
        fitsnames = [ii.split('\n')[0] for ii in ifitsname]
        objects = []
        realobj_lst = []
        for j in fitsnames:
            fits = pyfits.open(i + os.sep + j)
            objects.append(fits[0].header['object'].lower())
            fits.close()
        for j in objects:
            if 'bias' not in j and 'halogen' not in j and 'neon' not in j and 'helium' not in j \
                    and 'fear' not in j:
                FLAG = True
                for k in standard:
                    if k in j:
                        FLAG = False
                        break
                if FLAG == True:
                    realobj_lst.append(j)
        if len(realobj_lst) == 0:
            print('mv ' + i + ' other/')
            os.system('mv ' + i + ' other/')
        else:
            print(i + ' not move')
            for obj in realobj_lst:
                print(obj + ' is real object')

if __name__ == '__main__':
    main()
