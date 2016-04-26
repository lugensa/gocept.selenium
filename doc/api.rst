Selenese API
------------

.. _general-information:

General information
~~~~~~~~~~~~~~~~~~~

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
