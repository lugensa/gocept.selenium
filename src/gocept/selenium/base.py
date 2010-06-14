#############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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

import gocept.selenium.selenese
import selenium


class Layer(object):

    # override in subclass:
    # hostname and port of the app web server
    host = None
    port = None

    __name__ = 'Layer'

    def __init__(self, *bases):
        self.__bases__ = bases
        self.__name__ = '.'.join(x.__name__ for x in bases) + '.selenium'

    def setUp(self):
        pass

    def switch_db(self):
        raise NotImplemented


class TestCase(object):

    # XXX make configurable:
    # hostname and port of the Selenium RC server
    _server = 'localhost'
    _port = 4444

    browser = '*firefox'

    def setUp(self):
        super(TestCase, self).setUp()
        url = 'http://%s:%s/' % (self.layer.host, self.layer.port)
        self._selenium = selenium.selenium(
            self._server, self._port, self.browser, url)
        self._selenium.start()

        self.selenium = gocept.selenium.selenese.Selenese(self._selenium, self)

        self.layer.switch_db()

    def tearDown(self):
        self._selenium.stop()
        super(TestCase, self).tearDown()
