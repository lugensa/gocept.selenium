import gocept.selenium.webdriver
import os
import pytest
import unittest


class LayerTest(unittest.TestCase):

    def test_http_server_not_there(self):
        layer = gocept.selenium.webdriver.Layer()

        with pytest.raises(KeyError) as err:
            layer.setUp()
        assert "No base layer has set self['http_address']" in str(err.value)

    def test_stop_selenium_two_times(self):
        layer = gocept.selenium.webdriver.Layer()
        layer['http_address'] = 'localhost:34234'
        layer.setUp()
        layer.tearDown()
        layer._stop_selenium()

    def test_wrong_browser_warning(self):
        _environ = dict(os.environ)

        try:
            os.environ['GOCEPT_WEBDRIVER_BROWSER'] = 'sfsdfsd'
            with pytest.warns(UserWarning) as warning:
                layer = gocept.selenium.webdriver.Layer()
                layer['http_address'] = 'localhost:34234'
                layer.setUp()
            assert 'GOCEPT_WEBDRIVER_BROWSER invalid.' in str(
                warning[0].message)
        finally:
            layer.tearDown()
            os.environ.clear()
            os.environ.update(_environ)

    def test_wrong_browser_warning_2(self):
        """It raises a warning if no environment variable was set."""
        _environ = dict(os.environ)

        try:
            del os.environ['GOCEPT_WEBDRIVER_BROWSER']
            with pytest.warns(UserWarning) as warning:
                layer = gocept.selenium.webdriver.Layer()
                layer['http_address'] = 'localhost:34234'
                layer.setUp()
            assert 'GOCEPT_WEBDRIVER_BROWSER invalid.' in str(
                warning[0].message)
        finally:
            layer.tearDown()
            os.environ.clear()
            os.environ.update(_environ)

    @pytest.mark.skipif(
        os.environ.get('GOCEPT_WEBDRIVER_BROWSER').lower() == 'chrome',
        reason='This configuration raises not implemented')
    @pytest.mark.skipif(
        os.environ.get('GOCEPT_SELENIUM_HEADLESS').lower() == 'true',
        reason='Headless tests don\'t support this part. See test_chrome_head')
    def test_wrong_headless_warning(self):
        _environ = dict(os.environ)
        try:
            os.environ['GOCEPT_SELENIUM_HEADLESS'] = 'fasdfasdf'
            with pytest.warns(UserWarning) as warning:
                layer = gocept.selenium.webdriver.Layer()
                layer['http_address'] = 'localhost:34234'
                layer.setUp()

            assert 'GOCEPT_SELENIUM_HEADLESS invalid.' in str(
                warning[0].message)
        finally:
            layer.tearDown()
            os.environ.clear()
            os.environ.update(_environ)

    @pytest.mark.skipif(
        os.environ.get('GOCEPT_WEBDRIVER_BROWSER').lower() == 'chrome',
        reason='This configuration raises not implemented')
    @pytest.mark.skipif(
        os.environ.get('GOCEPT_SELENIUM_HEADLESS').lower() == 'true',
        reason='Headless tests don\'t support this part. See test_chrome_head')
    def test_wrong_headless_warning_2(self):
        """It raises a warning if no environment variable was set."""
        _environ = dict(os.environ)
        try:
            del os.environ['GOCEPT_SELENIUM_HEADLESS']
            with pytest.warns(UserWarning) as warning:
                layer = gocept.selenium.webdriver.Layer()
                layer['http_address'] = 'localhost:34234'
                layer.setUp()

            assert 'GOCEPT_SELENIUM_HEADLESS invalid.' in str(
                warning[0].message)
        finally:
            layer.tearDown()
            os.environ.clear()
            os.environ.update(_environ)

    def test_chrome_head(self):
        _environ = dict(os.environ)
        if os.environ.get('GOCEPT_WEBDRIVER_BROWSER').lower() != 'chrome':
            pytest.skip('This test is for chrome only')

        try:
            os.environ['GOCEPT_SELENIUM_HEADLESS'] = 'false'
            with pytest.raises(NotImplementedError) as err:
                layer = gocept.selenium.webdriver.Layer()
                layer['http_address'] = 'localhost:34234'
                layer.setUp()
            assert 'Chromedriver currently only works headless.' in str(
                err.value)
        finally:
            os.environ.clear()
            os.environ.update(_environ)
