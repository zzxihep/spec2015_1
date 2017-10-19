#!/usr/bin/env python

from pyraf import iraf


def main():
    print '='*20 + ' check wcal2d ' + '='*20
    iraf.imexamine('wftbo//@cor_halogen.lst', frame=1)


if __name__ == '__main__':
    main()
