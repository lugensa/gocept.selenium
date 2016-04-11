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
import gocept.selenium.webdriver
import mock
import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class LayerTest(unittest.TestCase):

    def test_connection_refused_should_raise_readable_error(self):
        layer = gocept.selenium.webdriver.Layer()
        layer['http_address'] = 'localhost:12345'
        layer._port = 4445  # default port is 4444
        try:
            layer.setUp()
        except Exception, e:
            self.assertIn('Failed to connect to Selenium server', str(e))

    def assert_driver(self, remote, module):
        layer = gocept.selenium.webdriver.Layer()
        layer['http_address'] = 'localhost:12345'
        with mock.patch.dict(
                os.environ, {'GOCEPT_WEBDRIVER_REMOTE': str(remote)}):
            layer.setUp()
            self.assertEqual(module, layer['seleniumrc'].__class__.__module__)

    def test_webdriver__Layer__setUp__2(self):
        """It uses a remote driver if GOCEPT_WEBDRIVER_REMOTE == `True`."""
        self.assert_driver(
            remote=True, module='selenium.webdriver.remote.webdriver')

    def test_webdriver__Layer__setUp__3(self):
        """It uses a local driver if GOCEPT_WEBDRIVER_REMOTE == `False`."""
        self.assert_driver(
            remote=False, module='selenium.webdriver.firefox.webdriver')
