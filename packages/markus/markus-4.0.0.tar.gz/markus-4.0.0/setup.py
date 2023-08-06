#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import os
import re
import sys
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        pytest_args = shlex.split(self.pytest_args) if self.pytest_args else []
        errno = pytest.main(pytest_args)
        sys.exit(errno)


def get_version():
    fn = os.path.join("src", "markus", "__init__.py")
    vsre = r"""^__version__ = ['"]([^'"]*)['"]"""
    version_file = open(fn).read()
    return re.search(vsre, version_file, re.M).group(1)


def get_file(fn):
    with open(fn) as fp:
        return fp.read()


INSTALL_REQUIRES = []
EXTRAS_REQUIRE = {
    "datadog": ["datadog"],
    "statsd": ["statsd"],
    "dev": [
        "black==21.9b0",
        "check-manifest==0.47",
        "flake8==4.0.1",
        "freezegun==1.1.0",
        "pytest==6.2.5",
        "Sphinx==4.2.0",
        "tox==3.24.4",
        "tox-gh-actions==2.8.1",
        "twine==3.4.2",
        "wheel==0.37.0",
    ],
}
TESTS_REQUIRES = ["pytest"]

setup(
    name="markus",
    version=get_version(),
    description="Metrics system for generating statistics about your app",
    long_description=(get_file("README.rst") + "\n\n" + get_file("HISTORY.rst")),
    author="Will Kahn-Greene",
    author_email="willkg@mozilla.com",
    url="https://github.com/willkg/markus",
    project_urls={
        "Documentation": "https://markus.readthedocs.io/",
        "Source": "https://github.com/willkg/markus/",
        "Tracker": "https://github.com/willkg/markus/issues",
    },
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    tests_requires=TESTS_REQUIRES,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    cmdclass={"test": PyTest},
    include_package_data=True,
    license="MPLv2",
    zip_safe=False,
    python_requires=">=3.7",
    keywords="metrics datadog statsd",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
