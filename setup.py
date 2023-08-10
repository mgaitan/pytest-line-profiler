#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import setup


def read(fname):
    return (Path(__file__).parent / fname).read_text()
    

setup(
    name='pytest-line-profiler',
    version='0.2.1',
    author='Martín Gaitán',
    author_email='gaitan@gmail.com',
    maintainer='Martín Gaitán',
    maintainer_email='gaitan@gmail.com',
    license='MIT',
    url='https://github.com/mgaitan/pytest-line-profiler',
    description='Profile code executed by pytest',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    py_modules=['pytest_line_profiler'],
    python_requires='>=3.7',
    install_requires=['pytest>=3.5.0', "line-profiler"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'line-profiler = pytest_line_profiler',
        ],
    },
)


