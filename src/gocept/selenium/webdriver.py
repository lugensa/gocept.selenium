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

from selenium.common.exceptions import JavascriptException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import atexit
import gocept.selenium.wd_selenese
import os
import pathlib
import plone.testing
import selenium.webdriver
import sys
import tempfile
import warnings


class Layer(plone.testing.Layer):

    profile = None
    headless = False
    _browser = 'firefox'

    def setUp(self):
        if 'http_address' not in self:
            raise KeyError("No base layer has set self['http_address']")

        browser = os.environ.get('GOCEPT_WEBDRIVER_BROWSER')
        headless = os.environ.get('GOCEPT_SELENIUM_HEADLESS')

        if headless is None or headless.lower() not in ['true', 'false']:
            warnings.warn('GOCEPT_SELENIUM_HEADLESS invalid. \
                          Possible values are true and false. Got: %s.\
                          Falling back to default (false).' %
                          os.environ.get('GOCEPT_SELENIUM_HEADLESS'))
            headless = 'false'

        if headless.lower() == 'true':
            self.headless = True

        if browser is None or browser.lower() not in ['chrome', 'firefox']:
            warnings.warn('GOCEPT_WEBDRIVER_BROWSER invalid. \
                          Possible values are firefox and chrome. Got: %s.\
                          Falling back to firefox.' %
                          os.environ.get('GOCEPT_WEBDRIVER_BROWSER'))
            browser = 'firefox'

        if browser.lower() == 'chrome':
            self._browser = 'chrome'
        else:
            self.profile = FirefoxProfile(
                os.environ.get(
                    'GOCEPT_WEBDRIVER_FF_PROFILE',
                    os.environ.get('GOCEPT_SELENIUM_FF_PROFILE')))
            self.profile.native_events_enabled = True
            self.profile.update_preferences()
            # Save downloads always to disk into a predefined dir.
            self['selenium_download_dir'] = pathlib.Path(tempfile.mkdtemp(
                prefix='gocept.selenium.download-dir'))
            self.profile.set_preference("browser.download.folderList", 2)
            self.profile.set_preference(
                "browser.download.manager.showWhenStarting", False)
            self.profile.set_preference(
                "browser.download.dir", str(self['selenium_download_dir']))
            self.profile.set_preference(
                "browser.helperApps.neverAsk.saveToDisk", "application/pdf")
            self.profile.set_preference("pdfjs.disabled", True)

        self._start_selenium()
        atexit.register(self._stop_selenium)

    def tearDown(self):
        self._stop_selenium()
        self['selenium_download_dir'].rmdir()
        del self['selenium_download_dir']
        # XXX upstream bug, quit should reset session_id
        self['seleniumrc'].session_id = None
        del self['seleniumrc']

    def _start_selenium(self):
        if self._browser == 'firefox':
            options = selenium.webdriver.FirefoxOptions()

            if self.headless:
                options.add_argument('-headless')

            self['seleniumrc'] = selenium.webdriver.Firefox(
                firefox_profile=self.profile, options=options)

        if self._browser == 'chrome':
            options = selenium.webdriver.ChromeOptions()
            options.add_argument('--disable-dev-shm-usage')

            if self.headless:
                options.add_argument('--headless')
            else:
                raise NotImplementedError(
                    'Chromedriver currently only works headless.')

            self['seleniumrc'] = selenium.webdriver.Chrome(
                options=options,
                service_args=['--log-path=chromedriver.log'])

    def _stop_selenium(self):
        # Only stop selenium if it is still active.
        if (self.get('seleniumrc') is None or
                self['seleniumrc'].session_id is None):
            return

        # Quit also removes the tempdir the ff profile is copied in.
        self['seleniumrc'].quit()

    def testTearDown(self):
        try:
            self['seleniumrc'].execute_script('window.localStorage.clear()')
        except JavascriptException:
            # We can't do anything here, there might be no current_url
            pass
        for path in self['selenium_download_dir'].iterdir():
            path.unlink()


class WebdriverSeleneseLayer(plone.testing.Layer):

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


class IntegrationBase:

    # hostname and port of the local application.
    host = os.environ.get('GOCEPT_SELENIUM_APP_HOST', 'localhost')
    port = int(os.environ.get('GOCEPT_SELENIUM_APP_PORT', 0))

    def __init__(self, *args, **kw):
        kw['module'] = sys._getframe(1).f_globals['__name__']
        super().__init__(*args, **kw)
        self.SELENIUM_LAYER = Layer(
            name='IntegratedSeleniumLayer', bases=[self])
        self.SELENESE_LAYER = WebdriverSeleneseLayer(
            name='IntegratedSeleneseLayer', bases=[self.SELENIUM_LAYER])

    def make_layer_name(self, bases):
        if bases:
            base = bases[0]
            name = f'({base.__module__}.{base.__name__})'
        else:
            name = self.__class__.__name__
        return name

    def setUp(self):
        super().setUp()
        self.SELENIUM_LAYER.setUp()
        self.SELENESE_LAYER.setUp()
        self['seleniumrc'] = self.SELENIUM_LAYER['seleniumrc']

    def tearDown(self):
        self.SELENESE_LAYER.tearDown()
        self.SELENIUM_LAYER.tearDown()
        del self['seleniumrc']
        super().tearDown()

    def testSetUp(self):
        super().testSetUp()
        self.SELENIUM_LAYER.testSetUp()
        self.SELENESE_LAYER.testSetUp()
        self['selenium'] = self.SELENESE_LAYER['selenium']

    def testTearDown(self):
        self.SELENESE_LAYER.testTearDown()
        self.SELENIUM_LAYER.testTearDown()
        super().testTearDown()


class WebdriverSeleneseTestCase:

    @property
    def selenium(self):
        return self.layer['selenium']
