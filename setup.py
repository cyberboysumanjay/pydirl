#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pydirl',
    version='0.3.2',
    description='Quick file sharing solution',
    license='GPLv3',
    url='https://github.com/ael-code/pydirl',
    install_requires=['flask-bootstrap < 4',
                      'flask',
                      'gevent',
                      'click',
                      'zipstream'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={'console_scripts': ['pydirl=pydirl.cli:pydirl']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Flask',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: File Sharing']
)
