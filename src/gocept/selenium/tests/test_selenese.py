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

from gocept.selenium.selenese import camelcase_to_underscore
from gocept.selenium.selenese import selenese_pattern_equals as match
import glob
import gocept.selenium.selenese
import gocept.selenium.static
import os
import pkg_resources
import shutil
import time
import unittest


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

    def test_regexp(self):
        self.assert_(match('foo', 'regexp:^fo+$'))
        self.assert_(not match('foo', 'regexp:^f+$'))

    def test_multiline_strings(self):
        self.assert_(match('foo\nbar', 'glob:foo*'))
        self.assert_(match('foo\nbar', 'regex:^foo.*$'))


class UtilsTest(unittest.TestCase):

    def test_camelcaseconvert(self):
        self.assertEquals('asdf', camelcase_to_underscore('asdf'))
        self.assertEquals('foo_bar', camelcase_to_underscore('fooBar'))


class NonexistentNameTest(unittest.TestCase):

    def setUp(self):
        class TestCase(object):
            failureException = None

        class Selenese(gocept.selenium.selenese.Selenese):
            def get_without_assert_type(self):
                pass

            @gocept.selenium.selenese.assert_type('wrong_type')
            def get_with_wrong_assert_type(self):
                pass

        self.selenese = Selenese(None, None, None)

    def assertError(self, error, name, expected_msg):
        try:
            getattr(self.selenese, name)
        except error, e:
            msg = e.args[0]
        self.assertEquals(expected_msg, msg)

    def assertAttributeError(self, name):
        self.assertError(AttributeError, name, name)

    def test_nonexistent_name(self):
        self.assertAttributeError('a_nonexistent_name')
        self.assertAttributeError('assert_a_nonexistent_name')

    def test_waitfor_verify(self):
        self.assertAttributeError('waitFor_a_nonexistent_name')
        self.assertAttributeError('verify_a_nonexistent_name')

    def test_not(self):
        self.assertAttributeError('a_Notexistent_name')
        self.assertAttributeError('assert_a_Notexistent_name')
        self.assertAttributeError('waitFor_a_Notexistent_name')
        self.assertAttributeError('verify_a_Notexistent_name')

    def test_broken_assert_type(self):
        self.assertError(AttributeError,
                         'assert_without_assert_type',
                         "'function' object has no attribute 'assert_type'")
        self.assertError(ValueError,
                         'assert_with_wrong_assert_type',
                         "Unknown assert type 'wrong_type' for "
                         "selenese method 'assert_with_wrong_assert_type'.")


class HTMLTestCase(gocept.selenium.static.TestCase):

    def setUp(self):
        super(HTMLTestCase, self).setUp()
        directory = pkg_resources.resource_filename(
            'gocept.selenium.tests.fixture', '')
        for name in glob.glob(os.path.join(directory, '*.html')):
            shutil.copy(os.path.join(directory, name), self.documentroot)


class AssertionTest(HTMLTestCase):

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
            'http://%s:%s/' % (self.layer.host, self.layer.port),
            self.selenium.getLocation())

    def test_alert_not_present(self):
        self.selenium.open('/')
        self.selenium.verifyAlertNotPresent()

    def test_alert_present(self):
        self.selenium.open('/alert.html')
        time.sleep(0.6)
        self.selenium.verifyAlertPresent()
        self.selenium.getAlert()

    def test_wait_for_alert(self):
        self.selenium.open('/alert.html')
        self.selenium.verifyAlertNotPresent()
        self.selenium.waitForAlertPresent()
        self.selenium.getAlert()

    def test_xpathcount_should_convert_to_ints(self):
        self.selenium.open('/divs.html')
        self.selenium.assertXpathCount("//div[@class='countable']", 3)
        self.selenium.assertXpathCount("//div[@class='countable']", '3')
        self.selenium.assertXpathCount("//div", 4)
        self.selenium.assertXpathCount("//div", '4')


class PopUpTest(HTMLTestCase):

    def setUp(self):
        super(PopUpTest, self).setUp()
        self.selenium.open('/launch-popup.html')

    def tearDown(self):
        try:
            self.selenium.selectPopUp(wait=False)
        except Exception:
            pass
        if self.selenium.getLocation().endswith('/popup.html'):
            self.selenium.close()
            self.selenium.deselectPopUp()
        self.selenium.setTimeout(30)
        super(PopUpTest, self).tearDown()

    def test_wait_for_and_select_popup(self):
        # smoke tests for calls not otherwise used in this test class
        self.selenium.waitForPopUp('gocept.selenium-popup')
        self.selenium.waitForPopUp()
        self.selenium.selectPopUp()

    def test_wait_for_popup_times_out(self):
        self.selenium.selectPopUp('gocept.selenium-popup')
        self.selenium.close()
        self.selenium.deselectPopUp()
        self.selenium.setTimeout(0)
        self.assertRaises(Exception, self.selenium.waitForPopUp,
                          'gocept.selenium-popup')
        self.assertRaises(Exception, self.selenium.waitForPopUp)
        self.selenium.setTimeout(1)
        self.assertRaises(Exception, self.selenium.waitForPopUp,
                          'gocept.selenium-popup')
        self.assertRaises(Exception, self.selenium.waitForPopUp)

    def test_select_popup(self):
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


class WindowManagementTest(HTMLTestCase):

    def tearDown(self):
        for name in self.selenium.getAllWindowNames():
            if name == u'selenium_main_app_window':
                continue
            self.selenium.selectWindow('name=%s' % name)
            self.selenium.close()
        self.selenium.selectWindow(u'null')

    def test_selenium_starts_out_with_one_window_listed(self):
        self.selenium.assertAllWindowNames([u'selenium_main_app_window'])
        self.selenium.assertEval('window.name', u'selenium_main_app_window')

    def test_opening_new_window_adds_new_id(self):
        self.selenium.openWindow('', 'foo')
        self.selenium.assertAllWindowNames(
            [u'selenium_main_app_window', u'foo'])

    def test_newly_opened_window_needs_to_be_selected(self):
        self.selenium.openWindow('', 'foo')
        self.selenium.assertEval('window.name', u'selenium_main_app_window')
        self.selenium.selectWindow('foo')
        self.selenium.assertEval('window.name', u'foo')

    def test_open_blank_window(self):
        self.selenium.openWindow('', '_blank')
        names = self.selenium.getAllWindowNames()
        self.assertEqual(2, len(names))
        self.assertEqual(u'selenium_main_app_window', names[0])
        self.assertTrue(names[1].startswith('selenium_blank'))

    def test_selecting_null_selects_main_window(self):
        self.selenium.openWindow('', 'foo')
        self.selenium.selectWindow('foo')
        self.selenium.selectWindow(u'null')
        self.selenium.assertEval('window.name', u'selenium_main_app_window')

    def test_selecting_none_selects_main_window(self):
        self.selenium.openWindow('', 'foo')
        self.selenium.selectWindow('foo')
        self.selenium.selectWindow(None)
        self.selenium.assertEval('window.name', u'selenium_main_app_window')

    def test_select_without_arg_selects_main_window(self):
        self.selenium.openWindow('', 'foo')
        self.selenium.selectWindow('foo')
        self.selenium.selectWindow()
        self.selenium.assertEval('window.name', u'selenium_main_app_window')

    def test_new_window_cannot_have_name_null(self):
        self.assertRaises(ValueError, self.selenium.openWindow, '', 'null')
