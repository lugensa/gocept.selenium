#############################################################################
#
# Copyright (c) 2009-2010 Zope Foundation and Contributors.
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

from gocept.selenium.selenese import selenese_pattern_equals
from gocept.selenium.screenshot import PRINT_JUNIT_ATTACHMENTS
from gocept.selenium.screenshot import junit_attach_line
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.select import Select
import contextlib
import json
import re
import selenium.common.exceptions
import time
import urlparse


LOCATOR_JS = 'javascript'
LOCATOR_JQUERY = 'jquery'

try:
    from .screenshot import (
        assertScreenshot, screenshot_window, ZeroDimensionError)
except ImportError:
    HAS_SCREENSHOT = False
else:
    HAS_SCREENSHOT = True


def assert_type(type):
    def decorate(func):
        func.assert_type = type
        return func
    return decorate


@contextlib.contextmanager
def no_screenshot(selense):
    """Temporarly disable screenshoting exception."""
    try:
        selense.screenshot_on_exception = False
        yield
    finally:
        selense.screenshot_on_exception = True


class Selenese(object):

    failureExceptionClass = AssertionError
    screenshot_on_exception = True

    def __init__(self, selenium, app_address, timeout=30):
        # timeout=30 default argument is due to backwards-compatibility
        self.selenium = selenium
        self.server = app_address
        self.setTimeout(timeout * 1000)

    def failureException(self, msg):
        if self.screenshot_on_exception:
            screenshot_msg = self.screenshot()
            if screenshot_msg:
                msg += '\n' + screenshot_msg
        return self.failureExceptionClass(msg)

    # Actions

    def pause(self, milliseconds):
        time.sleep(milliseconds / 1000.0)

    def setTimeout(self, timeout):
        self.timeout = timeout / 1000.0
        self.selenium.set_page_load_timeout(self.timeout)

    def waitForPageToLoad(self):
        time.sleep(0.1)  # Give the browser a bit time to remove the old page
        self.waitForElementPresent('css=body')

    def _popup_exists(self, window_id=''):
        handles = self.selenium.window_handles
        if window_id:
            return window_id in handles
        else:
            return len(handles) > 1

    def waitForPopUp(self, windowID=''):
        deadline = time.time() + self.timeout
        while time.time() < deadline:
            if self._popup_exists(windowID):
                break
            time.sleep(0.01)
        else:
            raise RuntimeError(
                'Timed out waiting for pop-up window %r.' % windowID)

    def selectPopUp(self, windowID='', wait=True):
        if not windowID:
            windowID = self.selenium.window_handles[1]
        if not wait and not self._popup_exists(windowID):
            raise RuntimeError('Pop-up window %r not available.' % windowID)
        self.selenium.switch_to_window(windowID)

    def open(self, url):
        self.selenium.get(urlparse.urljoin('http://' + self.server, url))

    def altKeyDown(self):
        ActionChains(self.selenium).key_down(Keys.ALT).perform()

    def altKeyUp(self):
        ActionChains(self.selenium).key_up(Keys.ALT).perform()

    def attachFile(self, locator, fileURL):
        # see https://github.com/SeleniumHQ/selenium/wiki/Frequently-Asked-Questions#q-does-webdriver-support-file-uploads  # noqa
        # `fileURL` might an absolute path in the filesystem, too.
        self._find(locator).send_keys(fileURL)

    def captureScreenshot(self, filename):
        self.selenium.get_screenshot_as_file(filename)

    def captureScreenshotToString(self):
        return self.selenium.get_screenshot_as_base64()

    def close(self):
        self.selenium.close()

    def createCookie(self, nameAndValue, options):
        options = urlparse.parse_qs(options)
        options['name'], options['value'] = nameAndValue.split('=', 1)
        self.selenium.add_cookie(options)

    def deleteCookie(self, name, options):
        self.selenium.delete_cookie(name)

    def deleteAllVisibleCookies(self):
        self.selenium.delete_all_cookies()

    def deselectPopUp(self):
        self.selectWindow()

    def dragAndDropToObject(self, locatorSource, locatorDestination,
                            movement=None):
        action = ActionChains(self.selenium)
        action.click_and_hold(self._find(locatorSource))
        if movement is not None:
            x, y = movement.split(',')
            action.move_by_offset(int(float(x)), int(float(y)))
        action.release(self._find(locatorDestination))
        action.perform()

    def dragAndDrop(self, locator, movement):
        x, y = movement.split(',')
        action = ActionChains(self.selenium)
        action.click_and_hold(self._find(locator))
        action.move_by_offset(int(float(x)), int(float(y)))
        action.release(None)
        action.perform()

    def check(self, locator):
        self.click(locator)

    def click(self, locator):
        start = time.time()
        while time.time() - start < self.timeout:
            try:
                self._find(locator).click()
            except (StaleElementReferenceException,
                    NoSuchElementException), e:
                exc = e
                time.sleep(0.1)
            else:
                break
        else:
            raise type(exc)(
                'Timed out after %s s. %s' % (self.timeout, exc.msg))

    def clickAndWait(self, locator):
        self.click(locator)
        self.waitForPageToLoad()

    def clickAt(self, locator, coordString):
        x, y = coordString.split(',')
        ActionChains(self.selenium).move_to_element_with_offset(
            self._find(locator), int(x), int(y)).click().perform()

    def contextMenu(self, locator):
        ActionChains(self.selenium).context_click(
            self._find(locator)).perform()

    def contextMenuAt(self, locator, coordString):
        x, y = coordString.split(',')
        ActionChains(self.selenium).move_to_element_with_offset(
            self._find(locator), int(x), int(y)).context_click().perform()

    def controlKeyDown(self):
        ActionChains(self.selenium).key_down(Keys.CONTROL).perform()

    def controlKeyUp(self):
        ActionChains(self.selenium).key_up(Keys.CONTROL).perform()

    def doubleClick(self, locator):
        ActionChains(self.selenium).double_click(self._find(locator)).perform()

    def doubleClickAt(self, locator, coordString):
        x, y = coordString.split(',')
        # XXX API inconsistency: the parameter for click() is optional, but
        # required for double_click()
        ActionChains(self.selenium).move_to_element_with_offset(
            self._find(locator), int(x), int(y)).double_click(None).perform()

    def goBack(self):
        self.selenium.back()

    def highlight(self, locator):
        raise NotImplementedError()

    def keyDown(self, locator, keySequence):
        ActionChains(self.selenium).key_down(
            keySequence, self._find(locator)).perform()

    def keyPress(self, locator, keySequence):
        ActionChains(self.selenium).key_down(
            keySequence, self._find(locator)).key_up(keySequence).perform()

    def keyUp(self, locator, keySequence):
        ActionChains(self.selenium).key_up(
            keySequence, self._find(locator)).perform()

    def metaKeyDown(self):
        ActionChains(self.selenium).key_down(Keys.META).perform()

    def metaKeyUp(self):
        ActionChains(self.selenium).key_up(Keys.META).perform()

    def mouseDown(self, locator):
        ActionChains(self.selenium).click_and_hold(
            self._find(locator)).perform()

    def mouseDownAt(self, locator, coord):
        x, y = coord.split(',')
        ActionChains(self.selenium).move_to_element_with_offset(
            self._find(locator), int(x), int(y)).click_and_hold().perform()

    def mouseDownRight(self, locator):
        ActionChains(self.selenium).move_to_element(
            self._find(locator)).perform()
        self.selenium.execute(Command.MOUSE_DOWN, {'button': 2})

    def mouseDownRightAt(self, locator, coord):
        x, y = coord.split(',')
        ActionChains(self.selenium).move_to_element_with_offset(
            self._find(locator), int(x), int(y)).perform()
        self.selenium.execute(Command.MOUSE_DOWN, {'button': 2})

    def mouseMove(self, locator):
        ActionChains(self.selenium).move_to_element(
            self._find(locator)).perform()

    def mouseMoveAt(self, locator, coord):
        x, y = coord.split(',')
        ActionChains(self.selenium).move_to_element_with_offset(
            self._find(locator), int(x), int(y)).perform()

    def mouseOut(self, locator):
        OFFSET = 10
        element = self._find(locator)
        width = element.size['width']
        height = element.size['height']
        ActionChains(self.selenium).move_to_element_with_offset(
            element, width + OFFSET, height + OFFSET).perform()

    def mouseOver(self, locator):
        ActionChains(self.selenium).move_to_element(
            self._find(locator)).perform()

    def mouseUp(self, locator):
        ActionChains(self.selenium).release(self._find(locator)).perform()

    def mouseUpAt(self, locator, coord):
        x, y = coord.split(',')
        ActionChains(self.selenium).move_to_element_with_offset(
            self._find(locator), int(x), int(y)).release().perform()

    def mouseUpRight(self, locator):
        ActionChains(self.selenium).move_to_element(
            self._find(locator)).perform()
        self.selenium.execute(Command.MOUSE_UP, {'button': 2})

    def mouseUpRightAt(self, locator, coord):
        x, y = coord.split(',')
        ActionChains(self.selenium).move_to_element_with_offset(
            self._find(locator), int(x), int(y)).perform()
        self.selenium.execute(Command.MOUSE_UP, {'button': 2})

    def openWindow(self, url, window_id):
        self.selenium.execute_script(
            'window.open("%s", "%s")' % (url, window_id))

    def refresh(self):
        self.selenium.refresh()
        self.waitForPageToLoad()

    def removeAllSelections(self, locator):
        Select(self._find(locator)).deselect_all()

    def removeSelection(self, locator, optionLocator):
        element = self._find(locator)
        method, option = split_option_locator(optionLocator, deselect=True)
        getattr(Select(element), method)(option)

    def select(self, locator, optionLocator):
        element = self._find(locator)
        method, option = split_option_locator(optionLocator)
        getattr(Select(element), method)(option)

    addSelection = select

    def selectFrame(self, locator):
        self.selenium.switch_to.frame(split_frame_locator(locator))

    def selectParentFrame(self):
        self.selenium.switch_to.parent_frame()
        return True

    def selectWindow(self, window_id=None):
        if not window_id:
            window_id = self.selenium.window_handles[0]
        return self.selenium.switch_to_window(window_id)

    def submit(self, locator):
        self._find(locator).submit()

    def getSpeed(self):
        # XXX Python bindings do not expose Command.GET_SPEED
        raise NotImplementedError()

    def setSpeed(self, speed):
        # XXX Python bindings do not expose Command.SET_SPEED
        raise NotImplementedError()

    def shiftKeyDown(self):
        ActionChains(self.selenium).key_down(Keys.SHIFT).perform()

    def shiftKeyUp(self):
        ActionChains(self.selenium).key_up(Keys.SHIFT).perform()

    def type(self, locator, value):
        element = self._find(locator)
        element.send_keys(value)

    def typeKeys(self, locator, value):
        element = self._find(locator)
        element.send_keys(value)

    def runScript(self, script):
        self.selenium.execute_script(script)

    def uncheck(self, locator):
        self.click(locator)

    def windowFocus(self):
        self.selenium.switch_to_window(self.selenium.current_window_handle)

    def windowMaximize(self):
        self.selenium.maximize_window()

    def setWindowSize(self, width, height):
        self.selenium.set_window_size(width, height)
        self.waitForEval('window.outerWidth', str(width))
        self.waitForEval('window.outerHeight', str(height))

    def screenshot(self):
        """Take a screenshot of the whole window."""
        if HAS_SCREENSHOT:
            try:
                path = screenshot_window(self)
            except (ZeroDimensionError, WebDriverException):
                return ('A screenshot could not be saved because document '
                        'body is empty.')
            if PRINT_JUNIT_ATTACHMENTS:
                print '\n' + junit_attach_line(path, 'screenshot')
            return 'A screenshot has been saved, see: %s' % path

    def clear(self, locator):
        element = self._find(locator)
        return element.clear()

    # Getter

    @assert_type('pattern')
    def getAlert(self):
        alert = self.selenium.switch_to_alert()
        text = alert.text
        alert.dismiss()
        return text

    @assert_type('list')
    def getAllWindowIds(self):
        return self.selenium.window_handles

    @assert_type('list')
    def getAllWindowNames(self):
        raise NotImplementedError()

    @assert_type('list')
    def getAllWindowTitles(self):
        raise NotImplementedError()

    @assert_type('locator_pattern')
    def getAttribute(self, locator):
        locator, sep, attribute_name = locator.rpartition('@')
        element = self._find(locator)
        return element.get_attribute(attribute_name)

    @assert_type('pattern')
    def getTitle(self):
        return self.selenium.title

    @assert_type('pattern')
    def getBodyText(self):
        return self._find('//body').text

    @assert_type('pattern')
    def getConfirmation(self):
        confirmation = self.selenium.switch_to_alert()
        text = confirmation.text
        confirmation.accept()
        return text

    @assert_type('pattern')
    def getCookie(self):
        return self.selenium.get_cookies()

    @assert_type('locator_pattern')
    def getCookieByName(self, name):
        return self.selenium.get_cookie(name)

    @assert_type('locator_pattern')
    def getEval(self, script):
        # Note: we use the locator_pattern because the script acts like a
        # locator: we pass it through and Selenium returns a result we can
        # compare with the pattern.
        #
        # BBB We should be glad to get typed values out of webdriver's eval
        # but currently we try to keep gocept.selenium's API stable.
        if 'return' not in script:
            script = 'return ' + script
        return json.dumps(self.selenium.execute_script(script))

    @assert_type('pattern')
    def getHtmlSource(self):
        return self.selenium.page_source

    @assert_type('pattern')
    def getPrompt(self):
        prompt = self.selenium.switch_to_alert()
        return prompt.text

    @assert_type('locator_pattern')
    def getSelectedLabel(self, locator):
        select = Select(self._find(locator))
        return select.first_selected_option.text

    @assert_type('locator_pattern')
    def getSelectedLabels(self, locator):
        select = Select(self._find(locator))
        return [x.text for x in select.all_selected_options]

    @assert_type('locator_pattern')
    def getSelectedValue(self, locator):
        select = Select(self._find(locator))
        return select.first_selected_option.get_attribute('value')

    @assert_type('locator_pattern')
    def getSelectedValues(self, locator):
        select = Select(self._find(locator))
        return [x.get_attribute('value') for x in select.all_selected_options]

    @assert_type('locator_pattern')
    def getSelectedIndex(self, locator):
        select = Select(self._find(locator))
        return select.first_selected_option.get_attribute('index')

    @assert_type('locator_pattern')
    def getSelectedIndexes(self, locator):
        select = Select(self._find(locator))
        return [x.get_attribute('index') for x in select.all_selected_options]

    @assert_type('locator_pattern')
    def getSelectedId(self, locator):
        select = Select(self._find(locator))
        return select.first_selected_option.id

    @assert_type('locator_pattern')
    def getSelectedIds(self, locator):
        select = Select(self._find(locator))
        return [x.id for x in select.all_selected_options]

    @assert_type('locator')
    def isSomethingSelected(self, locator):
        select = Select(self._find(locator))
        try:
            select.first_selected_option
            return True
        except NoSuchElementException:
            return False

    @assert_type('locator')
    def getSelectOptions(self, locator):
        select = Select(self._find(locator))
        return [x.text for x in select.options]

    @assert_type('locator')
    def isChecked(self, locator):
        return self._find(locator).get_attribute('checked')

    @assert_type('locator')
    def isCookiePresent(self, name):
        return self.selenium.get_cookie(name) is not None

    @assert_type('locator_pattern')
    def getText(self, locator):
        return self._find(locator).text

    @assert_type('locator_pattern')
    def getValue(self, locator):
        element = self._find(locator)
        return element.get_attribute('value')

    @assert_type(None)
    def isAlertPresent(self):
        alert = self.selenium.switch_to_alert()
        try:
            alert.text
            return True
        except selenium.common.exceptions.NoAlertPresentException:
            return False

    @assert_type(None)
    def isPromptPresent(self):
        return self.isAlertPresent()

    @assert_type('locator')
    def isElementPresent(self, locator):
        try:
            self._find(locator)
        except selenium.common.exceptions.InvalidSelectorException:
            raise
        except NoSuchElementException:
            return False
        except WebDriverException as e:
            # PhantomJS uses general WebDriverException if element not found
            if 'Unable to find element with css selector' in e.msg:
                return False
            else:
                raise
        else:
            return True

    @assert_type('locator')
    def isVisible(self, locator):
        element = self._find(locator)
        return element.is_displayed()

    @assert_type('locator')
    def isEditable(self, locator):
        return not self._find(locator).get_attribute('disabled')

    def getElementWidth(self, locator):
        element = self._find(locator)
        return element.size['width']

    def getElementHeight(self, locator):
        element = self._find(locator)
        return element.size['height']

    @assert_type('locator_pattern')
    def getExpression(self, expression):
        return self.getEval(expression)

    def isTextPresent(self, pattern):
        try:
            body = self.selenium.find_element(By.TAG_NAME, 'body')
        except NoSuchElementException:
            # The body element is not there. This happens for instance during
            # page load. In this case, text matching is not possible.
            return False
        try:
            body_text = body.text
        except StaleElementReferenceException:
            # The body element vanished in between. Text is not present then.
            return False
        return normalize(pattern) in normalize(body_text)

    @assert_type('pattern')
    def getLocation(self):
        return self.selenium.current_url

    def getXpathCount(self, xpath):
        result = self.selenium.find_elements(By.XPATH, xpath)
        return len(result)

    def getCssCount(self, css):
        by, value = split_locator(css)
        if by == LOCATOR_JS:
            result = self.selenium.execute_script(u'return %s' % value)
        elif by == LOCATOR_JQUERY:
            result = self.selenium.execute_script(
                u'return window.jQuery("%s")' % value)
        else:
            result = self.selenium.find_elements(by, value)
        return len(result)

    # Assertions

    def assertTextPresent(self, pattern):
        if not self.isTextPresent(pattern):
            raise self.failureException('Text %r not present' % pattern)

    def assertCondition(self, condition):
        return self.assertEval(condition, 'true')

    def assertXpathCount(self, xpath, count):
        result = self.getXpathCount(xpath)
        if result != int(count):
            raise self.failureException(
                'Actual count of XPath %r is %s, expected %s'
                % (xpath, result, count))

    def assertCssCount(self, css, count):
        result = self.getCssCount(css)
        if result != int(count):
            raise self.failureException(
                'Actual count of CSS %r is %s, expected %s'
                % (css, result, count))

    # XXX works only for relative xpath locators with Webdriver
    def assertOrdered(self, locator1, locator2):
        if self._find(locator2).id not in set(
            x.id for x in self.selenium.find_elements_by_xpath(
                locator1 + '/following-sibling::*')):
            raise self.failureException(
                'Element order did not match expected %r,%r'
                % (locator1, locator2))

    def assertElementWidth(self, locator, width):
        got = self.getElementWidth(locator)
        if width != got:
            raise self.failureException(
                'Width of %r is %r, expected %r.' % (locator, got, width))

    def assertElementHeight(self, locator, height):
        got = self.getElementHeight(locator)
        if height != got:
            raise self.failureException(
                'Height of %r is %r, expected %r.' % (locator, got, height))

    capture_screenshot = False
    screenshot_directory = '.'

    def assertScreenshot(self, name, locator, threshold=0.1):
        """Assert that a screenshot of an element is the same as a screenshot
           on disk, within a given threshold.

        If self.capture_screenshot is True, the screenshot is saved as new
        expected image for the given name, and the Test fails and remembers
        to remove capture mode and check in the image.

        Does also respect self.screenshot_directory setting, to decide where
        to save the screenshot when in capture mode and where to search for
        screenshots for diffing.

        :param name: A name for the screenshot, which will be appended with
        `.png`.
        :param locator: A locator to the element that to capture.
        :param threshold: The threshold for triggering a test failure."""
        if not HAS_SCREENSHOT:
            raise self.failureException(
                """PIL is not installed. Install gocept.selenium with
                   "screenshot" extra to use assertScreenshot.""")
        assertScreenshot(self, name, locator, threshold)

    def _find(self, locator):
        by, value = split_locator(locator)
        if by == LOCATOR_JS:
            result = self.selenium.execute_script(u'return %s' % value)
            if result is None:
                raise NoSuchElementException()
            return result
        elif by == LOCATOR_JQUERY:
            result = self.selenium.execute_script(
                u'return window.jQuery("%s")[0]' % value)
            if result is None:
                raise NoSuchElementException()
            return result
        elif by:
            return self.selenium.find_element(by, value)
        try:
            return self.selenium.find_element(By.ID, locator)
        except NoSuchElementException:
            return self.selenium.find_element(By.NAME, locator)

    def __getattr__(self, name):
        requested_name = name

        def _getattr(name):
            try:
                return getattr(self, name)
            except AttributeError:
                raise AttributeError(requested_name)

        # Generate a number of assertions that aren't implemented directly.
        # Apply a fall-back chain that first implements waitFor* using
        # corresponding assert* and maps verify* methods to corresponding
        # assert*, then implements negative assert* by negating their positive
        # counterparts. Generate only these three kinds of assertions. After
        # each fall-back step, getattr() is called to make use of all directly
        # implemented methods. If a method cannot be looked up in spite of the
        # fall-back, raise an AttributeError that reports the method name
        # actually used by client code.
        if name.startswith('waitFor'):
            name = name.replace('waitFor', 'assert', 1)
            assertion = _getattr(name)
            return (lambda *args, **kw:
                    self._waitFor(assertion, *args, **kw))

        if name.startswith('verify'):
            name = name.replace('verify', 'assert', 1)
            return _getattr(name)

        if not name.startswith('assert'):
            raise AttributeError(requested_name)

        if 'Not' in name:
            name = name.replace('Not', '', 1)
            assertion = _getattr(name)
            return (lambda *args, **kw:
                    self._negate(assertion, requested_name, *args, **kw))

        # Positive assertions are synthesised by looking up a getter method
        # for a value, getting the value and evaluating it in an appropriate
        # way. Getters may be named either get* or is*.
        try:
            getter = _getattr(name.replace('assert', 'get', 1))
        except AttributeError:
            getter = _getattr(name.replace('assert', 'is', 1))

        if getter.assert_type == 'pattern':
            return lambda pattern: self._assert_pattern(
                getter, requested_name, pattern)
        elif getter.assert_type == 'locator':
            return lambda locator: self._assert(
                getter, requested_name, locator)
        elif getter.assert_type == 'locator_pattern':
            return lambda locator, pattern: self._assert_pattern(
                getter, requested_name, pattern, locator)
        elif getter.assert_type == 'list':
            return lambda expected: self._assert_list(
                getter, requested_name, expected)
        elif getter.assert_type is None:
            return lambda: self._assert(getter, requested_name)
        else:
            raise ValueError('Unknown assert type %r for selenese method %r.'
                             % (getter.assert_type, requested_name))

    def _assert(self, getter, name, *args, **kw):
        value = getter(*args, **kw)
        if not value:
            raise self.failureException(
                'Failed: %s -> %r' %
                (self._call_repr(name, *args, **kw), value))

    def _assert_pattern(self, getter, name, pattern, *args):
        result = getter(*args)
        if not selenese_pattern_equals(result, pattern):
            raise self.failureException(
                'Expected: %r, got: %r from %s' %
                (pattern, result, self._call_repr(name, *args)))

    def _assert_list(self, getter, name, expected):
        result = getter()
        if expected != result:
            detail = ''
            if len(expected) != len(result):
                detail += ('Expected %s items, got %s items.\n' %
                           (len(expected), len(result)))
            if len(expected) < len(result):
                detail += ('First extra element: %r\n\n' %
                           (result[len(expected)],))
            elif len(expected) > len(result):
                detail += ('First missing element: %r\n\n' %
                           (expected[len(result)],))
            else:
                for i, x in enumerate(expected):
                    if x != result[i]:
                        detail += (
                            'First differing list item at index %s:\n'
                            '- %r\n+ %r\n\n' % (i, x, result[i]))
                        break
            raise self.failureException(
                detail + ('Expected: %s,\ngot: %s\nfrom %s' % (
                    abbrev_repr(expected), abbrev_repr(result),
                    self._call_repr(name))))

    def _negate(self, assertion, name, *args, **kw):
        try:
            assertion(*args, **kw)
        except self.failureExceptionClass:
            return
        else:
            raise self.failureException(
                'Failed: ' + self._call_repr(name, *args, **kw))

    def _waitFor(self, assertion, *args, **kw):
        start = time.time()
        while True:
            try:
                with no_screenshot(self):
                    assertion(*args, **kw)
            except self.failureExceptionClass, e:
                if time.time() - start > self.timeout:
                    raise self.failureException(
                        'Timed out after %s s. %s' % (self.timeout, e.args[0]))
            except StaleElementReferenceException, e:
                if time.time() - start > self.timeout:
                    raise StaleElementReferenceException(
                        'Timed out after %s s. %s' % (self.timeout, e.msg))
            except NoSuchElementException, e:
                if time.time() - start > self.timeout:
                    raise NoSuchElementException(
                        'Timed out after %s s. %s' % (self.timeout, e.msg))
            else:
                break
            time.sleep(0.1)

    def _call_repr(self, name, *args, **kw):
        return '%s(%s)' % (
            name,
            ', '.join(map(repr, args) +
                      ['%s=%r' % item for item in sorted(kw.items())]))


