.. image:: https://img.shields.io/pypi/status/SemVerIt
    :alt: PyPI - Status

.. image:: https://img.shields.io/pypi/wheel/SemVerIt
    :alt: PyPI - Wheel

.. image:: https://img.shields.io/pypi/pyversions/SemVerIt
    :alt: PyPI - Python Version

.. image:: https://img.shields.io/github/v/release/hendrikdutoit/SemVerIt
    :alt: GitHub release (latest by date)

.. image:: https://img.shields.io/github/license/hendrikdutoit/SemVerIt
    :alt: License

.. image:: https://img.shields.io/github/issues-raw/hendrikdutoit/SemVerIt
    :alt: GitHub issues

.. image:: https://img.shields.io/pypi/dm/BEETest21
    :alt: PyPI - Downloads

.. image:: https://img.shields.io/github/search/hendrikdutoit/SemVerIt/GitHub hit
    :alt: GitHub Searches

.. image:: https://img.shields.io/codecov/c/gh/hendrikdutoit/SemVerIt
    :alt: CodeCov
    :target: https://app.codecov.io/gh/hendrikdutoit/SemVerIt

.. image:: https://img.shields.io/github/workflow/status/hendrikdutoit/SemVerIt/Pre-Commit
    :alt: GitHub Actions - Pre-Commit
    :target: https://github.com/hendrikdutoit/SemVerIt/actions/workflows/pre-commit.yaml

.. image:: https://img.shields.io/github/workflow/status/hendrikdutoit/SemVerIt/CI
    :alt: GitHub Actions - CI
    :target: https://github.com/hendrikdutoit/SemVerIt/actions/workflows/ci.yaml

.. image:: https://img.shields.io/testpypi/v/SemVerIt
    :alt: PyPi

Manipulate semantic versioning (SemVer)

    Manipulate semantic version numbers. Currently, it only allows for the "0.0.0" format and should be expanded to allow for the rest of the specification as well. See also https://semver.org/


============
Installation
============

To install the latest release on PyPI, simply run:

.. code-block:: bash

    $ pip install semverit


=========
Example 1
=========

.. code-block:: bash

    >>> import semverit
    >>> svit = semverit.SemVerIt()
    >>> print("{} - Initialize".format(svit.version))
    >>> print("{} -> {} - Bump patch version".format(svit.version, svit.bump_patch()))
    >>> print("{} -> {} - Bump minor version".format(svit.version, svit.bump_min()))
    >>> print("{} -> {} - Bump minor version again".format(svit.version, svit.bump_min()))
    >>> print("{} -> {} - Bump patch version".format(svit.version, svit.bump_patch()))
    >>> print("{} -> {} - Bump major version".format(svit.version, svit.bump_maj()))

=========
Example 2
=========

.. code-block:: bash

    >>> import semverit.semverit
    >>> print("{} - Initialize".format(svit.version))
    >>> print("{} -> {} - Bump patch version".format(svit.version, svit.bump_patch()))
    >>> print("{} -> {} - Bump minor version".format(svit.version, svit.bump_min()))
    >>> print("{} -> {} - Bump minor version again".format(svit.version, svit.bump_min()))
    >>> print("{} -> {} - Bump patch version".format(svit.version, svit.bump_patch()))
    >>> print("{} -> {} - Bump major version".format(svit.version, svit.bump_maj()))

=========
Example 3
=========

.. code-block:: bash

    >>> import semverit
    >>> import tempfile
    >>> _setup_py_contents = """import setuptools
        setuptools.setup(
        name="SemVerIt",
        version="2.3.4",
        author="Hendrik du Toit",
        author_email="hendrik@brightedge.co.za",
        description="Project description",
        long_description="Project long description",
        classifiers=[
         "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
         "Programming Language :: Python :: 3.10",
       ],
    )
    """
    >>> working_dir = tempfile.mkdtemp()
    >>> setup_py_pth = working_dir / "setup.py"
    >>> setup_py_pth.write_text(_setup_py_contents)
    >>> svit = semverit.SemVerIt(p_setup_py_pth=setup_pth)
    >>> print("{} - Initialize".format(svit.version))
    >>> print("{} -> {} - Bump patch version".format(svit.version,svit.bump_patch()))
    >>> print("{} -> {} - Bump minor version".format(svit.version,svit.bump_min()))
    >>> print("{} -> {} - Bump minor version again".format(svit.version, svit.bump_min()))
    >>> print("{} -> {} - Bump patch version".format(svit.version, svit.bump_patch()))
    >>> print("{} -> {} - Bump major version".format(svit.version, svit.bump_maj()))
