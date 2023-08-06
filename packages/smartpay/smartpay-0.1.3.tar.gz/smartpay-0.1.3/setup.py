#!/usr/bin/env python

import os
from setuptools import setup, find_packages

ROOT = os.path.dirname(os.path.abspath(__file__))

VERSION = "0.1.3"

setup(
    name="smartpay",
    version=VERSION,
    author="Smartpay Co. Ltd.",
    author_email="uxe@smartpay.co",
    url="https://github.com/smartpay-co/sdk-python",
    description="Smartpay SDK Python",
    long_description=open(os.path.join(ROOT, "README.md")).read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["smartpay", "smartpay.schemas"],
    package_data={'': ['*.json']},
    install_requires=["requests==2.25.1",
                      "jtd == 0.1.1"],
)
