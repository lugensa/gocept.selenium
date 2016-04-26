Test helpers
------------

assertScreenshot
~~~~~~~~~~~~~~~~

.. NOTE:: ``assertScreenshot`` *needs* PIL. You might consider to require the
          `screenshot` extra in your setup.py like so:
          ``gocept.selenium[screenshot]``

The ``assertScreenshot`` method allows you to validate the rendering of a HTML
element in the browser. A screenshot of the element is saved in a given
directory and in your test ``assertScreenshot`` takes a picture of the
currently rendered element and compares it with the one saved in disk. The test
will fail, if the screenshot and the taken picture do not match (within a given
threshold).


``assertScreenshot`` takes the following arguments:

:name: A name for the screenshot (which will be appended with `.png`).
:locator: A locator_ to the element, which will be captured.
:threshold: If the difference [#1]_ in percent between the saved and current
            image is greater than the threshold, a failure is triggered.
            (defaults to 1)

.. _locator : http://release.seleniumhq.org/selenium-remote-control/0.9.0/doc/dotnet/html/Selenium.html

There is a capture mode available to help you in retrieving your master
screenshot (which will be left on disk for comparison). When writing your test,
set ``capture_screenshot`` on the `Selenese` object (see
:ref:`general-information`) to ``True`` and the test run will save the
screenshot to disk instead of comparing it. Before you check in your newly
created screenshot, you should watch it to make sure, it looks like you
expected it.  Setting ``capture_screenshot`` to ``False`` will compare the
screenshot on disk with a newly created temporary image during the next test
run.

If ``assertScreenshot`` fails, paths to the following images are provided to
you in the error message:

:original: The path to the original image (the master image).
:current: The path to the image taken in the current test run (from the
          browser).
:diff: The path to an image highlighting the differences between original and
       current.

If you would like to open the image showing the differences in an image viewer,
set the environment variable ``SHOW_DIFF_IMG`` before running the test.


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

.. [#1] The difference is computed as normalised root mean square deviation of
        the two images.
