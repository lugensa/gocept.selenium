import selenium
import unittest

from plone.testing import Layer
from plone.testing.z2 import ZSERVER_FIXTURE

import gocept.selenium.selenese


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

    def tearDown(self):
        super(Selenium, self).tearDown()
        self.selenium.stop()

SELENIUM = Selenium()


class TestCase(unittest.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.selenium = gocept.selenium.selenese.Selenese(
            self.layer['selenium'], self.layer['host'], self.layer['port'])
