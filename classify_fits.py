#!/usr/bin/env python

import os,shutil
import pyfits

def main():
    #ifitsname = os.popen('ls *.fits').readlines()
    ifitsname = os.listdir(os.getcwd())
    #fitsnames = [ i.split('\n')[0] for i in ifitsname ]
    fitsnames = [i for i in ifitsname if os.path.isfile(i) and i[-5:] == '.fits']
    dirnames  = {'bias':[]}
    for i in fitsnames:
        fits = pyfits.open(i)
        hdr  = fits[0].header
        if 'bias' in hdr['object'].lower():
            dirnames['bias'].append(i)
        else:
            dirname = (hdr['YGRNM'] + '_' + hdr['YAPRTNM']).replace(' ', '_')
            if dirnames.has_key(dirname):
                dirnames[dirname].append(i)
            else:
                dirnames[dirname] = [i]
    for i in dirnames:
        print ('mkdir ' + i)
	#os.system("mkdir " + i)
        os.mkdir(i)
        for name in dirnames[i]:
            print ('mv ' + name + ' ' + i)
            #os.system('mv ' + name + ' ' + i + '/')
            shutil.move(name, os.getcwd() + os.sep + i + os.sep + name)

if __name__ == '__main__':
    main()
