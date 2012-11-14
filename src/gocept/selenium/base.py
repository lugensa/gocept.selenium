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
import os.path
import re
import selenium.webdriver
import shutil
import tempfile
import urllib2
import warnings


try:
    import distutils.versionpredicate
except ImportError:
    have_predicate = False
else:
    have_predicate = True


class Layer(object):

    # hostname and port of the Selenium RC server
    _server = os.environ.get('GOCEPT_SELENIUM_SERVER_HOST', 'localhost')
    _port = int(os.environ.get('GOCEPT_SELENIUM_SERVER_PORT', 4444))

    _browser = os.environ.get('GOCEPT_SELENIUM_BROWSER', 'firefox')

    # hostname and port of the local application.
    host = os.environ.get('GOCEPT_SELENIUM_APP_HOST', 'localhost')
    port = int(os.environ.get('GOCEPT_SELENIUM_APP_PORT', 0))

    def __init__(self, *bases):
        self.__bases__ = bases
        if self.__bases__:
            base = bases[0]
            self.__name__ = '(%s.%s)' % (base.__module__, base.__name__)
        else:
            self.__name__ = self.__class__.__name__

    def _stop_selenium(self):
        # Only stop selenium if it is still active.
        if self.seleniumrc.session_id is None:
            return

        self.seleniumrc.quit()

        shutil.rmtree(self.profile.profile_dir)
        if os.path.dirname(self.profile.profile_dir) != tempfile.gettempdir():
            try:
                os.rmdir(os.path.dirname(self.profile.profile_dir))
            except OSError:
                pass

        if not os.environ.get('GOCEPT_SELENIUM_KEEP_NATIVE_FF_EVENTS_LOG'):
            native_ff_events_log = os.path.join(
                tempfile.gettempdir(), 'native_ff_events_log')
            try:
                os.unlink(native_ff_events_log)
            except OSError:
                pass

    def setUp(self):
        self.profile = selenium.webdriver.firefox.firefox_profile.\
            FirefoxProfile(os.environ.get('GOCEPT_SELENIUM_FF_PROFILE'))
        self.profile.native_events_enabled = True
        self.profile.update_preferences()
        try:
            self.seleniumrc = selenium.webdriver.Remote(
                'http://%s:%s/wd/hub' % (self._server, self._port),
                desired_capabilities=dict(browserName=self._browser),
                browser_profile=self.profile)
        except urllib2.URLError, e:
            raise urllib2.URLError(
                'Failed to connect to Selenium server at %s:%s,'
                ' is it running? (%s)'
                % (self._server, self._port, e))
        atexit.register(self._stop_selenium)
        speed = os.environ.get('GOCEPT_SELENIUM_SPEED')
        if speed is not None:
            self.seleniumrc.setSpeed(speed)

    def tearDown(self):
        self._stop_selenium()
        # XXX upstream bug, quit should reset session_id
        self.seleniumrc.session_id = None

    def testSetUp(self):
        # instantiate a fresh one per test run, so any configuration
        # (e.g. timeout) is reset
        self.selenium = gocept.selenium.selenese.Selenese(
            self.seleniumrc, self.host, self.port)


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
        return self.layer.selenium


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
        # XXX getEval dumps the user agent string returned by Webdriver to
        # JSON which adds quotes at both ends, which we need to remove here.
        user_agent_string = test_case.selenium.getEval(
            'window.navigator.userAgent')[1:-1]
        agent = httpagentparser.detect(user_agent_string)
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
