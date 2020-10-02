#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='pycrskrun',
    version='1.0',
    description='',
    author='yomura',
    author_email='yomura@hoge.jp',
    url='https://github.com/yomura-yomura/pycrskrun',
    packages=[
        'distutils', 'distutils.command',
        "numpy", "pandas", 
    ],
)
