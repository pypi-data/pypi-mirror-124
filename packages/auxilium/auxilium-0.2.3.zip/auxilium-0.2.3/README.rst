
.. image:: https://raw.githubusercontent.com/sonntagsgesicht/auxilium/master/doc/pix/auxilium_logo.png

|codeship|_ |readthedocs|_ |license|_ |github_version|_ |pip_version|_
|py_version|_ |pypi_downloads|_

.. |codeship| image:: https://img.shields.io/codeship/5b8cc2e0-ac1d-0137-31a2-06d5e6117547/master.svg
.. _codeship: https://codeship.com//projects/362165

.. |readthedocs| image:: https://img.shields.io/readthedocs/auxilium
.. _readthedocs: https://auxilium.readthedocs.io/en/latest/intro.html

.. |license| image:: https://img.shields.io/github/license/sonntagsgesicht/auxilium
.. _license: https://github.com/sonntagsgesicht/auxilium/raw/master/LICENSE

.. |github_version| image:: https://img.shields.io/github/release/sonntagsgesicht/auxilium?label=github
.. _github_version: https://github.com/sonntagsgesicht/auxilium/releases

.. |pip_version| image:: https://img.shields.io/pypi/v/auxilium
.. _pip_version: https://pypi.org/project/auxilium/

.. |py_version| image:: https://img.shields.io/pypi/pyversions/auxilium
.. _py_version: https://pypi.org/project/auxilium/

.. |pypi_frequency| image:: https://img.shields.io/pypi/dm/auxilium
.. _pypi_frequency: https://pypi.org/project/auxilium/

.. |pypi_downloads| image:: https://pepy.tech/badge/auxilium
.. _pypi_downloads: https://pypi.org/project/auxilium/

A Python project for an automated test and deploy toolkit - 100% reusable.


Code, Documentation and Tests
-----------------------------

Modern software development comes as a triple of

.. image:: https://raw.githubusercontent.com/sonntagsgesicht/auxilium/master/doc/pix/code-test-doc.png

.. .. :alt: **code is for machines** // **tests links docs and code** // **docs are for humans**



* The **code** is the actual software program or library which can executed or
  invoked.

* The **documentation** should give an introducing the idea and mission,
  guide how to use it, describe functionality and features.

* Finally, intensive **tests** increases the confidence that the documented
  functionality is correctly implemented.


To support this **auxilium** is designed to build, to auto-doc, to test and
to deploy small to medium size Python projects in **3 simple steps**.

1. copy your **source code** into a boilerplate project structure

2. write useful **documentation** in your python source code doc strings

3. add as many as possible **test cases**
   in a designated test directory structure


What's in the box?
------------------

Once setup up, **auxilium** serves as a development and integration
workflow manager. It provides tools to run a ci/cd
(continuous integration/continuous deployment) framework with state-of-art
development and integration tools like

* source code management with `git <https://git-scm.com>`_

* python environment virtualization with
  `venv <https://docs.python.org/3/tutorial/venv.html>`_

* integrated dependency management with `pip <https://pip.pypa.io>`_

* source code quality and style validation with
  `flake8 <https://flake8.pycqa.org>`_

* source code security checks with `bandit <https://bandit.readthedocs.io>`_

* automated software testing with
  `unittest <https://docs.python.org/3/library/unittest.html>`_
  and `regtest <https://regtest.readthedocs.io>`_

* test coverage measurement with `coverage <http://coverage.readthedocs.io>`_

* automated documentation generation with `sphinx <https://sphinx-doc.org>`_

* documentation templates base on
  `restructuredtext <https://docutils.sourceforge.io/rst.html>`_
  markup language

* designed to work even at online sites like
  `PyPi.com <https://pypi.org>`_ and `GitHub <https://github.com>`_

* standard python distribution packaging with
  `build <https://pypa-build.readthedocs.io/en/stable/index.html>`_
  and `twine <https://twine.readthedocs.io/en/latest/>`_

* remote `git` repo management for
  `BitBucket <https://bitbucket.com>`_,
  `GitHub <https://github.com>`_,
  `GitLab <https://gitlab.com>`_

* single command software release deployment to `PyPi <https://pypi.org>`_
  the Python Package Index database


How does it work?
-----------------

* conventions on how the project is structured,
  i.e. where to find source, test and doc files

* provides useful template structure of files
  which can be easy modified and extended

* keeps always a single source of truth
  for project information (like version number)

