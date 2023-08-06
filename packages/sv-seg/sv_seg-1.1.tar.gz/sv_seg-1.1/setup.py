# -*- coding: UTF-8 -*-
"""
Copyright (c) Yuwei Jin
Created at 2021-10-24 16:45 
Written by Yuwei Jin (642281525@qq.com)
"""

from setuptools import find_packages, setup

setup(
    name="sv_seg",
    version="1.1",
    description="A simplified version library for deep learning in semantic segmentation",
    author="jyw",
    license='MIT',
    repository='https://upload.pypi.org/legacy/',
    packages=find_packages(),
    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: System :: Logging',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
    # py_modules=['config_samples', 'libs', 'modules']
)
