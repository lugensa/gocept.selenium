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

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import ast
import atexit
import gocept.selenium.wd_selenese
import os
import os.path
import selenium.webdriver
import shutil
import tempfile
import urllib2


# work around Python 2.4 lack of absolute_import,
# see gocept.selenium.seleniumrc for details
plonetesting = __import__('plone.testing', {}, {}, [''])


class Layer(plonetesting.Layer):

    # hostname and port of the Selenium RC server
    _server = os.environ.get('GOCEPT_SELENIUM_SERVER_HOST', 'localhost')
    _port = int(os.environ.get('GOCEPT_SELENIUM_SERVER_PORT', 4444))

    _browser = os.environ.get('GOCEPT_WEBDRIVER_BROWSER', 'firefox')

    @property
    def is_remote(self):
        return ast.literal_eval(
            os.environ.get('GOCEPT_WEBDRIVER_REMOTE', 'True'))

    def setUp(self):
        if 'http_address' not in self:
            raise KeyError("No base layer has set self['http_address']")

        if self._browser.lower() == 'firefox':
            self.profile = FirefoxProfile(
                os.environ.get(
                    'GOCEPT_WEBDRIVER_FF_PROFILE',
                    os.environ.get('GOCEPT_SELENIUM_FF_PROFILE')))
            self.profile.native_events_enabled = True
            self.profile.update_preferences()
        else:
            self.profile = None

        if self.is_remote:
            self._start_remote()
        else:
            self._start_local()
        atexit.register(self._stop_selenium)
        speed = os.environ.get('GOCEPT_SELENIUM_SPEED')
        if speed is not None:
            self['seleniumrc'].setSpeed(speed)

    def tearDown(self):
        self._stop_selenium()
        # XXX upstream bug, quit should reset session_id
        self['seleniumrc'].session_id = None
        del self['seleniumrc']

    def _start_local(self):
        parameters = {}
        if self.profile:
            parameters['firefox_profile'] = self.profile
        ff_binary = os.environ.get('GOCEPT_WEBDRIVER_FF_BINARY')
        if ff_binary:
            parameters['firefox_binary'] = FirefoxBinary(ff_binary)
        module = getattr(selenium.webdriver, self._browser)
        self['seleniumrc'] = module.webdriver.WebDriver(**parameters)

    def _start_remote(self):
        parameters = {'desired_capabilities': {'browserName': self._browser}}
        ff_binary = os.environ.get('GOCEPT_WEBDRIVER_FF_BINARY')
        if ff_binary:
            parameters['desired_capabilities']['firefox_binary'] = ff_binary
        if self.profile:
            parameters['browser_profile'] = self.profile

        try:
            self['seleniumrc'] = selenium.webdriver.Remote(
                'http://%s:%s/wd/hub' % (self._server, self._port),
                **parameters)
        except urllib2.URLError, e:
            raise urllib2.URLError(
                'Failed to connect to Selenium server at %s:%s,'
                ' is it running? (%s)'
                % (self._server, self._port, e))

    def _stop_selenium(self):
        # Only stop selenium if it is still active.
        if (self.get('seleniumrc') is None or
                self['seleniumrc'].session_id is None):
            return

        self['seleniumrc'].quit()

        if self.profile and os.path.exists(self.profile.profile_dir):
            shutil.rmtree(self.profile.profile_dir)
            if os.path.dirname(
                    self.profile.profile_dir) != tempfile.gettempdir():
                try:
                    os.rmdir(os.path.dirname(self.profile.profile_dir))
                except OSError:
                    pass

            if not os.environ.get('GOCEPT_SELENIUM_KEEP_NATIVE_FF_EVENTS_LOG'):
                native_ff_events_log = os.path.join(
                    tempfile.gettempdir(), 'native_ff_events_log')
                try:
                    os.remove(native_ff_events_log)
                except OSError:
                    pass


class WebdriverSeleneseLayer(plonetesting.Layer):

    _timeout = int(os.environ.get('GOCEPT_SELENIUM_TIMEOUT', 30))

    def setUp(self):
        self['selenium'] = gocept.selenium.wd_selenese.Selenese(
            self['seleniumrc'], self['http_address'], self._timeout)

    def testSetUp(self):
        # BBB reset settings
        self['selenium'].setTimeout(self._timeout * 1000)
        class_ = gocept.selenium.wd_selenese.Selenese
        for name in ['screenshot_directory', 'capture_screenshot']:
            setattr(self['selenium'], name, getattr(class_, name))

    def tearDown(self):
        del self['selenium']


class WebdriverSeleneseTestCase(object):

    @property
    def selenium(self):
        return self.layer['selenium']
