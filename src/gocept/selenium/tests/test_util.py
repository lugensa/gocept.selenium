#############################################################################
#
# Copyright (c) 2012 Zope Foundation and Contributors.
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


class TestBrowserSkip(unittest.TestCase):

    user_agent = (
        u"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0 "
        "Gecko/20100101 Firefox/16.0")

    def call_test(self, browser, version=None):
        from gocept.selenium import skipUnlessBrowser
        self._inner_ran = False

        @skipUnlessBrowser(browser, version)
        def x(inner_self):
            self._inner_ran = True
        test = self._create_test()
        test.skipTest.side_effect = unittest.SkipTest()
        try:
            x(test)
        except unittest.SkipTest:
            pass
        return test

    def _create_test(self):
        test = mock.Mock()
        test.layer = dict(seleniumrc=mock.Mock(spec=('get_eval',)))
        test.layer['seleniumrc'].get_eval.return_value = self.user_agent
        return test

    def test_browser_name_missmatch_should_skip(self):
        self.assertTrue(self.call_test('aname').skipTest.called)

    def test_browser_name_mismatch_should_not_run_test(self):
        self.call_test('blubs')
        self.assertFalse(self._inner_ran)

    def test_browser_name_match_should_not_skip(self):
        self.assertFalse(self.call_test('Firefox').skipTest.called)

    def test_browser_name_match_should_run_test(self):
        self.call_test('Firefox')
        self.assertTrue(self._inner_ran)

    def test_version_mismatch_should_skip(self):
        self.assertTrue(self.call_test('Firefox', '<16.0').skipTest.called)

    def test_version_mismatch_should_not_run_test(self):
        self.call_test('Firefox', '<16.0')
        self.assertFalse(self._inner_ran)

    def test_version_match_should_not_skip(self):
        self.assertFalse(self.call_test('Firefox', '>=16.0').skipTest.called)

    def test_version_match_should_run_test(self):
        self.call_test('Firefox', '>=16.0')
        self.assertTrue(self._inner_ran)

    def test_invalid_version_number_should_raise_ValueError(self):
        # Note that versionpredicate uses stict version numbers. We gotta see
        # if this is useable in the real world.
        self.assertRaises(ValueError,
                          lambda: self.call_test('Firefox', '>1b7'))

    def test_missing_restriction_should_raise_ValueError(self):
        self.assertRaises(ValueError,
                          lambda: self.call_test('Firefox', '16.0'))

    def test_class_decorator_should_raise_ValueError(self):
        # Since the wohle selenium needs to be available to actually find out
        # the browser version it's quite hard to decorate an entire class. Thus
        # we fail in a useful way.
        from gocept.selenium import skipUnlessBrowser
        try:
            class MyTest(object):
                pass
            skipUnlessBrowser('hurz')(MyTest)
        except ValueError:
            pass
        else:
            self.fail('ValueError not raised')


class WebdriverSyntax(TestBrowserSkip):

    user_agent = '"%s"' % TestBrowserSkip.user_agent

    def _create_test(self):
        test = mock.Mock()
        test.layer = dict(seleniumrc=mock.Mock(spec=('execute_script',)))
        test.layer['seleniumrc'].execute_script.return_value = self.user_agent
        return test
