Selenium RC integration with zope.testing
=========================================

gocept.selenium integrates Selenium RC with your Plone/Zope 2/ZTK/Grok test
suite.


Quick start with ZTK
--------------------

Assuming that you already have a package that uses zc.buildout and
zope.testing, you need to do this to enable Selenium tests:

1. Add gocept.selenium to the list of eggs either in your setup.py, or in
   buildout.cfg, using the extra ``ztk``, i.e. ``gocept.selenium[ztk]``.

2. Install Selenium RC by some means, e.g. by downloading a version from
   `seleniumhq.org`_ . We do not recommend using the
   ``collective.recipe.seleniumrc`` buildout recipe for
   this since we have had some bad experiences with it related to new
   versions of Selenium RC and Firefox.

.. _`seleniumhq.org`: http://seleniumhq.org/download/

3. Run buildout to install gocept.selenium and selenium (the Python bindings
   for Selenium RC).

4. Create a layer for your tests, like this::

    import gocept.selenium.ztk
    import zope.app.testing.functional
    zcml_layer = zope.app.testing.functional.ZCMLLayer(
        'ftesting.zcml',
        __name__, __name__, allow_teardown=True)
    selenium_layer = gocept.selenium.ztk.Layer(zcml_layer)

  Essentially, the ``zcml_layer`` is what you would use for typical ZTK
  functional tests, and then you wrap it to create ``selenium_layer``.

5. Start writing tests that inherit ``gocept.selenium.ztk.TestCase``; make
   sure you set the ``layer`` attribute to ``selenium_layer`` on each test
   class.

6. In your tests, use ``self.selenium`` to control Selenium RC, e.g. ::

    class MyTest(gocept.selenium.ztk.TestCase):

        layer = selenium_layer

        def test(self):
            self.selenium.open('http://%s/foo.html' % self.selenium.server)
            self.selenium.assertBodyText('foo')

7. Run seleniumrc: java -jar /path/to/selenium-server.jar

8. Run bin/test and see it work!


Quick start with Zope 2/Plone
-----------------------------

Essentially the same, only use gocept.selenium.zope2 or gocept.selenium.plone
instead of gocept.selenium.ztk.


Quick start with Grok
---------------------

The layer works a little different than in the ZTK steps above, instead of
delegating to a (probably alredy existing functional-testing) layer, you'll
need a separate one for the Selenium tests.

1. Use the ``grok`` extra when requiring gocept.selenium.

4. Create a layer for your tests::

    import gocept.selenium.grok

    selenium_layer = gocept.selenium.grok.Layer(my.package)

5. Inherit from `gocept.selenium.grok.TestCase`. You will probably want to
   setup your app in your test setup::

    import transaction

    class MyTest(gocept.selenium.grok.TestCase):
        layer = selenium_layer

         def setUp(self):
             super(MyTest, self).setUp()
             root = self.getRootFolder()
             root['app'] = mypackage.App()
             transaction.commit()

         def test(self):
             self.selenium.open('/app')
             self.selenium.assertBodyText('foo')

The Grok Layer is based on a WSGI layer. You can test WSGI applications with
gocept.selenium by following the steps described above and substituting:

1. Use the ``wsgi`` extra when requiring gocept.selenium.

4. Create a layer for your tests::

    import gocept.selenium.wsgi

    from mypackage import App

    test_layer = gocept.selenium.wsgi.Layer(App())

5. Inherit from `gocept.selenium.wsgi.TestCase`::

    class TestWSGITestCase(gocept.selenium.wsgi.TestCase):

        layer = test_layer

Quick start with plone.testing
------------------------------

1. Use the ``plonetesting`` extra when requiring gocept.selenium.

4. gocept.selenium provides a plone.testing.Layer,
   ``gocept.selenium.plonetesting.SELENIUM`` that you can mix and match with
   your other layers, see plonetesting.testing/plonetesting.tests.zope2 and
   plonetesting.testing_plone/plonetesting.tests.plone{3,4} for some examples
   of integrating with Zope2 and Plone, respectively.

Selenium HTML tests conversion script
-------------------------------------

Selenium tests can be written in HTML tables. 

Their syntax is a bit clunky. But their development and debugging is eased a
lot by using Selenium IDE Firefox extension. 
Selenium IDE provides both initial recording of tests and stepping through 
those tests.
However, HTML tests have a main drawback : they are hard to include in a
continuous integration system.

``gocept.selenium`` provides a script that converts a set of
Selenium HTML tests into a Python module (based on ``gocept.selenium`` and
``plone.testing``). That Python module contains a ``TestCase`` that can be included in any
``zope.testing`` test suite.

Using the ``converthtmltests`` script, the developer can use HTML tests - written, 
debugged and maintained with the Selenium tools -
while being able to easily include those Selenium
tests in a continuous integration system.

Usage
~~~~~

See hereunder an excerpt of the help provided by the script ::

    converthtmltests -l LAYER [options] directory

    options:
      -f FILE, --file=FILE  write tests to FILE
      -l LAYER, --layer=LAYER
                            full python import path to layer instance

The script gathers and converts all Selenium HTML tests found in the mentioned
directory.

The user must refer to a ``plone.testing`` layer by specifying its Python import path.
That layer is set on the test case generated in the Python module.

An output file can be specified. In case no output file name is specified,
the module produced is named ``tests_all_selenium.py``.


Controlling gocept.selenium through environment variables
---------------------------------------------------------

You can configure the selenium server that gocept.selenium connects to from the
command line. Selenium RC defaults to localhost:4444, but you can also connect
to a selenium grid in your organization by using the following environment
variables::

    GOCEPT_SELENIUM_SERVER_HOST=selenium.mycompany.com
    GOCEPT_SELENIUM_SERVER_PORT=8888

If multiple browsers are connected to your selenium grid, you can choose the
browser to run the tests with as such::

    GOCEPT_SELENIUM_BROWSER=*iexplore

When you are running your selenium tests on a selenium grid, you need to
instruct the browser which host and port to connect to::

    GOCEPT_SELENIUM_APP_HOST=10.0.0.15
    GOCEPT_SELENIUM_APP_PORT=8001

When you are testing an application on one machine, you can access the running
application from another machine if you set ``GOCEPT_SELENIUM_APP_HOST = 0.0.0.0``
instead of the default ``localhost``.

You can set the speed with which the tests are run through an environment
variable::

    GOCEPT_SELENIUM_SPEED=500

This example will introduce a 500 millisecond pause between tests.

Similar packages
----------------

zc.selenium -- integrates Selenium Core with zope.testing.


Development
-----------

Report bugs at <https://intra.gocept.com/projects/projects/gocept-selenium/issues>.

Get the latest source with ::

  svn co http://svn.zope.org/repos/main/gocept.selenium/trunk gocept.selenium

