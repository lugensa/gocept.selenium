Upgrading to version 2 (using webdriver)
========================================

Starting with version 2, gocept.selenium uses Selenium's webdriver API, the
plan being to keep our own API as backwards-compatible as possible during the
2.x release series and switching to the webdriver API only with version 3.

This means that we've set out to implement the selenese API on top of
webdriver and while this has proven to be possible to a large extent, some
details of the selenese API don't make any sense or are too different to be
worth implementing in a webdriver environment.

Here's a list of backwards-incompatibilities between gocept.selenium version
1.x and 2.x:

- new browser name syntax: specify Firefox as "firefox", not "firefox*"

- the path to an existing Firefox profile can be selected through an
  environment variable, ``GOCEPT_SELENIUM_FF_PROFILE``

- selenese methods with changed behaviour:

  * open: dropped the ``ignoreResponseCode`` parameter
  * ``getEval`` adds a ``return`` statement in front of the code, i.e. to run
    Javascript code which is not an expression, use ``runScript``
  * ``getEval`` has access to different globals now: ``browserbot`` is no
    longer defined while ``window`` and ``document`` refer directly to the
    window under test
  * ``getEval`` returns the dictionary representation of objects instead of
    ``[object Object]``
  * ``assertOrdered`` only works with relative xpath locators

- methods removed from the selenese API:

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

- methods of the selenese API that have been kept but are non-functional
  temporarily:

  * ``highlight``
  * ``getSpeed``
  * ``setSpeed``
  * ``getAllWindowNames``
  * ``getAllWindowTitles``
  * ``selectPopUp``
  * ``deselectPopUp``

- locator patterns that can no longer be used:

  * element: dom, document
  * option: id
  * frame: relative, dom
