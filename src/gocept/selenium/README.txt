Selenium RC integration with zope.testing
=========================================

gocept.selenium integrates Selenium RC with your Plone/Zope 2/ZTK test suite.


Quick start with ZTK
--------------------

Assuming that you already have a package that uses zc.buildout and
zope.testing, you need to do this to enable Selenium tests:

1. Add gocept.selenium to the list of eggs either in your setup.py, or in
   buildout.cfg

2. Install Selenium RC by some means, e.g. by using
   collective.recipe.seleniumrc::

    [seleniumrc]
    recipe = collective.recipe.seleniumrc
    url = http://release.seleniumhq.org/selenium-remote-control/1.0.1/selenium-remote-control-1.0.1-dist.zip
    md5sum = 068b1adb26a7450717e6d6d67e261b58

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

7. Run seleniumrc.

8. Run bin/test and see it work!


Quick start with Zope 2/Plone
-----------------------------

Essentially the same, only use gocept.selenium.zope2 or gocept.selenium.plone
instead of gocept.selenium.ztk.


Similar packages
----------------

zc.selenium -- integrates Selenium Core with zope.testing.


Development
-----------

Report bugs at <https://intra.gocept.com/projects/projects/gocept-selenium/issues>.

Get the latest source with ::

  svn co http://svn.gocept.com/repos/gocept/gocept.selenium/trunk gocept.selenium

