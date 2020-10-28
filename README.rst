===============
gocept.selenium
===============

.. image:: https://readthedocs.org/projects/goceptselenium/badge/?version=latest
    :target: https://goceptselenium.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://travis-ci.com/gocept/gocept.selenium.svg?branch=master
    :target: https://travis-ci.com/gocept/gocept.selenium
.. image:: https://coveralls.io/repos/github/gocept/gocept.selenium/badge.svg
    :target: https://coveralls.io/github/gocept/gocept.selenium
.. image:: https://img.shields.io/pypi/v/gocept.selenium.svg
        :target: https://pypi.org/project/gocept.selenium/
        :alt: Current version on PyPI
.. image:: https://img.shields.io/pypi/pyversions/gocept.selenium.svg
        :target: https://pypi.org/project/gocept.selenium/
        :alt: Supported Python versions

gocept.selenium provides an API for `Selenium`_ that is
suited for writing tests and integrates this with your test suite for any WSGI,
Plone or Grok application.

While the testing API could be used independently, the integration is done
using `test layers`_, which are a feature of `zope.testrunner`_.

Use `gocept.pytestlayer`_ to integrate it with `pytest`_.


.. _`Selenium`: http://seleniumhq.org/
.. _`test layers`: http://pypi.python.org/pypi/plone.testing#layers
.. _`zope.testrunner`: http://pypi.python.org/pypi/zope.testrunner
.. _`gocept.pytestlayer`: https://bitbucket.org/gocept/gocept.pytestlayer
.. _`pytest`: http://pytest.org
