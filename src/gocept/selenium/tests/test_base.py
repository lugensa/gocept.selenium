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

import mock
import unittest


class LayerTest(unittest.TestCase):

    def test_connection_refused_should_raise_readable_error(self):
        import gocept.selenium.base
        layer = gocept.selenium.base.Layer()
        layer.port = 1234  # doesn't matter, but > 0
        layer._port = 0 # reserved by IANA
        try:
            layer.setUp()
        except Exception, e:
            self.assertTrue(str(e).startswith(
                'Failed to connect to Selenium RC'))


class TestBrowserSkip(unittest.TestCase):

    user_agent = (
        u"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0 "
        "Gecko/20100101 Firefox/16.0")

    def call_test(self, browser, version=None):
        from gocept.selenium.base import skipUnlessBrowser
        self._inner_ran = False
        @skipUnlessBrowser(browser, version)
        def x(inner_self):
            self._inner_ran = True
        test = mock.Mock()
        test.selenium.getEval.return_value = self.user_agent
        test.skipTest.side_effect = unittest.SkipTest()
        try:
            x(test)
        except unittest.SkipTest:
            pass
        return test


    def test_browser_name_missmatch_should_skip(self):
        self.call_test('aname').skipTest.assert_called()

    def test_browser_name_mismatch_should_not_run_test(self):
        self.call_test('blubs')
        self.assertFalse(self._inner_ran)

    def test_browser_name_match_should_not_skip(self):
        self.call_test('Firefox').skipTest.assert_called()

    def test_browser_name_match_should_run_test(self):
        self.call_test('Firefox')
        self.assertTrue(self._inner_ran)

    def test_version_mismatch_should_skip(self):
        pass
