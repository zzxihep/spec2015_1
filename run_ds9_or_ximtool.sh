#!/usr/bin/env bash

# if no instance of ds9 or ximtool run, this script will try to run ds9,
# if no ds9 is found, will try to run ximtool, else this script will do nothing

isinsds9=`ps -a | awk '{print $4}' | grep ds9 | grep -v grep`
isinsximtool=`ps -a | awk '{print $4}' | grep ximtool | grep -v grep`
if [[ $isinsds9 != "" ]]; then
    echo Already run ds9
    exit
fi
if [[ $isinsximtool != "" ]]; then
    echo Already run ximtool
    exit
fi
pathds9=`which ds9`
pathximtool=`which ximtool`
if [[ $pathds9 != "" ]]; then
    echo run ds9
    ds9 &
elif [[ $pathximtool != "" ]]; then
    echo run ximtool
    ximtool &
else
    echo "No ds9 and ximtool command found in this operating system !!"
fi
