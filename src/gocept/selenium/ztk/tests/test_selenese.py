#############################################################################
#
# Copyright (c) 2009 Zope Corporation and Contributors.
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

from gocept.selenium.selenese import selenese_pattern_equals as match
from gocept.selenium.selenese import camelcase_to_underscore
import gocept.selenium.ztk.testing
import unittest
import time


class PatternTest(unittest.TestCase):

    def test_no_prefix(self):
        self.assert_(match('foo', 'foo'))
        self.assert_(not match('foo', 'bar'))
        self.assert_(match('foo:bar', 'foo:bar'))

    def test_exact(self):
        self.assert_(match('foo', 'exact:foo'))
        self.assert_(not match('foo', 'exact:bar'))

    def test_glob(self):
        self.assert_(match('foo', 'glob:f*'))
        self.assert_(match('foo', 'glob:fo?'))
        self.assert_(not match('foo', 'glob:'))

        self.assert_(not match('foo', 'glob:b*'))
        self.assert_(not match('foo', 'glob:?ar'))

    def test_glob_with_regex_chars_should_work(self):
        self.assert_(match('(foo)', 'glob:(foo)'))
        self.assert_(match('[foo]', 'glob:[foo]'))

    def test_regex(self):
        self.assert_(match('foo', 'regex:^fo+$'))
        self.assert_(not match('foo', 'regex:^f+$'))


class UtilsTest(unittest.TestCase):

    def test_camelcaseconvert(self):
        self.assertEquals('asdf', camelcase_to_underscore('asdf'))
        self.assertEquals('foo_bar', camelcase_to_underscore('fooBar'))


class AssertionTest(gocept.selenium.ztk.testing.TestCase):

    def test_wait_for(self):
        self.selenium.open('/display-delay.html')
        self.selenium.assertElementNotPresent('css=div')
        self.selenium.waitForElementPresent('css=div')

    def test_wait_for_timeout(self):
        self.selenium.open('/display-delay.html')
        self.selenium.assertElementNotPresent('css=div')
        try:
            self.selenium.setTimeout(10)
            self.selenium.waitForElementPresent('css=div')
        except AssertionError:
            pass
        else:
            self.fail('Timeout did not raise')

    def test_assert_element_present_failure(self):
        self.selenium.open('/display-delay.html')
        try:
            self.selenium.assertElementNotPresent('css=body')
        except AssertionError:
            pass
        else:
            self.fail('assertion should have failed')

    def test_pause(self):
        start = time.time()
        self.selenium.pause(5000)
        if time.time() - start < 4:
            self.fail('Pause did not pause long enough')

    def test_deleteCookie_smoke(self):
        # Smoke test: just check that we don't break
        self.selenium.deleteCookie('foo', '/')

    def test_selectFrame_frame_doesnt_exist(self):
        self.assertRaises(Exception, self.selenium.selectFrame, 'foo')

    def test_waitForCondition_timeout(self):
        self.selenium.setTimeout(100)
        self.assertRaises(
            AssertionError, self.selenium.waitForCondition, 'false')

    def test_fireEvent_smoke(self):
        self.selenium.fireEvent('css=body', 'click')

    def test_location(self):
        self.selenium.open('/')
        self.assertEquals(
            'http://localhost:8087/',
            self.selenium.getLocation())


class PopUpTest(gocept.selenium.ztk.testing.TestCase):

    def setUp(self):
        super(PopUpTest, self).setUp()
        self.selenium.open('/launch-popup.html')

    def tearDown(self):
        if self.selenium.getLocation().endswith('/popup.html'):
            self.selenium.close()
            self.selenium.deselectPopUp()
        super(PopUpTest, self).tearDown()

    def test_wait_for_and_select_popup(self):
        # smoke tests for calls not otherwise used in this test class
        self.selenium.waitForPopUp('gocept.selenium-popup')
        self.selenium.waitForPopUp()
        self.selenium.selectPopUp()

    def test_0_select_popup(self):
        # XXX needs to be run first as pop-up windows can apparently be
        # selected even after they have been closed.
        self.assertRaises(Exception,
                          self.selenium.selectPopUp,
                          'gocept.selenium-popup', wait=False)
        self.selenium.selectPopUp('gocept.selenium-popup')
        self.selenium.verifyElementPresent('css=div#popup')

    def test_deselect_popup(self):
        self.selenium.selectPopUp('gocept.selenium-popup')
        self.selenium.deselectPopUp()
        self.selenium.verifyElementNotPresent('css=div#popup')
        self.selenium.verifyElementPresent('css=div#parent')

    def test_close(self):
        self.selenium.selectPopUp('gocept.selenium-popup')
        self.selenium.verifyElementPresent('css=div#popup')
        self.selenium.close()
        self.assertRaises(Exception,
                          self.selenium.verifyElementPresent, 'css=div#popup')
        self.selenium.deselectPopUp()
        self.selenium.verifyElementPresent('css=div#parent')
