#!/usr/bin/env python

from setuptools import setup


SETUP_REQUIRES = [
    "setuptools>=36",
    "pytest-runner",
]


setup(
    name="zconnectmqttauth",

    setup_requires=SETUP_REQUIRES,
)
