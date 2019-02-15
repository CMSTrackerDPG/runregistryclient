#!/usr/bin/python
# -*- coding: utf-8 -*-

# © Copyright 2019 CERN
#
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file “LICENSE”
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

import codecs
import os
import re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open(os.path.join(here, "README.md")) as f:
    long_description = f.read()


setup(
    name="runregistryclient",
    version=find_version("runreg", "__init__.py"),
    desription="CERN CMS RunRegistry client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ptrstn/runregistryclient",
    author="Peter Stein",
    author_email="peter.stein@cern.ch",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
