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

from plone.testing import Layer
from plone.testing.z2 import ZSERVER_FIXTURE
import gocept.selenium.selenese
import selenium


class Selenium(Layer):

    defaultBases = (ZSERVER_FIXTURE, )

    _rc_server = 'localhost'
    _rc_port = 4444
    _browser = '*firefox'

    def setUp(self):
        super(Selenium, self).setUp()
        self.selenium = self['selenium'] = selenium.selenium(
            self._rc_server, self._rc_port, self._browser,
            'http://%s:%s/' % (self['host'], self['port']))
        self.selenium.start()
        self['selenese'] = gocept.selenium.selenese.Selenese(
            self.selenium, self['host'], self['port'])

    def tearDown(self):
        super(Selenium, self).tearDown()
        self.selenium.stop()


SELENIUM = Selenium()
