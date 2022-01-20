# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='EvilWordle',
    version='0.1.1',
    description='Attempt at recreating the Evil version of Wordle',
    long_description=readme,
    author='Kyle Patterson',
    url='https://github.com/kylekap/EvilWordle',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)