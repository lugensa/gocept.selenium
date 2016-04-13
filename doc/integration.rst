Integration
===========

gocept.selenium provides integration with several web frameworks. Since version
1.1, however, the actual integration functionality has been extracted to
`gocept.httpserverlayer`_, so the recommended setup is to use one layer from
there that integrates with your application (see `gocept.httpserverlayer`_
documentation for details) and provides an HTTP server, and then stack the
layer from gocept.selenium on top of that, to provide the Selenium
integration::

    import gocept.httpserverlayer.wsgi
    import gocept.selenium
    from mypackage import App

    http_layer = gocept.httpserverlayer.wsgi.Layer(App())
    selenium_layer = gocept.selenium.RCLayer(
        name='SeleniumLayer', bases=(http_layer,))


    class TestWSGITestCase(gocept.selenium.RCTestCase):

        layer = selenium_layer

        def test_something(self):
            self.selenium.open('http://%s/foo.html' % self.selenium.server)
            self.selenium.assertBodyText('foo')

.. _`gocept.httpserverlayer`: http://pypi.python.org/pypi/gocept.httpserverlayer


The previous set of layers that provide both the HTTP server and Selenium in
one layer is still available. Different frameworks require different
dependencies; this is handled via setuptools extras of gocept.selenium (e.g.
for Grok integration you need to require ``gocept.selenium[grok]``). Generally,
you need a test layer that handles the setup, and then have your tests inherit
from the appropriate ``TestCase``.

WSGI
----

No extra requirements (simply ``gocept.selenium``).

This test layer takes a WSGI callable and runs it in a temporary HTTP server::

    import gocept.selenium.wsgi
    from mypackage import App

    test_layer = gocept.selenium.wsgi.Layer(App())

    class WSGIExample(gocept.selenium.RCTestCase):

        layer = test_layer

        def test_something(self):
            self.selenium.open('http://%s/foo.html' % self.selenium.server)
            self.selenium.assertBodyText('Hello world!')


Static files
------------

No extra requirements (simply ``gocept.selenium``).

This test case provides a temporary directory (as ``self.documentroot``) that
is served via HTTP where tests can put HTML files to examine::

    import gocept.selenium.static

    class StaticFilesExample(gocept.selenium.static.TestCase):

        def test_something(self):
            open(os.path.join(self.documentroot, 'foo.html'), 'w').write(
                'Hello World!')
                self.selenium.open('http://%s/foo.html' % self.selenium.server)
                self.selenium.assertBodyText('Hello world!')


Zope3 / ZTK (zope.app.wsgi)
---------------------------

If your ZTK application uses ``zope.app.wsgi.testlayer``, see `Grok`_ for
integrating ``gocept.selenium``.


Grok
----

Requires ``gocept.selenium[grok]``.

This test layer groks your package and sets everything up so Selenium can
access the application. You will probably want to setup your app in your test
setup::

    import gocept.selenium.grok
    import transaction

    selenium_layer = gocept.selenium.grok.Layer(my.package)

    class GrokExample(gocept.selenium.grok.TestCase):

        layer = selenium_layer

         def setUp(self):
             super(MyTest, self).setUp()
             root = self.getRootFolder()
             root['app'] = mypackage.App()
             transaction.commit()

         def test(self):
             self.selenium.open('/app')
             self.selenium.assertBodyText('Hello world!')



Zope 2
------

Requires ``gocept.selenium[zope2]``

This test layer requires ``Testing.ZopeTestCase.layer.ZopeLiteLayer`` and
provides an HTTP server for the tests. See
``gocept.selenium.zope2.tests.test_zope212`` for details how to set this up.


Zope 2 via WSGI
---------------

If your Zope 2 setup supports it, you can use the WSGI integration instead of a
specialised Zope 2 integration to run your tests.

You might see the following exception when running tests::

    File ".../repoze.retry-1.0-py2.7.egg/repoze/retry/__init__.py", line 55, in __call__
      cl = int(cl)
     ValueError: invalid literal for int() with base 10: ''

To fix it you can use an additional middleware around your WSGI
application: ``gocept.selenium.wsgi.CleanerMiddleware``. It also fixes an
issue with ``wsgiref``. See comments in the code for more information.


Zope 2 / Plone with plone.testing
---------------------------------

Requires ``gocept.selenium[plonetesting]``.

``gocept.selenium`` provides a ``plone.testing.Layer`` at
``gocept.selenium.plonetesting.SELENIUM`` that you can mix and match with your
other layers, see ``gocept.selenium.plonetesting.testing`` with
``gocept.selenium.plonetesting.tests.zope2``, and
``gocept.selenium.plonetesting.testing_plone`` with
``gocept.selenium.plonetesting.tests.plone{3,4}`` for details how to set this
up.


Converting Selenese HTML files
------------------------------

Selenium tests can be written in HTML tables.

Their syntax is a bit clunky. But their development and debugging is eased a
lot by using Selenium IDE Firefox extension. Selenium IDE provides both initial
recording of tests and stepping through those tests. However, HTML tests have a
main drawback: they are hard to include in a continuous integration system.

``gocept.selenium`` provides a script that converts a set of Selenium HTML
tests into a Python module with a ``TestCase`` (based on ``gocept.selenium``
and ``plone.testing``).

Using the ``converthtmltests`` script, the developer can use HTML tests --
written, debugged and maintained with the Selenium tools -- while being able to
easily include those Selenium tests in a continuous integration system.

Usage
~~~~~

::

    converthtmltests -l LAYER [options] directory

    options:
      -f FILE, --file=FILE  write tests to FILE
      -l LAYER, --layer=LAYER
                            full python import path to layer instance

The script gathers and converts all Selenium HTML tests found in the mentioned
directory.

The user must refer to a ``plone.testing`` layer by specifying its Python
import path. That layer is set on the test case generated in the Python module.

An output file can be specified. In case no output file name is specified,
the module produced is named ``tests_all_selenium.py``.
