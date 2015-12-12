# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 15:34:06 2015

@author: H.Gens

https://python-packaging.readthedocs.org/en/latest/index.html
https://gist.github.com/dupuy/1855764
https://python-packaging-user-guide.readthedocs.org/en/latest
       /distributing/#choosing-a-versioning-scheme
"""
from setuptools import setup


def readme():
    with open('README_package.rst') as f:
        return f.read()


setup(
	name='matplotgrid',
	version=0.1,
	description='Creates a grid of independent matplotlib windows',
	long_description=readme(),
	url='http://github.com/h-gens/matplotgrid',
	author='H.Gens',
	author_email='h.gens2@gmail.com',
	license='MIT',
	packages=['matplotgrid'],
	install_requires=[
		'screeninfo',
	],
	keywords='matplotlib plotting tile grid',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python',
		'Topic :: Scientific/Engineering',
	],
	zip_safe=False,
)
