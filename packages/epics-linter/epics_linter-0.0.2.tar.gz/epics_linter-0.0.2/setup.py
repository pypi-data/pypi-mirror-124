from __future__ import print_function, unicode_literals

import codecs
import os
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(file_paths, default=""):
    try:
        with codecs.open(os.path.join(here, *file_paths), "r") as fh:
            return fh.read()
    except Exception:
        return default


def find_version(file_paths):
    version_file = read(file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="epics_linter",
    version=find_version(["epics_linter", "__init__.py"]),
    url="https://github.com/cnpem-iot/epics-linter",
    license="GNU General Public License v3 or later (GPLv3+)",
    author="Guilherme F. de Freitas",
    author_email="guilherme.freitas@cnpem.br",
    description="EPICS Configuration Linter",
    long_description=read("README.md", default="EPICS Configuration Linter"),
    long_description_content_type="text/markdown",
    packages=["epics_linter"],
    include_package_data=True,
    platforms="any",
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
)
