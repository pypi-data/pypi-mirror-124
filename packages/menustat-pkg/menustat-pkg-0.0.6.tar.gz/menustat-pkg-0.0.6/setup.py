# -*- coding: utf-8 -*-

import os
from setuptools import find_packages


requires = [
  'beautifulsoup4==4.9.3',
  'camelot-py[base]==0.9.0',
  'chromedriver-autoinstaller',
  'chromedriver-binary',
  'ghostscript',
  'html5lib==1.1',
  'lxml==4.6.2',
  'oauthlib==3.1.1',
  'opencv-python',
  'pandas==1.3.2',
  'python-levenshtein==0.12.2',
  'pyyaml==5.4.1',
  'rapidfuzz==1.7.1',
  'requests',
  'selenium==3.141.0',
  'sqlalchemy==1.4.22',
  'tqdm==4.62.1',
  'urllib3==1.26.6',
]
def setup_package():
    metadata = dict(
        name="menustat-pkg",
        version="0.0.6",
        # description=about["__description__"],
        # long_description=readme,
        # long_description_content_type="text/markdown",
        # url=about["__url__"],
        author="Claire Peters",
        author_email="clairepeters@g.harvard.edu",
        license="BSD License",
        packages=find_packages(exclude=("tests",)),
        install_requires=requires,
        classifiers=[
            # Trove classifiers
            # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
        ],
    )

    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

    setup(**metadata)


if __name__ == "__main__":
    setup_package()