def split_locator(locator):
    if locator.startswith('//'):
        return By.XPATH, locator
    if locator.startswith('document'):
        return LOCATOR_JS, locator

    by, sep, value = locator.partition('=')
    if not value:
        return None, locator

    by = {
        'identifier': By.ID,
        'id': By.ID,
        'name': By.NAME,
        'xpath': By.XPATH,
        'link': By.PARTIAL_LINK_TEXT,
        'css': By.CSS_SELECTOR,
        'dom': LOCATOR_JS,
        'js': LOCATOR_JS,
        'jquery': LOCATOR_JQUERY,
    }.get(by)
    if not by:
        return None, locator

    if by is By.PARTIAL_LINK_TEXT:
        by = By.XPATH
        value = '//a[contains(string(.), "%s")]' % value.strip('*')

    return by, value


def split_option_locator(option_locator, deselect=False):
    prefix = 'deselect' if deselect else 'select'
    method, sep, option = option_locator.partition('=')
    if method == 'id':
        raise NotImplementedError()
    if not option:
        return prefix + '_by_visible_text', option_locator
    method = {
        'label': prefix + '_by_visible_text',
        'value': prefix + '_by_value',
        'index': prefix + '_by_index',
    }.get(method)
    if not method:
        return prefix + '_by_visible_text', option_locator
    return method, option


def split_frame_locator(frame_locator):
    valid_selectors = ['name', 'index']
    by, sep, value = frame_locator.partition('=')
    if by in ['relative', 'dom']:
        raise NotImplementedError('Invalid frame selector %r, valid are %r'
                                  % (by, valid_selectors))
    elif by not in valid_selectors:
        raise ValueError('Invalid frame selector %r, valid are %r'
                         % (by, valid_selectors))
    elif by == 'index':
        value = int(value)
    return value


WHITESPACE = re.compile(r'\s+')


def normalize(text):
    return WHITESPACE.sub(' ', text)


def abbrev_repr(x, size=70):
    r = repr(x)
    if len(r) > size:
        r = r[:size - 3] + '...'
    return r
