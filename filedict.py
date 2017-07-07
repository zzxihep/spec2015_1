#!/usr/bin/env python

import os
import numpy as np


class filedict:
    pathfilestr = ''
    idict = {}

    def __init__(self, filepathname):
        self.pathfilestr = filepathname
        self.idict = dict(np.genfromtxt(self.pathfilestr, str))

    def __getitem__(self, strindex):
        while strindex not in self.idict:
            print('not find ' + strindex + ' in ' + self.pathfilestr +
                  ' please edit the file and the routine will try again')
            os.popen('gedit ' + self.pathfilestr)
            self.idict = dict(np.genfromtxt(self.pathfilestr, str))
        return self.idict[strindex]
