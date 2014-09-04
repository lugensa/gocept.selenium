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
import unittest

# Python 2.4 does not have access to absolute_import,
# and we can't rename gocept.selenium.plone to something that
# does not clash with plone.testing (since that would break our API).
# So we use this workaround which passes empty globals to __import__,
# so it can't determine where we are to do something relatively.
# Also, we have to pass a fromlist with an empty string to have __import__
# return the module we asked for instead of its parent. *sigh*
plonetesting = __import__('plone.testing', {}, {}, [''])


class Layer(plonetesting.Layer):

    # hostname and port of the Selenium RC server
    _server = os.environ.get('GOCEPT_SELENIUM_SERVER_HOST', 'localhost')
    _port = int(os.environ.get('GOCEPT_SELENIUM_SERVER_PORT', 4444))

    _browser = os.environ.get('GOCEPT_SELENIUM_BROWSER', '*firefox')
    _timeout = int(os.environ.get('GOCEPT_SELENIUM_TIMEOUT', 30))

    def setUp(self):
        if 'http_address' not in self:
            raise KeyError("No base layer has set self['http_address']")
        self['seleniumrc'] = selenium.selenium(
            self._server, self._port, self._browser,
            'http://%s/' % self['http_address'])
        try:
            self['seleniumrc'].start()
        except socket.error, e:
            raise socket.error(
                'Failed to connect to Selenium RC server at %s:%s,'
                ' is it running? (%s)'
                % (self._server, self._port, e))
        atexit.register(self._stop_selenium)
        speed = os.environ.get('GOCEPT_SELENIUM_SPEED')
        if speed is not None:
            self['seleniumrc'].set_speed(speed)
        self['selenium'] = gocept.selenium.selenese.Selenese(
            self['seleniumrc'], self['http_address'], self._timeout)

    def _stop_selenium(self):
        # Only stop selenium if it is still active.
        if self['seleniumrc'].sessionId is not None:
            self['seleniumrc'].stop()

    def tearDown(self):
        self['seleniumrc'].stop()

    def testSetUp(self):
        # BBB reset timeout
        try:
            self['selenium'].setTimeout(self._timeout * 1000)
        except Exception:
            # possible exceptions:
            # * Exception: "ERROR: There was an unexpected Alert!"
            # * socket.timeout: "timed out"
            pass


class IntegrationBase(object):

    # hostname and port of the local application.
    host = os.environ.get('GOCEPT_SELENIUM_APP_HOST', 'localhost')
    port = int(os.environ.get('GOCEPT_SELENIUM_APP_PORT', 0))

    def __init__(self, *args, **kw):
        kw['module'] = sys._getframe(1).f_globals['__name__']
        super(IntegrationBase, self).__init__(*args, **kw)
        self.SELENIUM_LAYER = Layer(
            name='IntegratedSeleniumLayer', bases=[self])

    def make_layer_name(self, bases):
        if bases:
            base = bases[0]
            name = '(%s.%s)' % (base.__module__, base.__name__)
        else:
            name = self.__class__.__name__
        return name

    def setUp(self):
        super(IntegrationBase, self).setUp()
        self.SELENIUM_LAYER.setUp()
        self['seleniumrc'] = self.SELENIUM_LAYER['seleniumrc']

    def tearDown(self):
        self.SELENIUM_LAYER.tearDown()
        del self['seleniumrc']
        super(IntegrationBase, self).tearDown()

    def testSetUp(self):
        super(IntegrationBase, self).testSetUp()
        self.SELENIUM_LAYER.testSetUp()
        self['selenium'] = self.SELENIUM_LAYER['selenium']

    def testTearDown(self):
        self.SELENIUM_LAYER.testTearDown()
        super(IntegrationBase, self).testTearDown()


TEST_METHOD_NAMES = ('_TestCase__testMethodName', '_testMethodName')


class BaseTestCase(object):
    # the various flavours (ztk, zope2, grok, etc.) are supposed to provide
    # their own TestCase as needed, and mix this class in to get the
    # convenience functionality.
    #
    # Example:
    # some.flavour.TestCase(gocept.selenium.seleniumrc.TestCase,
    #                       the.actual.base.TestCase):
    #     pass

    @property
    def selenium(self):
        return self.layer['selenium']

    def setUp(self):
        super(BaseTestCase, self).setUp()
        for attr in TEST_METHOD_NAMES:
            method_name = getattr(self, attr, None)
            if method_name:
                break
        assert method_name
        self.selenium.setContext('%s.%s' % (self.__class__.__name__,
                                            method_name))


class TestCase(BaseTestCase, unittest.TestCase):
    """NOTE: MRO requires BaseTestCase to come first,
    otherwise its setUp/tearDown is never called, since unittest.TestCase
    does not call super().
    """
    pass
