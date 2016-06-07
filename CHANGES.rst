Changelog
=========


3.0 (2016-06-07)
----------------

- Drop support for:

  - ``zope.app.testing`` (extras_require: [ztk])

  - ``Testing.ZopeTestCase`` (extras_require: [zope2])

  - ``plone.app.testing`` (extras_require: [test_plonetestingz2])

  - ``Products.PloneTestCase`` (extras_require: [plonetestcase])

- Remove the empty ``script`` extras_require.

- Drop support for Python 2.4, 2.5, 2.6. Now only supporting Python 2.7.

- Currently only supporting a ``selenium`` version < 2.53 as this version
  breaks using a custom Firefox.
  See https://github.com/SeleniumHQ/selenium/issues/1965

- Add ``.wd_selense.Selenese.selectParentFrame()`` to select the
  parent of a frame or an iframe.


2.5.4 (2016-04-12)
------------------

- Fix using a local Firefox using ``GOCEPT_WEBDRIVER_REMOTE=False`` as the
  environment setting.

2.5.3 (2016-04-11)
------------------

- Update tests to `gocept.httpserverlayer >= 1.4`.


2.5.2 (2016-04-11)
------------------

- Add documentation for the Jenkins integration of screenshots made from
  test failures. (#13936)

- Webdriver: Add a loop with time-out to ``click`` in order to deal with
  ``StaleElementReferenceException`` and ``NoSuchElementException``.


2.5.1 (2015-08-27)
------------------

- Webdriver: ``waitFor`` retries an assertion when ``NoSuchElementException``
  was raised. (This is useful for assertions like ``waitForVisible``.)


2.5.0 (2015-08-05)
------------------

- Add ``clear`` to webdriver to delete the contents of an input
  field.


2.4.1 (2015-06-23)
------------------

- Write junit annotations when a screenshot was taken for assertions beside
  ``assertScreenshot()``. (#13678)


2.4.0 (2015-03-27)
------------------

- Added ``getCssCount`` and ``getXpathCount``, so tests can get a baseline
  before an action.

- Fix ``getSelectedValue`` for webdriver.


2.3.0 (2015-03-09)
------------------

- Webdriver: ``waitFor`` will now retry the assertion when
  ``StaleElementReferenceException`` was raised, instead of yielding the error.
  (This could happen for assertions like ``waitForAttribute``, which would
  retrieve the DOM node and *then* ask for it's attribute. Thus the node can
  be changed in-between, which leads to the error.)


2.2.2 (2015-01-09)
------------------

- Improve environment variable handling implementation.


2.2.1 (2015-01-07)
------------------

- Fix handling firefox profile in remote=false mode.


2.2.0 (2015-01-07)
------------------

- Allow launching the browser directly when using Webdriver
  (set ``GOCEPT_WEBDRIVER_REMOTE=False`` and the browser name accordingly).

- Add optional ``movement`` parameter to ``dragAndDropToObject`` that moves the
  mouse a little before releasing the button, so one gets more realistic
  behaviour when needed (Webdriver only, RC does not seem to have this issue).

- Add ``js`` and ``jquery`` locators (Webdriver only).


2.1.9 (2014-11-06)
------------------

- Fixed capitalisation of Selenese's ``chooseOkOnNextConfirmation``.
  (Backwards incompatibility should be OK as it can never have worked before,
  anyway.)


2.1.8 (2014-09-04)
------------------

- No longer stop whole test run if an exception occures during
  ``testSetUp`` of ``.seleniumrc.Layer`` (#13375)


2.1.7 (2014-08-12)
------------------

- Remove ``window.gocept_selenium_abort_all_xhr`` again, this solution is
  incomplete, since we can only inject this during ``open()`` -- when the
  browser then navigates to a different page, the injection is lost.


2.1.6 (2014-08-06)
------------------

- Inject JS function ``window.gocept_selenium_abort_all_xhr`` during ``open()``,
  which is useful to call during test teardown to avoid spurious XHR requests
  to still be performed after the actual test has already ended.
  (Implemented in Webdriver only, but could be backported to RC if needed).


2.1.5 (2014-07-26)
------------------

- Webdriver: Only create a firefox profile when the selected browser is firefox
  (#11763).


2.1.4 (2014-07-09)
------------------

- Restore Python 2.6 compatibility of tests accidently broken in release 2.1.3.

- Adjust `isElementPresent` of WebDriver to work with PhantomJS, since it may
  raise a general WebDriverException if the element was not found.


2.1.3 (2014-07-07)
------------------

- Webdriver: No longer screenshotting while waiting for the condition to
  become true when using a ``waitFor*`` method.


2.1.2 (2014-06-25)
------------------

- Remove seleniumrc variable from Layer on teardown for symmetry.

- Fix `isVisible` of WebDriver, so it also returns False if a parent element
  is hidden.


2.1.1 (2014-04-28)
------------------

- Close temporary files when making screenshots. This fixes some occurrences
  of "Too many open files".


2.1.0 (2013-12-20)
------------------

- Make timeout configurable via environment variable
  ``GOCEPT_SELENIUM_TIMEOUT`` (#10497).

- Apply ``setTimeout`` to the ``open()`` timeout, too (#10750).

- Add environment variable ``GOCEPT_SELENIUM_JUNIT_ATTACH`` to support the
  "JUnit Attachments Plugin" for Jenkins.

internal:

- Move instantiating Selenese object from testSetUp to layer setUp. This
  *should* not change the behaviour for clients (we take care to reset the
  configured timeout in testSetUp as before), but take care.

- Fix URL to GROK toolkit versions.


2.0.0 (2013-10-02)
------------------

- Marking 2.0 stable, yay.


2.0.0b6 (2013-10-02)
--------------------

- Save screenshots of assertion failures with mode 644 (world-readable),
  which is useful for build servers.


2.0.0b5 (2013-10-01)
--------------------

- Implement ``setWindowSize`` for both RC and Webdriver.

- Implement ``getAllWindowIds`` in RC-Selenese.


2.0.0b4 (2013-04-26)
--------------------

- If a test fails because of an empty body, taking automatically a screenshot
  failed and concealing the original error message. This is now fixed. (#12341)


2.0.0b3 (2013-04-10)
--------------------

- Improved documentation, in particular with respect to the changes by
  integrating webdriver.

- If an ``AssertionError`` occures in a test using webdriver, a screenshot
  is taken automatically and the path is presented to the user. (#12247)

- Made a test for ``assertScreenshot`` pass on systems with a different
  browser default font.


2.0.0b2 (2013-03-01)
--------------------

- Stabilize webdriver/selenese API functions `waitForPageToLoad()` and
  `isTextPresent` to not raise errors when the elements vanish in between.


2.0.0b1 (2013-02-14)
--------------------

- Extract StaticFilesLayer to gocept.httpserverlayer.

- Added `assertScreenshot` to visually compare rendered elements with a
  master screenshot.


2.0.0a2 (2013-01-09)
--------------------

- Add layer that uses Webdriver as the Selenium backend instead of the old
  Remote Control.


1.1.2 (2012-12-21)
------------------

- Fix: Initialise the WSGI layer in the correct order to actually allow the
  configured WSGI app to be remembered.

- Fix: updated some imports after the extraction of gocept.httpserverlayer.


1.1.1 (2012-12-19)
------------------

- Update StaticFilesLayer to the new httpserverlayer API.


1.1 (2012-12-19)
----------------

- Extract HTTP server integration into separate package, gocept.httpserverlayer


1.0 (2012-11-03)
----------------

- Marking the API as stable.


0.17 (2012-11-01)
-----------------

- Added ``gocept.selenium.skipUnlessBrowser`` decorator to skip tests unless
  ceratins browser requirements are met.

- Fix: The static test server did not shutdown in some situations.


0.16 (2012-10-10)
-----------------

- Fixed selenese popup tests.

- Open a random port for the server process by default: When the environment
  variable `GOCEPT_SELENIUM_APP_PORT` is not set, a random free port is bound.
  This allows parallel testing, for instance (#11323).

0.15 (2012-09-14)
-----------------

- WSGI-Layer is comptabile with Python 2.5.
- Encoding support in converthtmltests
  (Patch by Tom Gross <tom@toms-projekte.de>).
- XHTML support for selenium tables
  (Patch by Tom Gross <tom@toms-projekte.de>).


0.14 (2012-06-06)
-----------------

- API expansion: Added ``assertCssCount``. Thus requiring selenium_ >= 2.0.
- Added Trove classifiers to package metadata.
- Moved code to Mercurial.

.. _selenium : http://pypi.python.org/pypi/selenium


0.13.2 (2012-03-15)
-------------------

- Fixed WSGI flavor: There was a ``RuntimeError`` in tear down if the WSGI
  server was shut down correctly.


0.13.1 (2012-03-15)
-------------------

- Updated URL of bug tracker.

- `script` extra no longer requires `elementtree` on Python >= 2.5.


0.13 (2012-01-30)
-----------------

- Added a selenese assert type 'list' and added it to the window management
  query methods.

- API expansion: added ``openWindow``.

- API change: filter the result of ``getAllWindowNames`` to ignore 'null'.

- backwards-compatible API change: ``selectWindow`` now selects the main
  window also when passed the window id ``None`` or no argument at all.

- pinned compatible ZTK version to 1.0.1, grok version to 1.2.1, generally
  pinned all software packages used to consistent versions for this package's
  own testing


0.12 (2011-11-29)
-----------------

- API expansion: added ``getAllWindow*`` and ``selectWindow``.


0.11 (2011-09-15)
-----------------

- Added some notes how to test a Zope 2 WSGI application.

- Described how to test a Zope 2/Plone application if using `plone.testing`
  to set up test layers.


0.10.1 (2011-02-02)
-------------------

- Improvements on the README.

- Wrote a quick start section for packages using ZTK but using
  ``zope.app.wsgi.testlayer`` instead of ``zope.app.testing``.

- Allowed to use `regexp` as pattern prefix for regular expressions
  additionally to `regex` to be compatible with the docstring and the
  Selenium documentation.


0.10 (2011-01-18)
-----------------

- Script that generates python tests from Selenium HTML tables.
  Reused from KSS project, courtesy of Jeroen Vloothuis, original author.

- Using a URL of `Selenium RC` in README where version 1.0.3 can be
  downloaded (instead of 1.0.1) which works fine with Firefox on Mac OS X,
  too.

0.9 (2010-12-28)
----------------

- Provide integration with the recent testlayer approach
  (zope.app.appsetup/zope.app.wsgi) used by Grok (#8260).
- Provide integration with plone.testing
- Make browser and RC server configurable (#6484).
- Show current test case in command log (#7876).
- Raise readable error when connection to RC server fails (#6489).
- Quit browser when the testrunner terminates (#6485).


0.8 (2010-10-22)
----------------

- Fixed tests for the StaticFilesLayer to pass with Python 2.4 through 2.7.
- API expansion: ``getSelectOptions``


0.7 (2010-08-16)
----------------

- API expansion: ``getElementHeight|Width``, ``getCookie*`` and a few others.
- lots of action methods (``mouse*`` among others)


0.6 (2010-08-09)
----------------

- assertXpathCount now also takes ints (#7681).

- API expansion: add ``isChecked`` to verify checkboxes, ``runScript``,
  ``clickAt``, ``getLocation``, ``getSelectedValue``, ``getSelectedIndex``.

- The ``pause`` method uses float division now. Pauses where implicitly rounded
  to full seconds before when an int was passed.

- The name of the factored test layer contains the module of the bases now. The
  name is used by zope.testrunner distinguish layers. Before this fix selenium
  layers factored from base layers with the same names but in different modules
  would be considered equal by zope.testrunner.

- The factored ZTK layer cleanly shuts down the http server in tearDown now.
  This allows to run different selenium layers in one go.


0.5 (2010-08-03)
----------------

- Add a static files test layer for running selenium tests against a set
  of static (HTML) files.
- Patterns now also work with multiline strings,
  i. e. 'foo*' will match 'foo\nbar' (#7790).


0.4.2 (2010-05-20)
------------------

- API expansion: ``*keyDown``, ``*keyUp``, ``keyPress``.


0.4.1 (2010-04-01)
------------------

- API expansion: added ``getSelectedLabel``.

- Ignore the code of a server's response when calling `open`. The default
  behaviour of SeleniumRC changed between 1.0.1 and 1.0.2 but we want the old
  behaviour by default.


0.4 (2010-03-30)
----------------

- API expansion: add ``getLocation`` to retrieve currently loaded URL in
  browser.

- API expansion: added ``waitForPopUp``, ``selectPopUp``, ``deselectPopUp``
  and ``close``.

- API expansion: added ``verifyAlertPresent``, ``verifyAlertNotPresent`` and
  ``waitForAlertPresent``.

- Usability: raise a better readable exception when an unimplemented selenese
  method is called.

- Usability: raise failure exceptions that convey the name of the failed
  assertion in spite of some lambdas wrapped around it.


0.3 (2010-01-12)
----------------

- Extracted 'host' and 'port' as class attributes of gocept.selenium.ztk.Layer
  so subclasses can override them; stopped hardcoding 8087 as the server port.


0.2.1 (2009-12-18)
------------------

- Fix incomplete sdist release on PyPI.


0.2 (2009-12-18)
----------------

- Make Zope 2 test server reachable from the outside.
- Implemented getTitle/assertTitle/waitForTitle/etc.


0.1 (2009-11-08)
----------------

- first release
