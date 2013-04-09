#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup, find_packages
import airstrip

if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist upload')
    sys.exit()

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

requires = [
    'puke'
]

setup(
    name='AirStrip',
    version=airstrip.__version__,
    description='',
    long_description=open('README.md').read(),
    author='Education Numerique',
    author_email='tech@webitup.fr',
    url='http://education-numerique.github.com/api/',
    packages=find_packages(),
    scripts=[
        'airstrip/bin/airstrip'
    ],
    package_dir={'airstrip': 'airstrip'},
    package_data = {
        # If any package contains *.txt files, include them:
        '': ['*.json', '*.yaml']
    },
    include_package_data = True,

    install_requires=requires,
    license=open('LICENSE').read()
)
