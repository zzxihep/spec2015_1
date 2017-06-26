#!/usr/bin/env bash

if ! [ -d telluric ]; then
  mkdir telluric;
fi;
cp awftbo* telluric/
cd telluric
${0%/*}/cor_telluric.py
