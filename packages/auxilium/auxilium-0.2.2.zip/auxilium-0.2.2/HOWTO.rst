
.. currentmodule:: auxilium

under construction..

auxilium cli
============

* general workflow (create [code] update test [write] doc build [--deploy])
* general cli
* use of .aux/config

auxilium create
---------------

* auxilium create --update (usage in ci/existing projects)
* use of venv activate/deactivate resp. :code:`auxilium python`
* default location .aux/venv


auxilium update
---------------

* version numbers in __init__.py (docmaintain/header)
* use if .aux/last.json
* commit (use of git)
* tag -> push

auxilium test
-------------

* lint/security check
* use of unittest
* use of regtest
* coverage

auxilium doc
------------

* general rst intro
* use of __theme__
* use of sphinx_math_dollar
* use of sphinx_pytype_substitution
* doctest
* coverage
* html/epub/latex (readthedocs)
* Avoid :code:`.. doctest::` *rst*-directive and :code:`|something|`
  links in README.rst. This would fail with `setuptools` to serve
  as `long_description` for `pypi.org <https://pypi.org>`_.

auxilium build
--------------

* docmaintain
* build (dist)
* push (branch) + draw release
* deploy (creates or updates pypi.org)
