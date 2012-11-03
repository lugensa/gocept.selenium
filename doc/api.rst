API reference
=============

Selenese API
------------

The ``Selenese`` object available as ``self.selenium`` for each TestCase
provides methods to control the browser, and to make assertions about things
the browser sees.

For a detailed list of commands and assertions please consult the `Selenium
Reference <http://release.seleniumhq.org/selenium-core/1.0.1/reference.html>`_.

Assertions come in several flavours:

* Return the value ``self.selenium.getText('id=foo')``
* Assert ``self.selenium.assertText('id=foo', 'blabla')``
* Negated Assert ``self.selenium.assertNotText('id=foo', 'blabla')``
* Wait ``self.selenium.waitForElementPresent('id=foo')``
* Negated Wait ``self.selenium.waitForNotElementPresent('id=foo')``


Test helpers
------------

Skipping tests for certain browsers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are cases when a test should does not pass on certain browsers. This is
either due to the application using browser features which are not supported by
the browser, or due to selenium not working well with the browser. To aid in
skipping tests in these cases, there is a test decorator
``gocept.selenium.skipUnlessBrowser(name, version=None)``:

    >>> class TestClass(...):
    ...
    ... @gocept.selenium.skipUnlessBrowser('Firefox', '>=16.0')
    ... def test_fancy_things(self):
    ...     ...


.. NOTE:: ``skipUnlessBrowser`` *only* supports skipping test methods. It cannot
         be used as class decorator.

.. WARNING::
    The version test is only supported for Python >= 2.5. For Python < 2.5
    *only* a name check can be performed. Giving a version number will skip the
    test unconditionally.
