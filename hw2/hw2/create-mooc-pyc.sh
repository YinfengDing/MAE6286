#!/usr/bin/env bash

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"

hwdir=$scriptdir

python -m compileall $hwdir/mooc.py

destdir=$hwdir

#cp $hwdir/__pycache__/mooc.cpython-36.pyc $destdir/mooc36.pyc
#cp $hwdir/__pycache__/mooc.cpython-37.pyc $destdir/mooc37.pyc
cp $hwdir/__pycache__/mooc.cpython-38.pyc $destdir/mooc38.pyc


