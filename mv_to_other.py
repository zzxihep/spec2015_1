#!/usr/bin/env python

import os,sys,shutil
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
    #dirnames = os.popen("ls").readlines()
    dirnames = os.listdir(os.getcwd())
    #dirnames = [ i.split('\n')[0] for i in dirnames ]
    dirnames = [ i for i in dirnames if os.path.isdir(i) and 'bias' not in i and 'other' not in i]
    standard = get_standard_lst()
    standard = [i[0] for i in standard]
    print('mkdir other')
    #os.system('mkdir other')
    os.mkdir('other')
    for i in dirnames:
        #ifitsname = os.popen('ls ' + i).readlines()
        ifitsname = os.listdir(os.getcwd() + os.sep + i)
        #fitsnames = [ii.split('\n')[0] for ii in ifitsname]
        fitsnames = [ii for ii in ifitsname if os.path.isfile(os.getcwd() + os.sep + i + os.sep \
                + ii) and ii[0:2] == 'YF' and ii[-5:] == '.fits']
        objects = []
        realobj_lst = []
        for j in fitsnames:
            fits = pyfits.open(i + os.sep + j)
            object_val = fits[0].header['object'].lower()
            lamp_flag = fits[0].header['CLAMP2'] == 1 or fits[0].header['CLAMP3'] == 1 \
                or fits[0].header['CLAMP4'] == 1
            #objects.append(fits[0].header['object'].lower())
            #fits.close()
        #for j in objects:
            if 'bias' not in object_val and 'halogen' not in object_val and 'neon' not in \
                    object_val and 'helium' not in object_val and 'fear' not in object_val \
                    and not lamp_flag:
                FLAG = True
                for k in standard:
                    if k in object_val:
                        FLAG = False
                        break
                if FLAG == True:
                    realobj_lst.append(object_val)
        if len(realobj_lst) == 0:
            print('mv ' + i + ' other/')
            #os.system('mv ' + i + ' other/')
            shutil.move(i, os.getcwd() + os.sep + 'other' + os.sep + i)
        else:
            print(i + ' not move')
            for obj in realobj_lst:
                print(obj + ' is real object')

if __name__ == '__main__':
    main()
