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
    version='0.1.3-a',
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
        'License :: OSI Approved :: MIT License'
    ],
    keywords='sgp30 i2c smbus smbus2',

)
