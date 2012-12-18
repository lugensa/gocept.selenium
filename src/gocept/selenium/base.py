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

import atexit
import gocept.selenium.selenese
import httpagentparser
import os
import re
import selenium
import socket
import sys
import warnings

# Python 2.4 does not have access to absolute_import,
# and we can't rename gocept.selenium.plone to something that
# does not clash with plone.testing (since that would break our API).
# So we use this workaround which passes empty globals to __import__,
# so it can't determine where we are to do something relatively.
# Also, we have to pass a fromlist with an empty string to have __import__
# return the module we asked for instead of its parent. *sigh*
plonetesting = __import__('plone.testing', {}, {}, [''])

try:
    import distutils.versionpredicate
except ImportError:
    have_predicate = False
else:
    have_predicate = True


class Layer(plonetesting.Layer):

    # hostname and port of the Selenium RC server
    _server = os.environ.get('GOCEPT_SELENIUM_SERVER_HOST', 'localhost')
    _port = int(os.environ.get('GOCEPT_SELENIUM_SERVER_PORT', 4444))

    _browser = os.environ.get('GOCEPT_SELENIUM_BROWSER', '*firefox')

    def setUp(self):
        if 'http_address' not in self:
            raise KeyError("No base layer has set self['http_address']")
        self['seleniumrc'] = selenium.selenium(
            self._server, self._port, self._browser,
            'http://%s/' % self['http_address'])
        try:
            self['seleniumrc'].start()
        except socket.error, e:
            raise socket.error(
                'Failed to connect to Selenium RC server at %s:%s,'
                ' is it running? (%s)'
                % (self._server, self._port, e))
        atexit.register(self._stop_selenium)
        speed = os.environ.get('GOCEPT_SELENIUM_SPEED')
        if speed is not None:
            self['seleniumrc'].set_speed(speed)

    def _stop_selenium(self):
        # Only stop selenium if it is still active.
        if self['seleniumrc'].sessionId is not None:
            self['seleniumrc'].stop()

    def tearDown(self):
        self['seleniumrc'].stop()

    def testSetUp(self):
        # instantiate a fresh one per test run, so any configuration
        # (e.g. timeout) is reset
        self['selenium'] = gocept.selenium.selenese.Selenese(
            self['seleniumrc'], self['http_address'])

LAYER = Layer()


class IntegrationBase(object):

    # hostname and port of the local application.
    host = os.environ.get('GOCEPT_SELENIUM_APP_HOST', 'localhost')
    port = int(os.environ.get('GOCEPT_SELENIUM_APP_PORT', 0))

    def __init__(self, *args, **kw):
        kw['module'] = sys._getframe(1).f_globals['__name__']
        super(IntegrationBase, self).__init__(*args, **kw)
        self.SELENIUM_LAYER = Layer(
            name='IntegratedSeleniumLayer', bases=[self])

    def make_layer_name(self, bases):
        if bases:
            base = bases[0]
            name = '(%s.%s)' % (base.__module__, base.__name__)
        else:
            name = self.__class__.__name__
        return name

    def setUp(self):
        super(IntegrationBase, self).setUp()
        self.SELENIUM_LAYER.setUp()

    def tearDown(self):
        self.SELENIUM_LAYER.tearDown()
        super(IntegrationBase, self).tearDown()

    def testSetUp(self):
        super(IntegrationBase, self).testSetUp()
        self.SELENIUM_LAYER.testSetUp()
        self['selenium'] = self.SELENIUM_LAYER['selenium']

    def testTearDown(self):
        self.SELENIUM_LAYER.testTearDown()
        super(IntegrationBase, self).testTearDown()


TEST_METHOD_NAMES = ('_TestCase__testMethodName', '_testMethodName')


class TestCase(object):
    # the various flavours (ztk, zope2, grok, etc.) are supposed to provide
    # their own TestCase as needed, and mix this class in to get the
    # convenience functionality.
    #
    # Example:
    # some.flavour.TestCase(gocept.selenium.base.TestCase,
    #                       the.actual.base.TestCase):
    #     pass

    @property
    def selenium(self):
        return self.layer['selenium']

    def setUp(self):
        super(TestCase, self).setUp()
        for attr in TEST_METHOD_NAMES:
            method_name = getattr(self, attr, None)
            if method_name:
                break
        assert method_name
        self.selenium.setContext('%s.%s' % (self.__class__.__name__,
                                            method_name))


class skipUnlessBrowser(object):

    def __init__(self, name, version=None):
        self.required_name = name
        self.required_version = version

    def __call__(self, f):
        if isinstance(f, type):
            raise ValueError('%s cannot be used as class decorator' %
                             self.__class__.__name__)
        def test(test_case, *args, **kw):
            self.skip_unless_requirements_met(test_case)
            return f(test_case, *args, **kw)
        return test

    def skip_unless_requirements_met(self, test_case):
        agent = httpagentparser.detect(
            test_case.selenium.getEval('window.navigator.userAgent'))
        if re.match(self.required_name, agent['browser']['name']) is None:
            test_case.skipTest('Require browser %s, but have %s.' % (
                self.required_name, agent['browser']['name']))
        if self.required_version:
            if have_predicate:
                requirement = distutils.versionpredicate.VersionPredicate(
                    'Browser (%s)' % self.required_version)
                skip = not requirement.satisfied_by(
                    str(agent['browser']['version']))
            else:
                warnings.warn(
                    'distutils.versionpredicate not available, skipping.')
                skip = True
            if skip:
                test_case.skipTest('Require %s%s, got %s %s' % (
                    self.required_name, self.required_version,
                    agent['browser']['name'], agent['browser']['version']))
