#!/usr/bin/env python

from distutils.core import setup
import py2app
from dircache import listdir

# A list of files to include in the bundle.
files = ['amsn2', 'pymsn']

# Nibs need to be appened individually because they they need to be in the root of the bundle.
nibs = listdir('amsn2/gui/front_ends/cocoa/nibs/files/')
for nib in nibs:
    files.append('amsn2/gui/front_ends/cocoa/nibs/files/' + nib)

setup(
    name = 'aMSN2',
    app = ['amsn2.py'],
    data_files = files,
)
