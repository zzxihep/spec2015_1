#! /bin/sh
${0%/*}/mv_to_spec.py
cd spec
${0%/*}/classify_fits.py
${0%/*}/mv_to_other.py
${0%/*}/gen_lst.py
${0%/*}/check_lessing.py
${0%/*}/check_bad.py
${0%/*}/check_manual.py
${0%/*}/gen_zero.py
${0%/*}/re_all.py
cd ..
