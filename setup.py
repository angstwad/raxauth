#!/usr/bin/env python
from setuptools import setup, find_packages
from raxauth import __version__

setup(name='raxauth',
      version=__version__,
      description='Rackspace Cloud Authentication Module for Python',
      author='Paul Durivage',
      author_email='pauldurivage@gmail.com',
      url='https://github.com/angstwad/raxauth',
      license='GPL',
      package_dir = {'raxauth': 'raxauth/'},
      packages=['raxauth'],
      )
