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

import re
import time


def camelcase_to_underscore(name):
    new = ''
    for char in name:
        if char.isupper():
            new += '_'
        new += char
    return new.lower()


def passthrough(func):
    name = camelcase_to_underscore(func.__name__)

    def inner(self, *args, **kw):
        return getattr(self.selenium, name)(*args, **kw)

    inner.__name__ = func.__name__
    return inner


def assert_type(type):
    def decorate(func):
        func.assert_type = type
        return func
    return decorate


class Selenese(object):

    failureException = AssertionError

    def __init__(self, selenium, app_host, app_port):
        self.selenium = selenium
        self.host = app_host
        self.port = app_port
        self.timeout = 30

    @property
    def server(self):
        return '%s:%s' % (self.host, self.port)

    # Actions

    @passthrough
    def addLocationStrategy(self, name, definition):
        pass

    @passthrough
    def addScript(self, script):
        pass

    @passthrough
    def answerOnNextPrompt(self, answer):
        pass

    @passthrough
    def assignId(self, locator, id):
        pass

    @passthrough
    def allowNativeXpath(self, allow):
        pass

    @passthrough
    def ignoreAttributesWithoutValue(self, ignore):
        pass

    def pause(self, milliseconds):
        time.sleep(milliseconds / 1000.0)

    def setTimeout(self, timeout):
        self.timeout = timeout / 1000.0

    def waitForPageToLoad(self):
        self.selenium.wait_for_page_to_load(self.timeout * 1000)

    def waitForFrameToLoad(self):
        self.selenium.wait_for_frame_to_load(self.timeout * 1000)

    def waitForPopUp(self, windowID=''):
        self.selenium.wait_for_pop_up(windowID, self.timeout * 1000)

    def selectPopUp(self, windowID='', wait=True):
        if wait:
            timeout = self.timeout * 1000
        else:
            timeout = 0
        self.selenium.wait_for_pop_up(windowID, timeout)
        self.selenium.select_pop_up(windowID)

    def open(self, url, ignoreResponseCode=True):
        self.selenium.do_command("open", [url, ignoreResponseCode])

    @passthrough
    def addCustomRequestHeader(self, key, value):
        pass

    @passthrough
    def addSelection(self, locator, optionLocator):
        pass

    @passthrough
    def altKeyDown(self):
        pass

    @passthrough
    def altKeyUp(self):
        pass

    @passthrough
    def attachFile(self, locator, fileURL):
        pass

    @passthrough
    def captureNetworkTraffic(self, type_):
        pass

    @passthrough
    def captureScreenshot(self, filename):
        pass

    @passthrough
    def captureScreenshotToString(self):
        pass

    @passthrough
    def close(self):
        self.selenium.deselectPopUp()
        pass

    @passthrough
    def createCookie(self, nameAndValue, options):
        pass

    @passthrough
    def deleteCookie(self, name, options):
        pass

    @passthrough
    def deleteAllVisibleCookies(self):
        pass

    @passthrough
    def deselectPopUp(self):
        pass

    @passthrough
    def dragAndDropToObject(self, locatorSource, locatorDestination):
        pass

    @passthrough
    def dragAndDrop(self, locator, movement):
        pass

    @passthrough
    def check(self, locator):
        pass

    @passthrough
    def click(self, locator):
        pass

    def clickAndWait(self, locator):
        self.click(locator)
        self.waitForPageToLoad()

    @passthrough
    def clickAt(self, locator, coordString):
        pass

    @passthrough
    def contextMenu(self, locator):
        pass

    @passthrough
    def contextMenuAt(self, locator, coordString):
        pass

    @passthrough
    def chooseOKOnNextConfirmation(self):
        pass

    @passthrough
    def chooseCancelOnNextConfirmation(self):
        pass

    @passthrough
    def controlKeyDown(self):
        pass

    @passthrough
    def controlKeyUp(self):
        pass

    @passthrough
    def doubleClick(self, locator):
        pass

    @passthrough
    def doubleClickAt(self, locator, coordString):
        pass

    @passthrough
    def fireEvent(self, locator, eventName):
        pass

    @passthrough
    def focus(self, locator):
        pass

    @passthrough
    def goBack(self):
        pass

    @passthrough
    def highlight(self, locator):
        pass

    @passthrough
    def keyDown(self, locator, keySequence):
        pass

    @passthrough
    def keyPress(self, locator, keySequence):
        pass

    @passthrough
    def keyUp(self, locator, keySequence):
        pass

    @passthrough
    def metaKeyDown(self):
        pass

    @passthrough
    def metaKeyUp(self):
        pass

    @passthrough
    def mouseDown(self, locator):
        pass

    @passthrough
    def mouseDownAt(self, locator, coord):
        pass

    @passthrough
    def mouseDownRight(self, locator):
        pass

    @passthrough
    def mouseDownRightAt(self, locator, coord):
        pass

    @passthrough
    def mouseMove(self, locator):
        pass

    @passthrough
    def mouseMoveAt(self, locator, coord):
        pass

    @passthrough
    def mouseOut(self, locator):
        pass

    @passthrough
    def mouseOver(self, locator):
        pass

    @passthrough
    def mouseUp(self, locator):
        pass

    @passthrough
    def mouseUpAt(self, locator, coord):
        pass

    @passthrough
    def mouseUpRight(self, locator):
        pass

    @passthrough
    def mouseUpRightAt(self, locator, coord):
        pass

    def openWindow(self, url, window_id):
        if window_id == 'null':
            raise ValueError("Cannot name a window 'null' "
                             "as this name is used be Selenium internally.")
        return self.selenium.open_window(url, window_id)

    def refresh(self):
        # No thanks to selenium... why would one ever *not* want to wait for
        # the page to load?
        self.selenium.refresh()
        self.waitForPageToLoad()

    @passthrough
    def removeAllSelections(self, locator):
        pass

    @passthrough
    def removeSelection(self, locator, optionLocator):
        pass

    @passthrough
    def removeScript(self, id):
        pass

    @passthrough
    def retrieveLastRemoteControlLogs(self):
        pass

    @passthrough
    def select(self, locator, optionLocator):
        pass

    @passthrough
    def selectFrame(self):
        pass

    def selectWindow(self, window_id=None):
        return self.selenium.select_window(window_id or 'null')

    @passthrough
    def submit(self, locator):
        pass

    @passthrough
    def setBrowserLogLevel(self, level):
        pass

    def getSpeed(self):
        return int(self.selenium.get_speed())

    @passthrough
    def setSpeed(self, speed):
        pass

    def getMouseSpeed(self):
        return int(self.selenium.get_mouse_speed())

    @passthrough
    def setMouseSpeed(self, speed):
        pass

    @passthrough
    def setContext(self, message):
        pass

    @passthrough
    def setCursorPosition(self, locator, position):
        pass

    @passthrough
    def shiftKeyDown(self):
        pass

    @passthrough
    def shiftKeyUp(self):
        pass

    @passthrough
    def type(self):
        pass

    @passthrough
    def typeKeys(self):
        pass

    @passthrough
    def runScript(self, script):
        pass

    @passthrough
    def uncheck(self, locator):
        pass

    @passthrough
    def useXpathLibrary(self, name):
        pass

    @passthrough
    def windowFocus(self):
        pass

    @passthrough
    def windowMaximize(self):
        pass

    # Getter

    @assert_type('pattern')
    def getAlert(self):
        if not self.selenium.is_alert_present():
            raise self.failureException(
                'No alert occured.')
        return self.selenium.get_alert()

    @assert_type('list')
    @passthrough
    def getAllWindowIds(self):
        pass

    @assert_type('list')
    def getAllWindowNames(self):
        return [name for name in self.selenium.get_all_window_names()
                if name != 'null']

    @assert_type('list')
    @passthrough
    def getAllWindowTitles(self):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getAttribute(self, locator):
        pass

    @assert_type('pattern')
    @passthrough
    def getTitle(self):
        pass

    @assert_type('pattern')
    @passthrough
    def getBodyText(self):
        pass

    @assert_type('pattern')
    def getConfirmation(self):
        if not self.selenium.is_confirmation_present():
            raise self.failureException(
                'No confirmation occured.')
        return self.selenium.get_confirmation()

    @assert_type('pattern')
    @passthrough
    def getCookie(self):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getCookieByName(self, name):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getEval(self, script):
        # Note: we use the locator_pattern because the script acts like a
        # locator: we pass it through and Selenium returns a result we can
        # compare with the pattern.
        pass

    @assert_type('pattern')
    @passthrough
    def getHtmlSource(self):
        pass

    @assert_type('pattern')
    def getPrompt(self):
        if not self.selenium.is_prompt_present():
            raise self.failureException(
                'No prompt occured.')
        return self.selenium.get_prompt()

    @assert_type('locator_pattern')
    @passthrough
    def getSelectedLabel(self, locator):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getSelectedLabels(self, locator):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getSelectedValue(self, locator):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getSelectedValues(self, locator):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getSelectedIndex(self, locator):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getSelectedIndexes(self, locator):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getSelectedId(self, locator):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getSelectedIds(self, locator):
        pass

    @assert_type('locator')
    @passthrough
    def isSomethingSelected(self, locator):
        pass

    @passthrough
    def getSelectOptions(self, locator):
        pass

    @assert_type('locator')
    @passthrough
    def isChecked(self, locator):
        pass

    @assert_type('locator')
    @passthrough
    def isCookiePresent(self, name):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getText(self, locator):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getTable(self, locator):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getValue(self, locator):
        pass

    @assert_type(None)
    @passthrough
    def isAlertPresent(self):
        pass

    @assert_type(None)
    @passthrough
    def isPromptPresent(self):
        pass

    @assert_type('locator')
    @passthrough
    def isElementPresent(self, locator):
        pass

    @assert_type('locator')
    @passthrough
    def isVisible(self, locator):
        pass

    @assert_type('locator')
    @passthrough
    def isEditable(self, locator):
        pass

    def getElementWidth(self, locator):
        return int(self.selenium.get_element_width(locator))

    def getElementHeight(self, locator):
        return int(self.selenium.get_element_height(locator))

    @assert_type('locator_pattern')
    @passthrough
    def getExpression(self, expression):
        pass

    @passthrough
    def isTextPresent(self, pattern):
        pass

    @assert_type('pattern')
    @passthrough
    def getLocation(self):
        pass

    # Assertions

    def assertTextPresent(self, pattern):
        if not self.isTextPresent(pattern):
            raise self.failureException('Text %r not present' % pattern)

    def assertCondition(self, condition):
        # XXX comparing to `true` on a string-exact match might not be a good
        # idea as implicit bool conversion might happen in original Selenese.
        return self.assertEval(condition, 'exact:true')

    def assertXpathCount(self, xpath, count):
        result = self.selenium.get_xpath_count(xpath)
        if int(result) != int(count):
            raise self.failureException(
                'Actual count of XPath %r is %s, expected %s'
                % (xpath, result, count))

    def assertOrdered(self, locator1, locator2):
        if not self.selenium.is_ordered(locator1, locator2):
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

    # Internal

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
        except self.failureException:
            return
        else:
            raise self.failureException(
                'Failed: ' + self._call_repr(name, *args, **kw))

    def _waitFor(self, assertion, *args, **kw):
        start = time.time()
        while True:
            try:
                assertion(*args, **kw)
            except self.failureException, e:
                if time.time() - start > self.timeout:
                    raise self.failureException(
                        'Timed out. %s' % e.args[0])
            else:
                break
            time.sleep(0.1)

    def _call_repr(self, name, *args, **kw):
        return '%s(%s)' % (
            name,
            ', '.join(map(repr, args) +
                      ['%s=%r' % item for item in sorted(kw.items())]))


