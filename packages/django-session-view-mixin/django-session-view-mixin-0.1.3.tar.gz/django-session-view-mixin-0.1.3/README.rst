=============================
Django Session View Mixin
=============================

.. image:: https://badge.fury.io/py/django-session-view-mixin.svg/?style=flat-square
    :target: https://badge.fury.io/py/django-session-view-mixin

.. image:: https://readthedocs.org/projects/pip/badge/?version=latest&style=flat-square
    :target: https://django-session-view-mixin.readthedocs.io/en/latest/

.. image:: https://img.shields.io/coveralls/github/frankhood/django-session-view-mixin/master?style=flat-square
    :target: https://coveralls.io/github/frankhood/django-session-view-mixin?branch=master
    :alt: Coverage Status

Your project description goes here

Documentation
-------------

The full documentation is at https://django-session-view-mixin.readthedocs.io.

Quickstart
----------

Install Django Session View Mixin::

    pip install django-session-view-mixin

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'session_view_mixin',
        ...
    )


Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
