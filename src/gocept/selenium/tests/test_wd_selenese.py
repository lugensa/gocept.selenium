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

from gocept.selenium.screenshot import ScreenshotMismatchError
from gocept.selenium.screenshot import ScreenshotSizeMismatchError
from gocept.selenium.wd_selenese import LOCATOR_JS, LOCATOR_JQUERY
from gocept.selenium.wd_selenese import selenese_pattern_equals as match
from gocept.selenium.wd_selenese import split_locator, split_option_locator
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import gocept.httpserverlayer.static
import gocept.testing.assertion
from unittest import mock
import os.path
import pathlib
import pkg_resources
import shutil
import stat
import time
import unittest


class SplitLocatorTest(unittest.TestCase):

    def test_equal_sign_is_split_into_by(self):
        self.assertEqual((By.ID, 'foo'), split_locator('identifier=foo'))
        self.assertEqual((By.ID, 'foo'), split_locator('id=foo'))
        self.assertEqual((By.NAME, 'foo'), split_locator('name=foo'))
        self.assertEqual((By.XPATH, 'foo'), split_locator('xpath=foo'))
        self.assertEqual((LOCATOR_JS, 'foo'), split_locator('js=foo'))
        self.assertEqual((LOCATOR_JQUERY, 'foo'), split_locator('jquery=foo'))
        self.assertEqual(
            (By.XPATH, '//a[contains(string(.), "foo")]'),
            split_locator('link=foo'))
        self.assertEqual((By.CSS_SELECTOR, 'foo'), split_locator('css=foo'))

    def test_prefix_document_yields_js(self):
        self.assertEqual((LOCATOR_JS, 'document.getElementById("foo")'),
                         split_locator('document.getElementById("foo")'))

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
STATIC_WD_SELENESE_LAYER = gocept.selenium.webdriver.WebdriverSeleneseLayer(
    name='WebdriverStaticFilesLayer', bases=(STATIC_WD_LAYER,))


class HTMLTestCase(gocept.selenium.webdriver.WebdriverSeleneseTestCase,
                   unittest.TestCase):

    def setUp(self):
        super().setUp()
        directory = pathlib.Path(pkg_resources.resource_filename(
            'gocept.selenium.tests.fixture', ''))
        for glob in ('*.html', '*.pdf'):
            for name in directory.glob(glob):
                shutil.copy(directory / name, self.layer['documentroot'])


class AssertionTests(gocept.testing.assertion.String,
                     gocept.testing.assertion.Exceptions):

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
        self.selenium.pause(3000)
        if time.time() - start < 1:
            self.fail('Pause did not pause long enough')
        if time.time() - start > 10:
            self.fail('Pause did pause too long')

    def test_deleteCookie_smoke(self):
        with self.assertNothingRaised():
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
        self.assertEqual(
            'http://%s/' % self.layer['http_address'],
            self.selenium.getLocation())

    def test_alert_not_present(self):
        self.selenium.open('/')
        self.selenium.verifyAlertNotPresent()

    @gocept.selenium.skipUnlessBrowser('Firefox', '>=16.0')
    def test_alert_present(self):
        self.selenium.open('/alert.html')
        time.sleep(3.1)
        self.selenium.verifyAlertPresent()
        self.selenium.getAlert()

    @gocept.selenium.skipUnlessBrowser('Firefox', '>=16.0')
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

    def test_xpathcount_raises_nice_exception_on_mismatch(self):
        self.selenium.open('/divs.html')
        with self.assertRaisesRegex(
                AssertionError,
                "Actual count of XPath '//div' is 4, expected 3.*"):
            self.selenium.assertXpathCount("//div", 3)

    def test_csscount_should_convert_to_ints(self):
        self.selenium.open('/divs.html')
        self.selenium.assertCssCount("css=div", 4)
        self.selenium.assertCssCount("css=div", '4')

    def test_csscount_raises_nice_exception_on_mismatch(self):
        self.selenium.open('/divs.html')
        with self.assertRaisesRegex(
                AssertionError,
                "Actual count of CSS 'css=div' is 4, expected 3.*"):
            self.selenium.assertCssCount("css=div", 3)

    def test_configured_timeout_is_applied_for_open(self):
        self.selenium.setTimeout(1)
        with self.assertRaises(TimeoutException):
            self.selenium.open('/divs.html')


