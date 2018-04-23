# -*- coding: utf-8 -*-
# Learn more: https://github.com/zinob/RPI_SGP30

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    name='sgp30',
    description='Library for reading data from the sensiron SGP30',
    version='0.1.5',
    long_description=readme,
    author='Simon Albinsson',
    author_email='pipmon@zinob.se',
    url='https://github.com/zinob/RPI_SGP30',
    license='MIT',
    packages=find_packages(exclude=('tests')),
    install_requires=['smbus2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='sgp30 i2c smbus smbus2',
)
