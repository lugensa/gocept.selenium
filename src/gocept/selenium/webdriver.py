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
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import atexit
import gocept.selenium.wd_selenese
import os
import pathlib
import plone.testing
import selenium.webdriver
import selenium.webdriver.edge.options
import sys
import tempfile
import warnings


class Layer(plone.testing.Layer):

    profile = None
    _default_headless = False
    _default_browser = 'firefox'
    _supported_browsers = ('chrome', 'edge', 'firefox')

    def setUp(self):
        if 'http_address' not in self:
            raise KeyError("No base layer has set self['http_address']")

        browser = os.environ.get('GOCEPT_WEBDRIVER_BROWSER', '').lower()
        headless = os.environ.get('GOCEPT_SELENIUM_HEADLESS', '').lower()

        if headless not in {'true', 'false'}:
            warnings.warn(
                "The environment variable 'GOCEPT_SELENIUM_HEADLESS' has an"
                " invalid value. Allowed values are 'true' and 'false'."
                f" Got: {os.environ.get('GOCEPT_SELENIUM_HEADLESS')!r}."
                " Falling back to default ('false').")
            headless = 'false'

        self['headless'] = (headless == 'true')

        if browser not in self._supported_browsers:
            warnings.warn(
                "The environment variable 'GOCEPT_WEBDRIVER_BROWSER' has an "
                "invalid value. Possible values are:"
                f" {self._supported_browsers}."
                f" Got: {os.environ.get('GOCEPT_WEBDRIVER_BROWSER')!r}."
                " Falling back to 'firefox'.")
            browser = 'firefox'

        if browser in self._supported_browsers:
            self['browser'] = browser
        else:
            self['browser'] = self._default_browser

        # Setup download dir.
        self['selenium_download_dir'] = pathlib.Path(tempfile.mkdtemp(
            prefix='gocept.selenium.download-dir'))

        self._start_selenium()
        atexit.register(self._stop_selenium)

    def tearDown(self):
        self._stop_selenium()
        self['selenium_download_dir'].rmdir()
        del self['selenium_download_dir']
        # XXX upstream bug, quit should reset session_id
        self['seleniumrc'].session_id = None
        del self['seleniumrc']
        del self['browser']
        del self['headless']

    def get_firefox_webdriver_args(self):
        options = selenium.webdriver.FirefoxOptions()

        if self['headless']:
            options.add_argument('-headless')

        profile_path = os.environ.get(
            'GOCEPT_WEBDRIVER_FF_PROFILE',
            os.environ.get('GOCEPT_SELENIUM_FF_PROFILE'))
        if profile_path:
            options.set_preference('profile', profile_path)

        # Save downloads always to disk into a predefined dir.
        options.set_preference("browser.download.folderList", 2)
        options.set_preference(
            "browser.download.manager.showWhenStarting", False)
        options.set_preference(
            "browser.download.dir", str(self['selenium_download_dir']))
        options.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        options.set_preference("pdfjs.disabled", True)

        return {'options': options,
                'service': FirefoxService(GeckoDriverManager().install())}

    def get_edge_webdriver_args(self):
        options = selenium.webdriver.edge.options.Options()
        if self['headless']:
            options.add_argument('headless')

        return {'options': options,
                'service': EdgeService(EdgeChromiumDriverManager().install())}

    def get_chrome_webdriver_args(self):
        options = selenium.webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')

        if self['headless']:
            options.add_argument('--headless')

        # Save downloads always to disk into a predefined dir.
        prefs = {
            'download.default_directory': str(self['selenium_download_dir']),
            'download.prompt_for_download': False,
        }

        options.add_experimental_option('prefs', prefs)

        mobile_emulation = {
            'deviceMetrics': {
                'pixelRatio': 1.0,
                'width': 1600,
                'height': 1200,
            }
        }

        options.add_experimental_option('mobileEmulation', mobile_emulation)

        return {
            'options': options,
            'service_args': ['--log-path=chromedriver.log'],
            'service': ChromeService(ChromeDriverManager().install()),
        }

    def _start_selenium(self):
        if self['browser'] == 'firefox':
            self['seleniumrc'] = selenium.webdriver.Firefox(
                **self.get_firefox_webdriver_args(),
            )

        if self['browser'] == 'chrome':
            self['seleniumrc'] = selenium.webdriver.Chrome(
                **self.get_chrome_webdriver_args(),
            )
        if self['browser'] == 'edge':
            self['seleniumrc'] = selenium.webdriver.Edge(
                **self.get_edge_webdriver_args(),
            )

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
        except (JavascriptException, WebDriverException):
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
