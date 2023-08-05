#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################################
# Created Date : Tuesday October 19th 2021                                     #
# Author: Jingxin Fu (jingxin@broadinstitute.org)                              #
# ----------                                                                   #
# Last Modified: Tuesday October 19th 2021 7:55:52 pm                          #
# Modified By: Jingxin Fu (jingxin@broadinstitute.org)                         #
# ----------                                                                   #
# Copyright (c) Jingxin Fu 2021                                                #
################################################################################


__doc__=""" 
""" 
import setuptools
from scDB import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scDB",
    version=__version__,
    author="Jingxin Fu",
    author_email="jingxinfu.tj@gmail.com",
    description="single cell database utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://jingxinfu.github.io/scDB",
    packages=setuptools.find_packages(),
    scripts=['bin/scDB'],
    include_package_data=True,
    install_requires=['firecloud','tenacity','pandas','colorlog'],
    python_requires='>=3.4, <4',
    keywords=['single cell','terra'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ]
)