* sets up a clear and straight structure of the project
  as well as the corresponding documentation

* minimises the places to edit,
  by default there are only three documentation files to be edited

* comes with a shell script to trigger plenty test and analysis routines
  incl. drafting pushing on git remotes and distribute on pypi.org

* uses standard community tools
  like *unittest*, *flake8*, *coverage*, *sphinx* and more

* no detailed configurations of any tools are needed,
  so you can focus completely on coding your project

* demo of how to use the framework and various services to build true *ci/cd*;
  a full automated test and deploy pipeline for the rest of us.

* creates and uses *venv* virtual environment to test
  on clean python installation

Moreover, we recommend to use *pyenv* and *virtualenv*
to test different python installations, too.


Quick Start a Project
---------------------

Once installed simply invoke :code:`auxilium create`
and enter a few project details.

The whole project structure will be created.
Full functioning incl. documentation generation, testing, etc..


.. code-block:: bash

    $ auxilium create

     Please enter project details.

    Enter project name   : unicorn
    Enter project slogan : Always be a unicorn.
    Enter project author : dreamer
    Enter project email  : dreamer@home
    Enter project url    : www.dreamer.home/unicorn

    Created project unicorn with these files:

      unicorn/CHANGES.rst
      unicorn/HOWTO.rst
      unicorn/LICENSE
      unicorn/MANIFEST.in
      unicorn/README.rst
      unicorn/requirements.txt
      unicorn/setup.py
      unicorn/upgrade_requirements.txt

      unicorn/doc/sphinx/conf.py
      unicorn/doc/sphinx/doc.rst
      unicorn/doc/sphinx/index.rst
      unicorn/doc/sphinx/intro.rst
      unicorn/doc/sphinx/logo.png
      unicorn/doc/sphinx/releases.rst
      unicorn/doc/sphinx/tutorial.rst

      unicorn/test/__init__.py
      unicorn/test/unittests.py

      unicorn/unicorn/__init__.py


Default Structure of a Project
------------------------------

The top level of the directory structure consists of three sub-dirs for source,
doc and test files and some more or less standard project files.
Assume the project is called *unicorn*.

.. code-block:: bash

   /unicorn (project root dir)

      /.aux/venv (virtual python environment)

      /unicorn (python source files)
      /doc/sphinx (sphinx files)
      /test/unittests (unittest files)

      LICENSE (license to use)

      CHANGES.rst (change history)
      HOWTO.rst (user guide)
      README.rst (introduction)

      requirements.txt (pip dependencies)
      upgrade_requirements.txt (pip dependencies which always have to be upgraded)

      setup.py (configuration file to build a distribution)
      MANIFEST.in (configuration file to build a distribution)

      .gitignore (configuration file - files and folder which git should ignore)

On top level there ate the following files

* **LICENSE** is the license how to use, change or distribute the project.

* **CHANGES.rst** will contain the whole change and release history

* **HOWTO.rst** gives a intro how to use your project.
  This will show up in your documentation as tutorial.

* **README.rst** is this page which
  shows up on repository homepage at first.
  Moreover, this will show up in your documentation as introduction, too.

* **requirements.txt** are additional python packages,
  which are required for development and/or testing

* **upgrade_requirements.txt** are additional python packages
  (same as *requirements.txt*), which have to be upgraded,
  i.e. installed by :code:`pip` with the *--upgrade* option.
  Usually used for dev repos.

* **setup.py** configs the installation procedure with pip
  and the meta keywords of your project on pypi.org.
  Most of the entries are found in the project **__init__.py** file.

* **MANIFEST.in** configs the files
  which will be part of the final distribution.

* **.gitignore** configs git which files and folder to ignore

and subdirectories

* **.aux/venv** which contains the virtual python environment

