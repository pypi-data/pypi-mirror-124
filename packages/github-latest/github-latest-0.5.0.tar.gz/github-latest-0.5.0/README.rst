========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-github_latest/badge/?style=flat
    :target: https://python-github_latest.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/TaylorMonacelli/python-github_latest.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/TaylorMonacelli/python-github_latest

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/TaylorMonacelli/python-github_latest?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/TaylorMonacelli/python-github_latest

.. |requires| image:: https://requires.io/github/TaylorMonacelli/python-github_latest/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/TaylorMonacelli/python-github_latest/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/TaylorMonacelli/python-github_latest/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/TaylorMonacelli/python-github_latest

.. |version| image:: https://img.shields.io/pypi/v/github-latest.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/github-latest

.. |wheel| image:: https://img.shields.io/pypi/wheel/github-latest.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/github-latest

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/github-latest.svg
    :alt: Supported versions
    :target: https://pypi.org/project/github-latest

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/github-latest.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/github-latest

.. |commits-since| image:: https://img.shields.io/github/commits-since/TaylorMonacelli/python-github_latest/v0.5.0.svg
    :alt: Commits since latest release
    :target: https://github.com/TaylorMonacelli/python-github_latest/compare/v0.5.0...master



.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install github-latest

You can also install the in-development version with::

    pip install https://github.com/TaylorMonacelli/python-github_latest/archive/master.zip


Documentation
=============


https://python-github_latest.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
