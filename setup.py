#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='cloudmetrics',
    version='0.0.4',
    description='Send metrics to CloudWatch.',
    author='Raymond Butcher',
    author_email='randomy@gmail.com',
    url='https://github.com/raymondbutcher/cloudmetrics',
    license='MIT',
    packages=find_packages(),
)
