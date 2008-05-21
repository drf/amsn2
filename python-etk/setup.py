import sys
import os

from ez_setup import use_setuptools
use_setuptools('0.6c3')

from setuptools import setup, find_packages, Extension
from distutils.sysconfig import get_python_inc
from glob import glob
import commands

from Cython.Distutils import build_ext

def pkgconfig(*packages, **kw):
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
    pkgs = ' '.join(packages)
    cmdline = 'pkg-config --libs --cflags %s' % pkgs

    status, output = commands.getstatusoutput(cmdline)
    if status != 0:
        raise ValueError("could not find pkg-config module: %s" % pkgs)

    for token in output.split():
        if flag_map.get(token[:2]):
            kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])
        elif token.startswith("-Wl,"):
            kw.setdefault("extra_link_args", []).append(token)
        else:
            kw.setdefault("extra_compile_args", []).append(token)
    return kw


etkmodule = Extension('etk.c_etk',
                       sources=['etk/etk.c_etk.pyx'],
                       depends=glob('include/etk/*.pxd') + \
                          glob('etk/core/*.pxi'),
                       **pkgconfig('"etk >= 0.1.0.042"'))

headers = []

trove_classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console :: Framebuffer",
    "Environment :: X11 Applications",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX",
    "Programming Language :: C",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: User Interfaces",
    ]

long_description = """\
Python bindings for Etk, an EFL-based toolkit.
"""


class etk_build_ext(build_ext):
    def finalize_options(self):
        build_ext.finalize_options(self)
        self.include_dirs.insert(0, 'include')
        self.pyrex_include_dirs.extend(self.include_dirs)


setup(name = 'python-etk',
      version = '0.1.1',
      license = 'BSD',
      author='Caio Marcelo de Oliveira Filho',
      author_email='cmarcelo@gmail.com',
      url='http://www.enlightenment.org/',
      description = 'Python bindings for Etk',
      long_description = long_description,
      keywords = 'wrapper binding ui etk graphics',
      classifiers = trove_classifiers,
      packages = find_packages(),
      install_requires = ['python-evas>=0.2.1', 'python-ecore>=0.2.1'],
      setup_requires = ['python-evas>=0.2.1', 'python-ecore>=0.2.1'],
      headers = headers,
      ext_modules = [etkmodule],
      zip_safe=False,
      cmdclass = {'build_ext': etk_build_ext},
      )
