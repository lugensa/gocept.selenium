Webdriver API
-------------

Starting with version 2, gocept.selenium also includes integration with
Selenium's webdriver backend, the plan being to keep our own API as
backwards-compatible as possible during the 2.x release series and switching to
a modernized API only with version 3.

This means that we've set out to implement the Selenese API on top of
webdriver and while this has proven to be possible to a large extent, some
details of the Selenese API don't make any sense or are too different to be
worth implementing in a webdriver environment.

Here's how to set this up (see :doc:`integration` for details)::

    import gocept.httpserverlayer.wsgi
    import gocept.selenium
    from mypackage import App

    http_layer = gocept.httpserverlayer.wsgi.Layer(App())
    webdriver_layer = gocept.selenium.WebdriverLayer(
        name='WSGILayer', bases=(http_layer,))
    test_layer = gocept.selenium.WebdriverSeleneseLayer(
        name='WebdriverTestLayer', bases=(webdriver_layer))


    class TestWSGITestCase(gocept.selenium.WebdriverSeleneseTestCase):

        layer = test_layer

        def test_something(self):
            self.selenium.open('http://%s/foo.html' % self.selenium.server)
            self.selenium.assertBodyText('foo')

Here's a list of backwards-incompatibilities between using
WebdriverSeleneseLayer and the (old) SeleniumRC-backed gocept.selenium.RCLayer:

- ``getEval`` behaves differently.

  * ``getEval`` adds a ``return`` statement in front of the code, i.e. to run
    Javascript code which is not an expression, use ``runScript``
  * ``getEval`` has access to different globals now: ``browserbot`` is no
    longer defined, while ``window`` and ``document`` refer directly to the
    window under test.
  * ``getEval`` returns the dictionary representation of objects instead of
    the rather uninformative ``[object Object]``.

- The browser name syntax has changed: specify Firefox as "firefox", not "firefox*"
  (concerns the environment variable for setting the browser, which used to be
  ``GOCEPT_SELENIUM_BROWSER`` and is ``GOCEPT_WEBDRIVER_BROWSER`` for webdriver).
  See the `WebDriver wiki`_ for possible browser names.

.. _`WebDriver wiki`: http://code.google.com/p/selenium/wiki/DesiredCapabilities

- With Selenium Remote-Control one had to change the base Firefox profile to be
  used on the server side (by passing ``-firefoxProfileTemplate`` to
  ``selenium-server.jar``). With WebDriver this has moved to the client side,
  so you can select a profile by setting the path to an existing Firefox
  profile as the environment variable ``GOCEPT_SELENIUM_FF_PROFILE``.

- Selenese methods that don't work yet:

  * ``highlight``
  * ``getSpeed``
  * ``setSpeed``
  * ``getAllWindowNames``
  * ``getAllWindowTitles``
  * ``selectPopUp``
  * ``deselectPopUp``

- Selenese methods with changed behaviour:

  * ``open``: dropped the ``ignoreResponseCode`` parameter
  * ``assertOrdered`` only works with relative xpath locators, not with
    any element locators anymore.

- Selenese methods that have been removed and are not coming back:

  * ``addCustomRequestHeader``
  * ``addLocationStrategy``
  * ``addScript``
  * ``allowNativeXpath``
  * ``answerOnNextPrompt``
  * ``assignId``
  * ``captureNetworkTraffic``
  * ``chooseCancelOnNextConfirmation``
  * ``chooseOkOnNextConfirmation``
  * ``fireEvent``
  * ``focus``
  * ``getMouseSpeed``
  * ``getTable``
  * ``ignoreAttributesWithoutValue``
  * ``removeScript``
  * ``retrieveLastRemoteControlLogs``
  * ``setBrowserLogLevel``
  * ``setContext``
  * ``setCursorPosition``
  * ``setMouseSpeed``
  * ``useXpathLibrary``
  * ``waitForFrameToLoad``

- Locator patterns that can no longer be used:

  * option: id
  * frame: relative, dom


On the other hand, here are some new features that only WebdriverSeleneseLayer
offers:

- Locator ``js`` (or ``dom`` or anything that starts with ``document``): Find
  an element by evaluating a javascript expression.
  Example: ``getText('js=document.getElementsByClassName("foo")')``
- Convenience locator ``jquery`` (when your site already loads ``jQuery``).
  Example: ``getText('jquery=.foo')`` (this is the equivalent of
  ``getText('js=window.jQuery(".foo")[0]')``)
