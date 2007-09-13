import sys
import os

from ez_setup import use_setuptools
use_setuptools('0.6c3')

import distutils
from setuptools import setup, find_packages, Extension
import commands

python_inc = distutils.sysconfig.get_python_inc()

def pkgconfig(*packages, **kw):
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
    pkgs = ' '.join(packages)
    cmdline = 'pkg-config --libs --cflags %s' % pkgs

    status, output = commands.getstatusoutput(cmdline)
    if status != 0:
        raise ValueError("could not find pkg-config module: %s" % pkgs)

    for token in output.split():
        kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])
    return kw


etkmodule = Extension('etk.c_etk',
                       sources=['etk/etk.c_etk.pyx',
                                ],
                       depends=['etk/etk.c_etk.pxd',
                                'etk/signal_callback.pxd',
                                'etk/signal.pxd',
                                'etk/types.pxd',
                                'etk/type.pxi',
                                'etk/type.pxd',
                                'etk/object.pxi',
                                'etk/object.pxd',
                                'etk/widget.pxi',
                                'etk/widget.pxd',
                                'etk/stock.pxd',
                                'etk/bin.pxi',
                                'etk/bin.pxd',
                                'etk/box.pxi',
                                'etk/box.pxd',
                                'etk/image.pxi',
                                'etk/image.pxd',
                                'etk/button.pxi',
                                'etk/button.pxd',
                                'etk/table.pxi',
                                'etk/table.pxd',
                                'etk/window.pxi',
                                'etk/window.pxd',
                                'etk/toplevel.pxi',
                                'etk/toplevel.pxd',
                                'etk/container.pxi',
                                'etk/container.pxd',
                                'etk/embed.pxi',
                                'etk/embed.pxd',
                                'etk/label.pxi',
                                'etk/label.pxd',
                                'etk/combobox.pxi',
                                'etk/combobox.pxd',
                                'etk/combobox_entry.pxi',
                                'etk/combobox_entry.pxd',
                                'etk/progress_bar.pxi',
                                'etk/progress_bar.pxd',
                                'etk/slider.pxi',
                                'etk/slider.pxd',
                                'etk/frame.pxi',
                                'etk/frame.pxd',
                                'etk/entry.pxi',
                                'etk/entry.pxd',
                                'etk/toggle_button.pxi',
                                'etk/toggle_button.pxd',
                                'etk/event.pxi',
                                'etk/event.pxd',
                                'etk/canvas.pxi',
                                'etk/canvas.pxd',
                                'etk/python.pxd',
                                ],
                       **pkgconfig('"etk >= 0.1.0.005"'))

include_dirs = [os.path.join(python_inc, "python-evas")]
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

setup(name = 'python-etk',
      version = '0.0.1',
      license = 'BSD',
      author='Caio Marcelo de Oliveira Filho',
      author_email='cmarcelo@gmail.com',
      url='http://www.enlightenment.org/',
      description = 'Python bindings for Etk',
      long_description = long_description,
      keywords = 'wrapper binding ui etk graphics',
      classifiers = trove_classifiers,
      packages = find_packages(),
      install_requires = ['python-evas>=0.1.1'],
      setup_requires = ['python-evas>=0.1.1'],
      include_dirs = include_dirs,
      headers = headers,
      ext_modules = [etkmodule],
      zip_safe=False,
      )
