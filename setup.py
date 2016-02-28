#!/usr/bin/env python

from distutils.core import setup

setup(name='pydirl',
      version='0.1',
      description='Quick file sharing solution',
      license='GPLv3',
      install_requires=[ 'Flask', 'flask-bootstrap']
      py_modules = ['pydirl']
      )
