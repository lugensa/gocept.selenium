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
import os

import selenium

import gocept.selenium.selenese


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

    def setUp(self):
        self.seleniumrc = selenium.selenium(
            self._server, self._port, self._browser,
            'http://%s:%s/' % (self.host, self.port))
        self.seleniumrc.start()
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
    # their own TestCase as needed, and mix this class in to have
    # 'self.selenium' available on the TestCase itself for convenience.
    #
    # Example:
    # some.flavour.TestCase(gocept.selenium.base.TestCase,
    #                       the.actual.base.TestCase):
    #     pass

    def setUp(self):
        super(TestCase, self).setUp()
        self.selenium = self.layer.selenium
