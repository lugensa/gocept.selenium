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

from gocept.selenium.wd_selenese import split_locator, split_option_locator
from gocept.selenium.screenshot import \
        ScreenshotMismatchError, ScreenshotSizeMismatchError
from selenium.webdriver.common.by import By
import glob
import gocept.httpserverlayer.static
import gocept.selenium.tests.test_selenese
import os.path
import pkg_resources
import shutil


try:
    import unittest2 as unittest
except ImportError:
    import unittest


class SplitLocatorTest(unittest.TestCase):

    def test_equal_sign_is_split_into_by(self):
        self.assertEqual((By.ID, 'foo'), split_locator('identifier=foo'))
        self.assertEqual((By.ID, 'foo'), split_locator('id=foo'))
        self.assertEqual((By.NAME, 'foo'), split_locator('name=foo'))
        self.assertEqual((By.XPATH, 'foo'), split_locator('xpath=foo'))
        self.assertEqual(
            (By.XPATH, '//a[contains(string(.), "foo")]'),
            split_locator('link=foo'))
        self.assertEqual((By.CSS_SELECTOR, 'foo'), split_locator('css=foo'))

    def test_prefix_document_yields_dom(self):
        pass  # XXX nyi

    def test_prefix_slashes_yields_xpath(self):
        self.assertEqual((By.XPATH, '//foo'), split_locator('//foo'))

    def test_no_prefix_yields_none(self):
        self.assertEqual((None, 'foo'), split_locator('foo'))

    def test_invalid_prefix_yields_none(self):
        self.assertEqual((None, 'bar=foo'), split_locator('bar=foo'))


class SplitOptionLocatorTest(unittest.TestCase):

    def test_equal_sign_is_split_into_method(self):
        self.assertEqual(('select_by_visible_text', 'foo'),
                         split_option_locator('label=foo'))
        self.assertEqual(('select_by_value', 'foo'),
                         split_option_locator('value=foo'))
        # self.assertEqual(('select_by_???', 'foo'),
        #                  split_option_locator('id=foo'))  # nyi
        self.assertEqual(('select_by_index', 'foo'),
                         split_option_locator('index=foo'))

    def test_no_prefix_yields_label(self):
        self.assertEqual(('select_by_visible_text', 'foo'),
                         split_option_locator('foo'))

    def test_invalid_prefix_yields_label(self):
        self.assertEqual(('select_by_visible_text', 'bar=foo'),
                         split_option_locator('bar=foo'))


STATIC_WD_LAYER = gocept.selenium.WebdriverLayer(
    name='StaticFilesLayer',
    bases=(gocept.httpserverlayer.static.STATIC_FILES,))
STATIC_WD_LAYER = gocept.selenium.webdriver.WebdriverSeleneseLayer(
    name='StaticFilesLayer', bases=(STATIC_WD_LAYER,))


class HTMLTestCase(gocept.selenium.webdriver.WebdriverSeleneseTestCase,
                   unittest.TestCase):

    def setUp(self):
        super(HTMLTestCase, self).setUp()
        directory = pkg_resources.resource_filename(
            'gocept.selenium.tests.fixture', '')
        for name in glob.glob(os.path.join(directory, '*.html')):
            shutil.copy(
                os.path.join(directory, name), self.layer['documentroot'])


class AssertionTest(gocept.selenium.tests.test_selenese.AssertionTests,
                    HTMLTestCase):

    layer = STATIC_WD_LAYER

    def test_fireEvent_smoke(self):
        pass  # does not exist in Webdriver


class ScreenshotAssertionTest(HTMLTestCase):

    layer = STATIC_WD_LAYER

    def setUp(self):
        super(ScreenshotAssertionTest, self).setUp()
        self.selenium.screenshot_directory = 'gocept.selenium.tests.fixture'

    def test_successful_comparison(self):
        self.selenium.open('screenshot.html')
        self.selenium.assertScreenshot('screenshot', 'css=#block-1')

    def test_raises_exception_if_image_sizes_differ(self):
        self.selenium.open('screenshot.html')
        with self.assertRaises(ScreenshotSizeMismatchError):
            self.selenium.assertScreenshot('screenshot', 'css=#block-2')

    def test_does_not_fail_if_threshold_greater_than_distance(self):
        self.selenium.open('screenshot_threshold.html')
        self.selenium.assertScreenshot(
            'screenshot_threshold', 'css=#block-2', threshold=8)

    def test_does_fail_if_threshold_less_than_distance(self):
        self.selenium.open('screenshot_threshold.html')
        with self.assertRaises(ScreenshotMismatchError):
            self.selenium.assertScreenshot(
                'screenshot_threshold', 'css=#block-2' , threshold=4)

    def test_diffing_blocks(self):
        """Test to check if the image differ works good. You have to set 
        SHOW_DIFF_IMG=1 to see something."""
        self.selenium.open('screenshot_blocks.html')
        with self.assertRaises(ScreenshotMismatchError):
            self.selenium.assertScreenshot(
                    'screenshot_blocks', 'css=#block-2')
