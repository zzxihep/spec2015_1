#!/usr/bin/env python

import pyfits
import numpy as np
import matplotlib.pyplot as plt

def sspecplot(filename):
	fit = pyfits.open(filename)
	num = fit[0].data.shape[1]
	y = fit[0].data[0][0] + 2500
	y2= fit[0].data[1][0]
	length = len(y)
	begin = fit[0].header['CRVAL1']
	step  = fit[0].header['CD1_1']
	print('begin from ' + str(begin))
	print('step is ' + str(step))
	x = np.linspace(begin, begin+length*step,
			length, endpoint = False)
	print('end ' + str(x[-1]))
	plt.ion()
	plt.plot(x,y, color = 'red')
	plt.plot(x,y2, color = 'green')
	plt.show()