class AssertionTest(AssertionTests,
                    HTMLTestCase,
                    gocept.testing.assertion.Ellipsis):

    layer = STATIC_WD_SELENESE_LAYER

    def test_fireEvent_smoke(self):
        pass  # does not exist in Webdriver

    def test_js_selector(self):
        self.selenium.open('/divs.html')
        self.selenium.assertElementPresent(
            'js=document.getElementsByClassName("countable")[0]')
        self.selenium.assertElementNotPresent(
            'js=document.getElementsByClassName("countable")[7]')

    def test_wait_for_retries_assertion_when_element_was_stale(self):
        def assertion(*args, **kw):
            raise StaleElementReferenceException(
                'Element is no longer attached to the DOM')
        assertion_mock = mock.Mock(wraps=assertion)

        self.selenium.setTimeout(1000)
        with self.assertRaises(StaleElementReferenceException):
            self.selenium._waitFor(assertion_mock)
        self.assertGreaterEqual(assertion_mock.call_count, 10)

    def test_wait_for_retries_assertion_when_element_was_not_present(self):
        self.selenium.setTimeout(1000)
        with self.assertRaises(NoSuchElementException) as e:
            self.selenium.waitForVisible('css=.foo.bar')
        self.assertEllipsis(
            'Timed out after 1.0 s. ...Unable to locate element...',
            e.exception.msg)

    def test_wd_selenese__Selenese__click__1(self):
        """It waits for retries when a click is intercepted by an element."""
        self.selenium.setTimeout(1000)
        self.selenium.open('/intercepted.html')
        with self.assertRaises(ElementClickInterceptedException) as e:
            self.selenium.click('css=.intercepted')
        self.assertEllipsis(
            'Timed out after 1.0 s. Element ... not clickable ... obscures it',
            e.exception.msg)

    def test_wd_selenese__Selense__selectParentFrame__1(self):
        """It does nothing if there is no parent frame."""
        assert self.selenium.selectParentFrame()


class ScreenshotAssertionTest(HTMLTestCase,
                              gocept.testing.assertion.String):

    layer = STATIC_WD_SELENESE_LAYER

    def setUp(self):
        super().setUp()
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
            'screenshot_threshold', 'css=#block-2', threshold=12)

    def test_does_fail_if_threshold_less_than_distance(self):
        self.selenium.open('screenshot_threshold.html')
        with self.assertRaises(ScreenshotMismatchError):
            self.selenium.assertScreenshot(
                'screenshot_threshold', 'css=#block-2', threshold=4)

    def test_diffing_blocks(self):
        """Test to check if the image differ works good. You have to set
        SHOW_DIFF_IMG=1 to see something."""
        self.selenium.open('screenshot_blocks.html')
        with self.assertRaises(ScreenshotMismatchError):
            self.selenium.assertScreenshot('screenshot_blocks', 'css=#block-2')

    def test_raises_Exception_on_empty_element(self):
        from ..screenshot import ZeroDimensionError
        self.selenium.open('empty-tag.html')
        with self.assertRaises(ZeroDimensionError):
            self.selenium.assertScreenshot('emtpy-tag', 'css=#block0')

    def test_takes_screenshot_on_assertion_error(self):
        self.selenium.open('screenshot.html')
        with self.assertRaises(AssertionError) as err:
            self.selenium.assertTextPresent('FooBar')
        self.assertStartsWith(
            "Text 'FooBar' not present\nA screenshot has been saved, see: ",
            str(err.exception))

    def test_screenshot_on_assertion_error_does_not_break_on_empty_body(self):
        self.selenium.open('display-delay.html')
        with self.assertRaises(AssertionError) as err:
            self.selenium.assertTextPresent('FooBar')
        self.assertEqual(
            "Text 'FooBar' not present\nA screenshot could not be saved "
            "because document body is empty.", str(err.exception))

    def test_screenshot_files_have_normal_file_mode(self):
        self.selenium.open('screenshot.html')
        message = self.selenium.screenshot()
        # XXX not the best API in the world, but on the other hand, not really
        # meant for programmatic usage, so...
        filename = message.rsplit(': ', 1)[1]
        mode = stat.S_IMODE(os.stat(filename).st_mode)
        self.assertEqual(0o644, mode)

    def test_waitFor_does_not_screenshot_on_each_failed_check(self):
        # Regression test for waitFor* polling existance of locator
        # screenshotting on every failure.
        self.selenium.open('display-delay.html')
        screenshot = 'gocept.selenium.wd_selenese.Selenese.screenshot'
        with mock.patch(screenshot) as screenshot:
            self.selenium.waitForTextPresent('Hello, world')
        self.assertEqual([], screenshot.call_args_list)  # not called

    def test_assert_takes_screenshot_on_failed_check(self):
        # Regression test for waitFor* polling existance of locator
        # screenshotting on every failure.
        self.selenium.open('display-delay.html')
        screenshot = 'gocept.selenium.wd_selenese.Selenese.screenshot'
        with self.assertRaises(AssertionError):
            with mock.patch(screenshot) as screenshot:
                self.selenium.assertTextPresent('Hello, world')
            screenshot.assert_called_once_with(mock.ANY)  # called


