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

SELENIUM_SERVER_HOST_KEY = 'GOCEPT_SELENIUM_SERVER_HOST'
SELENIUM_SERVER_HOST_DEFAULT = 'localhost'

SELENIUM_SERVER_PORT_KEY = 'GOCEPT_SELENIUM_SERVER_PORT'
SELENIUM_SERVER_PORT_DEFAULT = '4444'

BROWSER_KEY = 'GOCEPT_SELENIUM_BROWSER'
BROWSER_DEFAULT = '*firefox'

APP_HOST_KEY = 'GOCEPT_SELENIUM_APP_HOST'
APP_HOST_DEFAULT = '0.0.0.0'

APP_PORT_KEY = 'GOCEPT_SELENIUM_APP_PORT'

SPEED_KEY = 'GOCEPT_SELENIUM_SPEED'


def _selenium_server_host():
    return os.environ.get(SELENIUM_SERVER_HOST_KEY,
                          SELENIUM_SERVER_HOST_DEFAULT)


def _selenium_server_port():
    return int(os.environ.get(SELENIUM_SERVER_PORT_KEY,
                              SELENIUM_SERVER_PORT_DEFAULT))


def _browser():
    return os.environ.get(BROWSER_KEY, BROWSER_DEFAULT)


def _app_host():
    return os.environ.get(APP_HOST_KEY, APP_HOST_DEFAULT)


def _app_port():
    return int(os.environ.get(APP_PORT_KEY, '5698'))


def _speed():
    return os.environ.get(SPEED_KEY)


class Layer(object):

    # hostname and port of the Selenium RC server
    _server = _selenium_server_host()
    _port = _selenium_server_port()
    _browser = _browser()

    # hostname and port of the local application.
    host = _app_host()
    port = _app_port()

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
        speed = _speed()
        if speed is not None:
            self.selenium.set_speed(speed)

    def tearDown(self):
        self.selenium.stop()

    def switch_db(self):
        raise NotImplemented


class TestCase(object):

    def setUp(self):
        super(TestCase, self).setUp()
        self.layer.switch_db()
        self.selenium = gocept.selenium.selenese.Selenese(
            self.layer.selenium, self)
