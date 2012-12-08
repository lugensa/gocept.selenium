Upgrading to version 2 (using webdriver)
========================================

Starting with version 2, gocept.selenium uses Selenium's webdriver API, the
plan being to keep our own API as backwards-compatible as possible during the
2.x release series and switching to the webdriver API only with version 3.

This means that we've set out to implement the Selenese API on top of
webdriver and while this has proven to be possible to a large extent, some
details of the Selenese API don't make any sense or are too different to be
worth implementing in a webdriver environment.

Here's a list of backwards-incompatibilities between gocept.selenium version
1.x and 2.x:

- ``getEval`` behaves differently.

  * ``getEval`` adds a ``return`` statement in front of the code, i.e. to run
    Javascript code which is not an expression, use ``runScript``
  * ``getEval`` has access to different globals now: ``browserbot`` is no
    longer defined, while ``window`` and ``document`` refer directly to the
    window under test.
  * ``getEval`` returns the dictionary representation of objects instead of
    the rather uninformative ``[object Object]``.

- The browser name syntax has changed: specify Firefox as "firefox", not "firefox*"
  (concerns the environment variable ``GOCEPT_SELENIUM_BROWSER``).
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
  * ``chooseOKOnNextConfirmation``
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

  * element: dom, document
  * option: id
  * frame: relative, dom
