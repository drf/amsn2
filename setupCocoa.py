#!/usr/bin/env python

from distutils.core import setup
import py2app
from dircache import listdir

# A list of files to include in the bundle.
files = ['amsn2', 'papyon']

# Nibs need to be appened individually because they they need to be in the root of the bundle.
for f in listdir('amsn2/gui/front_ends/cocoa/nibs/files/'):
    files.append('amsn2/gui/front_ends/cocoa/nibs/files/' + f)

setup(
    name = 'aMSN2',
    app = ['amsn2.py'],
    data_files = files,
)
