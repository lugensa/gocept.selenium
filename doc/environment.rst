Setting up the environment
==========================

Download the Selenium Server JAR from `seleniumhq.org`_  and run::

    $ java -jar /path/to/selenium-server-standalone-2.xx.xx.jar

This starts the server process that your tests will connect to to spawn and
control the browser.

.. _`seleniumhq.org`: http://seleniumhq.org/download/

Choose the appropriate test layer (see :doc:`integration`) and create a test
case::

    import gocept.selenium.wsgi
    from mypackage import App

    test_layer = gocept.selenium.wsgi.Layer(App())


    class TestWSGITestCase(gocept.selenium.wsgi.TestCase):

        layer = test_layer

        def test_something(self):
            self.selenium.open('http://%s/foo.html' % self.selenium.server)
            self.selenium.assertBodyText('foo')


Environment variables
---------------------

You can set some variables in the environment of your test runner to configure
which selenium server gocept.selenium connects to. Selenium Server defaults to
localhost:4444, but you can also connect to a selenium grid in your
organization by using the following environment variables::

    GOCEPT_SELENIUM_SERVER_HOST=selenium.mycompany.com
    GOCEPT_SELENIUM_SERVER_PORT=8888

If multiple browsers are connected to your selenium grid, you can choose the
browser to run the tests with like this::

    GOCEPT_SELENIUM_BROWSER=*iexplore

For use with Selenium Server's webdriver interface, the browser needs to be
specified differently::

    GOCEPT_WEBDRIVER_BROWSER=firefox

Webdriver supports instantiating the browser directly (instead of going through
the Java-based server component). If you want to do this, set::

    GOCEPT_WEBDRIVER_REMOTE=False

and specify one of the `browser classes`_ defined by the Python bindings, for
example::

    GOCEPT_WEBDRIVER_BROWSER=Firefox


.. _`browser classes`: https://github.com/SeleniumHQ/selenium/blob/master/py/selenium/webdriver/__init__.py

If you want to use a Firefox binary at a custom path, specify it like this::

    GOCEPT_WEBDRIVER_FF_BINARY=<PATH>/firefox

By default, the selenium layer will make the HTTP server under test bind to
localhost and listen to a random port chosen by the kernel (i.e. instruct it
to bind to port 0). This randomly chosen port is then used to point the
browser at the application. You may want to influence this behaviour, e.g.
when running your selenium tests on a selenium grid::

    GOCEPT_SELENIUM_APP_HOST=10.0.0.15
    GOCEPT_SELENIUM_APP_PORT=8001

When you are testing an application on one machine, you can access the running
application from another machine if you set ``GOCEPT_SELENIUM_APP_HOST =
0.0.0.0`` instead of the default ``localhost``.

You can control the timeout of ``waitFor`` assertions and other selenium
actions by setting a timeout in seconds::

    GOCEPT_SELENIUM_TIMEOUT=10  (default: 30 seconds)


You can also set the speed with which the tests are run through an environment
variable::

    GOCEPT_SELENIUM_SPEED=500

This example will introduce a 500 millisecond pause between tests.

Jenkins integration
-------------------

If you use Jenkins, you might be interested in the `JUnit Attachment Plugin`_,
and setting::

    GOCEPT_SELENIUM_JUNIT_ATTACH=True

This will print information about the screenshot of a failure that the plugin
can read and attach the screenshot to the test run.

In the configuration of the jenkins job you need a `Post-build Action` called
`Publish JUnit test result report`. This action needs an `Additional test
report feature` called `Publish test attachments` to ask Jenkins to keep the
screenshots for you.

*Caution:* `zope.testrunner`_ is not usable for this behavior, you have to use
a test runner like `py.test`_.

.. _`JUnit Attachment Plugin`: https://wiki.jenkins-ci.org/display/JENKINS/JUnit+Attachments+Plugin
.. _`zope.testrunner` : https://pypi.python.org/pypi/zope.testrunner
.. _`py.test` : https://pypi.python.org/pypi/pytest


Tips & Tricks
-------------

Using a custom Firefox profile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For debugging purposes it's helpful to have the `Firebug`_ debugger available
in the Selenium-controlled browser. To do that, create a new Firefox profile
and install Firebug into it. Then you can tell Selenium to use this profile as
a profile template when running Firefox::

    $ java -jar /path/to/selenium-server-standalone-2.xx.xx.jar -firefoxProfileTemplate ~/.mozilla/firefox/<PROFILE_FOLDER>

When using webdriver, instead set this environment variable for running the
tests (not Selenium Server)::

    GOCEPT_WEBDRIVER_FF_PROFILE=~/.mozilla/firefox/<PROFILE_FOLDER>

.. _`Firebug`: http://getfirebug.com/


Using a nested X Server
~~~~~~~~~~~~~~~~~~~~~~~

On Linux systems, the Selenium-controlled browser tends to steal the window focus,
which makes it impossible to do anything else while a Selenium test is running.
To prevent this, use Xephyr (successor of Xnest) to start an X server contained
in a window, for example:

.. code-block:: sh

    #!/bin/sh
    display=:1
    Xephyr -host-cursor -dpi 100 -wr -screen 1400x900 $display &
    export DISPLAY=$display
    sleep 2
    metacity &  # or any other window manager
    x-terminal-emulator -e java -jar /path/to/selenium-server-standalone-2.xx.xx.jar
