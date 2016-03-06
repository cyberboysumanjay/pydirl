#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pydirl',
    version='0.1',
    description='Quick file sharing solution',
    license='GPLv3',
    url='https://github.com/ael-code/pydirl',
    install_requires=['flask-bootstrap',
                      'flask',
                      'gevent',
                      'click',
                      'zipstream'],
    packages = find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={'console_scripts': [ 'pydirl=pydirl.cli:pydirl']}
)
