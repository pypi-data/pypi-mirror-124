#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='ctw',
    version='0.0.2',
    author='th35tr0n9',
    author_email='th35tr0n9@gmail.com',
    url='https://baidu.com',
    description=u'A script for count solidity codes.',
    packages=['ctw'],
    install_requires=['PrettyTable'],
    entry_points={
        'console_scripts': [
            'ctw=ctw:main',
        ]
    }
)