#!/usr/bin/env python


import os
import imp
from setuptools import Distribution
from setuptools import setup, find_packages
from setuptools.command.install import install

from distutils.core import setup
from distutils.command.install_scripts import install_scripts
from distutils import log



packages = find_packages(exclude=('tests', 'doc'))

provides = ['pymepixviewer',]


requires = [ 'pymepix','pyqtgraph']

install_requires = ['pymepix','pyqtgraph','numpy']



console_scripts = ['pymepixviewer=pymepixviewer.main:main']


entry_points = {'console_scripts': console_scripts,}


classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Unix',
    'Operating System :: OS Independent',
    'Topic :: Scientific/Engineering',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Environment :: X11 Applications :: Qt'
]

setup(name='pymepixviewer',
      author='CFEL-CMI group, et al (see AUTHORS)',
      author_email='cmidaq@cfel.de',
      maintainer='CFEL-CMI group',
      version='1.0',
      description='Timepix Data Acquisition GUI',
      download_url="https://stash.desy.de/projects/CMIPUBLIC/repos/timepix/browse",
      classifiers=classifiers,
      packages=packages,
      include_package_data=True,
      entry_points=entry_points,
      provides=provides,
      requires=requires,
      install_requires=install_requires,
)