* **unicorn/** as the actual python source directory
  (place to put the python scripts)
  **Note, project root dir and python source dir must have the same name!**


* **doc/sphinx/** file read by sphinx to build documentation sites
  which can be extended, e.g. by :code:`auxilium doc --api`,
  but also manually.

* **test/** to contain all test scripts and data
  (by default there will be two:
  :code:`unittests.py` and :code:`regtests.py`)


As the actual python source files can be structured as you like inside

.. code-block:: bash

    unicorn/unicorn/

only few information on your project are required and should be found in

.. code-block:: bash

   unicorn/unicorn/__init__.py

Most of them are needed to setup the *pip* installation (using *setuptools*),
deployment to `PyPi.org <https://pypi.org>`_
as well as the sphinx configuration for generation a documentation.
See here how :code:`unicorn/unicorn/__init__.py` looks like.

.. code-block:: python

   # -*- coding: utf-8 -*-

   # unicorn
   # -------
   # Always be a unicorn.
   #
   # Author:   dreamer
   # Version:  0.1, copyright Thursday, 29 August 2019
   # Website:  https://github.com/dreamer/unicorn
   # License:  Apache License 2.0 (see LICENSE file)


   import logging

   logging.getLogger(__name__).addHandler(logging.NullHandler())

   __doc__ = 'Always be a unicorn.'
   __license__ = 'Apache License 2.0'

   __author__ = 'dreamer'
   __email__ = 'unicorn@home'
   __url__ = 'https://www.dreamer.home/unicorn'

   __date__ = 'Thursday, 29 August 2019'
   __version__ = '0.1'
   __dev_status__ = '3 - Alpha'

   __dependencies__ = ()
   __dependency_links__ = ()
   __data__ = ()
   __scripts__ = ()
   __theme__ = ''

Once setup up, update file headers of all new and modified files
and adding them to the project source code repository simply by
:code:`auxilium update`.


Automated Documentation Generation
----------------------------------

The documentation is generated by sphinx_
and the main documentation files is located at

.. code-block:: bash

   /auxilium (project root dir)

      /doc/sphinx (sphinx files)

**auxilium** extracts all docs from the source code file and links
to some top level *rst* files.

So usually no file under :code:`/doc/sphinx` requires to be edited.

The site-map of a documentation will look like this

.. code-block:: bash

   /index.rst
      /intro.rst     -> README.rst
      /tutorial.rst  -> HOWTO.rst
      /doc.rst       -> api/* (generated by *sphinx-apidoc* via :code:`auxilium doc --api`)
      /releases.rst  -> CHANGES.rst

The project has a configuration (*conf.py*) to build *html* and *latex* resp.
*pdf* documentation. The later requires a latex installation to work.

And **auxilium** will run and check *code-blocks* of code examples
of your documentation during doc build (*doctest*).

All this is executed by just one command :code:`auxilium doc`.

Since only **doc.rst** will not refer to a top level doc file of the project
it is generated from the source code.
So here the work starts to write good python doc strings
in your source code files.

But if a more *sphinx* specific file reps. documentation is preferred.
May be in order to provide detailed insights into the project:
Simply delete :code:`api/*` (if existing) and replace the contents
of **doc.rst**.

More on documentation can be found in the
`documentation <https://auxilium.readthedocs.io/en/latest/doc.html>`_.


Automated Test and Test Coverage Framework
------------------------------------------

Test are invoked by
`unittest discovery <https://docs.python.org/3/library/unittest.html#test-discovery>`_
which searches by default for files
containing :code:`unittest.TestCase` classes and process them.

Same for measuring the test coverage
using coverage_
source code security and quality
using bandit_
and flake8_.

.. code-block:: bash

   /unicorn (project root dir)

      /test/unittests (unittest files)

Run all tests and checks with :code:`auxilium test`.

More on testing can be found in the documentation_.


Automated Build and Deployment Framework
----------------------------------------

Once a project milestone is reached, docs are written
and all tests are successfully passed,
it is ready for deployment.

The default deployment platform is `PyPi.org <https://pypi.org>`_.
Before deploying a distribution package is build.
Moreover, it's time to update (*push* to) the project state to
a git remote repo like on
GitHub_, GitLab_ anf BitBucket_

Invoke this with :code:`auxilium build`.
To *push* and *deploy* add options :code:`--push` and :code:`--deploy`.

More on build and deployment can be found in the documentation_.


Installation
------------

The latest stable version can always be installed or updated via pip:

.. code-block:: bash

    $ pip install auxilium



Development Version
-------------------

The latest development version can be installed directly from GitHub:

.. code-block:: bash

    $ pip install --upgrade git+https://github.com/sonntagsgesicht/auxilium.git


Contributions
-------------

.. _issues: https://github.com/sonntagsgesicht/auxilium/issues
.. __: https://github.com/sonntagsgesicht/auxilium/pulls

Issues_ and `Pull Requests`__ are always welcome.


License
-------

.. __: https://github.com/sonntagsgesicht/auxilium/raw/master/LICENSE

Code and documentation are available according
to the Apache Software License (see LICENSE__).


