# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='betable events',
    version='0.1.0',
    description='Simple structure for handling events that can be bet on',
    long_description=readme,
    author='Daniel Harris',
    author_email='dannyray44@hotmail.co.uk',
    url='https://github.com/dannyray44/betable_event',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
