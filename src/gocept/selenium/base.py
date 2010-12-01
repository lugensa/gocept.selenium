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


class LayerBase(object):

    # hostname and port of the Selenium RC server
    _server = os.environ.get('GOCEPT_SELENIUM_SERVER_HOST', 'localhost')
    _port = int(os.environ.get('GOCEPT_SELENIUM_SERVER_PORT', 4444))

    _browser = os.environ.get('GOCEPT_SELENIUM_BROWSER', '*firefox')

    # hostname and port of the local application.
    host = os.environ.get('GOCEPT_SELENIUM_APP_HOST', 'localhost')
    port = int(os.environ.get('GOCEPT_SELENIUM_APP_PORT', 5698))

    __name__ = 'Layer'

    def __init__(self, *bases):
        self.__bases__ = bases
        self.__name__ = '[%s].selenium' % (
            '/'.join('%s.%s' % (x.__module__, x.__name__) for x in bases))

    def setUp(self):
        self.selenium = selenium.selenium(
            self._server, self._port, self._browser,
            'http://%s:%s/' % (self.host, self.port))
        self.selenium.start()
        speed = os.environ.get('GOCEPT_SELENIUM_SPEED')
        if speed is not None:
            self.selenium.set_speed(speed)

    def tearDown(self):
        self.selenium.stop()


class Layer(LayerBase):
    __name__ = 'Layer'

    def __init__(self, *bases):
        self.__bases__ = bases
        self.__name__ = '[%s].selenium' % (
            '/'.join('%s.%s' % (x.__module__, x.__name__) for x in bases))

    def testSetUp(self):
        pass

    def testTearDown(self):
        pass


class SaneLayer(LayerBase):
    """Sane layer base class.

    Sane test layer base class inspired by zope.component.testlayer.

    The hack requires us to set __bases__, __module__ and __name__.
    This fools zope.testrunner into thinking that this layer instance is
    an object it can work with.
    """

    __bases__ = ()

    def __init__(self, name=None):
        if name is None:
            name = self.__class__.__name__
        self.__name__ = name


class TestCase(object):

    def setUp(self):
        super(TestCase, self).setUp()
        self.selenium = gocept.selenium.selenese.Selenese(
            self.layer.selenium, self)