def match_glob(text, pattern):
    pattern = re.escape(pattern)
    pattern = pattern.replace(r'\*', '.*')
    pattern = pattern.replace(r'\?', '.')
    pattern = '^%s$' % pattern
    return match_regex(text, pattern)


def match_regex(text, pattern):
    return re.search(pattern, text, re.DOTALL)


match_regexp = match_regex


def match_exact(text, pattern):
    return text == pattern


def selenese_pattern_equals(text, pattern):
    """Various Pattern syntaxes are available for matching string values:

    * glob:pattern: Match a string against a "glob" (aka "wildmat") pattern.
      "Glob" is a kind of limited regular-expression syntax typically used in
      command-line shells. In a glob pattern, "*" represents any sequence of
      characters, and "?" represents any single character. Glob patterns match
      against the entire string.
    * regexp:regexp: Match a string using a regular-expression. The full power
      of python regular-expressions is available.
    * exact:string: Match a string exactly, verbatim, without any of that fancy
      wildcard stuff.

      If no pattern prefix is specified, assume that it's a "glob"
      pattern.
    """
    matcher = match_glob
    if ':' in pattern:
        prefix, remainder = pattern.split(':', 1)
        try:
            matcher = globals()['match_' + prefix]
            pattern = remainder
        except KeyError:
            pass
    return matcher(text, pattern)


def abbrev_repr(x, size=70):
    r = repr(x)
    if len(r) > size:
        r = r[:size-3] + '...'
    return r
