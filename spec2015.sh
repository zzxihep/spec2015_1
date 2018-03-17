#! /bin/bash

# @Author: zhixiang zhang <zzx>
# @Date:   08-Jan-2017
# @Email:  zhangzx@ihep.ac.cn
# @Filename: spec2015.sh
# @Last modified by:   zzx
# @Last modified time: 02-Jul-2017

${0%/*}/run_ds9_or_ximtool.sh
${0%/*}/cp_to_spec.py
cd spec
${0%/*}/classify_fits.py
${0%/*}/mv_to_other.py
${0%/*}/gen_lst.py
${0%/*}/check_missing.py
${0%/*}/check_bad.py
${0%/*}/check_manual.py
${0%/*}/gen_zero.py
for dirname in `ls`; do
  if [ -d $dirname ] && [ $dirname != bias ] && [ $dirname != other ]; then
    cd $dirname
    echo current dir `pwd`
    ${0%/*}/cor_ftbo_2017.py
    ${0%/*}/sltcomblamp.py
    ${0%/*}/sltwcalib2d.py
    ${0%/*}/check_wcal2d.py
    ${0%/*}/re_apall.py
    ${0%/*}/re_corflux.py
    cd ..
  fi
done
cd ..
