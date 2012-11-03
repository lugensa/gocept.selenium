Installation
============

Download the Selenium Remote Control JAR from `seleniumhq.org`_  and run::

    $ java -jar /path/to/selenium-server.jar

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

The default for the port to bind is 0 which let the kernel choose a random,
free port.

When you are testing an application on one machine, you can access the running
application from another machine if you set ``GOCEPT_SELENIUM_APP_HOST =
0.0.0.0`` instead of the default ``localhost``.

You can set the speed with which the tests are run through an environment
variable::

    GOCEPT_SELENIUM_SPEED=500

This example will introduce a 500 millisecond pause between tests.


Tips & Tricks
-------------

Using a custom Firefox profile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For debugging purposes it's helpful to have the `Firebug`_ debugger available
in the Selenium-controlled browser. To do that, create a new Firefox profile
and install Firebug into it. Then you can tell Selenium to use this profile for
running Firefox::

    $ java -jar /path/to/selenium-server.jar -firefoxProfileTemplate ~/.mozilla/firefox/<PROFILE_FOLDER>

.. _`Firebug`: http://getfirebug.com/


Using a nested X Server
~~~~~~~~~~~~~~~~~~~~~~~

Under Linux, the Selenium-controlled browser tends to steal the mouse focus,
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
    x-terminal-emulator -e java -jar /path/to/selenium-server.jar
