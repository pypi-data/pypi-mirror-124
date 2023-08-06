.. image:: https://img.shields.io/pypi/status/ReleaseIt
    :alt: PyPI - Status

.. image:: https://img.shields.io/pypi/wheel/ReleaseIt
    :alt: PyPI - Wheel

.. image:: https://img.shields.io/pypi/pyversions/ReleaseIt
    :alt: PyPI - Python Version

.. image:: https://img.shields.io/github/v/release/hendrikdutoit/ReleaseIt
    :alt: GitHub release (latest by date)

.. image:: https://img.shields.io/github/license/hendrikdutoit/ReleaseIt
    :alt: License

.. image:: https://img.shields.io/github/issues-raw/hendrikdutoit/ReleaseIt
    :alt: GitHub issues

.. image:: https://img.shields.io/pypi/dm/BEETest21
    :alt: PyPI - Downloads

.. image:: https://img.shields.io/github/search/hendrikdutoit/ReleaseIt/GitHub hit
    :alt: GitHub Searches

.. image:: https://img.shields.io/codecov/c/gh/hendrikdutoit/ReleaseIt
    :alt: CodeCov
    :target: https://app.codecov.io/gh/hendrikdutoit/ReleaseIt

.. image:: https://img.shields.io/github/workflow/status/hendrikdutoit/ReleaseIt/Pre-Commit
    :alt: GitHub Actions - Pre-Commit
    :target: https://github.com/hendrikdutoit/ReleaseIt/actions/workflows/pre-commit.yaml

.. image:: https://img.shields.io/github/workflow/status/hendrikdutoit/ReleaseIt/CI
    :alt: GitHub Actions - CI
    :target: https://github.com/hendrikdutoit/ReleaseIt/actions/workflows/ci.yaml

.. image:: https://img.shields.io/testpypi/v/ReleaseIt
    :alt: PyPi

Project Short Description (default ini)

    Project long description or extended summary goes in here (default ini)

============
Installation
============

To install the latest release on PyPI, simply run:

.. code-block:: bash

    $ pip install releaseit


=======
Example
=======

.. code-block:: bash

    >>> import releaseit
    >>> import tempfile
    >>> from pathlib import Path
    >>> releaseit = releaseit.ReleaseIt('ReleaseIt', Path(tempfile.mkdtemp()))
    >>> releaseit.release_pth
    >>> print(releaseit.release_cfg)
