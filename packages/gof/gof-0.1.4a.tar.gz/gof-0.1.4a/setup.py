#!/usr/bin/env pyrhon
# -*- coding: "utf-8" -*-

from distutils.command.build_py import build_py as _build_py
from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
        name='gof',
        version='0.1.4a',
        author='Julien Tayon',
        author_email='julien@tayon.net',
        packages=['gof'],
        url='http://gof.readthedocs.org/',
        license='LICENSE.txt',
        description='''a little fun with Conway's Game Of Life''',
        long_description=long_description,
        requires=[ ],
        classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          ],
)
