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

    def __init__(self, selenium, testcase):
        self.selenium = selenium
        self.failureException = testcase.failureException
        self.testcase = testcase
        self.timeout = 30
        self.variables = {}

    @property
    def server(self):
        # we expect the testcase to have a gocept.selenium.layer.SeleniumLayer
        return '%s:%s' % (self.testcase.layer.host, self.testcase.layer.port)

    # Actions

    def pause(self, milliseconds):
        time.sleep(milliseconds / 1000)

    def setTimeout(self, timeout):
        self.timeout = timeout / 1000.0

    def waitForPageToLoad(self):
        self.selenium.wait_for_page_to_load(self.timeout * 1000)

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
    def altKeyDown(self):
        pass

    @passthrough
    def altKeyUp(self):
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
    def chooseCancelOnNextConfirmation(self):
        pass

    @passthrough
    def controlKeyDown(self):
        pass

    @passthrough
    def controlKeyUp(self):
        pass

    @passthrough
    def fireEvent(self, locator, eventName):
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
    def mouseDownAt(self, locator, coord):
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
    def mouseUpAt(self, locator, coord):
        pass

    @passthrough
    def refresh(self):
        pass

    @passthrough
    def select(self):
        pass

    @passthrough
    def selectFrame(self):
        pass

    @passthrough
    def setSpeed(self):
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

    # Getter

    @assert_type('pattern')
    def getAlert(self):
        if not self.selenium.is_alert_present():
            raise self.failureException(
                'No alert occured.')
        return self.selenium.get_alert()

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
    @passthrough
    def getConfirmation(self):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getEval(self, script):
        # Note: we use the locator_pattern because the script acts like a
        # locator: we pass it through and Selenium returns a result we can
        # compare with the pattern.
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getSelectedLabel(self, locator):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getText(self, locator):
        pass

    @assert_type('locator_pattern')
    @passthrough
    def getValue(self, locator):
        pass

    @assert_type(None)
    @passthrough
    def isAlertPresent(self):
        pass

    @assert_type('locator')
    @passthrough
    def isElementPresent(self, locator):
        pass

    @assert_type('locator')
    @passthrough
    def isVisible(self, locator):
        pass

    def getElementWidth(self, locator):
        return int(self.selenium.get_element_width(locator))

    def getElementHeight(self, locator):
        return int(self.selenium.get_element_height(locator))

    @passthrough
    def isTextPresent(self, pattern):
        pass

    @passthrough
    def getLocation(self):
        pass

    # Assertions

    def assertTextPresent(self, pattern):
        if not self.isTextPresent(pattern):
            raise self.failureException('Text %r not present' % pattern)

    def assertCondition(self, condition):
        # Extension to selenese API to make automatic `waitForCondition`
        # generation work
        # XXX comparing to `true` on a string-exact match might not be a good
        # idea as implicit bool conversion might happen in original Selenese.
        return self.assertEval(condition, 'exact:true')

    def assertXpathCount(self, xpath, count):
        result = self.selenium.get_xpath_count(xpath)
        if result != count:
            raise self.failureException(
                'Actual count of XPath %r is %s, expected %s'
                % (xpath, result, count))

    def assertOrdered(self, locator1, locator2):
        if not self.selenium.is_ordered(locator1, locator2):
            raise self.failureException(
                'Element order did not match expected %r,%r'
                % (locator1, locator2))

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
    return re.search(pattern, text)


def match_exact(text, pattern):
    return text == pattern


def selenese_pattern_equals(text, pattern):
    """Various Pattern syntaxes are available for matching string values:

    * glob:pattern: Match a string against a"glob" (aka "wildmat") pattern.
      "Glob" is a kind of limited regular-expression syntax typically used in
      command-line shells. In a glob pattern, "*" represents any sequence of
      characters, and "?" represents any single character. Glob patterns match
      against the entire string.
    * regexp:regexp: Match a string using a regular-expression. The full power
      of python regular-expressions is available.
    * exact:string: Match a string exactly, verbatim, without any of that fancy
      wildcard stuff.

      If no pattern prefix is specified, assume that it's a"glob"
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
