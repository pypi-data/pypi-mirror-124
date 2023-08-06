#!/usr/bin/env python3
"""ai-common setup script."""
from setuptools import setup, find_packages

setup(
    name="ai-common",
    version="0.0.1",
    author="TIKI GmbH",
    author_email="info@tiki-institut.com",
    description="AI platform helper library",
    long_description="Blank ai-common library.",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    url="https://bitbucket.org/TIKI-Institut/ai-common-python",
    packages=find_packages(exclude=["tests"])
)
