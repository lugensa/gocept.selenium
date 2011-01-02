#############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import atexit
import gocept.selenium.selenese
import os
import selenium
import socket
import sys


if sys.version_info < (2, 5):
    TEST_METHOD_NAME = '_TestCase__testMethodName'
else:
    TEST_METHOD_NAME = '_testMethodName'


class Layer(object):

    # hostname and port of the Selenium RC server
    _server = os.environ.get('GOCEPT_SELENIUM_SERVER_HOST', 'localhost')
    _port = int(os.environ.get('GOCEPT_SELENIUM_SERVER_PORT', 4444))

    _browser = os.environ.get('GOCEPT_SELENIUM_BROWSER', '*firefox')

    # hostname and port of the local application.
    host = os.environ.get('GOCEPT_SELENIUM_APP_HOST', 'localhost')
    port = int(os.environ.get('GOCEPT_SELENIUM_APP_PORT', 5698))

    def __init__(self, *bases):
        self.__bases__ = bases
        if self.__bases__:
            base = bases[0]
            self.__name__ = '(%s.%s)' % (base.__module__, base.__name__)
        else:
            self.__name__ = self.__class__.__name__

    def _stop_selenium(self):
        # Only stop selenium if it is still active.
        if self.seleniumrc.sessionId is not None:
            self.seleniumrc.stop()

    def setUp(self):
        self.seleniumrc = selenium.selenium(
            self._server, self._port, self._browser,
            'http://%s:%s/' % (self.host, self.port))
        try:
            self.seleniumrc.start()
        except socket.error, e:
            raise socket.error(
                'Failed to connect to Selenium RC server at %s:%s,'
                ' is it running? (%s)'
                % (self._server, self._port, e))
        atexit.register(self._stop_selenium)
        speed = os.environ.get('GOCEPT_SELENIUM_SPEED')
        if speed is not None:
            self.seleniumrc.set_speed(speed)

    def tearDown(self):
        self.seleniumrc.stop()

    def testSetUp(self):
        # instantiate a fresh one per test run, so any configuration
        # (e.g. timeout) is reset
        self.selenium = gocept.selenium.selenese.Selenese(
            self.seleniumrc, self.host, self.port)


class TestCase(object):
    # the various flavours (ztk, zope2, grok, etc.) are supposed to provide
    # their own TestCase as needed, and mix this class in to get the
    # convenience functionality.
    #
    # Example:
    # some.flavour.TestCase(gocept.selenium.base.TestCase,
    #                       the.actual.base.TestCase):
    #     pass

    @property
    def selenium(self):
        return self.layer.selenium

    def setUp(self):
        super(TestCase, self).setUp()
        self.selenium.setContext('%s.%s' % (
            self.__class__.__name__, getattr(self, TEST_METHOD_NAME)))