class ScreenshotDirectorySettingTest(HTMLTestCase):

    layer = STATIC_WD_SELENESE_LAYER

    def test_default_setting_when_not_set(self):
        # the default is the directory where the current test is
        img = pkg_resources.resource_filename(self.__module__, 'foo.png')
        self.selenium.capture_screenshot = True
        self.selenium.open('screenshot.html')
        with self.assertRaisesRegex(ValueError, img):
            self.selenium.assertScreenshot('foo', 'css=#block-1')
        self.assertTrue(os.path.isfile(img))
        os.unlink(img)

    def test_screenshot_directory_setting_resolves_dotted_name(self):
        directory = 'gocept.selenium.tests.screenshot_directory'
        self.selenium.screenshot_directory = directory
        img = pkg_resources.resource_filename(directory, 'foo.png')
        self.selenium.capture_screenshot = True
        self.selenium.open('screenshot.html')
        with self.assertRaisesRegex(ValueError, img):
            self.selenium.assertScreenshot('foo', 'css=#block-1')
        self.assertTrue(os.path.isfile(img))
        os.unlink(img)


class SelectFrameTests(HTMLTestCase):
    """Testing selectFrame and selectParentFrame."""

    layer = STATIC_WD_SELENESE_LAYER

    def test_wd_selense__Selenese__selectFrame__1(self):
        """It selects a frame by name."""
        sel = self.selenium
        sel.open('iframe.html')
        assert 1 == sel.getCssCount('css=.countable')
        sel.selectFrame('name=foo')
        assert 3 == sel.getCssCount('css=.countable')

    def test_wd_selense__Selenese__selectFrame__2(self):
        """It selects a frame by index."""
        sel = self.selenium
        sel.open('iframe.html')
        assert 1 == sel.getCssCount('css=.countable')
        sel.selectFrame('index=0')
        assert 3 == sel.getCssCount('css=.countable')

    def test_wd_selense__Selenese__selectFrame__3(self):
        """It does not select a frame by css."""
        sel = self.selenium
        sel.open('iframe.html')
        with self.assertRaises(ValueError) as err:
            sel.selectFrame('css=iframe')
        self.assertEqual(
            "Invalid frame selector 'css', valid are ['name', 'index']",
            str(err.exception))

    def test_wd_selense__Selenese__selectFrame__4(self):
        """It does not select a frame by relative."""
        sel = self.selenium
        sel.open('iframe.html')
        with self.assertRaises(NotImplementedError) as err:
            sel.selectFrame('relative=parent')
        self.assertEqual(
            "Invalid frame selector 'relative', valid are ['name', 'index']",
            str(err.exception))


class DownloadTests(HTMLTestCase):
    """Testing downloading of files."""

    layer = STATIC_WD_SELENESE_LAYER

    def test_webdriver__Layer__setUp__1(self):
        """It stores PDF files in a temporary download directory."""
        sel = self.selenium
        sel.open('download.html')
        sel.click('link=Example')
        download_dir = self.layer['selenium_download_dir']
        for i in range(10 * int(sel.timeout)):
            time.sleep(0.1)
            if list(download_dir.iterdir()):
                break
        else:
            self.fail('PDF-File was not downloaded, download dir is empty.')
        download_files = list(download_dir.iterdir())
        assert len(download_files) == 1
        assert download_files[0].name == 'example.pdf'
        assert download_files[0].read_bytes().startswith(b'%PDF-1.3')


class PatternTest(unittest.TestCase):
    """Testing selenese_pattern_equals"""

    def test_no_prefix(self):
        self.assertIs(match('foo', 'foo'), True)
        self.assertIs(match('foo', 'bar'), False)
        self.assertIs(match('foo:bar', 'foo:bar'), True)

    def test_exact(self):
        self.assertIs(match('foo', 'exact:foo'), True)
        self.assertIs(match('foo', 'exact:bar'), False)

    def test_glob(self):
        self.assertIs(match('foo', 'glob:f*'), True)
        self.assertIs(match('foo', 'glob:fo?'), True)
        self.assertIs(match('foo', 'glob:'), False)

        self.assertIs(match('foo', 'glob:b*'), False)
        self.assertIs(match('foo', 'glob:?ar'), False)

    def test_glob_with_regex_chars_should_work(self):
        self.assertIs(match('(foo)', 'glob:(foo)'), True)
        self.assertIs(match('[foo]', 'glob:[foo]'), True)

    def test_regex(self):
        self.assertIs(match('foo', 'regex:^fo+$'), True)
        self.assertIs(match('foo', 'regex:^f+$'), False)

    def test_regexp(self):
        self.assertIs(match('foo', 'regexp:^fo+$'), True)
        self.assertIs(match('foo', 'regexp:^f+$'), False)

    def test_multiline_strings(self):
        self.assertIs(match('foo\nbar', 'glob:foo*'), True)
        self.assertIs(match('foo\nbar', 'regex:^foo.*$'), True)
